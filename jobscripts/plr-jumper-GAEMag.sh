
#!/bin/sh
mkdir logs/plr-jumper-GAEMag

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-jumper-GAEMag
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-jumper-GAEMag/%J.out
#BSUB -e logs/plr-jumper-GAEMag/%J.err

echo "Running plr-jumper-GAEMag"
python3 plr.py 1 0 jumper