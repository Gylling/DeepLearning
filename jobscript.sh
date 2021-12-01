#!/bin/sh
bsub < jobscripts/PPO-starpilot.sh
bsub < jobscripts/PPO-maze.sh
bsub < jobscripts/PPO-heist.sh
bsub < jobscripts/plr-starpilot-GAEMag.sh
bsub < jobscripts/plr-starpilot-OneStep.sh
bsub < jobscripts/plr-starpilot-GAE.sh
bsub < jobscripts/plr-maze-GAEMag.sh
bsub < jobscripts/plr-maze-OneStep.sh
bsub < jobscripts/plr-maze-GAE.sh
bsub < jobscripts/plr-heist-GAEMag.sh
bsub < jobscripts/plr-heist-OneStep.sh
bsub < jobscripts/plr-heist-GAE.sh
bsub < jobscripts/PPO-2.sh
bsub < jobscripts/plr-2.sh
bsub < jobscripts/PPO-3.sh
bsub < jobscripts/plr-3.sh