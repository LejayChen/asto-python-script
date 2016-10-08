#1me 2hubble 3both

from astropy.table import *
from astropy.io import fits
from astropy.wcs import WCS
from math import *
import numpy as np
import pandas
import matplotlib.pyplot as plt
import os
from cc_new import * 

def selection(g, g_best, i, i_4):
	if g-i<1.15 and g-i>0.55 and 20<g_best<24 and i_4-i>-0.15 and i_4-i<0.25:
		return 1   #is gc
	else:
		return 0  #is not gc

def selection2(u, g, z, g_best, i, i_4):
	if g-z<1.5 and g-z>0.62 and u-g>0.8 and u-g<1.79 and 18<g_best<25 and i_4-i>-0.35 and i_4-i<0.35:
		if g-z< 0.77*(u-g)+0.35 and g-z>0.95*(u-g)-0.31:
			return 1  #is gc
		else:
			return 0  #is not gc
	else:
		return 0  #is not gc
'''
	if g-z<1.5 and g-z>0.62 and u-g>0.8 and u-g<1.79 and 18<g_best<25 and i_4-i>-0.15 and i_4-i<0.25:
		if g-z< 0.77*(u-g)+0.35 and g-z>0.95*(u-g)-0.31:
'''
item = 'vcc1545'
ra_center,dec_center = 188.54792, 12.048996  #vcc1545 center coordinate
field = 'NGVS+1+0'
r_e = 24.1   #in arcsec from SDSS
r =  r_e*4

#count GC numbers
#mags with aperture correction
cat_me = Table.read('1545.ugiz.fits')
u = cat_me['u_MAG_APER'][:,5]-0.548
g = cat_me['g_MAG_APER'][:,5]-0.454
z = cat_me['z_MAG_APER'][:,5]-0.420
g_best = cat_me['g_MAG_BEST']
i = cat_me['i_MAG_APER'][:,5]-0.280
i_4 = cat_me['i_MAG_APER'][:,1]-0.780

coords_1=[]
for k in range(len(cat_me.field(0))):
	ra = cat_me['ALPHA_J2000'][k]
	dec = cat_me['DELTA_J2000'][k]
	if sqrt((cat_me['ALPHA_J2000'][k] - ra_center)**2 + (cat_me['DELTA_J2000'][k] - dec_center)**2) < r/3600.:
		a = selection2(u[k], g[k], z[k], g_best[k], i[k], i_4[k])
		if a == 1:  coords_1.append((ra,dec))
coords_1 = np.array(coords_1)
gc_num=len(coords_1)*2  #gc_num doubled because of truncation of GCLF

#From Hubble Data
cat2 = Table.read('vcc1545_gctbl.fits')
mask = cat2['CLASS']>0.95
cat2 = cat2[mask]
coords_2 = []
for k in range(len(cat2.field(0))):
	ra = cat2['RA'][k]
	dec = cat2['DEC'][k]
	if sqrt((cat2['RA'][k] - ra_center)**2 + (cat2['DEC'][k] - dec_center)**2) < r/3600.:
		coords_2.append((ra,dec))
coords_2 = np.array(coords_2)
gc_num_h = len(coords_2)

print gc_num,gc_num_h

#create a new catalog to visually inspect the selection criteria in topcat
coords_3 = []
for coord in coords_1:
	flag = False
	for coord2 in coords_2:
		if (coord[0]-coord2[0])**2 + (coord[1]-coord2[1])**2<6e-8:
			coords_3.append([coord[0],coord[1],3])
			flag = True
	if flag == False:
		coords_3.append([coord[0],coord[1],1])

for coord in coords_2:
	flag = False
	for coord2 in coords_1:
		if (coord[0]-coord2[0])**2 + (coord[1]-coord2[1])**2<6e-8:  #position difference about 0.88 arcsec
			flag = True
	if flag == False:
		coords_3.append([coord[0]-9e-05,coord[1]+0.00019,2])  # shift distance maybe wrong

coords_3 = np.array(coords_3)
np.save('coords_3',coords_3)
matched = []
for i in range(len(cat_me)):
	ra = cat_me[i]['ALPHA_J2000']
	dec = cat_me[i]['DELTA_J2000']
	flag = False
	for coord in coords_3:
		if (coord[0]-ra)**2 + (coord[1]-dec)**2<6e-8:
			matched.append(coord[2])
			flag = True
			break
	if flag == False:
		matched.append(0)
	print i,len(matched)

match = Column(name='match',data=matched)
print len(cat_me),len(match)
cat_me.add_column(match)

match = np.array(match)
print len(coords_3),len(match[match!=0])

if os.path.isfile('gc_selection_check_vcc1545_new.fits'):
	os.system('rm gc_selection_check_vcc1545_new.fits')
cat_me.write('gc_selection_check_vcc1545_new.fits')