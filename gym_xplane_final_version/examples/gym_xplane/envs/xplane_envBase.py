import gym
from scipy.spatial.distance import pdist, squareform
import math

import gym_xplane.xpc as xpc
import gym_xplane.parameters as parameters
import gym_xplane.space_definition as envSpaces
import numpy as np
import itertools
from time import sleep


class XplaneEnv(gym.Env):

	def __init__(self, target_values, tolerance, max_episode_steps=303, test=False):

		self.CLIENT = None
		envSpace = envSpaces.xplane_space()

		self.action_space = envSpace._action_space()
		self.observation_space = envSpace._observation_space()
		self.ControlParameters = parameters.getParameters()
		self.target_values = target_values
		self.curr_target_values = []
		self.tolerance = tolerance
		self.successful = False  # Represents that agent has achieved target successfully
		self.done = False  # Just shows the end of an episode, does not care about success.
		self.current_step = 0
		self.crashed = False
		self.max_episode_steps = max_episode_steps

		self.statelength = 10
		# self.actions = [0, 0, 0, 0]
		self.test = test
		try:
			self.CLIENT = xpc.XPlaneConnect()
		except:
			print("connection error. Check your paramters")
		print('I am client', self.CLIENT)

	def close(self):
		self.CLIENT.close()

	def step(self, actions):
		self.current_step += 1
		reward = 0
		info = "*******************"
		# Might wanna add the testing step later on
		self.CLIENT.pauseSim(True)  # pauseSim(2) simply toggles between Pause and Unpause state.
		self.CLIENT.sendCTRL(actions)
		sleep(0.0003)
		self.CLIENT.pauseSim(False)

		# 	Following sleep is to let the aircraft move and environment to change.
		sleep(1.0)

		self.CLIENT.pauseSim(True)  # This pause is to make sure that environment does not change while we are
		# performing computations.
		self.observation_space = self.getObservationSpace()
		reward = self.getReward()
		return self.observation_space, reward, self.done, info

	def reset(self):
		"""
		Reset environment and setup for new episode.
		Returns:
			initial state of reset environment.
		"""
		self.done = False
		self.current_step = 0
		self.crashed = False
		self.successful = False

	def getObservationSpace(self):
		"""
	        1. Indicated Airspeed (kias) (0-300)
	        2. Vertical Speed (m/s) (-200 - 200)
	        3. Altitude (m) (0-10000)
	        4. Pitch (deg) (-180-180) (I think this is the range)
	        5. Roll (deg) (-180-180)
	        6. Heading (deg) (-180-180)
	        7. Alpha - Angle of Attack (deg) (-180-180)
	        8. Beta - Sideslip (deg) (-180-180)
        """

		observation_space_dict = self.ControlParameters.observationSpaceDict
		return np.array(self.CLIENT.getDREFs(observation_space_dict))

	def getActionSpace(self):
		"""
        **********************
        Defining my own action space as:
        1. Latitudinal Stick - Elevator [-1, -1]
        2. Longitudinal Stick - Aileron [-1, -1]
        3. Rudder Pedal - Yaw [-1, 1]
        4. Throttle [-1, 1]. -1 = minimum throttle setting. I will set it as -1/4 so that engine doesnt shutdown.
        """

		action_space_temp = self.CLIENT.getCTRL
		acion_space = action_space_temp[:4]

		return np.array(acion_space)

	def getReward(self):
		reward = -1  # For every step it will give it at least -1 reward
		self.checkTerminalState()

		if self.crashed:
			reward -= 1000

		elif self.successful:
			reward += 1000

		elif self.done and not self.successful:
			reward -= 500
		else:
			heading_reward = -math.sqrt(abs(self.target_values[0] ** 2 - self.curr_target_values[0] ** 2))
			altitude_reward = -math.sqrt(abs((self.target_values[1]/1000) ** 2 - (self.curr_target_values[1]/1000) **2))
			reward = reward + heading_reward + altitude_reward

		return reward

	def checkTerminalState(self, ):
		crashed_drefs = self.ControlParameters.crashDict
		curr_target_var_drefs = self.ControlParameters.currTargetVar
		time_drefs = self.ControlParameters.timesDict
		drefs = crashed_drefs + curr_target_var_drefs + time_drefs
		drefs_values = self.CLIENT.getDREFs(drefs)

		crashed_values = [i[0] for i in drefs_values[:len(crashed_drefs)]]
		self.curr_target_values = [i[0] for i in drefs_values[len(crashed_drefs):len(crashed_drefs) +
		                                                                      len(curr_target_var_drefs)]]
		time_values = [i[0] for i in drefs_values[len(crashed_drefs) + len(curr_target_var_drefs) +
		                                       len(curr_target_var_drefs):]]

		# This is the core logic for determining whether the plane has crashed or not
		# Checks if plane has crashed
		if crashed_values[0] == 1:
			self.done = True
			self.successful = False
			return

		# Checks if the values are out of our tolerance limits
		target_bool = True
		for i in range(len(self.curr_target_values)):
			if not ((self.target_values[i] - self.tolerance[i]) < self.curr_target_values[i] < (self.target_values[i] +
			                                                                                    self.tolerance[i])):
				target_bool = False

		# If the values are within tolerance limits and number of steps have not exceeded max_steps them successful
		# else
		# unsuccessful.

		if self.current_step == self.max_episode_steps:
			self.done = True
		if target_bool:
			self.successful = True
			self.done = True

	def _get_info(self):
		"""Returns a dictionary contains debug info"""
		# return {'control Parameters': self.ControlParameters, 'actions': self.action_space}
		pass

	def render(self, mode='human', close=False):
		pass