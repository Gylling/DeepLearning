
#!/bin/sh
mkdir logs/PPO-fruitbot

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-fruitbot
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-fruitbot/%J.out
#BSUB -e logs/PPO-fruitbot/%J.err

echo "Running PPO-fruitbot"
python3 plr.py 1 fruitbot