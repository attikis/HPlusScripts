#!/usr/bin/env python
'''
DESCRIPTION:
Submit multible jobs to condor


USAGE:
./submitCondor.py [options]


EXAMPLE:
./submitCondor.py --topMass 400 --bdt 0p40


LAST USED:
submitCondor.py --topMass 500 --bdt 0p40 --codeTarball HiggsAnalsysis.tgz --binning 4EtaBins5PtBins --mcrabTarball multicrab_Hplus2tbAnalysis_v8030_20180508T0644.tgz 


'''

#================================================================================================ 
# Modules here
#================================================================================================ 
import subprocess
from subprocess import Popen, PIPE
import os
import sys
import datetime
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
        print "=== submitCondor.py:"

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

def CheckForValidProxy():
    process = Popen(['voms-proxy-info'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
        # err  = err.replace("\n", "")
        # err += " Continuing anyway (not needed)"
        # Print(es + err + ns, True)
    else:
        lines = output.splitlines()
        for l in lines:
            if "timeleft" not in l:
                continue
            time  = l.split(": ")[-1]
            hours = int(time.split(":")[0])
            mins  = int(time.split(":")[1])
            secs  = int(time.split(":")[2])

            # Determine the time remaining in seconds
            dt = hours*60*60 + mins*60 + secs

            # Require at least 60 seconds of valid proxy
            if dt < 60:
                raise Exception(es + "No valid CMS VO proxy found!" + ns)
            else:
                Print(ss + "Valid CMS VO proxy found!" + ns, True)
    return


def CreateRunningScript(scriptName="runSystOnCondor.csh", opts):
    filePath = os.path.join(opts.dirName, scriptName)

    Print("Creating newfile %s" % filePath, True)
    f = open(filePath, "w")
    
    #'''
    f.write('#!/bin/tcsh\n')
    f.write('#================================================================================================\n')
    f.write('# Get command line parameters\n')
    f.write('#================================================================================================\n')
    f.write('if ($#argv < 3) then\n')
    f.write('echo "=== You must give at least 3 arguments:"\n')
    f.write('echo "1=ANALYSISDIR"\n')
    f.write('echo "2=LABEL"\n')
    f.write('echo "3=GROUP"\n')
    f.write('echo "4=SYSTEMATICS (optional)"\n')
    f.write('echo\n')
    f.write('exit 1\n')
    f.write('endif\n')
    f.write('\n')
    f.write('#================================================================================================\n')
    f.write('# Define variables\n')
    f.write('#================================================================================================\n')
    f.write('set ANALYSISDIR = ${1}\n')
    f.write('set LABEL       = ${2}\n')
    f.write('set GROUP       = ${3}\n')
    f.write('set SYSTEMATICS = ${4}\n')
    f.write('\n')
    f.write('#set TARBALL = multicrab_Hplus2tbAnalysis_v8030_20180223T0905\n')
    f.write('set TARBALL = multicrab_Hplus2tbAnalysis_v8030_20180508T0644\n')
    f.write('\n')
    f.write('echo "\n=== Running on:" \n')
    f.write('hostname -A\n')
    f.write('pwd\n')
    f.write('echo ${_CONDOR_SCRATCH_DIR}\n')
    f.write('source /cvmfs/cms.cern.ch/cmsset_default.csh\n')
    f.write('\n')
    f.write('echo "\n=== Untarring the code tarball"\n')
    f.write('tar -xf HiggsAnalysis.tgz\n')
    f.write('rm -rf HiggsAnalysis.tgz\n')
    f.write('\n')
    f.write('echo "\n=== Untarring the multicrab dir tarball"\n')
    f.write('tar -xf $TARBALL.tgz\n')
    f.write('\n')
    f.write('# Source the environment settings script\n')
    f.write('echo "\n=== Changing dir to HiggsAnalysis and sourcing setup.csh"\n')
    f.write('cd HiggsAnalysis\n')
    f.write('source setup.csh\n')
    f.write('echo `pwd`\n')
    f.write('\n')
    f.write('# Go to work directory to run the analysis\n')
    f.write('set WORKDIR = NtupleAnalysis/src/$ANALYSISDIR/work/\n')
    f.write('echo "\n=== Changing dir to $WORKDIR"\n')
    f.write('cd $WORKDIR\n')
    f.write('\n')
    f.write('# Save the submit/start time for future use\n')
    f.write('set STIME = `date "+%Hh-%Mm-%Ss-%d%h%Y"`\n')
    f.write('\n')
    f.write('# Run the analyser\n')
    f.write('echo "\n=== Running the analysis by executing runSystematics.py as follows:"\n')
    f.write('echo "./runSystematics.py -m ${_CONDOR_SCRATCH_DIR}/$TARBALL/ --doSystematics --group $GROUP\n"\n')
    f.write('./runSystematics.py -m ${_CONDOR_SCRATCH_DIR}/$TARBALL/ --group $GROUP --systVars $SYSTEMATICS \n')
    f.write('\n')
    f.write('echo "\n=== Listing all directories"\n')
    f.write('echo`ls -alt | grep ^d` #| grep $ANALYSISDIR`\n')
    f.write('\n')
    f.write('echo "\n=== Listing the latest directory"\n')
    f.write('echo `ls -td */ | head -1`\n')
    f.write('\n')
    f.write('echo "\n=== Determining output dir using ls and grep commands"\n')
    f.write('set OUTPUTDIR = `ls -td */ | head -1`\n')
    f.write('echo "\n=== Output dir determined to be $OUTPUTDIR"\n')
    f.write('# -t orders by time (latest first)\n')
    f.write('# -d only lists items from this folder\n')
    f.write('# */ only lists directories\n')
    f.write('# head -1 returns the first item\n')
    f.write('\n')
    f.write('# Create the tarball name\n')
    f.write('set FTIME = `date "+%Hh-%Mm-%Ss-%d%h%Y""\n')
    f.write('# set TIME = `date "+%Hh%Mm%Ss_%d%h%Y"`\n')
    f.write('# set TIME = `date "+%Hh-%Mm-%Ss-%d%h%Y"`\n')
    f.write('# set TIME = `date "+%d%h%Y"`\n')
    f.write('# set TIME = `date +"%d%m%Y"`\n')
    f.write('echo "\n=== Tarball name will be ${ANALYSISDIR}_${LABEL}_${STIME}_${FTIME}.tgz"\n')
    f.write('set TARBALL = "${ANALYSISDIR}_${LABEL}_${STIME}_${FTIME}.tgz"\n')
    f.write('\n')
    f.write('# Make the output directory to a tarball\n')
    f.write('echo "\n=== Compressing the output dir $OUTPUTDIR into tarball file $TARBALL"\n')
    f.write('tar -cvzf $TARBALL $OUTPUTDIR\n')
    f.write('\n')
    f.write('#echo "\n=== Copying output directory $OUTPUTDIR to EOS"\n')
    f.write('#xrdcp -rf $OUTPUTDIR  root://cmseos.fnal.gov//store/user/$USER/.\n')
    f.write('set EOSDIR = store/user/$USER/CONDOR_TransferData\n')
    f.write('echo "\n=== Copying output tarball $TARBALL to $EOSDIR"\n')
    f.write('xrdcp $TARBALL  root://cmseos.fnal.gov//$EOSDIR/\n')
    f.write('\n')
    f.write('echo "\n=== Delete everything from ${_CONDOR_SCRATCH_DIR} before exiting"\n')
    f.write('cd ${_CONDOR_SCRATCH_DIR}\n')
    f.write('rm -rf HiggsAnalysis\n')
    #'''
    f.close()
    return


def main(opts):

    Verbose("Check that a CMS VO proxy exists (voms-proxy-init)", True)
    CheckForValidProxy()


    Verbose("Create directory %s" % (opts.dirName), True)
    if os.path.isdir(opts.dirName):
        Print("Directory %s already exists! EXIT" % (es + opts.dirName + ns), True)
        sys.exit()
    else:
        Print("Creating directory %s" % (ss + opts.dirName + ns), True)
        os.mkdir(opts.dirName)
    os.system("cp %s %s/." % ("runSystOnCondor.csh", opts.dirName) )
    os.chdir(opts.dirName)

    # Settings
    analyses  = ["Hplus2hwAnalysisWithTop", "FakeBMeasurement"]
    nSyst     = len(opts.systVarsList)
    groupDict = {}
    jdlList   = []
    groupDict["Hplus2tbAnalysis"] = map(chr, range(65, 91))
    groupDict["FakeBMeasurement"] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]


    Verbose("Create the runSystOnCondor.csh script that will create the job", True)
    CreateRunningScript(scriptName="runSystOnCondor.csh", opts)
    sys.exit()

    Verbose("Creating the jdl files", True)
    # For-loop: All analyses
    for i, analysis in enumerate(analyses, 1):
        groups  = groupDict[analysis]
        nGroups = len(groups)

        # For-loop: All systematics
        for j, syst in enumerate(opts.systVarsList, 1):
            
            # For-loop: All groups
            for k, group in enumerate(groups, 1):
                baseName = "%s_Group%s_Syst%s" % (analysis, group, syst)
                # fileName = "%s_Cluster$(Cluster)_Process$(Process)" % (baseName) #original
                fileName = baseName
                jdl = "run_%s.jdl" % (baseName)
                
                msg = "Creating %s (%d/%d)" % (jdl, j*k, nGroups*nSyst)
                if "FakeB" in analysis:
                    PrintFlushed(ts + msg + ns, i*j*k==1)
                else:
                    PrintFlushed(hs + msg + ns, i*j*k==1)
                f = open(jdl, "w")    
                f.write("universe = vanilla\n")
                f.write("Executable = runSystOnCondor.csh\n")
                f.write("Should_Transfer_Files = YES\n")
                f.write("WhenToTransferOutput = ON_EXIT\n")
                f.write("Transfer_Input_Files = runSystOnCondor.csh, %s/HiggsAnalysis.tgz, %s/%s.tgz\n" % (opts.codePath, opts.mcrabPath, opts.mcrab) )
                f.write("Output = output_%s.txt\n" % (fileName) )
                f.write("Error  = error_%s.txt\n"  % (fileName) )
                f.write("Log    = log_%s.txt\n"    % (fileName) )
                f.write("x509userproxy = /tmp/x509up_u52142\n")
                f.write("Arguments = %s %s_%s_Group%s_Syst%s %s %s\n" % (analysis, opts.finalState, opts.region, group, syst, group, syst) )
                f.write("Queue 1\n")
                f.close()
                jdlList.append(jdl)
        print
        
    Verbose("Submitting the jobs", True)
    for i, jdl in enumerate(jdlList, 1):
        cmd = "condor_submit %s" %  (jdl)
        #PrintFlushed(hs + cmd + ns, i==1)
        os.system(cmd)

    Print("Total of %s%d jobs submitted%s" % (ss, len(jdlList), ns), True)
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
    SYSTVARS  = None
    CODEPATH  = "/uscms_data/d3/aattikis/workspace/cmssw/CMSSW_10_6_17/src"
    MCRABPATH = "/uscms_data/d3/aattikis/workspace/multicrab"
    MCRAB     = "multicrab-Hplus2hwAnalysis-CMSSW10_6_17-Run2016BCDEFGH-dataVersion2016_102X-29Sep2020"
    DIRNAME   = None
    FINALSTATE= None
    REGION    = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--systVars", dest="systVars", default = SYSTVARS,
                      help="List of comma-separated (NO SPACE!) systematic variations to  perform. Overwrites the default list of systematics [default: %s]" % SYSTVARS)

    parser.add_option("--codePath", dest="codePath", default = CODEPATH,
                      help="Full path to HiggsAnalysis code tarball to be ran on [default: %s]" % CODEPATH)

    parser.add_option("--mcrabPath", dest="mcrabPath", default = MCRABPATH,
                      help="Full path to multicrab Ntuples to be ran on [default: %s]" % MCRABPATH)

    parser.add_option("--mcrab", dest="mcrab", action="store", default = MCRAB,
                      help="Path to the multicrab directory for input [default: %s]" % (MCRAB) )

    parser.add_option("-d", "--dirName", dest="dirName", action="store",
                      help="Name of directory to be created where all the output will be stored [default: %s]" % (DIRNAME) )

    parser.add_option("--finalState", dest="finalState", action="store", default = FINALSTATE,
                      help="The final state you wish to run on (different analyzer)  (default: %s)" % (FINALSTATE) )

    parser.add_option("--region", dest="region", action="store", default = REGION,
                      help="The region you wish to run on (different cuts)  (default: %s)" % (REGION) )

    (opts, parseArgs) = parser.parse_args()

    opts.fsList = ["ETau", "MuTau"]
    if opts.finalState == None:
        raise Exception("Please provide a valid --finalState option: \"%s\"" % ("\", \"".join(opts.fsList)) )

    opts.regionList = ["SR", "VR1", "VR2"]
    if opts.region == None:
        raise Exception("Please provide a valid --region option: \"%s\"" % ("\", \"".join(opts.regionList)) )

    # Define output dir name
    timeStamp = datetime.datetime.now().strftime("%d%b%Y_%Hh%Mm%Ss")
    if opts.dirName == None:
        opts.dirName = "Hplus2hwAnalysisWithTop_%s_%s_%s" % (opts.finalState, opts.region, timeStamp)
    else:
        opts.dirName += "_%s" % (date)

    # Overwrite default systematics
    opts.systVarsList = []
    if opts.systVars != None:
        opts.doSystematics = True
        opts.systVarsList = opts.systVars.split(",")
    else:
        opts.systVarsList = ["JES", "JER", "BTagSF", "PUWeight",  "TopTagSF"]

    # Call the main function
    main(opts)
