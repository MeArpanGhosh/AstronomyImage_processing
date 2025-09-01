# AstronomyImage_processing using IRAF/PyRAF

# 1.3m Devasthal Fast Optical Telescope Image Cleaning Pipeline

An automated Python pipeline for cleaning and processing raw astronomical images from 1.3m Devasthal Fast Optical Telescope using IRAF/PyRAF. This tool performs bias subtraction, flat field correction, image alignment, and stacking to produce science-ready astronomical images.

## Features

- **Bias Subtraction**: Removes electronic noise using master bias frames
- **Flat Field Correction**: Corrects for pixel sensitivity variations and vignetting
- **Interactive Image Alignment**: User-guided star selection for precise image registration
- **Image Stacking**: Combines aligned frames to improve signal-to-noise ratio
- **Multi-filter Support**: Processes images across multiple photometric bands
- **CCD-specific Parameters**: Optimized for 512 and 2k CCD configurations

## Prerequisites

### Software Requirements
- Python 2.7 (required for PyRAF compatibility)
- IRAF (Image Reduction and Analysis Facility)
- PyRAF
- NumPy
- DS9 (SAOImage DS9 for interactive image display)
- A Unix/Linux environment

### System Requirements
- Linux/Unix operating system
- DS9 image viewer installed and accessible from command line
- Sufficient disk space (approximately 3x the size of raw data)
- Text editor (vi/vim) for coordinate file editing

## Installation

### 1. Install IRAF and PyRAF
```bash
# Install IRAF (follow official documentation for your system)
# For Ubuntu/Debian:
sudo apt-get install iraf

# Install PyRAF
pip install pyraf numpy
```

### 2. Install DS9
```bash
# Ubuntu/Debian
sudo apt-get install saods9

# Or download from: http://ds9.si.edu/site/Download.html
```

### 3. Download the Script
```bash
# Clone or download the script
wget [your-repository-url]/1_3m_cleaning.py
```

## Required Calibration Files

Before running the pipeline, ensure you have the following calibration files in your working directory:

### Master Bias Frame
- **Filename**: `mbias.fits`
- **Description**: Combined bias frame created from multiple bias exposures

### Normalized Flat Field Frames
- **Filename format**: `normflat_[filtername].fits`
- **Examples**: 
  - `normflat_v.fits` (V-band)
  - `normflat_b.fits` (B-band)
  - `normflat_r.fits` (R-band)

### Login File
- **Filename**: `login.cl`
- **Description**: IRAF login configuration file (should be in the same directory as the script)

## Usage

### 1. Run the Pipeline
```bash
python 1_3m_cleaning.py
```

### 2. Interactive Setup
The script will prompt you for:

1. **Raw images directory**: Full path to your raw FITS files
2. **Number of filters**: How many photometric bands you observed
3. **Filter names**: Enter each filter name in lowercase (e.g., 'v', 'b', 'r', 'i')
4. **Target prefix**: Initial characters of your target image filenames
5. **Flat field selection**: Choose appropriate normalized flat for each band
6. **Reference image**: Select the image to use as alignment reference
7. **CCD type**: Choose between 512 CCD or 2k CCD
8. **Observation date**: Date for output filename generation

### 3. Interactive Alignment Process

The pipeline includes an interactive alignment step:

1. **DS9 will open** displaying your processed images
2. **Star selection**: Press `,` (comma) on stars visible in all frames
3. **Exit DS9**: Press `q` when finished selecting stars
4. **Reference coordinates**: DS9 will reload with reference image
5. **Select reference stars**: Press `,` on the same stars in reference image
6. **Edit coordinate files**: Vi editor will open for manual cleanup of coordinate logs

## Processing Steps

The pipeline follows this workflow:

1. **Image Copying**: Extracts first extension from multi-extension FITS files
2. **Bias Subtraction**: Subtracts master bias from all target images
3. **Flat Field Correction**: Divides by normalized flat fields for each filter
4. **Interactive Alignment**: 
   - User selects common stars across all frames
   - Calculates shift parameters relative to reference image
   - Applies geometric transformations
