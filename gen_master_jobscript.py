types = ["PPO", "plr"]
games = [
    "starpilot",
    "bossfight",
    "coinrun",
    "jumper"
]

count = 0
text = "#!/bin/sh"
for type in types:
    for game in games:
        text += f"""
bsub < jobscripts/{type}-{game}.sh"""

with open(f"jobscript.sh", "w") as f:
            f.write(text)