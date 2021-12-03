
#!/bin/sh
mkdir logs/plr-heist-GAEMag

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J plr-heist-GAEMag
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-heist-GAEMag/%J.out
#BSUB -e logs/plr-heist-GAEMag/%J.err

echo "Running plr-heist-GAEMag"
python3 plr.py 1 0 heist