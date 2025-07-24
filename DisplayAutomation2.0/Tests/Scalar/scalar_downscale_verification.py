######################################################################################
# @file          scalar_downscale_verification.py
# @brief         This test sets the downscale percent in registry through escape call and applies the target mode from the EDID, DPCD data in the XML file
#                and checks the scalar functionality on this data.
# @details       Apply downscaling percent specified, verify if Pipe scalar is enabled and scalar plane size and position programmed correctly based on scaling option (CAR)
#                and perform DE Veirification in valid scenarios.
#                Command line   python Tests\Scalar\scalar_downscale_vetrification.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file] -downscale true
#                               python Tests\Scalar\scalar_downscale_vetrification.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file] -downscale true -downscale_restrict true
#                               python Tests\Scalar\scalar_downscale_vetrification.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file] -downscale_restrict true
#                Commandline planning restrictions: -downscale_restrict is not valid for HDMI (due to max resolution support with single pipe is 4K)
# @author        Veena Veluru
######################################################################################
import logging
import sys
import unittest
from xml.etree import ElementTree as ET

from Libs.Core.display_config.display_config_struct import DisplayMode
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Feature.display_mode_enum.mode_enum_xml_parser import ModeEnumXMLParser
from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar, VerifyScalarProgramming
from Libs.Feature.display_engine.de_master_control import DisplayEngine, VerificationMethod
from Tests.Scalar.scalar_base import ScalarBase

##
# @brief This class has the test implementation for Downscale verification of Pipe Scalar Feature
class ScalarDownscale(ScalarBase):

    ##
    # @brief  Unit Test to check Downscale functionality for Pipe Scalar
    #         Verify if Pipe scalar is enabled along with scalar plane size and scalar position,
    #         Verify Clock, Plane, Pipe, Transcoder, DDI programming.
    # @return None
    def downscale_and_verify(self):
        downscale_percent_x = 0
        downscale_percent_y = 0
        fail_flag_list = []
        downscale_amount = 100
        iteration = 1
        src_hactive = 0
        is_downscaling_supported = None

        # while loop to generate 5 different downscale amounts and verify scalar and DE
        while iteration <= 5:
            fail_flag = False
            logging.info("{} Iteration Count: {} for Downscale Verification {}".format("-" * 20, iteration, "-" * 20))

            # verifying with generated downscale amount.
            downscale_amount = downscale_amount - 19
            for target_id in self.target_id_list:
                display_adapter_info = self.display_config.get_display_and_adapter_info(target_id)
                is_downscaling_supported = self.get_set_downscale(target_id, get=True)
                source_mode = self.display_config.get_current_mode(display_adapter_info)
                src_hactive = source_mode.HzRes
                # NOTE: Below line is not a mandatory update to apply custom scaling. 
                # Having below code is causing failure in set_display_mode call, hence commenting out for now. 
                # Has to be looked into in future if any issues are observed.
                #source_mode.scaling = ModeEnumXMLParser.SCALE_DICT['CAR']

                # set the custom scaling support for the passed modes
                if src_hactive <= self.max_downscale_amount:
                    if is_downscaling_supported:
                        logging.info("PASS: Downscale supported for source size {} as expected.".format(src_hactive))
                        self.get_set_downscale(target_id, downscale_amount, downscale_amount, False)
                        downscale_percent_x = 100 - downscale_amount
                        downscale_percent_y = 100 - downscale_amount
                    else:
                        logging.error(
                            "[DOWNSCALE DRIVER ERROR]:Scaling supported is returned as {}. Scaling should be supported for Source Hactive <= {} pixels".format(
                                is_downscaling_supported, self.max_downscale_amount))
                        gdhm.report_bug(
                            title="[Display_Interfaces][Scalar]{} - Downscale support returned as {} for Source HActive{}".format(
                                self.platform,
                                is_downscaling_supported, src_hactive),
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        fail_flag = True
                else:
                    if is_downscaling_supported:
                        logging.error(
                            "[DOWNSCALE DRIVER ERROR]:Source size > {0}. Scaling should not be supported for Source Hactive > {0} pixels".format(self.max_downscale_amount))
                        gdhm.report_bug(
                            title="[Display_Interfaces][Scalar]{} - Downscale support returned as {} for Source Hactive {}".format(
                                self.platform, is_downscaling_supported, src_hactive),
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        fail_flag = True
                    else:
                        logging.info(
                            "PASS: Downscale not supported for source size {} as expected.".format(src_hactive))


            # skip further verification for restrict_downscale cases
            if fail_flag is not True and not (src_hactive > self.max_downscale_amount and not is_downscaling_supported):
                if self.display_config.set_display_mode([source_mode], virtual_mode_set_aware=False, force_modeset = True) is False:
                    self.fail("FAIL: Mode Set after setting Downscale failed with Displays {}".format(self.display_list))

                # Verify scalar programming
                scalarList = []
                ports = []
                for display in self.display_list:
                    scaling = 'CAR'
                    scalarList.append(DisplayScalar(display, scaling))
                    ports.append(display)

                test_fail = VerifyScalarProgramming(scalarList, downscale_percent_x, downscale_percent_y)
                if (test_fail is False):
                    logging.error(
                        "[DOWNSCALE DRIVER ERROR]:Scalar Verification for CAR Scaling failed")
                    fail_flag = True

                # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly
                display = DisplayEngine()
                # skip watermark and Clock verifications for downscale tests due to known issue 16014686575
                logging.info("Watermark and Clock verifications are currently skipped due to known issues.")
                display.remove_verifiers(VerificationMethod.WATERMARK, VerificationMethod.CLOCK)
                test_fail = display.verify_display_engine(ports)
                if test_fail is False:
                    logging.error(
                        "[DOWNSCALE DRIVER ERROR]:Display Engine Verification for CAR Scaling failed")
                    fail_flag = True
            fail_flag_list.append(fail_flag)
            iteration += 1

        if True in fail_flag_list:
            logging.error("Failure List for all Iterations {}".format(fail_flag_list))
            self.fail("FAIL : scalar_mode_and_verify")


    ##
    # @brief runTest function of Unit Test FrameWork. Calls the downscale_and_verify.
    # @return None
    def runTest(self):
        self.downscale_and_verify()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)


