
#!/bin/sh
GAME = heist
NUM = 1
NAME= "plr-$GAME"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-heist
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-heist/%J.out
#BSUB -e logs/plr-heist/%J.err

echo "Running $NAME"
python3 plr.py $NUM $GAME