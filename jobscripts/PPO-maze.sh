
#!/bin/sh
mkdir logs/PPO-maze

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-maze
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-maze/%J.out
#BSUB -e logs/PPO-maze/%J.err

echo "Running PPO-maze"
python3 PPO.py 1 maze