5. **Image Combination**: Averages aligned frames for each filter
6. **Final Output**: Creates science-ready images with standardized naming

## File Naming Convention

### During Processing
- **Original**: `target*.fits`
- **Bias subtracted**: `btarget*.fits` 
- **Flat corrected**: `fbtarget*.fits`
- **Aligned**: `afbtarget*.fits`

### Final Output
- **Format**: `[date][target]_[filter].fits`
- **Example**: `20241201NGC1234_v.fits`

## Generated Files

The pipeline creates several intermediate files:
- `bias_sub.lst`: List of files for bias subtraction
- `[filter]flat.lst`: Lists for each filter's flat correction
- `obj.lst`: List of objects for alignment
- `coord.log`: Coordinates of selected stars
- `ref.log`: Reference image coordinates
- `shift.log`: Calculated shift parameters

## CCD Parameters

The script automatically configures CCD-specific parameters:

### 512 CCD
- **Read Noise**: 6.1 e⁻
- **Gain**: 1.4 e⁻/ADU

### 2k CCD  
- **Read Noise**: 8.4 e⁻
- **Gain**: 2.25 e⁻/ADU

## Example Workflow

```bash
# 1. Prepare your directory structure
/data/
├── raw_images/
│   ├── target001_v.fits
│   ├── target002_v.fits
│   └── ...
├── mbias.fits
├── normflat_v.fits
├── normflat_b.fits
└── login.cl

# 2. Run the pipeline
python 1_3m_cleaning.py

# 3. Follow prompts:
# - Enter path: /data/raw_images/
# - Number of filters: 2
# - Filter names: v, b
# - Target prefix: target
# - Select flats and reference image
# - Choose CCD type and date
```

## Troubleshooting

### Common Issues

**"Cannot find mbias.fits"**
```
Solution: Ensure master bias frame is named exactly "mbias.fits" in working directory
```

**"No normalized flat found"**
```
Solution: Rename flat fields to format "normflat_[filter].fits"
```

**"DS9 won't open"**
```
Solution: Ensure DS9 is installed and accessible from command line
Check: which ds9
```

**"Coordinate selection issues"**
```
Solution: 
- Select bright, isolated stars present in all frames
- Avoid saturated or blended stars
- Select at least 3-4 stars for robust alignment
```

**"Vi editor difficulties"**
```
Solution: In vi editor:
- Delete unwanted lines with 'dd'
- Keep only coordinate number pairs
- Save and exit with ':wq'
```

### Performance Tips

- Use a fast disk for processing (SSD recommended)
- Ensure sufficient free space (3x raw data size)
- Select well-distributed stars across the field for alignment
- Use the sharpest, highest S/N image as reference

## Output Quality Check

After processing, verify:
- Final images have consistent backgrounds
- Stars appear sharp and round
- No obvious alignment residuals
- Photometric zero-points are stable across frames

## File Cleanup

The script automatically removes:
- `login.cl` (copied IRAF configuration)
- Intermediate processing files can be manually deleted if disk space is limited

## Limitations

- Requires Python 2.7 (PyRAF dependency)
- Manual star selection process (not automated)
- Limited to linear geometric transformations
- Assumes simple image alignment (no field rotation/distortion correction)

## Support

For issues related to:
- **IRAF/PyRAF**: Consult IRAF documentation
- **DS9 problems**: Check DS9 installation and X11 forwarding
- **Script errors**: Ensure all calibration files are present and properly named

## Citation

If you use this pipeline in your research, please acknowledge:
```
"Image processing was performed using a custom Python/IRAF pipeline 
for 1.3m Devasthal Fast Optical Telescope data reduction."
```

## License

This code is provided as-is for astronomical research purposes. Please cite appropriately if used in publications.

## Contributing

Improvements and bug fixes are welcome. Consider:
- Adding automated star detection
- Python 3 compatibility
- Error handling improvements
- Support for additional CCD types
