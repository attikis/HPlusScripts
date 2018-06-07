## Package for all systematic uncertainties in the analysis

#######################################
# Shape uncertainties

# These are obtained automatically for each dataset from the SystVar identifier in the analysis module names
# Also, one can take the full list of shapes, since the variations are zero compared to nominal,
# unless the analysis has proceeded to a stage where the selection to be varied has been applied

# Considered shape uncertainties:
# - Tau trg SF uncertainty
# (- MET trg SF uncertainty)
# - fake tau SF uncertainty FIXME to be implemented
# - tau energy scale (TES)
# - jet energy scale (JES)
# - MET (unclustered) energy scale
# - jet energy resolution (JER)
# - btag SF
# - top pT reweight SF uncertainty FIXME to be implemented
# - pileup uncertainty
# - QCD method normalization
# - statistical uncertainties

#######################################
# Scalar uncertainties

# List of considered uncertainties:
# - tau ID uncertainty
# - tau mis-ID uncertainty
# - e/mu reco and ID
# - Embedding specific FIXME: add if necessary
# - cross section uncertainties
# - luminosity

from math import sqrt

import ShellStyles

## Helper class for a scalar uncertainty
class ScalarUncertaintyItem:
    def __init__(self, uncertaintyName, *args, **kwargs):
        self._name = uncertaintyName
        self._uncertUp = 0.0 # relative uncertainty squared
        self._uncertDown = 0.0 # relative uncertainty squared
        # Handle inputs
        if len(args) == 1:
            if isinstance(args[0], ScalarUncertaintyItem):
                self._uncertUp = args[0]._uncertUp
                self._uncertDown = args[0]._uncertDown
            else:
                # Symmetric uncertainty
                self._uncertUp = args[0]
                self._uncertDown = args[0]
        elif len(args) == 0 and len(kwargs) == 2:
            if not "plus" in kwargs or not "minus" in kwargs:
                raise Exception("Error: You forgot to give plus= and minus= arguments to ScalarUncertaintyItem()!")
            self._uncertUp = kwargs["plus"]
            self._uncertDown = kwargs["minus"]
        else:
            raise Exception("Error: You forgot to give the uncertainty value(s) to ScalarUncertaintyItem()!")

    def add(self,other):
        self._name += "+%s"%other._name
        self._uncertUp = sqrt(self._uncertUp**2 + other._uncertUp**2)
        self._uncertDown = sqrt(self._uncertDown**2 + other._uncertDown**2)

    def Clone(self):
        return ScalarUncertaintyItem(self._name, self)

    def scale(self, factor):
        self._uncertUp *= factor
        self._uncertDown *= factor

    def getName(self):
        return self._name

    def isAsymmetric(self):
        return abs(self._uncertDown - self._uncertUp) > 0.0000001

    def getUncertaintySquaredDown(self):
        return self._uncertDown**2

    def getUncertaintyDown(self):
        return self._uncertDown

    def getUncertaintySquaredUp(self):
        return self._uncertUp**2

    def getUncertaintyUp(self):
        return self._uncertUp

    def getUncertaintyMax(self):
        return max([self._uncertUp, self._uncertDown])

