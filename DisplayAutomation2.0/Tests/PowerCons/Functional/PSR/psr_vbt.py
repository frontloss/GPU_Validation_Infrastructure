#################################################################################################################
# @file         psr_vbt.py
# @brief        PSR vbt test
#
# @author       creddyy
#################################################################################################################
import ctypes

from Libs.Core import display_power
from Libs.Core.test_env import test_environment
from Libs.Core.vbt import vbt
from Tests.PowerCons.Functional.PSR.psr_base import *
from Tests.PowerCons.Modules import common, dpcd


##
# @brief        Exposed Class for Psr Wait time for Entry
class WaitTime(ctypes.LittleEndianStructure):
    _fields_ = [
        ("idle_frame_count", ctypes.c_uint8, 4),  # 0 to 3
        ("lines_to_wait_before_link_standby", ctypes.c_uint8, 1),  # 4 to 6
        ("reserved_7", ctypes.c_uint8, 1),  # 7 to 7
         ]


##
# @brief       Exposed Union for PSR block_9 wait time fields
class PsrWaitTime(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      WaitTime),
        ("value", ctypes.c_uint8)]


##
# @brief       Exposed structure for PSR block_9 feature support fields
class PsrConfig(ctypes.LittleEndianStructure):
    _fields_ = [
        ("FullLink", ctypes.c_uint8, 1),  # 0 to 0
        ("RequireAuxToWakeUp", ctypes.c_uint8, 1),  # 1 to 1
        ("reserved_7", ctypes.c_uint8, 6),  # 2 to 7
         ]


##
# @brief       Exposed Union for PSR block_9 feature support
class PsrFeatureBit(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      PsrConfig),
        ("value", ctypes.c_uint8)]


##
# @brief        This class contains PSR VBT test
class PsrVbtTest(PsrBase):

    ##
    # @brief        This function verifies PSR with VBT settings in AC mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["AC"])
    # @endcond
    def t_11_vbt(self):
        self.verify_psr_with_vbt(display_power.PowerSource.AC)
        self.verify_srd_block()

    ##
    # @brief        This function verifies PSR with VBT settings in DC mode
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["DC"])
    # @endcond
    def t_12_vbt(self):
        self.verify_psr_with_vbt(display_power.PowerSource.DC)
        self.verify_srd_block()

    ##
    # @brief        This function verifies PSR with VBT settings on applied power source
    # @param[in]    power_source enum AC/DC
    # @return       None
    def verify_psr_with_vbt(self, power_source):
        if not self.display_power_.set_current_powerline_status(power_source):
            self.fail("Failed to switch power line status to {0}(Test Issue)".format(
                power_source.name))
        self.power_source = power_source
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.psr_caps.is_psr_supported is False and (panel.pr_caps.is_pr_supported is False):
                    continue
                logging.info(f"STEP: Disable {self.feature_str} in VBT")
                if psr.update_vbt(adapter, panel, False) is False:
                    self.fail("Failed to update PSR settings in VBT")
                if adapter.lfp_count > 1:
                    dut.refresh_panel_caps(adapter)
                if psr.is_psr_enabled_in_driver(adapter, panel, self.feature):
                    self.fail(f"{self.feature_str} is not disabled")
                logging.info(f"PASS: {self.feature_str} is disabled in driver with VBT disable")
                logging.info(f"STEP: Enable {self.feature_str} in VBT")
                if psr.update_vbt(adapter, panel, True) is False:
                    self.fail(f"Failed to update {self.feature_str} settings in VBT")
                if adapter.lfp_count > 1:
                    dut.refresh_panel_caps(adapter)
                if psr.is_psr_enabled_in_driver(adapter, panel, self.feature) is False:
                    self.fail(f"{self.feature_str} is not enabled")
                logging.info(f"PASS: {self.feature_str} is enabled in driver with VBT enable")
        logging.info(f"PASS: {self.feature_str} feature verification with VBT")

    ##
    # @brief        This function verifies PSR with SRD VBT(Block 9) settings on applied power source
    # @return       None
    def verify_srd_block(self):
        status = True
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                if panel.is_lfp is False:
                    continue
                if panel.psr_caps.is_psr_supported is False:
                    continue
                if panel.pr_caps.is_pr_supported is True:
                    continue
                gfx_vbt = vbt.Vbt(adapter.gfx_index)
                # Skip VBT update for unsupported VBT version
                if gfx_vbt.version < 205:
                    logging.info("\tVbt version is < 205. Skip Vbt update")
                    return True
                panel_index = gfx_vbt.get_lfp_panel_type(panel.port)
                wait_time = PsrWaitTime()
                feature_data = PsrFeatureBit()
                feature_data.value = gfx_vbt.block_9.FeatureBit
                wait_time.value = gfx_vbt.block_9.WaitTime
                idle_frames = wait_time.idle_frame_count
                if self.feature >= psr.UserRequestedFeature.PSR_2:

                    # verify PSR2 VBT field data w.r.t MMIO programmed value
                    psr2_ctl = MMIORegister.read(
                        'PSR2_CTL_REGISTER', 'PSR2_CTL_' + panel.transcoder, adapter.name, gfx_index=adapter.gfx_index)
                    tp2_val = (gfx_vbt.block_9.Psr2ChannelEqualizationTime & (3 << (panel_index * 2)) >> (panel_index * 2))
                    # ToDO - Uncomment after confirmation from Dev team
                    # if psr2_ctl.tp2_time != tp2_val:
                    #     logging.error(
                    #         f"FAIL : Tp2 Expected val= {tp2_val} Actual = {psr2_ctl.tp2_time}")
                    #     status = False
                else:
                    # verify PSR1 VBT field data w.r.t MMIO programmed value
                    psr_cap = dpcd.PsrCapability(panel.target_id)
                    is_link_training_req = psr_cap.link_training_required_on_psr_exit
                    srd_ctl = MMIORegister.read('SRD_CTL_REGISTER', 'SRD_CTL_' + panel.transcoder, adapter.name,
                                                gfx_index=adapter.gfx_index)
                    if srd_ctl.idle_frame != 4:
                        logging.error(
                            f"FAIL : Idle frame count expected = 4 Actual = {srd_ctl.idle_frame}")
                        status = False
                    if is_link_training_req == 0:
                        if srd_ctl.tp1_time != gfx_vbt.block_9.PsrClockRecoveryTime:
                            logging.error(
                                f"FAIL : TP1 Expected val= {gfx_vbt.block_9.PsrClockRecoveryTime} "
                                f"Actual = {srd_ctl.tp1_time}")
                            status = False
                        if srd_ctl.tp2_tp3_time != gfx_vbt.block_9.Psr1ChannelEqualizationTime:
                            logging.error(
                                f"FAIL : TP2/Tp3 Expected val= {gfx_vbt.block_9.Psr1ChannelEqualizationTime} "
                                f"Actual = {srd_ctl.tp2_tp3_time}")
                            status = False
                    elif srd_ctl.tp1_time != 0x3 or srd_ctl.tp2_tp3_time != 0x3:
                        logging.error(
                            f"FAIL : TP1/TP2/Tp3 Expected val= 3 Actual = {srd_ctl.tp2_tp3_time}")
                        status = False
        if status is False:
            self.fail(f"FAIL: {self.feature_str} feature verification with VBT")
        logging.info(f"PASS: {self.feature_str} feature verification with VBT")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(PsrVbtTest))
    test_environment.TestEnvironment.cleanup(test_result)