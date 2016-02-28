import sys
#from test import doSomething
from mlb import thali

class sport(object):
	infile = sys.argv[1]
	outfile = sys.argv[2]
	
	def main(self):
		if self.infile == "testing.tsv":
			thali(self.infile,self.outfile)
		else:
			print 'failed!'	

if __name__=="__main__":
	sport().main()