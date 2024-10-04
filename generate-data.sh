#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for T in $(seq 1. .1 2.)
do
    echo "$T 0 5000"
    #./pris_pd_Qlearning_glut $T 0 5000
done
