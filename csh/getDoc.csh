#!/bin/csh

#==========================================================================================================================
# Script Arguments
#==========================================================================================================================
if ($#argv != 2 ) then
    echo "=== getDoc.csh:\n\t Two script arguments must be passed on execution:"
    echo "\t 1) The type of document to checkout (PAS, AN, PAPER)"
    echo "\t 2) The AN/PAS/PAPER number (AN-15-321 or HIG-11-019)"
    echo ""
    echo "\t Examples:"
    echo "\t ./getDoc.csh AN AN-15-321"
    echo "\t ./getDoc.csh PAS HIG-11-008"
    echo "\t ./getDoc.csh PAPER HIG-11-019"
    echo 
    echo "\t Twiki:"
    echo "\t https://twiki.cern.ch/twiki/bin/view/Main/SubmittingAN"  
    exit 1
endif
set noteType=$1 # 'AN', 'PAS', 'PAPER'
set NOTE=$2     # 'AN-15-321', 'HIG-11-019'


#==========================================================================================================================
# Ask to continue
#==========================================================================================================================
echo "=== getDoc.csh:\n\t Will checkout $NOTE (type=$noteType). Do you want to proceed (y/n)?"
set userInput = $<
if ($userInput == y) then
    echo "\t ..."
else
    echo "\t EXIT [ userInput=$userInput (instead of 'y') ]"
    exit -1
endif


#==========================================================================================================================
# Main body
#==========================================================================================================================
echo "=== getDoc.csh:"
if (! -d tdr2 ) then
    echo "\t svn co -N svn+ssh://attikis@svn.cern.ch/reps/tdr2"
    svn co -N svn+ssh://attikis@svn.cern.ch/reps/tdr2
    echo "\t cd tdr2"
    cd tdr2
else
    echo "\t cd tdr2"
    cd tdr2
endif


echo "=== getDoc.csh:\n\t svn update utils"
svn update utils


echo "=== getDoc.csh:"
if ($noteType == 'PAPER') then
    echo "\t Updating papers"
    svn update -N papers
else
    echo "\t Updating notes"
    svn update -N notes
endif


echo "=== getDoc.csh:"
if ($noteType == 'PAPER') then
    echo "\t svn update papers/$NOTE"
    svn update papers/$NOTE
else
    echo "\t svn update notes/$NOTE"
    svn update notes/$NOTE
endif


echo "=== getDoc.csh:"
if ($noteType == 'PAPER') then
    #echo "\t cd papers"
    cd papers
    #echo "\t pwd=`pwd`"
else
    #echo "\t cd notes"
    cd notes
    #echo "\t pwd=`pwd`"
endif


# Set commands
set tdr = ''
set cwd = `pwd`
set eval='eval `./tdr runtime -csh`'


# Determine compilation command
if ($noteType == 'PAPER') then
    set tdr="tdr --style paper b $NOTE"
 else if ($noteType == 'PAS') then
    set tdr="tdr --style pas b $NOTE"
else if ($noteType == 'AN') then
    set tdr="tdr --style an b $NOTE"
else 
    echo "=== getDoc.csh:\n\t ERROR! Unknown note type $-NOTE"
    exit 1
endif

echo "\nTo compile copy/paste the following:"
echo "cd $cwd && $eval && $tdr"
echo
