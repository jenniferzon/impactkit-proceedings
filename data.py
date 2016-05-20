
from GaudiConf import IOHelper
from Configurables import DaVinci

prefix = 'root://eoslhcb.cern.ch/'
file_name = '/eos/lhcb/user/r/raaij/Impactkit/00051318_00000509_1.turbo.mdst'

IOHelper('ROOT').inputFiles([prefix+file_name])

