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
import secrets
import sys
import os.path
import time
from dataclasses import dataclass, field
import random
import os
import numpy as np


from utils import make_env, Storage, orthogonal_init


def create_envs():
    envs = {}
    for i in range(total_levels+val_levels):
        envs[i] = make_env(num_envs, num_levels=1, start_level=i)

    print(f"Created all {total_levels} levels")
    return envs

def checkfolder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# Hyperparameters. These values should be a good starting point. You can modify them later once you have a working
# implementation.


# Hyperparameters
total_steps = 20e6  # procgen recommends 25e6
num_envs = 32
num_levels = 200  # procgen recommends 200
total_levels = 200
val_levels = 10
val_interval = 122
num_steps = 256
num_epochs = 3
batch_size = 512
eps = .2
grad_eps = .5
value_coef = .5
entropy_coef = .01
played_levels = set()
level_sequence = np.random.choice(np.arange(total_levels), total_levels, False)
# choose levels above seen levels
test_sequence = np.arange(total_levels, total_levels+val_levels)
current_level = 0
beta = 0.1
gamma = 0.99
lmbda = 0.95
rho = 0.1

test_rewards = []
train_rewards = []


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

    def set_score(self, storage):
        if error_function == 1:
            self.score = one_step_TD_error(storage)
        elif error_function == 2:
            self.score = GAE(storage)
        else:
            self.score = GAE_magnitude(storage)

def GAE_magnitude(storage):
  return torch.abs(storage.advantage.mean(1)).mean(0).item()

def GAE(storage):
  return storage.advantage.mean(1).mean(0).item()

def one_step_TD_error(storage):
  advantages = np.zeros(num_steps)
  for i in range(num_steps):
    delta = (storage.reward[i] + storage.gamma * storage.value[i + 1] * (1 - storage.done[i])) - storage.value[i]
    advantages[i] = torch.abs(delta).mean(0)
  return advantages.mean(0)

def current_milli_time():
    return round(time.time() * 1000)


def get_new_level_seed():
    global played_levels

    # Reset seed
    torch.manual_seed(secrets.randbelow(10000))

    # Bernoulli distribution decides between seen and unseen levels
    d = len(played_levels)/total_levels
    play_replay_level = Bernoulli(torch.tensor([d])).sample().item()

    if len(level_sequence) == 0 or play_replay_level == 1:
        return get_replay_level()
    else:
        return get_unseen_level()


def get_unseen_level():
    global level_sequence
    level_sequence
    lvl_seed, level_sequence = int(level_sequence[-1]), level_sequence[:-1]
    return lvl_seed


def get_replay_level():
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
        probs[i] = (1-rho)*score_dist(lvl, score_sum)+rho * \
            staleness_dist(lvl, summed_episode_diffs)

    # Create distribution and retrieve an index
    lvl_index = Categorical(torch.FloatTensor(probs)).sample().item()

    # return seed of corresponding level
    return int(lvls_list[lvl_index].seed)


def update_ranks(lvls_seen):
    ranks = sorted(lvls_seen, reverse=True, key=lambda lvl: lvl.score)
    for i in range(1, len(ranks)+1):
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


games_dict = {
    "plunder": ("plunder", 4.5, 30),
    "starpilot": ("starpilot", 2.5, 64),
    "bossfight": ("bossfight", 0.5, 13),
    "caveflyer": ("caveflyer", 3.5, 12),
    "dodgeball": ("dodgeball", 1.5, 19),
    "chaser": ("chaser", 0.5, 13),
    "miner": ("miner", 1.5, 13),
    "heist": ("heist", 3.5, 10),
    "maze": ("maze", 5, 10),
    "climber": ("climber", 2, 12.6),
    "coinrun": ("coinrun", 5, 10),
    "jumper": ("jumper", 3, 10),
    "ninja": ("ninja", 3.5, 10),
    "leaper": ("leaper", 3, 10),
    "fruitbot": ("fruitbot", -1.5, 32),
    "bigfish": ("bigfish", 1, 40)
}

