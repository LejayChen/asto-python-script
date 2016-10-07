#1me 2hubble 3both

from astropy.table import *
from astropy.io import fits
from astropy.wcs import WCS
from math import *
import numpy as np
import pandas
import matplotlib.pyplot as plt
from reg import *
import os

def selection(g, g_best, i, i_4):
	if g-i<1.15 and g-i>0.55 and 20<g_best<24 and i_4-i>-0.11 and i_4-i<0.15:
		return 1   #is gc
	else:
		return 0  #is not gc

def selection2(u, g, z, g_best, i, i_4):
	if g-z<1.5 and g-z>0.62 and u-g>0.8 and u-g<1.79 and 18.5<g_best<24.6 and i_4-i>-0.15 and i_4-i<0.25:
		if g-z< 0.77*(u-g)+0.35 and g-z>0.95*(u-g)-0.31:
			return 1  #is gc
		else:
			return 0  #is not gc
	else:
		return 0  #is not gc

item = 'vcc1545'
ra_center,dec_center = 188.54792, 12.048996
field = 'NGVS+1+0'
r_e = 24.1   #in arcsec from SDSS
r =  r_e*4
coords=[]


#cut an area for counting
cat_field = Table.read(field+'.l.Mg002.sexcat.apcor.fits')
mask1 = abs(cat_field['RA'] - ra_center) <r/3600.
cat_field2 = cat_field[mask1]
mask2 = abs(cat_field2['DEC'] - dec_center) < r/3600.
cat_field2 = cat_field2[mask2]

#count GC numbers
indices = []
u = cat_field2['MAGCOR_AP8'][:,0]
g = cat_field2['MAGCOR_AP8'][:,1]
z = cat_field2['MAGCOR_AP8'][:,4]
g_best = cat_field2['MAG_BEST'][:,1]
i = cat_field2['MAGCOR_AP8'][:,3]
i_4 = cat_field2['MAGCOR_AP4'][:,3]
for k in range(len(cat_field2.field(0))):
	ra = cat_field2['RA'][k]
	dec = cat_field2['DEC'][k]
	if sqrt((cat_field2['RA'][k] - ra_center)**2 + (cat_field2['DEC'][k] - dec_center)**2) < r/3600.:
		a = selection2(u[k], g[k], z[k], g_best[k], i[k], i_4[k])
		indices.append(a)
		if a == 1:  coords.append((ra,dec,1))
	else:
		indices.append(0)
indices = np.array(indices)
gc_num=len(indices[indices==1])*2  #gc_num doubled because of truncation of GCLF

#From Hubble Data
cat2 = Table.read('vcc1545_gctbl.fits')
mask = cat2['CLASS']>0.95
cat2 = cat2[mask]
indices_h = []
for k in range(len(cat2.field(0))):
	ra = cat2['RA'][k]
	dec = cat2['DEC'][k]
	if sqrt((cat2['RA'][k] - ra_center)**2 + (cat2['DEC'][k] - dec_center)**2) < r/3600.:
		indices_h.append(1)
		coords.append((ra,dec,2))
	else:
		indices_h.append(0)
indices_h = np.array(indices_h)
gc_num_h = len(indices_h[indices_h==1])

print gc_num,gc_num_h
build_reg(coords)


#create a new catalog to visually inspect the selection criteria in topcat
coords = np.array(coords)
coords_1 = coords[coords[:,2]==1]
coords_2 = coords[coords[:,2]==2]

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
		coords_3.append([coord[0]-9e-05,coord[1]+0.00019,2])

coords_3 = np.array(coords_3)
np.save('coords_3',coords_3)
matched = []
for i in range(len(cat_field2)):
	ra = cat_field2[i]['RA']
	dec = cat_field2[i]['DEC']
	flag = False
	for coord in coords_3:
		if (coord[0]-ra)**2 + (coord[1]-dec)**2<6e-8:
			matched.append(coord[2])
			flag = True
	if flag == False:
		matched.append(0)

match = Column(name='match',data=matched)
cat_field2.add_column(match)
match = np.array(match)
print len(coords_3),len(match[match!=0])
if os.path.isfile('gc_selection_check_vcc1545.fits'):
	os.system('rm gc_selection_check_vcc1545.fits')
cat_g.write('gc_selection_check_vcc1545.fits')