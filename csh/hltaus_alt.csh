#!/bin/csh
#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
# if ($#argv != 2 && $#argv != 3) then
#     echo "\n=== You must give exactly 2 argument ($#argv given):"
#     echo "1=PATH"
#     echo "2=CMSSW_RELEASE"
#     echo "\n=== For example:"
#     echo "source ~/HPlusScripts/tcsh/setenv_cmssw.csh ~/scratch0/ 7_6_5"
#     echo
#     exit 1
# endif


#================================================================================================
# Define variables
#================================================================================================
set DESTINATION="/afs/cern.ch/user/a/attikis/scratch0/" #${1}
set CMSSW="CMSSW_6_2_0_SLHC22" #${2}
set SETUPCRAB=true #${3}
set CRAB="/cvmfs/cms.cern.ch/crab3/crab.csh"
set CRABVERSION='crab --version'
set ENDPATH="/afs/cern.ch/user/a/attikis/scratch0/CMSSW_6_2_0_SLHC12_patch1/src/SLHCUpgradeSimulations/L1TrackTrigger/test"

#================================================================================================
# CMSSW
#================================================================================================
#echo "\n=== Setting environment for CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"#; pwd
cd ~

echo "\n=== Setting CMS Runtime Environment"
cd $DESTINATION/$CMSSW/src/
#pwd
cmsenv  

#================================================================================================
# CRAB
#================================================================================================
if ($SETUPCRAB == true) then
    
    echo "\n=== Setting CRAB3 Environment"
    source $CRAB

    set vCRAB = `$CRABVERSION`
    echo "\n=== Using CRAB Version $vCRAB"

    echo "\n=== Request a proxy to VO CMS. This looks for the user's Grid certificate in the  $HOME/.globus/ directory."
    set requestProxy='voms-proxy-init --voms cms'.
    
    echo "\n=== Request a longer validity using the --valid option. To request a proxy valid for seven days (168 hours)"
    set requestProxy7Days='voms-proxy-init --voms cms --valid 168:00'
    $requestProxy7Days
    # The proxy is saved in the /tmp/ directory of the current machine in a file named x509up_u<user-id>.
    # The user-id can be obtained by executing the command 'id -u'. Proxies are not specific to a login session;
    
    echo "\n=== Get more information about the proxy"
    set proxyInfo='voms-proxy-info --all'
    $proxyInfo
endif


#================================================================================================
# ENDPATH
#================================================================================================
cd $ENDPATH
echo "\n=== Done"
#ls
echo
