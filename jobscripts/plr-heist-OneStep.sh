
#!/bin/sh
mkdir logs/plr-heist-OneStep

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J plr-heist-OneStep
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-heist-OneStep/%J.out
#BSUB -e logs/plr-heist-OneStep/%J.err

echo "Running plr-heist-OneStep"
python3 plr.py 1 1 heist