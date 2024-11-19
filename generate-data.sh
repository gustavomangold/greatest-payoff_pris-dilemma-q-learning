#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for mobility in 0. 0.01 0.05 0.1 0.5 1.
        do
        for defects in $(seq 9000 50 9500)
                do
                echo "1.4 $defects $mobility 0.1"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility 0.1 &
                done
        wait
done

for mobility in 0. 0.01 0.05 0.1 0.5 1.
        do
        for defects in $(seq 9500 50 10000)
                do
                echo "1.4 $defects $mobility 0.1"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility 0.1 &
                done
        wait
done
