import numpy as np
import random
import gym

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers.legacy import Adam

import tensorflow.keras as tf
from keras import __version__
tf.__version__ = __version__


from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory



env = gym.make("CartPole-v1", render_mode="human")

states = env.observation_space.shape[0]
actions = env.action_space.n


model = Sequential()
model.add(Flatten(input_shape= (1, states)))
model.add(Dense(24, activation="relu"))
model.add(Dense(24, activation="relu"))
model.add(Dense(2, activation="linear"))

agent=DQNAgent(
    model=model,
    memory=SequentialMemory(limit=50000,window_length=1),
    policy=BoltzmannQPolicy(),
    nb_actions = actions,
    nb_steps_warmup=10,
    target_model_update=0.01
)

agent.compile(Adam(lr=0.001), metrics=["mae"])
agent.fit(env, nb_steps=100000, visualize=False, verbose=1)

results = agent.test(env, nb_episodes=10, visualize=True)

print(np.mean(results.history["episode_reward"]))

env.close()

# episodes = 10

# for episode in range(1, episodes+1):
#     state = env.reset()
#     done = False
#     score = 0

#     while not done:
#         action = random.choice([0,1])
#         _, reward, done, _ = env.step(action)
#         score += reward
#         env.render()

#     print(f'Episode {episode} ,Score {score}')

# env.close()