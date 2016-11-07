# coding=utf8
# import gym
# env = gym.make('CartPole-v0')
# for _ in range(1000):
#   env.render()
#   action = env.action_space.sample() # your agent here (this takes random actions)
#   observation, reward, done, info = env.step(action)
# # env.reset()
# # env.render()
#
# import gym
# env = gym.make("Taxi-v1")
# observation = env.reset()
# for _ in range(1000):
#   env.render()
#   action = env.action_space.sample() # your agent here (this takes random actions)
#   observation, reward, done, info = env.step(action)


# 12whz

# choices = [
#               'LinearSvm',
#               'GridSearchSvm',
#               'GMM',
#               'RadialSvm',
#               'DecisionTree',
#               'GaussianNB',
#               'DBN'],
# help = 'The type of classifier to use.',
# default = 'LinearSvm'

import gym
env = gym.make('CartPole-v0') #实例化一个 CartPole 环境
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render() #更新动画
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action) #推进一步
        if done:
            break



# import gym
#
# env = gym.make('LunarLander-v2')
# env.reset()
# env.render()