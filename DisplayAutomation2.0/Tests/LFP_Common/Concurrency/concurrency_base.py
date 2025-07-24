#######################################################################################################################
# @file         concurrency_base.py
# @brief        This file contains base class for LFP concurrency tests.
# @remarks      @ref concurrency_base.py contains common setUp and tearDown steps for all concurrency tests.
#               Also contains the dynamic pipe allocation method
# @author       Bhargav Adigarla
#######################################################################################################################

import logging
import sys
import unittest

from DisplayRegs.DisplayArgs import TranscoderType
from Libs.Core import cmd_parser, display_power, registry_access
from Libs.Core import enum, display_utility
from Libs.Core.display_config import display_config
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Tests.Color.Common import common_utility
from Tests.LFP_Common.Concurrency import edp_feature_utility
from Tests.PowerCons.Modules import dut, common

##
# @brief        Exposed Class for LFP concurrency tests. Any new LFP concurrency test can inherit this class to use
#               common setUp and tearDown functions. LrrBase also includes some functions used across all LFP concurrency
#               tests.
class ConcurrencyBase(unittest.TestCase):
    cmd_line_param = None
    display_config_ = display_config.DisplayConfiguration()
    display_power_ = display_power.DisplayPower()
    display_feature_dict = {}
    lace1p0_status = None
    lace1p0_reg_value = None

    ##
    # @brief        This class method is the entry point for any LFP concurrency test cases that inherits this class.
    #               This helps to initialize some of the parameters required for LFP concurrency test execution.
    # @details      This function checks for feature support and initialises parameters to handle
    #               multi-adapter scenarios in test cases
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info(" SETUP: LFP_CONCURRENCY ".center(common.MAX_LINE_WIDTH, "*"))
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        #Read registry for LACE
        cls.lace1p0_status, cls.lace1p0_reg_value = common_utility.read_registry(gfx_index="GFX_0",
                                                                                   reg_name="LaceVersion")
        # Handle multi-adapter scenario
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]

        dut.prepare()
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if (panel.port == 'DP_A' or panel.port == "MIPI_A") and cls.cmd_line_param[0]['LFP1'] is not None:
                    cls.display_feature_dict.update({panel.port: cls.cmd_line_param[0]['LFP1'][0].upper()})
                    setattr(panel, 'feature', cls.cmd_line_param[0]['LFP1'][0].upper())
                    logging.info("Feature requested on {0} {1} pipe {2}".format(panel.port, panel.feature, panel.pipe))

                if (panel.port == 'DP_B' or panel.port == "MIPI_C") and cls.cmd_line_param[0]['LFP2'] is not None:
                    cls.display_feature_dict.update({panel.port: cls.cmd_line_param[0]['LFP2'][0].upper()})
                    setattr(panel, 'feature', cls.cmd_line_param[0]['LFP2'][0].upper())
                    logging.info("Feature requested on {0} {1} pipe {2}".format(panel.port, panel.feature, panel.pipe))

                logging.info("{0}".format(panel))
                logging.info("\t{0}".format(panel.psr_caps))
                logging.info("\t{0}".format(panel.drrs_caps))
                logging.info("\t{0}".format(panel.vrr_caps))
                logging.info("\t{0}".format(panel.mipi_caps))

    ##
    # @brief        This method is the exit point for all LFP concurrency test cases that inherit this class.
    #               This resets the environment changes done for execution of LFP concurrency tests
    # @return       None
    @classmethod
    def TearDownClass(cls):
        # Resetting LACE to default version
        if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                         reg_datatype=registry_access.RegDataType.DWORD,
                                         reg_value=cls.lace1p0_reg_value,
                                         driver_restart_required=True) is False:
            logging.error("Failed to enable default Lace2.0 registry key")
            cls.fail(ConcurrencyBase(), "Failed to enable default Lace2.0 registry key")
        else:
            logging.info("Pass: Lace restored back to default Lace2.0 in TearDown")
        logging.info("Registry key add to enable default Lace2.0 is successful")
        dut.reset()

    ##
    # @brief        Test function to make sure all the requirements are fulfilled before running other LFP concurrency
    #               test functions. Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        panels = dut.adapters['gfx_0'].panels.values()

        if ('MIPI_A' in self.display_feature_dict.keys() and 'DP_B' in self.display_feature_dict.keys()) or ('MIPI_C' in self.display_feature_dict.keys() and 'DP_A' in self.display_feature_dict.keys()):
            pipe_result = []
            for panel in panels:
                pipe_result.append("True") if ('DP' in panel.port and panel.pipe == "A") or ('MIPI' in panel.port and panel.pipe == "B") else pipe_result.append("False")

            if "False" in pipe_result:
                self.fail(f"FAIL:{panel.port} is allocated on PIPE_{panel.pipe} (Unexpected)")
            else:
                logging.info(f"Pass:{panel.port} is allocated on PIPE_{panel.pipe} (Expected)")

        for panel in panels:
            if panel.feature in ["VDSC", "DPST", "FBC", "LACE"]:
                edp_feature_utility.enable(dut.adapters["gfx_0"], panel)
                if panel.feature == "DPST":
                    # Enable Simulated Battery for AC/DC switch
                    logging.info("Enabling Simulated Battery")
                    assert self.display_power_.enable_disable_simulated_battery(
                        True), "Failed to enable Simulated Battery"
                    logging.info("\tPASS: Enabled Simulated Battery successfully")
                    if not self.display_power_.set_current_powerline_status(display_power.PowerSource.DC):
                        self.fail("Failed to switch power line status to DC (Test Issue)")

    ##
    # @brief        Test function to make sure the panel feature is enabled.
    #   `           Failure of this test will stop the execution.
    # @return       None
    # @cond
    @common.configure_test(critical=True)
    # @endcond
    def t_20_cleanup(self):
        panels = dut.adapters['gfx_0'].panels.values()
        for panel in panels:
            if panel.feature in ["VDSC", "DPST", "FBC", "LACE"]:
                edp_feature_utility.enable(dut.adapters["gfx_0"], panel, 0)

    ##
    # @brief        Update pipe details in panel object
    # @param[in]    config - panels as config list
    # @return       None
    def update_dynamic_pipe(self, config):
        panels = dut.adapters['gfx_0'].panels.values()
        for panel in panels:
            if panel.port in config:
                display_base_obj = DisplayBase(panel.port)
                trans, pipe = display_base_obj.get_transcoder_and_pipe(panel.port)

                # Get panel transcoder
                if trans == 0:
                    panel.transcoder = 'EDP'
                elif trans == 5:
                    panel.transcoder = 'DSI0'
                elif trans == 6:
                    panel.transcoder = 'DSI1'
                else:
                    panel.transcoder = chr(int(trans) + 64)

                panel.transcoder_type = TranscoderType(trans) if trans >= 0 else TranscoderType.TRANSCODER_NULL
                panel.pipe = chr(int(pipe) + 65)
                logging.info("updated pipe {0} for panel {1}".format(panel.pipe, panel.port))