_crossSectionUncertainty = {
    # TTJets, based on arxiv:1303.6254 and https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
    "TTJets_scale": ScalarUncertaintyItem("xsect", plus=19.77/831.76, minus=29.20/831.76),
    "TTJets_pdf": ScalarUncertaintyItem("xsect", 35.06/831.76),
    "TTJets_mass": ScalarUncertaintyItem("xsect", plus=23.18/831.76, minus=22.45/831.76),    
    "TTJets": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.066), # scale, pdf and mass combined (quadratically)

    # Light H+ signal, normalized to TTJets --> use combined TTJets uncertainty
    "TTToHplus": ScalarUncertaintyItem("xsect", plus=0.062, minus=0.066),

    # Heavy H+ signal, what is the effect of this number?
    "HplusTB": ScalarUncertaintyItem("xsect", 0.30),
    
    # Single top, based on http://arxiv.org/abs/1311.0283 and https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_Wt_channel_cross_sect
    "SingleTop_scale":  ScalarUncertaintyItem("xsect", 1.80/71.7),
    "SingleTop_pdf":  ScalarUncertaintyItem("xsect", 3.40/71.7), 

    # W+jets, based on "Total W" on https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
    "WJets_scale":  ScalarUncertaintyItem("xsect", plus=165.7/20508.9, minus=88.2/20508.9), 
    "WJets_pdf":  ScalarUncertaintyItem("xsect", 770.9/20508.9),
    
    # DY, based on "Z/a* (50) on https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive
    "DYJetsToLL_scale": ScalarUncertaintyItem("xsect", plus=13.2/2008.4, minus=7.5/2008.4),
    "DYJetsToLL_pdf": ScalarUncertaintyItem("xsect", 75.0/2008.4), 
    
    # Diboson, values from MIT PAS AN-16-194 (see also https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat13TeVInclusive)
    "Diboson_scale": ScalarUncertaintyItem("xsect", 0.032), 
    "Diboson_pdf": ScalarUncertaintyItem("xsect", 0.044),

    # ttW, values from HIG-17-022 which shows consistency with all other systematics defined here (TTJets, SingleTop, WJets, DY, Diboson, ..)
    "TTW_scale": ScalarUncertaintyItem("xsect", plus=0.13, minus=0.12), 
    "TTW_pdf"  : ScalarUncertaintyItem("xsect", 0.02),  # 2%

    # ttZ, values from HIG-17-022 which shows consistency with all other systematics defined here (TTJets, SingleTop, WJets, DY, Diboson, ..)
    "TTZ_scale": ScalarUncertaintyItem("xsect", plus=0.10, minus=0.12), 
    "TTZ_pdf"  : ScalarUncertaintyItem("xsect", 0.03),  # 2%

    # tttt
#    "TTTT_scale": ScalarUncertaintyItem("xsect", plus=0.10, minus=0.12), 
#    "TTTT_pdf"  : ScalarUncertaintyItem("xsect", 0.03),  # 2%
#    "TTTT"      : ScalarUncertaintyItem("xsect", 0.12), # scale and pdf combined (quadratically)
    
    # MC QCD: we do not trust the MC QCD, therefore 100 % uncertainty
    "QCD": ScalarUncertaintyItem("xsect", 1.00),
    "QCD_Pt20_MuEnriched": ScalarUncertaintyItem("xsect", 1.00),
    
    # default: no uncertainty
    "default": ScalarUncertaintyItem("xsect", 0.00),
}

def getCrossSectionUncertainty(uncertName):
    if uncertName in _crossSectionUncertainty:
        return _crossSectionUncertainty[uncertName]
    if "pseudo" in uncertName:
        return _crossSectionUncertainty["default"]
    # Ok, dataset name not found and not in the known list, give a warning message
    print ShellStyles.WarningLabel()+"Could not find cross section uncertainty for dataset label: %s!%s"%(uncertName,ShellStyles.NormalStyle())
    return _crossSectionUncertainty["default"]

# def getLeptonVetoUncertainty(uncertName):
#     if "pseudo" in uncertName:
#         return ScalarUncertaintyItem("LeptonVeto", 0.00)
#     return ScalarUncertaintyItem("LeptonVeto", 0.002)

def getLeptonVetoUncertainty():
     return ScalarUncertaintyItem("LeptonVeto", 0.02)

def getTauIDUncertainty(isGenuineTau=True):
    if isGenuineTau:
        return ScalarUncertaintyItem("tauID", 0.06)
    else:
        return ScalarUncertaintyItem("tauID", 0.00)

