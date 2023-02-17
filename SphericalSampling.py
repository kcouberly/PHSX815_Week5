import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from Random import Random


#rejection sampling for points in the cubic region [1,1,1] covering 1/8th of the volume of a sphere
if __name__ == "__main__":

	#set default number of samples
	Nsample = 10000

	# read the user-provided seed from the command line (if there)
	if '-Nsample' in sys.argv:
		p = sys.argv.index('-Nsample')
		Nsample = int(sys.argv[p+1])
	if '-h' in sys.argv or '--help' in sys.argv:
		print ("Usage: %s -Nsample [number]" % sys.argv[0])
		print
		sys.exit(1) 

	nAccept = 0
	nTotal = 0
	
	# accepted values
	Xaccept = []
	Yaccept = []
	Zaccept = []

	# reject values
	Xreject = []
	Yreject = []
	Zaccept = []

	# sample number
	isample = []
	# calculated values of 4/3 Pi (per sample)
	calcPi = []

	random = Random()

	idraw = max(1,int(Nsample)/100000)
	for i in range(0,Nsample):
		X = random.rand()
		Y = random.rand()
		Z = random.rand()

		nTotal += 1
		if(X*X + Y*Y + Z*Z <= 1): #accept if inside
			nAccept += 1
			if(i % idraw == 0):
				Xaccept.append(X)
				Yaccept.append(Y)
		else: # reject if outside
			if(i % idraw == 0):
				Xreject.append(X)
				Yreject.append(Y)
		if(i % idraw == 0):
			isample.append(nTotal)
            #1/1/1 radius cube contains 1/8 of sphere
			calcPi.append(8*nAccept/nTotal)



	#plot calculated pi vs sample number
	fig1 = plt.figure()
	plt.plot(isample,calcPi)
	plt.ylabel(r'Approximate 4/3 $\pi$')
	plt.xlabel("Sample number")
	plt.xlim(0,isample[len(isample)-1])
	ax = plt.gca()
	ax.axhline(y=4/3*np.arccos(-1),color='green',label=r'true 4/3 $\pi$')
	plt.title(r'Approximation of 4/3 $\pi$ as a function of number of samples')
	plt.legend()












