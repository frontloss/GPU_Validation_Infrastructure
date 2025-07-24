##
# @file nnis_scaling_modeset_custommode.py
# @brief The Script apply different custom added mode and verify NN/IS scaling applied or not.
# @details  script takes NN or IS scaling and Plane or Pipe scalar as input.
#        *  parse the XML which fetches the EDID/DPCD from XML and fetch the scalar mode to be applied
#        *  Add the custom mode parse from xml
#        *  Apply Custom added mode and verify NN/IS scaling programming.
# @author Nainesh Doriwala

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.wrapper.driver_escape_args import CustomModeOperation
from Tests.NNIS_Scaling.nnis_scaling_base import *


##
# @brief It contains methods to ensure driver is programing properly when we enable NN/ IS scaling with custom mode
class NNISScalingCustomMode(ScalingBase):
    custom_mode_dict = {}
    skip_plane_scaler = False

    ##
    # @brief Function to parse xml given in command line.
    # @return None
    def parse_xml(self):
        logging.info("parsing xml to get custom mode")
        sup_platform = []
        tree = ET.parse(self.xml_file)

        Platform = tree.getroot()
        for plat_temp in Platform:
            if plat_temp.tag == "Platform" and self.platform == plat_temp.get('Name'):
                sup_platform.append(plat_temp.get('Name'))
                # Fetch the EDID/DPCD from XML and fetch the scalar mode to be applied, copy to self.scalar_config_dict
                for index in range(0, len(self.display_list)):
                    modes_list = []
                    enumerated_displays = self.display_config.get_enumerated_display_info()
                    # Get Target-ID for connected port
                    for display_index in range(enumerated_displays.Count):
                        enum_port = (CONNECTOR_PORT_TYPE(
                            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType)).name
                        if enum_port == self.display_list[index]:
                            targetId = enumerated_displays.ConnectedDisplays[display_index].TargetID

                            display = self.display_list[index].split("_")
                            mode_list = plat_temp.find(display[0] + "CustomModes")
                            for modeInstance in mode_list:
                                if modeInstance.tag == "EDIDInstance":
                                    mode = DisplayMode()
                                    mode.targetId = targetId
                                    mode.HzRes = int(modeInstance.get('HActive'))
                                    mode.VtRes = int(modeInstance.get('VActive'))
                                    mode.refreshRate = int(modeInstance.get('RefreshRate'))
                                    mode.BPP = 4  # Assuming RGB888
                                    mode.rotation = 1
                                    mode.scanlineOrdering = 1
                                    mode.scaling = self.SCALE_DICT[modeInstance.get('Scaling')]
                                    modes_list.append(mode)

                            self.custom_mode_dict[self.display_list[index]] = modes_list
                            break

        # If platform supported is not part of XML file, fail the test
        if self.platform not in sup_platform:
            logging.error(
                "ERROR : XML file : %s specified is not valid for the %s platform" % (self.xml_file, self.platform))
            gdhm.report_bug(
                title="[NN/IS] {0} Platform not enable in XML ".format(self.platform),
                problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail()

    ##
    # @brief adds custom mode to driver for each display planned in command line
    # @return None
    def add_and_verify_custom_mode(self):

        logging.info("parsing xml to get custom mode")
        for scalarkey, scalarvalue in self.custom_mode_dict.items():
            for index in range(0, len(scalarvalue)):
                logging.debug("Adding custom mode: {} X {} for targetID: {}".format(scalarvalue[index].HzRes,
                                                                                    scalarvalue[index].VtRes,
                                                                                    scalarvalue[index].targetId))
                if driver_escape.add_custom_mode(scalarvalue[index].targetId, scalarvalue[index].HzRes,
                                                 scalarvalue[index].VtRes) is True:
                    logging.info("Added custom mode: {} X {} for targetID: {}".format(scalarvalue[index].HzRes,
                                                                                      scalarvalue[index].VtRes,
                                                                                      scalarvalue[index].targetId))
                else:
                    gdhm.report_bug(
                        title="[NN/IS] Escape call failed : add_custom_mode()",
                        problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(f"Escape call failed : add_custom_mode() for {scalarvalue[index].targetId}")

                custom_mode_args = CustomModeArgs()
                custom_mode_args.ModeOperation = CustomModeOperation.CUSTOM_MODE_GET_MODES.value
                custom_mode_args.target_id = scalarvalue[index].targetId
                status, custom_mode_args = driver_escape.get_custom_mode(scalarvalue[index].targetId,
                                                                         custom_mode_args)
                logging.info("Number of custom mode added {0}".format(custom_mode_args.NumOfModes))
                for modes in range(0, custom_mode_args.NumOfModes):
                    logging.info("The Modes added by CUSTOM API {0} x {1}".format(custom_mode_args.XRes[modes].SourceX,
                                                                                  custom_mode_args.XRes[modes].SourceY))

                if status is False:
                    gdhm.report_bug(
                        title="[NN/IS] Escape call failed : get_custom_mode()",
                        problem_classification=gdhm.ProblemClassification.LOG_FAILURE,
                        component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(f"Escape call failed : get_custom_mode() for {scalarvalue[index].targetId}")

    ##
    # @brief test_start add NNISscaling registry and do system restart if request by OS
    # @return - None
    def test_setup(self):
        status, reboot_required = self.check_and_add_nnis_scaling_registry()
        if status:
            logging.info("NNISScaling registry updated and successfully restarted driver.")
        elif status is False and reboot_required is True:
            if reboot_helper.reboot(self, 'test_run') is False:
                self.fail("Failed to reboot the system")
        else:
            self.fail("Failed to restart display driver")

    ##
    # @brief Unit-test runTest function. Check Mode enumeration and Modeset
    # @return - None
    def test_run(self):
        self.is_teardown_required = True
        logging.debug(" test_run() started ".center(64, "*"))
        self.parse_xml()
        self.add_and_verify_custom_mode()

        # Apply NN/IS scaling based on input
        self.apply_nn_is_scaling(is_integer_scaling=self.is_integer_scaling)

        # Apply mode and verify scaling
        self.apply_mode_and_verify_scaling(config_dict=self.custom_mode_dict,
                                           virtual_mode_set_aware=self.virtual_mode_set_aware)
        # Apply native mode due to plane downscale removal custom mode applied and exite
        # Next test starts with currently applied custom mode and test fails HSD: 18021894480
        self.apply_native_mode()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('NNISScalingCustomMode'))
    TestEnvironment.cleanup(outcome)
