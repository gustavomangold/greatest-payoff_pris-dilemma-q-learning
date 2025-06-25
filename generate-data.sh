#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for defects in 1 2 3 4 5 6 7 8 9 10 
do
        echo "1.4 4000 .1 500"
        ./pris_pd_Qlearning_glut 1.4 4000 .1 500 
done
wait
