
#!/bin/sh
NUM = 1
NAME= "plr-jumper"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-jumper
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-jumper/%J.out
#BSUB -e logs/plr-jumper/%J.err

echo "Running plr-jumper"
python3 plr.py $NUM jumper