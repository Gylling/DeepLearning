
#!/bin/sh
mkdir logs/PPO-plunder

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-plunder
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-plunder/%J.out
#BSUB -e logs/PPO-plunder/%J.err

echo "Running PPO-plunder"
python3 plr.py 1 plunder