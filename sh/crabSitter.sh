#!/bin/bash
 
# Definitions
#cmd="multicrab.py --status -i VVTo2L2Nu_ext1 && multicrab.py --resubmit -i VVTo2L2Nu_ext1"
cmd="multicrab.py --status && multicrab.py --resubmit"
dt=10m #1s 1m 1h (no unit implies seconds)

# Execute for-loop
for i in {1..12..1};
do echo "=== $i) `date`"
    echo "${cmd}"
    ${cmd}

    #echo "=== Will re-execute script in ${dt}"
    sleep ${dt}; 
    echo ""
echo "=== DONE!"
done