def getLuminosityUncertainty(year="2015"):
    if year=="2012":
        return ScalarUncertaintyItem("lumi", 0.026) # for 8 TeV
    elif year=="2015":
        return ScalarUncertaintyItem("lumi", 0.027) # for 13 TeV 2015, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM
    elif year=="2016":
        return ScalarUncertaintyItem("lumi", 0.025) # for 13 TeV 2016, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiLUM
    else:
        return ScalarUncertaintyItem("lumi", 0.025) # default, here 13 TeV 2016

def getProbabilisticBtagUncertainty():
    return ScalarUncertaintyItem("probBtag", 0.5)

# Note: if majority of sample is genuine taus, set isGenuineTau=true
def getScalarUncertainties(datasetName, isGenuineTau):
    myList = []
    myList.append(getCrossSectionUncertainty(datasetName))
    myList.append(getLeptonVetoUncertainty(datasetName))
    myList.append(getTauIDUncertainty(isGenuineTau))
    myList.append(getLuminosityUncertainty())
    return myList

def getBinningForTetrajetMass(binLevel=0):
    '''
    Binning for H->tb invariant mass histogram 
    tetrajet object = ldg (in pT) trijet  + ldg (in ) free bjet 
    '''
    myBins = []
    if binLevel == -1: #1 bin (counting experiment)
        myBins = [0.0, 3000.0] 
    elif binLevel == 0: #default binning
        for i in range(0, 1000, 50):
            myBins.append(i)
        for i in range(1000, 2000, 100):
            myBins.append(i)
        for i in range(2000, 3000+500, 500):
            myBins.append(i)
    elif binLevel == 1: #finer binning
        for i in range(0, 1000, 25):
            myBins.append(i)
        for i in range(1000, 2000, 50):
            myBins.append(i)
        for i in range(2000, 3000+250, 250):
            myBins.append(i)
    elif binLevel == 2: #even finer binning
        for i in range(0, 1000, 20):
            myBins.append(i)
        for i in range(1000, 2000, 40):
            myBins.append(i)
        for i in range(2000, 3000+200, 200):
            myBins.append(i)
    elif binLevel == 3: #even more finer binning
        print "%sWARNING! This binning will take hours to compute limits!%s" % (ShellStyles.ErrorStyle(), ShellStyles.NormalStyle())
        for i in range(0, 1000, 10):
            myBins.append(i)
        for i in range(1000, 2000, 20):
            myBins.append(i)
        for i in range(2000, 3000+50, 50):
            myBins.append(i)
    elif binLevel == 4: # 20 GeV bins
        for i in range(0, 3000+20, 20):
            myBins.append(i)
    elif binLevel == 5: # 30 GeV bins
        for i in range(0, 3000+30, 30):
            myBins.append(i)
    elif binLevel == 6: # 40 GeV bins
        for i in range(0, 3000+40, 40):
            myBins.append(i)
    elif binLevel == 7: # 100 GeV bins
        for i in range(0, 3000+100, 100):
            myBins.append(i)
    elif binLevel == 8: # 300 GeV bins
        for i in range(0, 3000+300, 300):
            myBins.append(i)
    elif binLevel == 9: # 50 GeV bins
        for i in range(0, 3000+50, 50):
            myBins.append(i)
    elif binLevel == 10:
        for i in range(0, 800, 20):
            myBins.append(i)
        for i in range(800, 1000, 40):
            myBins.append(i)
        for i in range(1000, 1500, 80):
            myBins.append(i)
        for i in range(1500, 2000, 100):
            myBins.append(i)
        for i in range(2000, 3000+200, 200):
            myBins.append(i)
    elif binLevel == 11:
        for i in range(0, 1000+40, 40):
            myBins.append(i)
    elif binLevel == 12: #default binning variation
        for i in range(0, 1000, 20):
            myBins.append(i)
        for i in range(1000, 1500, 100):
            myBins.append(i)
        for i in range(1500, 2000, 200):
            myBins.append(i)
        #for i in range(2000, 3000+500, 500):
        for i in range(2000, 3000, 500):  # Up to 2500
            myBins.append(i)
    elif binLevel == 13: #default binning variation
        for i in range(0, 700, 10):
            myBins.append(i)
        for i in range(700, 1000, 25):
            myBins.append(i)
        for i in range(1000, 1500, 50):
            myBins.append(i)
        for i in range(1500, 2000, 200):
            myBins.append(i)
        for i in range(2000, 2500+250, 250):
            myBins.append(i)
        #for i in range(2500, 3000, 500):  # Up to 2500
        #myBins.append(i)
    else:
        raise Exception(ShellStyles.ErrorStyle() + "Please choose bin-level from -1 to 2" + ShellStyles.NormalStyle())
    return myBins

