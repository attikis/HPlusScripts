#!/usr/bin/env python

# Script docstrings
'''
Permissions: 
chmod +x checkoutSvnNote.py

Install python package:
sudo easy_install package_name

Description:
Checkout a CMS Note from SVN.

Usage: 
checkoutSvnNote.py [options]

Options:
  -h, --help            show this help message and exit
  -n ID OF SV NOTE TO CHECKOUT, --noteid=ID OF SV NOTE TO CHECKOUT
                        ID OF SV NOTE TO CHECKOUT
  -d DIR NAME TO CHECKOUT NOTE, --dirname=DIR NAME TO CHECKOUT NOTE
                        DIR NAME TO CHECKOUT NOTE
  -s TYPE OF SHELL USED, --shell=TYPE OF SHELL USED
                        TYPE OF SHELL USED
'''

# Modules here
import subprocess
import os
import sys
from optparse import OptionParser 

# Declarations here
parser = OptionParser()

parser.add_option("-n", "--noteid", default = "DN-14-002", dest = "noteid", help = "ID OF SV NOTE TO CHECKOUT", metavar = "ID OF SV NOTE TO CHECKOUT")
parser.add_option("-d", "--dirname", default = "TTI_Note", dest = "dirname", help = "DIR NAME TO CHECKOUT NOTE", metavar = "DIR NAME TO CHECKOUT NOTE")
parser.add_option("-s", "--shell", default = "csh", dest = "shell", help = "TYPE OF SHELL USED", metavar = "TYPE OF SHELL USED")
(options, args) = parser.parse_args()

# Check that mandatory options are declared/provided
if not (options.noteid and options.dirname):
    print __doc__
    parser.error("NOTEID and DIRNAME are mandatory")

# Main function
if __name__ == "__main__":

    # Check whether path exists or not
    if os.path.exists(options.dirname):
        print "---> ERROR! Directory \'%s\' already exists. System exit." % (options.dirname)
        sys.exit()
        
    # Algorithm to be followed for getting note repository
    cmds = ["svn co -N svn+ssh://svn.cern.ch/reps/tdr2 " + options.dirname, 
            "cd " + os.getcwd() + "/" + options.dirname + "/", 
            "svn update utils ", 
            'svn update -N notes',
            "svn update notes/" + options.noteid, 
            "cd " + os.getcwd() + "/" + options.dirname + "/",
            "eval `notes/tdr runtime -%s`" % (options.shell),
            "cd " + os.getcwd() + "/" + options.dirname + "/notes/" + options.noteid + "/trunk", 
            "tdr --draft --style=an b " + options.noteid]

#svn co -N svn+ssh://svn.cern.ch/reps/tdr2 TTI_Note
#cd TTI_Note
#svn update utils
#svn update -N notes
#svn update notes/DN-14-002
#eval `notes/tdr runtime -csh` # for tcsh. use -sh for bash.
#cd notes/DN-14-002/trunk
#and then after editing it, compile the document by doing:
#tdr --draft --style=an b DN-14-002
    
    # Loop over shell commands to be executed
    for cmd in cmds:
        print "---> %s" % (cmd)
        if(cmd.startswith("cd ")):
            dirname = cmd.replace("cd ", "") #+ os.getcwd()
            if os.path.exists(dirname):
                os.chdir( dirname )
            else:
                print "---> ERROR! Directory \'%s\' does not exist. System exit." % (dirname)
                sys.exit()
        else:
            subprocess.call(cmd, shell=True)
        print
