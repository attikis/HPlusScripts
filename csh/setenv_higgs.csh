#!/bin/csh
#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 1) then
    echo "\n=== You must give exactly 1 argument ($#argv given):"
    echo "1=PATH"
    echo "\n=== For example:"
    echo "source ~/HPlusScripts/csh/setenv_higgs.csh ~/w0"
    echo
    exit 1
endif


#================================================================================================
# Define variables
#================================================================================================
set DESTINATION=${1}
#/afs/cern.ch/user/a/attikis/w0/HiggsAnalysis

#================================================================================================
# Execute script steps
#================================================================================================
echo "\n=== Changing directory HiggsAnalysis"#; pwd
cd $DESTINATION/HiggsAnalysis/

echo "\n=== Setting environment"#; pwd
source setup.csh

echo "\n=== Done"
echo
