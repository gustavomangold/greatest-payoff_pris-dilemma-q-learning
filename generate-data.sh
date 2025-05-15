#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for defects in $(seq 3000 100 5000)
do
        echo "1.4 4000 .1 500"
        ./pris_pd_Qlearning_glut 1.4 4000 .1 500 
done
wait
