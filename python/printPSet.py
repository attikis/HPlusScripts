#!/usr/bin/env python
'''
Usage:
./printPSet.py -q -a output.root -b TauTriggerAnalyzer_140211_065523/ttbar/output_1X.root && cat PSets_Differences.txt
or
./printPSet.py -v -a output.root -b TauTriggerAnalyzer_140211_065523/ttbar/output_1X.root && cat PSets_Differences.txt

Options:
  -h, --help            show this help message and exit
  -a ROOTFILENAME1, --rootFileName1=ROOTFILENAME1
                        PATH of root  file to read (1)
  -b ROOTFILENAME2, --rootFileName2=ROOTFILENAME2
                        PATH of root  file to read (1)
  -q, --quiet           DISABLE verbose (quiet)
  -v, --verbose         ENABLE vervose (verbose)
  -s SAVEFILENAME, --saveFileName=SAVEFILENAME
                        NAME of save file in which PSet differences will be
                        saved in
  -p PSETFOLDERPATH, --psetFolderPath=PSETFOLDERPATH
                        PATH where the configinfo can be found within a ROOT
                        file
'''
######################################################################
# All imported modules
######################################################################
### System modules
import subprocess
import sys
import os
import re
from optparse import OptionParser
import ROOT

######################################################################
def main():

    ### Get the user-defined options
    myParser = getUserOptions()
    (options, args) = myParser.parse_args()
    if options.verbose:
        print "\n*** OPTIONS:\n\t%s" % (options)

    ### Save user-defined (or default) options (if the user fails to provide his own)
    #cfgFileName   = options.cfgFileName
    rootFileName1  = options.rootFileName1
    rootFileName2  = options.rootFileName2
    psetFolderPath = options.psetFolderPath

    ### Sanity checks
    if rootFileName1 == None and rootFileName2 == None:
        raise Exception ("At least one input ROOT file must be provided!")
        print __doc__
        sys.exit()
    elif rootFileName2 == None:
        ### Get PSets from user-defined ROOT file
        rootFilePsetsPath1 = GetRootFilePsets(options, rootFileName1 , "PSets1_" + rootFileName1.replace("root", "txt").replace("/", "_"))
    elif rootFileName1 == None:
        ### Get PSets from user-defined ROOT file
        rootFilePsetsPath2 = GetRootFilePsets(options, rootFileName2 , "PSets2_" + rootFileName1.replace("root", "txt").replace("/", "_"))
    else:
        ### Get PSets from user-defined ROOT file
        rootFilePsetsPath1 = GetRootFilePsets(options, rootFileName1 , "PSets1_" + rootFileName1.replace("root", "txt").replace("/", "_"))
        rootFilePsetsPath2 = GetRootFilePsets(options, rootFileName2 , "PSets2_" + rootFileName1.replace("root", "txt").replace("/", "_"))
        ### Compare the PSets from two  user-defined ROOT files and write the differences to a file
        ComparePSets(options, rootFilePsetsPath1, rootFilePsetsPath2 )

    ### Get PSets from the user-defined cfg file 
    #cfgFilePsetsPath = GetEdmConfigDumpPsets(options, cfgFileName)
    
    return

######################################################################
def GetEdmConfigDumpPsets(options, cfgFileName):

    ### Setup the command to be called by subprocess
    saveFileName = "PSet_EdmConfigDump.txt"
    saveFilePath = os.getcwd() + "/" + saveFileName
    cmsswCmd     = "edmConfigDump"
    fullCmd      = cmsswCmd + " " + cfgFileName + " > " + saveFileName

    ### Execute command only if cfgFileName exists and saveFileName does not already exist
    fileExists(cfgFileName , True)
    #fileExists(saveFileName, False)
    
    ### Execute the CMSSW script edmConfigDump on the user-defined python configuration file
    if options.verbose:
        print "\n*** VERBOSE: Executing shell command\n    %s" % (fullCmd)

    ### Redirect command  stdout to /dev/null.
    if options.verbose:
        print "\n*** Saving PSets from \"edmConfigDump\" of \"%s\" to:\n    \"%s\"" % (cfgFileName, saveFilePath)
    cmdOutput = subprocess.Popen(fullCmd , shell=True, stdout=open(os.devnull, 'wb'))

    if options.verbose:
        print "\n*** VERBOSE: Obtained PSets from \"%s\"" % (cfgFileName)
    return saveFilePath

######################################################################
def GetRootFilePsets(options, rootFileName, txtSaveName):

    ### Get the ROOT files for all datasets, merge datasets and reorder them
    if options.verbose:
        print "\n*** VERBOSE: Obtaining datasets from ROOT file '%s.'" % (rootFileName)

    ### Set path for the txt file
    saveFilePath = txtSaveName

    ### Check that file does not already exist
    #fileExists(saveFilePath, False)

    ### Save Psets
    saveFile = open(saveFilePath, "w")

    if options.verbose:
        print "\n*** Attempting to get PSets from ROOT file '%s', folder '%s'." % (rootFileName, options.psetFolderPath)
    info = GetTFile(rootFileName).Get(options.psetFolderPath)
    info.SaveAs(saveFilePath)

    if options.verbose:
        print "\n*** Saving PSets from ROOT file '%s' to '%s'." % (rootFileName, saveFilePath)
    saveFile.close()
        
    if options.verbose:
        print "\n*** VERBOSE: Obtained PSets from %s" % (rootFileName)
    return saveFilePath

