#############################################################################
### File ............: myEnvironment.csh
### Description:.....: general purpose .tcshrc file
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################      
echo "\n=== myEnvironment.csh"
set USER_INITIAL=`echo $USER | cut -c1`
set SCRAM_ARCHITECTURE=slc6_amd64_gcc530

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


#############################################################################
# Set your prompt
# set prompt="$HOST "           # plus1         #
# set prompt='\! > '            # 3 >           # 3 means the third
# set prompt='\! %~ %# '        # 3 ~/public >  #
# set prompt="[$HOST] > "       # [plus1] >     #
# set prompt='R; '              # R;            # for VM hackers!
#############################################################################
# set prompt = "%m > "
set prompt = '[%n@%m:%c]%#'

#############################################################################
# Set aliases
#############################################################################
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
#alias root          'root -l'
alias glogin        'source $HOME/bin/grid_environment'
alias grid          'source $HOME/bin/grid_environment'
alias scram5        'setenv SCRAM_ARCH slc5_amd64_gcc462'
#alias scram6        'setenv SCRAM_ARCH slc6_amd64_gcc481'
alias scram6        'setenv SCRAM_ARCH $SCRAM_ARCHITECTURE' #19 July 2016

#############################################################################
# Setup "screen"
#############################################################################
alias reattach "screen -r"
if ( "$TERM" == "screen" ) then
  if (!~ $?SHOWED_SCREEN_MESSAGE ) then
    set detached_screens=`screen -list | grep Detached`
    if ( "$detached_screens" != "" ) then
      echo "+-------------------------------------+"
      echo "| Detached screens are available:     |"
      echo "$detached_screens"
      echo "+-------------------------------------+"
    else
      echo "[ screen is activated ]"
    endif
    setenv SHOWED_SCREEN_MESSAGE true
  endif
endif


#############################################################################
### Configure environment variables
#############################################################################
# setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.00/x86_64-slc5-gcc43-dbg/root  # slehti (~Summer 2016)
# setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.00/x86_64-slc6-gcc48-opt/root/ # does not exist!
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.00/x86_64-slc6-gcc46-opt/root/  # HiggsAnalysis works also on LPC
setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc493/lcg/root/6.02.12-kpegke4 # 20 Sep 2016

setenv LD_LIBRARY_PATH $ROOTSYS/lib
setenv PATH ${PATH}:$ROOTSYS/bin

#setenv SCRAM_ARCH slc6_amd64_gcc491 #slehti
setenv SCRAM_ARCH $SCRAM_ARCHITECTURE #19 July 2016

setenv STAGE_HOST castorcms

#############################################################################
# Setup Python and PyROOT (assuming root paths exist)
#############################################################################
#setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.5.4p2/slc4_amd64_gcc34
setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/
#setenv PYTHONDIR /cvmfs/cms.cern.ch/$SCRAM_ARCH/external/2.7.6-kpegke/ #doesn't work
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
setenv PRINTER 40-4b-cor


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

# To print All locale settings uncomment the command below
# echo "\nLOCALE settings:"
# locale 


#############################################################################
# Inform user
#############################################################################
echo "FORTRAN=$FORTRAN"
echo "SCRATCH=$SCRATCH"
echo "W0=$W0"
echo "PUBLIC=$PUBLIC"
echo "TMP=$TMP"
echo "WORKSPACE=$WORKSPACE"
echo "EDITOR=$EDITOR"
echo "PRINTER=$PRINTER"
echo "ROOTSYS=$ROOTSYS"
echo
