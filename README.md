# Deep Learning Project for the DTU course, 02456

## Reproduce rewards
To reproduce results of this project you should run the following commands:

        python3 plr.py 2
        python3 plr.py 3
        python3 PPO.py 2
        python3 PPO.py 3
        python3 PPO.py 1 bigfish
        python3 plr.py 1 0 bigfish
        python3 plr.py 1 1 bigfish
        python3 plr.py 1 2 bigfish
        python3 PPO.py 1 jumper
        python3 plr.py 1 0 jumper
        python3 plr.py 1 1 jumper
        python3 plr.py 1 2 jumper
        python3 PPO.py 1 ninja
        python3 plr.py 1 0 ninja
        python3 plr.py 1 1 ninja
        python3 plr.py 1 2 ninja

## Create plots
Locate the newly generated rewards for each simulation under the rewards folder. Insert the relative paths in Plots.py and PlotsMulti.py. 

Run the following commands to create the plots:

        python3 Plots.py
        python3 PlotsMulti.py