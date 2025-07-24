######################################################################################
# @file         mipi_verify_bllp_config.py
# @brief        It verifies if BLLP configuration register bits are programmed correctly in accordance with what is
#               set in VBT.
# @details      Test is applicable only for LKF1 video mode.
#               CommandLine: python mipi_verify_bllp_config.py -mipi_a
#               Test will pass only if all required register bits are programmed correctly, otherwise it fails.
# @author       Sri Sumanth Geesala
######################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.MIPI.mipi_base import *
from registers.mmioregister import MMIORegister


##
# @brief        This class contains test to verify if BLLP configuration register bits are programmed correctly in
#               accordance with VBT
class MipiVerifyBllpConfig(MipiBase):

    ##
    # @brief        This function verifies if BLLP configuration register bits are programmed correctly in accordance
    #               with the VBT for every DSI port
    # @return       None
    def runTest(self):

        if (self.platform not in ['lkf1', 'tgl', 'ryf', 'adlp']):
            self.fail('Test is not applicable for %s platform. Aborting test.' % (self.platform))

        ##
        # for each DSI port
        for port in self.port_list:
            panel_index = self.mipi_helper.get_panel_index_for_port(port)
            VBT_BLLP = self.mipi_helper.gfx_vbt.block_52.MipiDataStructureEntry[panel_index].BlankingPacketsDuringBLLP

            if (self.mipi_helper.get_mode_of_operation(panel_index) != mipi_helper.VIDEO_MODE):
                self.fail(
                    'Port %s: Test is applicable only for Video mode. Current mode of operation is not video mode.' % (
                        port))

            ##
            # check LP/blanking packets in BLLP regions
            reg_trans_dsi_func_conf = MMIORegister.read("TRANS_DSI_FUNC_CONF_REGISTER", "TRANS_DSI_FUNC_CONF" + port,
                                                        self.platform)
            self.mipi_helper.verify_and_log_helper(register='TRANS_DSI_FUNC_CONF' + port,
                                              field='Blanking packet during BLLP',
                                              expected=VBT_BLLP,
                                              actual=reg_trans_dsi_func_conf.blanking_packet_during_bllp)

        ##
        # report test failure if fail_count>0
        if (self.fail_count + self.mipi_helper.verify_fail_count) > 0:
            self.fail(f'Some checks in the test have failed. Check error logs. '
                      f'No. of failures= {(self.fail_count + self.mipi_helper.verify_fail_count)}')



if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
