#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for defects in $(seq 50 50 3000)
do
        for mobility in 0 .02 .05 .07 .1 .12 .15 .17 .2 .23 .25 .3 .32 .35 .4

        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done
