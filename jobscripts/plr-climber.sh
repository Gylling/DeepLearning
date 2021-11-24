
#!/bin/sh
GAME = climber
NUM = 1
NAME= "plr-$GAME"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-climber
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-climber/%J.out
#BSUB -e logs/plr-climber/%J.err

echo "Running $NAME"
python3 plr.py $NUM $GAME