python3 parallelprocess.py -t 0 -o 4 > zero.log  2>zero.err  &
python3 parallelprocess.py -t 1 -o 4 > one.log   2>one.err   & 
python3 parallelprocess.py -t 2 -o 4 > two.log   2>two.err   & 
python3 parallelprocess.py -t 3 -o 4 > three.log 2>three.err &
