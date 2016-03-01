import sys,os
import aplpy
import random
from termcolor import colored

filelist = open('files_all','r').readlines()
random.shuffle(filelist)

for index in filelist[:1]:
	index = index.rstrip()
	print colored('RGB image gernerating :','green'), colored(' VCC'+index,'yellow')
	image_r = index+'.i.fits'
	image_g = index+'.g.fits'
	image_b = index+'.u.fits'
	cube_name = index+'_rgb.fits'
	cube_name2 = index +'_rgb_2d.fits'
	output_image_name =index+'.png'
	if os.path.exists('./'+output_image_name)==False and index !=1347 and index !=0167:
             	aplpy.make_rgb_cube([image_r,image_g,image_b],cube_name)
             	aplpy.make_rgb_image(cube_name,output_image_name,
             		stretch_r='arcsinh',stretch_g='arcsinh',stretch_b='arcsinh',
             		#vmin_r=0, vmin_g=0,vmin_b=0,
             		embed_avm_tags = False)
             	os.system('rm '+cube_name+' '+cube_name2)
             	
             	#os.system('shotwell '+output_image_name+'&')