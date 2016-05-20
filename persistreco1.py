from Configurables import  DaVinci, DecayTreeTuple, DstConf, TurboConf
from DecayTreeTuple import Configuration

from Configurables import CombineParticles, DaVinci, FilterDesktop

from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand

DstConf().Turbo = True 

#Do not line below when data from 2015

TurboConf().PersistReco=True


turbo_loc = '/Event/Turbo/{0}/Particles'
dz_line = 'Hlt2CharmHadD02KmPipTurbo'

dtt = DecayTreeTuple('TupleD0ToKpi')
dtt.Inputs = [turbo_loc.format(dz_line)]
dtt.Decay = '[D0 -> K- pi+]CC'
dtt.addBranches({
    'D0': '[D0 -> K- pi+]CC'
})

dz=DataOnDemand(turbo_loc.format(dz_line))
pions = DataOnDemand('Phys/StdAllNoPIDsPions/Particles')


dst = CombineParticles('DstToD0pi',
                        DecayDescriptors=['[D*(2010)+ -> D0 pi+]cc'],
                        CombinationCut=("AM - ACHILD(M,1) < 800*MeV"),
                        MotherCut="(VFASPF(VCHI2/VDOF) < 6)") 

dst_sel = Selection(
    'Sel_DstToD0pi',
    Algorithm=dst,
    RequiredSelections=[dz, pions]
)
dst_selseq = SelectionSequence(
    'SelSeq_DstToD0pi',
    TopSelection=dst_sel
)

dtt_dst = DecayTreeTuple('TupleDstToD0pi_D0ToKpi_PersistReco')
dtt_dst.addTupleTool('TupleToolTrackInfo')
dtt_dst.Inputs = dst_selseq.outputLocations()
dtt_dst.Decay = '[D*(2010)+ -> ^(D0 -> ^K- ^pi+) ^pi+]CC'
dtt_dst.addBranches({
    'Dst': '[D*(2010)+ -> (D0 -> K- pi+) pi+]CC',
    'Dst_pi': '[D*(2010)+ -> (D0 -> K- pi+) ^pi+]CC',
    'D0': '[D*(2010)+ -> ^(D0 -> K- pi+) pi+]CC',
    'D0_K': '[D*(2010)+ -> (D0 -> ^K- pi+) pi+]CC',
    'D0_pi': '[D*(2010)+ -> (D0 -> K- ^pi+) pi+]CC',
})

dstar_hybrid = dtt_dst.Dst.addTupleTool('LoKi::Hybrid::TupleTool/LoKi_Dstar')

dstar_hybrid.Variables = {
    'dstar_delta_mass': 'M - CHILD(M,1)',
  }

DaVinci().UserAlgorithms = [dtt, dst_selseq.sequence(), dtt_dst]
DaVinci().DataType ='2016'

DaVinci().EvtMax=1000

DaVinci().TupleFile = 'PersistRecoTuple2.root'


