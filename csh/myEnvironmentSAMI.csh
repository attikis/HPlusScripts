set autolist
setenv FORTRAN $HOME/public/fortran/src
setenv PATH "${PATH}:${HOME}/bin:."
#setenv PATH "${PATH}:${HOME}/public/git/bin"

setenv SCRATCH $HOME/scratch0
#setenv DOWNLOAD $HOME/download
setenv TMP /tmp/${USER}
setenv WORKSPACE /afs/cern.ch/work/s/slehti

#setenv CERN $HOME/Programs/cernlib
#setenv CERN_LEVEL pro

setenv DATA $HOME/public/ORCA/data

set prompt = "%m > "

 alias l             'ls -lth --color=never'
 alias ls             'ls --color=never'
 alias cd            'cd \!*;echo $cwd'
 alias pwd           'echo $cwd'
 alias del           'rm -i'
 alias type          'cat'
 alias dir           'ls -la'
 alias lo            'exit'
# alias edit          'em'
 alias edit          me404linux.bin
 alias cd..          'cd ..'
 alias pine          'alpine'
 alias ssh           'ssh -Y'
 alias scp           'scp -p'
 alias kinit         'kinit slehti@CERN.CH'

 alias root "root -l -n"
 alias vgap /data/slehti/wine-20021031/wine /data/slehti/windows/games/vgasmi/winplan.exe

 alias glogin "source $HOME/bin/grid_environment"
 alias grid "source $HOME/bin/grid_environment"

 alias scram5 "setenv SCRAM_ARCH slc5_amd64_gcc462"
 alias scram6 "setenv SCRAM_ARCH slc6_amd64_gcc530"

 alias confdb 'javaws http://confdb.web.cern.ch/confdb/v2/gui/start.jnlp'
 alias tm-editor '/afs/cern.ch/user/a/arnold/public/bin/tm-editor'

source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.csh

#setenv ROOTSYS /afs/cern.ch/sw/lcg/external/root/5.20.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.26.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00/slc4_ia32_gcc34/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.32.03/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.00/x86_64-slc5-gcc43-dbg/root
#setenv ROOTSYS /afs/cern.ch/sw/lcg/external/root/5.16.00/slc4_amd64_gcc34/root
#setenv ROOTSYS /afs/cern.ch/cms/slc5_amd64_gcc462/lcg/root/5.34.01-cms2/
setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.03.02/x86_64-slc6-gcc48-opt/root

setenv LD_LIBRARY_PATH $ROOTSYS/lib
setenv PATH "${ROOTSYS}/bin:${PATH}"

#setenv SCRAM_ARCH slc3_ia32_gcc323
#setenv SCRAM_ARCH slc5_amd64_gcc434 
#setenv SCRAM_ARCH slc5_amd64_gcc462
#setenv SCRAM_ARCH slc6_amd64_gcc481
#setenv SCRAM_ARCH slc6_amd64_gcc491
#setenv SCRAM_ARCH slc6_amd64_gcc493
#setenv SCRAM_ARCH slc6_amd64_gcc530
#setenv SCRAM_ARCH slc6_amd64_gcc600
#setenv SCRAM_ARCH slc6_amd64_gcc630
setenv SCRAM_ARCH slc6_amd64_gcc700

setenv CMSSW /afs/cern.ch/user/s/slehti/scratch0/hplusAnalysis/CMSSW_3_5_8/src/HiggsAnalysis/HeavyChHiggsToTauNu/test

#grid environment
#source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh
#source $CMS_PATH/ccs/wm/scripts/Crab/crab.csh

#setenv CRAB $SCRATCH/tmp/ORCA_8_7_1/src/HiggsAnalysis/MssmA2tau2l/test

#setenv STAGE_HOST stagecms
#setenv  STAGE_HOST  castorrh
setenv STAGE_HOST castorcms

#source /afs/cern.ch/user/k/kaitanie/public/git/gitenv.csh

setenv SKIM $HOME/scratch0/TauTriggerEfficiencyMeasurement/Skim

#PyROOT, assuming root paths exist
#setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.5.4p2/slc4_amd64_gcc34
setenv PYTHONDIR /usr
setenv PYTHONPATH $PYTHONDIR/bin
setenv PATH $PYTHONDIR/bin:$PATH
setenv LD_LIBRARY_PATH $PYTHONDIR/lib:$LD_LIBRARY_PATH
setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH


setenv CVSROOT ":ext:slehti@lxplus5.cern.ch:/afs/cern.ch/user/c/cvscmssw/public/CMSSW"

#setenv PATH ${HOME}/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:${PATH}

setenv TZ CET # for the confdb gui

setenv PATH $HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
