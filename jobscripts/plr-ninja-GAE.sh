
#!/bin/sh
mkdir logs/plr-ninja-GAE

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-ninja-GAE
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-ninja-GAE/%J.out
#BSUB -e logs/plr-ninja-GAE/%J.err

echo "Running plr-ninja-GAE"
python3 plr.py 1 2 ninja