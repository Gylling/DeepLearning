#!/bin/sh
bsub < jobscripts/plr-ninja-GAEMag.sh
bsub < jobscripts/plr-ninja-OneStep.sh
bsub < jobscripts/plr-ninja-GAE.sh