
#!/bin/sh
mkdir logs/PPO-climber

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-climber
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-climber/%J.out
#BSUB -e logs/PPO-climber/%J.err

echo "Running PPO-climber"
python3 plr.py 1 climber