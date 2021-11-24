
#!/bin/sh
mkdir logs/plr-bossfight

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-bossfight
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-bossfight/%J.out
#BSUB -e logs/plr-bossfight/%J.err

echo "Running plr-bossfight"
python3 plr.py 1 bossfight