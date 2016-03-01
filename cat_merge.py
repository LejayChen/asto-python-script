'''
merge catalogs from different bands created by SExtractor
'''

import sys,os
from astropy.io import fits

def merge(filename):
	cat_u = fits.open(filename+'.u.fits')
	cat_g = fits.open(filename+'.g.fits') 
	cat_i = fits.open(filename+'.i.fits') 
	cat_z = fits.open(filename+'.z.fits') 
	for i in range(len(cat_g[1].columns)):
		cat_u[1].columns[i].name += '_U'
		cat_g[1].columns[i].name += '_G'
		cat_i[1].columns[i].name += '_I'
		cat_z[1].columns[i].name += '_Z'

	col_u = cat_u[1].columns
	col_g = cat_g[1].columns
	col_i = cat_i[1].columns
	col_z = cat_z[1].columns
	new_columns =  col_u + col_g + col_i + col_z
	hdu = fits.BinTableHDU.from_columns(new_columns)
	try:
		hdu.writeto(filename+'.ugiz.fits')
	except IOError:
		os.system('rm '+filename+'.ugiz.fits')
		hdu.writeto(filename+'.ugiz.fits')

if __name__=='__main__':
	for i in range(1,len(sys.argv)):
		filename = sys.argv[i]
		merge(filename)
		print filename
