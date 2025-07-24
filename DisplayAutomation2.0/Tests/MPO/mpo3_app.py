########################################################################################################################
# @file         mpo3_app.py
# @brief        MPO App that obtains the plane information from the XML file and presents planes on the screen.
#               * Enable DFT framework and feature.
#               * Submit information about planes.
#               * Check the hardware support for the plane.
#               * Disable DFT framework and feature.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import time
import unittest

from Libs.Core import flip

##
# @brief    Contains unittest default functions for setUp and tearDown function to get plane information from XML file
class MPOApp(unittest.TestCase):
    enable_mpo = None

    ##
    # @brief            Unittest setUp function
    # @return           void
    def setUp(self):
        self.enable_mpo = flip.MPO()
        ##
        # Enable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(True, 1)

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []

        source_rect_coordinates = flip.MPO_RECT(0, 0, 1920, 1080)
        destination_rect_coordinates = flip.MPO_RECT(0, 0, 1920, 1080)
        clip_rect_coordinates = flip.MPO_RECT(0, 0, 1920, 1080)

        plane_attributes = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                           flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED,
                                           source_rect_coordinates, destination_rect_coordinates, clip_rect_coordinates,
                                           flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, flip.MPO_BLEND_VAL(0))
        planes.append(plane_attributes)

        pplanes = flip.PLANE(planes)

        ##
        # Check the hardware support for the plane
        supported = self.enable_mpo.check_mpo3(pplanes)

        if (supported):
            ##
            # Present the planes on the screen
            self.enable_mpo.set_source_address_mpo3(pplanes)
        else:
            logging.info("Check MPO failed")

        time.sleep(20)

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        ##
        # Disable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(False, 1)


if __name__ == '__main__':
    unittest.main()
