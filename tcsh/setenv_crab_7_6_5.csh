#!/bin/csh
#================================================================================================
# See the TWiki for "Running CMSSW code on the Grid using CRAB3"
#    https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
#================================================================================================

#================================================================================================
# Define variables
#================================================================================================
set CMSSW="CMSSW_7_6_5"
set DESTINATION="~/scratch0/"
set ENDPATH=$DESTINATION$CMSSW"/src/UCYHiggsAnalysis/MiniAOD2FlatTree/test/"
set gridUI='which grid-proxy-info'
set lcgGridUI='/afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.sh'
set arch=`echo $SCRAM_ARCH`
set crab3File='/cvmfs/cms.cern.ch/crab3/crab.csh'
set crabCheck='which crab'
set crabVersion='crab --version'


#================================================================================================
# Grid environment
#================================================================================================
# Source a Grid UI manually (Some sites provide the grid environment to all shells by default)
echo "=== setenv_crab_7_6_5.csh:\n\t Set Grid UI"
$gridUI

# Get the LCG Grid UI by sourcing the following (SLC6 has already the UI by default)
#echo "=== setenv_crab_7_6_5.csh:\n\t echo $lcgGridUI"
#echo $lcgGridUI

# Check whether the scram architecture is the one needed.
echo "=== setenv_crab_7_6_5.csh:\n\t $arch"
if ($arch =~ {slc6_amd64_gcc491,slc6_amd64_gcc481}) then
    echo "\t'$arch' is a valid SCRAM_ARCH environment variable"
else
    echo "\t'$arch' is not a valid SCRAM_ARCH environment variable."
    echo "\t Set SCRAM_ARCH to the desired SCRAM architecture with 'export SCRAM_ARCH=slc6_amd64_gcc491'." 
endif


#================================================================================================
# CMSSW environment
#================================================================================================
echo "=== setenv_crab_7_6_5.csh:\n\t cd $ENDPATH"
cd $ENDPATH
#pwd

# Setup the CMSSW environment
echo "=== setenv_crab_7_6_5.csh:\n\t cmsenv"
cmsenv


#================================================================================================
# CRAB environment
#================================================================================================
# Setup CRAB3 by sourcing a dedicated script.This script always points to the latest version of CRAB3.
echo "=== setenv_crab_7_6_5.csh:\n\t source $crab3File"
source $crab3File

# Check that the crab command is indeed available and the version being used by executing:
#echo "=== setenv_crab_7_6_5.csh:\n\t Check CRAB command"
#$crabCheck

# Or more explicitly
set vCRAB = `$crabVersion`
echo "=== setenv_crab_7_6_5.csh:\n\t CRAB Version used is $vCRAB"


#================================================================================================
# Get a CMS VO proxy
#================================================================================================
# Request a proxy to VO CMS. This looks for the user's Grid certificate in the  $HOME/.globus/ directory.
set requestProxy='voms-proxy-init --voms cms'. 
#echo "=== setenv_crab_7_6_5.csh:\n\t  $requestProxy"

# Request a longer validity using the --valid option. To request a proxy valid for seven days (168 hours):
set requestProxy7Days='voms-proxy-init --voms cms --valid 168:00'
echo "=== setenv_crab_7_6_5.csh:\n\t $requestProxy7Days"
$requestProxy7Days
# The proxy is saved in the /tmp/ directory of the current machine in a file named x509up_u<user-id>.
# The user-id can be obtained by executing the command 'id -u'. Proxies are not specific to a login session;

# Get more information about the proxy
set proxyInfo='voms-proxy-info --all'
echo "=== setenv_crab_7_6_5.csh:\n\t $proxyInfo"
$proxyInfo

#================================================================================================
# CMSSW environment (again)
#================================================================================================
# Setup the CMSSW environment
echo "=== setenv_crab_7_6_5.csh:\n\t cmsenv"
cmsenv

# Done
echo "=== setenv_crab_7_6_5.csh:\n\t done"

