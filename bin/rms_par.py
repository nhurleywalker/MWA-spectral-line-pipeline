#!/usr/bin/env python

#import sys
import os
from astropy.io import fits
import numpy as np
from glob import glob
import argparse
# Parallelise the code
import multiprocessing
# multiple cores support, deprecated in python3
#import pprocess

''' calculate image RMS'''

def _crms(args):
    """
    A shallow wrapper for calc_rms

    Parameters
    ----------
    args : list
        A list of arguments for calc_rms

    Returns
    -------
    None
    """
    # an easier to debug traceback when multiprocessing
    # thanks to https://stackoverflow.com/a/16618842/1710603
    try:
        return calc_rms(*args)
    except:
        import traceback
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


def calc_rms(image):
    rmsimage = image.replace(".fits", "_rms.fits")
    #    if not os.path.exists(rmsimage):
    hdu = fits.open(image)
    rms = np.nanstd(hdu[0].data)
    if blank:
        # Give blank images very large RMS
        if rms == 0.0:
            rms = 2.**126
            hdu[0].data.fill(np.nan)
            hdu.writeto(image, overwrite=True)
    rms_map = rms * np.ones(hdu[0].data.shape, dtype="float32")
    hdu[0].data = rms_map
    hdu.writeto(rmsimage, overwrite=True)
    hdu.close()
    return [rmsimage]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group("required arguments:")
    group1.add_argument(
        "--images",
        type=str,
        dest="images",
        default=None,
        help="The image files to calculate the RMS for (no default, use globbing)",
    )
    group2 = parser.add_argument_group("optional arguments:")
    group2.add_argument(
        "--blank",
        type=bool,
        dest="blank",
        default=True,
        help="set RMS very large for blank frames (default True)",
    )
    options = parser.parse_args()

    imagelist = glob(options.images)
    
    blank = options.blank

    cores = multiprocessing.cpu_count()

# Replaced tidy pprocess with baggy multiprocess because pprocess is deprecated in python3
    pool = multiprocessing.Pool(processes=cores, maxtasksperchild=1)
    try:
        # chunksize=1 ensures that we only send a single task to each process
        results = pool.map_async(_crms, imagelist, chunksize=1).get(timeout=10000000)
    except KeyboardInterrupt:
        pool.close()
        sys.exit(1)
    pool.close()
    pool.join()

    rmslist = map(list, zip(*results))

#    results = pprocess.Map(limit=cores)
#    calc = results.manage(pprocess.MakeParallel(calc_rms))

#    for image in imagelist:
#        print(image)
#        calc(image)

# Unless you do this, it never finishes
#    rmslist = map(list, zip(*results))
