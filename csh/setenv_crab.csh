#!/bin/csh
#================================================================================================
# See the TWiki for "Running CMSSW code on the Grid using CRAB3"
#    https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
#================================================================================================

### Ensure all script arguments are passed from command line
if ($#argv != 2) then
    echo "=== You must give exactly 2 argument:"
    echo "1=PATH"
    echo "2=CMSSW_RELEASE"
    echo "\n=== The arguments you provided were:"
    echo "1=$1"
    echo "2=$2"
    echo "\n=== For example:"
    echo "source ~/HPlusScripts/tcsh/setenv_crab.csh ~/scratch0/ CMSSW_7_6_5"
    echo
    exit 1
endif

#================================================================================================
# Define variables
#================================================================================================
set PATH=$1
set CMSSW=$2
set ENDPATH=$PATH$CMSSW"/src/HiggsAnalysis/MiniAOD2TTree/test/"
set gridUI='which grid-proxy-info'
set lcgGridUI='/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh'
set arch=`echo $SCRAM_ARCH`
#set crabScript='/cvmfs/cms.cern.ch/crab3/crab.csh' #sourcing this crashes for some reason. script-related bug
set crabScript='/cvmfs/cms.cern.ch/crab3/crab.sh'
set crabCheck='which crab'
set crabVersion='crab --version'


#================================================================================================
# Grid environment
#================================================================================================
echo "\n=== Source a Grid UI manually (Some sites provide the grid environment to all shells by default)"; pwd
$gridUI


#echo "\n=== Get the LCG Grid UI by sourcing the following (SLC6 has already the UI by default)"
#echo $lcgGridUI


#echo "\n=== Check whether the scram architecture is the one needed"; pwd
#if ($arch =~ {slc6_amd64_gcc491,slc6_amd64_gcc481}) then
#    echo "'$arch' is a valid SCRAM_ARCH environment variable"
#else
#    echo "'$arch' is not a valid SCRAM_ARCH environment variable."
#    echo "Set SCRAM_ARCH to the desired SCRAM architecture with 'export SCRAM_ARCH=slc6_amd64_gcc491'." 
#endif


#================================================================================================
# CMSSW environment
#================================================================================================
echo "\n=== Changing directory to $ENDPATH"; pwd
cd $ENDPATH


echo "\n=== Setting up CMS Runtime Environment"; pwd
cmsenv


echo "\n=== Using SCRAM architecture $SCRAM_ARCH";


#================================================================================================
# CRAB environment
#================================================================================================
echo "\n=== Setting up CRAB3 by sourcing script that always points to the latest version of CRAB."; pwd
sh +x  $crabScript

#echo "\n=== Check that the crab command is indeed available and the version being used by executing:"
#$crabCheck


# Or more explicitly
set vCRAB = `$crabVersion`
echo "\n=== Using CRAB Version $vCRAB"; pwd

#================================================================================================
# Get a CMS VO proxy
#================================================================================================
echo "\n=== Request a proxy to VO CMS. This looks for the user's Grid certificate in the  $HOME/.globus/ directory."; pwd
set requestProxy='voms-proxy-init --voms cms'. 


echo "\n=== Request a longer validity using the --valid option. To request a proxy valid for seven days (168 hours)"; pwd
set requestProxy7Days='voms-proxy-init --voms cms --valid 168:00'
$requestProxy7Days
# The proxy is saved in the /tmp/ directory of the current machine in a file named x509up_u<user-id>.
# The user-id can be obtained by executing the command 'id -u'. Proxies are not specific to a login session;


echo "\n=== Get more information about the proxy"; pwd
set proxyInfo='voms-proxy-info --all'
$proxyInfo


#================================================================================================
# CMSSW environment (again)
#================================================================================================
echo "\n=== Setting up CMS Runtime Environment"; pwd
cmsenv


echo "\n=== Done! Current working directory is $cwd"
echo ""

