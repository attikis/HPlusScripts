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
set INSTALLATION_PATH=$1
set CMSSW_RELEASE=CMSSW_$2
set GIT_BRANCH=$3
set GIT_REPO_DIR="HiggsAnalysis"
set GIT_REPO="http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git"
set SCRIPTS_REPO="$USER@lxplus.cern.ch:/afs/cern.ch/user/a/attikis/public/html/HPlusScripts.git/"
set SCRIPTS_PATH=bash/
set SCRIPTS_FILE=Higgs
#set SCRAM_ARCHITECTURE="slc6_amd64_gcc493"
set SCRAM_ARCHITECTURE="slc6_amd64_gcc530" #19 July 2016

#================================================================================================
# Execute commands
#================================================================================================
echo "\n=== Will install $CMSSW_RELEASE (branch=$GIT_BRANCH) under $INSTALLATION_PATH for USER=$USER with SCRAM ARCHITECTURE=$SCRAM_ARCHITECTURE (CMSSW-compatible?)"
echo "=== Continue ? (Y/N)"
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


echo "\n=== Setting SCRAM ARCHITECTURE"
#echo "setenv SCRAM_ARCH 'slc6_amd64_gcc493'"
#setenv SCRAM_ARCH 'slc6_amd64_gcc493' #works
#
echo "setenv SCRAM_ARCH $SCRAM_ARCHITECTURE" 
setenv SCRAM_ARCH $SCRAM_ARCHITECTURE #19 July 2016


echo "\n=== Changing directory to $INSTALLATION_PATH"#; pwd
cd $INSTALLATION_PATH
# pwd


# echo "\n=== Listing available CMSSW releases"
# echo "scram list | grep CMSSW"
# scram list | grep CMSSW


echo "\n=== Creating a local release area for $CMSSW_RELEASE"
echo "cmsrel $CMSSW_RELEASE"
cmsrel $CMSSW_RELEASE


echo "\n=== Changing directory to $CMSSW_RELEASE/src/"
cd $CMSSW_RELEASE/src/
#pwd

# Instructions for 2016 analysis: Stop program execution, print out a message, and wait for user to  press <RETURN>
set text = "\n=== WARNING! Changes are required for 2016 Analysis (8X) that are not yet automated. See https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChFullyHadronic#MiniAOD2TTree_Producer for more info. Exiting.."
printf "\n$text"
set junk = ($<)
echo 
exit 1


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
#pwd


echo "\n=== Setting environment"
chmod +x setup.csh setup.sh
echo "source setup.csh"
source setup.csh


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


echo "\n=== Building MiniAOD2TTree code (CMSSW code)"#; pwd
echo "cmsenv && scram b -j 16"
cmsenv && scram b -j 16


echo "\n=== Done"
pwd
echo "\n"
