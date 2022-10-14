import gym
import numpy as np
import random
import matplotlib.pyplot as plt

done=False
learning_rate=0.1
discount=0.9
epsilon_reduce=0.005

env=gym.make('MountainCar-v0')
env.reset()
discrete_ob=[100,100]
piece_of_obspace=(env.observation_space.high-env.observation_space.low)/discrete_ob
q_table=np.random.uniform(low=-2, high=0,size=discrete_ob+[env.action_space.n])
total_episode=500000
epsilon=1

def translate_discrete(state):
    c_state=(state-env.observation_space.low)/piece_of_obspace
    return tuple(c_state.astype(np.int64))

train_r=[]
for i in range(total_episode):
    done=False
    if epsilon-epsilon_reduce>=0:
        epsilon-=epsilon_reduce
    current_state=translate_discrete(env.reset())
    episode_r=0
    while not done:
        if random.random()>epsilon:
            action = np.argmax(q_table[current_state])
        else:action=random.randint(0,2)
        #if i%2000==0:env.render()
        ob,r,done,_=env.step(action)
        new_state=translate_discrete(ob)
        q_current = q_table[current_state][action]
        q_max=np.max(q_table[new_state])
        if not done:
            new_q=(1-learning_rate)*q_current+learning_rate*(r+discount*q_max)
        elif ob[0] >= 0.5:
            new_q=r
        q_table[current_state][action]=new_q
        episode_r+=r
        current_state=new_state
    train_r.append(episode_r)

plt.plot(range(total_episode),train_r)
plt.show()
env.close()