#######################################################################################################################
# @file         lace_min_lux_inf_customization_iet_verification.py
# @addtogroup   Test_Color
# @section      lace_min_lux_inf_customization_iet_verification
# @remarks      @ref lace_min_lux_inf_customization_iet_verification.py \n
#               The test script is developed with an intent to perform validation for the RCR VSRI- and VSRI-4900.
#               The RCR enables OEMs to customize min ambient light LUX input
#               for LACE to kick-in instead of the hardcoded 1000nits
#               This customization, done through Driver INF,is applicable to all three Aggressiveness levels.

#               Test script invokes Driver PCEscape call to enable LACE with Lux & Aggr Levels
#               If the registry key customization is not there,
#               then driver will fall back to the default T0,T1,T2 values
#               Register verification is performed to verify if LACE is enabled/disabled appropriately
#               along with IET Verification between Frames after applying the Lux and AggrLevels
# CommandLine:  python lace_min_lux_inf_customization_iet_verification.py -edp_a -config SINGLE
# CommandLine:  python lace_min_lux_inf_customization_iet_verification.py -edp_a -edp_b -config CLONE
# CommandLine:  python lace_min_lux_inf_customization_iet_verification.py -mipi_a -config SINGLE
# CommandLine:  python lace_min_lux_inf_customization_iet_verification.py -mipi_a -mipi_c -config CLONE

# @author       Smitha B
#######################################################################################################################
import win32api
from Tests.Color.LACE.lace_base import *


class LACEMinMaxINFCustWithIETVerify(LACEBase):
    def runTest(self):

        min_lux_customization_list = [("LaceMinLuxForLowAggressiveness",15000), ("LaceMinLuxForModerateAggressiveness", 6000),
                                      ("LaceMinLuxForHighAggressiveness", 3500)]
        ##
        # The list is constructed in such a way that, for each aggressivessness levels
        # lux value > T0 to verify if LACE is enabled and IET is fetched
        # lux value > LaceMaxLuxValue to verify no change in IETs since lux > MaxValue
        aggr_lux_combo_list = [(15001, enum.AGGR_LEVEL_LOW), (25000, enum.AGGR_LEVEL_LOW),
                               (6001, enum.AGGR_LEVEL_MODERATE), (25000, enum.AGGR_LEVEL_MODERATE),
                               (3505, enum.AGGR_LEVEL_HIGH), (25000, enum.AGGR_LEVEL_HIGH)]

        ##
        # Set the Min and Max INF customization Registry Keys
        for index in range(0, len(min_lux_customization_list)):
            if not perform_registry_customization(min_lux_customization_list[index]):
                logging.error("Failed to set Registry_Key %s for Lux %s" % (
                    min_lux_customization_list[index][0], min_lux_customization_list[index][1]))
                self.fail()
            else:
                logging.info("Successfully set Registry_Key %s for Lux %s" % (
                    min_lux_customization_list[index][0], min_lux_customization_list[index][1]))
        ##
        # Perform a DFT flip and display an image
        IMAGE_FILE = "earth.bmp"
        ##
        # Enable DFT
        self.mpo.enable_disable_mpo_dft(True, 1)

        ##
        # Set Cursor Position to (500,500)
        win32api.SetCursorPos((500, 500))
        self.display_staticimage(IMAGE_FILE)
        logging.info("Image Displayed!!")
        time.sleep(5)
        for index in range(len(self.lfp_target_ids)):
            iet_data_single_tile = [0]
            for aggr_lux_index in range(len(aggr_lux_combo_list)):
                lux = aggr_lux_combo_list[aggr_lux_index][0]
                aggressiveness_level = aggr_lux_combo_list[aggr_lux_index][1]
                logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))
                if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[index], lux=lux,
                                                                   lux_operation=True,
                                                                   aggressiveness_level=aggressiveness_level,
                                                                   aggressiveness_operation=True):

                    logging.info("Lux and aggressiveness levels set successfully")
                    logging.info("Verifying for underrun after setting Lux and Aggressiveness Levels")
                    if self.underrun.verify_underrun():
                        logging.error("Underrun Occured")
                    current_pipe = get_current_pipe(self.connected_list[index])
                    self.actual_lace_status = get_actual_lace_status(current_pipe)
                    self.expected_lace_status = get_expected_lace_status(lux, aggressiveness_level)

                    time.sleep(5)

                    if self.expected_lace_status == self.actual_lace_status:
                        logging.info("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        logging.info("Expectation : LACE %s; Actual : LACE %s" % (
                            self.expected_lace_status, self.actual_lace_status))

                        # Disable IE enable bit before IET read
                        self.disable_ieenable_function()
                        time.sleep(2)
                        # Get IET from registers
                        iet_data = read_iet_from_registers_for_single_tile(self.lfp_pipe_ids[index], 0, 0)
                        logging.debug("IET Data is")
                        logging.debug(iet_data)
                        if iet_data != iet_data_single_tile[-1]:
                            logging.info("IET Data has changed between Current and Previous Frame AS EXPECTED")
                        else:
                            logging.error("IET Data has NOT changed between Current and Previous Frame AS EXPECTED")

                        ##
                        # Append the Current Frame's IET Data to the list to compare with Previous Frame's IET Data
                        iet_data_single_tile.append(iet_data)

                    else:
                        logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                        logging.error("Expectation : LACE %s; Actual : LACE %s" % (
                            self.expected_lace_status, self.actual_lace_status))
                        self.fail("LACE is not enabled")
                else:
                    logging.error("Failed to set lux and aggressiveness levels")
                    logging.error("Lux = %s AggressivenessLevel %s" % (lux, aggressiveness_level))
                    self.fail("Failed to set lux and aggressiveness levels")



        ##
        # Disable DFT
        self.mpo.enable_disable_mpo_dft(False, 1)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
