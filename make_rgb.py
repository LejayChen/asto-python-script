import pyfits
import numpy as np
import pylab as py
import img_scale

u_img = pyfits.getdata('0596.u.fits')
g_img = pyfits.getdata('0596.g.fits')
i_img = pyfits.getdata('0596.i.fits')

img = np.zeros((u_img.shape[0] , g_img.shape[1] , 3 ), dtype = float)
img[:,:,0]=img_scale.asinh(u_img)
img[:,:,1]=img_scale.asinh(g_img)
img[:,:,2]=img_scale.asinh(i_img)

py.clf()
py.imshow(img , aspect = 'equal')
py.title('0596')
py.savefig('0596.jpeg')