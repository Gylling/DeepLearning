
#!/bin/sh
mkdir finallogs/PPO-jumper

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-jumper
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/PPO-jumper/%J.out
#BSUB -e finallogs/PPO-jumper/%J.err

echo "Running PPO-jumper"
python3 PPO.py 1 jumper