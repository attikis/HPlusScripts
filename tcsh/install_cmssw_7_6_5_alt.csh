#!/bin/csh

### Define variables
set DESTINATION="~/scratch0/"
set CMSSW_RELEASE="CMSSW_7_6_5"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc530" #See: https://cmssdt.cern.ch/SDT/cgi-bin/ReleasesXML
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"
set GIT_BRANCH="heitor"

### Execute commands
echo "\n=== Installing CMSSW=$CMSSW_RELEASE for USER=$USER at DESTINATION=$DESTINATION"; pwd
cd ~


#echo "\n=== Setting up SCRAM architecture"; pwd
#setenv SCRAM_ARCH $SCRAM_ARCHITECTURE 


echo "\n=== Changing directory to $DESTINATION + Listing available CMSSW releases"; pwd
cd $DESTINATION
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


echo "\n=== Setting environment"
source setup.csh


echo "\n=== Building NtupleAnalysis code (standalone code)"
cd NtupleAnalysis
make -j 16

echo "\n=== Building MiniAOD2TTree code (CMSSW code)"
cd ../MiniAOD2TTree/
scram b -j 16

echo "\n=== Done"; pwd

