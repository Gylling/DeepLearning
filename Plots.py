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
        "starpilot": {"test": "rand.csv", "train": "rand.csv"},
        "heist": {"test": "rand.csv", "train": "rand.csv"},
        "maze": {"test": "rand.csv", "train": "rand.csv"}
    },
    "plr-td": {
        "starpilot": {"test": "rand2.csv", "train": "rand.csv"},
        "heist": {"test": "rand2.csv", "train": "rand.csv"},
        "maze": {"test": "rand2.csv", "train": "rand.csv"}
    },
    "plr-gae": {
        "starpilot": {"test": "rand3.csv", "train": "rand.csv"},
        "heist": {"test": "rand3.csv", "train": "rand.csv"},
        "maze": {"test": "rand3.csv", "train": "rand.csv"}
    },
    "plr-gaem": {
        "starpilot": {"test": "rand4.csv", "train": "rand.csv"},
        "heist": {"test": "rand4.csv", "train": "rand.csv"},
        "maze": {"test": "rand4.csv", "train": "rand.csv"}
    }
}

x = np.linspace(0, 25, 25)


def generate_graph(fig, colors, ax, ax_coord, list_of_paths, label_names, title="Results", xlabel="Steps in M",
                   ylabel="Rewards"):
    ax_x, ax_y = ax_coord
    test = False
    # 2: Loop through paths
    for path, label, color in zip(list_of_paths, label_names, colors):
        if test:
            df = np.random.sample(25, )
        else:
            df = pd.read_csv(path, header=None)

        ax[ax_x, ax_y].plot(x, df, label=label, c=color)

        if not (ax_x == 0 and ax_y == 0):
            ax[ax_x, ax_y].set_xlabel(xlabel)
        if ax_y == 0:
            ax[ax_x, ax_y].set_ylabel(ylabel)

        ax[ax_x, ax_y].set_title(title)


fig, axs = plt.subplots(2, 2, sharey=True)
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
axs[0, 1].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
# fig.legend(handles, labels, loc=(0.5, 0), ncol=3)

fig.show()

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
        test = pd.read_csv(file_dict[label][game]["test"], header=None)
        train = pd.read_csv(file_dict[label][game]["train"], header=None)
        df_test[i] = (test- min_score) / (max_score - min_score)
        df_train[i] = (train- min_score) / (max_score - min_score)

    df_test_mean = pd.concat(df_test, axis=1).mean(axis=1)
    plt.plot(x, df_test_mean, ":", label="test", color=colors[label])

    df = pd.concat(df_train, axis=1)
    plt.plot(x, df.mean(axis=1), "--", label="train", color=colors[label])

plt.show()
