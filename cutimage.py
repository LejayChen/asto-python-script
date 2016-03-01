from cutout import *

filelist = ['NGVS+1+1.l.z.Mg002.fits','NGVS+1+1.l.u.Mg002.fits','NGVS+1+1.l.g.Mg002.fits','NGVS+1+1.l.i.Mg002.fits']


#objects=[[xc,yc,xw,yw]]
objects = [[19200,19710,6200,6700,'IC3506']]

for filename in filelist:
	for obj in objects:
		cutoutimg(filename, (obj[0]+obj[1])/2, (obj[2]+obj[3])/2,(obj[1]-obj[0])/2,(obj[3]-obj[2])/2,'pixels',obj[4]+'.'+filename[11]+'.ogn.fits', True, False, 'celestial', False, None)
