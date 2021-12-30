
#!/bin/sh
mkdir finallogs/plr-2

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-2
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/plr-2/%J.out
#BSUB -e finallogs/plr-2/%J.err

echo "Running plr-2"
python3 plr.py 2