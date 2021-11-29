#!/bin/sh
bsub < jobscripts/plr-starpilot-GAEMag.sh
bsub < jobscripts/plr-starpilot-OneStep.sh
bsub < jobscripts/plr-starpilot-GAE.sh
bsub < jobscripts/plr-coinrun-GAEMag.sh
bsub < jobscripts/plr-coinrun-OneStep.sh
bsub < jobscripts/plr-coinrun-GAE.sh
bsub < jobscripts/plr-jumper-GAEMag.sh
bsub < jobscripts/plr-jumper-OneStep.sh
bsub < jobscripts/plr-jumper-GAE.sh