import aplpy
import pyregion
from astropy.wcs import WCS
from astropy.io import fits
from astropy.table import Table
import numpy as np

cat = np.load('coords_3.npy')
fig = aplpy.FITSFigure('../../vcc.image/1545.g.fits')
fig.show_grayscale(vmin=0,vmid=-0.3,invert='y',stretch='log')
#fig.show_regions('vcc1545_backup.reg')
img = fits.open('../../vcc.image/1545.g.fits')

w = WCS('../../vcc.image/1545.g.fits')
x_max = img[0].header['NAXIS1']
y_max = img[0].header['NAXIS2']
ra_center,dec_center = w.all_pix2world(x_max/2+0.5,y_max/2+0.5,0)# Pixel to WCS
print ra_center, dec_center
fig.show_circles(round(ra_center,5),round(dec_center,5),22.491/3600)
for item in cat:
	if item[2]==1:
		fig.show_circles(item[0],item[1],2./3600,color='red',linewidth=2)
	if item[2]==2:
		fig.show_circles(item[0],item[1],2./3600,color='yellow')
	if item[2]==3:
		fig.show_circles(item[0],item[1],2./3600,color='blue',linewidth=2)
fig.save('aa.png')