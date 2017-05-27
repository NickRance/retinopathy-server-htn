import time
import os
from path import Path
def clean():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	d = Path(dir_path)
	files = d.walkfiles("*.jpeg")
	starttime=time.time()
	for file in files:
	    file.remove()
	    print "Removed {} file".format(file)
	    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
	return "Done"