games = [
    "bigfish",
    "ninja",
    "jumper"
]


def choose_game(seed):
    if category == 1:
        return games_dict[default_game]
    elif category == 2:
        return games_dict[games[:2][seed % 2]]
    elif category == 3:
        return games_dict[games[1:][seed % 2]]
    else:
        return games_dict[games[seed % category]]


def normalize_reward(reward, min_score, max_score):
    return (reward-min_score)/(max_score-min_score) if category > 1 else reward


class Flatten(nn.Module):
    def forward(self, x):
        return x.view(x.size(0), -1)


class Encoder(nn.Module):
    def __init__(self, in_channels, feature_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=32,
                      kernel_size=8, stride=4), nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=4, stride=2), nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64,
                      kernel_size=3, stride=1), nn.ReLU(),
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
        self.policy = orthogonal_init(
            nn.Linear(feature_dim, num_actions), gain=.01)
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


def create_and_train_network():
    global current_level
    global train_rewards
    # Define environment
    # check the utils.py file for info on arguments
    x = current_milli_time()
    seed = get_new_level_seed()
    game, min_score, max_score = choose_game(seed)
    env = make_env(num_envs, env_name=game,
                   num_levels=1, start_level=seed)
    y = current_milli_time()
    channels_in = env.observation_space.shape[0]
    actions = env.action_space.n

    # Define network
    encoder = Encoder(channels_in, actions)
    policy = Policy(encoder, actions, actions)
    policy.cuda()

    # Define optimizer
    # these are reasonable values but probably not optimal
    optimizer = torch.optim.Adam(policy.parameters(), lr=5e-4, eps=1e-5)

    # Define temporary storage
    # we use this to collect transitions during each iteration
    storage = Storage(
        env.observation_space.shape,
        num_steps,
        num_envs,
        gamma,
        lmbda,
        normalize_advantage=False
    )

    # Run training
    obs = env.reset()
    step = 0
    # envs = create_envs()
    while step < total_steps:

        # Use policy to collect data for num_steps steps
        cur_done = np.zeros(num_envs)
        policy.eval()
        for _ in range(num_steps):
            # Use policy
            action, log_prob, value = policy.act(obs)

            # Take step in environment
            next_obs, reward, done, info = env.step(action)

            cur_done = np.logical_or(cur_done, done)

            reward = normalize_reward(reward, min_score, max_score)

            # Store data
            storage.store(obs, action, reward, done, info, log_prob, value)

            # Update current observation
            obs = next_obs

            if cur_done.all():
                new_seed = get_new_level_seed()
                # print(f"Level changed from {seed} to {new_seed}")
                env = envs[new_seed]
                obs = env.reset()

        # Add the last observation to collected data
        _, _, value = policy.act(obs)
        storage.store_last(obs, value)

        # Compute return and advantage
        storage.compute_return_advantage()

        # Optimize policy
        policy.train()
        for epoch in range(num_epochs):

            # Iterate over batches of transitions
            generator = storage.get_generator(batch_size)
            for batch in generator:
                b_obs, b_action, b_log_prob, b_value, b_returns, b_advantage = batch

                # Get current policy outputs
                new_dist, new_value = policy(b_obs)
                new_log_prob = new_dist.log_prob(b_action)

                # Clipped policy objective
                ratio = (new_log_prob - b_log_prob).exp().squeeze(0)
                m1 = ratio * b_advantage
                m2 = torch.clamp(ratio, 1.0 - eps, 1.0 + eps) * b_advantage
                pi_loss = torch.min(m1, m2).mean()

                # Clipped value function objective
                value_loss = value_coef * encoder.loss(new_value, b_advantage)

                # Entropy loss
                entropy_loss = entropy_coef * new_dist.entropy().mean()

                # Backpropagate losses
                # Eq. 9 in PPO article(https://arxiv.org/pdf/1707.06347.pdf)
                loss = - pi_loss + value_loss - entropy_loss
                loss.backward()

                # Clip gradients
                torch.nn.utils.clip_grad_norm_(policy.parameters(), grad_eps)

                # Update policy
                optimizer.step()
                optimizer.zero_grad()

         # Update stats
        step += num_envs * num_steps

        level_seed = storage.info[0][1]['level_seed']
        level = None
        if not storage.info[0][1]['level_seed'] in [x.seed for x in played_levels]:
            level = Level(seed=level_seed, last_played=current_level)
            played_levels.add(level)
        else:
            level = [
                level for level in played_levels if level_seed == level.seed][0]
            level.last_played = current_level

        # Update score of level
        level.set_score(storage)
        print(
            f'Step: {step}\tGame: {game},\tSeed: {seed},\tMean reward: {storage.get_reward(False)}\tMean error: {level.score}')
        # print(f'{step},{game},{storage.get_reward()},{level.score}')

        # Save mean reward
        last_iteration = step >= total_steps
        if current_level % val_interval == 0 or last_iteration:
            train_rewards.append(storage.get_reward(False))

            # Evaluate network
            record_and_eval_policy(policy, last_iteration)

        current_level += 1
        seed = get_new_level_seed()
        game, min_score, max_score = choose_game(seed)
        env = make_env(num_envs, env_name=game, start_level=seed, num_levels=1)
        obs = env.reset()


