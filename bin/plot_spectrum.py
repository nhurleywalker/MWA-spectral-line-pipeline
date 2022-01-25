#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import sys

# Publication-quality plotting
from matplotlib import rc
rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['serif']})

infile = sys.argv[1]
whdu = fits.open(infile)
wcube = whdu[0].data

# frequency info
chans = np.arange(whdu[0].header["CRVAL3"], whdu[0].header["CRVAL3"]+whdu[0].header["NAXIS3"]*whdu[0].header["CDELT3"], 256*whdu[0].header["CDELT3"])
chans = [x * 1.e-6 for x in chans]

#undata = uncube[:,uncube.shape[1]/2,uncube.shape[2]/2]
wdata = wcube[:,int(wcube.shape[1]/2),int(wcube.shape[2]/2)]
nchans = wdata.shape[0]

wrms = np.nanstd(wcube[:,0:50,0:50],axis=(1,2))

fig = plt.figure(figsize = (15,3))
ax = fig.add_subplot(111)
ax2 = ax.twiny()
ax2.set_xlim((np.min(chans), np.max(chans)))
ax.fill_between(np.arange(0,nchans), -3.e3*wrms, 3.e3*wrms, color="blue", alpha=0.3, lw=0)
#ax.plot(undata, label="unweighted", color="red", alpha = 0.3)
ax.plot(1.e3*wdata, label="weighted", color="black")
start, end = ax.get_xlim()
ax.xaxis.set_ticks(np.arange(start, end, 100))
ax2.set_xticks(chans)
ax2.set_xlabel("Frequency / MHz")
#ax.plot(3*wrms, ls = ":", color="black")
#ax.plot(-3*wrms, ls = ":", color="black")
ax.set_ylabel("peak flux density (mJy/beam)")
ax.set_xlabel("10-kHz channel number")
#ax.set_ylim([-0.5, 0.5])
ax.set_xlim([0, 3072])
#ax.set_ylim([-1000., 1000.])
#f=22
#ax.set_xlim([(128*f)+0, (128*f)+256])
#ax.axvline(x=(128*f)+124)
#ax.axvline(x=(128*f)+131)
#ax.legend(loc = 2)
ax2.axvspan(207.06, 208.27, alpha = 0.2, color="red")
fig.savefig(infile.replace(".fits", "_spectrum.pdf"), bbox_inches="tight")
fig.savefig(infile.replace(".fits", "_spectrum.png"), bbox_inches="tight")

#fig.savefig("temp.png", bbox_inches="tight")

#ax.set_xlim([2500,2650])
#fig.savefig("zoom.png")
