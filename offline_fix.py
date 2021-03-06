#!/usr/bin/env python
import ROOT

f = ROOT.TFile.Open("PersistRecoTuple2.root")
t = f.Get("TupleDstToD0pi_D0ToKpi_PersistReco/DecayTree")

c = ROOT.TCanvas("c1", "before cut", 1024, 768)
c.cd()
t.Draw("Dst_dstar_delta_mass")
c.SaveAs("before.png")

t.Draw(">>evtlist_reject","abs(Dst_pi_P - D0_pi_P) < 0.05")
evtlist_reject = ROOT.gROOT.FindObject("evtlist_reject")
t.Draw(">>evtlist_keep","abs(Dst_pi_P - D0_pi_P) > 0.05")
evtlist_keep = ROOT.gROOT.FindObject("evtlist_keep")

c2 = ROOT.TCanvas("c2", "reject with cut", 1024, 768)
c2.cd()
t.SetEventList(evtlist_reject)
t.Draw("Dst_dstar_delta_mass")
c2.SaveAs("reject.png")

c3 = ROOT.TCanvas("c3", "after cut", 1024, 768)
c3.cd()
t.SetEventList(evtlist_keep)
t.Draw("Dst_dstar_delta_mass")
c3.SaveAs("after.png")
