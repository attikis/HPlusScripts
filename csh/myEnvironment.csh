#############################################################################
### File ............: myEnvironment.csh
### Description:.....: general purpose environment script file
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################      
echo "\n=== $HOME/myEnvironment.csh"
set USER_INITIAL=`echo $USER | cut -c1`

############################################################################# 
# Determine Location
############################################################################# 
if (! $?LOCATION) then 
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "Mac"* ) then
        set LOCATION="mac"
     else if (`hostname` =~ *".cern.ch" ) then  #Example: p06109780e53561.cern.ch
        set LOCATION="lxbatch"
     else if (`hostname` =~ *".fnal.gov" ) then #Example: cmslpc35.fnal.gov
        set LOCATION="lpc"
    endif
endif
   

############################################################################# 
# Enable tab completion to show a menu of options (tcsh)
############################################################################# 
set autolist


#############################################################################      
# Set PATHS & Environment variables
#############################################################################      
#setenv EOS /store/user/$USER/CRAB3_TransferData
setenv EOS /eos/cms/store/user/attikis
setenv EOSHOME /eos/cms/store/user/attikis
setenv BOX /eos/user/$USER_INITIAL/$USER/ #CRAB3_TransferData
setenv CERNBOX /eos/user/$USER_INITIAL/$USER/ #CRAB3_TransferData
#setenv BOX /eos/home-a/attikis/CRAB3_TransferData/
setenv PUBLIC $HOME/public
setenv SCRATCH $HOME/scratch0
setenv TMP /tmp/${USER}
setenv W0 $HOME/w0
setenv WORKSPACE /afs/cern.ch/work/$USER_INITIAL/$USER


#############################################################################
# Setup my prompt
#############################################################################
set prompt = '[%n@%m:%c]%#'


#############################################################################
# Set aliases
#############################################################################
alias H              'history -r | fgrep "\!*"'
alias ps             'ps l'
alias cmsenvUnset    'eval `scram unsetenv -sh`'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw.csh ~/scratch0/ 8_0_27 false'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 8_0_27 false'
#alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 8_0_27 true'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_1_5 false'
#alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_1_5 true'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/scratch0/ 10_1_7 false'
#alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/scratch0/ 10_1_7 true'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/scratch0/ 10_5_0_pre1 false'
#alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/scratch0/ 10_5_0_pre1 true'
#alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/ 10_1_7 false'
#alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/ 10_1_7 true'
alias cmssw          'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_6_0_pre4 false'
alias cmssw-crab     'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_6_0_pre4 true'
alias cmssw-crab-1   'cmssw-crab && cd /afs/cern.ch/user/a/attikis/workspace/cmssw/CMSSW_10_6_0_pre4/src/HLTausAnalysis/Raw2TTree' 
alias cmssw-crab-2   'cmssw-crab && cd /afs/cern.ch/user/a/attikis/workspace/cmssw/CMSSW_10_6_0_pre4/src/L1Trigger/Phase2L1Taus/test/'
alias hltaus-produce 'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_6_1_patch2 true && cd /afs/cern.ch/user/a/attikis/workspace/cmssw/CMSSW_10_6_1_patch2/src/L1Trigger/Phase2L1Taus/test/'
alias hltaus-ntuples 'source ~/HPlusScripts/csh/setenv_cmssw_hltaus.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 10_6_1_patch2 true && cd /afs/cern.ch/user/a/attikis/workspace/cmssw/CMSSW_10_6_1_patch2/src/HLTausAnalysis/Raw2TTree'
alias keras         'cd ~/scratch0/CMSSW_10_2_11/src/ && cmsenv && setenv SCRAM_ARCH slc7_amd64_gcc700 && cd /afs/cern.ch/user/a/attikis/workspace/Keras_ANN/'

