'''
Prepare feedme file from image for GalFit
   Lejay Chen
version 0.1 2015.5.20
version 0.2 2015.5.27  (finished source selecting method)
version 0.2.1 2015.6.7  (corrected fitting box and other things)
'''

from astropy.io import fits
from create_feedme import *
from math import *

def get_size(FileName):#get the size of the image
	img = fits.open(FileName+'.g.fits')
	x_max = img[0].header['NAXIS1']
	y_max = img[0].header['NAXIS2']
	return x_max,y_max

def find_obj(FileName,xc,yc):
	catalog = fits.open('b'+FileName+'.fits')
	data = catalog[1].data

	#Find the object to be fitted 
	data_re = sorted(data, key=lambda x:x[6],reverse=True)  #sort by effective radius
	candidiate = data_re[:len(data)/2+1]     #pick out 50% objects with larger radius
	dis = [10000] * (len(data)/2+1)
	for i in range(len(candidiate)):
		x = candidiate[i][1]
		y = candidiate[i][2]
		dis[i] = sqrt((x-xc)**2+(y-yc)**2)
	index = dis.index(min(dis))   #choose the one most close to the image center
	##print index,len(data),len(candidiate)
	return candidiate[index]

def main():
	flist=open('files','r')  #read file list

	#batch processing
	for FileName in flist.readlines():  
		FileName = FileName.rstrip()
		
		x_max,y_max=get_size(FileName)   # get Image Size
		obj = find_obj(FileName,x_max/2,y_max/2)  # get the interested object
		create_feedme(obj,FileName,x_max,y_max) # create feedme file GalFit
		print 'VCC'+FileName+' processed...'

main()
