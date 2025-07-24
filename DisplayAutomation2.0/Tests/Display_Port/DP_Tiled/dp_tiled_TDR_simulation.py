#######################################################################################################################
# @file         dp_tiled_TDR_simulation.py
# @brief        This test verifies TDR generation and recovery
# @details      Ensure system recovers from TDR and after recovery Display comes up back in 8k/5k.
# @author       Amanpreet Kaur Khurana, Ami Golwala, Veena Veluru
#######################################################################################################################
import ctypes

from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.Verifier.common_verification_args import VerifierCfg, Verify
from Libs.Core.wrapper import control_api_args, control_api_wrapper
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledGenerateTDR(DisplayPortBase):
    ##
    # @brief        This test plugs required displays, set config, applies max mode, simulates TDR.
    # @return       None
    def runTest(self):
        ##
        # Plug the Tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set display configuration with topology as SINGLE
        self.set_config(self.config, no_of_combinations=1)
        ##
        # Apply 5K3K/8k4k resolution and check for applied mode
        self.apply_tiled_max_modes()
        VerifierCfg.tdr = Verify.SKIP
        logging.debug("Updated config under-run:{}, tdr:{}".format(VerifierCfg.underrun.name, VerifierCfg.tdr.name))
        ##
        # Simulate TDR
        for adapter in self.adapter_list_to_verify:
            if display_essential.generate_tdr(gfx_index=adapter, is_displaytdr=True) is True:
                logging.info("TDR generated Successfully for adapter {}".format(adapter))
            time.sleep(Delay_5_Secs)
            time.sleep(Delay_5_Secs)

        ##
        # check TDR status
        for adapter in self.adapter_list_to_verify:
            tdr_status = display_essential.detect_system_tdr(gfx_index=adapter)
            time.sleep(Delay_5_Secs)
            if tdr_status is True:
                logging.info("TDR detected successful")
            else:
                logging.error("[Test Issue]: TDR failed for adapter {}. Exiting....".format(adapter))
                gdhm.report_bug(
                    title="[Interfaces][DP_Tiled] Failed to simulate TDR",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail()

        if display_essential.clear_tdr() is True:
            logging.info("TDR cleared successfully post TDR generation")

        displayEncoderProperties = control_api_args.ctl_adapter_display_encoder_properties_t()
        displayEncoderProperties.Size = ctypes.sizeof(displayEncoderProperties)
        enumerated_display_info = self.display_config.get_enumerated_display_info()

        logging.info("IGCL Display Type Verification")
        for index in range(enumerated_display_info.Count):
            if control_api_wrapper.get_display_encoder_properties(displayEncoderProperties, plugged_target_ids[index]):
                if plugged_target_ids[index] == \
                        displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID:
                    logging.info("Display Target_ID {}, EncoderConfigFlags {}"
                                 .format(displayEncoderProperties.Os_display_encoder_handle.WindowsDisplayEncoderID,
                                         displayEncoderProperties.EncoderConfigFlags))
                    if control_api_args.ctl_encoder_config_flags_v.VESA_TILED_DISPLAY.value and \
                            displayEncoderProperties.EncoderConfigFlags:
                        logging.info("Tiled Display Enabled {}".format(
                            control_api_args.ctl_encoder_config_flags_v.VESA_TILED_DISPLAY.value and
                            displayEncoderProperties.EncoderConfigFlags))
                        logging.info("Pass: IGCL Tiled Display Type Verified")
                    else:
                        logging.error("Tiled Display Config Flag is not reported from IGCL {}".format(
                            control_api_args.ctl_encoder_config_flags_v.VESA_TILED_DISPLAY.value and
                            displayEncoderProperties.EncoderConfigFlags))

        ##
        # check current mode
        flag = self.verify_tiled_mode()
        if flag:
            logging.info("Current mode is same as before TDR")
        else:
            logging.error("[Driver Issue]: Current mode is not same as before TDR. Exiting....")
            # Gdhm bug reporting handled in verify_tiled_mode
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
