#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: lumicalc.sh <json>"
    exit
fi

export BRIL=brilconda-1.0.3
export BRILDIR=/afs/cern.ch/cms/lumi/$BRIL

echo $BRILDIR
export PATH=$HOME/.local/bin:$BRILDIR/bin:$PATH
# do this only once: pip install --install-option="--prefix=$HOME/.local" brilws

#export JSONPATH=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/
####export JSONPATH=./
####export JSON=$JSONPATH$1
export JSON=$1
echo $JSON

export NORMTAG=/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json
#export NORMTAG=/afs/cern.ch/user/l/lumipro/public/normtag_file/moriond16_normtag.json # 2015 data
echo $NORMTAG

#brilcalc lumi -b "STABLE BEAMS" --normtag $NORMTAG -u /pb -i $JSON
brilcalc lumi -b "STABLE BEAMS" -u /pb -i $JSON
#brilcalc lumi --xing -u /pb -i $JSON -o test.out
#brilcalc lumi --byls -i $JSON -o pileup.csv