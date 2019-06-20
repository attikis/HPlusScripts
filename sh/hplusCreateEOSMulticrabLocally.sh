#!/bin/sh
#==================================================
# Script to make a multicrab directory with symbolic links
# Input parameters
# ----------------
#   eos_dir: eos Directory 
#   loc_dir: derivable local directory from the eos name
# nb: The name of the eos_dir should not end with / and the full path should be given
# usage:  ./mk_eos.sh /eos/uscms/store/<user>/<path> 
#
# LAST USED:
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
find ${eos_dir} > dir2create.txt
i=0

for File2Create in `awk -F: '{ print $1 }' dir2create.txt` # Read the content of the file 
do 
   i=$((i + 1))
#   if [ $i -gt 500 ] ; then
#       exit
#   fi
   if [[ -d "${File2Create}" ]] ; then
       Dir2Create=${File2Create#*"${eos_dir}/"}
       echo "Creating directory" $i ":...." ${Dir2Create}
       mkdir ${Dir2Create}
   else
       CrabDir=${File2Create#*"${eos_dir}/"}  # The part of the name without the $eos_dir
       DirPath=${CrabDir%/*}                  # The directory (excluding the part from /<filename>)
       FileName=${CrabDir#*"${DirPath}/"}     # The filename
       FullFileName=${DirPath}/${FileName}
       echo "Creating symbolic link..." $File2Create $FullFileName
       ln -s $File2Create $FullFileName 
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
