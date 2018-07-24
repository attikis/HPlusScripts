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
./checkCondor.py -d TopMassLE400_BDT0p40_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_22Jul2018 --getoutput


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
    if not opts.verbose:
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
        #raise Exception(es + err + ns)
        Verbose(es + err + ns)
        nJobs = 0
    else:
        nJobs = int(output.replace(" ", ""))
    return nJobs


def GetSummary(nRunTotal, nDoneTotal, infoDict, printSummary=True):
    Verbose("Fill the dictionaries with all the information retrieved", True)
    jobsDict = {}
    jobsDict["total"] = str( nRunTotal )
    jobsDict["done"]  = str( nDoneTotal )
    jobsDict["run"]   = str( infoDict["running"] )
    jobsDict["fail"]  = str( nRunTotal-nDoneTotal-infoDict["running"] )
    
    # Create table
    table   = []
    align  = "{:>20} {:>20} {:>20} {:>20}"
    header = align.format(ns + "TOTAL" + ns, ss+ "DONE" + ns, ts + "RUN" + ns, es + "FAIL" + ns)
    hLine  = "="*40
    # table.append("{:^80}".format(opts.dirName))
    table.append(hLine)
    table.append(header)
    table.append(hLine)
    for k in jobsDict:
        table.append( align.format(ns + jobsDict["total"] + ns, ss + jobsDict["done"] + ns, ts + jobsDict["run"] + ns, es + jobsDict["fail"] + ns) )
    table.append(hLine)
    for i, row in enumerate(table, 1):
        Print(row, i==1)

    return jobsDict, table


def GetOutputFiles(eosdir):
    cmd = "eos root://cmseos.fnal.gov ls %s" % (eosdir)
    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = process.communicate()

    # Get list of contents 
    output = output.splitlines()

    # Remove anything not ending in ".tgz"
    for o in output:
        if o.endswith(".tgz") == False:
            output.remove(o)
    
    # Separate into "Hplus2tbAnalysis" and "FakeBMeasurement"
    outputH2tb  = []
    outputFakeB = []
    for i, o in enumerate(output, 1):

        if "Hplus2tbAnalysis" in o:
            Verbose(hs + o + ns, i ==1)
            outputH2tb.append(o)

        if "FakeBMeasurement" in o:
            Verbose(ts + o + ns, i==1)
            outputFakeB.append(o)

    # If no results found
    if len(output) < 1:
        return [], [], []
    return output, outputH2tb, outputFakeB
    

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
        filledOnce = False
        for l in output.splitlines():
            if keyword in l and "Total for all users" not in l:
                infoList  = [int(s) for s in l.split() if s.isdigit()]

                # Fill the dictionary
                if filledOnce:
                    infoDict["jobs"]      += infoList[0]
                    infoDict["completed"] += infoList[1]
                    infoDict["removed"]   += infoList[2]
                    infoDict["idle"]      += infoList[3]
                    infoDict["running"]   += infoList[4]
                    infoDict["held"]      += infoList[5]
                    infoDict["suspended"] += infoList[6]
                else:
                    infoDict["jobs"]      = infoList[0]
                    infoDict["completed"] = infoList[1]
                    infoDict["removed"]   = infoList[2]
                    infoDict["idle"]      = infoList[3]
                    infoDict["running"]   = infoList[4]
                    infoDict["held"]      = infoList[5]
                    infoDict["suspended"] = infoList[6]
                filledOnce = True
        else:
            Verbose("Found zero jobs", True)

    if len(infoDict.keys()) < 1:
        raise Exception("Something went wrong and could not determing the jobs running, idle, held, etc..")
    return infoDict


def GetSystToOutputDict(filesList):
    '''
    The input file list (fList) contains all the
    output files of a given analysis (e.g. Hplus2tbAnalysis or
    FakeBMeasurement). But they are for all systematics considered

    This functions returns them in a dictionary so that:
    dict["Systematic"] = list-of-files-for-Systematic
    '''
    # Definitions
    filesDict  = {}
    systematic = None

    # For-loop: All files
    for i, f in enumerate(filesList, 1):

        m = re.search('_Syst(.+?)_', f)
        if m:
            systematic = m.group(1)
        else:
            raise Exception("Could not determine systematics type for file %s" % (f))

        # if key does not exist add it
        if systematic in filesDict.keys():
            filesDict[systematic].append(f)
        else:
            filesDict[systematic] = [f]
    return filesDict


