
#!/bin/sh
mkdir logs/plr-maze-GAE

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J plr-maze-GAE
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-maze-GAE/%J.out
#BSUB -e logs/plr-maze-GAE/%J.err

echo "Running plr-maze-GAE"
python3 plr.py 1 2 maze