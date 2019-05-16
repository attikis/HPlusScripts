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


def main():

    tarballs   = sys.argv[1:]
    success    = []
    fail       = []
    mgVersion  = None
    nEvents    = 10
    rndSeed    = 12345678
    nCPUS      = 4

    # For-loop: All tarballs provide
    for index, tb in enumerate(tarballs, 1):
        
        if not tb.endswith(".xz"):
            Verbose("%d/%d: Skipping tarball %s (not a tarball!)" % (index, len(tarballs), ErrorStyle() + os.path.basename(tb) + NormalStyle()), True)
            continue
        else:
            pass

        outdirName = "" # tmp_%s" % (index)
        outdirPath = os.path.join(os.getcwd(), outdirName) 
        tarball    = os.path.abspath(tb)
        path       = os.path.dirname(tarball)
        output     = os.path.basename(tarball).replace(".tar.xz",".out")
        outputPath = os.path.join(outdirPath, output)


        if not os.path.exists(outdirPath):
            if outdirName != "":
                os.makedirs(outdirPath)
            Print("Created directory %s" % (NoteStyle() + outdirPath + NormalStyle()), True)
        else:
            pass #continue
            
        Print("%d/%d: Unpacking tarball %s to %s" % (index, len(tarballs), NoteStyle() + os.path.basename(tarball) + NormalStyle(), outdirPath), True) #index==1)
        if 1: #opts.verbose:
            cmd = "tar xfv %s -C %s" % (tarball, outdirPath) 
        else:
            cmd = "tar xf %s -C %s" % (tarball, outdirPath) 
        os.system(cmd)

        # Determine the madgraph version 
        cmd       = "grep VERSION %s" % (os.path.join(outdirPath, "gridpack_generation.log") )
        mgVersion = subprocess.check_output(cmd, shell=True)
        mgVersion = str(mgVersion).replace(" ", "").replace("VERSION", "").replace("x", "").replace("*", "").replace("-", "").replace("\n", "")
        Verbose("MadGraph version is %s " % (NoteStyle() + mgVersion + NormalStyle()), True)
        
        Verbose("Producing the LHE file using the gridpack. Saving output to %s" % (NoteStyle() + outputPath + NormalStyle()), True)
        cmd = "./runcmsgrid.sh %s %s %s >& %s | tee %s" % (nEvents, rndSeed, nCPUS, outputPath, outputPath)
        Verbose("%s" % (HighlightStyle() + cmd + NormalStyle()), True)
        Print("%d/%d: Producing the LHE file and redirecting output to %s" % (index, len(tarballs), HighlightStyle() + os.path.basename(outputPath) + NormalStyle()), True)
        os.system(cmd)
        
        if 0:
            cmd = "tail -50 %s" % (outputPath) 
            Print("%s" % (HighlightStyle() + cmd + NormalStyle()), True)
            os.system(cmd)

        ok = "unknown"
        if os.path.exists("cmsgrid_final.lhe") or os.path.exists("cmsgrid_final.lhe.gz"):
            ok = "ok"
            Verbose("LHE file found, gridpack %s" % (SuccessStyle() + ok + NormalStyle()), True)
            success.append(outputPath)
        else:
            ok = "err"
            Verbose("LHE file not found, gridpack %s. See below for details:" % (ErrorStyle() + ok + NormalStyle()), True)
            if 0:
                os.system("grep error %s" % outputPath)
            fail.append(outputPath)

        cmd = "cp %s %s" % (outputPath, os.path.join(path, output + "." + ok) )
        Verbose("%s" % (HighlightStyle() + cmd + NormalStyle()), True)
        os.system(cmd)

    # Statistics
    nSuccess = len(success)
    nFail    = len(fail)

    Print("%d gridpacks ready and ok:" % (nSuccess), True)
    for i,s in enumerate(success, 1):
        Print(SuccessStyle() + s + NormalStyle(), False)

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
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                     help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE) #fixme
    
    (opts, parseArgs) = parser.parse_args() 

    # Call the main function
    main()
