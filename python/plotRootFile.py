#!/usr/bin/env python
'''
DESCRIPTION:
This script is designed to plot all histograms from a ROOT file or from a specific
TDirectory inside a ROOT file. It does not take care of any luminosity weights or any other
weights so use with caution. 


USAGE:
./plotRootFile.py -f <file.root> [opts


EXAMPLES:
./plotRootFile.py -f tauFR.root
./plotRootFile.py -f tauFR.root --folder plots


LAST USED:
./plotRootFile.py -f tauFR.root --folder plots

'''

#================================================================================================   
# Imports
#================================================================================================   
import os
import sys
from optparse import OptionParser
import getpass
import ROOT

import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux


#================================================================================================
# Variable definition
#================================================================================================
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
ls = ShellStyles.HighlightStyle()
es = ShellStyles.ErrorStyle()
cs = ShellStyles.CaptionStyle()


#================================================================================================   
# Function definition
#================================================================================================   
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true.
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def usage():
    print
    print "### Usage: ",os.path.basename(sys.argv[0])," <pseudomulticrab dir>"
    print
    sys.exit()

def main():

    ROOT.gROOT.SetBatch(opts.batchMode)
    style = tdrstyle.TDRStyle()

    # For-loop: All ROOT files
    for i, f in enumerate(opts.rootFiles, 1):
        Print("%d/%d) File %s" % (i, len(opts.rootFiles), ls + f + ns), i==1)
        
        # Load the TFile in memory
        f = ROOT.TFile.Open(opts.rootFile , "READONLY");

        if f.IsZombie():
            msg = "The ROOT file \"%s\" is a zombie!" % (opts.rootFile)
            raise Exception(es + msg + ns)

        # Get List of histograms in ROOT file
        histoList = getHistoList(f)

        # Now draw the histograms
        PlotHistoListForFile(f, histoList)
        PlotHistoDivisionForFile(f, "plots/TauPt_TightTau" , "plots/TauPt_LooseTau" , hName="TauFakeRate_Pt")
        PlotHistoDivisionForFile(f, "plots/TauEta_TightTau", "plots/TauEta_LooseTau", hName="TauFakeRate_Eta")
        PlotHistoDivisionForFile(f, "plots/TauPtJetPtRatio_TightTau", "plots/TauPtJetPtRatio_LooseTau", hName="TauFakeRate_R")
        
        # Close the ROOT file
        f.Close()

    # inform user of output location
    Print("Plots saved under directory %s"% (ls + aux.convertToURL(opts.saveDir, opts.url) + ns), True)
    return


def getHistoList(rootFile):

    histoList = []
    if opts.rootFolder != None:
        histoList_ = getListOfKeys(rootFile, opts.rootFolder)
        histoList  = [os.path.join(opts.rootFolder, h) for h in histoList_]
    else:
        objDict = {}
        listRecursive(rootFile, objDict)
        #histoList = getRootObjectDictionary(f, objDict)
        histoList = [objDict[key]["Path"] for key in objDict.keys() if "Path" in objDict[key].keys()]
        
    if len(histoList) < 1:
        raise Exception(es + "Found no histograms to be plotted!" + ns)
    else:
        Print("Found %s%d%s objects for plotting:" % (ss, len(histoList), ns), True)
        for h in histoList:
            Print(hs + h + ns, False)
        return histoList


def getListOfKeys(rootFile, dir=""):
    '''
    Given a ROOT file, it returns the list of object names contained in the file in the provided directory.

    param rootFile: a ROOT.TFile instance
    :param dir: the directory (default: "", i.e., the root of the file)
    :return: a list of object names
    '''
    if not isinstance(rootFile, ROOT.TFile):
        msg = "The parameter \"rootFile\" is not a ROOT.TFile instance"
        raise Exception(es + msg + ns)

    rootFile.cd(dir)
    keyList = [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()] 
    rootFile.cd("")    
    return keyList


