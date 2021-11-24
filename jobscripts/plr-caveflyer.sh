
#!/bin/sh
NUM = 1
NAME= "plr-caveflyer"
mkdir logs/$NAME

source ~/.bashrc

#BSUB -q gpua100
#BSUB -gpu "num=1"
#BSUB -J plr-caveflyer
#BSUB -n 1
#BSUB -W 16:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-caveflyer/%J.out
#BSUB -e logs/plr-caveflyer/%J.err

echo "Running plr-caveflyer"
python3 plr.py $NUM caveflyer