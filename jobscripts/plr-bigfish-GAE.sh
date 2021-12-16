
#!/bin/sh
mkdir logs/plr-bigfish-GAE

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-bigfish-GAE
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-bigfish-GAE/%J.out
#BSUB -e logs/plr-bigfish-GAE/%J.err

echo "Running plr-bigfish-GAE"
python3 plr.py 1 2 bigfish