
#!/bin/sh
mkdir logs/plr-jumper-GAE

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-jumper-GAE
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-jumper-GAE/%J.out
#BSUB -e logs/plr-jumper-GAE/%J.err

echo "Running plr-jumper-GAE"
python3 plr.py 1 2 jumper