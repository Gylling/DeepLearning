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
    "ppo": {
        "starpilot": {"test": "rewards/ppo-starpilot/test_rewards-1638731995.6470635.csv", "train": "rewards/ppo-starpilot/train_rewards-1638731995.6521041.csv"},
        "heist": {"test": "rewards/ppo-heist/test_rewards-1638789892.8010404.csv", "train": "rewards/ppo-heist/train_rewards-1638789892.8077898.csv"},
        "maze": {"test": "rewards/ppo-maze/test_rewards-1638797839.9878278.csv", "train": "rewards/ppo-maze/train_rewards-1638797839.9934442.csv"}
    },
    "plr-td": {
        "starpilot": {"test": "rewards/plr-starpilot-OneStep/test_rewards-1638828612.513363.csv", "train": "rewards/plr-starpilot-OneStep/train_rewards-1638828612.5180354.csv"},
        "heist": {"test": "", "train": ""},
        "maze": {"test": "rewards/plr-maze-OneStep/test_rewards-1638809491.8857126.csv", "train": "rewards/plr-maze-OneStep/train_rewards-1638809491.8898652.csv"}
    },
    "plr-gae": {
        "starpilot": {"test": "rewards/plr-starpilot-GAE/test_rewards-1638867795.0073612.csv", "train": "rewards/plr-starpilot-GAE/train_rewards-1638867795.0123215.csv"},
        "heist": {"test": "", "train": ""},
        "maze": {"test": "", "train": ""}
    },
    "plr-gaem": {
        "starpilot": {"test": "rewards/plr-starpilot-GAEMag/test_rewards-1638825768.9538002.csv", "train": "rewards/plr-starpilot-GAEMag/train_rewards-1638825768.960656.csv"},
        "heist": {"test": "", "train": ""},
        "maze": {"test": "rewards/plr-maze-GAEMag/test_rewards-1638815208.0819683.csv", "train": "rewards/plr-maze-GAEMag/train_rewards-1638815208.0867116.csv"}
    }
}

x = np.linspace(1, 22, 22)


def generate_graph(fig, colors, ax, ax_coord, list_of_paths, label_names, title="Results", xlabel="Steps in M",
                   ylabel="Rewards"):
    ax_x, ax_y = ax_coord
    # 2: Loop through paths
    for path, label, color in zip(list_of_paths, label_names, colors):
        if(len(path) == 0):
            continue
        else:
            df = pd.read_csv(path, header=None)
        ax[ax_x, ax_y].plot(x, df, label=label, c=color)

        ax[ax_x, ax_y].set_xlabel(xlabel)
        ax[ax_x, ax_y].set_ylabel(ylabel)

        ax[ax_x, ax_y].set_title(title)


fig, axs = plt.subplots(2, 2, sharey=False)
# 1: Initialize variables
# DO THIS 4 times, one for each subplot

label_names = [
    "ppo",
    "plr-td",
    "plr-gae",
    "plr-gaem"
]

coords = [(0, 0), (0, 1), (1, 0)]
# Starpilot
games = [
    "starpilot",
    "maze",
    "heist"
]

for game, coord in zip(games, coords):
    generate_graph(colors=layout_colorway, fig=fig, ax=axs, ax_coord=coord, list_of_paths=[
        file_dict["ppo"][game]["test"],
        file_dict["plr-td"][game]["test"],
        file_dict["plr-gae"][game]["test"],
        file_dict["plr-gaem"][game]["test"]
    ], label_names=label_names, title=game)

fig.delaxes(axs[1][1])

# handles, labels = axs[1, 1].get_legend_handles_labels()
# axs[0, 0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
# fig.legend(handles, labels, loc=(0.5, 0), ncol=3)

fig.tight_layout()
plt.savefig('rewards.png')
fig.show()
plt.clf()

"""
Figure 2
"""

games_dict = {
    "starpilot": ("starpilot", 2.5, 64),
    "heist": ("heist", 3.5, 10),
    "maze": ("maze", 5, 10)
}

colors = {}
for color, label in zip(layout_colorway, label_names):
    colors[label] = color

for label in label_names:
    df_train = [[] for i in range(3)]
    df_test = [[] for i in range(3)]
    for i, game in enumerate(games):
        name, min_score, max_score = games_dict[game]
        test_path = file_dict[label][game]["test"]
        train_path = file_dict[label][game]["train"]
        if len(test_path) > 0:
            test = pd.read_csv(test_path, header=None)
            train = pd.read_csv(train_path, header=None)
            df_test[i] = (test- min_score) / (max_score- min_score)
            df_train[i] = (train- min_score) / (max_score- min_score)
            # df_test[i] = (test- test.mean()) / test.std()
            # df_train[i] = (train- train.mean()) / train.std()

    df_test = [d for d in df_test if len(d)>0]
    df_test_mean = pd.concat(df_test, axis=1).mean(axis=1)
    plt.plot(x, df_test_mean, ":", label=f"{label} test", color=colors[label])

    df_train = [d for d in df_train if len(d)>0]
    df_train_mean = pd.concat(df_train, axis=1).mean(axis=1)
    plt.plot(x, df_train_mean, "--", label=f"{label} train", color=colors[label])

plt.xlabel("Steps in M")
plt.ylabel("Rewards")
plt.title("Mean normalized rewards")
plt.legend(loc='best', ncol=2)
plt.tight_layout()
plt.savefig('gap.png')
plt.show()
