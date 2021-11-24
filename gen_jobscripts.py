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

count = 1
for type in types:
    for game in games:
        name = f"{type}-{game}"
        text = f"""
#!/bin/sh
mkdir logs/{name}

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J {name}
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/{name}/%J.out
#BSUB -e logs/{name}/%J.err

echo "Running {name}"
python3 plr.py {count} {game}"""
        with open(f"jobscripts/{name}.sh", "w") as f:
            f.write(text)