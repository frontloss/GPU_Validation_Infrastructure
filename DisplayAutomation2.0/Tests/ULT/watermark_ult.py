######################################################################################
# \file
# \addtogroup PyLibs_DisplayWatermark
# \brief ULT module for DisplayWatermark
# \author   Kumar V,Arun
######################################################################################
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_watermark.watermark import *


class WaterMarkBasicTest(unittest.TestCase):

    def runTest(self):
        test1 = DisplayWatermark()
        status = test1.verify_watermarks()
        if status:
            logging.info('Watermark ULT pass')
        else:
            logging.error('Watermark ULT fail')
            self.fail("Watermark ULT fail")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
