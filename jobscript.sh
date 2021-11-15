 #!/bin/sh
 source ~/.bashrc

 #BSUB -q gpua100
 #BSUB -gpu "num=1"
 #BSUB -J myJob
 #BSUB -n 1
 #BSUB -W 16:00
 #BSUB -u gylling.erik@gmail.com
 #BSUB -B
 #BSUB -N
 #BSUB -R "rusage[mem=64GB]"
 #BSUB -o logs/%J.out
 #BSUB -e logs/%J.err

 echo "Running script..."
 python3 ppo.py
