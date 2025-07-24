########################################################################################################################
# @file         async_flips_stream.py
# @brief        Basic test to verify there is no TDR or underrun while running the streams.
#               * Apply display configuration and verify.
#               * Play the streams based on the command line parameters.
#               * Verify for TDR or underrun.
# @author       Ilamparithi Mahendran
########################################################################################################################
import time
import xml.etree.ElementTree as ET
import logging
import os
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Flips.ImmediateFlips import async_flips_base
from Libs.Core.logger import gdhm

##
# @brief        Contains function to check various async flips stream
class AysnFlipsStreams(async_flips_base.AsyncFlipsBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Parse the async_stream.xml to get the command line for the input stream
        xml_tree = ET.parse("%s\AsyncFlips\\async_streams.xml" % self.flip_stream_artifactory)
        if not xml_tree:
            gdhm.report_bug(
                title="[Immediate Flips]The streams file is not found. Exiting the test",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            logging.info("The streams file is not found. Exiting the test")
            self.fail()
        stream_info = xml_tree.getroot()
        stream = stream_info.find("./Stream[@name='%s']" % self.cmd_line_param['STREAM'][0])

        command_line = stream.find("./Command").text

        ##
        # For all configs in display config list, run the tests
        for config_list in self.display_config_list:
            if not self.display_config.set_display_configuration_ex(config_list[0], config_list[1]):
                self.fail("Display Configuration failed")

            os.system("%s\AsyncFlips\GfxBench\\x64\GfxPlayer.exe %s %s\AsyncFlips\%s\capture.lcs2"
                      % (self.flip_stream_artifactory, command_line, self.flip_stream_artifactory,
                         self.cmd_line_param['STREAM'][0]))

            time.sleep(5)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
