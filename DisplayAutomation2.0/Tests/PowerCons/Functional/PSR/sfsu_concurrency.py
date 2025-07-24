#######################################################################################################################
# @file             sfsu_concurrency.py
# @brief            Tests for verifying SFSU/FFSU feature co-existence with other features
#
# @author           Chandrakanth Reddy
#######################################################################################################################

from Libs.Core.wrapper import control_api_wrapper
from Libs.Core import etl_parser, registry_access
from Libs.Core.flip import MPO
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_environment
from Libs.Core.machine_info import machine_info
from Libs.Core.test_env import test_environment
from Tests.Color.Common import common_utility
from Tests.PowerCons.Functional import pc_external
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Functional.PSR.sfsu import verify_su_mode


##
# @brief        This class contains SFSU concurrency tests
class SfsuConcurrency(PsrBase):

    ##
    # @brief        Function to verify co-existence of SFSU with LACE
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['LACE'])
    # @endcond
    def t_11_sfsu_lace(self):
        self.verify_with_lace()

    ##
    # @brief        Function to verify co-existence of SFSU with 3D_LUT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['3D_LUT'])
    # @endcond
    def t_12_sfsu_3d_lut(self):
        self.verify_with_3d_lut()

    ##
    # @brief        Function to verify co-existence of SFSU with plane formats
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['PLANE_FORMAT'])
    # @endcond
    def t_13_sfsu_plane_format(self):
        self.verify_with_plane_formats()

    ##
    # @brief        Function to verify co-existence of SFSU with MPO scenario
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['MPO'])
    # @endcond
    def t_14_sfsu_mpo(self):
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                status, etl_file = pc_external.run_d3d_app(full_screen=False, is_multi_instance=True)
                if status is False:
                    self.fail("3D APP application not launched properly")
                if self.verify_mpo(adapter, panel, etl_file) is False:
                    self.fail("CFFU Check with MPO is failed")
                logging.info(f"PASS: Full Fetch verification with MPO on {panel}")

    ##
    # @brief        Helper Function to verify co-existence of SFSU with MPO
    # @param[in]    adapter Adapter Object
    # @param[in]    panel Panel Object
    # @param[in]    etl_file etl file path
    # @return       None
    def verify_mpo(self, adapter, panel, etl_file):
        time_stamp = 0
        if etl_parser.generate_report(etl_file) is False:
            return False
        plane_ctl_3 = MMIORegister.get_instance("PLANE_CTL_REGISTER", "PLANE_CTL_3_" + panel.pipe, adapter.name)
        psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                                 adapter.name)
        plane_3_data = etl_parser.get_mmio_data(plane_ctl_3.offset)
        for val in plane_3_data:
            plane_ctl_3.asUint = val.Data
            if plane_ctl_3.plane_enable:
                logging.info(f"Plane3 enabled at {val.TimeStamp}")
                time_stamp = val.TimeStamp
                break
        if time_stamp == 0:
            logging.error("Plane3 is not enabled")
            return False
        man_trk = etl_parser.get_mmio_data(psr2_man_trk.offset, start_time=time_stamp)
        for data in man_trk:
            psr2_man_trk.asUnit = data.Data
            if psr2_man_trk.sf_continuous_full_frame == 0:
                logging.error("CFFU is not enabled for MPO")
                return False
        return True

    ##
    # @brief        Helper Function to verify co-existence of SFSU with LACE
    # @return       None
    def verify_with_lace(self):
        cff_ctl = None
        sff_ctl = None
        #Enable Lace1.0 version support for ARL
        if SystemInfo().get_sku_name('gfx_0') == 'ARL' and self.lace1p0_status:
            if common_utility.write_registry(gfx_index="GFX_0", reg_name="LaceVersion",
                                             reg_datatype=registry_access.RegDataType.DWORD, reg_value=10,
                                             driver_restart_required=True) is False:
                logging.error("Failed to enable Lace1.0 registry key")
                self.fail("Failed to enable Lace1.0 registry key")
            logging.info("Registry key add to enable Lace1.0 is successful")
        else:
            logging.info("Lace1.0 Registry Key is either not present or not enabled")

        for adapter in dut.adapters.values():
            feature, _ = self.get_feature(adapter)
            for panel in adapter.panels.values():
                if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                    cff_ctl = MMIORegister.read("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
                    sff_ctl = MMIORegister.read("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                if adapter.name in ['TGL', 'DG1', 'DG2'] and panel.pipe == 'B':
                    logging.error("LACE is not supported on PIPE {0} on {1}".format(panel.pipe, panel.port))
                    return
                try:
                    lace_enable_status, etl_file_during_lace_enable = pc_external.enable_disable_lace(adapter, panel, True, adapter.gfx_index)
                    if lace_enable_status is False:
                        self.fail(f"Failed to enable LACE in adapter {adapter.gfx_index}")

                    if pc_external.get_lace_status(adapter, panel) is False:
                        self.fail("LACE is not enabled")
                    logging.info("LACE was successfully enabled")

                    psr_enable_status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
                    if feature >= psr.UserRequestedFeature.PSR2_SFSU:
                        if psr_enable_status is False:
                            self.fail("SFSU is disabled when LACE is Enabled on {0}".format(panel.port))
                        logging.info("PASS : Manual tracking is not disabled when LACE is enabled")
                        psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                     adapter.name)
                        status, _ = sfsu.verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl)
                        if not status:
                            logging.error("SU mode status verification failed")
                            return False
                        if sfsu.get_man_trk_status(adapter, panel) != sfsu.SuType.SU_CONTINUOUS_UPDATE:
                            self.fail("Continuous Full Frame update not happened")
                        dpst_enable = is_dpst_possible(panel, self.power_source)
                        if sfsu.verify_sfsu(adapter, panel, etl_file_during_lace_enable, 'LACE', feature, dpst_enable, is_basic=True) is False:
                            self.fail("Full Fetch verification Failed for LACE")
                    elif feature == psr.UserRequestedFeature.PSR2_FFSU:
                        if psr_enable_status is False:
                            self.fail("FFSU is disabled when LACE is Enabled on {0}".format(panel.port))
                        logging.info("PASS: Manual Tracking is Enabled")
                except Exception as e:
                    self.fail(e)
                finally:
                    # Disable LACE at the end of verification
                    lace_disable_status, etl_file_during_lace_disable = pc_external.enable_disable_lace(adapter, panel, False, adapter.gfx_index)
                    if lace_disable_status is False:
                        self.fail(f"Failed to disable LACE in adapter {adapter.gfx_index}")
                    logging.info(f"Successfully disabled LACE in adapter {adapter.gfx_index}")


    ##
    # @brief        Helper Function to verify co-existence of SFSU with 3D_LUT
    # @return       None
    def verify_with_3d_lut(self):
        feature_str = None
        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if panel.pipe == 'B' and adapter.name in ['TGL', 'DG1', 'DG2']:
                    logging.error("\tSFSU is not supported on PIPE {0} on {1}".format(panel.pipe, panel.port))
                    return
                try:
                    res, etl_file = pc_external.verify_3dlut(adapter, panel)
                    if res is False:
                        self.fail("\t3D LUT verification Failed")
                    status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
                    if feature >= psr.UserRequestedFeature.PSR2_SFSU and status is False:
                        self.fail("\tSelective Fetch is disabled when 3D LUT is Enabled")
                    if feature == psr.UserRequestedFeature.PSR2_FFSU and status is False:
                        self.fail("\tPSR2 Manual tracking is disabled when 3D LUT is Enabled")
                    if verify_mode(adapter, panel, etl_file) is False:
                        self.fail("\tSFF verification Failed")
                except Exception as e:
                    self.fail(e)
                finally:
                    # Apply default bin before returning
                    pc_external.apply_default_bin(adapter, panel)
        logging.info("\tPASS : {} verification successful".format(feature_str))

    ##
    # @brief        Helper Function to verify co-existence of SFSU with plane formats
    # @return       None
    def verify_with_plane_formats(self):
        feature_str = None
        source_id = []
        for index in range(0, self.no_of_displays):
            source_id.append(index)

        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            enable_mpo = MPO()
            ##
            # Enable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=adapter.gfx_index)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                if panel.pipe == 'B' and adapter.name in ['TGL', 'DG1', 'DG2']:
                    logging.error(" SFSU/FFSU is not supported on PIPE {0} on {1}".format(panel.pipe, panel.port))
                    return
                for pixel_frmt in list(pc_external.PIXEL_FORMAT.values()):
                    pixel_format = [pixel_frmt, None, None]
                    if pc_external.plane_format(adapter, panel, self.no_of_displays, source_id, enable_mpo, pixel_format=pixel_format) is False:
                        self.fail("Failed to generate FLIP {0}".format(pixel_frmt[0]))
                    status = psr.is_psr_enabled_in_driver(adapter, panel, feature)
                    if feature >= psr.UserRequestedFeature.PSR2_SFSU and status is False:
                        self.fail("Selective Fetch is disabled for Non-RGB888 formats")
                    if feature == psr.UserRequestedFeature.PSR2_FFSU and status is False:
                        self.fail("PSR2 Manual tracking is disabled for Non-RGB888 Formats")
            ##
            # Disable the DFT framework and feature
            enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter.gfx_index)
            logging.info("\tDisable the DFT framework success")
            time.sleep(2)
        logging.info("PASS : {} verification successful".format(feature_str))

