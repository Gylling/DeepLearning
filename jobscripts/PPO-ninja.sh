
#!/bin/sh
mkdir logs/PPO-ninja

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-ninja
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-ninja/%J.out
#BSUB -e logs/PPO-ninja/%J.err

echo "Running PPO-ninja"
python3 PPO.py 1 ninja