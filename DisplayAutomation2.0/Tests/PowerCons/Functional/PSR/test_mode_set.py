#################################################################################################################
# @file         test_mode_set.py
# @brief        PSR Tests with modeset
# @details      @ref test_mode_set.py <br>
#               Test for Mode Set scenario
#               This file implements PSR1/PSR2 test for following scenarios
#               1. if panel supports multi RR -> RR switch
#               2. if panel supports single RR -> mode switch
#
# @author       Ashish Tripathi, Vinod D S
#################################################################################################################

from Libs.Core.display_config.display_config_enums import Scaling
from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.PSR.psr_base import *


##
# @brief        This class contains LRR VBT tests
class TestModeSet(PsrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        This test function verifies PSR with modeset, connected to  AC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_mode_set_ac(self):
        self.verify_with_mode_set(display_power.PowerSource.AC)

    ##
    # @brief        This test function verifies PSR with modeset, connected to  DC power source
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_mode_set_dc(self):
        self.verify_with_mode_set(display_power.PowerSource.DC)

    ############################
    # Helper Function
    ############################

    ##
    # @brief        This a helper function to verifies PSR with modeset, different power sources
    # @param[in]    power_source enum member indicating the power source
    # @return       None
    def verify_with_mode_set(self, power_source):
        status = True
        if not self.display_power_.set_current_powerline_status(power_source):
            self.fail("Failed to switch power line status to {0}(Test Issue)".format(
                power_source.name))

        # Apply supported modes on all active edp
        for adapter in dut.adapters.values():
            feature, feature_str = self.get_feature(adapter)
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and panel.pr_caps.is_pr_supported is False:
                    continue
                mode_list = []
                if len(panel.rr_list) > 1:
                    for rr in panel.rr_list:
                        mode_list.extend(common.get_display_mode(panel.target_id, rr, limit=2))
                else:
                    mode_list = common.get_display_mode(panel.target_id, limit=2, scaling=True)
                for mode in mode_list:
                    scaling = Scaling(mode.scaling).name
                    logging.info(f"Applying display mode - {scaling} : {mode.HzRes}x{mode.VtRes}@{mode.refreshRate}Hz")
                    if self.display_config_.set_display_mode([mode], False) is False:
                        self.fail("\tFailed to apply display mode")
                    time.sleep(5)
                    if adapter.name not in ['ICLLP'] and self.feature >= psr.UserRequestedFeature.PSR_2:
                        scalar1_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_1_" + panel.pipe, adapter.name,
                                                        gfx_index=adapter.gfx_index)

                        scalar2_reg = MMIORegister.read("PS_CTRL_REGISTER", "PS_CTRL_2_" + panel.pipe, adapter.name,
                                                        gfx_index=adapter.gfx_index)

                        if scalar1_reg.enable_scaler or scalar2_reg.enable_scaler:
                            logging.info("Scalar1 :{0} scalar 2:{1} on {2}".
                                         format(scalar1_reg.enable_scaler, scalar2_reg.enable_scaler, panel))
                        if mode.scaling != enum.MDS:
                            cff_ctl = None
                            sff_ctl = None
                            psr2_man_trk = MMIORegister.read("PSR2_MAN_TRK_CTL_REGISTER", "PSR2_MAN_TRK_CTL_" + panel.transcoder, adapter.name, 
                                                             gfx_index=adapter.gfx_index)
                            if adapter.name not in common.PRE_GEN_15_PLATFORMS:
                                cff_ctl = MMIORegister.get_instance("CFF_CTL_REGISTER", "CFF_CTL_" + panel.transcoder, adapter.name)
                                sff_ctl = MMIORegister.get_instance("SFF_CTL_REGISTER", "SFF_CTL_" + panel.transcoder, adapter.name)

                            # Expectation : For Post-Gen12 platforms, driver has to disable PSR2 manual tracking, program full frame co-ordinates and -
                            # disable CFF/SFF in respective MMIO registers 
                            if adapter.name not in common.PRE_GEN_13_PLATFORMS:
                                su_mode_status , actual_su_mode = sfsu.verify_su_mode(adapter.name, psr2_man_trk, cff_ctl, sff_ctl, [sfsu.SuType.SU_NONE])
                                if not su_mode_status:
                                    gdhm.report_driver_bug_pc(f"[PowerCons][PSR] Unexpected SU mode programming for non identity scaling")
                                    self.fail(f"Unexpected SU mode programming for {scaling} mode. Actual SU mode : {sfsu.SuType(actual_su_mode).name}")
                                logging.info(f"PASS : Driver did not enable Manual tracking/CFF/SFF for {scaling} mode")

                                native_node = self.display_config_.get_native_mode(panel.target_id)
                                # Check whether driver is programming full frame co-ordinates
                                if not psr.verify_su_region_programming(psr2_man_trk, native_node.vActive):
                                    self.fail("FAIL : Driver is not programming full frame coordinates for pipe scalar enable")
                                logging.info("SUCCESS : Driver is programming full frame coordinates for pipe scalar enable")

                    if panel.pr_caps.is_pr_supported is False:
                        status &= psr.delayed_vblank_wa_check(adapter, panel, self.feature)
                        if self.feature >= psr.UserRequestedFeature.PSR_2:
                            srd_ctl = MMIORegister.read("SRD_CTL_REGISTER", "SRD_CTL_" + panel.transcoder, adapter.name,
                                                        gfx_index=adapter.gfx_index)
                            if srd_ctl.tp2_tp3_select != 0:
                                logging.error(f"TP2_TP3 BIT not cleared in SRD_CTL for PSR2 enable")
                                status &= False
                    self.validate_feature()
                if status is False:
                    self.fail('PSR verification failed')
                logging.info("\tPASS: {0} verification on {1} on {2}".format(feature_str, adapter.name, panel))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestModeSet))
    test_environment.TestEnvironment.cleanup(test_result)
