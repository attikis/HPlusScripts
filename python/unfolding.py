#!/usr/bin/env python
import ROOT, math, os, sys, re, random
import numpy as np
from subprocess import call

def CreateLegend(xmin=0.55, ymin=0.75, xmax=0.85, ymax=0.85):
    leg = ROOT.TLegend(xmin, ymin, xmax, ymax)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.040)
    leg.SetTextFont(42)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    return leg

def SaveCanvas(canvas, saveName, saveFormats=["png", "pdf", "C"]):
    for ext in saveFormats:
        canvas.SaveAs("/afs/cern.ch/user/a/attikis/public/html/%s.%s" % (saveName, ext) )
    return

def makeObs():
    '''
    '''
    global shapes
    shapes= {}
    hData = ROOT.TH1D("Data","", 10, 0.0, 10.0)
    hData.Sumw2()

    for xtrue,xreco,xmass in makeSignalTree(1) + makeBackgroundTree(1):
        #print "DEBUG","filling data", xtrue, xreco, xmass
        hData.Fill(xreco)
        #shapes
        recobin=hData.FindBin(xreco)
        if(recobin>0 and recobin< hData.GetNbinsX()+1):
            #no over/underflows
            BookAndFill(shapes,"DataObs_Reco_%d"%recobin,100,0,10,xmass)## mass
            removeOverflows(hData)
    return hData

def removeOverflows(h):
    '''
    overflows and underflows are there to mimic efficiency. make sure they are removed
    '''
    #print "=== removeOverflows()"

    if h.InheritsFrom("TH2D"):
        h.SetBinContent(0,0,0)
        h.SetBinContent(h.GetNbinsX()+1,h.GetNbinsY()+1,0)
        for x in range(0,h.GetNbinsX()+1):
            h.SetBinContent(x,0,0)
            h.SetBinContent(x,h.GetNbinsY()+1,0)
        for y in range(0,h.GetNbinsY()+1):            
            h.SetBinContent(0,y,0)
            h.SetBinContent(h.GetNbinsX()+1,y,0)
        return
    if h.InheritsFrom("TH1D"):
        h.SetBinContent(0,0)
        h.SetBinContent(h.GetNbinsX()+1,0)
        return

def BookAndFill(d,name, nBins,xmin,xmax,value,weight=1.):
    #print "=== BookAndFill()"
    if name not in d:
        d[name]=ROOT.TH1D(name,name,nBins,xmin,xmax)
    d[name].Fill(value,weight)

    return

def makeSignalTree(k=1):
    '''
    Create signal shapes and templates. x is ~ pT from 0 to 10 GeV (say)
    A second dimension is added (~mass). (mass range is yet 0 to 10)

    Signal is distributed as exponential in the range 0-10 and parameter of 8. 
    Signal resolution has a lognormal component (log of x is normally distributed) 
    and a gaussian component with sigmas=0.1,.1
    '''
    # We expect 10 000 signal events
    Nexp = 10000*k
    Nobs = ROOT.gRandom.Poisson(Nexp)
    #truth function is: exp(-c*pt)
    #resolution function is: ptreco=ptgen*exp(gaus(0,1))+gaus(0,1) 
    sigma1 = 0.1
    sigma2 = 0.1
    events = []
    print "-> Generating ",Nobs, "events for signal"
    for ievt in range(0,Nobs):
        xtrue = -1
        while xtrue<0 or xtrue>10: xtrue=ROOT.gRandom.Exp(8.0)
        xreco = xtrue*ROOT.TMath.Exp(ROOT.gRandom.Gaus(0,sigma1)) + ROOT.gRandom.Gaus(0,sigma2)
        xmass = ROOT.gRandom.Gaus(5, 1.0)
        events.append( (xtrue, xreco, xmass) )
    return events

def makeBackgroundTree(k=1):
    '''
    as signal, but no smearing assume is alerady reco level

    Background is uniformly distributed in 0-10
    '''
    # We expect 10 000 background events
    Nexp   = 10000*k
    Nobs   = ROOT.gRandom.Poisson(Nexp)
    events = []
    print "-> Generating ",Nobs, "events for background"
    for ievt in range(0,Nobs):
        xtrue=-1
        while xtrue<0 or xtrue>10: xtrue=ROOT.gRandom.Uniform(0,10)
        # xtrue = xreco for background
        xmass = ROOT.gRandom.Uniform(0,10)
        events.append( (xtrue, xtrue, xmass) )
    return events

def makeResponseMatrix():
    #print "=== makeResponseMatrix()"
    global shapes
    hGen  = ROOT.TH1D("GEN" ,"GEN" , 10, 0.0, 10.0)
    hReco = ROOT.TH1D("RECO","RECO", 10, 0.0, 10.0)
    hBkg  = ROOT.TH1D("Background","Background", 10, 0.0, 10.0)
    hResp = ROOT.TH2D("Response","Response Matrix", 10, 0.0, 10.0, 10, 0.0, 10.0)

    nMC = 10.0
    for xtrue,xreco,xmass in makeSignalTree(nMC):
        #print "filling sig", xtrue, xreco, xmass
        hReco.Fill(xreco, 1./nMC)
        hGen.Fill(xtrue , 1./nMC)
        hResp.Fill(xreco, xtrue, 1./nMC)

        recobin=hData.FindBin(xreco)
        genbin=hGen.FindBin(xtrue) ## this should be ok
        if(recobin>0 and recobin< hData.GetNbinsX()+1):
            #no over/underflows
            BookAndFill(shapes,"Reco_%d_Gen_%d"%(recobin,genbin),100,0,10,xmass,1./nMC)
            
    for xtrue,xreco,xmass in makeBackgroundTree(nMC): 
        hBkg.Fill(xreco,1./nMC)
        if(recobin>0 and recobin< hData.GetNbinsX()+1):
            #no over/underflows
            BookAndFill(shapes,"Bkg_%d"%(recobin),100,0,10,xmass,1./nMC)

    #hReco.Add(hBkg)
    removeOverflows(hGen)
    removeOverflows(hReco)
    removeOverflows(hResp)
    removeOverflows(hBkg)
    return hGen,hReco,hResp,hBkg

