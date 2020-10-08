#!/bin/csh

setenv SCRAM_ARCH slc7_amd64_gcc700

cd /afs/cern.ch/user/a/attikis/scratch0/

scram p CMSSW CMSSW_10_2_22
cd CMSSW_10_2_22/src
cmsenv

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j 8

git clone ssh://git@gitlab.cern.ch:7999/HPlus/HiggsAnalysis.git
cd HiggsAnalysis
git branch --track NanoAOD origin/NanoAOD
git checkout NanoAOD
cd NanoAODSkim/test
# python NanoAOD _HplusTauNuAnalysisSkim.py
