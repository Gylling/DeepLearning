#!/bin/sh
bsub < jobscripts/PPO-bigfish.sh
bsub < jobscripts/PPO-ninja.sh
bsub < jobscripts/PPO-jumper.sh
bsub < jobscripts/plr-bigfish-GAEMag.sh