def makeRooUnfold():
    '''
    https://gitlab.cern.ch/RooUnfold/RooUnfold/blob/master/README.md
    '''
    # Check if RooUnfold exists locally
    if not os.path.isdir("RooUnfold"):
        call("git clone https://gitlab.cern.ch/RooUnfold/RooUnfold.git", shell=True)
    call("cd RooUnfold && make", shell=True)

    # Check if code is compilered already or not
    if not os.path.isfile("RooUnfold/libRooUnfold.so"):makeRooUnfold()
    ROOT.gSystem.Load("RooUnfold/libRooUnfold.so")
    return

def main():

    #init random engine
    random.seed = os.urandom(10)
    myseed=random.randint(0,999999)
    myseed=123001
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetBatch(ROOT.kTRUE)

    gc = [] #?
    hList = []
    # Make them global for further usage
    print "-> Setting seed", myseed
    ROOT.gRandom.SetSeed(myseed)
    global hData

    # The data will only see the reconstruction part contaminated w/ backgroung
    hData = makeObs()

    # The response matrix contains all the information separately
    hGen,hReco,hResp,hBkg = makeResponseMatrix()
    gc.extend([hData, hGen, hReco, hResp, hBkg])
    
    hRecoTot=hReco.Clone("Signal + Background") 
    hRecoTot.Add(hBkg)
    hList.extend([hData, hGen, hReco, hRecoTot, hBkg])

    print "-> Using RooUnfold" 
    makeRooUnfold()
    
    # 
    canvas = ROOT.TCanvas()
    leg = CreateLegend(0.15, 0.15, 0.45, 0.40)
    canvas.cd()
    logy = True
    if logy:
        canvas.SetLogy()

    colours = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kGray]
    mStyles = [ROOT.kFullCircle, 1, 1, 1, 1]
    mSizes  = [1.2, 0.0, 0.0, 0.0, 0.0]
    lStyles = [ROOT.kSolid, ROOT.kSolid, ROOT.kSolid, ROOT.kSolid, ROOT.kDashed] 
    fStyles = [0, 0, 0, 3001, 0] 
    
    # For-loop: all graphic content
    for i, h in enumerate(hList, 0):
        
        # Customise histos
        h.SetLineWidth(3)
        h.SetLineColor( colours[i] )        
        h.SetFillStyle( fStyles[i] ) 
        h.SetLineStyle( lStyles[i] )
        h.SetMarkerSize( mSizes[i] )
        h.SetMarkerStyle( mStyles[i] )
        h.SetMarkerColor(colours[i])

        # Add legend entry
        leg.AddEntry(h, h.GetName(), "lp")

        # Set y-max
        if logy:
            h.SetMinimum(500)
        else:
            h.SetMinimum(0)

        # Set axes titles
        h.GetXaxis().SetTitle("p_{T} (GeV)")
        h.GetYaxis().SetTitle("Events")

        if i==0:
            h.Draw()
        else:
            h.Draw("same HIST9")

    # Draw the legend and re-draw data histo to bring to front. Save the canvas
    leg.Draw()
    hList[0].Draw("same") 
    SaveCanvas(canvas, "unfolding_1")
    

    hList   = []
    leg     = CreateLegend(0.15, 0.15, 0.45, 0.30)
    R       = ROOT.RooUnfoldResponse(hRecoTot, hGen, hResp)
    unfold  = ROOT.RooUnfoldInvert(R, hData)
    hUnfold = unfold.Hreco()
    hUnfold.SetName("Data (unfolded)")
    hUnfold.SetTitle("Unfolded")
    hList.extend([hUnfold, hGen])

    # For-loop: all graphic content
    for i, h in enumerate(hList, 0):
        
        # Customise histos
        h.SetLineWidth(3)
        h.SetLineColor( colours[i] )        
        h.SetFillStyle( fStyles[i] ) 
        h.SetLineStyle( lStyles[i] )
        h.SetMarkerSize( mSizes[i] )
        h.SetMarkerStyle( mStyles[i] )
        h.SetMarkerColor(colours[i])

        # Add legend entry
        leg.AddEntry(h, h.GetName(), "lp")

        # Set y-max
        if logy:
            h.SetMinimum(100)
        else:
            h.SetMinimum(0)

        # Set axes titles
        h.GetXaxis().SetTitle("p_{T} (GeV)")
        h.GetYaxis().SetTitle("Events")

        if i==0:
            h.Draw()
        else:
            h.Draw("same HIST9")

    # Draw the legend and re-draw data histo to bring to front
    leg.Draw()
    SaveCanvas(canvas, "unfolding_2")
    
    # Create canvas 
    canvas = ROOT.TCanvas()
    canvas.cd()
    hResp.Draw("COLZ")
    hResp.GetXaxis().SetTitle("p_{T}^{reco} (GeV)")
    hResp.GetYaxis().SetTitle("p_{T}^{true} (GeV)")
    SaveCanvas(canvas, "responseMatrix")
    return

                        
if __name__ == '__main__':

    print "=== Calling main()"
    main()
