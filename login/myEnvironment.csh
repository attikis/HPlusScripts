#############################################################################
### File ............: myEnvironment.csh
### Description:.....: general purpose .tcshrc file
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################      
echo "\n=== myEnvironment.csh"
set INITIAL=`echo $USER | cut -c1`

set autolist

#############################################################################
### How can you change your prompt:
#############################################################################
### Definition                  # Result        # Comment
# set prompt="$HOST "           # plus1         #
# set prompt='\! > '            # 3 >           # 3 means the third
# set prompt='\! %~ %# '        # 3 ~/public >  #
# set prompt="[$HOST] > "       # [plus1] >     #
# set prompt='R; '              # R;            # for VM hackers!
set prompt = '[%n@%m:%c]%#'
#set prompt = "%m > "

#############################################################################
### Set my aliases
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
alias root          'root -l'
alias glogin        'source $HOME/bin/grid_environment'
alias grid          'source $HOME/bin/grid_environment'
alias scram5        'setenv SCRAM_ARCH slc5_amd64_gcc462'
alias scram6        'setenv SCRAM_ARCH slc6_amd64_gcc481'
# alias edit        'em'
# alias edit        me404linux.bin
### SCREEN-START: Execute screen program at login and define setup
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
### SCREEN-END


#############################################################################
### Source  my scripts
#############################################################################
source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.csh


#############################################################################
### Add or change environment variables
#############################################################################
setenv PATH "${PATH}:${HOME}/bin:."

### Additional PATHS
setenv PATH $PATH\:$HOME/HPlusScripts/
setenv PATH $PATH\:$HOME/HPlusScripts/tcsh/
setenv PATH $PATH\:$HOME/HPlusScripts/bash/
setenv PATH $PATH\:$HOME/HPlusScripts/python/
setenv PATH $PATH\:$HOME/HPlusScripts/login/
setenv PATH $PATH\:$HOME/HPlusScripts/lxbatch/

setenv FORTRAN $HOME/public/fortran/src
echo "FORTRAN=$FORTRAN"

setenv SCRATCH $HOME/scratch0
echo "SCRATCH=$SCRATCH"

setenv W0 $HOME/w0
echo "W0=$W0"

setenv PUBLIC $HOME/public
echo "PUBLIC=$PUBLIC"


setenv TMP /tmp/${USER}
echo "TMP=$TMP"

setenv WORKSPACE /afs/cern.ch/work/$INITIAL/$USER
echo "WORKSPACE=$WORKSPACE"

setenv EDITOR emacs
echo "EDITOR=$EDITOR"

setenv PRINTER 40-4b-cor
echo "PRINTER=$PRINTER"

### ROOT
#setenv ROOTSYS /afs/cern.ch/sw/lcg/external/root/5.20.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.26.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00/slc4_ia32_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.32.03/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.00/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/external/root/5.16.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/cms/slc5_amd64_gcc462/lcg/root/5.34.01-cms2/
setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.03.02/x86_64-slc6-gcc48-opt/root
echo "ROOTSYS=$ROOTSYS"

### pyROOT (assuming root paths exist)
#setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.5.4p2/slc4_amd64_gcc34
setenv PYTHONDIR /usr
setenv PYTHONPATH $PYTHONDIR/bin
setenv PATH $PYTHONDIR/bin:$PATH
setenv LD_LIBRARY_PATH $PYTHONDIR/lib:$LD_LIBRARY_PATH
setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH

setenv LD_LIBRARY_PATH $ROOTSYS/lib
setenv PATH "${ROOTSYS}/bin:${PATH}"


### Setup SCRAM Architecture (cmsenv overwrites this)
#setenv SCRAM_ARCH slc3_ia32_gcc323
#setenv SCRAM_ARCH slc5_amd64_gcc434 
#setenv SCRAM_ARCH slc5_amd64_gcc462
#setenv SCRAM_ARCH slc6_amd64_gcc481
#setenv SCRAM_ARCH slc6_amd64_gcc491
#setenv SCRAM_ARCH slc6_amd64_gcc493
setenv SCRAM_ARCH slc6_amd64_gcc530
echo "SCRAM_ARCH=$SCRAM_ARCH"

#setenv CMSSW /afs/cern.ch/user/$INITIAL/$USER/scratch0/CMSSW_7_5_2/src/UCYHiggsAnalysis
#setenv CVSROOT ":ext:slehti@lxplus5.cern.ch:/afs/cern.ch/user/c/cvscmssw/public/CMSSW"


### To fix a compilation problem of CMSSW (Added on 28 May 2015): https://hypernews.cern.ch/HyperNews/CMS/get/linux/150/1/1.html
#setenv LANGUAGE "C"
#setenv LC_ALL "C"
echo "\nLOCALE settings:"
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
locale 

echo
