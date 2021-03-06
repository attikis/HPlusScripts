#!/bin/csh
#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 2) then
    echo "\n=== You must give exactly 2 argument ($#argv given):"
    echo "1=PATH"
    echo "2=CMSSW_RELEASE"
    echo "\n=== For example:"
    echo "source ~/HPlusScripts/tcsh/setenv_cmssw.csh ~/scratch0/ 7_6_5"
    echo
    exit 1
endif


#================================================================================================
# Define variables
#================================================================================================
set DESTINATION=${1}
set CMSSW="CMSSW_"${2}
set ENDPATH="HiggsAnalysis/"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc472"
set CRAB_UI_ENV="/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh"
set CRAB="/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh"


#================================================================================================
# Execute script steps
#================================================================================================
echo "\n=== Setting environment for CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"#; pwd
cd ~
pwd


echo "\n=== Setting Standalone environment"
cd $DESTINATION/$CMSSW/src/$ENDPATH 
pwd
source setup.csh


echo "\n=== Setting CMS Runtime Environment"
cd ../
pwd
cmsenv #alias for `scramv1 runtime -csh`


echo "\n=== Setting CRAB3 Environment"
source $CRAB


set myROOTSYS = `echo $ROOTSYS`
echo "\t Working with ROOT version $myROOTSYS"


echo "\n=== Done"
ls
echo
