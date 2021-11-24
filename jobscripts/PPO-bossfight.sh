
#!/bin/sh
mkdir logs/PPO-bossfight

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-bossfight
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-bossfight/%J.out
#BSUB -e logs/PPO-bossfight/%J.err

echo "Running PPO-bossfight"
python3 plr.py 1 bossfight