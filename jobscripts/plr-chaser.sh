
#!/bin/sh
mkdir logs/plr-chaser

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

echo "Running plr-chaser"
python3 plr.py 1 chaser