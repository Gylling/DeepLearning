import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# list of paths for the training on 4 games
layout_colorway = ['#990000', '#2F3EEA', '#1FD082', '#030F4F']

"""
n = number of games

Plot 1..n:
- GAE Mag
- GAE
- TD-Error
- PPO

1 plot per spil
"""

file_dict = {
    "PPO": {
        "Different": {"test": "rewards/ppo-2/test_rewards-1640104719.3333845.csv", "train": "rewards/ppo-2/train_rewards-1640104719.3389702.csv"},
        "Similar": {"test": "rewards/ppo-3/test_rewards-1640146812.2935631.csv", "train": "rewards/ppo-3/train_rewards-1640146812.2987802.csv"}
    },
    "PLR GAE Magnitude": {
        "Different": {"test": "rewards/plr-2-GAEMag/test_rewards-1640115587.315737.csv", "train": "rewards/plr-2-GAEMag/train_rewards-1640115587.3201234.csv"},
        "Similar": {"test": "rewards/plr-3-GAEMag/test_rewards-1640261008.7316384.csv", "train": "rewards/plr-3-GAEMag/train_rewards-1640261008.7395754.csv"}
    }
}

# x = np.linspace(1, 22, 22)


def generate_graph(fig, colors, ax, ax_coord, list_of_paths, label_names, title="Results", xlabel="Steps in M",
                   ylabel="Rewards"):
    # 2: Loop through paths
    for path, label, color in zip(list_of_paths, label_names, colors):
        if(len(path) == 0):
            continue
        else:
            df = pd.read_csv(path, header=None)
        print(path)
        x = np.linspace(1, 22, len(df.index))
        print(len(df.index))
        ax[ax_coord].plot(x, df, label=label, c=color)

        ax[ax_coord].set_xlabel(xlabel)
        ax[ax_coord].set_ylabel(ylabel)

        ax[ax_coord].set_title(title)


fig, axs = plt.subplots(2, sharey=False)
# 1: Initialize variables
# DO THIS 4 times, one for each subplot

label_names = [
    "PPO",
    "PLR GAE Magnitude"
]

coords = [0,1]
# Starpilot
games = [
    "Different",
    "Similar"
]

for game, coord in zip(games, coords):
    generate_graph(colors=layout_colorway, fig=fig, ax=axs, ax_coord=coord, list_of_paths=[
        file_dict["PPO"][game]["test"],
        file_dict["PLR GAE Magnitude"][game]["test"]
    ], label_names=label_names, title=game)


handles, labels = axs[1].get_legend_handles_labels()
fig.legend(handles, labels, loc=(0.68, 0.45), ncol=1)

fig.tight_layout()
plt.savefig('multi_rewards.png')
fig.show()
