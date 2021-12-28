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
        "jumper": {"test": "rewards/ppo-jumper/test_rewards-1640046985.3327672.csv", "train": "rewards/ppo-jumper/train_rewards-1640046985.3378258.csv"},
        "ninja": {"test": "rewards/ppo-ninja/test_rewards-1640011771.8472745.csv", "train": "rewards/ppo-ninja/train_rewards-1640011771.8518178.csv"},
        "bigfish": {"test": "rewards/ppo-bigfish/test_rewards-1639986849.5726612.csv", "train": "rewards/ppo-bigfish/train_rewards-1639986849.5768883.csv"}
    },
    "plr-td": {
        "jumper": {"test": "rewards/plr-jumper-OneStep/test_rewards-1640123833.4178863.csv", "train": "rewards/plr-jumper-OneStep/train_rewards-1640123833.4224465.csv"},
        "ninja": {"test": "rewards/plr-ninja-OneStep/test_rewards-1640145094.9311488.csv", "train": "rewards/plr-ninja-OneStep/train_rewards-1640145094.9371839.csv"},
        "bigfish": {"test": "rewards/plr-bigfish-OneStep/test_rewards-1640061956.0442092.csv", "train": "rewards/plr-bigfish-OneStep/train_rewards-1640061956.04891.csv"}
    },
    "plr-gae": {
        "jumper": {"test": "rewards/plr-jumper-GAE/test_rewards-1640360949.4017658.csv", "train": "rewards/plr-jumper-GAE/train_rewards-1640360949.407864.csv"},
        "ninja": {"test": "rewards/plr-ninja-GAE/test_rewards-1640090183.7667.csv", "train": "rewards/plr-ninja-GAE/train_rewards-1640090183.7718542.csv"},
        "bigfish": {"test": "rewards/plr-bigfish-GAE/test_rewards-1640075308.8060634.csv", "train": "rewards/plr-bigfish-GAE/train_rewards-1640075308.8102653.csv"}
    },
    "plr-gaem": {
        "jumper": {"test": "rewards/plr-jumper-GAEMag/test_rewards-1640124835.600524.csv", "train": "rewards/plr-jumper-GAEMag/train_rewards-1640124835.6055303.csv"},
        "ninja": {"test": "rewards/plr-ninja-GAEMag/test_rewards-1640101918.664596.csv", "train": "rewards/plr-ninja-GAEMag/train_rewards-1640101918.6686788.csv"},
        "bigfish": {"test": "rewards/plr-bigfish-GAEMag/test_rewards-1640018769.8121777.csv", "train": "rewards/plr-bigfish-GAEMag/train_rewards-1640018769.817248.csv"}
    }
}

# x = np.linspace(1, 22, 22)


def generate_graph(fig, colors, ax, ax_coord, list_of_paths, label_names, title="Results", xlabel="Steps in M",
                   ylabel="Rewards"):
    ax_x, ax_y = ax_coord
    # 2: Loop through paths
    for path, label, color in zip(list_of_paths, label_names, colors):
        if(len(path) == 0):
            continue
        else:
            df = pd.read_csv(path, header=None)
        print(path)
        x = np.linspace(1, 22, len(df.index))
        print(len(df.index))
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
    "bigfish",
    "jumper",
    "ninja"
]

for game, coord in zip(games, coords):
    generate_graph(colors=layout_colorway, fig=fig, ax=axs, ax_coord=coord, list_of_paths=[
        file_dict["ppo"][game]["test"],
        file_dict["plr-td"][game]["test"],
        file_dict["plr-gae"][game]["test"],
        file_dict["plr-gaem"][game]["test"]
    ], label_names=label_names, title=game)

fig.delaxes(axs[1][1])

handles, labels = axs[1, 1].get_legend_handles_labels()
axs[0, 0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
fig.legend(handles, labels, loc=(0.5, 0), ncol=3)

fig.tight_layout()
plt.savefig('rewards.png')
fig.show()
plt.clf()

"""
Figure 2
"""

games_dict = {
    "jumper": ("jumper", 3, 10),
    "ninja": ("ninja", 3.5, 10),
    "bigfish": ("bigfish", 1, 40)
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
            #df_test[i] = (test- min_score) / (max_score- min_score)
            #df_train[i] = (train- min_score) / (max_score- min_score)
            df_test[i] = (test- test.mean()) / test.std()
            df_train[i] = (train- train.mean()) / train.std()

    df_test = [d for d in df_test if len(d)>0]
    df_test_mean = pd.concat(df_test, axis=1).mean(axis=1)

    plt.plot(np.linspace(1, 22, len(df_test_mean.index)), df_test_mean, ":", label=f"{label} test", color=colors[label])

    df_train = [d for d in df_train if len(d)>0]
    df_train_mean = pd.concat(df_train, axis=1).mean(axis=1)
    plt.plot(np.linspace(1, 22, len(df_train_mean.index)), df_train_mean, "--", label=f"{label} train", color=colors[label])

plt.xlabel("Steps in M")
plt.ylabel("Rewards")
plt.title("Mean normalized rewards")
#plt.legend(loc='best', ncol=4)
plt.legend(loc='center right', bbox_to_anchor=(1.4, 0.5),
          ncol=1, fancybox=True, shadow=False)
plt.tight_layout()
plt.savefig('gap.png')
plt.show()
