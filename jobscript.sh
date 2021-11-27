#!/bin/sh
bsub < jobscripts/PPO-starpilot.sh
bsub < jobscripts/PPO-bossfight.sh
bsub < jobscripts/PPO-coinrun.sh
bsub < jobscripts/PPO-jumper.sh
bsub < jobscripts/plr-starpilot.sh
bsub < jobscripts/plr-bossfight.sh
bsub < jobscripts/plr-coinrun.sh
bsub < jobscripts/plr-jumper.sh