#!/bin/csh
echo "=== setenv_cmssw_7_6_5.csh:"

### Define variables
set CMSSW="CMSSW_7_6_5"
set DESTINATION="~/scratch0/"
set ENDPATH=$DESTINATION$CMSSW"/src/UCYHiggsAnalysis/"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc472"
set CRAB_UI_ENV="/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh"
set CRAB="/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh"


### Inform User
echo "\t Setting environment for CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"#; pwd
cd ~


### Setup CMSSW Environment
echo "\t Setting up CMS Runtime Environment"#; pwd
cd $DESTINATION/$CMSSW/src/
cmsenv #alias for `scramv1 runtime -sh\


### Setting up CRAB
echo "\t Setting up CRAB3 Environment"#; pwd
#echo "source $CRAB"
source $CRAB


### Inform user of ROOT
set myROOTSYS = `echo $ROOTSYS`
echo "\t Working with ROOT version $myROOTSYS" 


### Setup Standalone Environment
cd $ENDPATH
echo "\t Setting Standalone environment"
#echo "source setup.csh"
source setup.csh


### Print Current Working Directory
set cwd = `pwd`
echo "=== setenv_cmssw_7_6_5.csh:\n\t Done! Current working directory is $cwd"
echo ""
