#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

<<<<<<< HEAD
for defects in $(seq 3000 250 6500)
=======
for defects in $(seq 3000 250 5500)
>>>>>>> 3b034c5fc1230c15749460e6572a10e216ef6be8
do
        for noise in 0 .01 .02 .03 .04 .05 .06 .07 .08 .09 .1 

        do
                echo "1.4 $defects 0.01 $noise"
                ./pris_pd_Qlearning_glut 1.4 $defects .01 $noise &
        done
        wait
        
	for noise in 0 .12 .14 .16 .18 .2 .25 .3 .4 .5 .6 

        do
                echo "1.4 $defects 0.01 $noise"
                ./pris_pd_Qlearning_glut 1.4 $defects .01 $noise &
        done
        wait
done
