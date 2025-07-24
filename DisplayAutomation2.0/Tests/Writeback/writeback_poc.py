######################################################################################
# @file         writeback_poc.py
# @brief        The test scenario tests the following functionalities.
#               * Verify whether the devices are correctly plugged and enumerated and applies the display configuration.
#               * Verify whether the writeback buffer capture is working properly or not
# @author       Patel, Ankurkumar G
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.framebuffer_verification import framebuffer_verification
from Tests.Writeback.writeback_poc_base import *
from Libs.Core.display_config import display_config

##
# @brief     Contains unittest runTest function to verify whether writeback buffer capture is working properly or not
class WritebackBasic(WritebackPoCBase):

    ##
    # @brief        unittest runTest function
    # @param[in]    self; Object of writeback_poc base class
    # @return       void
    def runTest(self):

        # Plug and verify writeback devices
        logging.info("Step1 - Plug and verify writeback devices")
        self.assertEquals(self.plug_wb_devices(), True,
                          "Aborting the test as plug & Verify failed for writeback devices")
        logging.info("\tPASS: Writeback devices are plugged and enumerated successfully")

        self.apply_config()

        disp_cfg = display_config.DisplayConfiguration()
        current_config, display_list, display_and_adapter_info_list = disp_cfg.get_current_display_configuration_ex()
        for display_index in range(len(display_list)):
            if "WD_" in display_list[display_index] and \
                    display_and_adapter_info_list[display_index].adapterInfo.gfxIndex == 'gfx_0':
                target_id = display_and_adapter_info_list[display_index].TargetID
                break
        gfx_index = "gfx_0"
        tolerance = 2
        comparision_rect = framebuffer_verification.COMPARISION_RECT(0,0,1919,1079)
        framebuffer_verification.verify(gfx_index, target_id, comparision_rect, tolerance)

    def apply_config(self):
        wd_display = []
        enumerated_display = self.disp_config.get_enumerated_display_info()
        for display_count in range(0, enumerated_display.Count):
            port_type = str(CONNECTOR_PORT_TYPE(enumerated_display.ConnectedDisplays[display_count].ConnectorNPortType))
            if "WD_" in port_type:
                wd_display.append(port_type)
        status = self.disp_config.set_display_configuration_ex(enum.SINGLE, wd_display,
                                                               self.disp_config.get_enumerated_display_info())
        if status is False:
            self.fail('Failed to apply display configuration')


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
