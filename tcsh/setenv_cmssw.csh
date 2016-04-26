#!/bin/csh

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 2) then
    echo "=== You must give exactly 2 argument ($#argv given):"
    echo "1=PATH"
    echo "2=CMSSW_RELEASE"
    echo "\n=== For example:"
    echo "source /HPlusScripts/tcsh/setenv_cmssw.csh ~/scratch0/ 7_6_5"
    echo
    exit 1
endif

#================================================================================================
# Define variables
#================================================================================================
set PATH=$argv[1]
set CMSSW="CMSSW_"$argv[2]
set ENDPATH=$PATH/$CMSSW"/src/HiggsAnalysis/"
set CRAB_UI_ENV="/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh"
set CRAB="/afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh"


#================================================================================================
# Execute the script
#================================================================================================
echo "\n=== Setting environment for CMSSW=$CMSSW for USER=$USER at PATH=$PATH"#; pwd
cd ~


echo "\n=== Setting up CMS Runtime Environment"#; pwd
cd $PATH/$CMSSW/src/
cmsenv #alias for `scramv1 runtime -sh\


echo "\n=== Setting up CRAB3 Environment"#; pwd
source $CRAB


set myROOTSYS = `echo $ROOTSYS`
echo "\n=== Working with ROOT version $myROOTSYS"#; pwd


echo "\n=== Setting Standalone environment"#; pwd
cd $ENDPATH
source setup.csh


set cwd = `pwd`
echo "\n=== Done! Current working directory is $cwd"
echo ""
