import os

index = raw_input('Input a VCC index:')
os.system('sextractor '+index+'.block.fits[3],'+index+'.u.fits -c photometric.sex -CATALOG_NAME '+index+'.u.cat.fits') #u
os.system('sextractor '+index+'.block.fits[3],'+index+'.g.fits -c photometric.sex -CATALOG_NAME '+index+'.g.cat.fits') #g
os.system('sextractor '+index+'.block.fits[3],'+index+'.i.fits -c photometric.sex -CATALOG_NAME '+index+'.i.cat.fits') #i
os.system('sextractor '+index+'.block.fits[3],'+index+'.z.fits -c photometric.sex -CATALOG_NAME '+index+'.z.cat.fits') #z