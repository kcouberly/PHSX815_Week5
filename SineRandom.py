import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from Random import Random 

#global variables
bin_width = 0.
Xmin = 0.
Xmax = 1.
random = Random()

def Sine(x):
    return (1./np.sqrt(2.*np.arccos(-1.))*np.sin(np.pi*x))

def PlotSine(x,bin_width):
	return bin_width*Sine(x)

# Uniform (flat) distribution scaled to Sinesian max
# Note: multiply by bin width to match histogram
def Flat(x):
	return 1./np.sqrt(2*np.arccos(-1.))
	
def PlotFlat(x,bin_width):
	return bin_width*Flat(x)

# Get a random X value according to a flat distribution
def SampleFlat():
	return Xmin + (Xmax-Xmin)*random.rand()


#main function
if __name__ == "__main__":


	# default number of samples
	Nsample = 100

	doLog = False
	doExpo = False

	# read the user-provided seed from the command line (if there)
	#figure out if you have to have -- flags before - flags or not
	if '-Nsample' in sys.argv:
		p = sys.argv.index('-Nsample')
		Nsample = int(sys.argv[p+1])
	if '-range' in sys.argv:
		p = sys.argv.index('-range')
		Xmax = float(sys.argv[p+1])
		Xmin = -float(sys.argv[p+1])
	if '--log' in sys.argv:
		p = sys.argv.index('--log')
		doLog = bool(sys.argv[p])
	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s [-Nsample] number [-range] Xmax [--log] " % sys.argv[0])
		print
		sys.exit(1)  


	data = []
	Ntrial = 0.
	i = 0.
	while i < Nsample:
		Ntrial += 1
		X = SampleFlat()
		R = Sine(X)/Flat(X)
		rand = random.rand()
		if(rand > R): #reject if outside
			continue
		else: #accept if inside
			data.append(X)
			i += 1 #increase i and continue
	
	if Ntrial > 0:
		print("Efficiency was",float(Nsample)/float(Ntrial))


	#normalize data for probability distribution
	weights = np.ones_like(data) / len(data)
	n = plt.hist(data,weights=weights,alpha=0.3,label="samples from f(x)",bins=100)
	plt.ylabel("Probability / bin")
	plt.xlabel("x")
	bin_width = n[1][1] - n[1][0]
	hist_max = max(n[0])

	if not doLog:
		plt.ylim(min(bin_width*Sine(Xmax),1./float(Nsample+1)),
		1.5*max(hist_max,bin_width*Sine(0)))
	else:
		plt.ylim(min(bin_width*Sine(Xmax),1./float(Nsample+1)),
		80*max(hist_max,bin_width*Sine(0)))
		plt.yscale("log")


	x = np.arange(Xmin,Xmax,0.001)
	y_norm = list(map(PlotSine,x,np.ones_like(x)*bin_width))
	# y_norm = list(map(PlotSine(x,bin_width))
	plt.plot(x,y_norm,color='green',label='target f(x) - Sine function')
	y_flat = list(map(PlotFlat,x,np.ones_like(x)*bin_width))
	
plt.plot(x,y_flat,color='red',label='proposal g(x)')
plt.title("Density estimation with Monte Carlo")
plt.legend()
plt.show()