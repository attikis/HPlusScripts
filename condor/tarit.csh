#!/bin/tcsh

tar -czvf HiggsAnalysis.tgz HiggsAnalysis/.git/ \
                                HiggsAnalysis/.gitignore \
                                HiggsAnalysis/.gitmodules \
                                HiggsAnalysis/installexternals.sh \
                                HiggsAnalysis/NtupleAnalysis/ \
                                HiggsAnalysis/setup.csh \
                                HiggsAnalysis/setup.sh \
                                HiggsAnalysis/XSectionsAndBr/ \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work/*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/FakeBMeasurement/work/FakeBMeasurement_*" \
    --exclude "HiggsAnalysis/NtupleAnalysis/src/Hplus2tbAnalysis/work/Hplus2tbAnalysis_*" \

