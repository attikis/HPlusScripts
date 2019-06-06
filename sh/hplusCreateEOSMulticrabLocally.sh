#!/bin/sh
#==================================================
# Script to make a multicrab directory with symbolic links
# Input parameters
# ----------------
#   eos_dir: eos Directory 
#   loc_dir: local directory
# nb: The name of the eos_dir should not end with / 
#
# LAST USED:
# ./hplusCreateEOSMulticrabLocally.sh /eos/uscms/store/user/aattikis/CRAB3_TransferData/multicrab_Hplus2hwAnalysis_v8030_20181205T1455
#
# Helpful tricks
# RemoteUser=${eos_dir%%:*} # to remove everything from : to end of $To_Dir var
# RemoteDir=${eos_dir#*:}   # get the remote directory removing up to :
#====================================================
eos_dir=$1
loc_dir=${eos_dir##*/} # trick to get the last directory part of the $eos_dir
if [ ! -d "${loc_dir}" ] ; then 
    mkdir ${loc_dir}
    echo ${loc_dir}
fi
cd ${loc_dir}
echo "===================================================="
echo "      Setting up to remote copy with parameters     "
echo "At directory:  " `pwd`
echo "EOS Directory: " ${eos_dir}
echo "Loc Directory: " ${loc_dir}
echo "===================================================="
#eosls -1 ${eos_dir} > dir2create.txt  # Put the dir content to be copied in a file to read it
find ${eos_dir} > dir2create.txt
i=0
for File2Create in `awk -F: '{ print $1 }' dir2create.txt` # Read the content of the file 
do 
   i=$((i + 1))
#   if [ $i -gt 20 ] ; then
#       exit
#   fi
   if [[ -d "${File2Create}" ]] ; then
       Dir2Create=${File2Create#*"${eos_dir}/"}
       echo "Creating directory" $i ":...." ${Dir2Create}
       mkdir ${Dir2Create}
   else
       filename=${Dir2Create}/${File2Create#*"${Dir2Create}/"}
       echo "Creating symbolic link..." $File2Create $filename
       ln -s $File2Create $filename 
   fi
   status=$?
   if [ $status -eq 0 ];then
      echo "Succesfully created"
   else
      echo "Symbolic link failed"
   fi 
done
rm dir2create.txt

# Create multicrab.cfg file
find * -maxdepth 0 -type d | awk '{print "["$1"]"}' > multicrab.cfg 
exit
