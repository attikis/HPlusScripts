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
set INITIAL=`echo $USER | cut -c1-1`
set DESTINATION="/afs/cern.ch/user/$INITIAL/$USER/scratch0/" #${1}
set CMSSW="CMSSW_${1}"
set SETUPCRAB=true #${3}
set CRAB="/cvmfs/cms.cern.ch/crab3/crab.csh"
set CRABVERSION='crab --version'
if ($CMSSW == "CMSSW_6_2_0_SLHC12_patch1") then
    set ENDPATH="$DESTINATION/$CMSSW/src/SLHCUpgradeSimulations/L1TrackTrigger/test"
    else
    #set ENDPATH="$DESTINATION/$CMSSW/src/L1Trigger/TrackFindingTracklet/test/"
    #set ENDPATH="$DESTINATION/$CMSSW/src/L1Trigger/L1TCommon/test"
    set ENDPATH="$DESTINATION/$CMSSW/src/L1Trigger/L1TNtuples/plugins"
endif
#set SCRAM_ARCHITECTURE="slc5_amd64_gcc472" #"slc5_amd64_gcc472"

#================================================================================================
# SCRAM ARCHITECTURE
#================================================================================================
#echo "\n=== Setting SCRAM ARCHITECTURE"
#echo "setenv SCRAM_ARCH $SCRAM_ARCHITECTURE"
#setenv SCRAM_ARCH $SCRAM_ARCHITECTURE
# According to Stefano (CRAB Support)
# the Production architecture for the "CMSSW_6_2_0_SLHC12_patch1" release  is slc5_amd64_gcc472
# and NOT slc6_amd64_gcc472. If not changed it will cause  errors when delegating My-proxy in CRAB
# submission time. "That error is not there when using the production architecture for this
# release, at least not in  a quick test I did. If you use a CMSSW release which breaks the SSL
#  library needed by myproxy, it is very hard for CRAB (or any possible trick) to fix it.


#================================================================================================
# CMSSW
#================================================================================================
echo "\n=== Setting environment for CMSSW=$CMSSW for USER=$USER at DESTINATION=$DESTINATION"#; pwd
cd ~

echo "\n=== Setting CMS Runtime Environment"
cd $DESTINATION/$CMSSW/src/
#pwd
echo 'cmsenv'
cmsenv
echo


#================================================================================================
#setenv SCRAM_ARCH $SCRAM_ARCHITECTURE
# CRAB
#================================================================================================
if ($SETUPCRAB == true) then
    
    echo "\n=== Setting CRAB3 Environment"
    echo 'source $CRAB'
    source $CRAB

    set vCRAB = `$CRABVERSION`
    echo "\n=== CRAB Version $vCRAB"

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
    echo
endif


#================================================================================================
# ENDPATH
#================================================================================================
cd $ENDPATH
echo "\n=== Done"
ls
echo
