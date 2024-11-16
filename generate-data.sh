#!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for defects in $(seq 0 50 9000)
do
        for mobility in 0

        do
                echo "1.4 $defects $mobility"
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility &
        done
        wait
done
