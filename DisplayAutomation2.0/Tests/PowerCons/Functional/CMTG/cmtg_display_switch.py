########################################################################################################################
# @file         cmtg_display_switch.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification in with display switch scenarios.
# @author       Chandrakanth Reddy
########################################################################################################################
import time

from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CMTG.cmtg_base import *


##
# @brief        Contains basic CMTG display switch tests
class CmtgDisplaySwitch(CmtgBase):

    ##
    # @brief        This function verifies CMTG with Display switch scenarios
    # @return       None
    def t_10_display_switch(self):
        for adapter in dut.adapters.values():
            lfp_panels = []
            ext_panels = []
            for panel in adapter.panels.values():
                if panel.is_lfp is True:
                    lfp_panels.append(panel.port)
                else:
                    ext_panels.append(panel.port)

            if len(lfp_panels) > 1:
                ##
                # Dual eDP case
                if len(ext_panels) == 0:
                    ##
                    # Dual eDP only
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]
                else:
                    ##
                    # Dual eDP with external panel
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[1]]),
                                        (enum.EXTENDED, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.CLONE, [lfp_panels[0], lfp_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]

            else:
                ##
                # Single eDP case
                if len(ext_panels) > 1:
                    ##
                    # Single eDP with multiple external panels
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0],
                                                         ext_panels[1]]),
                                        (enum.SINGLE, [lfp_panels[0]])
                                        ]
                elif len(ext_panels) == 1:
                    ##
                    # Single eDp with single external panel
                    self.config_list = [(enum.SINGLE, [lfp_panels[0]]),
                                        (enum.EXTENDED, [lfp_panels[0], ext_panels[0]]),
                                        (enum.CLONE, [lfp_panels[0], ext_panels[0]]),
                                        (enum.SINGLE, [lfp_panels[0]])]

            for config in self.config_list:
                logging.info("Applying {0} on {1}".format(config[0], config[1]))
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail("Failed to apply display configuration")
                time.sleep(5)

                # Update pipe in panel object in case of dynamic allocation
                dut.refresh_panel_caps(adapter)

                for panel in adapter.panels.values():
                    if panel.is_lfp and config[0] == enum.SINGLE:
                        if panel.psr_caps.is_psr2_supported or panel.pr_caps.is_pr_supported:
                            if cmtg.verify(adapter, [panel]) is False:
                                self.fail("CMTG verification failed")
                            if panel.vrr_caps.is_vrr_supported:
                                if cmtg.verify_cmtg_vrr(adapter, panel, self.method) is False:
                                    self.fail("CMTG VRR sequence verification failed")
                                logging.info("CMTG VRR sequence verification successful")
                            logging.info("CMTG verification successful")
                        else:
                            status = cmtg.verify_cmtg_status(adapter)
                            if adapter.name in common.PRE_GEN_15_PLATFORMS:
                                if status:
                                    self.fail("CMTG enabled in non-PSR2 panel")
                                logging.info("CMTG is not enabled in non PSR2 panel as expected")
                            # GEN15+ CMTG will be enabled on non-PSR panel as well
                            else:
                                if status is False:
                                    self.fail("CMTG not enabled in non-PSR2 panel")
                                logging.info("CMTG enabled in non PSR2 panel as expected")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)