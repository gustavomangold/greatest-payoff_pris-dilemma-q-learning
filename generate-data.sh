#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for mobility in .1 .12 .13 .15 .17 .2 .23 .25 .3 .32 .35 .4
do
        for defects in $(seq 3000 100 6500)
        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done
~      
