#!/bin/sh
bsub < jobscripts/plr-bigfish-OneStep.sh
bsub < jobscripts/plr-bigfish-GAE.sh
bsub < jobscripts/plr-ninja-GAEMag.sh
bsub < jobscripts/plr-ninja-OneStep.sh