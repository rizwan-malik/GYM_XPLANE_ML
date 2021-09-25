
def getParameters():
	'''
	This function is used to define training parameters.
	This is separated from the main loop pf the program for ease of reference.
	There are many  state variables
	so that having them in a separate file is a good idea.
	'''

	''''
	I am going to redefine everything in these parameters to make it more intuitive and easy to understand. I will 
	define 3 lists for 1. Action Space Parameters, 2. Observation Space Parameters and 3. Resetting Parameters
	'''

	# Global dictionary for acrquiring the parameters for the training
	globalDictionary = {
		"observationSpaceDict": ["sim/flightmodel/position/indicated_airspeed", "sim/flightmodel/position/vh_ind",
		                         "sim/flightmodel/position/elevation", "sim/flightmodel/position/theta",
		                         "sim/flightmodel/position/phi", "sim/flightmodel/position/true_psi",
		                         "sim/flightmodel/position/alpha", "sim/flightmodel/position/beta"],

		"observationSpaceValues": [],

		"actionSpaceValues": [],  # This will be left blank here and assigned through getCTRL

		# We can change this later on to suit other reward functions as well.
		"currTargetVar": ["sim/flightmodel/position/true_psi", "sim/flightmodel/position/elevation"],
		"desTargetVar": [0, 0],

		"crashDict": ["sim/flightmodel2/misc/has_crashed", "sim/flightmodel2/gear/on_ground"],
		"successful": False,  # represents that we've achieved the target without crashing or running out of time.

		"finished": False,

		"timesDict": ["sim/time/total_running_time_sec", "sim/time/total_flight_time_sec"],
		"timesValues": []
	}

	globalDictionary = dotdict(globalDictionary)  # make the dot notation for dictionary possible

	return globalDictionary

class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__
