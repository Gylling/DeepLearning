# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xN2_zPtrx-ZVBlGVeOCgpP6ZPLQ1uD-9
"""

import imageio
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions.categorical import Categorical
from torch.distributions.uniform import Uniform
from torch.distributions.bernoulli import Bernoulli
import sys
import os.path
import time
from dataclasses import dataclass, field
import random
import os


# The cell below installs `procgen` and downloads a small `utils.py` script that contains some utility functions. You
# may want to inspect the file for more details.

from utils import make_env, Storage, orthogonal_init

FOLDER_NAME = "plr"

def checkfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

checkfolder(f"checkpoints./{FOLDER_NAME}")
checkfolder(f"videos./{FOLDER_NAME}")

# Hyperparameters. These values should be a good starting point. You can modify them later once you have a working
# implementation.

# Hyperparameters
total_steps = 20e6
num_envs = 32
num_levels = 100
start_level = 3
total_levels = 100
num_steps = 256
num_epochs = 3
batch_size = 512
eps = .2
grad_eps = .5
value_coef = .5
entropy_coef = .01
played_levels = set()
played_level_seeds = set()
current_level = 0
beta = 0.1
gamma = 0.99
lmbda = 0.95
multi_games = True

# Network definitions. We have defined a policy network for you in advance. It uses the popular `NatureDQN` encoder
# architecture (see below), while policy and value functions are linear projections from the encodings. There is
# plenty of opportunity to experiment with architectures, so feel free to do that! Perhaps implement the `Impala`
# encoder from [this paper](https://arxiv.org/pdf/1802.01561.pdf) (perhaps minus the LSTM).

@dataclass(unsafe_hash=True)
class Level:
    """Class for keeping track of levels."""
    last_played: int = field(default=False, compare=False, hash=False)
    seed: int = field(default=False, hash=True)
    score: float = field(default=False, hash=True, compare=True)
    rank = 1

    def set_score(self, advantages):
      self.score = advantages.mean().item()



def current_milli_time():
    return round(time.time() * 1000)

def get_new_level_seed():
  global played_levels
  # Bernoulli distribution decides between seen and unseen levels
  unseen_levels = [x for x in range(total_levels) if x not in played_level_seeds]
  play_replay_level = Bernoulli(torch.tensor([len(played_levels)/total_levels])).sample().item()
  if play_replay_level and len(unseen_levels) > 0:
    return get_replay_level()
  else:
    return get_unseen_level(unseen_levels)

def get_unseen_level(unseen_levels):
  global played_level_seeds
  lvl = int(random.choice(unseen_levels))
  played_level_seeds.add(lvl)
  return lvl

def get_replay_level():
  rho = 0.3
  probs = [0]*len(played_levels)
  lvls_list = list(played_levels)
  
  # Calculate ranks once and save it on levels
  update_ranks(lvls_list)

  # Calculate sums once per creation of replay distribution
  score_sum = sum_of_score_dist()
  summed_episode_diffs = sum_staleness()

  # Calculate probabilities
  for i in range(len(lvls_list)):
    lvl = lvls_list[i]
    probs[i]=(1-rho)*score_dist(lvl,score_sum)+rho*staleness_dist(lvl, summed_episode_diffs)

  # Create distribution and retrieve an index
  lvl_index = Categorical(torch.FloatTensor(probs)).sample().item()

  # return seed of corresponding level
  return int(lvls_list[lvl_index].seed)


 
def update_ranks(lvls_seen):
  ranks = sorted(lvls_seen, reverse=True, key=lambda lvl: lvl.score)
  for i in range(1,len(ranks)+1):
    ranks[i-1].rank = i

def sum_of_score_dist():
  sum = 0
  for lvl in played_levels:
    sum += (1/lvl.rank)**(1/beta)
  return sum if sum > 0 else 1

def score_dist(lvl, score_sum):
      return (1/lvl.rank)**(1/beta)/score_sum

def sum_staleness():
  summed_episode_diffs = 0
  for lvl in played_levels:
    summed_episode_diffs += current_level - lvl.last_played
  
  return summed_episode_diffs if summed_episode_diffs > 0 else 1

def staleness_dist(lvl, summed_episode_diffs):
  staleness = current_level - lvl.last_played
  staleness_weight = staleness/summed_episode_diffs
  return staleness_weight

def choose_game(seed):
    if multi_games: 
        return [
            "bigfish",
            "bossfight",
            "caveflyer",
            "chaser",
            "climber",
            "coinrun",
            "dodgeball",
            "fruitbot",
            "heist",
            "jumper",
            "leaper",
            "maze",
            "miner",
            "ninja",
            "plunder",
            "starpilot",
        ][seed % 16]
    else:
        return "starpilot"


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)


class Encoder(nn.Module):
    def __init__(self, in_channels, feature_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=32, kernel_size=8, stride=4), nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2), nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1), nn.ReLU(),
            Flatten(),
            nn.Linear(in_features=1024, out_features=feature_dim), nn.ReLU()
        )
        self.apply(orthogonal_init)

    def forward(self, x):
        return self.layers(x)

    def loss(self, q_outputs, q_targets):
        return F.mse_loss(q_outputs, q_targets)


class Policy(nn.Module):
    def __init__(self, encoder, feature_dim, num_actions):
        super().__init__()
        self.encoder = encoder
        self.policy = orthogonal_init(nn.Linear(feature_dim, num_actions), gain=.01)
        self.value = orthogonal_init(nn.Linear(feature_dim, 1), gain=1.)

    def act(self, x):
        with torch.no_grad():
            x = x.cuda().contiguous()
            dist, value = self.forward(x)
            action = dist.sample()
            log_prob = dist.log_prob(action)

        return action.cpu(), log_prob.cpu(), value.cpu()

    def forward(self, x):
        x = self.encoder(x)
        logits = self.policy(x)
        value = self.value(x).squeeze(1)
        dist = torch.distributions.Categorical(logits=logits)

        return dist, value

def create_network_from_checkpoint(path):
    global current_level
    # Define environment
    # check the utils.py file for info on arguments
    env = make_env(num_envs, env_name=choose_game(start_level), num_levels=1, start_level=start_level)
    channels_in = env.observation_space.shape[0]
    actions = env.action_space.n

    # Define network
    encoder = Encoder(channels_in, actions)
    policy = Policy(encoder, actions, actions)
    policy.cuda()

    policy.load_state_dict(torch.load(path))

    return policy


# Below cell can be used for policy evaluation and saves an episode to mp4 for you to view.
def record_and_eval_policy(policy):
    # Make evaluation environment
    eval_env = make_env(num_envs, env_name=choose_game(random.randint(0,15)), start_level=num_levels, num_levels=num_levels)
    obs = eval_env.reset()

    frames = []
    total_reward = []

    # Evaluate policy
    policy.eval()
    for _ in range(512):
        # Use policy
        action, log_prob, value = policy.act(obs)

        # Take step in environment
        obs, reward, done, info = eval_env.step(action)
        total_reward.append(torch.Tensor(reward))

        # Render environment and store
        frame = (torch.Tensor(eval_env.render(mode='rgb_array')) * 255.).byte()
        frames.append(frame)

    # Calculate average return
    total_reward = torch.stack(total_reward).sum(0).mean(0)
    print('Average return:', total_reward)

    # Save frames as video
    frames = torch.stack(frames)
    imageio.mimsave(f'{FOLDER_NAME}-video-backup-{time.time()}', frames, fps=25)
    imageio.mimsave(f'videos/{FOLDER_NAME}/video-{time.time()}', frames, fps=25)


complete_policy = create_network_from_checkpoint("checkpoints/plr/checkpoint-1637047482.9451299.pt")
record_and_eval_policy(complete_policy)