##
# @brief        Helper Function to verify the sff mode
# @param[in]    adapter Object
# @param[in]    panel Object
# @param[in]    etl_file etl file path
# @return       True/False boolean
def verify_mode(adapter, panel, etl_file):
    if etl_parser.generate_report(etl_file) is False:
        return False
    psr2_man_trk = MMIORegister.get_instance("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder,
                                             adapter.name)
    man_trk_data = etl_parser.get_mmio_data(psr2_man_trk.offset, is_write=True)
    if man_trk_data is None:
        logging.info("psr2_man_trk mmio data is empty")
        return False
    if adapter.name not in common.PRE_GEN_15_PLATFORMS:
        sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)
        sff_data = etl_parser.get_mmio_data(sff_ctl.offset, is_write=True)
        if sff_data is None:
            logging.info("sff_ctl mmio data is empty")
            return False
        for data in sff_data:
            sff_ctl.asUint = data.Data
            if sff_ctl.sf_single_full_frame:
                logging.info(f"PASS: Single Full Frame update at {data.TimeStamp}")
                break
    else:
        for data in man_trk_data:
            psr2_man_trk.asUnit = data.Data
            if psr2_man_trk.sf_single_full_frame:
                logging.info(f"PASS: Single Full Frame update at {data.TimeStamp}")
                break
    return True


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(SfsuConcurrency))
    test_environment.TestEnvironment.cleanup(test_result)
