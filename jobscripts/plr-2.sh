
#!/bin/sh
mkdir logs/plr-2

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J plr-2
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-2/%J.out
#BSUB -e logs/plr-2/%J.err

echo "Running plr-2"
python3 plr.py 2