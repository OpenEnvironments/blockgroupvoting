#!/bin/bash
# Shell script to run blockgroup voting in parallel across states
# -t option is the number of this parallel thread
# -o option is 'out of' how many threads
# These will depend on the number of CPU threads available
# and assume at least one of the CPU threads is needed by OS background tasks

python3 parallelprocess.py -t 0 -o 4 > zero.log  2>zero.err  &
python3 parallelprocess.py -t 1 -o 4 > one.log   2>one.err   & 
python3 parallelprocess.py -t 2 -o 4 > two.log   2>two.err   & 
python3 parallelprocess.py -t 3 -o 4 > three.log 2>three.err &
