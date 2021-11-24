
#!/bin/sh
mkdir logs/plr-miner

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-miner
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-miner/%J.out
#BSUB -e logs/plr-miner/%J.err

echo "Running plr-miner"
python3 plr.py 1 miner