#!/bin/csh

### Ensure all script arguments are passed from command line
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments, in this order:"
    echo "1=INSTALLATION_PATH"
    echo "2=CMSSW_RELEASE"
    echo "3=GIT_BRANCH"
    echo "\n=== The arguments you provided were:"
    echo "1=$1"
    echo "2=$2"
    echo "3=$3"
    echo "\n=== For example:"
    echo "~/HPlusScripts/tcsh/install_cmssw_7_6_5.csh ~/scratch0/ CMSSW_7_6_5 cmssw76x" #or heitor
    echo 
    exit 1
endif

### Define variables
set INSTALLATION_PATH=$1 #~/scratch0/"
set CMSSW_RELEASE=$2 #"CMSSW_7_6_5"
set GIT_BRANCH=$3 #"heitor"
set HIGGS_SCRIPTS_TCSH=`echo $0 | sed 's,/*[^/]\+/*$,,'`
set HIGGS_SCRIPTS=`echo $HIGGS_SCRIPTS_TCSH | sed 's,/*[^/]\+/*$,,'`
set HIGGS_SCRIPTS_BASH=$HIGGS_SCRIPTS/bash/
set INSTALLATION_SCRIPT=$HIGGS_SCRIPTS_BASH/Higgs
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"


### Execute commands
echo "\n=== Will install $CMSSW_RELEASE (branch=$GIT_BRANCH) under $INSTALLATION_PATH for USER=$USER, using script $INSTALLATION_SCRIPT.\nContinue ? (Y/N)"
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

echo "\n=== Changing directory to $INSTALLATION_PATH + Listing available CMSSW releases"; pwd
cd $INSTALLATION_PATH
scram list | grep CMSSW


echo "\n=== Creating a local release area for $CMSSW_RELEASE (cmsrel)"; pwd
cmsrel $CMSSW_RELEASE


echo "\n=== Setting up CMS Runtime Environment (cmsenv)"; pwd
cd $CMSSW_RELEASE/src/
cmsenv #alias for `scramv1 runtime -sh\


echo "\n=== Cloning git-repository $GIT_REPO"
git clone $GIT_REPO


echo "\n=== Changing directory to $GIT_REPO_DIR"
cd $GIT_REPO_DIR
pwd


echo "\n=== Checking out branch $GIT_BRANCH"
git branch -a
git checkout -b $GIT_BRANCH origin/$GIT_BRANCH


echo "\n=== Install External Packages (BOOST)"
sh +x installexternals.sh


echo "\n=== Rehashing"
rehash


#echo "\n=== Setting environment"
#source setup.csh


echo "\n=== Building NtupleAnalysis code (standalone code)"
cd NtupleAnalysis
make -j 16


echo "\n=== Building MiniAOD2TTree code (CMSSW code)"
cd ../MiniAOD2TTree/
scram b -j 16


echo "\n=== Done"; pwd
