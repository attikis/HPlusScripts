#!/bin/tcsh
#================================================================================================ 
# Get command line parameters
#================================================================================================ 
if ($#argv != 1) then
    echo "=== You must give exactly 1 argument:"
    echo "1=ANALYSISDIR"
    echo
    exit 1
endif

#================================================================================================ 
# Define variables
#================================================================================================ 
set ANALYSISDIR = ${1}

echo "=== Running on:" 
hostname -A
pwd
echo ${_CONDOR_SCRATCH_DIR}
source /cvmfs/cms.cern.ch/cmsset_default.csh

echo "=== Untarring the code tarball"
tar -xf HiggsAnalysis.tgz
rm -rf HiggsAnalysis.tgz

echo "=== Untarring the multicrab dir tarball"
tar -xf multicrab_Hplus2tbAnalysis_v8030_20180223T0905.tgz

echo "=== Changing dir to HiggsAnalysis"
cd HiggsAnalysis

echo "=== Sourcing setup.csh"
source setup.csh
echo `pwd`

echo "=== Changing dir to "
cd NtupleAnalysis/src/$ANALYSISDIR/work/

echo "=== Running the analysis"
./run.py -m ${_CONDOR_SCRATCH_DIR}/multicrab_Hplus2tbAnalysis_v8030_20180223T0905/

echo "=== Copying output to EOS"
set OUTPUTDIR = `ls -al | grep ^d | grep $ANALYSISDIR`
xrdcp -rf $OUTPUTDIR  root://cmseos.fnal.gov//store/user/$USER/.

echo "=== Delete everythig before exiting"
cd ${_CONDOR_SCRATCH_DIR}
rm -rf HiggsAnalysis
