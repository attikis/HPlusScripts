#!/bin/sh
### The root file output.root and the log file log.txt (and any product of your cmsRun job)
### is created in the temporary area that is dedicated to your batch job.

### Definitions
cwd=`pwd`
cwd_last=`basename "$cwd"` #or basename `pwd`
py_cfg=TkTauFromCaloNTupleMaker_cfg.py
cc_file=TkTauFromCaloNTupleMaker.cc
ROOT_FILE=output.root
LOG_FILE=log.txt
SAVE_DIR=/afs/cern.ch/work/a/attikis/lxbatch/LSFJOB_$cwd_last

### Define the analysis directory: the dir that you would run your configuration file in interactive mode:
ANAL_DIR=/afs/cern.ch/user/a/attikis/scratch0/CMSSW_6_2_0_SLHC12_patch1/src/SLHCUpgradeSimulations/L1TrackTrigger/test

### Go to analysis directory
cd $ANAL_DIR
eval `scram runtime -sh`

### Go back to current directory on lxbatch
cd $cwd

### Copy the python configuration file that you want to run 
cp $ANAL_DIR/$py_cfg go.py

### Execute cmsRun 
cmsRun go.py > $LOG_FILE

### Once the cmsRun is done running, copy the files your desired path. Here, I copy these files locally or EOS
mkdir $SAVE_DIR
#cmsStageOut $ROOT_FILE $SAVE_DIR/$ROOT_FILE
cp $ANAL_DIR/$py_cfg $SAVE_DIR/.
cp $ANAL_DIR/$cc_file $SAVE_DIR/.
cp go.py $SAVE_DIR/.
cp $ROOT_FILE $SAVE_DIR/$ROOT_FILE
cp $LOG_FILE $SAVE_DIR/$LOG_FILE


