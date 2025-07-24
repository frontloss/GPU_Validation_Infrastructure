######################################################################################
# @file          scalar_unit_tests.py
# @brief         This test has a set of unit tests to validate various restrictions on Source sizes as per BSpec and verify Scalar Programing
# Command line   python Tests\Scalar\scalar_unit_tests.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file] -unit_test 0x01
#                python Tests\Scalar\scalar_unit_tests.py -[hdmi_*/dp_*] -dispconfig [single/dual] -xml [XML file] -unit_test 0x03
#
# @author        Veena Veluru
######################################################################################
import logging

from Libs.Feature.display_engine.de_base.display_scalar import DisplayScalar, VerifyScalarProgramming
from Libs.Feature.display_engine.de_master_control import DisplayEngine
from Tests.PowerCons.Modules import common
from Tests.Scalar.scalar_base import *


##
# @brief This class implements the functions for Pipe Source Size limits verification
class ScalarUnitTest(ScalarBase):
    fail_flag = []
    mode_flag = False

    ##
    # @brief  Function to validate Pipe Source Size Limits as per BSpec.
    # @details If successful,
    #         Verify if Pipe scalar is enabled along with scalar plane size and scalar position,
    #         Verify Clock, Plane, Pipe, Transcoder, DDI programming.
    # @param[in]    verification_tag: str
    #                    supported tags are PipeSrcSize and PipeSize
    # @return None
    def validate_bspec_srcsz(self, verification_tag):
        mode_list = []
        sup_platform = []
        is_supported_mode_list = []
        self.enumerated_displays = self.display_config.get_enumerated_display_info()

        logging.info(" Test: Validate BSPEC Restriction '{}' ".format(verification_tag).center(common.MAX_LINE_WIDTH, "*"))
        for plat_temp in self.platform_xml:
            logging.info("plat_temp.tag: {}, plat_temp.get('Name') {}: {} self.sku: {},{}".format(plat_temp.tag, plat_temp.get('Name'), self.platform, self.sku,  plat_temp.get('SKU')))
            if ((plat_temp.tag == "Platform") and (self.platform == plat_temp.get('Name'))
                    and (self.sku == plat_temp.get('SKU'))):                
                sup_platform.append(plat_temp.get('Name'))
                logging.info("v: {}".format(sup_platform))
                for index in range(0, len(self.display_list)):
                    target_id = self.display_config.get_target_id(self.display_list[index],
                                                                  self.enumerated_displays)
                    modes_list = plat_temp.find(verification_tag)
                    for modeInstance in modes_list:
                        if (modeInstance.tag == "EDIDInstance"):
                            mode = DisplayMode()
                            mode.targetId = target_id
                            mode.HzRes = int(modeInstance.get('HActive'))
                            mode.VtRes = int(modeInstance.get('VActive'))
                            mode.refreshRate = int(modeInstance.get('RefreshRate'))
                            mode.BPP = 4  # Assuming RGB888
                            mode.rotation = 1
                            mode.scanlineOrdering = 1
                            mode.scaling = self.scale_dict[modeInstance.get('Scaling')]
                            mode_list.append(mode)
                            is_supported_mode_list.append(modeInstance.get('Supported'))

                    self.scalar_config_dict[self.display_list[index]] = mode_list
                    break

        # If platform supported is not part of XML file, fail the test
        if self.platform not in sup_platform:
            gdhm.report_bug(
                title="[Display_Interfaces][Scalar]{} - Platform is missing from Scalar XML".format(
                    self.platform),
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("FAIL : XML file : %s specified is not valid for the %s platform ; %s" % (
            self.xml_file, self.platform, sup_platform))

        for scalarkey, scalarvalue in self.scalar_config_dict.items():
            for scalar in range(0, len(scalarvalue)):
                logging.info(
                    "Source Mode to Verify {} - Target ID {}: {}".format(scalar+1, scalarvalue[scalar].targetId,
                                                              scalarvalue[scalar].to_string(
                                                                  self.enumerated_displays)))
                self.mode_flag = False
                supported_mode_list = self.display_config.get_all_supported_modes([scalarvalue[scalar].targetId],
                                                                                  False)
                for supported_key, supported_value in supported_mode_list.items():
                    for sup in range(0, len(supported_value)):
                        logging.debug(
                            "OS Supported Modes - TargetID : %s - " % (supported_value[sup].targetId) +
                            supported_value[
                                sup].to_string(self.enumerated_displays))
                        if is_supported_mode_list[scalar] in ['True']:
                            if self.compare_modes(scalarvalue[scalar], supported_value[sup]):
                                logging.info("PASS : Scalar Mode is Supported - TargetID : %s - "
                                             % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                    self.enumerated_displays))
                                self.mode_flag = True
                                # apply the user requested mode
                                # To Force PLANE Scalar set "virtual_mode_set_aware" parameter as True (Default).
                                # To Force PIPE Scalar set "virtual_mode_set_aware" parameter as False.
                                status = self.display_config.set_display_mode(mode_list=[scalarvalue[scalar]],
                                                                              virtual_mode_set_aware=False,
                                                                              enumerated_displays=None)
                                if status is False:
                                    self.fail("FAIL : Failed to apply display mode. Exiting ...")
                                else:
                                    logging.info("INFO : Requested Mode is successfully applied")
                                    # Test whether clock, plane, pipe, transcoder, DDI are programmed correctly in case of a non DSC Panel
                                    ports = []
                                    ports.append(scalarkey)
                                    display = DisplayEngine()
                                    if not display.verify_display_engine(ports):
                                        self.fail_flag.append(True)
                                break
                            else:
                                continue
                        # Driver should not support the Scalar Mode
                        else:
                            if self.compare_modes(scalarvalue[scalar], supported_value[sup]):
                                logging.warning("WARN: Driver enumerated the Mode that is not supported as per "
                                                "BSPEC\n {}".format(supported_value[
                                                 sup].to_string(self.enumerated_displays)))
                                self.mode_flag = True
                                break
                            else:
                                continue

                if is_supported_mode_list[scalar] in ['True'] and not self.mode_flag:
                    self.fail_flag.append(True)
                    logging.error(
                        "Mode [{} X {}] supported by BSPEC is not supported by Driver for TargetID {} ".format(
                            scalarvalue[scalar].HzRes,
                            scalarvalue[scalar].VtRes, scalarvalue[scalar].targetId))
                    gdhm.report_bug(
                        title="[Display_Interfaces][Scalar]Mode [{} X {}] supported by BSPEC is not supported by Driver".format(
                            scalarvalue[scalar].HzRes,
                            scalarvalue[scalar].VtRes),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )

                if is_supported_mode_list[scalar] in ['False']:
                    if not self.mode_flag:
                        logging.info(
                            "PASS : Scalar Mode(not Supported as per BSPEC) is not Supported by Driver- TargetID : %s - "
                            % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                self.enumerated_displays))
                    else:
                        logging.warning("WARN: Checking if driver is able to set the mode that is unsupported by BSPEC!")
                        status = self.display_config.set_display_mode(mode_list=[scalarvalue[scalar]],
                                                                      virtual_mode_set_aware=False,
                                                                      enumerated_displays=None)
                        if status:
                            self.fail_flag.append(True)
                            logging.error(
                                "Driver applied a mode that is not valid as per BSPEC for Target Scalar Mode is Supported - TargetID : %s - "
                                % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                    self.enumerated_displays))
                            gdhm.report_bug(
                                title="[Display_Interfaces][Scalar]Driver applied a mode that is not valid as per BSPEC, Mode: {}".format(
                                    self.platform),
                                problem_classification=gdhm.ProblemClassification.OTHER,
                                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                        else:
                            self.fail_flag.append(True)
                            logging.error(
                                "Driver supports a mode that is not valid as per BSPEC for Target Scalar Mode is Supported - TargetID : %s - "
                                % (scalarvalue[scalar].targetId) + scalarvalue[scalar].to_string(
                                    self.enumerated_displays))
                            gdhm.report_bug(
                                title="[Display_Interfaces][Scalar]Driver supports a mode that is not valid as per BSPEC, Mode: {}".format(
                                    self.platform),
                                problem_classification=gdhm.ProblemClassification.OTHER,
                                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
        return self.fail_flag

    ##
    # @brief    This Test method helps to perform all the test steps.
    # @return   None
    def runTest(self):
        test_fail = {}

        if self.controlFlag.data.pipe_srcsz:
            unit_test_fail = self.validate_bspec_srcsz('PipeSrcSize')
            test_fail.update({'PipeSrcSize': unit_test_fail})
        if self.controlFlag.data.pipe_sz:
            unit_test_fail = self.validate_bspec_srcsz('PipeSize')
            test_fail.update({'PipeSize': unit_test_fail})

        logging.info("Test Failure dict values for all unit tests: {}".format(test_fail))

        for key, value in test_fail.items():
            if True in value:
                self.fail("FAIL : Scalar Unit Tests")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
