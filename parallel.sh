python3 parallelprocess.py -t 0 -o 8 > zero.log  2>zero.err  & 
python3 parallelprocess.py -t 1 -o 8 > one.log   2>one.err   & 
python3 parallelprocess.py -t 2 -o 8 > two.log   2>two.err   & 
python3 parallelprocess.py -t 3 -o 8 > three.log 2>three.err & 
python3 parallelprocess.py -t 4 -o 8 > four.log  2>four.err  & 
python3 parallelprocess.py -t 5 -o 8 > five.log  2>five.err  & 
python3 parallelprocess.py -t 6 -o 8 > six.log   2>six.err   & 
python3 parallelprocess.py -t 7 -o 8 > seven.log 2>seven.err & 