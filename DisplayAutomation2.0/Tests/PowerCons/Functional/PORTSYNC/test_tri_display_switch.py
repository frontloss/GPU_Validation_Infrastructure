#######################################################################################################################
# @file         test_tri_display_switch.py
# @addtogroup   Powercons
# @section      PORTSYNC
# @brief        Test for port sync in display switch scenarios SD EDP, Dual eDP Clone and extended,
#
# @author       Bhargav Adigarla
#######################################################################################################################
from Tests.PowerCons.Functional.PORTSYNC.port_sync_base import *
from Libs.Core.test_env import test_environment
from Libs.Core.display_config import display_config as config_
from Libs.Core import app_controls
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains basic port sync tests with tri display scenario
class TestDisplaySwitch(PortSyncBase):

    ##
    # @brief        this function verifies port sync with display switch scenario
    # @return       None
    def t_10_display_switch(self):
        for adapter in dut.adapters.values():
            ##
            # Dual eDP + external display only
            # Display Switch will be in below sequence. objective here is to verify port sync enabled
            config_list = [(enum.EXTENDED, [self.lfp_panels[0].port, self.lfp_panels[1].port],
                            [self.lfp_panels[0], self.lfp_panels[1]]),
                           (enum.SINGLE, [self.ext_panels[0].port], [self.ext_panels[0]]),
                           (enum.CLONE, [self.lfp_panels[0].port, self.lfp_panels[1].port],
                            [self.lfp_panels[0], self.lfp_panels[1]]),
                           (enum.SINGLE, [self.ext_panels[0].port], [self.ext_panels[0]])]

            for config in config_list:
                if self.display_config_.set_display_configuration_ex(config[0], config[1]) is False:
                    self.fail("Applying Display config {0} {1} Failed".
                              format(config_.DisplayConfigTopology(config[0]).name, config[1]))
                logging.info("Applied Display config {0} {1}".
                             format(config_.DisplayConfigTopology(config[0]).name, config[1]))

                # Update pipe in panel object in case of dynamic allocation
                self.update_dynamic_pipe(config[1])

                if config[2][0].is_lfp:
                    if port_sync.verify(adapter, config[2]) is True:
                        logging.info("\tPort sync programming verification successful")

                        if len(config[2]) == 2:
                            monitors = app_controls.get_enumerated_display_monitors()
                            monitor_ids = [_[0] for _ in monitors]
                            etl_file, _ = workload.run(workload.SCREEN_UPDATE, [monitor_ids])

                            if port_sync.verify_vbis(config[2], etl_file) is False:
                                self.fail("\tPort sync VBI timing verification Failed")

                            logging.info("\tPort sync functional verification successful")

                    else:
                        self.fail("\tPort sync verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestDisplaySwitch))
    test_environment.TestEnvironment.cleanup(test_result)