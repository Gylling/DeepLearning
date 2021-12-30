
#!/bin/sh
mkdir finallogs/PPO-2

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-2
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/PPO-2/%J.out
#BSUB -e finallogs/PPO-2/%J.err

echo "Running PPO-2"
python3 PPO.py 2