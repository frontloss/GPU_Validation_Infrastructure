##############################################################################################
# \file             hw_3d_lut_with_psr_coexistence.py
# \addtogroup       Test_Color
# \section          hw_3d_lut_with_psr_coexistence
# \ref              hw_3d_lut_with_psr_coexistence.py \n
# \remarks          This is a custom script which is used to verify co-existence of HW3DLUT and PSR1/PSR2
#
# CommandLine:      python hw_3d_lut_with_psr_coexistence.py -edp_a -PSRVERSION PSR1
#                   python hw_3d_lut_with_psr_coexistence.py -edp_a -PSRVERSION PSR2
# \author           Smitha B
###############################################################################################
from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Hw_3D_LUT.hw_3d_lut_base import *
from Tests.Color.Hw_3D_LUT.hw_3d_lut_verification import *
from Tests.PowerCons.Functional.PSR import psr
from Tests.PowerCons.Modules import dut


class Hw3DLutWithPSRCoExistence(unittest.TestCase):
    feature, psr_version, panels, module_name, psr_reg = None, None, None, None, None
    hw3dlut_verify = Hw3DLutVerification()
    hw3dlut_base = Hw3DLUTBase()

    ##
    # @brief        Get PSR Version from command line
    # @param[in]    None
    # @return       Returns the PSR Version from command line
    def get_psr_version(self):
        for index in range(0, len(sys.argv)):
            if sys.argv[index][:4].upper() == 'PSR1':
                return psr.UserRequestedFeature.PSR_1
            elif sys.argv[index][:4].upper() == 'PSR2':
                return psr.UserRequestedFeature.PSR_2
            else:
                if index == len(sys.argv):
                    logging.error("Check PSRVersion given in the command line")
                    self.fail("Check PSRVersion given in the command line")

    def setUp(self):
        ##
        # Prepare the test DUT : Plugs the display, applies the config
        dut.prepare()
        self.panels = dut.adapters['gfx_0'].panels.values()
        self.feature = self.get_psr_version()
        if psr.is_feature_supported_in_panel(self.panels[0].target_id, self.feature):
            logging.info("Panel supports PSR")
        else:
            logging.error("Panel does not support PSR, please plan the test with correct panel")
            self.fail("Panel does not support PSR, please plan the test with correct panel")

    def runTest(self):
        ##
        # Enable PSR based on the PSRVersion passed as command line parameter
        for adapters in dut.adapters.values():
            psr_status = psr.enable(adapters.gfx_index, self.feature)
            if psr_status is False:
                self.fail(f"FAILED to enable PSR")
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()
                if status is False:
                    self.fail("FAILED to restart the driver")

            if psr.is_psr_enabled_in_driver(adapters, self.panels[0], self.feature) is False:
                logging.error(f"PSR not enabled")
                self.fail(f"PSR not enabled")
            logging.info(f"PSR enabled")

            gfx_index = self.hw3dlut_base.internal_gfx_adapter_index
            ##
            # Apply and verify HW3DLUT
            cui_dpp_hw_lut_info = DppHwLutInfo(self.panels[0].target_id, DppHwLutOperation.UNKNOWN.value, 0)
            ##
            # Get the DPP Hw LUT info
            result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(gfx_index, cui_dpp_hw_lut_info)
            if result is False:
                logging.error(f'Escape call failed : get_dpp_hw_lut() for {self.panels[0].target_id}')
            path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\\Hw3DLUT\\CustomLUT\\CustomLUT_no_G.bin")

            cui_dpp_hw_lut_info = DppHwLutInfo(self.panels[0].target_id, DppHwLutOperation.APPLY_LUT.value,
                                               cui_dpp_hw_lut_info.depth)
            if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
                self.fail(f'Invalid bin file path provided : {path}!')
            ##
            # Set the DPP Hw LUT Info
            result = driver_escape.set_dpp_hw_lut(gfx_index, cui_dpp_hw_lut_info)
            if result is False:
                logging.error(f'Escape call failed : set_dpp_hw_lut() for {self.panels[0].target_id}')
            hw_3d_lut_status, hw_lut_buffer_status = self.hw3dlut_verify.verify_3dlut(self.panels[0].pipe,
                                                                                      "CustomLUT_no_G.bin")
            if hw_3d_lut_status == "DISABLED":
                gdhm_report_app_color(
                    title="[COLOR]Verification of HW_3D_LUT failed due to 3D_LUT status: Disabled")
                self.fail()
            if hw_lut_buffer_status == "NOT_LOADED":
                gdhm_report_app_color(
                    title="[COLOR]Hardware did not load the lut buffer into internal working RAM")
                self.fail()

            if psr.is_psr_enabled_in_driver(adapters, self.panels[0], self.feature):
                logging.info("Verification of co-existence of PSR feature with HW3DLUT successful")
            else:
                logging.info("Verification of co-existence of PSR feature with HW3DLUT failed")
                self.fail("Verification of co-existence of PSR feature with HW3DLUT failed")

    def tearDown(self):
        gfx_index = self.hw3dlut_base.internal_gfx_adapter_index
        ##
        # Apply the Default Bin to restore the system
        cui_dpp_hw_lut_info = DppHwLutInfo(self.panels[0].target_id, DppHwLutOperation.UNKNOWN.value, 0)
        path = os.path.join(test_context.SHARED_BINARY_FOLDER, "Color\Hw3DLUT\CustomLUT\CustomLUT_default.bin")
        result, cui_dpp_hw_lut_info = driver_escape.get_dpp_hw_lut(gfx_index, cui_dpp_hw_lut_info)
        if result is False:
            logging.error(f'Escape call failed : get_dpp_hw_lut() for {self.panels[0].target_id}')

        cui_dpp_hw_lut_info = DppHwLutInfo(self.panels[0].target_id, DppHwLutOperation.APPLY_LUT.value,
                                           cui_dpp_hw_lut_info.depth)
        if cui_dpp_hw_lut_info.convert_lut_data(path) is False:
            self.fail(f'Invalid bin file path provided : {path}!')

        ##
        # Set the DPP Hw LUT Info
        result = driver_escape.set_dpp_hw_lut(gfx_index, cui_dpp_hw_lut_info)
        if result is False:
            logging.error(f'Escape call failed : set_dpp_hw_lut() for {self.panels[0].target_id}')

        ##
        # Disable PSR, PSRVersion is passed as command line parameter
        for adapter in dut.adapters.values():
            psr_status = psr.disable(adapter.gfx_index, self.feature)
            if psr_status is True:
                status, reboot_required = display_essential.restart_gfx_driver()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
