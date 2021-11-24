
#!/bin/sh
mkdir logs/PPO-heist

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-heist
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-heist/%J.out
#BSUB -e logs/PPO-heist/%J.err

echo "Running PPO-heist"
python3 plr.py 1 heist