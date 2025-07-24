from Libs.Core.display_config import display_config
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3args import MPO_BLEND_VAL, RECT1, PlaneInfo
from Tests.Color.HDR.Gen11_Flip.MPO3H.mpo3enums import SURFACE_MEMORY_TYPE, PLANE_ORIENTATION
from Tests.Color.HDR.Gen11_Flip.hdr_base import *


class Test_ThreePlanesHDR(HDRBase):
    NoLayers = [3, 3, 3, 3]

    ##
    # LFP simulation requires reboot for LFP to be enumerated.
    # Triggering S5 power event only in case of LFP simulation.
    def test_before_reboot(self):
        exec_type = self.utility.get_execution_environment_type()
        display_attached = display_config.is_display_attached(self.enumerated_displays, self.port)
        if (exec_type != 'POST_SI_ENV') or (display_attached == True) or (self.lfp_support_in_vbt == False):
            logging.debug("Execution env type is %s ; Display attached is %s; LFP Support in VBT is %s" % (
                exec_type, display_attached, self.lfp_support_in_vbt))
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

        ##
        # Enable DFT
        self.enable_disable_mpo(True)

        Test_ThreePlanesHDR.xml = sys.argv.pop()
        count = [0, 0]
        stMPOBlend = MPO_BLEND_VAL()

        tiling = SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
        sdimension1 = RECT1(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)
        ddimension1 = RECT1(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        ##
        # The Rectangle members should have an even value. CheckMPO failure will be observed if input to the driver for destination panning position is an odd value.
        # This is a known bspec restriction. Hence performing a rounding to make the values Even.
        left = (self.current_mode.HzRes // 8) if (self.current_mode.HzRes // 8) % 2 == 0 else ((self.current_mode.HzRes // 8) - 1)
        top = (self.current_mode.VtRes // 8) if (self.current_mode.VtRes // 8) % 2 == 0 else ((self.current_mode.VtRes // 8) - 1)
        right = (self.current_mode.HzRes // 8 * 4) if (self.current_mode.HzRes // 8 * 4) % 2 == 0 else ((self.current_mode.HzRes // 8 * 4) - 1)
        bottom = (self.current_mode.VtRes // 8 * 4) if (self.current_mode.VtRes // 8 * 4) % 2 == 0 else ((self.current_mode.VtRes // 8 * 4) - 1)
        sdimension2 = RECT1(left, top, right, bottom)
        ddimension2 = RECT1(left, top, right, bottom)

        left = self.current_mode.HzRes // 8 * 5 if (self.current_mode.HzRes // 8 * 5) % 2 == 0 else  ((self.current_mode.HzRes // 8 * 5) - 1)
        top = self.current_mode.VtRes // 8 * 5 if (self.current_mode.VtRes // 8 * 5) % 2 == 0 else ((self.current_mode.VtRes // 8 * 5) - 1)
        right = self.current_mode.HzRes // 8 * 8
        bottom = self.current_mode.VtRes // 8 * 8
        sdimension3 = RECT1(left, top, right, bottom)
        ddimension3 = RECT1(left, top, right, bottom)
        pyPlanes = []

        for index in range(0, self.NoOfDisplays):
            out_file0 = self.convert_image(self.path[0], self.current_mode.HzRes, self.current_mode.VtRes,
                                           self.pixel_format[0], 0)
            out_file1 = self.convert_image(self.path[1], self.current_mode.HzRes // 8 * 3,
                                           self.current_mode.VtRes // 8 * 3, self.pixel_format[1], 0)
            out_file2 = self.convert_image(self.path[2], self.current_mode.HzRes // 8 * 3,
                                           self.current_mode.VtRes // 8 * 3, self.pixel_format[2], 0)
            Plane1 = PlaneInfo(self.sourceID[index], 2, 1, self.pixel_format[0], tiling, sdimension1, ddimension1,
                               ddimension1, PLANE_ORIENTATION.ORIENTATION_0, stMPOBlend, self.color_space[0], out_file0,
                               self.cs_flags[0])
            Plane2 = PlaneInfo(self.sourceID[index], 1, 1, self.pixel_format[1], tiling, sdimension2, ddimension2,
                               ddimension2, PLANE_ORIENTATION.ORIENTATION_0, stMPOBlend, self.color_space[1], out_file1,
                               self.cs_flags[1])
            Plane3 = PlaneInfo(self.sourceID[index], 0, 1, self.pixel_format[2], tiling, sdimension3, ddimension3,
                               ddimension3, PLANE_ORIENTATION.ORIENTATION_0, stMPOBlend, self.color_space[2], out_file2,
                               self.cs_flags[2])
            pyPlanes.append(Plane1)
            pyPlanes.append(Plane2)
            pyPlanes.append(Plane3)

        planes = PLANES(pyPlanes, self.hdrmetadata)
        if self.performFlip(planes):
            logging.info("Flipped successfully and the Register Verification has passed")
            ##
            # Disable DFT
            self.test_after_reboot_status = True
            self.enable_disable_mpo(False)
        else:
            ##
            # Disable DFT
            self.enable_disable_mpo(False)
            self.test_after_reboot_status = True
            self.fail("SDR/HDR three plane flips verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('Test_ThreePlanesHDR'))
    TestEnvironment.cleanup(outcome)
