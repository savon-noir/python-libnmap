#!/usr/bin/env python

import unittest
from libnmap.parser import NmapParser

osmatch_v2 = """

    <os>
        <osmatch name="Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, or Windows 8" accuracy="100" line="53077">
          <osclass type="general purpose" vendor="Microsoft" osfamily="Windows" osgen="7" accuracy="100">
              <cpe>cpe:/o:microsoft:windows_7::-</cpe> 
              <cpe>cpe:/o:microsoft:windows_7::sp1</cpe> 
          </osclass>
        </osmatch>
    </os>
"""

osmatch_buggy1 = """
    <os>
        <osmatch name="Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, or Windows 8" accuracy="100" line="53077">
          <osbourne type="black" vendor="Sabbath" osfamily="Metal" osgen="0" accuracy="100">
              <cpe>cpe:/o:microsoft:windows_7::-</cpe> 
              <cpe>cpe:/o:microsoft:windows_7::sp1</cpe> 
          </osclass>
        </osmatch>
    </os>
"""


class TestNmapService(unittest.TestCase):
#    def setUp(self):
    def test_osmatch(self):
        myservice = NmapParser.parse(osmatch_v2)
        myosmatch = myservice.os.osmatch[0]
        self.assetEqual(osmatch.accuracy, 100)
        sname = "Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, or Windows 8"
        self.assetEqual(myosmatch.name, sname)
        self.assetEqual(myosmatch.line, 53077)
        osclass_dict = {
                'type': 'general purpose'
                'vendor': 'Microsoft',
                'osfamily': 'Windows',
                'osgen': '7',
                'accuracy': '100'
        }
        self.assetEqual(myosmatch.osclasses, [osclass_dict])
        self.assertRaises(NmapParserException, NmapParser.parse, osmatch_buggy1)
