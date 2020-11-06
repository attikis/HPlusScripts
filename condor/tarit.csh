#!/bin/tcsh
set timeStamp=`date +"%d%b%y"`
set CMSSWv=`pwd | grep -o -m 1 "CMSSW_.*/" | tr -d "/"`

# For testing:
# touch HiggsAnalysis_${CMSSWv}_${timeStamp}.tgz


tar -czvf HiggsAnalysis_${CMSSWv}_${timeStamp}.tgz HiggsAnalysis/.git/ \
                                HiggsAnalysis/.gitignore \
                                HiggsAnalysis/.gitmodules \
                                HiggsAnalysis/installexternals.sh \
                                HiggsAnalysis/NtupleAnalysis/ \
                                HiggsAnalysis/setenv.csh \
                                HiggsAnalysis/setup.sh \
                                HiggsAnalysis/XSectionsAndBr/ \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work/*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/FakeBMeasurement/work/FakeBMeasurement_*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/Hplus2tbAnalysis/work/Hplus2tbAnalysis_*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/TauFakeRate/work/TauFakeRate_*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/TauFakeRate/work/Plots*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/Hplus2hwAnalysisWithTop/work/Hplus2hwAnalysisWithTop*" \
    
