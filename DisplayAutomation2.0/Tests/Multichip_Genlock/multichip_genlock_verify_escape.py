######################################################################################
# @file         multichip_genlock_verify_escape.py
# @brief        These tests verify whether driver escape related to genlock are functioning correct or not.
# @details      Its run either with multiple displays on single DUT or displays across multiple DUTs.
# 1) Sample cmdline for genlock on single system:
# multichip_genlock_verify_escape.py -dp_b -dp_c -master_dut true -master_display dp_c
# 2) If you need test to not disable genlock and wait, make cmdline as below (useful to run workloads during Genlock):
# multichip_genlock_verify_escape.py -hdmi_b -hdmi_c -master_dut true -master_display dp_c -wait_with_genlock true
# 3) Sample cmdlines for genlock on multi system (append "-wait_with_genlock true" if needed just like above):
# Master: multichip_genlock_verify_escape.py -dp_b -dp_c -master_dut true -master_display dp_c
# Slave: multichip_genlock_verify_escape.py -dp_b -dp_d
#
# @author       Sri Sumanth Geesala
######################################################################################

import logging
import sys
import unittest
from Libs.Core import enum
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.driver_escape import get_set_genlock
from Tests.Multichip_Genlock.multichip_genlock_base import MultichipGenlockBase


##
# @brief Class for Multichip Genlock test that verifies the feature by enabling/disabling via escape call
class MultichipGenlockVerifyEscape(MultichipGenlockBase):

    ##
    # @brief Test to enable genlock and verify the registers
    # @return None
    def runTest(self):

        # Ensure all genlock displays are active.
        adapter_list = ['gfx_0'] * len(self.display_list)
        self.set_and_validate_config(enum.EXTENDED if len(self.display_list) > 1 else enum.SINGLE,
                                     self.display_list, adapter_list)

        logging.info('-----------Before enabling genlock, register values are:-----------')
        self.print_verify_genlock_registers(self.display_list, verify_prog=False)

        # Fill genlock args. Apply SD config with LFP or a slave display; this is required to do SD config with
        # master display post enabling genlock.
        self.genlock_args = self.fill_genlock_args(self.display_list)
        if self.lfp_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.lfp_display], adapter_list)
        elif len(self.slave_disp_list) > 0:
            self.set_and_validate_config(enum.SINGLE, [self.slave_disp_list[0]], adapter_list)

        # Enable genlock
        enumerated_displays = self.disp_config.get_enumerated_display_info()
        target_id = self.disp_config.get_target_id(self.display_list[0], enumerated_displays)
        display_and_adapter_info = self.disp_config.get_display_and_adapter_info(target_id)
        if get_set_genlock(display_and_adapter_info, True, self.genlock_args):
            logging.info(f'Enable genlock successful on {display_and_adapter_info.adapterInfo.gfxIndex}')
        else:
            logging.error(f'Enable genlock failed on {display_and_adapter_info.adapterInfo.gfxIndex}')
            self.fail('Enable genlock call failed')

        # Do display switching so as to do modeset on all displays after genlock is enabled.
        # Post enabling genlock, first modeset should be of master.
        if self.master_display is not None:
            self.set_and_validate_config(enum.SINGLE, [self.master_display], adapter_list)
        self.set_and_validate_config(enum.EXTENDED if len(self.display_list) > 1 else enum.SINGLE,
                                     self.display_list, adapter_list)

        # Verify Genlock bits register programming
        logging.info('-----------After enabling genlock and doing modeset on all the genlock displays:-----------')
        if not self.print_verify_genlock_registers(self.display_list):
            self.fail('Genlock register verification failed.')

        # Disable genlock
        self.disable_genlock_and_do_modeset_on_displays()

        logging.info('-----------After disabling genlock, register values are:-----------')
        self.print_verify_genlock_registers(self.display_list, verify_prog=False)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
