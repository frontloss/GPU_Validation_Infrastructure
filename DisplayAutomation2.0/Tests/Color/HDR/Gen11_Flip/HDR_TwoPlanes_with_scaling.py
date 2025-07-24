from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3args import MPO_BLEND_VAL, RECT1, PlaneInfo
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import SURFACE_MEMORY_TYPE, PLANE_ORIENTATION
from Tests.Color.HDR.Gen11_Flip.hdr_base import *
from Tests.Color.Common.common_utility import get_bit_value


class Test_TwoPlanesHDR_Scaling(HDRBase):
    NoLayers = [2, 2, 2, 2]

    ##
    # To Disable DFT and perform other cleanup as part of the runTest
    def post_test_cleanup(self):
        ##
        # Disable DFT
        self.test_after_reboot_status = True
        self.enable_disable_mpo(False)

    ##
    # LFP simulation requires reboot for LFP to be enumerated.
    # Triggering S5 power event only in case of LFP simulation.
    def test_before_reboot(self):
        exec_type = self.utility.get_execution_environment_type()
        lfp_details = display_config.is_display_attached(self.enumerated_displays, self.port)
        if (exec_type != 'POST_SI_ENV') or (lfp_details is True):
            logging.debug("Execution env type is %s and LFP details is %s" % (exec_type, lfp_details))
            self.test_before_reboot_skipped = True
        else:
            ##
            # Invoke reboot
            logging.info("Invoking POWER_STATE_S5 event")
            if reboot_helper.reboot(self, 'test_after_reboot') is False:
                self.fail("S5 Power Event: Failed")

    def test_after_reboot(self):

        self.parseXML(self.xml)
        if self.blendingMode[0] == BT2020_LINEAR:
            self.setup_for_linear_mode()
        else:
            logging.info("Blending Mode is not Linear - ForceHDRMode Regkey need not be set")

        topology = enum.SINGLE
        if self.display_config.set_display_configuration_ex(topology, self.connected_list) is True:
            logging.info("Successfully applied the configuration")

        ##
        # Enable DFT
        self.enable_disable_mpo(True)

        count = [0, 0]
        stMPOBlend = MPO_BLEND_VAL()

        tiling = SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR

        sdimension1 = RECT1(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)  # downscaling
        ##
        # Downscaling is supported only upto a shrink factor of 2 and not beyond
        ddimension1 = RECT1(0, 0, self.current_mode.HzRes - 2, self.current_mode.VtRes)
        sdimension2 = RECT1(00, 0, self.current_mode.HzRes // 3, self.current_mode.VtRes // 3)
        ddimension2 = RECT1(0, 0, self.current_mode.HzRes // 2, self.current_mode.VtRes // 2)  # Upscaling
        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            out_file0 = self.convert_image(self.path[0], self.current_mode.HzRes, self.current_mode.VtRes,
                                           self.pixel_format[0], 0)
            out_file1 = self.convert_image(self.path[1], self.current_mode.HzRes // 3, self.current_mode.VtRes // 3,
                                           self.pixel_format[1], 0)
            Plane1 = PlaneInfo(self.sourceID[index], 1, 1, self.pixel_format[0], tiling, sdimension1, ddimension1,
                               ddimension1, PLANE_ORIENTATION.ORIENTATION_0, stMPOBlend, self.color_space[0], out_file0,
                               self.cs_flags[0])
            Plane2 = PlaneInfo(self.sourceID[index], 0, 1, self.pixel_format[1], tiling, sdimension2, ddimension2,
                               ddimension2, PLANE_ORIENTATION.ORIENTATION_0, stMPOBlend, self.color_space[1], out_file1,
                               self.cs_flags[1])
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)

        planes = PLANES(pyPlanes, self.hdrmetadata)
        ##
        # As per the DCN: 14010862793, Driver is expected to Fail CheckMPO in case it gets a Linear Scaling for HDR
        # Note : With this implementation, in Linear test, the CheckMPO failure, although expected, will be logged as error in the base.
        # Also, the CheckMPO could be false because of other genuine reasons as well sometimes, but still the test could pass
        # Ideally test should check for the restriction specifically for linear case.
        # @todo : As part of refactoring, care has been taken to decode the error status returned by CheckMPO and Pass/fail accordingly
        # @todo : Porting to the RW tests
        reg_args = registry_access.StateSeparationRegArgs(gfx_index="gfx_0")
        reg_value, reg_type = registry_access.read(args=reg_args, reg_name="DisplayFeatureControl")
        enable_linear_scaling_support = get_bit_value(reg_value, 20, 20)
        logging.info("enable_linear_scaling_support {0}".format(enable_linear_scaling_support))
        if enable_linear_scaling_support == 0:
            if self.performFlip(planes) is False:
                if self.blendingMode[0] == BT2020_LINEAR:
                    logging.info("Expected CheckMPO failure since test tried to perform Linear Scaling in HDR mode")
                    self.post_test_cleanup()
                else:
                    logging.error("Failed to Perform Flip")
                    self.post_test_cleanup()
                    self.fail()
            else:
                if self.blendingMode[0] == BT2020_LINEAR:
                    logging.error("CheckMPO SUCCESSFUL although since test tried to perform Linear Scaling in HDR mode")
                    self.post_test_cleanup()
                    self.fail("Linear scaling is not allowed in HDR mode")
                else:
                    logging.info("Successfully performed flip")
                    self.post_test_cleanup()
        else:
            if self.performFlip(planes):
                logging.info("Successfully performed flip")
                self.post_test_cleanup()
            else:
                logging.error("Failed to Perform Flip")
                self.post_test_cleanup()
                self.fail("Failed to perform HDR Flip")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Test_TwoPlanesHDR_Scaling'))
    TestEnvironment.cleanup(outcome)