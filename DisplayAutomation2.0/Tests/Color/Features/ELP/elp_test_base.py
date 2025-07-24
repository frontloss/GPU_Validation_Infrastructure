#################################################################################################
# @file         elp_test_base.py
# @brief        This script is a Feature Base class specific to the RCR for Samsung - ELP.
#               The elp_test_base performs the below functionalities
#               to setup all the infra needed by the test scripts.
#               1.setUp() -  Invokes Common class's setUp() to perform basic functionalities
#               2.__parse_user_opt_level() - To parse the user input optimization level from the command line
#               3.stop_and_start_etl() - An encapsulating function which helps in stopping an ETL and
#                                        generates a report and starts a new ETL
#               5.verify_opt_level_in_dpcd() - Verify if the specified optimization level has been successfully
#                                               updated in the DPCD 0x358
#               6.enable_optimization_and_verify() - Encapsulating function which invokes the escape call to set the
#                                                    optimization level input by the user
#                                                    Invokes verification functions to validate if the optimization level
#                                                    is successfully getting updated invoking the Get Escape call
#                                                    and also verify if the same has been updated in the DPCD
# @author       Smitha B
#################################################################################################
import random
from Libs.Core import etl_parser
from Libs.Core import display_power, window_helper
from Libs.Core.vbt.vbt import Vbt
from Libs.Core.wrapper import control_api_wrapper
from Tests.test_base import *
from Tests.Color.Common import color_etl_utility
from Tests.Color.Features.ELP.elp import *


class ELPTestBase(TestBase):
    scenario = None
    user_opt_level = 1
    optimization_level = -1

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        self.custom_tags["-OPT_LEVEL"] = None

        ##
        # Invoking Common BaseClass's setUp() to perform all the basic functionalities
        super().setUp()

        ##
        # Performing a VBT operation to enable ELP feature
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                gfx_vbt = Vbt(gfx_index)
                if panel.is_lfp:
                    if set_elp_feature_in_vbt(gfx_index, gfx_vbt, port, True) is False:
                        self.fail()

        ##
        # Fetch the user input for scenario if anything specific to ELP test suite
        self.scenario = str(self.context_args.test.cmd_params.test_custom_tags["-SCENARIO"][0])
        self.optimization_level = int(str(self.context_args.test.cmd_params.test_custom_tags["-OPT_LEVEL"][0]))
        logging.debug("Slider Level requested by User {0}".format(self.optimization_level))

        ##
        # Check if the panel supports the feature and proceed to apply the optimization level provided by the user
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_lfp:
                    num_of_elp_panels = verify_panel_support_for_elp(self.context_args)
                    if num_of_elp_panels == 0:
                        logging.error("FAIL : Atleast one ELP supported panel should be planned in the command line")
                        self.fail()

                    if verify_power_caps_for_elp_support(panel.target_id) is False:
                        self.fail()

                    ##
                    # If the Optimization levels are not specified by the user, taking a default of 1
                    self.__parse_user_opt_level(self.optimization_level)
                    ##
                    # Switch the Power Mode to DC as the power savings is intended in DC Mode only
                    status = common_utility.apply_power_mode(display_power.PowerSource.DC)
                    if status is False:
                        self.fail()
                else:
                    logging.debug("Skipping the verification for non-lfp panels")

    ##
    # @brief        Helper function to parse the user input optimization level from the command line
    #               If user has not provided any optimization level, initializes the level to a value
    #               other than the current value
    # @param[in]    user_level - user input optimization level
    # @return       True if OS has issued the DDI and the Optimization Level
    def __parse_user_opt_level(self, user_level: int):

        ##
        # If the Optimization levels are not specified by the user, initialize the level to a value
        # other than the current value
        ##
        # Get the current optimization level
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                current_level = color_igcl_escapes.get_current_elp_opt_level(panel.target_id)
                logging.debug("The Current Opt Level is {0}".format(current_level))
                if (user_level is None) or (current_level == user_level):
                    logging.info("User requested optimization Level is {0}; Current Level is {1}; Hence setting a "
                                 "random value between 1-6".format(
                        self.optimization_level, current_level))
                    while True:
                        new_level = random.randint(1, 3)
                        if current_level != new_level:
                            break
                    self.user_opt_level = new_level
                else:
                    self.user_opt_level = user_level
                logging.info("Updated User Level is {0}".format(self.user_opt_level))

    #
    # ##
    # # @brief Helps in stopping an ETL and generates a report and starts a new ETL
    # # @param[in] self
    # # @param[in] etl_name
    # # @return None
    def stop_and_start_etl(self, etl_name: str):
        # Check if OS has issued the Blc3Optimization DDI so that the driver can proceed to program
        # the DPCD
        init_etl_path = color_etl_utility.stop_etl_capture(etl_name)

        if etl_parser.generate_report(init_etl_path) is False:
            logging.error("\tFailed to generate EtlParser report")
            self.fail()
        else:
            ##
            # Start the ETL again for capturing other events
            if color_etl_utility.start_etl_capture() is False:
                logging.error("Failed to Start Gfx Tracer")
                self.fail()

    ##
    # @brief Encapsulating function which invokes the escape call to set the optimization level input by the user
    # Invokes verification functions to validate if the optimization level is successfully getting updated
    # by invoking the Get Escape call and also verify if the same has been updated in the DPCD
    # @param[in] self
    # @param[in] gfx_index
    # @param[in] panel
    # @param[in] port
    # @param[in] level
    # @return bool True or False
    def enable_elp_optimization_and_verify(self, level: int):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp:
                    dpcd_value_358 = color_escapes.fetch_dpcd_data(color_enums.EdpHDRDPCDOffsets.EDP_BRIGHTNESS_OPTIMIZATION.value,
                                                                   panel.display_and_adapterInfo)
                    opt_level = common_utility.get_bit_value(dpcd_value_358, 5, 7)
                    logging.debug("Optimization Level in the DPCD before setting the new Level {0}".format(opt_level))
                    ##
                    # Invoke the escape call to set the optimization level
                    logging.info("Invoking Escape call with optimization level as {0} on adapter {1} on Panel {2} "
                                 "connected to {3}".format(level, gfx_index, port, panel.pipe))
                    if color_igcl_escapes.set_dpst_info(level, panel.target_id) is False:
                        gdhm.report_driver_bug_pc("[ELP] Failed to set ELP optimization level via IGCL")
                        return False
                    if perform_elp_verification(gfx_index, panel, port, level) is False:
                        return False
        return True

    ##
    # @brief To perform cleanup after completing the test steps.
    # @param[in] self
    def tearDown(self):
        # Disable ELP in VBT
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                gfx_vbt = Vbt(gfx_index)
                if panel.is_lfp:
                    if set_elp_feature_in_vbt(gfx_index, gfx_vbt, port, False) is False:
                        self.fail()

        logging.info("Switching the PowerMode back to AC")
        status = common_utility.apply_power_mode(display_power.PowerSource.AC)
        if status is False:
            self.fail()
        super().tearDown()