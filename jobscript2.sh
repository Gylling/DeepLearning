#!/bin/sh
bsub < jobscripts/PPO-jumper.sh
bsub < jobscripts/plr-bigfish-GAEMag.sh
bsub < jobscripts/plr-bigfish-GAE.sh
bsub < jobscripts/plr-ninja-OneStep.sh
bsub < jobscripts/plr-ninja-GAE.sh
bsub < jobscripts/plr-jumper-GAEMag.sh
bsub < jobscripts/plr-jumper-OneStep.sh
bsub < jobscripts/plr-jumper-GAE.sh
bsub < jobscripts/PPO-2.sh
bsub < jobscripts/plr-2.sh
bsub < jobscripts/PPO-3.sh