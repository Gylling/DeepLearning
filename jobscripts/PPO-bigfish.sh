
#!/bin/sh
mkdir logs/PPO-bigfish

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-bigfish
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/PPO-bigfish/%J.out
#BSUB -e logs/PPO-bigfish/%J.err

echo "Running PPO-bigfish"
python3 plr.py 1 bigfish