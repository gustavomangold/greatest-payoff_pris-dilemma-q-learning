#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for defects in $(seq 500 500 9000)
do
	for mobility in .01 .02 .03 .04 .05 .06 .07 .08 .09 .1
        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done

for defects in $(seq 500 500 9000)
do
        for mobility in .1 .2 .3 .4 .5 .6 .7 .8 .9 1.
        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done

for defects in $(seq 500 500 9000)
do
        for mobility in .15 .25 .35 .45 .55 .65 .75 .85 .95
        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done
