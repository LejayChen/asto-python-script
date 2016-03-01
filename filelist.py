import sys,os,re
import aplpy
from termcolor import colored

#select a path
if len(sys.argv)==1:
	path = '.'
else:
	if os.path.exists(sys.argv[1]):
		path = sys.argv[1]
	else:
		print 'No such directory'
		sys.exit()

#preprocess: select orignial images in the path
for dirname, dirnames, filenames in os.walk(path):
	pattern = re.compile(r'\d\d\d\d\W\w\Wfits')
	for filename in filenames:
		match = pattern.match(filename)
		if not match:
			filenames.remove(filename)

#prepare the indices
vcc_indices = []
for filename in filenames:
	raw_index = filename[:4]
	if raw_index not in vcc_indices:
		vcc_indices.append(raw_index)

filelist = open('files','w')
for index in vcc_indices:
	filelist.write(str(index)+'\n')

filelist.close()

