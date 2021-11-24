
#!/bin/sh
NUM = 1
NAME= "PPO-chaser"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-chaser
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-chaser/%J.out
#BSUB -e logs/plr-chaser/%J.err

echo "Running PPO-chaser"
python3 plr.py $NUM chaser