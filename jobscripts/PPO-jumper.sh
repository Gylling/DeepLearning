
#!/bin/sh
mkdir logs/PPO-jumper

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-jumper
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-jumper/%J.out
#BSUB -e logs/PPO-jumper/%J.err

echo "Running PPO-jumper"
python3 PPO.py 1 jumper