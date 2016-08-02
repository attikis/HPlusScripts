#!/bin/csh

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments, in this order:"
    echo "1=INSTALLATION_PATH"
    echo "2=GIT_BRANCH"

    echo "\n=== For example:"
    echo "~/HPlusScripts/tcsh/install_cmssw.csh ~/scratch0/ cmssw76x"
    echo 
    exit 1
endif


#================================================================================================
# Define variables
#================================================================================================
set INSTALLATION_PATH=$1
set GIT_BRANCH=$2
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"
set SCRIPTS_REPO="https://github.com/attikis/HPlusScripts.git"
set SCRIPTS_PATH=bash/
set SCRIPTS_FILE=Higgs


#================================================================================================
# Execute commands
#================================================================================================
echo "\n=== Will install git branch=$GIT_BRANCH under $INSTALLATION_PATH for USER=$USER. Continue ? (Y/N)"
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

echo "\n=== Changing directory to $INSTALLATION_PATH"#; pwd
cd $INSTALLATION_PATH
# pwd


echo "\n=== Getting installation script $SCRIPTS_FILE from remote repository"
echo "git archive --remote=$SCRIPTS_REPO  HEAD:$SCRIPTS_PATH $SCRIPTS_FILE | tar -x"
git archive --remote=$SCRIPTS_REPO  HEAD:$SCRIPTS_PATH $SCRIPTS_FILE | tar -x


echo "\n=== Installing branch $GIT_BRANCH"
echo "./$SCRIPTS_FILE $GIT_BRANCH"
./$SCRIPTS_FILE $GIT_BRANCH


echo "\n=== Deleting installation script"
echo "rm -f $SCRIPTS_FILE"
rm -f $SCRIPTS_FILE


echo "\n=== Changing directory to $GIT_REPO_DIR/"
cd $GIT_REPO_DIR
pwd


echo "\n=== Setting environment"
chmod +x setup.csh setup.sh
echo "source setup.csh"
sh +x setup.sh


echo "\n=== Re-compute the internal hash table (to account for new commands added)"
echo "rehash"
rehash


echo "\n=== Changing directory to NtupleAnalysis/"
cd NtupleAnalysis
#pwd


echo "\n=== Building NtupleAnalysis code (standalone code)"
echo "make -j 16"
make -j 16


echo "\n=== Changing directory to MiniAOD2TTree/"
cd ../MiniAOD2TTree/


echo "\n=== Done"
pwd
echo "\n"
