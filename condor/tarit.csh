#!/bin/tcsh

tar -czvf HiggsAnalysis.tgz HiggsAnalysis/.git/ \
                                HiggsAnalysis/.gitignore \
                                HiggsAnalysis/.gitmodules \
                                HiggsAnalysis/installexternals.sh \
                                HiggsAnalysis/NtupleAnalysis/ \
                                HiggsAnalysis/setup.csh \
                                HiggsAnalysis/setup.sh \
                                HiggsAnalysis/XSectionsAndBr/