######################################################################
def GetTFile(rootFilePath, mode = "READ"):

    fileName = rootFilePath.rsplit("/", 1)[-1]
    ### Check that the path actually exists
    if os.path.exists(rootFilePath) == False:
        raise Exception("ROOT file '%s' does not exist! Please make sure the provided path for the file is correct." % (rootFilePath) )
    else:
        rootFile = ROOT.TFile.Open( rootFilePath, mode, fileName, 1, 0)

    ### Ensure that file being accessed is indeed a ROOT file. If so return it, else raise exception
    if isinstance(rootFile, ROOT.TFile) == True:
        return rootFile
    else:
        raise Exception("The file '%s' exists but it is not a ROOT file!" % (rootFile.GetName()) )
    return

######################################################################
def ComparePSets(options, RootFilePsetsPath1, RootFilePsetsPath2):

    ### Read contents of txt file containing the PSets
    RootFilePsets1 = readFile(RootFilePsetsPath1)
    RootFilePsets2 = readFile(RootFilePsetsPath2)

    ### Sort the lists for coherence
    RootFilePsets1.sort()
    RootFilePsets2.sort()

    ### Create lists to place the differences in the two PSets
    RootFileDiffList1 = []
    RootFileDiffList2 = []
    diffList          = []

    ### Create a user-friendly format for the differences found
    title = " "* 10 + "(1) %s <-> (2) %s" % (RootFilePsetsPath1, RootFilePsetsPath2) + " "* 10 
    hLine = "*" * len(title)
    diffList.append(hLine)
    diffList.append(title)
    diffList.append(hLine)

    if options.verbose:
        print hLine + "\n" + title + "\n" + hLine

    ### Loop over the two lists simultaneously and look for differences
    for i,j in zip(RootFilePsets1, RootFilePsets2):
        if i not in j:
            i.strip()
            RootFileDiffList1.append("(1)" + i)
        if i not in j:
            j.strip()
            RootFileDiffList2.append("(2)" + j)

    ### Print differences between the two PSets and save to a txt file
    if options.verbose:
        print "\n*** VERBOSE: Printing differences between the two PSets ..."
    for i, j in zip(RootFileDiffList1, RootFileDiffList2):
        diff = i.replace("\n","") + " <-> " + j.replace("\n","")
        diffList.append(diff)
        if options.verbose:
            print diff

    ### Save results to a txt file
    saveFileName = options.saveFileName
    saveFilePath = os.getcwd() + "/" + saveFileName
    #fileExists(saveFilePath, False)
    saveFile = open(saveFilePath, "w")
    print "\n*** Saving differences in PSets to:\n    \"%s\"" % (saveFilePath)
    for item in diffList:
        saveFile.write(item+"\n")
    saveFile.close()

    return

######################################################################
def readFile(filePath):

    ### First check that file does exists
    fileExists(filePath, True)
    f = open(filePath, "r")
    fileContentsList = f.readlines()
    f.close()

    return fileContentsList

######################################################################
def fileExists(filePath, bRequirement):

    bExists = False
    if os.path.exists(filePath) == True:
        bExists = True
    else:
        bExists = False

    if bRequirement == True and bExists == False:
        print "\n*** WARNING: The file \"%s\" does not exist. Exiting." % (filePath)
        print __doc__
        sys.exit()
    elif bRequirement == False and bExists == True:
        print "\n*** WARNING: The file \"%s\" already exists. Exiting." % (filePath)
        print __doc__
        sys.exit()
    else:
        return
        
######################################################################
def getUserOptions():
    
    ### Parse the user-defined arguments, and put them into an appropriate format to pass to the readFile(cfgFileName, nLines) function
    parser = OptionParser()
    #parser.add_option("-c", "--cfgFileName" , dest = "cfgFileName" , default = "TauTrigger_ExtendedPhase2TkBE5D_cfg.py", help = "PATH of python config file to read", metavar = "CFGFILENAME")
    parser.add_option("-a", "--rootFileName1", dest = "rootFileName1", default = None, help = "PATH of root  file to read (1)", metavar = "ROOTFILENAME1")
    parser.add_option("-b", "--rootFileName2", dest = "rootFileName2", default = None, help = "PATH of root  file to read (1)", metavar = "ROOTFILENAME2")
    parser.add_option("-q", "--quiet", action="store_false", dest = "verbose", default = False, help = "DISABLE verbose (quiet)", metavar = "VERBOSE")
    parser.add_option("-v", "--verbose", action="store_true" , dest = "verbose", default = False, help = "ENABLE vervose (verbose)", metavar = "VERBOSE")
    parser.add_option("-s", "--saveFileName", dest = "saveFileName", default = "PSets_Differences.txt", help = "NAME of save file in which PSet differences will be saved in", metavar = "SAVEFILENAME")
    parser.add_option("-p", "--psetFolderPath", dest="psetFolderPath", default = "TauTrigger/configInfo/parameterSet", help = "PATH where the configinfo can be found within a ROOT file", metavar = "PSETFOLDERPATH")

    return parser
 
######################################################################
if __name__ == "__main__":
    
    main()
