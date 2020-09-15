'''
DESCRIPTION:
A plotting script that uses as input a nanoAOD (or skimmed nanoAOD) file.
Retrieves events objects as collections and loops over them to do basic 
plots. Light use recommended, heavy use possible but this scipt is not optimised
for that.


USAGE:


EXAMPLES: 



LAST USED: 


TEMPLATES: 

'''
#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def getListOfFiles(dataset="Run2016B-DoubleMuon-NANOAOD-02Apr2020"):
    '''
    dasgoclient --query 'file dataset=/DoubleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD'
    '''
    
    fileLists = {}
    fileLists["Run2016B-DoubleMuon-NANOAOD-02Apr2020"] = ["C4804A85-5EE9-ED4A-8F87-FE23D9A682AE_Skim.root",
                                                          "AACB26B2-3924-3F48-9E27-30FAD0AD092F_Skim.root",
                                                          "9F890C30-18E8-2D42-920F-5BDE836E3B57_Skim.root",
                                                          "96200C93-DA5C-C145-A0E8-FB59D7E584A0_Skim.root",
                                                          "7985E7AF-EC8F-C34D-9848-44A5E3EDE0A2_Skim.root",
                                                          "792E70B0-2715-F24B-A8DE-1327E9F6480B_Skim.root",
                                                          "3D4A9ACB-7ACC-AA4B-A3F1-F300B50D6196_Skim.root",
                                                          "13CBB9A0-5CCA-0347-8C64-1F0A7E652071_Skim.root"]
    if dataset in fileLists.keys():
        return fileLists[dataset]
    else:
        msg = "Cannot find dataset key \"%s\" in dictionary" % (dataset)
        raise Exception(msg)


class ExampleAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self, histFile=None, histDirName=None):
	Module.beginJob(self, histFile, histDirName)
        
        # Pt
        self.hTauPt_LooseTau  = ROOT.TH1F('TauPt_LooseTau' , 'TauPt_LooseTau ; #tau_{h} p_{T} (GeV); Occur', 40,  0.0, 200.0)
        self.hTauEta_LooseTau = ROOT.TH1F('TauEta_LooseTau', 'TauEta_LooseTau; #tau_{h} #eta; Occur'       , 50, -2.5,   2.5)

        self.hTauPt_TightTau  = ROOT.TH1F('TauPt_TightTau' , 'TauPt_TightTau ; #tau_{h} p_{T} (GeV); Occur', 40,  0.0, 200.0)
        self.hTauEta_TightTau = ROOT.TH1F('TauEta_TightTau', 'TauEta_TightTau; #tau_{h} #eta; Occur'       , 50, -2.5,   2.5)
        self.hTauDM_TightTau  = ROOT.TH1F('TauDM_TightTau' , 'TauDM_TightTau ; #tau_{h} p_{T} (GeV); Occur', 12,  0.0,  12.0)

        # Closest muon
        self.hMuonDeltaPt_MinDeltaR    = ROOT.TH1F('MuonDeltaPt_MinDeltaR'   , 'MuonDeltaPt_MinDeltaR   ; p_{T}^{#tau_{h}} - p_{T}^{#mu} (GeV); Occur', 100, -5.0, 5.0)
        self.hMuonDeltaR_MinDeltaR     = ROOT.TH1F('MuonDeltaR_MinDeltaR'    , 'MuonDeltaR_MinDeltaR    ; #DeltaR(#tau_{h}, #mu); Occur', 100, 0.0, 5.0)
        self.hMuonPt_MinDeltaR         = ROOT.TH1F('MuonPt_MinDeltaR'        , 'MuonPt_MinDeltaR        ; #mu p_{T} (GeV); Occur',  40,  0.0, 200.0)
        self.hMuonEta_MinDeltaR        = ROOT.TH1F('MuonEta_MinDeltaR'       , 'MuonEta_MinDeltaR       ; #mu #eta; Occur'       ,  50, -2.5,   2.5)
        self.hMuonDxy_MinDeltaR        = ROOT.TH1F('MuonDxy_MinDeltaR'       , 'MuonDxy_MinDeltaR       ; d_{xy} (cm);Occur' , 200,  0.0,   2.0);
        self.hMuonDz_MinDeltaR         = ROOT.TH1F('MuonDz_MinDeltaR'        , 'MuonDz_MinDeltaR        ; d_{z} (cm);Occur'   , 400,  0.0,  20.0);
        self.hMuonSIP3D_MinDeltaR      = ROOT.TH1F('MuonSIP3D_MinDeltaR'     , 'MuonSIP3D_MinDeltaR     ; SIP_{3D}=|IP/#sigma_{IP}^{3D}|;Occur', 400, 0.0, 20.0);
        self.hMuonMvaID_MinDeltaR      = ROOT.TH1F('MuonMvaID_MinDeltaR'     , 'MuonMvaID_MinDeltaR     ; MVA ID|;Occur', 5, 0.0, 5.0);
        self.hMuonIsPFCand_MinDeltaR   = ROOT.TH1F('MuonIsPFCand_MinDeltaR'  , 'MuonIsPFCand_MinDeltaR  ; is PF cand;Occur', 2, 0.0, 2.0);
        self.hMuonIsTracker_MinDeltaR  = ROOT.TH1F('MuonIsTracker_MinDeltaR' , 'MuonIsTracker_MinDeltaR ; is tracker;Occur', 2, 0.0, 2.0);
        self.hMuonIsGlobal_MinDeltaR   = ROOT.TH1F('MuonIsGlobal_MinDeltaR'  , 'MuonIsGlobal_MinDeltaR  ; is Global;Occur' , 2, 0.0, 2.0);
        self.hMuonJetPtRelv2_MinDeltaR = ROOT.TH1F('MuonJetPtRelv2_MinDeltaR', 'MuonJetPtRelv2_MinDeltaR; jet p_{T}^{rel};Occur', 20, 0.0, 100.0);
        self.hMuonJetRelIso_MinDeltaR  = ROOT.TH1F('MuonJetRelIso_MinDeltaR' , 'MuonJetRelIso_MinDeltaR ; jet rel iso;Occur', 200, 0.0, 20.0);
        self.hMuonPFRelIso03_MinDeltaR = ROOT.TH1F('MuonPFRelIso03_MinDeltaR', 'MuonPFRelIso03_MinDeltaR; PF rel iso ;Occur', 200, 0.0, 20.0);

        hList = []
        hList.append(self.hTauPt_LooseTau)
        hList.append(self.hTauEta_LooseTau)
        #
        hList.append(self.hTauPt_TightTau)
        hList.append(self.hTauEta_TightTau)
        hList.append(self.hTauDM_TightTau)
        #
        hList.append(self.hMuonDeltaPt_MinDeltaR)
        hList.append(self.hMuonDeltaR_MinDeltaR)
        hList.append(self.hMuonPt_MinDeltaR)
        hList.append(self.hMuonEta_MinDeltaR)
        hList.append(self.hMuonDxy_MinDeltaR)
        hList.append(self.hMuonDz_MinDeltaR)
        hList.append(self.hMuonSIP3D_MinDeltaR)
        hList.append(self.hMuonMvaID_MinDeltaR)
        hList.append(self.hMuonIsPFCand_MinDeltaR)
        hList.append(self.hMuonIsTracker_MinDeltaR)
        hList.append(self.hMuonIsGlobal_MinDeltaR)
        hList.append(self.hMuonJetPtRelv2_MinDeltaR)
        hList.append(self.hMuonJetRelIso_MinDeltaR)
        hList.append(self.hMuonPFRelIso03_MinDeltaR)

        # For-loop: All histograms
        for h in hList:
            h.Sumw2()        
            self.addObject(h)
        return

    def getTauVSjetWP(self, WPstring="medium"):
        '''
        DeepTau WPs can be found here: 
        https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
        '''
        tauWPs = {}
        tauWPs["tight"]    = 32 # 2^x5
        tauWPs["medium"]   = 16 # 2^4
        tauWPs["loose"]    = 8  # 2^3
        tauWPs["vloose"]   = 4  # 2^2
        tauWPs["vvloose"]  = 2  # 2^1
        tauWPs["vvvloose"] = 1  # 2^0

        if WPstring in tauWPs.keys():
            #print "%s = %d" % (WPstring, tauWPs[WPstring])
            return tauWPs[WPstring]
        else:
            msg = "Unsupported tau VSjet working point \"%s\"" % (WPstring)
            raise Exception(msg)

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        jets      = Collection(event, "Jet")
        taus      = Collection(event, "Tau")
        tau_p4    = ROOT.TLorentzVector()
        looseTaus = []
        tightTaus = []
        
        # For-loop: All taus        
        for tau in taus:

            bPassVSe    = bool(tau.idDeepTau2017v2p1VSe >= 4)
            bPassVSmu   = bool(tau.idDeepTau2017v2p1VSmu >= 8)
            bPassVSjetL = bool(tau.idDeepTau2017v2p1VSjet >= self.getTauVSjetWP("vloose"))
            bPassVSjetT = bool(tau.idDeepTau2017v2p1VSjet >= self.getTauVSjetWP("medium"))
            bPassEta    = bool(abs(tau.p4().Eta()) < 1.5)
            bPassDM     = bool(tau.decayMode == 0)

            # Apply some fiducial cuts
            if not bool(bPassVSe & bPassVSmu & bPassEta & bPassDM):
                continue

            # Save the deeptau (loose and tight)
            if (bPassVSjetL):
                #print "VSjet = %.3f" % (tau.idDeepTau2017v2p1VSjet)
                looseTaus.append(tau)

            if (bPassVSjetT):
                #print "VSjet = %.3f" % (tau.idDeepTau2017v2p1VSjet)
                tightTaus.append(tau)

	# Events with at least 1 loose tau
        if len(looseTaus) < 1:
            return False

        # Fill histograms
        self.hTauPt_LooseTau.Fill(looseTaus[0].p4().Pt()) 
        self.hTauEta_LooseTau.Fill(looseTaus[0].p4().Eta()) 


	# Events with at least 1 tight tau
        if len(tightTaus) < 1: 
            return False

        # Calculate minimum dR(ldg tau, muon)
        tau_p4  = looseTaus[0].p4()
        dPt_min = 999.9
        dR_min  = 999.9
        muonPt_min         = -1.0
        muonEta_min        = -1.0
        muonDxy_min        = -1.0
        muonDz_min         = -1.0
        muonSIP3D_min      = -1.0
        muonMvaID_min      = -1.0
        muonIsPFCand_min   = -1.0
        muonIsTracker_min  = -1.0
        muonIsGlobal_min   = -1.0
        muonJetIdIndex_min = -1.0
        muonJetRelIso_min  = -1.0
        muonPFRelIso03_min = -1.0

        # For-loop: All muons
        for mu in muons:
            # FIXME - add some quatlity cuts!  (e.g. loose muon)
            dR = tau_p4.DeltaR(mu.p4())
            if dR < dR_min:
                dR_min  = dR
                dPt_min = tau_p4.Pt() - mu.p4().Pt()
                muonPt_min  = mu.p4().Pt()
                muonEta_min = mu.p4().Eta()
                muonDxy_min = mu.dxy
                muonDz_min  = mu.dz
                muonSIP3D_min = mu.sip3d
                muonMvaID_min = mu.mvaId
                muonIsPFCand_min   = mu.isPFcand
                muonIsTracker_min  = mu.isTracker
                muonIsGlobal_min   = mu.isGlobal
                muonJetPtRelv2_min = mu.jetPtRelv2
                muonJetRelIso_min  = mu.jetRelIso
                muonPFRelIso03_min = mu.pfRelIso03_all

        #
        self.hTauPt_TightTau.Fill(tightTaus[0].p4().Pt()) 
        self.hTauEta_TightTau.Fill(tightTaus[0].p4().Eta()) 
        self.hTauDM_TightTau.Fill(tightTaus[0].decayMode)
        #
        self.hMuonPt_MinDeltaR.Fill(muonPt_min)
        self.hMuonEta_MinDeltaR.Fill(muonEta_min)
        self.hMuonDeltaPt_MinDeltaR.Fill(dPt_min)
        self.hMuonDeltaR_MinDeltaR.Fill(dR_min)
        self.hMuonDxy_MinDeltaR.Fill(muonDxy_min)
        self.hMuonDz_MinDeltaR.Fill(muonDz_min)
        self.hMuonSIP3D_MinDeltaR.Fill(muonSIP3D_min)
        self.hMuonMvaID_MinDeltaR.Fill(muonMvaID_min)
        self.hMuonIsPFCand_MinDeltaR.Fill(muonIsPFCand_min)
        self.hMuonIsTracker_MinDeltaR.Fill(muonIsTracker_min)
        self.hMuonIsGlobal_MinDeltaR.Fill(muonIsGlobal_min)
        self.hMuonJetPtRelv2_MinDeltaR.Fill(muonJetPtRelv2_min)
        self.hMuonJetRelIso_MinDeltaR.Fill(muonJetRelIso_min)
        self.hMuonPFRelIso03_MinDeltaR.Fill(muonPFRelIso03_min)


        return True


#================================================================================================  
# Definitions
#================================================================================================  
#preselection = "Tau_pt[0] > 20 && fabs(Tau_eta[0]) < 1.5 && Tau_decayMode[0] == 0"
#preselection = "Tau_pt[0] > 20 && fabs(Tau_eta[0]) < 1.5 && Tau_decayMode[0] == 1"
#
#preselection = "Tau_pt > 20 && fabs(Tau_eta) < 1.5 && Tau_decayMode == 0"
preselection = "Tau_pt > 20 && Tau_decayMode == 0"
preselection+= "&& @Muon_pt.size() >= 2"
#preselection+= "&& @Tau_pt.size() >= 1"

#files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]

p = PostProcessor(".", getListOfFiles(), cut=preselection, branchsel=None, modules=[ExampleAnalysis()], noOut=True, histFileName="tauFR.root", histDirName="plots")
p.run()
