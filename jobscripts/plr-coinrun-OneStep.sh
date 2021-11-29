
#!/bin/sh
mkdir logs/plr-coinrun-OneStep

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-coinrun-OneStep
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-coinrun-OneStep/%J.out
#BSUB -e logs/plr-coinrun-OneStep/%J.err

echo "Running plr-coinrun-OneStep"
python3 plr.py 1 1 coinrun