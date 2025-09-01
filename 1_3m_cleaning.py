import numpy as np
from pyraf import iraf
import subprocess
import glob
import time
import os
import sys
import shutil

s=raw_input("\n Enter the full path to the desired directory where the raw images are kept:\t")
dir=s
shutil.copy('login.cl',dir)
print '\n\n###########################################################################################################################################'
print '\n Make sure that the bias frames and the respective normalised flat frames are present in the current directory.Your bias frame should have name like "mbias.fits" and normalised flat frames be like "normflat_(filtername).fits" else rename them accordingly.'
print '\n\n###########################################################################################################################################'
a=raw_input('\n\n\n Press p to proceed further:\t')

if (a == 'p'):
        iraf.cd(dir)  #changing to the destination directory
        subprocess.call("rm -f *.lst",shell=True)
        n=int(input('\n Enter the number of filters in which you have observed:\t'))
        band=[]

        for i in range (0,n):
                s=str(raw_input('Enter the band name in lower:\t'))
                band.append(s)
	iraf.imcopy(input='*.fits[*,*,1]', output='*.fits[*,*]')
	
	target=raw_input('\nEnter the initials of the filenames of the target:\t')
	str1=target+'*fits'
	lst=glob.glob(str1)
	lst.sort()
	f=open('bias_sub.lst','w')
	for i in lst:
		f.write("%s\n"%(i))
	f.close()

        op1='@'+'bias_sub.lst'
        res='b//'+op1
        iraf.imarith(operand1=op1,op='-',operand2='mbias.fits',result=res)

	print "\n\nBias substraction is complete. Original files target files will be pre-appended with 'b' to denote bias substraction.\n\n"

	for i in range (0,n) :
		str2='b'+target+'*'+band[i]+'*fits'
		lst=glob.glob(str2)
		lst.sort()
		filename=band[i]+'flat.lst'
		f=open(filename,'w')
		for j in lst :
			f.write("%s\n"%(j))
		f.close()
		print 'For %s band\t'%(band[i])
		op2=raw_input('enter the normalised flat frame you want:\t')
		#Creating the flat corrected FITS files from the list
		in_s='@'+band[i]+'flat.lst'
		out_s='f//'+in_s
		iraf.imarith(operand1=in_s,op='/',operand2=op2,result=out_s)
		time.sleep(1)

	print "\n\nFlat correction is complete. Bias subtracted files are pre-appended with 'f' to denote flat correction."

	lst=glob.glob('fb*fits')
        lst.sort()
        f=open('obj.lst','w')
        for i in lst:
                f.write("%s\n"%(i))
        f.close()

	print '\n\n*********************************************************************************'
        print '\nImages in %d frames are aligned now'%(n)
        print '\n\n**********************************************************************************\n\n'

        print 'ds9 will open with the list of files to be aligned loaded. \nPress "," on top of a star which is present in all the frames.\tPress "q"    to quit when finished.'

        subprocess.Popen('ds9')
        time.sleep(3)  # Give 3 seconds for ds9 to startup

        iname='@'+'obj.lst'
        iraf.imexa(iname,logfile='coord.log',keeplog='yes')

       #reference coordinate file is created below
        ref=raw_input('Enter reference image filename. With this image frame all the list of files will be aligned:\t')
        print '\nAt ds9 the reference image will load. Press "," on top of few stars and then press "q" to quit when finished.'
        time.sleep(2)
        iraf.imexa(ref,logfile='ref.log',keeplog='yes')

        print '\nvim editor will open the coord.log and ref.log files successively delete all entries keeping only the coordinate entries. Press ":wq  " each time when you have deleted all the entries except the coordinate information to save and exit.'

        subprocess.call("vi coord.log ",shell=True)
        subprocess.call("vi ref.log ",shell=True)
        ref_pos=0
	for m in range (0,len(lst)) :
        	if (lst[m] == ref) :
			 ref_pos= m

       #shifts are calculated below
        d1,d2=np.loadtxt("coord.log",dtype='float',unpack='True',usecols=[0,1])
        s1,s2=[],[]
        t=open("shift.log",'w')
        for i in range (0,len(d1)):
                s1.append(-(d1[i]-d1[ref_pos]))
                s2.append(-(d2[i]-d2[ref_pos]))
                t.write("%2.6f\t%2.6f\n"%(s1[i],s2[i]))
        t.close()
	iraf.imalign(input=iname,referenc=ref,coords='ref.log',output='a//@obj.lst',shifts='shift.log',trimima='yes')
       

	print "\n\nFrame alignment is done. Flat corrected frames are pre-appended with 'a' to specify alignment correction."

        ccd = int(raw_input('\n Enter "0" for 512 CCD or "1" for 2k CCD:\t'))
        rdnoise,gain = 8.4,2.25 
        if ccd == 0 :
          rdnoise,gain = 6.1,1.4
       
        #Final images in each band are created.	
        date = str(raw_input("\nEnter the date of observation:\t"))        

        for i in range (0,n):
		inp='afb'+target+'*'+band[i]+'*fits'
		out=date+target+'_'+band[i]+'.fits'
		iraf.imcombine(input=inp,output=out,combine='average',scale='none',rdnoise = rdnoise,gain=gain)
        os.remove("login.cl")

print "\n\n********************************************************************************************************************************************\n"
print "\n\n Images are succesfully cleaned and final target frames in each band are formed. Now you can proceed to do photometry on them.\n\t\t Enjoy\n\n"
print "********************************************************************************************************************************************\n"
