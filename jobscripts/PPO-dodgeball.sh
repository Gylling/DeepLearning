
#!/bin/sh
mkdir logs/PPO-dodgeball

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-dodgeball
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-dodgeball/%J.out
#BSUB -e logs/PPO-dodgeball/%J.err

echo "Running PPO-dodgeball"
python3 plr.py 1 dodgeball