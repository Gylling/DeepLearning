
#!/bin/sh
mkdir logs/PPO-starpilot

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J PPO-starpilot
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-starpilot/%J.out
#BSUB -e logs/PPO-starpilot/%J.err

echo "Running PPO-starpilot"
python3 PPO.py 1 starpilot