#!/bin/sh
bsub < jobscripts/PPO-2.sh
bsub < jobscripts/plr-2.sh
bsub < jobscripts/PPO-3.sh
bsub < jobscripts/plr-3.sh