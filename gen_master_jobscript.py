types = ["PPO", "plr"]
games = [
    "plunder",
    "starpilot",
    "bossfight",
    "caveflyer",
    "dodgeball",
    "chaser",
    "miner",
    "heist",
    "maze",
    "climber",
    "coinrun",
    "jumper",
    "ninja",
    "leaper",
    "fruitbot",
    "bigfish"
]

count = 0
text = "#!/bin/sh"
for type in types:
    for game in games:
        text += f"""
bsub < jobscripts/{type}-{game}.sh"""

with open(f"jobscript.sh", "w") as f:
            f.write(text)