def listRecursive(obj, objDict, path=""):
    if not isinstance(objDict, dict):
        objDict = {}
    else:
        pass
        
    keyList = []
    try:
        keyList = obj.GetListOfKeys()
    except:
        msg = "Cannot get list of keys from object of type %s" % (type(obj))
        Verbose(msg, True)

    nKeys = len(keyList)

    # For-loop: All keys
    for i, key in enumerate(keyList, 1):
        objDict[key.GetName()] = {}
        objDict[key.GetName()]["TKey"]  = key
        objDict[key.GetName()]["Class"] = key.GetClassName()
        objDict[key.GetName()]["Bytes"] = key.GetNbytes() # Number of bytes for the object on file

        Verbose("i = %d, path = %s, name = %s, className = %s" % (i, path, key.GetName(), key.GetClassName()), i==1)

        # https://root.cern.ch/doc/master/classTDirectory.html
        if "TH" in key.GetClassName():

            integral = obj.FindObjectAny(key.GetName()).Integral()
            entries  = obj.FindObjectAny(key.GetName()).GetEntries()
            objDict[key.GetName()]["TKey"]     = key
            objDict[key.GetName()]["Integral"] = integral
            objDict[key.GetName()]["Entries"]  = entries
            if path != "":
                objDict[key.GetName()]["Path"] = os.path.join(path, key.GetName())
            else:
                objDict[key.GetName()]["Path"] = key.GetName()
        
        d = key.ReadObj()
        if (d):
            if "TDirectory" in key.GetClassName():
                path = key.GetName()
            listRecursive(d, objDict, path)
    return


def getRootObjectDictionary(f, objDict):
    nKeys   = len(objDict.keys())
    table   = []
    align   = "{:>5} {:^20} {:<45}"
    title   = "{:^70}".format("%s" % (f.GetName()))
    header  = align.format("#", "parameter", "value")
    objList = []
    hLine   = "="*70
    table.append(title)

    # For-loop: All ROOT objects in file
    for i, key1 in enumerate(objDict.keys(), 1):
        
        table.append("{:^70}".format("%s" % (key1) ))
        table.append(hLine)
        table.append(header)
        table.append(hLine)
        print key1
        objList.append(key1["Path"])

        # For-loop: All objects
        for j, key2 in enumerate(objDict[key1], 1):
            table.append(align.format(j, key2, objDict[key1][key2]))

        for k, row in enumerate(table, 1):
            Verbose(row, k==1)            
    return objList

def PlotHistoListForFile(f, histoList):
    
    nHistos = len(histoList)
    for i, hPath in enumerate(histoList, 1):

        hName = os.path.basename(hPath)

        Verbose("%d/%d) Retrieving rootHisto from ROOT file \"%s\"" % (i, nHistos, f.GetName()), True)
        rh = getattr(f, hPath)
        
        if 0:
            print rh.Integral()

        Verbose("%d/%d) Creating histogram object from rootHisto" % (i, nHistos), False)
        if 0:
            h = histograms.Histo(rh, "rh", drawStyle="EP")
            styles.dataStyle(h)
        else:
            h = histograms.Histo(rh, "rh", drawStyle="HIST")
            styles.qcdFillStyle(h)
        
        
        Verbose("%d/%d) Plotting base histogram" % (i, nHistos), False)
        p = plots.PlotBase( [h], [".png"])
        p.createFrame(hName, opts={"ymin": 10, "ymaxfactor": 1.2}, opts2={"ymin": 0.5, "ymax": 1.5})
        p.getFrame().GetYaxis().SetTitle("Events")
        #p.getFrame().GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
        #p.getPad().SetLogy(True)
        p.draw()

        Verbose("%d/%d) Adding standard text" % (i, nHistos), False)
        if opts.intLumi!= None:
            histograms.addStandardTexts(lumi=opts.intLumi)
        myText = "Entries= %d, Integral = %.1f" % (h.getRootHisto().GetEntries(), h.getRootHisto().Integral())
        histograms.addText(0.2, 0.86, myText, 22)

        Verbose("%d/%d) Saving canvas for histogram \"%s\"" % (i, nHistos, hPath), False)
        # p.save([".png"])
        SavePlot(p, opts.saveDir, hName, [".png"])

        if opts.verbose:
            print

    return


