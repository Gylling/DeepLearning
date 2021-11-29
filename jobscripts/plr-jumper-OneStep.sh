
#!/bin/sh
mkdir logs/plr-jumper-OneStep

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-jumper-OneStep
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-jumper-OneStep/%J.out
#BSUB -e logs/plr-jumper-OneStep/%J.err

echo "Running plr-jumper-OneStep"
python3 plr.py 1 1 jumper