def RetrieveUnpackCleanupFiles(filesSyst, analysis):

    # For-loop: All output files for given systematic
    for i, s in enumerate(filesSyst.keys(), 1):

        # Definitions
        nSyst = len(filesSyst.keys())
        sDir  = False            

        # For-loop: All output files for given systematic
        for j,  f in enumerate(filesSyst[s], 1):
                
            # Define stuff
            m = re.search('_Group(.+?)_', f)
            if m:
                datasetGroup = m.group(1)
            else:
                raise Exception("Could not determine datasets group for file %s" % (f))

            nFiles = len(filesSyst[s])
            if not sDir:
                date   = f.split("-")[-1].replace(".tgz", "")
                time   = f.split("Syst%s" % s)[-1].replace(".tgz", "")#.replace("-" + date, "")
                newDir = f.replace(time, "").replace(".tgz", "") + "_" + date
                newDir = newDir.replace("_Group%s" % datasetGroup, "")
                
            Verbose("Make new dir %s? Or does it already exist?"  % (newDir), True)
            if not os.path.isdir(newDir) and not sDir:
                os.mkdir(newDir)
                # Some jobs might finish at a different day. This causes 2 dirs for a given syst. this fixes it
                sDir = True
            else:
                Verbose(hs + "Dir %s already exists!" % (newDir) + ns, True)

            Verbose("Copy all tarballs under new dir", True)
            eosPath = os.path.join(opts.eosdir, f)
            cmd  = "xrdcp root://cmseos.fnal.gov:/%s %s/." % (eosPath, newDir )
            #msg  = "Copying file %d/%d, systematic %s %d/%d)" % ( j, nFiles, hs + s + ns, i, nSyst)
            msg  = "%s: Systematic %d/%d , File %d/%d" % (hs + analysis + ns, i, nSyst, j, nFiles)
            PrintFlushed(msg, j*i==1)
            process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = process.communicate()
            Verbose(cmd, True)
 
            Verbose("Unpack and subsequently remove the tarball", True)
            filePath = os.path.join(newDir, f)
            cmd = "tar xvzf %s --strip-components=1 -C %s && rm -f %s" % (filePath, newDir, filePath)
            process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, err = process.communicate()
            if len(err) > 0:
                raise Exception(es + err + ns)
            else:
                Verbose(cmd, True)

        Verbose("Now create the \"multicrab.cfg\" file", True)
        os.chdir(newDir)
        cmd = "find * -maxdepth 0 -type d | awk '{print \"[\"$1\"]\"}' > multicrab.cfg"
        process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output, err = process.communicate()
        if len(err) > 0:
            raise Exception(es + err + ns)
        else:
            Verbose(cmd, True)                
            os.chdir("../")
    print
    return

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
    nDoneH2tb  = 0
    nDoneFakeB = 0
    if nOutputH2tb > 0:
        nDoneH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "output_Hplus2tbAnalysis*.txt", "Results are in")
    if nOutputFakeB> 0:
        nDoneFakeB = GetNumberOfJobsWithKeyword(opts.dirName, "output_FakeBMeasurement*.txt", "Results are in")
    nDoneTotal = nDoneH2tb + nDoneFakeB
    Verbose("Found %s%d%s jobs done (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (ts, nDoneTotal, ns, nDoneH2tb, nDoneFakeB), False) 


    Verbose("Determine total number of failed jobs (using error files)")
    nFailH2tb  = 0
    nFailFakeB = 0
    if nErrorH2tb > 0:
        nFailH2tb  = GetNumberOfJobsWithKeyword(opts.dirName, "error_Hplus2tbAnalysis*.txt", "Results are in")
    if nErrorFakeB > 0:
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
        Print(row, i==1)
        

    Verbose("Get the jobs dictionary and the summary table", True)
    jobsDict, table = GetSummary(nRunTotal, nDoneTotal, infoDict, printSummary=True)

    if opts.getoutput:
        if len(jobsDict["done"]) < 1:
            Print("No jobs in \"done\" mode found.", True)
        else:
            Verbose("Found %s jobs in %s state!" % (jobsDict["done"], ss + "DONE" + ns), True)
            
        files, filesH2tb, filesFakeB = GetOutputFiles(opts.eosdir)
        Print("Found %d files in %s (Hplus2tbAnalysis=%d, FakeBMeasurement=%d)" % (len(files), opts.eosdir, len(filesH2tb), len(filesFakeB)), True)
        

        Verbose("Get mapping of systematic->fileList", True)
        filesSystH2tb  = GetSystToOutputDict(filesH2tb)
        filesSystFakeB = GetSystToOutputDict(filesFakeB)

        RetrieveUnpackCleanupFiles(filesSystH2tb, "Hplus2tbAnalysis")
        RetrieveUnpackCleanupFiles(filesSystFakeB, "FakeBMeasurement")

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
    GETOUTPUT = False
    EOSDIR    = "$CONDOR"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-d", "--dirName", dest="dirName", action="store", default = DIRNAME,
                      help="Name of directory to be checked for status [default: %s]" % (DIRNAME) )

    parser.add_option("-u", "--userName", dest="userName", action="store", default = USERNAME,
                      help="User name (FNAL account) to be used for condor commands [default: %s]" % (USERNAME) )

    parser.add_option("-g", "--getoutput", dest="getoutput", action="store_true", default = GETOUTPUT,
                      help="Retrieve output from EOS? [default: %s]" % (GETOUTPUT) )

    parser.add_option("--eosdir", dest="eosdir", action="store", default = EOSDIR,
                      help="Location of CONDOR output files in EOS? [default: %s]" % (EOSDIR) )

    (opts, parseArgs) = parser.parse_args()

    # Sanity checks
    if opts.dirName == None:
        Print("Please provide a directory as argument (-d or --dirName option). EXIT!", True)
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
