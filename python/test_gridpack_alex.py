#!/usr/bin/env python
'''
This script unpacks gridpacks (contain all the needed code to produce events) and attempts to validate it by 
running the gridpack from CMSSW.

First we unpack theMG5_aMC@NLO gridpacks with the command:
tar -xavf <path of gridpack creation>/<gridpack>.tar.xz

Then, the LHE file is produced out of this gridpack:

bash
./runcmsgrid.sh <NEvents> <RandomSeed> <NumberOfCPUs>

where the runcmsgrid.sh script requires at least 3 parameters: 
<NEvents>      = number of events to be generated, 
<RandomSeed>   = a random seed 
<NumberOfCPUs> = the number of CPUs


LAST USED:
./test_gridpack_alex.py gridpacks_HToTB_MG5_v260/ChargedHiggs_TB_madspin_NLO_M3000_slc6_amd64_gcc630_CMSSW_9_3_8_tarball.tar.xz


NOTE:
To test OLD gridpacks it is needed to setup a release first, which must be consistent with the release and architecture that was used for the gridpack creation. So add before :
cmsrel CMSSW_X_Y_Z 
cd CMSSW_X_Y_Z/src
cmsenv


LINKS:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Quick_tutorial_on_how_to_produce

'''
#================================================================================================
# Imports
#================================================================================================
import os
import sys
import subprocess
from optparse import OptionParser 

#================================================================================================
# Function Definition 
#================================================================================================
def NoteStyle():
    return "\033[0;35m"

def HighlightStyle():
    return "\033[0;33m"

def WarningStyle():
    return "\033[0;43m\033[1;37m"

def ErrorStyle():
    return "\033[1;31m"       

def NormalStyle():
    return "\033[0;0m"

def SuccessStyle():
    return "\033[92m"
                       
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=False):
    if not opts.verbose:
        return
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def Execute(cmd):
    Print(cmd, True)
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    stdin  = p.stdout
    stdout = p.stdout
    ret    = []
    for line in stdout:
        ret.append(line.replace("\n", ""))
    stdout.close()
    return ret    
   

def main():

    tarballs   = sys.argv[1:]
    success    = []
    fail       = []
    mgVersion  = None
    nEvents    = 5
    rndSeed    = 12345678
    nCPUS      = 16

    # For-loop: All tarballs provide
    for index, tb in enumerate(tarballs, 1):
        
        if not tb.endswith(".xz"):
            Verbose("%d/%d: Skipping tarball %s (not a tarball!)" % (index, len(tarballs), ErrorStyle() + os.path.basename(tb) + NormalStyle()), True)
            continue
        else:
            pass

        # Definitions
        massPoint = os.path.basename(tb).split("_M")[1].split("_")[0]
        if isinstance(massPoint, str):
            Verbose("Processing mass point %s" % (massPoint), True)
        else:
            Print("Could not determine  mass point for tarball %s. Exit" % (tb), True)
            sys.exit()
        outdirName = "gridpack_M" + massPoint
        outdirPath = os.path.join(os.getcwd(), outdirName) 
        tarball    = os.path.abspath(tb)
        path       = os.path.dirname(tarball)
        outFile    = os.path.basename(tarball).replace(".tar.xz",".out")
        outFileAlt = outFile.replace(".out", "2.out")
        outputPath = os.path.join(outdirPath, outFile)

        if not os.path.exists(outdirPath):
            if outdirName != "":
                os.makedirs(outdirPath)
            Verbose("Created directory %s" % (NoteStyle() + outdirPath + NormalStyle()), True)
        else:
            Print("Directory %s exists. Exit" % (NoteStyle() + outdirPath + NormalStyle()), True)
            sys.exit()

        Print("%d/%d: Unpacking %s to %s" % (index, len(tarballs), HighlightStyle() + os.path.basename(tarball) + NormalStyle(), outdirPath), index==1)
        if opts.verbose:
            cmd = "tar xfv %s -C %s" % (tarball, outdirPath) 
        else:
            cmd = "tar xf %s -C %s" % (tarball, outdirPath) 
        os.system(cmd)

        # Determine the madgraph version 
        logFile   = os.path.join(outdirPath, "gridpack_generation.log") 
        cmd       = "grep VERSION %s" % (logFile)
        mgVersion = subprocess.check_output(cmd, shell=True)
        mgVersion = str(mgVersion).replace(" ", "").replace("VERSION", "").replace("x", "").replace("*", "").replace("-", "").replace("\n", "")
        Verbose("MadGraph version is %s " % (NoteStyle() + mgVersion + NormalStyle()), True)

        Verbose("Producing the LHE file using the gridpack. Saving output to %s" % (NoteStyle() + outputPath + NormalStyle()), True)
        #cmd = "cd %s && ./runcmsgrid.sh %s %s %s >& %s | tee %s" % (outdirPath, nEvents, rndSeed, nCPUS, outFile, outFile)
        cmd = "cd %s && ./runcmsgrid.sh %s %s %s >& %s" % (outdirPath, nEvents, rndSeed, nCPUS, outFile)
        Verbose("%s" % (HighlightStyle() + cmd + NormalStyle()), True)
        Print("%d/%d: Producing the LHE file and redirecting output to %s" % (index, len(tarballs), HighlightStyle() + outFile + NormalStyle()), False)
        os.system(cmd) #ret = Execute(cmd)

        # Determine success/failure
        ok = "unknown"
        lheFile = os.path.join(outdirPath, "cmsgrid_final.lhe") 
        gzFile  = os.path.join(outdirPath, "cmsgrid_final.lhe.gz")
        if os.path.exists(lheFile) or os.path.exists(gzFile):
            ok = "ok"
            Verbose("LHE file found, gridpack %s" % (SuccessStyle() + ok + NormalStyle()), True)
            success.append(outputPath)
        else:
            ok = "err"
            Verbose("LHE file not found, gridpack %s. See below for details:" % (ErrorStyle() + ok + NormalStyle()), True)
            if 0:
                os.system("grep error %s" % outputPath)
            fail.append(outputPath)

        if opts.cleanup:
            cmd = "rm -rf %s" % outdirPath
            Print(cmd, True)
            os.system(cmd)

    # Statistics
    nSuccess = len(success)
    nFail    = len(fail)

    if len(success) > 0:
        Print("%d gridpacks ready and ok:" % (nSuccess), True)
        for i,s in enumerate(success, 1):
            Print(SuccessStyle() + s + NormalStyle(), False)
    if len(fail) > 0:            
        Print("%d gridpacks failed" % (nFail), True)
        for i,f in enumerate(fail, 1):
            Print(ErrorStyle() + f + NormalStyle(), False)

    return
            
#================================================================================================
# Main
#================================================================================================
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
    
    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]") 
    
    # Default Settings
    VERBOSE  = False
    CLEANUP  = False

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                     help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--cleanup", dest="cleanup", action="store_true", default=CLEANUP, 
                      help="Delete unpacked directory after determining success/failure of gridpack) [default: %s]" % CLEANUP)
    
    (opts, parseArgs) = parser.parse_args() 

    # Call the main function
    main()
