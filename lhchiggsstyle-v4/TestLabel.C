
#include "LHCHiggsStyle.h"
#include "LHCHiggsUtils.h"

#include "TCanvas.h"
#include "TPad.h"

void TestLabel()
{

  SetLHCHiggsStyle();

  TCanvas* test = new TCanvas("test","",0,0,800,600);

#ifdef __CINT__
  gROOT->LoadMacro("LHCHiggsUtils.C");
#endif

  LHCHIGGS_LABEL(0.2,0.8); myText(0.34,0.8,1,"Preliminary");

  myText(0.2,0.7,1,"Higgs Invariant Mass");

}


#ifndef __CINT__

int main() { 
  TestLabel();
  gPad->Print("label.png");
  return 0;
}

#endif
