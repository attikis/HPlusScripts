#!/usr/bin/env python
'''
DESCRIPTION:
Submits all gridpacks under a given directorty to LXBATCH


USAGE:
submit2lxbatch.py [options]


EXAMPLE:
cd /afs/cern.ch/user/a/attikis/workspace/MCProduction2017/genproductions/bin/MadGraph5_aMCatNLO
./submit2lxbatch.py -d cards/production/2017/13TeV/ChargedHiggs_TB
./submit2lxbatch.py -d cards/production/2017/13TeV/ChargedHiggs_TB --queue 2nw --queueMaster 2nw -i "M300"

LAST USED:
 ./submit2lxbatch.py -d cards/production/2017/13TeV/ChargedHiggs_TB --queue 2nw --queueMaster 2nw 


USEFUL LINKS:
https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs
https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO
'''

#================================================================================================ 
# Modules here
#================================================================================================ 
import subprocess
from subprocess import Popen, PIPE
import os
import sys
import re
import datetime
import time
import getpass 
from optparse import OptionParser 

#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return
    if printHeader:
        print "=== submit2lxbatch.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    return __file__.replace("./", "")

def Print(msg, printHeader=True):
    fName = GetFName() #"submit2lxbatch.py"
    if printHeader:
        print "=== ", fName
    if msg !="":
        print "\t", msg
    return

def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg
    if printHeader:
        print "=== ", GetFName()
    sys.stdout.write(msg)
    sys.stdout.flush()
    return     

def AskUser(msg, printHeader=False):
    '''
    Prompts user for keyboard feedback to a certain question.
    Returns true if keystroke is \"y\", false otherwise.
    '''
    if printHeader:
                keystroke = raw_input("=== " + GetFName() + "\n\t" +  msg + " (y/n): ")
    else:
        keystroke = raw_input("\t" +  msg + " (y/n): ")

    if (keystroke.lower()) == "y":
        return True
    elif (keystroke.lower()) == "n":
        return False
    else:
        AskUser(msg)

def includeExcludeTasks(tasks, **kwargs):
    '''
    Helper function to choose tasks with includeOnlyTasks/excludeTasks
    
    \param tasks  List of strings for task names
    \param kwargs Keyword arguments (see below)
    
    <b>Keyword arguments</b>
    \li \a excludeTasks      String, or list of strings, to specify regexps.
    If a dataset name matches to any of the
    regexps, Dataset object is not constructed for
    that. Conflicts with \a includeOnlyTasks

    \li \a includeOnlyTasks  String, or list of strings, to specify
    regexps. Only datasets whose name matches
    to any of the regexps are kept. Conflicts
    with \a excludeTasks.

    \return List of selected tasks (all tasks if neither excludeTasks or includeOnlyTasks is given)
    '''
    if "excludeTasks" in kwargs and "includeOnlyTasks" in kwargs:
        raise Exception("Only one of 'excludeTasks' or 'includeOnlyTasks' is allowed")

    def getRe(arg):
        if isinstance(arg, basestring):
            arg = [arg]
        return [re.compile(a) for a in arg]

    if "excludeTasks" in kwargs:
        exclude = getRe(kwargs["excludeTasks"])
        tmp = []
        for task in tasks:
            found = False
            for e_re in exclude:
                if e_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                continue
            tmp.append(task)
        return tmp

    if "includeOnlyTasks" in kwargs:
        include = getRe(kwargs["includeOnlyTasks"])
        tmp = []
        for task in tasks:
            found = False
            for i_re in include:
                if i_re.search(os.path.basename(task)):
                    found = True
                    break
            if found:
                tmp.append(task)
        return tmp
    return tasks


def main(cardName, cardDir, sopts):
    
    # Calling subprocess.Popen() works but truncates output
    submitScript   = "submit_gridpack_generation.sh"
    memoryInMBytes = opts.memMB
    diskInMBytes   = opts.diskMB
    queueMaster    = opts.queueMaster
    queue          = opts.queue
    cmdList        = [submitScript, memoryInMBytes, diskInMBytes, queueMaster, cardName, cardDir, queue]
    cmd            = "./" + " ".join(cmdList)
    Verbose(cmd, False)
    process        = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        # raise Exception(err)
        Print(err, True)
    return


