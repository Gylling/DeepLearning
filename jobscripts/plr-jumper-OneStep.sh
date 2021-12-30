
#!/bin/sh
mkdir finallogs/plr-jumper-OneStep

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-jumper-OneStep
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/plr-jumper-OneStep/%J.out
#BSUB -e finallogs/plr-jumper-OneStep/%J.err

echo "Running plr-jumper-OneStep"
python3 plr.py 1 1 jumper