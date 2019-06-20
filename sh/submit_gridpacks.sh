#!/bin/bash  
DIR=cards/production/2017/13TeV/ChargedHiggs_TB/ChargedHiggs_TB_madspin_NLO_M500
BASE=$(basename $DIR)
nohup ./submit_cmsconnect_gridpack_generation.sh ${BASE} ${DIR} 16 "16 Gb" > ${BASE}_$(date '+%d%b%Y').debug 2>&1 &
