
#!/bin/sh
mkdir logs/plr-bigfish-OneStep

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-bigfish-OneStep
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-bigfish-OneStep/%J.out
#BSUB -e logs/plr-bigfish-OneStep/%J.err

echo "Running plr-bigfish-OneStep"
python3 plr.py 1 1 bigfish