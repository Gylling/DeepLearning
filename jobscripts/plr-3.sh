
#!/bin/sh
mkdir logs/plr-3

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-3
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-3/%J.out
#BSUB -e logs/plr-3/%J.err

echo "Running plr-3"
python3 plr.py 3