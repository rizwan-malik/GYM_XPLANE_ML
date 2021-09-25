import numpy as np
from gym import spaces
import gym


class xplane_space():

	def _action_space(self):
		"""
        **********************
        Defining my own action space as:
        1. Latitudinal Stick - Elevator [-1, -1]
        2. Longitudinal Stick - Aileron [-1, -1]
        3. Rudder Pedal - Yaw [-1, 1]
        4. Throttle [-1, 1]. -1 = minimum throttle setting. I will set it as -1/4 so that engine doesnt shutdown.
        """

		return spaces.Box(np.array([-1, -1, -1, -1 / 4]), np.array([1, 1, 1, 1]))

	def _observation_space(self):
		"""
        **********************
        Defining my own observation space as:
        1. Indicated Airspeed (kias) (0-300)
        2. Vertical Speed (m/s) (-200 - 200)
        3. Altitude (m) (0-10000)
        4. Pitch (deg) (-180-180) (I think this is the range)
        5. Roll (deg) (-180-180)
        6. Heading (deg) (-180-180)
        7. Alpha - Angle of Attack (deg) (-180-180)
        8. Beta - Sideslip (deg) (-180-180)
        """

		return spaces.Box(np.array([0, -200, 0, -180, -180, -180, -180, -180]), np.array([300, 200, 10000, 180,
		                                                                                     180, 180, 180, 180]))
