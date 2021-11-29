
#!/bin/sh
mkdir logs/plr-coinrun-GAE

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-coinrun-GAE
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-coinrun-GAE/%J.out
#BSUB -e logs/plr-coinrun-GAE/%J.err

echo "Running plr-coinrun-GAE"
python3 plr.py 1 2 coinrun