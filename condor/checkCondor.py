#!/usr/bin/env python
'''
DESCRIPTION:
Check status of multible CONDOR jobs under 
a given sub-directory


USAGE:
./checkCondor.py [options]


EXAMPLE:
./checkCondor.py -d TopMassLE400_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_22Jul2018


LAST USED:
./checkCondor.py -d TopMassLE400_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_22Jul2018


USEFUL LINKS:
https://uscms.org/uscms_at_work/computing/setup/batch_systems.shtml#condor_6

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
import getpass 
from optparse import OptionParser 

import ShellStyles as ShellStyles

#================================================================================================ 
# Variable definition
#================================================================================================ 
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
es = ShellStyles.ErrorStyle()

#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    if not VERBOSE:
        return
    if printHeader:
        print "=== checkCondor.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    fName = __file__.split("/")[-1]
    fName = fName.replace(".pyc", ".py")
    return fName

def Print(msg, printHeader=True):
    fName = GetFName()
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


def GetNumberOfJobsWithKeyword(dirName, fileName="output_FakeBMeasurement_Group*.txt", keyword="Results are in"):
    cmd = "cat %s/%s | grep -c '%s' " % (dirName, fileName, keyword)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
    else:
        nJobs = int(output.replace(" ", ""))
    return nJobs


def GetNumberOfJobs(dirName, fileName="run*.jdl"):
    cmd     = "ls %s | wc -w" % ( os.path.join(os.getcwd(), dirName, fileName) )
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
    else:
        nJobs = int(output.replace(" ", ""))
    return nJobs


def GetJobStatusDict(username, keyword="Total for query: "):
    '''
    When executing:
    condor_q --submitter aattikis

    expect to see a line as follows:
    Total for query: 3 jobs; 0 completed, 0 removed, 0 idle, 3 running, 0 held, 0 suspended 

    this is the starting point forthis method
    '''
    
    # Define variables
    infoDict  = {}

    # Executed command
    cmd     = "condor_q --submitter %s" % username
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)

    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
    else:
        for l in output.splitlines():
            if keyword in l:
                infoList  = [int(s) for s in l.split() if s.isdigit()]
                # Fill the dictionary
                infoDict["jobs"]      = infoList[0]
                infoDict["completed"] = infoList[1]
                infoDict["removed"]   = infoList[2]
                infoDict["idle"]      = infoList[3]
                infoDict["running"]   = infoList[4]
                infoDict["held"]      = infoList[5]
                infoDict["suspended"] = infoList[6]
                break
        else:
            Print("Found zero jobs", True)

    if len(infoDict.keys()) < 1:
        raise Exception("Something went wrong and could not determing the jobs running, idle, held, etc..")
    return infoDict


def main(opts):
    
    
    Verbose("Check that a CMS VO proxy exists (voms-proxy-init)", True)
    process = Popen(['voms-proxy-info', '--all'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    if len(err) > 0:
        #raise Exception(es + err + ns)
        err  = err.replace("\n", "")
        err += " Continuing anyway (not needed)" 
        Print(es + err + ns, True)
    else:
        Verbose("Valid CMS VO proxy found!", True)
        

    Verbose("Check that directory %s exists" % (opts.dirName), True)
    if os.path.isdir(opts.dirName):
        Verbose("Directory %s exists!" % (ss + opts.dirName + ns), True)
    else:
        Print("Directory %s does not exist! EXIT" % (es + opts.dirName + ns), True)
        os.mkdir(opts.dirName)
        sys.exit()


    Verbose("Determine total number of jobs (using jdl files)", True)
    nRunH2tb  = GetNumberOfJobs(opts.dirName, "run_Hplus2tbAnalysis*.jdl")
    nRunFakeB = GetNumberOfJobs(opts.dirName, "run_FakeBMeasurement*.jdl")
    nRunTotal = GetNumberOfJobs(opts.dirName, "run*.jdl")
    Verbose("Found %s%d%s run files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nRunTotal, ns, nRunH2tb, nRunFakeB), True) 


    Verbose("Determine total number of jobs (using output files)")
    nOutputH2tb  = GetNumberOfJobs(opts.dirName, "output_Hplus2tbAnalysis*.txt")
    nOutputFakeB = GetNumberOfJobs(opts.dirName, "output_FakeBMeasurement*.txt")
    nOutputTotal = nOutputH2tb + nOutputFakeB
    Verbose("Found %s%d%s output files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nOutputTotal, ns, nOutputH2tb, nOutputFakeB), False) 


    Verbose("Determine total number of jobs (using error files)")
    nErrorH2tb  = GetNumberOfJobs(opts.dirName, "error_Hplus2tbAnalysis*.txt")
    nErrorFakeB = GetNumberOfJobs(opts.dirName, "error_FakeBMeasurement*.txt")
    nErrorTotal = nOutputH2tb + nOutputFakeB
    Verbose("Found %s%d%s error files (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nErrorTotal, ns, nErrorH2tb, nErrorFakeB), False) 


    Verbose("Determine total number of done jobs (using error files)")
    nDoneH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "output_Hplus2tbAnalysis*.txt", "Results are in")
    nDoneFakeB = GetNumberOfJobsWithKeyword(opts.dirName, "output_FakeBMeasurement*.txt", "Results are in")
    nDoneTotal = nDoneH2tb + nDoneFakeB
    Verbose("Found %s%d%s jobs done (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nDoneTotal, ns, nDoneH2tb, nDoneFakeB), False) 


    Verbose("Determine total number of failed jobs (using error files)")
    nFailH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "error_Hplus2tbAnalysis*.txt", "Results are in")
    nFailFakeB = GetNumberOfJobsWithKeyword(opts.dirName, "error_FakeBMeasurement*.txt", "Results are in")
    nFailTotal = nDoneH2tb + nDoneFakeB
    Verbose("Found %s%d%s jobs failed (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nFailTotal, ns, nFailH2tb, nFailFakeB), False) 


    Verbose("Determine jobs still running")
    infoDict  = GetJobStatusDict(opts.userName)
    table   = []
    align  = "{:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}"
    header = align.format("Jobs", "Completed", "Removed", "Idle", "Running", "Held", "Suspended")
    hLine  = "="*15*(7+1)
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    for k in infoDict:
        table.append(align.format(infoDict["jobs"], infoDict["completed"], infoDict["removed"], infoDict["idle"], infoDict["running"], infoDict["held"], infoDict["suspended"]) )
    table.append(hLine)
    for i, row in enumerate(table, 1):
        Verbose(row, i==1)
        

    Verbose("Fill the dictionaries with all the information retrieved", True)
    jobs  = {}
    jobs["total"] = str( nRunTotal )
    jobs["done"]  = str( nDoneTotal )
    jobs["run"]   = str( infoDict["running"] )
    jobs["fail"]  = str( nRunTotal-nDoneTotal-infoDict["running"] )
    
    # Create table
    table   = []
    align  = "{:>20} {:>20} {:>20} {:>20}"
    header = align.format(ns + "TOTAL" + ns, ss+ "DONE" + ns, ts + "RUN" + ns, es + "FAIL" + ns)
    hLine  = "="*40
    # table.append("{:^80}".format(opts.dirName))
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    for k in jobs:
        table.append( align.format(ns + jobs["total"] + ns, ss + jobs["done"] + ns, ts + jobs["run"] + ns, es + jobs["fail"] + ns) )
    table.append(hLine)
    for i, row in enumerate(table, 1):
        Print(row, i==1)

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
    VERBOSE   = False
    DIRNAME   = None
    USERNAME  = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-d", "--dirName", dest="dirName", action="store", default = DIRNAME,
                      help="Name of directory to be checked for status [default: %s]" % (DIRNAME) )

    parser.add_option("-u", "--userName", dest="userName", action="store", default = USERNAME,
                      help="User name (FNAL account) to be used for condor commands [default: %s]" % (USERNAME) )

    (opts, parseArgs) = parser.parse_args()

    # Sanity checks
    if opts.dirName == None:
        Print("Please provide a directory as argument (--dirName option). EXIT!", True)
        sys.exit()

    if opts.userName == None:
        opts.userName = getpass.getuser()

    # Inform user of compatibility issues
    pyV1  =  sys.version_info[0] 
    pyV2  =  sys.version_info[1] 
    pyV3  =  sys.version_info[2] 
    pyVer = "%d.%d.%d" % (pyV1, pyV2, pyV3)
    
    if pyV2 < 7 or pyV3 < 6:
        Print("Requires %sPython 2.7.6%s or later (using %sPython %s). EXIT!" % (hs, ns, es, pyVer + ns), True)
        sys.exit()
    else:
        Print("Requires %sPython 2.7.6%s or later (using %sPython %s)" % (hs, ns, ss, pyVer + ns), True)


    # Call the main function
    main(opts)
