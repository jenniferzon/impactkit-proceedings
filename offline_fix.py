#!/usr/bin/env python
import ROOT

f = ROOT.TFile.Open("PersistRecoTuple2.root")
t = f.Get("TupleDstToD0pi_D0ToKpi_PersistReco/DecayTree")

c = ROOT.TCanvas("c1", "before cut", 1024, 768)
c.cd()
t.Draw("Dst_dstar_delta_mass")
c.SaveAs("before.png")

t.Draw(">>evtlist","abs(Dst_pi_P - D0_pi_P) > 0.05")
evtlist = ROOT.gROOT.FindObject("evtlist")
t.SetEventList(evtlist)

c2 = ROOT.TCanvas("c2", "after cut", 1024, 768)
c2.cd()
t.Draw("Dst_dstar_delta_mass")
c2.SaveAs("after.png")
