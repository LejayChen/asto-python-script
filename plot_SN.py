#Lejay Chen   plot GC specific frequency of galaixes (S_N ~ M_V)

import pandas
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

def plot_SN():
	'''
	plot with error bar
	'''
	dEdata = Table.read('dEdata.fits')
	V_list = dEdata['MV']
	SN_list  = dEdata['SN']
	SN_err = dEdata['SNerr']
	b=plt.errorbar(np.array(V_list),np.array(SN_list),yerr=SN_err,fmt='ok',markersize=4,linewidth=1.5,capsize=0,ecolor='0.7')  #plot data
	b.set_label('This work')

	liter = pandas.read_excel('100galaxies.xlsx')
	V_liter = np.array(liter['M_V'][1:])
	SN_liter = np.array(liter['S_N'][1:])
	SN_liter_err = np.array(liter['S_N_err'][1:])
	a=plt.errorbar(V_liter,SN_liter,yerr=SN_liter_err, fmt='ok',markerfacecolor='white',markersize=4,linewidth=1.5,capsize=0,ecolor='0.7')#from literature
	a.set_label('Peng et.al')

	V_mean = [-22.5,-21.3,-20.5,-19.5,-18.7]
	SN_mean = [5.4,2.2,1.3,1.3,1.7]
	for i in range(5):
		V_sum = 0
		SN_sum = 0
		count = 0
		mv = -18 + i
		for j in range(len(V_list)):
			if V_list[j]>mv and V_list[j]<mv + 1:
				V_sum = V_sum +V_list[j]
				SN_sum = SN_sum + SN_list[j]
				count += 1
		for k in range(len(V_liter)):
			if V_liter[k]>mv and V_liter[k]<mv + 1:
				V_sum = V_sum +V_liter[k]
				SN_sum = SN_sum + SN_liter[k]
				count += 1
		print '(%d,%d):<M_v>:%0.4f,<S_N>,%0.4f'%(mv,mv+1,V_sum/count,SN_sum/count)
		V_mean.append(V_sum/count)
		SN_mean.append(SN_sum/count)
		
	plt.plot(V_mean,SN_mean,'--b',linewidth=2)#mean trend

	plt.ylim(0,40)
	plt.xlim(-24,-12)
	plt.ylabel(r'$S_N$',fontsize=16)
	plt.xlabel(r'$M_V$',fontsize=16)
	plt.legend(numpoints=1,frameon=True,loc='upper left')
	plt.savefig('SNtoV_doubled.eps')
	plt.savefig('SNtoV_doubled.png')

if __name__ == '__main__':
	plot_SN()