# Binning for data-driven control plots and final shapes
# Needed to get systematics right for QCD anti-isol. -> isol. systematics
# Format: list of left bin edges; last entry is maximum value
_dataDrivenCtrlPlotBinning = {
    "WeightedCounters": None,
    "NVertices_AfterStandardSelections": None,
    #"Njets*": [3,4,5,6,7,8,9,10],
    "JetPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,1000],
    "JetEta_AfterStandardSelections": [-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5],
    "JetPt_AfterAllSelections": [0,20,30,40,60,70,80,90,100,120,150,200,250,300,400,500,1000],
    "JetEta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "ImprovedDeltaPhiCuts*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "CollinearAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "BackToBackAngularCutsMinimum*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260],
    "MET": [0,20,40,60,80,100,120,140,160,200,250,300,400,500,600,700,800],
    "METPhi": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "METPhiMinusTauPhi": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "MET_AfterAllSelections": [0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,700,800],
#    "MET_AfterAllSelections"  : [i for i in range(0, 100, 10)] + [i for i in range(100, 200, 20)] + [i for i in range(200, 300, 50)] + [i for i in range(300, 700+100, 100)], #HToTB
    "METPhi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "METPhiMinusTauPhi_AfterAllSelections": [0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "TauPlusMETPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,450,500,600,700,800,900,1000],
    "TauPlusMETPt_AfterAllSelections": [0,40,80,120,160,200,240,280,320,360,400,450,500,600,700,800,900,1000],
    "NBjets": [0,1,2,3,4,5,6,7,8],
    "BJetSelection*": [0,1,2,3,4,5,6,7,8],
    "BJetPt": [0,30,50,70,90,110,130,150,200,300,400,500],
    "BJetEta": [-2.5,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.5],
    "BtagDiscriminator": [-1.0,-0.9,0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "NBjets_AfterAllSelections": [0,1,2,3,4,5,6,7,8],
    "BJetPt_AfterAllSelections": [0,20,30,50,70,90,110,130,150,200,300,400,500],
    "BJetEta_AfterAllSelections": [-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5],
    "BtagDiscriminator_AfterAllSelections": [0.0,0.2,0.4,0.5,0.6,0.7,0.8,0.9,1.0],
    "DeltaPhiTauMet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MinDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "TopMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500],
    "TopPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000],
    "WMass": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "WPt": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000],
    "TopMass_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],
    "TopPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],
    "WMass_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,100,120,130,140,160,180,200,250,300],
    "WPt_AfterAllSelections": [0,20,40,60,80,100,150,200,300,500,600,700,800,900,1000],

    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000,1500,2000,3000,4000,5000], #extended to 5000
#    "TransverseMass*": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000,1500], # MIT rebin

#    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800],
#    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800,900,1000,1500,2000,3000,4000,5000], #default extended to 5000
    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,800,10000], #aggressive rebinning to get rid of empty bins
