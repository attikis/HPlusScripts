#!/bin/csh

### Define variables
set CMSSW="CMSSW_6_2_0_SLHC12_patch1"
set DESTINATION="~/scratch0/"
set ENDPATH=$DESTINATION$CMSSW/src/"SLHCUpgradeSimulations/L1TrackTrigger/test/"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc472" #"slc5_amd64_gcc472"
set CRAB_UI_ENV="/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh"
set CRAB="/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh"

### Execute commands
echo "\nSetting environment for CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"; pwd
cd ~

#echo "\n---> Setting up SCRAM architecture"; pwd
#setenv SCRAM_ARCH $SCRAM_ARCHITECTURE 
cd $DESTINATION

echo "\nEntering release area for $CMSSW"; pwd
cd $CMSSW/src/

echo "\nSetting up CMS Runtime Environment"; pwd
cmsenv #alias for `scramv1 runtime -sh\

### Obsolete since ~May 2015
#echo "\nSourcing CRAB scripts"; pwd
echo "source $CRAB_UI_ENV"  #as of CRAB_2_10_7, crab2 works on lxplus6 w/o any UI setup
source $CRAB_UI_ENV         #as of CRAB_2_10_7, crab2 works on lxplus6 w/o any UI setup
echo "source $CRAB"
source $CRAB

echo "\nWorking with ROOT version: " 
echo $ROOTSYS

cd $ENDPATH
echo "\nDone"; pwd

