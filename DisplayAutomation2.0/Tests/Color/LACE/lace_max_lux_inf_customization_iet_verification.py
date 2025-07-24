#######################################################################################################################
# @file         lace_max_lux_inf_customization_iet_verification.py
# @addtogroup   Test_Color
# @section      lace_max_lux_inf_customization_iet_verification
# @remarks      @ref lace_min_max_inf_customization.py \n
#               The test script is developed with an intent to perform validation for the RCR VSRI-4900.
#               The RCR enables OEMs to customize min ambient light LUX input for LACE to kick-in instead of the hardcoded 1000nits
#               This customization, done through Driver INF,is applicable to all three Aggressiveness levels.
#
#               The "Max" value is the maximum Lux input after which Driver does not perform any further contrast enhancement.
#               Hence, setting each of the Aggressiveness level, and verifying if the value set beyond the LaceMaxLuxValue
#               is affecting the IET change
#               Registry key to configure the "Max" value is:
#                   "LaceMaxLuxValue"
#               Test script invokes Driver PCEscape call to enable LACE with Lux and Aggressiveness Levels and with the registry keys
#               If the registry key customization is not there, then driver will fall back to the default T0,T1,T2 values
#               Register verification is performed to verify if LACE is enabled/disabled appropriately along with the IET Verification
# CommandLine:  python lace_max_lux_inf_customization_iet_verification.py -edp_a
# @author       Smitha B
#######################################################################################################################
import win32api
from Tests.Color.LACE.lace_base import *


class LACEMaxINFCustWithIETVerification(LACEBase):
    def runTest(self):

        max_lux_customization_list = [("LaceMaxLuxValue", 25000)]

        aggr_lux_beyond_max_val_list = [(25001, enum.AGGR_LEVEL_LOW), (30000, enum.AGGR_LEVEL_LOW),
                               (25100, enum.AGGR_LEVEL_MODERATE), (35000, enum.AGGR_LEVEL_MODERATE),
                               (35005, enum.AGGR_LEVEL_HIGH), (40000, enum.AGGR_LEVEL_HIGH)]

        ##
        # Set the Max INF customization Registry Key
        for index in range(len(max_lux_customization_list)):
            if not perform_registry_customization(max_lux_customization_list[index]):
                logging.error("Failed to set Registry_Key %s for Lux %s" % (
                    max_lux_customization_list[index][0], max_lux_customization_list[index][1]))
                self.fail()
            else:
                logging.info("Successfully set Registry_Key %s for Lux %s" % (
                    max_lux_customization_list[index][0], max_lux_customization_list[index][1]))
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

            ##
            # Iterate through the lisst having aggr_levels and corresponding Lux values
            for aggr_lux_index in range(len(aggr_lux_beyond_max_val_list)):
                lux = aggr_lux_beyond_max_val_list[aggr_lux_index][0]
                aggressiveness_level = aggr_lux_beyond_max_val_list[aggr_lux_index][1]
                logging.info("Setting Lux = %s and AggressivenessLevel %s" % (lux, aggressiveness_level))
                if driver_escape.als_aggressiveness_level_override(display_and_adapter_info=self.lfp_target_ids[index],
                                                                   lux=lux,
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
                        ##
                        # For each Aggr_levels, Driver escape is called
                        # Expecting change in the IET only when there is a change in the aggressiveness level
                        if aggr_lux_index % 2 == 0:
                            if iet_data != iet_data_single_tile[-1]:
                                logging.info("PASS : IET Data has changed between Current and Previous Frame AS EXPECTED")
                            else:
                                logging.error("FAIL : IET Data NOT changed between Current and Previous Frame EXPECTED")
                        else:
                            if iet_data == iet_data_single_tile[-1]:
                                logging.info("PASS : IET Data has NOT changed between Current and Previous Frame AS EXPECTED")
                            else:
                                logging.error("FAIL : IET Data changed between Current and Previous Frame NOT EXPECTED")

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


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
