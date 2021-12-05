
#!/bin/sh
mkdir logs/PPO-3

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-3
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-3/%J.out
#BSUB -e logs/PPO-3/%J.err

echo "Running PPO-3"
python3 PPO.py 3