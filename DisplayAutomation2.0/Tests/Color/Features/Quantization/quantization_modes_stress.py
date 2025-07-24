#################################################################################################
# @file         quantization_modes_stress.py
# @brief        This scripts contain functions to apply the all the modes and  will perform below functionalities
#               1.To configure avi info for the display
#               2.To perform register verification OCSC,Coeff,Pre/post off and quantization range
# @author       Vimalesh D
#################################################################################################
import unittest
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Common.common_utility import apply_mode
from Tests.Color.Features.Quantization.quantization_test_base import *


##
# @brief - Quantisation basic test
class QuantisationTestModesStress(QuantizationTestBase):

    ##
    # @brief test_01_mode_stress() - Function to perform stress test by applying all supported modes and
    #                                to perform register verification on all panels.
    # @param[in] self
    # @return None
    @unittest.skipIf(get_action_type() != "STRESS",
                     "Skip the  test step as the action type is not Monitor Turnoff_on")
    def test_01_mode_stress(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp is False:

                    all_supported_modes = self.config.get_all_supported_modes([panel.display_and_adapterInfo])
                    for keys, modes in all_supported_modes.items():
                        for mode in modes:
                            if not apply_mode(panel.display_and_adapterInfo, mode.HzRes, mode.VtRes, mode.refreshRate,
                                              mode.scaling):
                                self.fail("Failed to apply display mode {0} X {1} @ {2} Scaling : {3}"
                                          .format(mode.HzRes, mode.VtRes, mode.refreshRate, mode.scaling))

                            if panel.is_active and panel.is_lfp is False:
                                plane_id = color_etl_utility.get_plane_id(panel.pipe, gfx_index)
                                self.enable_and_verify(panel.display_and_adapterInfo,
                                                       adapter.platform, panel.pipe, plane_id, panel.transcoder,
                                                       panel.connector_port_type, configure_avi=True)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Configure the quantization range and perform verification on all panels")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
