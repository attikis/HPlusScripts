#!/bin/sh
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
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/batch-concepts-and-cern-batch-systemy
# https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs
# https://twiki.cern.ch/twiki/bin/view/Main/UsingLxBatch
# http://information-technology.web.cern.ch/services/batch
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/using-batch-system
#================================================================================================
echo '=== lxbatch.sh'

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
# If number of arguments is not (numerically) equal to 1
if [ "$#" -ne 1 ]; then
    # Inform USER
    echo "=== You must give exactly 1 argument(s), in this order:"
    echo "1=DATASET NAME"
    # Exit with a failure status code.
    exit 1
fi

# Get the variables
dataset_name=${1}

#########################################################################################################
# Definitions
#########################################################################################################
CWD=`pwd`
CWD_BASENAME=`basename $CWD`
FILE_PyCFG=TkTauFromCaloNTupleMaker_cfg.py
FILE_PRODUCER=TkTauFromCaloNTupleMaker.cc
FILE_OUTPUT=output.root
FILE_OUTPUTSAVE=output-${dataset_name}.root
FILE_LOG=log.txt
BASE_DIR=/afs/cern.ch/work/a/attikis/lxbatch/LSFJOB_${CWD_BASENAME}_`date +%d%b%Y_%Hh%Mm%Ss` #date +%d-%m-%Y
SAVE_DIR=$BASE_DIR/${dataset_name}
SAVE_DIR_RES=$SAVE_DIR/res
FILE_SCRIPT_EXE=submit_lxbatch.csh
FILE_SCRIPT_AUX=lxbatch.sh
ANAL_DIR=/afs/cern.ch/user/a/attikis/scratch0/CMSSW_6_2_0_SLHC12_patch1/src/SLHCUpgradeSimulations/L1TrackTrigger/test


#########################################################################################################
# Execute Steps
#########################################################################################################
cd $ANAL_DIR
eval `scram runtime -sh`

# Go back to current directory on lxbatch
cd $CWD

# Copy the python configuration file that you want to run 
cp $ANAL_DIR/$FILE_PyCFG go.py

# Creae dir to save output
mkdir $BASE_DIR
mkdir $SAVE_DIR
mkdir $SAVE_DIR_RES

# Copy files used in running the code
cp $ANAL_DIR/$FILE_SCRIPT_EXE $SAVE_DIR/.
cp $ANAL_DIR/$FILE_SCRIPT_AUX $SAVE_DIR/.
cp $ANAL_DIR/$FILE_PyCFG $SAVE_DIR/.
cp $ANAL_DIR/$FILE_PRODUCER $SAVE_DIR/.
cp go.py $SAVE_DIR/.

# Execute cmsRun 
cmsRun go.py ${dataset_name} > $FILE_LOG


#########################################################################################################
# Retrieve Output
#########################################################################################################
cp $FILE_LOG $SAVE_DIR/$FILE_LOG
cp $FILE_OUTPUT $SAVE_DIR_RES/$FILE_OUTPUTSAVE