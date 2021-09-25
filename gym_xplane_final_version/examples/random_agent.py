import argparse

import gym_xplane
#import p3xpc 
import gym



class RandomAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self):
        return self.action_space.sample()


if __name__ == '__main__':
    env = gym.make('gymXplane-v2')

    agent = RandomAgent(env.action_space)

    episodes = 0
    while episodes < 50:
        # obs = env.reset()
        done = False
        while not done:
            action = agent.act()
            obs, reward, done, _ = env.step(action) 

            print(obs, reward, done)
            #print(done)
        episodes += 1

    env.close()
