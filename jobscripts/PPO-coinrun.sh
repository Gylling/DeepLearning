
#!/bin/sh
mkdir logs/PPO-coinrun

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-coinrun
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-coinrun/%J.out
#BSUB -e logs/PPO-coinrun/%J.err

echo "Running PPO-coinrun"
python3 PPO.py 1 coinrun