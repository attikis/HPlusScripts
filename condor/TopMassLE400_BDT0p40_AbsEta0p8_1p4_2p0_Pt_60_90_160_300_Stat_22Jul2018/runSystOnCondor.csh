#!/bin/tcsh
#================================================================================================ 
# Get command line parameters
#================================================================================================ 
if ($#argv < 3) then
    echo "=== You must give at least 3 arguments:"
    echo "1=ANALYSISDIR"
    echo "2=LABEL"
    echo "3=GROUP"
    echo "4=SYSTEMATICS (optional)"
    echo
    exit 1
endif

#================================================================================================ 
# Define variables
#================================================================================================ 
set ANALYSISDIR = ${1}
set LABEL       = ${2}
set GROUP       = ${3}
set SYSTEMATICS = ${4}

#set TARBALL = multicrab_Hplus2tbAnalysis_v8030_20180223T0905
set TARBALL = multicrab_Hplus2tbAnalysis_v8030_20180508T0644

echo "\n=== Running on:" 
hostname -A
pwd
echo ${_CONDOR_SCRATCH_DIR}
source /cvmfs/cms.cern.ch/cmsset_default.csh

echo "\n=== Untarring the code tarball"
tar -xf HiggsAnalysis.tgz
rm -rf HiggsAnalysis.tgz

echo "\n=== Untarring the multicrab dir tarball"
tar -xf $TARBALL.tgz

# Source the environment settings script
echo "\n=== Changing dir to HiggsAnalysis and sourcing setup.csh"
cd HiggsAnalysis
source setup.csh
echo `pwd`

# Go to work directory to run the analysis
set WORKDIR = NtupleAnalysis/src/$ANALYSISDIR/work/
echo "\n=== Changing dir to $WORKDIR"
cd $WORKDIR

# Save the submit/start time for future use
set STIME = `date '+%Hh-%Mm-%Ss-%d%h%Y'`

# Run the analyser
echo "\n=== Running the analysis by executing runSystematics.py as follows:"
echo "./runSystematics.py -m ${_CONDOR_SCRATCH_DIR}/$TARBALL/ --doSystematics --group $GROUP\n"
./runSystematics.py -m ${_CONDOR_SCRATCH_DIR}/$TARBALL/ --group $GROUP --systVars $SYSTEMATICS 

echo "\n=== Listing all directories"
echo`ls -alt | grep ^d` #| grep $ANALYSISDIR`

echo "\n=== Listing the latest directory"
echo `ls -td */ | head -1`

echo "\n=== Determining output dir using ls and grep commands"
set OUTPUTDIR = `ls -td */ | head -1`
echo "\n=== Output dir determined to be $OUTPUTDIR"
# -t orders by time (latest first)
# -d only lists items from this folder
# */ only lists directories
# head -1 returns the first item

# Create the tarball name
set FTIME = `date '+%Hh-%Mm-%Ss-%d%h%Y'`
# set TIME = `date '+%Hh%Mm%Ss_%d%h%Y'`
# set TIME = `date '+%Hh-%Mm-%Ss-%d%h%Y'`
# set TIME = `date '+%d%h%Y'`
# set TIME = `date +"%d%m%Y"`
echo "\n=== Tarball name will be ${ANALYSISDIR}_${LABEL}_${STIME}_${FTIME}.tgz"
set TARBALL = "${ANALYSISDIR}_${LABEL}_${STIME}_${FTIME}.tgz"

# Make the output directory to a tarball
echo "\n=== Compressing the output dir $OUTPUTDIR into tarball file $TARBALL"
tar -cvzf $TARBALL $OUTPUTDIR

#echo "\n=== Copying output directory $OUTPUTDIR to EOS"
#xrdcp -rf $OUTPUTDIR  root://cmseos.fnal.gov//store/user/$USER/.
set EOSDIR = store/user/$USER/CONDOR_TransferData
echo "\n=== Copying output tarball $TARBALL to $EOSDIR"
xrdcp $TARBALL  root://cmseos.fnal.gov//$EOSDIR/

echo "\n=== Delete everything from ${_CONDOR_SCRATCH_DIR} before exiting"
cd ${_CONDOR_SCRATCH_DIR}
rm -rf HiggsAnalysis