def PlotHistoDivisionForFile(f, numeratorHisto, denominatorHisto, hName="TauFakeRate"):
    
    # Define your histograms here
    rh1 = getattr(f, numeratorHisto)    
    rh2 = getattr(f, denominatorHisto)

    # Print ?
    if opts.verbose:
        aux.PrintTH1Info(rh1)
        aux.PrintTH1Info(rh2)

    # Create histogram objects
    h1 = histograms.Histo(rh1,"rh1", drawStyle="EP")
    h2 = histograms.Histo(rh2,"rh2", drawStyle="HIST")

    # Sapply styles
    styles.dataStyle(h1) #styles.ttStyle(h1)
    styles.invertedStyle(h2) #styles.ewkfakeFillStyle(h2) # styles.qcdFillStyle(h2) #styles.genTauFillStyle(h2)

    # Create plotting object
    p = plots.ComparisonPlot(h1, h2)
    p.createFrame(hName, createRatio=True, opts={"ymin": 0.9e-2, "ymaxfactor": 10}, opts2={"ymin": 0.0, "ymax": 1.0})
    #p.getFrame().GetXaxis().SetTitle("#tau_{h} p_{T} (GeV)")
    p.getFrame().GetXaxis().SetTitle(rh1.GetXaxis().GetTitle())
    p.getFrame().GetYaxis().SetTitle("fake factors (j #rightarrow #tau_{h})")
    p.getFrame2().GetYaxis().SetTitle("Ratio")
    p.getFrame2().GetYaxis().SetTitleOffset(1.1*p.getFrame().GetYaxis().GetTitleOffset())
    p.getPad1().SetLogy(True)
    p.draw()
    histograms.addStandardTexts(lumi=35900)
    myText = "Entries= %d (%d)" % (h1.getRootHisto().GetEntries(), h2.getRootHisto().GetEntries())
    histograms.addText(0.2, 0.86, myText, 22)

    # Szave the plot
    # p.save([".png"])    
    SavePlot(p, opts.saveDir, hName, [".png"])
    return

def SavePlot(plot, saveDir, plotName, saveFormats = [".png", ".pdf"]):
    # Check that path exists
    if not os.path.exists(saveDir):#fixme
        os.makedirs(saveDir)

    # Create the name under which plot will be saved
    saveName = os.path.join(saveDir, plotName.replace("/", "_"))

    # For-loop: All save formats
    for i, ext in enumerate(saveFormats, 1):
        saveNameURL = saveName + ext
        saveNameURL = saveNameURL.replace("/afs/cern.ch/user/a/attikis/public/html", "https://cmsdoc.cern.ch/~%s" % getpass.getuser())
        if opts.url:
            Verbose (saveNameURL, False)
        else:
            Verbose(saveName + ext, False)
        plot.saveAs(saveName, formats=saveFormats)    
    return

if __name__=="__main__":
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
    
    # Default Settings
    BATCHMODE  = True
    ROOTFILE   = "dumbie.root"
    ROOTFOLDER = None
    INTLUMI    = None# 35900.0
    SAVEDIR    = "/publicweb/%s/%s/tmp" % (getpass.getuser()[0], getpass.getuser())
    VERBOSE    = False
    URL        = True 

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-f", "--file", dest="rootFile", action="store", default=ROOTFILE,
                      help="Path to the ROOT file(s) to be used as input. For multiple files use comma-separated string (no spaces). [default: %s]" % ROOTFILE)

    parser.add_option("--folder", dest="rootFolder", action="store", default=ROOTFOLDER,
                      help="The ROOT folder name where the histograms to be plotted can be found. If nothing is specified then ALL histograms in all folders will be plotted [default: %s]" % ROOTFOLDER)

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--intLumi", dest="intLumi", type=float, default=INTLUMI,
                      help="Override the integrated lumi [default: %s]" % INTLUMI)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--url", dest="url", action="store_true", default=URL,
                      help="Don't print the actual save path the plots are saved, but print the URL instead [default: %s]" % URL)


    (opts, parseArgs) = parser.parse_args()

    if "," in opts.rootFile:
        opts.rootFiles = opts.rootFile.split(",")
    else:
        opts.rootFiles = [opts.rootFile]

    # Sanity-check (files exist)
    for f in opts.rootFiles:
        if not os.path.isfile(f):
            msg = "The (alleged) file \"%s\" does not exist!" % (f)
            raise Exception(es + msg + ns)

    main()
