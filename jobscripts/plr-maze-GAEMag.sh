
#!/bin/sh
mkdir logs/plr-maze-GAEMag

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-maze-GAEMag
#BSUB -n 1
#BSUB -W 24:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-maze-GAEMag/%J.out
#BSUB -e logs/plr-maze-GAEMag/%J.err

echo "Running plr-maze-GAEMag"
python3 plr.py 1 0 maze