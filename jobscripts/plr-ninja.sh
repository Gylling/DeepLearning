
#!/bin/sh
mkdir logs/plr-ninja

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-ninja
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-ninja/%J.out
#BSUB -e logs/plr-ninja/%J.err

echo "Running plr-ninja"
python3 plr.py 1 ninja