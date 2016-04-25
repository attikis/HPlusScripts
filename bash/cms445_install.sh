#!/usr/bin/env bash

### Traditional way
cd /afs/cern.ch/user/a/attikis/scratch0/
setenv SCRAM_ARCH "slc5_amd64_gcc462" #export SCRAM_ARCH="slc5_amd64_gcc462"
cmsrel CMSSW_4_4_5
cd CMSSW_4_4_5/src
echo pwd
git clone http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git
cd HiggsAnalysis
echo "*** cwd:"
pwd
git checkout -b 2011 origin/2011
cd ..
echo "*** cwd:"
pwd
cmsenv
source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh
source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
echo "*** cwd:"
pwd
./HiggsAnalysis/HeavyChHiggsToTauNu/test/checkoutTags.sh
scram b -j 16

cd
echo "*** cwd:"
pwd
cd /afs/cern.ch/user/a/attikis/scratch0/CMSSW_4_4_5/src/HiggsAnalysis/
echo "*** cwd:"
pwd

### Take care of git repos
git remote add lxplus http://cmsdoc.cern.ch/~attikis/HiggsAnalysis.git
git remote add sami http://cmsdoc.cern.ch/~slehti/HiggsAnalysis.git
git remote add matti http://cmsdoc.cern.ch/~mkortela/HiggsAnalysis.git
git remote add lauri http://cmsdoc.cern.ch/~wendland/HiggsAnalysis.git
git remote add ritva http://cmsdoc.cern.ch/~kinnunen/HiggsAnalysis.git
git remote add alexandros http://cmsdoc.cern.ch/~attikis/HiggsAnalysis.git
git remote add tapio http://cmsdoc.cern.ch/~tlampen/HiggsAnalysis.git
git remote add cristina http://cmsdoc.cern.ch/~cferro/HiggsAnalysis.git
git remote add stefan http://cmsdoc.cern.ch/~srichter/HiggsAnalysis.git

echo "The following git aliases have been set up (check that the path for public is correct!):"
git remote -v

