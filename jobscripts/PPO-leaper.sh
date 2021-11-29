
#!/bin/sh
mkdir logs/PPO-leaper

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-leaper
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-leaper/%J.out
#BSUB -e logs/PPO-leaper/%J.err

echo "Running PPO-leaper"
python3 PPO.py 1 leaper