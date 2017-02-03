#############################################################################
### File ............: $HOME/.login
### Description:.....: general purpose .login file where one defines commands
###                    to be executed only once per login:
###                    terminal setting (tset)
###                    mailbox checking (checkmail)
###                    status checks and messages (echo, uptime, date etc)
### Author: .........: Alexandros Attikis
### Email ...........: attikis@cern.ch
### Comments ........: http://info.eps.surrey.ac.uk/FAQ/loginfiles.html
#############################################################################
echo "\n=== $HOME/.login"
set uptime=`uptime`
echo "\tThe current system has been running since: $uptime"
#sleep 1
echo

#############################################################################
# echo "Launching screen:"
# exec screen

#############################################################################
# Detect LXPLUS or MAC OS X (Darwin) or LPC @ FNAL
set LOCATION=""
if ( $LOCATION == "" ) then
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "Mac"* ) then
        set LOCATION="mac"
     else if (`hostname` =~ *".cern.ch" ) then #Example: p06109780e53561.cern.ch
	set LOCATION="lxbatch"
     else if (`hostname` =~ *".fnal.gov" ) then #Example: cmslpc35.fnal.gov
	set LOCATION="lpc"
    endif
endif
echo "=== $HOME/.login\n\tLOCATION=$LOCATION"
echo

#############################################################################
set users=`users`
echo "=== $HOME/.login\n\tThe users currently logged on this machine are: $users"
echo


#############################################################################
set envScript=myEnvironment.csh
echo "=== $HOME/.login\n\tSourcing custom environment script $envScript"
source $envScript

# http://www.uscms.org/uscms_at_work/computing/setup/setup_software.shtml
if ( $LOCATION == "lpc" ) then
    echo "=== $HOME/.login\n\tSetting the CMS software environment using an environment setup script (csh/tcsh)"
    source /cvmfs/cms.cern.ch/cmsset_default.csh    
endif
echo

#############################################################################
#echo "Getting an ssh agent running in my interactive sessions:"
#if ( ! $?SSH_AUTH_SOCK ) then
#      eval `ssh-agent -c`
#      ssh-add
#   endif
#echo

#############################################################################
#echo "=== $HOME/.login\n\tTesting github configuration:"
#ssh -T git@github.com

#############################################################################
echo "=== $HOME/.login\n\t DONE!"
#echo
