#######################################################################################################################
# @file         test_vbt_disable.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in symmetric Dual eDP non PSR scenario,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Libs.Core.test_env import test_environment
from Libs.Core import app_controls, display_essential
from Tests.PowerCons.Modules import workload
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *


##
# @brief        This class contains basic port sync tests with VBT enable disable
class TestVbtDisable(PortSyncBase):

    ##
    # @brief        this function verifies port sync with VBT enable/disable
    # @return       None
    def t_10_test_vbt_disable(self):
        self.verify_basic()

        gfx_vbt = Vbt()
        set_vbt = False
        self.panel1_index = gfx_vbt.block_40.PanelType
        panel1_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (1 << self.panel1_index)) >> \
                               self.panel1_index
        if panel1_port_sync_bit != 0:
            gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (0 << self.panel1_index)
            set_vbt = True
        else:
            logging.info("Port sync disabled in VBT for panel1")

        if len(self.lfp_panels) == 2:
            self.panel2_index = gfx_vbt.block_40.PanelType2
            panel2_port_sync_bit = (gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (
                    1 << self.panel2_index)) >> self.panel2_index
            if panel2_port_sync_bit != 0:
                gfx_vbt.block_42.DualLfpPortSyncEnablingBits = \
                    gfx_vbt.block_42.DualLfpPortSyncEnablingBits & (0 << self.panel2_index)
                set_vbt = True
            else:
                logging.info("Port sync disabled in VBT for panel2")

        if set_vbt is True:
            if gfx_vbt.apply_changes() is False:
                self.fail('Setting VBT block 52 failed')
            else:
                is_vbt_modified = True
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("Failed to restart driver")
                gfx_vbt.reload()
                logging.info("Port sync disabled in VBT for panel1")
                logging.info("Port sync disabled in VBT for panel2")

        for adapter in dut.adapters.values():
            if cmtg.verify_cmtg_status(adapter) is True:
                panels = list(adapter.panels.values())
                panel1_slave_status = cmtg.verify_cmtg_slave_status(adapter, panels[0])
                panel2_slave_status = cmtg.verify_cmtg_slave_status(adapter, panels[1])
                if panel1_slave_status == 1 and panel2_slave_status == 1:
                    self.fail(f"\tCMTG slave status enabled after power event "
                              f"panel1 {panel1_slave_status} panel2 {panel2_slave_status}")
            else:
                self.fail("\tCMTG status disabled")
            logging.info("PortSync verification successful")

    ##
    # @brief        this function verifies port sync with VBT enable/disable
    # @return       None
    def verify_basic(self):
        for adapter in dut.adapters.values():
            if port_sync.verify(adapter, self.lfp_panels) is True:
                logging.info("\tPort sync programming verification successful")

                if len(self.lfp_panels) == 2:
                    monitors = app_controls.get_enumerated_display_monitors()
                    monitor_ids = [_[0] for _ in monitors]
                    etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                    if port_sync.verify_vbis(self.lfp_panels, etl_file) is False:
                        self.fail("\tPort sync VBI timing verification Failed")

                    logging.info("\tPort sync functional verification successful")
            else:
                self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestVbtDisable))
    test_environment.TestEnvironment.cleanup(test_result)