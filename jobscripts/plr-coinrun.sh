
#!/bin/sh
mkdir logs/plr-coinrun

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-coinrun
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-coinrun/%J.out
#BSUB -e logs/plr-coinrun/%J.err

echo "Running plr-coinrun"
python3 plr.py 1 coinrun