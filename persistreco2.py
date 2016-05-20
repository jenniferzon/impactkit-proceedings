from Configurables import DaVinci, CombineParticles, DecayTreeTuple, TurboConf, DstConf
from DecayTreeTuple import Configuration
from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand

DstConf().Turbo = True
TurboConf().PersistReco = True

pions = DataOnDemand('Phys/StdAllNoPIDsPions/Particles')
ks0 = CombineParticles('Ks0Topipi',
                        DecayDescriptors=['[KS0 -> pi+ pi+]cc'],
                        CombinationCut=("AM < 320*MeV"), #parent
                        MotherCut="ALL")
ks0_sel = Selection(
    'Sel_Ks0Topipi',
    Algorithm=ks0,
    RequiredSelections=[pions]
)
ks0_selseq = SelectionSequence(
    'SelSeq_Ks0Topipi',
    TopSelection=ks0_sel
)

dtt_ks0 = DecayTreeTuple('TupleKs0Topipi')
dtt_ks0.Inputs = ks0_selseq.outputLocations()
dtt_ks0.Decay = '[KS0 -> ^pi+ ^pi+]CC'
dtt_ks0.addBranches({
    'Ks0': '[KS0 -> pi+ pi+]CC',
    'pi1': '[KS0 -> ^pi+ pi+]CC',
    'pi2': '[KS0 -> pi+ ^pi+]CC'
})

DaVinci().UserAlgorithms = [ks0_selseq.sequence(), dtt_ks0]
DaVinci().DataType = '2016'
DaVinci().EvtMax = 1000
DaVinci().TupleFile = 'PersistRecoTuple_ks0_pipi.root'
