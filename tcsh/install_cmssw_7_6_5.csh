#!/bin/csh

### Define variables
set DESTINATION="~/scratch0/"
set CMSSW_RELEASE="CMSSW_7_6_5"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc530" #See: https://cmssdt.cern.ch/SDT/cgi-bin/ReleasesXML
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"
set HIGGS_SCRIPT="~/HPlusScripts/bash/Higgs"
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


echo "\n=== Installing branch $GIT_BRANCH using installation script Higgs from $GIT_REPO_SCRIPTS"; pwd
sh +x $HIGGS_SCRIPT $GIT_BRANCH


echo "\n=== Changing directory to $GIT_REPO_DIR"; pwd
cd $GIT_REPO_DIR


echo "\n=== Install External Packages (BOOST)"; pwd
sh +x installexternals.sh


echo "\n=== Rehashing"; pwd
rehash


echo "\n=== Setting environment"; pwd
source setup.csh


echo "\n=== Building NtupleAnalysis code (standalone code)"; pwd
cd NtupleAnalysis
make -j 16


echo "\n=== Building MiniAOD2TTree code (CMSSW code)"; pwd
cd ../MiniAOD2TTree/
scram b -j 16


echo "\n=== Done"; pwd
