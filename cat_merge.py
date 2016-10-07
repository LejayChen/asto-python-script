'''
merge catalogs from different bands created by SExtractor
'''

import sys,os
from astropy.table import *

def merge(filename):
	cat_u = Table.read(filename+'.u.cat.fits')
	cat_g = Table.read(filename+'.g.cat.fits') 
	cat_i = Table.read(filename+'.i.cat.fits') 
	cat_z = Table.read(filename+'.z.cat.fits') 
	common_cols = ['NUMBER','X_IMAGE','Y_IMAGE','ALPHA_J2000','DELTA_J2000']
	cat_merge = join(cat_u, cat_g, keys=common_cols,table_names=['u','g'],uniq_col_name='{table_name}_{col_name}')
	cat_merge = join(cat_merge, cat_i, keys=common_cols)
	cat_merge = join(cat_merge, cat_z, keys=common_cols,table_names=['i','z'],uniq_col_name='{table_name}_{col_name}')
	try:
		cat_merge.write(filename+'.ugiz.fits')
		print cat_merge3.info
	except IOError:
		os.system('rm '+filename+'.ugiz.fits')
		cat_merge.write(filename+'.ugiz.fits')
		print cat_merge.info

if __name__=='__main__':
	for i in range(1,len(sys.argv)):
		filename = sys.argv[i]
		merge(filename)
		print filename
