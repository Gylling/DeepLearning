types = ["PPO", "plr"]
games = [
    "starpilot",
    "maze",
    "heist"
]
error_functions = ["GAEMag", "OneStep", "GAE"]

for game in games:
    name = f"PPO-{game}"
    text = f"""
#!/bin/sh
mkdir logs/{name}

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J {name}
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/{name}/%J.out
#BSUB -e logs/{name}/%J.err

echo "Running {name}"
python3 PPO.py 1 {game}"""
    with open(f"jobscripts/{name}.sh", "w") as f:
        f.write(text)


for game in games:
    for err in range(3):
        name = f"plr-{game}-{error_functions[err]}"
        text = f"""
#!/bin/sh
mkdir logs/{name}

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J {name}
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/{name}/%J.out
#BSUB -e logs/{name}/%J.err

echo "Running {name}"
python3 plr.py 1 {err} {game}"""
        with open(f"jobscripts/{name}.sh", "w") as f:
            f.write(text)


# Mulitple games
for category in [2,3]:
    for type in types:
        name = f"{type}-{category}"
        text = f"""
#!/bin/sh
mkdir logs/{name}

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J {name}
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/{name}/%J.out
#BSUB -e logs/{name}/%J.err

echo "Running {name}"
python3 {type}.py {category}"""
        with open(f"jobscripts/{name}.sh", "w") as f:
            f.write(text)