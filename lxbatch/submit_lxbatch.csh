#!/bin/csh -f   
#================================================================================================
# C Shell Programming:
# http://www-cs.canisius.edu/ONLINESTUFF/UNIX/shellprogramming.html
# 
# Desctiption:
# "Jobs" are submitted from the LXPLUS cluster.
# A "job" consists of a script, typically located inside AFS (the AFS filesystem is visible to the batch nodes).
# After submission the jobs typically queues until the scheduler decides that its turn has come.
# The job has its own local "pool" directory on the worker node where it can read and write local files.
# The pool directory is deleted at the end of the job.
# Large data files needed for the job should be copied to the local pool directory (e.g. by Castor) in or accessed remotely (e.g. by EOS).
# Data files written locally by the job should be copied out to CERN storage (typically EOS or Castor).
# The results of the job run (STDOUT/STDERR) and job completion status are sent back to the user.
# 
# Return Codes:
# http://information-technology.web.cern.ch/services/fe/lxbatch/howto/how-interpet-batch-job-return-codes
# 
# Useful Links:
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/batch-concepts-and-cern-batch-system
# https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs
# https://twiki.cern.ch/twiki/bin/view/Main/UsingLxBatch
# http://information-technology.web.cern.ch/services/batchy
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/using-batch-system
#================================================================================================
echo '=== submit_lxbatch.csh'

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments, in this order:"
    echo "1=QUEUE NAME"
    echo "2=JOB NAME"
    echo "3=DATASET NAME"

    echo
    echo "=== Usage:"
    echo "./submit_lxbatch.csh <queue_name> <job_name> <datataset_name>"

    echo
    echo "=== Example:"
    echo "./submit_lxbatch.csh 1nd test VBF"
    echo
    exit 1
endif

#================================================================================================
# Get command line arguments
#================================================================================================
set queue_name=$1
set job_name=$2
set dataset_name=$3


#================================================================================================
# Ask to continue
#================================================================================================
echo "bsub -q ${queue_name} -J ${job_name} 'sh lxbatch.sh ${dataset_name}'"
echo
echo "Proceed (y/n)?"
set userInput = $<
if ($userInput == y) then
    echo
    echo "Submitting job to LXBATCH..."
    bsub -q ${queue_name} -J ${job_name} "sh lxbatch.sh ${dataset_name}"
else
    echo
    echo "EXIT [ userInput=$userInput (instead of 'y') ]"
    exit -1
endif

