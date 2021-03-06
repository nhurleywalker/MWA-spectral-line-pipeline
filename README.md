# MWA-spectral-line-pipeline
A simple spectral line processing pipeline for the Murchison Widefield Array

This memo describes the overall goal, initial testing performed, and computational costs of the pipeline:
Fast_Targeted_Spectral_Line_Imaging_for_the_MWA.pdf

If you do not already have flagged and calibrated MWA data, you will also need to install the GLEAM-X-pipeline (https://github.com/nhurleywalker/GLEAM-X-pipeline) as it uses it for these steps. Review the documentation there for an overall description of how this pipeline is designed to run on Pawsey systems.

## Credits
Please credit Natasha Hurley-Walker if you use this code, or incorporate it into your own workflow. Please acknowledge the use of this code by citing this repository, and until I have a publication accepted on this work, I request that I be added as a co-author on papers that rely on this code.

The unique parts of this pipeline are described here:

### Wrapper scripts
Carry out the recommended steps of the spectral line processing to go from raw visibilities to continuum-subtracted fine-channel images
- spec_process.sh
- chain.tmpl

### uv-plane continuum subtraction
- obs_sub.sh -- the wrapper script to submit the job
- sub.tmpl -- the template file that is modified to produce the job script
- sub_uv_cont.py -- actually do the visibility continuum subtraction

### Imaging scripts
- obs_spec_image.sh -- the wrapper script to submit the job
- specimage.tmpl -- the template file that is modified to produce the job script
- update_bscale.py -- rescale the images by the primary beam
- rms_par.py -- measure the RMS of all the final images in a fast parallelised way

### Plotting scripts
These help diagnose bad images and can be run in the project directory directly on the command-line.
- plot_peak.py -- plot the peak value of the center of each MFS image as a function of epoch
- plot_rms.py -- plot the RMS of each MFS image as a function of epoch
