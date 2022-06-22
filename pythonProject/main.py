import gym
from stable_baselines3 import PPO

env = gym.make('CartPole-v0')
module=PPO('Mlppolicy',env)
module.learn(10000)

for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        action,_=module.predict(observation)
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()