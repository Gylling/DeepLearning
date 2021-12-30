#!/bin/sh
bsub < jobscripts/plr-bigfish-GAEMag.sh
bsub < jobscripts/plr-bigfish-OneStep.sh
bsub < jobscripts/plr-bigfish-GAE.sh