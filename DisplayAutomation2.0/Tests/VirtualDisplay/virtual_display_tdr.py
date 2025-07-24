########################################################################################################################
# @file          virtual_display_tdr.py
# @brief         The script enables/disable virtual display by writing into the registry, restart the drivers, verifies
#                and applies display configuration obtained from the command line.
#                * Verifies virtual display before sleep event then genarates TDR 3 times
#                * Verifies virtual display after sleep event.
# @author        Suraj Gaikwad, Sridharan.V
########################################################################################################################

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Tests.VirtualDisplay.virtual_display_base import *

##
# @brief     It contains unittest runTest function to verify virtual displays after entering and resuming from S3
class VirtualDisplayTDR(VirtualDisplayBase):
    ##
    # @brief        Unittest runTest function
    # @param[in]    self; Object of virtual display base class
    # @return       void
    def runTest(self):

        # Enable and verify virtual displays
        self.enable_disable_virtual_display()

        # Set the display config as provided in command line
        topology = eval("enum.%s" % (self.cmd_line_param['CONFIG']))
        if self.display_config.set_display_configuration_ex(topology, self.displays_list) is False:
            self.fail('Failed to apply display configuration %s %s' %
                      (DisplayConfigTopology(topology).name, self.displays_list))

        logging.info('Successfully applied the display configuration as %s %s' %
                     (DisplayConfigTopology(topology).name, self.displays_list))

        # Verify virtual displays before sleep event
        if self.verify_virtual_display() is False:
            self.fail('Failed to verify virtual displays before sleep event')
        logging.info('Successfully verified virtual displays before sleep event. Virtual displays count : %s'
                     % self.number_virtual_displays)

        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))

        # Generate TDR 3 times
        for index in range(3):

            # Generate & Verify TDR
            if display_essential.generate_tdr(gfx_index='gfx_0', is_displaytdr=True) is not True:
                self.fail('Failed to generate TDR')

            if display_essential.detect_system_tdr(gfx_index='gfx_0') is not True:
                self.fail('Iteration {} : TDR generated successfully'.format(index + 1))

            time.sleep(15)

            # Verify virtual displays after sleep event
            if self.verify_virtual_display() is False:
                self.fail('Failed to verify virtual displays after sleep event')
            logging.info('Successfully verified virtual displays after sleep event. Virtual displays count : %s'
                         % self.number_virtual_displays)

        if display_essential.clear_tdr() is True:
            logging.info("TDR clear successful")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
