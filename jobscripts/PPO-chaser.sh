
#!/bin/sh
mkdir logs/PPO-chaser

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-chaser
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-chaser/%J.out
#BSUB -e logs/PPO-chaser/%J.err

echo "Running PPO-chaser"
python3 PPO.py 1 chaser