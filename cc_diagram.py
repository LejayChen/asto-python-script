import os,re
from math import *
import numpy as np
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def cc_diagram(u_all,g_all,z_all,u,g,z,item,indices):
	fig = Figure()
	canvas = FigureCanvas(fig)
	ax  = fig.add_axes([0.1, 0.1, 0.82, 0.82])
	cat, =  ax.plot(u_all-g_all,g_all-z_all,'.k',color='0.7',label='field',markersize=3)
	obj, = ax.plot(u-g,g-z,'+k',markersize=5.5,linewidth=2,label=item)  #plot data
	for i in range(len(indices)):
	             if indices[i]==1: 
	                          a, =ax.plot(u[i]-g[i],g[i]-z[i],'.r',markersize=7)              #plot selected GCs	
	ax.set_xlim([-0.1,3])
	ax.set_ylim([-0.2,3.6])
	ax.legend(numpoints=1,frameon=True,loc='upper left')
	ax.set_xlabel(r'$(u-g)_0$',fontsize = 16)
	ax.set_ylabel(r'$(g-z)_0$',fontsize = 16)

	verts = [0.8,0.62],[0.979,0.62],[1.79,1.39],[1.79,1.5],[1.49,1.5],[0.8,0.966]
	poly = patches.Polygon(verts,fill=False,color='red') 
	ax.add_patch(poly)

	canvas.print_figure(item+'.cc.png')