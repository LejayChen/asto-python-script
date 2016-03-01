#Module for create feedme file
#INPUT:
#    obj--(index,x,y,PA,e,mag,r_e)
#    FileName--name of output feedme file
#Lejay Chen
#2015.5.20

def create_feedme(obj,FileName,xmax,ymax):
              x=obj[1]    # x-axis value of the object
              y=obj[2]    # y-axis value of the object
              PA=obj[3]   # position angle
              e=obj[4]      # Ellipicity
              mag=obj[5] #magnitude (mag_best)
              r_e=obj[6]    # effective radius  (flux_radius)

              outfile=open(FileName+'.g.feedme','w')
              outfile.write('# IMAGE and GALFIT CONTROL PARAMETERS\n')
              outfile.write('A) '+FileName+'.g.fits            # Input data image (FITS file)\n')
              outfile.write('B) '+FileName+'.block.fits       # Output data image block\n')
              outfile.write('C) none                # Sigma image name (made from data if blank or "none") \n')
              outfile.write('D) psf.fits          # Input PSF image and (optional) diffusion kernel\n')
              outfile.write('E) 1                   # PSF fine sampling factor relative to data\n')
              outfile.write('F) none                # Bad pixel mask (FITS image or ASCII coord list)\n')
              outfile.write('G) none                # File with parameter constraints (ASCII file)\n') 
              # outfile.write('H) %d  %d  %d  %d     # Image region to fit (xmin xmax ymin ymax)\n'%(x-200,x+200,y-200,y+200))
              outfile.write('H) 1  %d  1  %d     # Image region to fit (xmin xmax ymin ymax)\n'%(xmax,ymax))
              outfile.write('I) 100    100          # Size of the convolution box (x y)\n')
              outfile.write('J) 30              # Magnitude photometric zeropoint \n')
              outfile.write('K) 0.187  0.187        # Plate scale (dx dy)    [arcsec per pixel]\n')
              outfile.write('O) regular             # Display type (regular, curses, both)\n')
              outfile.write('P) 0                  # Choose: 0=optimize, 1=model, 2=imgblock, 3=subcomps\n')

              outfile.write('\n')
              outfile.write('==============================================\n')

              outfile.write('# Component number: 1\n')
              outfile.write(' 0) sersic                 #  Component type\n')
              outfile.write('1)  %0.4f  %0.4f 1 1  #  Position x, y\n'%(x,y))
              outfile.write('3) %0.4f  1          #  Integrated magnitude\n'%mag)
              outfile.write('4)  %0.4f  1          #  R_e (effective radius)   [pix]\n'%r_e)
              outfile.write('5)  1  1'+'          #  Sersic index n (de Vaucouleurs n=4)\n')
              outfile.write('9)  %0.4f   1          #  Axis ratio (b/a)\n'%e)
              outfile.write('10)  %0.4f   1        #  Position angle (PA) [deg: Up=0, Left=90]\n'%PA)
              outfile.write('Z) 0   '+'                      #  Skip this model in output image?  (yes=1, no=0)')

              outfile.close()
