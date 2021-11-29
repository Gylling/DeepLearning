
#!/bin/sh
mkdir logs/PPO-caveflyer

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-caveflyer
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-caveflyer/%J.out
#BSUB -e logs/PPO-caveflyer/%J.err

echo "Running PPO-caveflyer"
python3 PPO.py 1 caveflyer