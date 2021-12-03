
#!/bin/sh
mkdir logs/plr-starpilot-GAE

source ~/.bashrc

#BSUB -q hpc
#BSUB -gpu "num=1"
#BSUB -J plr-starpilot-GAE
#BSUB -n 1
#BSUB -W 36:00
#BSUB -u gylling.erik@gmail.com
#BSUB -B
#BSUB -N
#BSUB -R "rusage[mem=32GB]"
#BSUB -o logs/plr-starpilot-GAE/%J.out
#BSUB -e logs/plr-starpilot-GAE/%J.err

echo "Running plr-starpilot-GAE"
python3 plr.py 1 2 starpilot