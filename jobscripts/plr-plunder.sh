
#!/bin/sh
mkdir logs/plr-plunder

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-plunder
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-plunder/%J.out
#BSUB -e logs/plr-plunder/%J.err

echo "Running plr-plunder"
python3 plr.py 1 plunder