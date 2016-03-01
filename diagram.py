#Lejay Chen 2015.11.16
# Revised on 2015.11.23 
# 	can take external arguments   batch process
# 	interstellar extinction
# Revised on 2015.12.2
#	more genral function magnitude()
#Revised on 2015.12.7
#	revise plot to object-orient
'''
Draw color-color for u-g vs g-i  or color-magnitude diagrams for g vs g-i

usage:
  python diagram.py <option> <filename>...
  your filename should be
     filename.g.fits
     filename.u.fits
     filename.i.fits
   option:
      -cc: draw color-color diagram
      -cm: draw color-magnitude diagram
   you need SFD_dust_4096.ngp.fits to cancel the interstellar extinction
 '''

import sys
from astropy.io import fits
from reg import *
from math import *
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

dust_map = fits.open('SFD_dust_4096_ngp.fits')

def get_extinction(band,r,d):
	global dust_map
	coord = SkyCoord(ra=r*u.degree, dec=d*u.degree, frame='fk5') 

	#galactic coord in rad
	l = coord.galactic.l.value/180*pi
	b = coord.galactic.b.value/180*pi

	#pixel coord
	x = sqrt(1-sin(b))*cos(l)*2048+2047.5
	y = -sqrt(1-sin(b))*sin(l)*2048+2047.5

	ebv = dust_map[0].data[x,y]  #E(B-V) value at (x,y)
	av = [1.490,1.190,0.874,0.674,0.498]  #[u,g,r,i,z]
	if band == 'u':
		return ebv*av[0]*3.1
	if band == 'g':
		return ebv*av[1]*3.1
	if band == 'r':
		return ebv*av[2]*3.1
	if band == 'i':
		return ebv*av[3]*3.1
	if band == 'z':
		return ebv*av[4]*3.1
	else:
		return 0

def  magnitude(filename, band, aperture=8):
	aperture=[3,4,5,6,7,8,16,32].index(aperture)
	catalog = fits.open(filename+'.'+band+'.cat.fits')
	num_obj = len(catalog[1].data['NUMBER']) 
	data = catalog[1].data

	mag=[]
	ext=[]
	for j in range(num_obj):
		mag.append(data['MAG_APER'][j][aperture] - get_extinction(band,data['ALPHA_J2000'][j],data['DELTA_J2000'][j]))
	mag = np.array(mag) 
	return mag

def cc_diagram(filename):
	u = magnitude(filename,'u')
	g = magnitude(filename,'g')
	i = magnitude(filename,'i')
	g_16 = magnitude(filename,'g',16)
	z = magnitude(filename,'z')
	indices = selection(g,g_16,i)

	fig = Figure()
	canvas = FigureCanvas(fig)
	ax  = fig.add_axes([0.1, 0.1, 0.82, 0.82])
	all_obj, = ax.plot(u-g,g-z,'*',label=filename)  #plot data
	for i in indices: 
		a, =ax.plot(u[i]-g[i],g[i]-z[i],'*r')              #plot selected GCs
	a.set_label('Selected GCs')
	ax.set_xlim([-0.1,3])
	ax.set_ylim([-0.2,3.6])

	ax.grid()
	ax.legend(numpoints=1,frameon=True)
	ax.set_xlabel(r'$(u-g)_0$',fontsize = 16)
	ax.set_ylabel(r'$(g-z)_0$',fontsize = 16)

	canvas.print_figure(filename+'.cc.png')

def cm_diagram(filename):
	g = magnitude(filename,'g')
	g_16 = magnitude(filename,'g',16)
	i = magnitude(filename,'i')
	indices = selection(g,g_16,i)

	fig = Figure()
	canvas = FigureCanvas(fig)
	ax = fig.add_axes([0.1, 0.1, 0.82, 0.82])

	all_obj, = ax.plot( g-i, g_16,'*',label=filename)   #plot all
	for k in indices:
		a, =ax.plot(g[k]-i[k],g_16[k],'go',markersize=6)   #plot selected GCs
	a.set_label('selected GCs')
	ax.set_xlim(-0.5,3)
	ax.set_ylim((19,27)[::-1])

	ax.grid()
	ax.legend(numpoints=1,frameon=True)
	ax.set_xlabel(r'$(g-i)_0$',fontsize = 16)
	ax.set_ylabel(r'$g_0$',fontsize = 16)

	canvas.print_figure(filename+'.cm.png')

def selection(g,g_16,i):
	indices=[]
	i_4 = magnitude(filename,'i',4)
	for k in range(len(g)):
		if g[k]-i[k]<1.15 and g[k]-i[k]>0.55 and 20<g_16[k]<24 and i_4[k]-i[k]>0.4 and i_4[k]-i[k]<0.9:
			indices.append(k)
	print 'No. of GCs: '+str(len(indices))
	build_reg(filename,indices)
	#append the catalog to include a row identifying the GCs
	return indices

if __name__ == '__main__':
	if sys.argv[1] != '-cc' and sys.argv[1] != '-cm' :
		raise SyntaxError('lack option: -cm or -cc, Syntax: python diagram.py <option> <filename>... ')
	for i in range(2,len(sys.argv)):
		filename = sys.argv[i]
		if sys.argv[1] == '-cc':
			cc_diagram(filename)
			print 'color-color diagram for '+filename
		if sys.argv[1] == '-cm':
			cm_diagram(filename)
			print 'color-magnitude diagram for '+filename
		else:
			pass