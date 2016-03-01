'''
   create region file for ds9 use
'''
import sys
from astropy.io import fits
import numpy as np

def build_reg(filename, indices=[]):
	catalog = fits.open(filename+'.g.cat.fits')
	if indices != []:
		reg_file = open(filename+'.selected.reg','w')
	else:
		reg_file = open(filename+'.reg','w')	

	for k in range(len(catalog[1].data['NUMBER'])):
		x = catalog[1].data['ALPHA_J2000'][k]
		y = catalog[1].data['DELTA_J2000'][k]
		if k in indices:
			color = 'red'
			#print catalog[1].data['NUMBER'][k]
		else:
			color = 'green'
		reg_file.write(('J2000; circle  %0.7f    %0.7f      1" # color='+color+'\n')%(x,y))

if __name__=='__main__':
	for i in range(1,len(sys.argv)):
		filename = sys.argv[i]
		build_reg(filename)
		print filename

