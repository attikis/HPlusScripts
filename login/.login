#############################################################################
### File ............: $HOME/.login
### Description:.....: includes commands to be executed only once per login:
###                    terminal setting (tset)
###                    mailbox checking (checkmail)
###                    status checks and messages (echo, uptime, date etc)
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################
set uptime=`uptime`
echo "\n=== $HOME/.login\n\t$uptime"
sleep 1
echo

#############################################################################
# Detect LXPLUS or MAC OS X (Darwin) or LPC @ FNAL
#############################################################################
set LOCATION=""
if ( $LOCATION == "" ) then
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
echo "=== $HOME/.login\n\tLOCATION=$LOCATION"
echo


#############################################################################
# Detect users on this machine
#############################################################################
set users=`users`
echo "=== $HOME/.login\n\t$users"
echo


#############################################################################
# Setup the General CMS Software Environment
# http://www.uscms.org/uscms_at_work/computing/setup/setup_software.shtml
#############################################################################
set cmsswScript=/cvmfs/cms.cern.ch/cmsset_default.csh
if ( $LOCATION == "lpc" ) then
    echo "=== $HOME/.login\n\tSourcing $cmsswScript"
    source $cmsswScript
endif
echo

#############################################################################
set envScript=myEnvironment.csh
echo "=== $HOME/.login\n\tSourcing $envScript"
source $envScript


#############################################################################
# SSH agent setup
#############################################################################
#echo "Getting an ssh agent running in my interactive sessions:"
#echo "Getting an ssh agent running in my interactive sessions:"
#if ( ! $?SSH_AUTH_SOCK ) then
#      eval `ssh-agent -c`
#      ssh-add
#   endif
#echo


#############################################################################
# EOF
#############################################################################
echo "=== $HOME/.login\n\tDONE!"

