from photutils import *
from astropy.io import fits
from astropy.table import *
from math import pi
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mask import *


plate_scale = 0.187

def petro_Rp(radius):
	L1 = aperture_photometry(img,CircularAperture(positions, r=0.8*radius),mask=mask_1)['aperture_sum'][0]
	L2 = aperture_photometry(img,CircularAperture(positions, r=1.25*radius),mask=mask_1)['aperture_sum'][0]
	L3 = aperture_photometry(img,CircularAperture(positions, r=radius),mask=mask_1)['aperture_sum'][0]
	R_p1 = (L2-L1)/(pi*(1.25**2-0.8**2)*radius**2)
	R_p2 = L3/(pi*radius**2)
	return R_p1/R_p2

def Rp_shape(item,img_width):
	x = np.arange(1,img_width/2)
	y = []
	for i in x:
		y.append(petro_Rp(i))
	y = np.array(y)

	fig = Figure()
	canvas = FigureCanvas(fig)
	ax  = fig.add_axes([0.1, 0.1, 0.82, 0.82])
	ax.plot(x,y,'.k')
	canvas.print_figure(item+'.shape.png')	

def get_rp(radius,img_width,item):
	criteria = 0.2
	Rp_shape(item,img_width)
	R_p = petro_Rp(radius)
	while abs(R_p - criteria)>0.0002:
		#print 'rp:',radius,'delta:',R_p-criteria
		R_p = petro_Rp(radius)
		if abs(R_p - criteria)>0.1:
			step = 10
		else:
			step = 5
		radius = radius + (R_p - criteria)*step

	if 1.25*radius<img_width/2.:
		return radius,1
	else:
		return radius,0

def get_re(total_flux,re):
	flux_re = aperture_photometry(img,CircularAperture(positions, r=re),mask=mask_1)['aperture_sum'][0]
	while abs((total_flux/2 - flux_re)/total_flux)>0.0005:
		#print 're:',re,'(f_half-f_re)/f',( total_flux/2 - flux_re)/total_flux,'f_half',total_flux/2,'f_re',flux_re
		flux_re = aperture_photometry(img,CircularAperture(positions, r=re),mask=mask_1)['aperture_sum'][0]  #no background substraction
		if abs((total_flux/2 - flux_re)/total_flux)>0.1:
			step =10
		if abs((total_flux/2 - flux_re)/total_flux)>0.01:
			step = 5
		if abs((total_flux/2 - flux_re)/total_flux)>0.001:
			step = 4
		else:
			step =2
		re = re + (total_flux/2 - flux_re)/total_flux*step
	return re

def measure_re(filelist):
	cat = Table(names=('Index','re','flag'),dtype=('a4','f8','i4'))
	for item in filelist:
		global img,positions,mask_1
		item = item.rstrip()
		img = fits.open(item+'.cut.fits')[0]
		img_width = img.header['NAXIS1']
		positions = [(img_width/2.,img_width/2.)]
		mask_1 = mask(img.data,item)
		rp , flag = get_rp(1.,img_width,item)

		total_flux = aperture_photometry(img,CircularAperture(positions, r=2*rp),mask=mask_1)['aperture_sum'][0] #total flux
		re = get_re(total_flux,rp)*plate_scale

		print item,'re:',re,flag
		cat.add_row((item,re,flag))

	return cat


if __name__=='__main__':
	filelist = open('den.used').readlines() #list of galaxies
	cat = measure_re(filelist)
	cat.write('measure_re.fits',overwrite=True)