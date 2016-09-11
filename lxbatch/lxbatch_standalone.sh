#!/bin/sh
#########################################################################################################
# The root file output.root and the log file log.txt (and any product of your cmsRun job)
# is created in the temporary area that is dedicated to your batch job.
# 
# Usage:
# bsub -q <queue_name> -J <job_name> < lxbatch_standalone.sh
#
# Example:
# bsub -q 1nd -J MuPlusNoPUAllPt < lxbatch_standalone.sh
#########################################################################################################

#########################################################################################################
# Definitions
#########################################################################################################
CWD=`pwd`
CWD_BASENAME=`basename "$CWD"` #or basename `pwd`
FILE_PyCFG=TkTauFromCaloNTupleMaker_cfg.py
FILE_PRODUCER=TkTauFromCaloNTupleMaker.cc
FILE_OUTPUT=output.root
FILE_LOG=log.txt
SAVE_DIR=/afs/cern.ch/work/a/attikis/lxbatch/LSFJOB_$CWD_BASENAME
FILE_SCRIPT=lxbatch.sh
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
mkdir $SAVE_DIR

# Copy files used in running the code
cp $ANAL_DIR/$FILE_SCRIPT $SAVE_DIR/.
cp $ANAL_DIR/$FILE_PyCFG $SAVE_DIR/.
cp $ANAL_DIR/$FILE_PRODUCER $SAVE_DIR/.
cp go.py $SAVE_DIR/.

# Execute cmsRun 
cmsRun go.py > $FILE_LOG

#########################################################################################################
# Retrieve Output
#########################################################################################################
cp $FILE_OUTPUT $SAVE_DIR/$FILE_OUTPUT
cp $FILE_LOG $SAVE_DIR/$FILE_LOG
#cmsStageOut $FILE_OUTPUT $SAVE_DIR/$FILE_OUTPUT