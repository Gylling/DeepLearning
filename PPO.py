import torch
import imageio
import torch.nn as nn
import torch.nn.functional as F
import random
import time
import os
import sys
import numpy as np

# The cell below installs `procgen` and downloads a small `utils.py` script that contains some utility functions. You
# may want to inspect the file for more details.

# ! pip install procgen
# ! wget https://raw.githubusercontent.com/nicklashansen/ppo-procgen-utils/main/utils.py

from utils import make_env, Storage, orthogonal_init


def checkfolder(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


# Hyperparameters. These values should be a good starting point. You can modify them later once you have a working
# implementation.
# Hyperparameters
total_steps = 20e6
num_envs = 32
num_levels = 200
val_levels = 10
val_interval = 122
num_steps = 256
num_epochs = 3
batch_size = 512
eps = .2
grad_eps = .5
value_coef = .5
entropy_coef = .01
test_rewards = []
train_rewards = []
# choose levels above seen levels
test_sequence = np.arange(num_levels, num_levels+val_levels)


# Network definitions. We have defined a policy network for you in advance. It uses the popular `NatureDQN` encoder
# architecture (see below), while policy and value functions are linear projections from the encodings. There is
# plenty of opportunity to experiment with architectures, so feel free to do that! Perhaps implement the `Impala`
# encoder from [this paper](https://arxiv.org/pdf/1802.01561.pdf) (perhaps minus the LSTM).
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


games = [
    "starpilot",
    "maze",
    "heist"
]


def choose_game(seed):
    if category == 1:
        return default_game
    elif category == 2:
        return games[:2][seed % 2]
    elif category == 3:
        return games[1:][seed % 2]
    else:
        return games[seed % category]


def create_and_train_network():
    global train_rewards
    # Define environment
    # check the utils.py file for info on arguments
    count = 0
    current_level = 0
    game = choose_game(count)
    env = make_env(num_envs, env_name=game, num_levels=num_levels)
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
        num_envs
    )

    # Run training
    obs = env.reset()
    step = 0
    while step < total_steps:

        # Use policy to collect data for num_steps steps
        policy.eval()
        for _ in range(num_steps):
            # Use policy
            action, log_prob, value = policy.act(obs)

            # Take step in environment
            next_obs, reward, done, info = env.step(action)

            # Store data
            storage.store(obs, action, reward, done, info, log_prob, value)

            # Update current observation
            obs = next_obs

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
        print(f'{step},{game},{storage.get_reward()}')

        # Save mean reward
        last_iteration = step >= total_steps
        if current_level % val_interval == 0 or last_iteration:
            train_rewards.append(storage.get_reward())

            # Evaluate network
            record_and_eval_policy(policy, last_iteration)

        count = (count + 1) % num_levels
        current_level += 1
        game = choose_game(count)
        env = make_env(num_envs, env_name=game,
                       start_level=count, num_levels=1)
        obs = env.reset()


# Below cell can be used for policy evaluation and saves an episode to mp4 for you to view.
def record_and_eval_policy(policy, record_video):
    global test_rewards
    frames = []
    total_reward = []

    # Make evaluation environment
    for seed in test_sequence:
        seed = int(seed)
        game = choose_game(seed)
        eval_env = make_env(num_envs, env_name=game,
                            num_levels=1, start_level=seed)
        obs = eval_env.reset()

        temp_reward = []
        # Evaluate policy
        policy.eval()
        for _ in range(num_steps*2):
            # Use policy
            action, log_prob, value = policy.act(obs)

            # Take step in environment
            obs, reward, done, info = eval_env.step(action)
            temp_reward.append(torch.Tensor(reward))

            # Render environment and store
            if record_video:
                frame = (torch.Tensor(eval_env.render(
                    mode='rgb_array')) * 255.).byte()
                frames.append(frame)

            # A level is played once.
            if done.all():
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
    if len(sys.argv) > 2:
        default_game = sys.argv[2]
    FOLDER_NAME = f"ppo-{default_game if category == 1 else category}"
    create_and_train_network()
    write_rewards_to_file()
