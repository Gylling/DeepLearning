
#!/bin/sh
mkdir logs/plr-ninja-OneStep

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-ninja-OneStep
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-ninja-OneStep/%J.out
#BSUB -e logs/plr-ninja-OneStep/%J.err

echo "Running plr-ninja-OneStep"
python3 plr.py 1 1 ninja