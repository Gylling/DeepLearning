
#!/bin/sh
mkdir logs/PPO-miner

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-miner
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-miner/%J.out
#BSUB -e logs/PPO-miner/%J.err

echo "Running PPO-miner"
python3 PPO.py 1 miner