alias d3            'cd /uscms_data/d3/aattikis/workspace/'
alias work          'cd /afs/cern.ch/user/a/attikis/workspace/'
alias emacs         'emacs -nw'
alias glogin        'source $HOME/bin/grid_environment'
alias grid          'source $HOME/bin/grid_environment'
alias h             'history'
alias higgs         'source ~/HPlusScripts/csh/setenv_higgs.csh /afs/cern.ch/user/a/attikis/workspace/cmssw/ 8_0_27'
alias cmssw920      'source ~/HPlusScripts/csh/hltaus.csh 9_2_0'
alias cmssw910      'source ~/HPlusScripts/csh/hltaus.csh 9_1_0_pre2'
alias cmssw620      'source ~/HPlusScripts/csh/hltaus.csh 6_2_0_SLHC12_patch1'
alias tkTaus        'hltaus && source setup.csh && cd NtupleAnalysis/src/TkTaus/work'
alias tkEG          'hltaus && source setup.csh && cd NtupleAnalysis/src/TkEG/work'
alias caloTk        'hltaus && source setup.csh && cd NtupleAnalysis/src/CaloTk/work'
alias caloTau       'hltaus && source setup.csh && cd NtupleAnalysis/src/CaloTau/work'
alias limits        'source ~/HPlusScripts/csh/setenv_limits.csh ~/scratch0/ 8_1_0' #do NOT name alias "combine"
alias madgraph      'cd /afs/cern.ch/user/a/attikis/workspace/MCProduction2017/genproductions/bin/MadGraph5_aMCatNLO'
alias l             'ls -lth'
alias ls            'ls -pt --color=auto'
alias lsd           'ls -lpt --color=force | grep ^d'
alias lxplus        'ssh -N -L 10121:itrac50012-v.cern.ch:10121 attikis@lxplus.cern.ch'
alias uscms         'ssh -Y attikis@login.uscms.org'
alias pwd           'echo $cwd'
alias rm            'rm -i'
alias root          'root -l'
#alias scram530      'setenv SCRAM_ARCH $SCRAM_ARCHITECTUREgcc530'
#alias scram600      'setenv SCRAM_ARCH $SCRAM_ARCHITECTUREgcc600'
#alias scram630      'setenv SCRAM_ARCH $SCRAM_ARCHITECTUREgcc630'
#alias scram700      'setenv SCRAM_ARCH $SCRAM_ARCHITECTUREgcc700'
alias setmyscram    'setenv SCRAM_ARCH slc7_amd64_gcc700'
alias slc6          'setenv SCRAM_ARCH slc6_amd64_gcc630'
alias setbrilcalc   'setenv PATH ${PATH}:$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:'
alias setcrab       'source /cvmfs/cms.cern.ch/crab3/crab.csh'
alias ssh           'ssh -Y'


if ( "$LOCATION" == "lxplus" ) then
    alias hltaus 'cd /afs/cern.ch/user/a/attikis/workspace/cmssw/CMSSW_10_6_0_pre4/src/HLTausAnalysis/'
    #alias hltaus 'cd /afs/cern.ch/user/a/attikis/scratch0/CMSSW_10_5_0_pre1/src/HLTausAnalysis/'
else
    alias hltaus 'echo Alias not set for LOCATION=$LOCATION'
endif

#############################################################################
# Setup "screen"
#############################################################################
# alias reattach "screen -r"
# if ( "$TERM" == "screen" ) then
#   if (!~ $?SHOWED_SCREEN_MESSAGE ) then
#     set detached_screens=`screen -list | grep Detached`
#     if ( "$detached_screens" != "" ) then
#       echo "+-------------------------------------+"
#       echo "| Detached screens are available:     |"
#       echo "$detached_screens"
#       echo "+-------------------------------------+"
#     else
#       echo "[ screen is activated ]"
#     endif
#     setenv SHOWED_SCREEN_MESSAGE true
#   endif
# endif


#############################################################################
# Configure environment variables
#############################################################################
echo "\n=== Setting scram architecture"
setmyscram
echo "\tSCRAM_ARCH is set to $SCRAM_ARCH"

