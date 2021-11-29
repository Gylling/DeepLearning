
games = [
    "starpilot",
    "coinrun",
    "jumper"
]
error_functions = ["GAEMag", "OneStep", "GAE"]


text = "#!/bin/sh"
for game in games:
        text += f"""
bsub < jobscripts/PPO-{game}.sh"""

for game in games:
    for err in range(3):
        name = f"plr-{game}-{error_functions[err]}"
        text += f"""
bsub < jobscripts/{name}.sh"""

with open(f"jobscript.sh", "w") as f:
            f.write(text)