 #!/bin/bash
LC_NUMERIC="en_US.UTF-8"

for mobility in .1 .12 .13 .15 .17 .2 .23 .25 .3 .32 .35 .4 1. 1. 1. 1. 1. 1. 1. 1.
do
        echo "1.4 4000 .1 500"
        ./pris_pd_Qlearning_glut 1.4 4000 .1 500 
done
               