# set SCRAM_ARCHITECTUREgcc530="slc6_amd64_gcc530"
# set SCRAM_ARCHITECTUREgcc600="slc6_amd64_gcc600"
# set SCRAM_ARCHITECTUREgcc630="slc6_amd64_gcc630"
# set SCRAM_ARCHITECTUREgcc700="slc6_amd64_gcc700"
#setenv LD_LIBRARY_PATH '/uscms/home/${USER}/.local/lib:'
#setenv LD_LIBRARY_PATH '/uscms/home/$USER/.local/lib:'$LD_LIBRARY_PATH

# setenv ROOTSYS /cvmfs/cms.cern.ch/$SCRAM_ARCHITECTURE/lcg/root/6.02.12-kpegke4 # CMSSW_7_6_5

# setenv LD_LIBRARY_PATH $ROOTSYS/lib
# setenv PATH ${PATH}:$ROOTSYS/bin

# setenv SCRAM_ARCH $SCRAM_ARCHITECTURE

# setenv STAGE_HOST castorcms


#############################################################################
# Setup Python and PyROOT (assuming root paths exist)
#############################################################################
#setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/  # CMSSW_7_6_5
# #setenv PYTHONDIR /cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/python/2.7.11-giojec2 # CMSSW_8_0_24

# #setenv PYTHONDIR /usr
# setenv PYTHONPATH $PYTHONDIR/bin
#setenv PATH $PYTHONDIR/bin:$PATH
# setenv LD_LIBRARY_PATH $PYTHONDIR/lib:$LD_LIBRARY_PATH
# setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH


#############################################################################
# Set additional PATHS
#############################################################################
setenv PATH ${PATH}:$HOME/HPlusScripts/
setenv PATH ${PATH}:$HOME/HPlusScripts/tcsh/
setenv PATH ${PATH}:$HOME/HPlusScripts/bash/
setenv PATH ${PATH}:$HOME/HPlusScripts/python/
setenv PATH ${PATH}:$HOME/HPlusScripts/login/
setenv PATH ${PATH}:$HOME/HPlusScripts/lxbatch/


#############################################################################
# Additional variables
#############################################################################
setenv EDITOR emacs
if ( "$LOCATION" == "lxplus" ) then
    setenv PRINTER 40-4b-cor
    echo "\n=== $HOME/myEnvironment.csh\n\tPRINTER=$PRINTER"
endif



#############################################################################
# Fix a compilation problem of CMSSW (Added on 28 May 2015) 
# More info: https://hypernews.cern.ch/HyperNews/CMS/get/linux/150/1/1.html
#############################################################################
setenv LANG "en_US.UTF-8"
setenv LC_CTYPE "en_US.UTF-8"
setenv LC_NUMERIC "en_US.UTF-8"
setenv LC_TIME "en_US.UTF-8"
setenv LC_COLLATE "en_US.UTF-8"
setenv LC_MONETARY "en_US.UTF-8"
setenv LC_MESSAGES "en_US.UTF-8"
setenv LC_PAPER "en_US.UTF-8"
setenv LC_NAME "en_US.UTF-8"
setenv LC_ADDRESS "en_US.UTF-8"
setenv LC_TELEPHONE "en_US.UTF-8"
setenv LC_MEASUREMENT "en_US.UTF-8"
setenv LC_IDENTIFICATION "en_US.UTF-8"
#setenv LC_ALL 


#############################################################################
# To print All locale settings uncomment the command below
#############################################################################
# echo "\nLOCALE settings:"
# locale 


#############################################################################
# Inform user
#############################################################################
echo "\tEDITOR   = $EDITOR"
echo "\tLOCATION = $LOCATION"
if ( "$LOCATION" == "lxplus" ) then
    echo "\tPRINTER  = $PRINTER"
endif 
echo "\tPUBLIC   = $PUBLIC"
echo "\tSCRATCH  = $SCRATCH"
echo "\tTMP      = $TMP"
echo "\tW0       = $W0"
echo "\tWORKSPACE= $WORKSPACE"
#echo "\tFORTRAN  = $FORTRAN"
#echo "\tROOTSYS  = $ROOTSYS"


#############################################################################
# EOF
#############################################################################
echo "\n=== $HOME/myEnvironment.csh\n\tDONE!"
echo
