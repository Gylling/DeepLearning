
#!/bin/sh
mkdir logs/plr-bigfish

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-bigfish
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-bigfish/%J.out
#BSUB -e logs/plr-bigfish/%J.err

echo "Running plr-bigfish"
python3 plr.py 1 bigfish