<<<<<<< HEAD
 #!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for mobility in .1 .12 .13 .15 .17 .2 .23 .25 .3 .32 .35 .4 1. 1. 1. 1. 1. 1. 1. 1.
do
        echo "1.4 4000 .1 500"
        ./pris_pd_Qlearning_glut 1.4 4000 .1 500 
=======
# !/bin/bash
# LC_NUMERIC="en_US.UTF-8"
LANG=en_US # seq 0.1 0.1 0.8
 
for defects in $(seq 0 250 9000)
do
	for mobility in $(seq .005 .005 .105)
        do
                echo "1.4 $defects $mobility "
                ./pris_pd_Qlearning_glut 1.4 $defects $mobility  &
        done
        wait
>>>>>>> e2e4ee8d14c1db77aeb8e83518f10201af32bcfc
done
