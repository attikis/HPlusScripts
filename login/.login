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
set uptime = `uptime`
echo "=== $HOME/.login: The current system has been running since:\n\t $uptime"
#sleep 1
echo

#############################################################################
set users = `users`
echo "=== $HOME/.login: The users currently logged on this machine are:\n\t $users"
echo

#############################################################################
#echo ".login *** Launching screen:"
#exec screen

#############################################################################
#echo "=== $HOME/.login\n\t Getting an ssh agent running in my interactive sessions:"
#if ( ! $?SSH_AUTH_SOCK ) then
#      eval `ssh-agent -c`
#      ssh-add
#   endif
#echo

#NOTE: Generate C-shell commands on stdout. This is the default if SHELL looks
#      like it's a csh style of shell.

#############################################################################
#echo "=== $HOME/.login\n\t Testing github configuration:"
#ssh -T git@github.com

#echo "=== $HOME/.login\n\t DONE!"
#echo