#    "shapeTransverseMass": [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,500,600,700,800,900,1000,1500], # MIT rebin

    "shapeInvariantMass": [0,20,40,60,80,100,120,140,160,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
    "InvariantMass*": [0,20,40,60,80,100,120,140,160,200,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000],
    "SelectedTau_pT_AfterStandardSelections": [0,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_eta_AfterStandardSelections": [-2.5,-2.1,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.1,2.5],
#    "SelectedTau_eta_AfterStandardSelections": [float(x) * 0.1 for x in range(-25, 26)],
    "SelectedTau_phi_AfterStandardSelections": [-3.14,-2.75,-2.36,-1.96,-1.57,-1.18,-0.79,-0.39,0.00,0.39,0.79,1.18,1.57,1.96,2.36,2.75,3.14],
    "SelectedTau_ldgTrkPt_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_Rtau_AfterStandardSelections": [0.70,0.72,0.74,0.75,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00],
    "SelectedTau_Rtau_FullRange_AfterStandardSelections": [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_p_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_LeadingTrackP_AfterStandardSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,170,190,220,250,300,400,500,600,700,800,900,1000],
    "SelectedTau_DecayMode_AfterStandardSelections": None,
    "SelectedTau_Nprongs_AfterStandardSelections": None,
    "SelectedTau_source_AfterStandardSelections": None,
    "SelectedTau_pT_AfterAllSelections": [0,50,60,80,100,150,200,300,400,500,600,700,800,900,1000],
    "SelectedTau_eta_AfterAllSelections": [-2.5,-2.1,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,-0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.1,2.5],
    "SelectedTau_phi_AfterAllSelections": [-3.14,-2.36,-1.57,-0.79,0.00,0.79,1.57,2.36,3.14],
    "SelectedTau_ldgTrkPt_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300,400,500,600,700,800,900,1000],
    "SelectedTau_Rtau_FullRange_AfterAllSelections": [0.0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00],
    "SelectedTau_Rtau_AfterAllSelections": [0.70,0.72,0.74,0.75,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.00],
    "SelectedTau_p_AfterAllSelections": [0,20,40,50,60,70,80,100,150,200,300,500,600,700,800,900,1000],
    "SelectedTau_LeadingTrackP_AfterAllSelections": [0,41,60,80,100,150,200,300,500,600,700,800,900,1000],
    "SelectedTau_DecayMode_AfterAllSelections": None,
    "SelectedTau_Nprongs_AfterAllSelections": None,
    "SelectedTau_source_AfterAllSelections": None,
    "DeltaPhiTauMET_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MinDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "MaxDeltaPhiTauJet_AfterAllSelections": [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180],
    "NVertices_AfterAllSelections": None,
    # HToTB
    "HT_AfterAllSelections"   : [i for i in range(500, 1500, 50)] + [i for i in range(1500, 2000, 100)] + [i for i in range(2000, 3000+200, 200)],
    "MHT_AfterAllSelections"  : [i for i in range(0, 140, 10)] + [i for i in range(140, 240, 20)] + [i for i in range(240, 400, 50)],
    "QGLR_AfterAllSelections" : [float(i)/100.0 for i in range(0, 105, 5)],
    "LdgTrijetPt_AfterAllSelections"        : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "SubldgTrijetPt_AfterAllSelections"     : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "LdgTrijetMass_AfterAllSelections"      : [i for i in range(50, 360, 10)],
    "SubldgTrijetMass_AfterAllSelections"   : [i for i in range(50, 360, 10)],
    "LdgTrijetBjetPt_AfterAllSelections"    : [j for j in range(0, 300, 10)] + [k for k in range(300, 700+40, 40)],
    "SubldgTrijetBjetPt_AfterAllSelections" : [j for j in range(0, 300, 10)] + [k for k in range(300, 700+40, 40)],
    "LdgTrijetBjetEta_AfterAllSelections"   : None,
    "SubldgTrijetBjetEta_AfterAllSelections": None,
    "LdgTrijetBjetBdisc_AfterAllSelections" : None,
    "SubldgTrijetBjetBdisc_AfterAllSelections": None,
    "LdgTrijetDijetPt_AfterAllSelections"   : [j for j in range(0, 400, 10)] + [k for k in range(400, 700+25, 25)],
    "SubldgTrijetDijetPt_AfterAllSelections": [j for j in range(0, 400, 10)] + [k for k in range(400, 700+25, 25)],
    "LdgTrijetDijetMass_AfterAllSelections" : None,
    "SubldgTrijetDijetMass_AfterAllSelections": None,
    "LdgTrijetTopMassWMassRatioAfterAllSelections": None,
    #"TetrajetBjetPt_AfterAllSelections"     : [j for j in range(0, 400, 20)] + [k for k in range(400, 600, 40)] + [k for k in range(600, 900+100, 100)],
    "TetrajetBjetPt_AfterAllSelections"     : [j for j in range(0, 300, 20)] + [k for k in range(300, 500+40, 40)] + [600, 900],
    "TetrajetBjetEta_AfterAllSelections"    : None,
    "LdgTetrajetPt_AfterAllSelections"      : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    "SubldgTetrajetPt_AfterAllSelections"   : [j for j in range(0, 500, 20)] + [k for k in range(500, 700, 50)] + [k for k in range(700, 900+100, 100)],
    #"LdgTetrajetMass_AfterAllSelections"    : getBinningForTetrajetMass(12),
    #"SubldgTetrajetMass_AfterAllSelections" : getBinningForTetrajetMass(12),
    "LdgTetrajetMass_AfterAllSelections"    : getBinningForTetrajetMass(13),
    "SubldgTetrajetMass_AfterAllSelections" : getBinningForTetrajetMass(13),
    "NVertices_AfterAllSelections": [j for j in range(0, 40, 2)] + [j for j in range(40, 60, 5)] + [j for j in range(60, 80+10, 10)],
    "Njets_AfterAllSelections"  : [i for i in range(7, 19, 1)],
    "Jet1Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700, 1000],
    "Jet2Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500, 700], #1000],
    "Jet3Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet4Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300, 400],
    "Jet5Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet6Pt_AfterAllSelections" : [i for i in range(0,300, 20)] + [300],
    "Jet7Pt_AfterAllSelections" : [i for i in range(0,200, 10)],
    "BJet1Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet2Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500, 700],
    "BJet3Pt_AfterAllSelections": [i for i in range(0,300, 20)] + [300, 400, 500],
    "Jet1Eta_AfterAllSelections"  : None,
    "Jet2Eta_AfterAllSelections"  : None,
    "Jet3Eta_AfterAllSelections"  : None,
    "Jet4Eta_AfterAllSelections"  : None,
    "Jet5Eta_AfterAllSelections"  : None,
    "Jet6Eta_AfterAllSelections"  : None,
    "Jet7Eta_AfterAllSelections"  : None,
    "BJet1Eta_AfterAllSelections" : None,
    "BJet2Eta_AfterAllSelections" : None,
    "BJet3Eta_AfterAllSelections" : None,
    "MET_AfterAllSelections"      : [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250,300],
}


# Add EWK fake tau shape definitions
for key in _dataDrivenCtrlPlotBinning.keys():
    if "shape" in key:
        _dataDrivenCtrlPlotBinning[key.replace("shape","shapeEWKFakeTaus")] = _dataDrivenCtrlPlotBinning[key]


def getBinningForPlot(plotName):
    s = plotName.split("/")
    shortName = s[len(s)-1]
    for plot in _dataDrivenCtrlPlotBinning:
        if plot[len(plot)-1] == "*" and plot[:(len(plot)-1)] == shortName[:(len(plot)-1)]:
            return _dataDrivenCtrlPlotBinning[plot]
    if shortName in _dataDrivenCtrlPlotBinning.keys():
        return _dataDrivenCtrlPlotBinning[shortName]
    raise Exception("Cannot find bin specifications for plotname %s! (implemented are: %s)"%(shortName,', '.join(map(str, _dataDrivenCtrlPlotBinning.keys()))))