if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default settings
    VERBOSE     = False
    DIRNAME     = None
    USERNAME    = None
    QUEUEMASTER = "2nw"
    QUEUE       = "2nw"
    MEMMB       = "30000" # 30000MB when generating NLO (or LO with madspin)
    DISKMB      = "30000" # 30000MB when generating NLO (or LO with madspin)

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-d", "--dirName", dest="dirName", action="store", default = DIRNAME,
                      help="Name of directory to be checked for status [default: %s]" % (DIRNAME) )

    parser.add_option("-u", "--userName", dest="userName", action="store", default = USERNAME,
                      help="User name to be used for commands [default: %s]" % (USERNAME) )

    parser.add_option("--queue", dest="queue", action="store", default = QUEUE,
                      help="Queue for job in LXBATCH [default: %s]" % (QUEUE) )

    parser.add_option("--queueMaster", dest="queueMaster", action="store", default = QUEUEMASTER,
                      help="Queue for master job in LXBATCH [default: %s]" % (QUEUEMASTER) )

    parser.add_option("--diskMB", dest="diskMB", action="store", default = DISKMB,
                      help="Disk size to request in MB [default: %s]" % (MEMMB) )

    parser.add_option("--memMB", dest="memMB", action="store", default = MEMMB,
                      help="Memory size to request in MB [default: %s]" % (MEMMB) )

    parser.add_option("-i", "--includeOnlyTasks", dest="includeOnlyTasks", action="store",
                      help="List of cards to include, regex based")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks", action="store",
                      help="List of cards to exclude, regex based")

    (opts, parseArgs) = parser.parse_args()

    if opts.dirName == None:
        Print("Please provide a directory as argument (-d or --dirName option). EXIT!", True)
        sys.exit()

    if not os.path.isdir(opts.dirName):
        Print("The directory %s does not exist. EXIT!" % (opts.dirName), True)
        sys.exit()

    if opts.userName == None:
        opts.userName = getpass.getuser()

    # Inform user of compatibility issues
    cont = os.listdir(opts.dirName)
    dirs = []
    # For-loop: Dir contents
    for i, c in enumerate(cont, 1):
        fullPath = os.path.join(opts.dirName, c)#.replace(" ","")
        if os.path.isfile(fullPath):
            # Verbose("fullPath = %s" % fullPath, False)
            continue
        else:
            # Ignore the template directory (ugly hack)
            if "M" not in c.split("_")[-1]:
                Verbose("Ignoring template directory \"%s\"" % (fullPath), i==1)
                continue
            Verbose("Appending directory \"%s\"" % (fullPath), i==1)
            dirs.append(fullPath)


    # Select specific tasks
    myDirs = []
    kwargs = {}
    if opts.includeOnlyTasks != None:
        kwargs["includeOnlyTasks"] = opts.includeOnlyTasks
    if opts.excludeTasks != None:
        kwargs["excludeTasks"] = opts.excludeTasks
    if len(kwargs.keys()) > 0:
        myDirs = includeExcludeTasks(dirs, **kwargs)

    if len(myDirs)>0:
        dirs = myDirs

    Print("Sumbitting LXBATCH jobs for the following tasks:", printHeader=True)
    for i, d in enumerate(dirs, 1):
        Print(os.path.basename(d), False)
        
    if not AskUser("Proceed with submission?", printHeader=True):
        Print("Aborting!", True)
        sys.exit()

    # For-loop: All directories to be submitted
    for i, d in enumerate(dirs, 1):
        Verbose("%d) %s" % (i, d), i==1)
        cardName = os.path.basename(d)
        cardDir = d
        PrintFlushed("Submitting %d/%d (%s)" % (i, len(dirs), os.path.basename(d)), i==1)
        main(cardName, cardDir, opts)
        time.sleep(0.2)
    print

    # Check the status of your jobs (if any submitted)
    Print("", True)
    os.system("bjobs")

