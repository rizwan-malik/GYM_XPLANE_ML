import argparse
import gym
import gym_xplane


if __name__ == '__main__':
	# This is simply to setup the environment and connection with x-plane 11.
	parser = argparse.ArgumentParser()

	parser.add_argument('--clientAddr', help='xplane host address', default='0.0.0.0')
	parser.add_argument('--xpHost', help='x plane port', default='127.0.0.1')
	parser.add_argument('--xpPort', help='client port', default=49009)
	parser.add_argument('--clientPort', help='client port', default=1)

	args = parser.parse_args()

	env = gym.make('gymXplane-v2')
	env.clientAddr = args.clientAddr
	env.xpHost = args.xpHost
	env.xpPort = args.xpPort
	env.clientPort = args.xpPort

	print(env.action_space.sample())
	print(env.observation_space.sample())

	env.reset()