# Below cell can be used for policy evaluation and saves an episode to mp4 for you to view.
def record_and_eval_policy(policy, record_video):
    global test_rewards
    frames = []
    total_reward = []
    # Make evaluation environment
    # envs = create_envs()
    for seed in test_sequence:
        seed = int(seed)
        game, min_score, max_score = choose_game(seed)
        eval_env = envs[seed]
        obs = eval_env.reset()

        temp_reward = []
        # Evaluate policy
        cur_done = np.zeros(num_envs)
        policy.eval()
        for _ in range(num_steps*2):
            # Use policy
            action, log_prob, value = policy.act(obs)

            # Take step in environment
            obs, reward, done, info = eval_env.step(action)
            reward = normalize_reward(reward, min_score, max_score)
            temp_reward.append(torch.Tensor(reward))

            # Render environment and store
            if record_video:
                frame = (torch.Tensor(eval_env.render(
                    mode='rgb_array')) * 255.).byte()
                frames.append(frame)

            cur_done = np.logical_or(cur_done, done)
            # A level is played once.
            if cur_done.all():
                break

        total_reward.append(torch.stack(temp_reward).mean(1).sum(0))
        

    # Calculate average return
    total_reward = torch.stack(total_reward).mean(0)

    # Save mean reward
    test_rewards.append(total_reward)

    # Save frames as video
    if record_video:
        video_folder = f"videos/{FOLDER_NAME}"
        checkfolder(video_folder)
        frames = torch.stack(frames)
        imageio.mimsave(
            f'{video_folder}/video-{time.time()}.mp4', frames, fps=25)


def write_rewards_to_file():
    rewards_folder = f"rewards/{FOLDER_NAME}"
    checkfolder(rewards_folder)
    np.savetxt(f"{rewards_folder}/test_rewards-{time.time()}.csv",
               np.array(test_rewards), delimiter=",", fmt="%10.5f")
    np.savetxt(f"{rewards_folder}/train_rewards-{time.time()}.csv",
               np.array(train_rewards), delimiter=",", fmt="%10.5f")



if __name__ == '__main__':
    default_game = "starpilot"
    category = int(sys.argv[1])
    error_function = 0
    if len(sys.argv) > 3:
        error_function = int(sys.argv[2])
        default_game = sys.argv[3]
    error_functions = ["GAEMag", "OneStep", "GAE"]
    FOLDER_NAME = f"plr-{default_game if category == 1 else category}-{error_functions[error_function]}"
    envs = create_envs()
    create_and_train_network()
    write_rewards_to_file()
