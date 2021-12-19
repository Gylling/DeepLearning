#!/bin/sh
bsub < jobscripts/plr-ninja-GAE.sh
bsub < jobscripts/plr-jumper-GAEMag.sh
bsub < jobscripts/plr-jumper-OneStep.sh
bsub < jobscripts/plr-jumper-GAE.sh