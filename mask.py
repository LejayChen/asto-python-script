from math import *
from astropy.io import fits
import numpy as np
# data = astropy.io.fits[0].data
def mask(data,item):
	xmax,ymax = data.shape
	mask = np.zeros_like(data,dtype=bool)
	data2 = np.ones(data.shape)
	for x in range(1,xmax):
		for y in range(1,ymax):
			dis = sqrt((x-xmax/2)**2+(y-ymax/2)**2)
			L_central  = sum(sum(data[xmax/2-2:xmax/2+2,ymax/2-2:ymax/2+2])/16)
			if dis>ymax/50 and data[x,y]>L_central*exp(-4*dis/xmax)*2:
				mask[x,y] = True
				data2[x,y] = 0
			else:
				data2[x,y] = data[x,y]
	hdu = fits.PrimaryHDU(data2)
	hdulist = fits.HDUList([hdu])
	hdulist.writeto(item+'.masked.fits',clobber=True)
	return mask

if __name__=='__main__':
	data = fits.open('0313.cut.fits')[0].data
	mask_1 = mask(data,'0313')