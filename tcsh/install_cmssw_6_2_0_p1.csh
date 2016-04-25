#!/bin/csh
# Instuctions: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TrackTriggerIntegration#Producing_L1tracks

# Define variables
set CMSSW="CMSSW_6_2_0_SLHC12_patch1"
set DESTINATION="~/scratch0/"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc472" #"slc5_amd64_gcc472"
set CRAB_UI_ENV="/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh"
set CRAB="/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh"

# Execute commands
echo "\n1) Installing CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"; pwd
cd ~

echo "\n2) Setting up SCRAM architecture"; pwd
setenv SCRAM_ARCH $SCRAM_ARCHITECTURE 
cd $DESTINATION

echo "\n3) Creating a local release area for $CMSSW and entering it"; pwd
cmsrel $CMSSW
cd $CMSSW/src/

echo "\n4) Setting up CMS Runtime Environment"; pwd
cmsenv #alias for `scramv1 runtime -sh\

echo "\n5) Fetching additional packages from git"; pwd
git cms-addpkg SLHCUpgradeSimulations/L1TrackTrigger
git cms-merge-topic EmanuelPerez:TTI_62X_TrackTriggerObjects

echo "\n6) Building the code"; pwd
echo "scramv1 b -j16"
scramv1 b -j16

echo "7) Done"; pwd

