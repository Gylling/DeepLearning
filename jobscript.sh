 #!/bin/sh
 NAME=plr-15
 mkdir logs/$NAME

 source ~/.bashrc

 #BSUB -q gpua100
 #BSUB -gpu "num=1"
 #BSUB -J $NAME
 #BSUB -n 1
 #BSUB -W 16:00
 #BSUB -u gylling.erik@gmail.com
 #BSUB -B
 #BSUB -N
 #BSUB -R "rusage[mem=32GB]"
 #BSUB -o logs/$NAME/%J.out
 #BSUB -e logs/$NAME/%J.err

 echo "Running script..."
 python3 ppo.py
