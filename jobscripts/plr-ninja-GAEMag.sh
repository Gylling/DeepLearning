
#!/bin/sh
mkdir finallogs/plr-ninja-GAEMag

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-ninja-GAEMag
#BSUB -n 1
#BSUB -W 56:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o finallogs/plr-ninja-GAEMag/%J.out
#BSUB -e finallogs/plr-ninja-GAEMag/%J.err

echo "Running plr-ninja-GAEMag"
python3 plr.py 1 0 ninja