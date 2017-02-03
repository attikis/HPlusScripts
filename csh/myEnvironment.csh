#############################################################################
### File ............: myEnvironment.csh
### Description:.....: general purpose .tcshrc file
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################      
echo "\n=== myEnvironment.csh"
set USER_INITIAL=`echo $USER | cut -c1`
set SCRAM_ARCHITECTURE=slc6_amd64_gcc493 #CMSSW_7_6_5
# set SCRAM_ARCHITECTURE=slc6_amd64_gcc530 #CMSSW_8_0_24


############################################################################# 
# Enable tab completion to show a menu of options (tcsh)
############################################################################# 
set autolist


#############################################################################      
# Set PATHS & Environment variables
#############################################################################      
setenv FORTRAN $HOME/public/fortran/src
setenv PATH "${PATH}:${HOME}/bin:."

setenv SCRATCH $HOME/scratch0
setenv W0 $HOME/w0
setenv PUBLIC $HOME/public
setenv TMP /tmp/${USER}
setenv WORKSPACE /afs/cern.ch/work/$USER_INITIAL/$USER
setenv EOS /store/user/$USER/CRAB3_TransferData


#############################################################################
# Set your prompt
#############################################################################
set prompt = '[%n@%m:%c]%#'
# set prompt="$HOST "           # plus1         #
# set prompt='\! > '            # 3 >           # 3 means the third
# set prompt='\! %~ %# '        # 3 ~/public >  #
# set prompt="[$HOST] > "       # [plus1] >     #
# set prompt='R; '              # R;            # for VM hackers!


#############################################################################
# Set aliases
#############################################################################
alias lxplus        'ssh -N -L 10121:itrac50012-v.cern.ch:10121 attikis@lxplus.cern.ch'
alias l             'ls -lth'
alias cd            'cd \!*;echo $cwd'
alias pwd           'echo $cwd'
alias del           'rm -i'
alias type          'cat'
alias dir           'ls -la'
alias lo            'exit'
alias emacs         'emacs -nw'
alias H             'history -r | fgrep "\!*"'         # just type H latex to get the 
alias h             'history'                          # just type h for the history
alias rm            'rm -i'                            # ask confirmation before deleting
alias ls            'ls -pt --color=auto'              # enable automatic list-highlight
alias lsd           'ls -lpt --color=force | grep ^d'  # list only the directories 
alias ssh           'ssh -Y'
alias root          'root -l'
alias glogin        'source $HOME/bin/grid_environment'
alias grid          'source $HOME/bin/grid_environment'
alias scram6        'setenv SCRAM_ARCH $SCRAM_ARCHITECTURE'
alias cmssw         'source ~/HPlusScripts/csh/setenv_cmssw.csh ~/scratch0/ 8_0_24 false'
alias cmssw-crab    'source ~/HPlusScripts/csh/setenv_cmssw.csh ~/scratch0/ 8_0_24 true'
alias hltaus        'source HPlusScripts/csh/hltaus.csh'
alias cmsenvUnset   'eval `scram unsetenv -sh`'
alias higgs         'source ~/HPlusScripts/csh/setenv_higgs.csh ~/scratch0/ 8_0_24'
alias d3            'cd /uscms_data/d3/aattikis/workspace/'
alias setbrilcalc   'setenv PATH ${PATH}:$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:'


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
setenv ROOTSYS /cvmfs/cms.cern.ch/$SCRAM_ARCHITECTURE/lcg/root/6.02.12-kpegke4 # CMSSW_7_6_5

setenv LD_LIBRARY_PATH $ROOTSYS/lib
setenv PATH ${PATH}:$ROOTSYS/bin

setenv SCRAM_ARCH $SCRAM_ARCHITECTURE

setenv STAGE_HOST castorcms


#############################################################################
# Setup Python and PyROOT (assuming root paths exist)
#############################################################################
setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/  # CMSSW_7_6_5
#setenv PYTHONDIR /cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/python/2.7.11-giojec2 # CMSSW_8_0_24

#setenv PYTHONDIR /usr
setenv PYTHONPATH $PYTHONDIR/bin
setenv PATH $PYTHONDIR/bin:$PATH
setenv LD_LIBRARY_PATH $PYTHONDIR/lib:$LD_LIBRARY_PATH
setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH


#############################################################################
# Additional PATHS
#############################################################################
setenv PATH $PATH\:$HOME/HPlusScripts/
setenv PATH $PATH\:$HOME/HPlusScripts/tcsh/
setenv PATH $PATH\:$HOME/HPlusScripts/bash/
setenv PATH $PATH\:$HOME/HPlusScripts/python/
setenv PATH $PATH\:$HOME/HPlusScripts/login/
setenv PATH $PATH\:$HOME/HPlusScripts/lxbatch/


#############################################################################
# Additional variables
#############################################################################
setenv EDITOR emacs
# setenv PRINTER 40-4b-cor


#############################################################################
# Fix a compilation problem of CMSSW (Added on 28 May 2015) 
# More info: https://hypernews.cern.ch/HyperNews/CMS/get/linux/150/1/1.html
#############################################################################
# setenv LANG "en_US.UTF-8"
# setenv LC_CTYPE "en_US.UTF-8"
# setenv LC_NUMERIC "en_US.UTF-8"
# setenv LC_TIME "en_US.UTF-8"
# setenv LC_COLLATE "en_US.UTF-8"
# setenv LC_MONETARY "en_US.UTF-8"
# setenv LC_MESSAGES "en_US.UTF-8"
# setenv LC_PAPER "en_US.UTF-8"
# setenv LC_NAME "en_US.UTF-8"
# setenv LC_ADDRESS "en_US.UTF-8"
# setenv LC_TELEPHONE "en_US.UTF-8"
# setenv LC_MEASUREMENT "en_US.UTF-8"
# setenv LC_IDENTIFICATION "en_US.UTF-8"
# #setenv LC_ALL 

# To print All locale settings uncomment the command below
# echo "\nLOCALE settings:"
# locale 


#############################################################################
# Inform user
#############################################################################
echo "\tFORTRAN  = $FORTRAN"
echo "\tSCRATCH  = $SCRATCH"
echo "\tW0       = $W0"
echo "\tPUBLIC   = $PUBLIC"
echo "\tTMP      = $TMP"
echo "\tWORKSPACE= $WORKSPACE"
echo "\tEDITOR   = $EDITOR"
# echo "PRINTER=$PRINTER"
# echo "ROOTSYS=$ROOTSYS"
echo
