
#!/bin/sh
mkdir finallogs/PPO-bigfish

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J PPO-bigfish
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/PPO-bigfish/%J.out
#BSUB -e finallogs/PPO-bigfish/%J.err

echo "Running PPO-bigfish"
python3 PPO.py 1 bigfish