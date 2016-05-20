import sys

import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import DaVinci

dv = DaVinci()
dv.DataType = '2016'

# Pass file to open as first command line argument
inputFiles = [sys.argv[-1]]
IOHelper('ROOT').inputFiles(inputFiles)

appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

appMgr.run(1)
evt.dump()

def nodes(evt, node=None):
    """List all nodes in `evt`"""
    nodenames = []

    if node is None:
        root = evt.retrieveObject('')
        node = root.registry()

    if node.object():
        nodenames.append(node.identifier())
        for l in evt.leaves(node):
            # skip a location that takes forever to load
            # XXX How to detect these automatically??
            if 'Swum' in l.identifier():
                continue

            temp = evt[l.identifier()]
            nodenames += nodes(evt, l)

    else:
        nodenames.append(node.identifier())

        return nodenames

    def advance(Hlt_line):
        """Advance until stripping decision is true, returns
        number of events by which we advanced"""
        n = 0
        while True:
            appMgr.run(1)
            n += 1
            reports = evt['Hlt2/DecReports']
            report = reports.decReport('{0}Decision'.format(Hlt_line))
            if report is False:
                print 'Line does not exist'
    #            break
            if report.decision():
                print 'Positive decision'
                break
        return n
