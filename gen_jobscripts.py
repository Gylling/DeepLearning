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
for type in types:
    for game in games:
        text = f"""
#!/bin/sh
GAME = {game}
NUM = 1
NAME= "{type}-$GAME"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-{game}
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-{game}/%J.out
#BSUB -e logs/plr-{game}/%J.err

echo "Running $NAME"
python3 plr.py $NUM $GAME"""
        with open(f"jobscripts/{type}-{game}.sh", "w") as f:
            f.write(text)