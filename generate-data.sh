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
done
