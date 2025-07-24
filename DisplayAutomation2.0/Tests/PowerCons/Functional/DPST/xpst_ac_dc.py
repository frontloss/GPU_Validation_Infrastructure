########################################################################################################################
# @file         xpst_ac_dc.py
# @brief        Test for XPST kei scenarios
# @author       Tulika
########################################################################################################################
import logging
import unittest

from Libs.Core import registry_access, display_essential, display_power
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Tests.CABC import cabc
from Tests.CABC.cabc import OsCabcOption
from Tests.PowerCons.Functional.DPST import dpst
from Tests.PowerCons.Functional.DPST.dpst_base import DpstBase
from Tests.PowerCons.Modules import common, dut
from Libs.Core import etl_parser

display_power_ = display_power.DisplayPower()


##
# @brief        This class contains OS Option AC DC test cases for XPST
class XpstAcDc(DpstBase):
    os_option = None

    ##
    # @brief        This class method is the entry point for XPST Os Option test case.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(XpstAcDc, cls).setUpClass()
        if cls.cmd_line_param[0]['OS_OPTION'] != 'NONE':
            cls.os_option = cls.cmd_line_param[0]['OS_OPTION'][0]
            cabc.toggle_os_cabc_option(cabc.OsCabcOption[cls.os_option])
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            assert False, "Failed to restart display driver after VBT update"

    ##
    # @brief       This method is the exit point for XPST Os Option test case
    # @return       None
    @classmethod
    def tearDownClass(cls):
        reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE,
                                                 reg_path=r"System\CurrentControlSet")
        registry_access.delete(args=reg_args, reg_name="CABCOption", sub_key=r"Control\GraphicsDrivers")

        if "WITH_EPSM" in cls.cmd_line_param[0]['SELECTIVE']:
            for adapter in dut.adapters.values():
                epsm_status = dpst.set_epsm(adapter, disable_epsm=True)
                if epsm_status is False:
                    assert False, "FAILED to configure EPSM status"

        result, reboot_required = display_essential.restart_gfx_driver()
        if result is False:
            assert False, f"FAILED to restart display driver"

        super(XpstAcDc, cls).tearDownClass()

    ##
    # @brief        This function verifies XPST for OS option
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['WITHOUT_EPSM'])
    # @endcond
    def t_11_xpst_os_option(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                for trial in range(2):
                    toggle_status, pwr_src = cabc.toggle_power_source()
                    if toggle_status is False:
                        self.fail(f"FAILED to toggle power source")

                    etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
                    # Generate reports from ETL file using EtlParser
                    logging.info("Step: Generating EtlParser Report for {0}".format(etl_file))
                    if etl_parser.generate_report(etl_file) is False:
                        self.fail("\tFAILED to generate ETL Parser report (Test Issue)")
                    logging.info("\tPASS: Successfully generated ETL Parser report")

                    if not self.verify_xpst(adapter, panel, pwr_src) or not self.verify_max_min_level_in_igcl(adapter,
                                                                                                              panel,
                                                                                                              pwr_src):
                        self.fail(f"FAIL: XPST verification failed for {self.os_option}")
                    logging.info(f"PASS: XPST verification passed for {self.os_option}")

    ##
    # @brief        This function verifies XPST EPSM status for OS option
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['WITH_EPSM'])
    # @endcond
    def t_12_xpst_os_option_with_epsm(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                epsm_status = dpst.set_epsm(adapter, disable_epsm=True)
                if epsm_status is False:
                    assert False, "FAILED to configure EPSM status"
                if epsm_status is True:
                    result, reboot_required = display_essential.restart_gfx_driver()
                    if result is False:
                        assert False, f"FAILED to restart display driver for {adapter.name}"

                for trial in range(2):
                    toggle_status, pwr_src = cabc.toggle_power_source()
                    if toggle_status is False:
                        self.fail(f"FAILED to toggle power source")

                    etl_file = dpst.run_workload(dpst.WorkloadMethod.PSR_UTIL)
                    if etl_file is False:
                        self.fail("FAILED to run the workload")
                    if etl_parser.generate_report(etl_file) is False:
                        logging.error("\tFAILED to generate ETL Parser report (Test Issue)")
                        return None

                    if not self.verify_xpst(adapter, panel, pwr_src) or not self.verify_epsm_with_os_option(panel,
                                                                                                            etl_file,
                                                                                                            pwr_src):
                        self.fail(f"FAIL: XPST verification failed for {self.os_option} with EPSM")
                    logging.info(f"PASS: XPST verification passed for {self.os_option} with EPSM")

    ##
    # @brief        Api to verify XPST CTL and Dithering register with OS option
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    pwr_src
    # @return       None
    def verify_xpst(self, adapter, panel, pwr_src):
        status = True
        logging.info("Verifying MMIO registers for DPST CTL and Dithering")
        ctl_status = dpst.verify_dpst_ctl(adapter, panel, self.xpst_feature)
        dithering_status = dpst.verify_dithering(adapter, panel)
        logging.info(f"DPST CTL= {ctl_status}, Dithering= {dithering_status}")
        if self.os_option == OsCabcOption.OFF:
            if ctl_status is True or dithering_status is True:
                status = False
                logging.error(f"Fail: MMIO verification failed for {self.os_option}")
        if self.os_option == OsCabcOption.ALWAYS_ON:
            if ctl_status is False or dithering_status is False:
                status = False
                logging.error(f"Fail: MMIO verification failed for {self.os_option}")
        if self.os_option == OsCabcOption.ON_BATTERY and pwr_src == display_power.PowerSource.AC:
            if ctl_status is True or dithering_status is True:
                status = False
                logging.error(f"Fail: MMIO verification failed for {self.os_option}")
        if self.os_option == OsCabcOption.ON_BATTERY and pwr_src == display_power.PowerSource.DC:
            if ctl_status is False or dithering_status is False:
                status = False
                logging.error(f"Fail: MMIO verification failed for {self.os_option}")
        return status

    ##
    # @brief        Api to verify max and min level in IGCL
    # @param[in]    adapter
    # @param[in]    panel
    # @param[in]    pwr_src
    # @return       None
    def verify_max_min_level_in_igcl(self, adapter, panel, pwr_src):
        status = True
        power_scheme = display_power_.get_current_power_scheme()
        feature_params = dpst.get_status(panel.target_id, pwr_src, power_scheme)
        logging.info("Verifying IGCL default Params with CABC OS Option")
        if feature_params is None:
            self.fail("Fail: IGCL Get status failed for target_id:{0}".format(panel.target_id))

        logging.info(f"IGCL: Max Level= {feature_params.max_level}, Min Level= {feature_params.min_level}, "
                     f"Current Level= {feature_params.current_level}, EPSM Supported= {feature_params.is_epsm_supported}, "
                     f"EPSM Enabled= {feature_params.is_epsm_enabled}")
        sku_name = None
        if adapter.name in ['ADLP']:
            sku_name = machine_info.SystemInfo().get_sku_name(adapter.gfx_index)
        if adapter.name not in common.PRE_GEN_14_PLATFORMS or (sku_name in ['TwinLake']):
            if pwr_src == display_power.PowerSource.AC:
                if feature_params.max_level != 1 or feature_params.min_level != 1 or feature_params.current_level != 1:
                    status = False
                    logging.error("Fail: Max level and Min level verification failed")
            if pwr_src == display_power.PowerSource.DC:
                if feature_params.max_level != 3 or feature_params.min_level != 1 or feature_params.current_level != 2:
                    status = False
                    logging.error("Fail: Max level and Min level verification failed")
            if pwr_src in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
                if feature_params.is_epsm_supported is not False or feature_params.is_epsm_enabled is not False:
                    status = False
                    logging.error("Fail: EPSM default status verification failed")
        else:
            if pwr_src in [display_power.PowerSource.DC, display_power.PowerSource.AC]:
                if feature_params.max_level != 6 or feature_params.min_level != 1 or feature_params.current_level != 6:
                    status = False
                    logging.error("Fail: Max level and Min level verification failed")
                if feature_params.is_epsm_supported is not True and feature_params.is_epsm_enabled is not False:
                    status = False
                    logging.error("Fail: EPSM default status verification failed")
        return status

    ##
    # @brief        Api to verify EPSM with OS option
    # @param[in]    panel
    # @param[in]    etl_file
    # @param[in]    pwr_src
    # @return       None
    def verify_epsm_with_os_option(self, panel, etl_file, pwr_src):
        status = True
        power_scheme = display_power_.get_current_power_scheme()
        logging.info(f"Verifying EPSM with CABC OS Option")
        epsm_status = dpst.verify_epsm(etl_file)

        feature_params = dpst.get_status(panel.target_id, pwr_src, power_scheme)
        if feature_params is None:
            self.fail(f"Fail: IGCL Get status failed for target_id:{panel.target_id}")
        logging.info(
            f"IGCL: EPSM Support= {feature_params.is_epsm_supported}, EPSM Enabled= {feature_params.is_epsm_enabled}")

        if ((self.os_option == OsCabcOption.ALWAYS_ON or self.os_option == OsCabcOption.ON_BATTERY)
                and pwr_src == display_power.PowerSource.DC):
            if not (epsm_status and feature_params.is_epsm_supported and feature_params.is_epsm_enabled):
                status = False
                logging.error(f"Fail: EPSM is NOT supported or enabled in {pwr_src} for {self.os_option}")
        else:
            if epsm_status is True or feature_params.is_epsm_supported or feature_params.is_epsm_enabled:
                status = False
                logging.error(f"Fail: EPSM is either supported or enabled in {pwr_src} for {self.os_option}")
        return status


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(XpstAcDc))
    test_environment.TestEnvironment.cleanup(test_result)
