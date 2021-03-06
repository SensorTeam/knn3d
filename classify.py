"""
# input array of data
# append/store it the database
# load model
# predict using model
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
from rgb_to_hsv import *
import sys
sys.path.append('..')
from config import *

# Classifies based on pre-existing loaded training set
# Filename, class, R, G, B
def classify(data):
	# load model and transform
	model = pickle.load(open(PATH_KNN_MODEL, 'rb'))
	scaler = pickle.load(open(PATH_SCALER_TRANSFORM, 'rb'))
	# print("\n=================================================")
	# print("LOADED DATA = %s"% data)
	
	# label?
	try:
		c = int(data[1])
	except:
		c = 'None'

	########### Check that macros are valid
	bit = [8, 14]
	cs = ["RGB", "HSV"]
	coords = ["polar", "cartesian"]
	weights = ["uniform", "distance"]

	if BIT in bit and COLORSPACE in cs and COORD_SYSTEM in coords and WEIGHT in weights:
		pass
	else:
		raise ValueError("Incorrect macros parsed. Check config.py")

	# transform the data using desired method
	transformed_data = transform(np.asarray(data))

	# standardise using scaler
	newX = np.asarray(transformed_data)
	# Standardise data (transform based on training data)
	newX = newX.reshape(1,-1)
	newX = scaler.transform(newX)

	# If 2D, plot the new point in classification space
	if NORMALISED or COLORSPACE == "HSV":
		ax = pickle.load(open(PATH_PLOT, "rb"))
		plt.scatter(newX[0][0], newX[0][1], s=250,marker='*', facecolors='w', edgecolors='k',linewidths=1)
		# plt.show()
		plt.close()

	# make prediction
	p = model.predict(newX)[0]
	neighbour_dist = model.kneighbors(newX)[0]
	
	# RETURN RESULTS
	returnstr = "==========================\nTransformed data: " +str(transformed_data)
	returnstr += "\nFILE: %s\nLABEL: %s\n"%(data[0],str(c))
	
	# if closest neighbour is too far away, possibly new class
	if neighbour_dist[0][0] > 0.5:
		returnstr += "Distance from closest neighbour: %f\n" % neighbour_dist[0][0]
		returnstr += "Class unclear\n"
	else:
		returnstr += "PREDICTION: %i\n"%(p)
	return returnstr, p


# transform data using desired method from flags
def transform(data):
	X = data[2:].astype(np.float)

	# data is always given in original rgb values
	r,g,b = X

	# normalise for 2D RGB
	if COLORSPACE == "RGB":
		if NORMALISED:			# 2D r/t, g/t, b/t
			return normalise(r,g,b)
		else:
			return [r,g,b]

	# transform to 2D hue and saturation
	else:
		hsv = rgb_to_hsv(r,g,b, BIT)
		if COORD_SYSTEM == "polar":		# polar coordinates
			pol = pol2cart(hsv[0], hsv[1]*100)
			return pol
		else:		# cartesian
			return [hsv[0], hsv[1]*100]
	

def normalise(r,g,b):
	tot = r+g+b
	r,g,b = r/tot, g/tot, b/tot
	x = 1/math.sqrt(2)*(r-g)
	y = 1/math.sqrt(6)*(2*b-r-g)
	return [x,y]

