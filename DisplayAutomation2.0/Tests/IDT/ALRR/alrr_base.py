#######################################################################################################################
# @file         alrr_base.py
# @brief        Contains the base TestCase class for all ALRR tests, New ALRR tests can be created by inheriting this
#               class and adding new test functions.
#
# @author       Ravichandran M
#######################################################################################################################
import logging
import sys
import unittest
from Libs.Core.logger import html
from Libs.Core import etl_parser
from Tests.PowerCons.Modules import common, dut, workload
from Tests.IDT.ALRR import alrr
from Libs.Core import cmd_parser
from Libs.Core import display_essential
from registers.mmioregister import MMIORegister
from Tests.PowerCons.Modules import dpcd


##
# @brief        Exposed Class to write ALRR tests. Any new test can inherit this class to use common setUp and tearDown
#               functions.


class Alrrbase(unittest.TestCase):
    cmd_line_param = None

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any ALRR test case. Helps to initialize some of the
    #               parameters required for ALRR test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        cls.cmd_line_param = cmd_parser.parse_cmdline(sys.argv, custom_tags=common.CUSTOM_TAGS)

        # Handle multi-adapter scenarios
        if not isinstance(cls.cmd_line_param, list):
            cls.cmd_line_param = [cls.cmd_line_param]
        # Need to check if we need ALRR command line tag or not.

        dut.prepare()

    ##
    # @brief        This method is the exit point for all ALRR test cases. This resets the environment changes for the
    #               ALRR tests
    # @return       None
    @classmethod
    def tearDownClass(cls):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                alrr_status = alrr.disable(adapter)
                if alrr_status is False:
                    assert False, f"Failed to disable ALRR in{adapter.name}"
                if alrr_status is True:
                    alrr_status, reboot_required = display_essential.restart_gfx_driver()
                    if alrr_status is False:
                        logging.error("Failed to do Driver restart post Regkey updates")
                    else:
                        logging.info("Successfully restarted display driver")

        dut.reset()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify system and panel requirements for ALRR test
    # @return       None
    # @cond

    @common.configure_test(critical=True)
    # @endcond
    def t_00_requirements(self):
        html.step_start("Verify system and panel requirements for ALRR test")
        for adapter in dut.adapters.values():
            logging.info(f"Active panel capabilities for {adapter.name}")
            for panel in adapter.panels.values():
                logging.info(f"\t{panel}")
                if panel.is_lfp is False:
                    continue
                logging.info(f"\t\t{panel.psr_caps}")
                logging.info(f"\t\t{panel.idt_caps}")
                logging.info(f"\t\t{panel.vrr_caps}")
        html.step_end()

    ############################
    # Test Function
    ############################

    ##
    # @brief        Test function is to verify system and panel requirements for ALRR test
    # @return       None
    # # @cond
    # @common.configure_test(critical=True)
    # # @endcond
    def t_01_alrr_panel_requirements(self):
        for adapter in dut.adapters.values():
            logging.info(f"Active panel capabilities for {adapter.name}")
            for panel in adapter.panels.values():
                logging.info(f"\t{panel}")
                if not panel.idt_caps.is_alrr_supported:
                    self.fail(f"ALRR is not supported on current panel {panel.port}")
                if not panel.psr_caps.is_psr2_supported:
                    self.fail(f"PSR2 is not supported on current panel {panel.port}")
                if not panel.vrr_caps.is_vrr_supported:
                    self.fail(f"VRR is not supported on current panel {panel.port}")
                if not len(panel.rr_list) > 1:
                    self.fail(f"Multi RR is not supported on current panel {panel.port}")

                #  The ALRR requires display panel to support two refresh rates, default and low by using same pixel
                #  clock and different vertical blanking.  Additionally, the default refresh rate (Default RR)
                #  must an integer multiple of low refresh rate (Low RR)
                #  The Default RR = n x Low RR, where n=1, 2, 3, 4, …
                min_rr = panel.vrr_caps.min_rr
                max_rr = panel.vrr_caps.max_rr
                i = 2
                status = False
                while True:
                    rr_multiple = min_rr * i
                    if rr_multiple == max_rr:
                        status = True
                        break
                    if rr_multiple > max_rr:
                        break
                    i += 1
                if status is False:
                    self.fail(f"RR requirement for ALRR is NOT met for panel on {panel.port}")
                logging.info(f"RR requirement for ALRR is met for panel on {panel.port}")

    ##
    # @brief        Test function is to enable ALRR via Regkey
    # @return       None
    # @cond

    @common.configure_test(critical=True)
    # @endcond
    def t_10_enable_alrr(self):
        for adapter in dut.adapters.values():
            alrr_status = alrr.enable(adapter)
            if alrr_status is False:
                self.fail(f"Failed to enable ALRR on {adapter.name}")
            if alrr_status is True:
                alrr_status, reboot_required = display_essential.restart_gfx_driver()
                if alrr_status is False:
                    self.fail(f"Failed to do Driver restart post Regkey updates")
                logging.info("Successfully restarted display driver")

    ##
    # @brief        Test function to make sure ALRR is enabled
    # @param[in]    adapter - object of Adapter
    # @param[in]    panel - object of Panel
    # @param[in]    expect_alrr Boolean - True if ALRR should not work, False otherwise
    # @param[in]    expect_psr2 Boolean - True if psr2 should not work, False otherwise
    # @return       None
    def validate_alrr(self, adapter, panel, expect_alrr=False, expect_psr2=True):
        status = True
        if adapter.name in common.PRE_GEN_13_PLATFORMS + ["DG2"]:
            logging.info("\tALRR is not supported on pre-ADLP paltform, skipping verification..")
            return
        if panel.is_lfp is False:
            logging.info("\tALRR is not supported on external panel, skipping verification..")
            return

        status, etl_file_path = workload.etl_tracer_stop_existing_and_start_new(f"GfxTrace_{panel.port}_ALRR_Enable")
        if status is None:
            self.fail("FAILED to get ETL during ALRR Enable case")

        # Check for the MMIO entries of PSR2_CTL_REGISTER in ETL
        # get the mmio offsets for PSR2 CTL register
        etl_parser.generate_report(etl_file_path)
        psr2_ctl = MMIORegister.get_instance("PSR2_CTL_REGISTER", "PSR2_CTL_" + panel.transcoder, adapter.name)
        if adapter.name in common.PRE_GEN_14_PLATFORMS:
            psr2_mmio_ctl_output = etl_parser.get_mmio_data(psr2_ctl.offset, is_write=True)
            data = psr2_mmio_ctl_output[-1].Data
        else:
            # from GEN14+, Driver will write first 16 bits & last 16 bit's separately to avoid synchronization issues
            offset = 0x60902
            if panel.transcoder == 'B':
                offset = 0x61902
            psr2_mmio_ctl_output = etl_parser.get_mmio_data(offset, is_write=True)
            data = psr2_mmio_ctl_output[-1].Data << 16

        if psr2_mmio_ctl_output is None:
            logging.error(f"No MMIO output found for PSR2_CTL_{panel.transcoder}")
            status = False
        else:
            # @todo verify PSR2 and DPCD sequencing instead of just checking PSR2 CTL
            # PSR2 disable -> DPCD update -> PSR2 Enable
            psr2_ctl.asUint = data
            logging.info(f"\tOffset: {hex(psr2_mmio_ctl_output[-1].Offset)}= {hex(data)} at "
                         f"{psr2_mmio_ctl_output[-1].TimeStamp} ms")

            if bool(psr2_ctl.psr2_enable) == expect_psr2:
                logging.info(f"\tPSR2 CTL is {'enabled' if expect_psr2 else 'disabled'}")
            else:
                logging.error(f"\tPSR2 CTL is not {'enabled' if expect_psr2 else 'disabled'}")
                status = False

            # PSR2 selective updates are send at the start of the frame (SOF)
            # Whenever ALRR is enabled, Driver should set the selective update from the start of the frame.
            # So, selective region programming will be checked from the ETL.

            alrr_dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.ALRR_UBRR_CONFIG, is_write=True)

            if alrr_dpcd_data is None:
                self.fail("\t0x316H DPCD data not found in ETL")

            for alrr_data in alrr_dpcd_data:
                alrr_config_dpcd = dpcd.AlrrUbrrConfig(panel.target_id)

                if alrr_config_dpcd.enable_alrr is False and expect_alrr is False:
                    self.fail(f"ALRR is not enabled on {panel.port} on {adapter.name}")

                if alrr_config_dpcd.enable_alrr:

                    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER",
                                                             "PSR2_MAN_TRK_CTL_" + panel.transcoder, adapter.name)
                    psr2_man_trk_output = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True,
                                                                   start_time=alrr_data.TimeStamp)
                    if psr2_man_trk_output is None:
                        self.fail(f"No MMIO output found for PSR2_MAN_TRK_{panel.transcoder}")

                    logging.info(f"\tOffset: {hex(psr2_man_trk_output[-1].Offset)}= "
                                 f"{hex(psr2_man_trk_output[-1].Data)} at {psr2_man_trk_output[-1].TimeStamp} ms")

                    if psr2_man_trk.su_region_start_address != 0:
                        logging.error(f"Driver is not setting selective update from the start of the frame")
                        status = False
                    else:
                        logging.info(f"Driver is setting the selective update from the start of the frame")

        if alrr.verify(adapter, panel, etl_file_path, expect_alrr) is False:
            logging.error(f"\tFAILED to verify "
                          f"ALRR {'DISABLE' if expect_alrr else 'ENABLE'} "
                          f"programming in DPCD on {panel.port} on {adapter.name}")
            status = False
        else:
            logging.info(f"\tALRR {'DISABLE' if expect_alrr else 'ENABLE'} "
                         f"programming is verified in DPCD on {panel.port} on {adapter.name}")

        if status is False:
            self.fail(f"FAILED to verify ALRR on {panel.port} on {adapter.name}")
