
#!/bin/sh
mkdir finallogs/PPO-ninja

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-ninja
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/PPO-ninja/%J.out
#BSUB -e finallogs/PPO-ninja/%J.err

echo "Running PPO-ninja"
python3 PPO.py 1 ninja