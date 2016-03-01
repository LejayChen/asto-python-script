import os

def main():
	flist = open('files','r')  #read file list

	#batch processing
	for FileName in flist.readlines():  
		FileName=FileName.rstrip()
		os.system('sextractor  '+FileName+'.g.fits'+' -c extract_main.sex -CATALOG_NAME '+'b'+FileName+'.fits')

main()