#!/bin/csh

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments, in this order:"
    echo "1=INSTALLATION_PATH"
    echo "2=CMSSW_RELEASE"
    echo "3=GIT_BRANCH"

    echo "\n=== For example:"
    echo "~/HPlusScripts/tcsh/install_cmssw.csh ~/scratch0/ 7_6_5 cmssw76x"
    echo 
    exit 1
endif

#================================================================================================
# Define variables
#================================================================================================
#set HIGGS_SCRIPTS_TCSH=`echo $0 | sed 's,/*[^/]\+/*$,,'`
#set HIGGS_SCRIPTS=`echo $HIGGS_SCRIPTS_TCSH | sed 's,/*[^/]\+/*$,,'`
#set HIGGS_SCRIPTS_BASH=$HIGGS_SCRIPTS/bash/
#set INSTALLATION_SCRIPT=$HIGGS_SCRIPTS_BASH/Higgs

set INSTALLATION_PATH=$1
set CMSSW_RELEASE=CMSSW_$2
set GIT_BRANCH=$3
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"

set SCRIPTS_REPO="$USER@lxplus.cern.ch:/afs/cern.ch/user/a/attikis/public/html/HPlusScripts.git/"
set SCRIPTS_PATH=bash/
set SCRIPTS_FILE=Higgs

#================================================================================================
# Execute commands
#================================================================================================
echo "\n=== Will install $CMSSW_RELEASE (branch=$GIT_BRANCH) under $INSTALLATION_PATH for USER=$USER. Continue ? (Y/N)"
set proceed=$<

if ($proceed == y || $proceed == Y) then
    echo "Continuing ..."
else if ($proceed == n || $proceed == N) then
    echo "Exiting ..."
    exit 1
else
    echo "Invalid option $proceed. Exiting ..."
    exit 1
endif


echo "Setting SCRAM ARCHITECTURE"
setenv SCRAM_ARCH 'slc6_amd64_gcc491'


echo "\n=== Changing directory to $INSTALLATION_PATH + Listing available CMSSW releases"#; pwd
cd $INSTALLATION_PATH
scram list | grep CMSSW


echo "\n=== Creating a local release area for $CMSSW_RELEASE (cmsrel)"#; pwd
cmsrel $CMSSW_RELEASE


echo "\n=== Getting installation script $SCRIPTS_FILE from remote repository $SCRIPTS_REPO$SCRIPTS_PATH"
cd $CMSSW_RELEASE/src/
git archive --remote=$SCRIPTS_REPO  HEAD:$SCRIPTS_PATH $SCRIPTS_FILE | tar -x


echo "\n=== Installing branch $GIT_BRANCH"#; pwd
./$SCRIPTS_FILE $GIT_BRANCH
rm -f $SCRIPTS_FILE

echo "\n=== Changing directory to $GIT_REPO_DIR"#; pwd
cd $GIT_REPO_DIR


echo "\n=== Setting environment"#; pwd
chmod +x setup.csh setup.sh
source setup.csh


echo "\n=== Rehashing"#; pwd
rehash


echo "\n=== Building NtupleAnalysis code (standalone code)"#; pwd
cd NtupleAnalysis
make -j 16


echo "\n=== Building MiniAOD2TTree code (CMSSW code)"#; pwd
cd ../MiniAOD2TTree/
#cmsenv #alias for `scramv1 runtime -sh\
scram b -j 16


echo "\n=== Done"#; pwd
