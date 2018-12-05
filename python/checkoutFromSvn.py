#!/usr/bin/env python
'''
PREREQUISITES:
chmod +x checkoutSvnNote.py


INSTALLING PYTHON PACKAGES:
sudo easy_install <package_name>


DESCRIPTION:
Checkout a CMS Note from SVN.


USAGE: 
checkoutSvnNote.py [options]


EXAMPLES:
./checkoutFromSvn.py -n HIG-18-014 --noteType papers
./checkoutFromSvn.py -n HIG-18-015 --noteType papers
./checkoutFromSvn.py -n DN-14-002 --noteType notes


LAST USED:
./checkoutFromSvn.py -n HIG-18-015 --noteType papers


LINKS:
https://twiki.cern.ch/twiki/bin/view/Main/HowtoNotesInCMS


OPTIONS:
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

parser.add_option("-n", "--noteid"  , default = "HIG-18-015", dest = "noteid"  , help = "ID OF SV NOTE TO CHECKOUT", metavar = "ID OF SV NOTE TO CHECKOUT")
parser.add_option("-t", "--noteType", default = "papers"    , dest = "noteType", help = "papers, notes, .."        , metavar = "papers, notes, ..")
parser.add_option("-d", "--dirname" , default = "FromSvns" , dest = "dirname" , help = "DIR NAME TO CHECKOUT NOTE", metavar = "DIR NAME TO CHECKOUT NOTE")
parser.add_option("-s", "--shell"   , default = "csh"       , dest = "shell"   , help = "TYPE OF SHELL USED"       , metavar = "TYPE OF SHELL USED")
parser.add_option("--tdr"  , default = "tdr2", dest = "tdr"   , help = "TDR VERSION", metavar = "TDR VERSION")
parser.add_option("--style", default = "an"  , dest = "style" , help = "STYLE"      , metavar = "NOTE STYLE")

(options, args) = parser.parse_args()

# Check that mandatory options are declared/provided
if not (options.noteid):
    print __doc__
    parser.error("NOTEID and DIRNAME are mandatory")


allowedTypes = ["papers", "notes"]
if options.noteType not in allowedTypes:
    print "=== checkoutFromSvn.py\n\tInvalid note type \"%s\". Please select one of the following: " % (options.noteType, ", ".join(allowedTypes))
    print __doc__
    parser.error("NOTEID and DIRNAME are mandatory")

# Main function
if __name__ == "__main__":

    # Changed directory
    if os.path.exists(options.dirname):
        os.chdir(options.dirname)
        
    # Check whether path exists or not
    if os.path.exists(options.noteid):
        print "=== checkoutFromSvn.py\n\tDirectory \'%s\' already exists!" % (options.noteid)
        sys.exit()

    # Algorithm to be followed for getting note repository
    cmds1 = ["svn co -N svn+ssh://svn.cern.ch/reps/" + options.tdr + " " + options.noteid, 
            "cd " + os.getcwd() + "/" + options.noteid + "/", 
            "svn update utils ", 
            'svn update -N %s' % options.noteType,
            "svn update " +  os.path.join(options.noteType, options.noteid)]

    cmds2 = [
        "cd " + os.path.join(os.getcwd(), options.noteid),
        "eval `%s/tdr runtime -%s`" % (options.noteType, options.shell),
        "cd %s" % (os.path.join(os.getcwd(), options.noteid, options.noteType,  options.noteid, "trunk") ), 
        "tdr --draft --style=%s b %s" % (options.style, options.noteid),
        "open %s" % (os.path.join(os.getcwd(), options.noteid, options.noteType, "tmp", options.noteid + "_temp.pdf") )]
        
    # For-loop: All shell commands to be executed
    for i, cmd in enumerate(cmds1, 1):
        if i!=1:
            print "=== checkoutFromSvn.py"
        print "\t", cmd
        
        if(cmd.startswith("cd ")):
            dirname = cmd.replace("cd ", "") #+ os.getcwd()
            if os.path.exists(dirname):
                os.chdir( dirname )
            else:
                print "=== checkoutFromSvn.py\n\tDirectory \'%s\' does not exist. System exit." % (dirname)
                sys.exit()
        else:
            subprocess.call(cmd, shell=True)        
    
    # For-loop: All shell commands to be executed
    print "\n=== checkoutFromSvn.py (Please copy-paste the following commands):"
    for i, cmd in enumerate(cmds2, 1):
        #print "\t", cmd
        print cmd
    print
    
