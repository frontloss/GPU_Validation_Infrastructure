########################################################################################################################
# @file         mpo_app.py
# @brief        MPO App that obtains the plane information from the XML file and presents planes on the screen.
#               * Enable DFT framework and feature.
#               * Get the plane info from the XML file.
#               * Check the hardware support for the plane.
#               * Disable DFT framework and feature.
# @author       Shetty, Anjali N
########################################################################################################################
import logging
import os
import sys
import time
import unittest
from xml.etree import ElementTree as ET

from Libs.Core import flip
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment

##
# @brief    Contains unittest default functions for setUp and tearDown function to get plane information from XML file
class MPOApp(unittest.TestCase, test_context.TestContext):
    cmdargs = None
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
        tree = ET.parse(self.cmdargs[1])
        plane_info = tree.getroot()

        plane = plane_info.findall("./Plane")

        for element in plane:
            ##
            # Get the plane info from the XML file
            source_id = int(element.find("./SourceId").text, 10)
            layer_index = int(element.find("./LayerIndex").text, 10)
            enabled = int(element.find("./Enabled").text, 10)
            pixel_format = getattr(flip.PIXEL_FORMAT, element.find("./PixelFormat").text)
            tile_format = getattr(flip.SURFACE_MEMORY_TYPE, element.find("./TileFormat").text)
            source_rect = element.find("./SourceRect").text.split(",")
            source_rect_coordinates = flip.MPO_RECT(int(source_rect[0]), int(source_rect[1]), int(source_rect[2]),
                                                    int(source_rect[3]))
            destination_rect = element.find("./DestRect").text.split(",")
            destination_rect_coordinates = flip.MPO_RECT(int(destination_rect[0]), int(destination_rect[1]),
                                                         int(destination_rect[2]), int(destination_rect[3]))
            clip_rect = element.find("./ClipRect").text.split(",")
            clip_rect_coordinates = flip.MPO_RECT(int(clip_rect[0]), int(clip_rect[1]), int(clip_rect[2]),
                                                  int(clip_rect[3]))
            hw_orientation = getattr(flip.MPO_PLANE_ORIENTATION, element.find("./HwOrientation").text)
            blend_val = flip.MPO_BLEND_VAL(int(element.find("./BlendValue").text, 10))
            path = (os.path.join(test_context.SHARED_BINARY_FOLDER, element.find("./Path").text))
            plane_attributes = flip.PLANE_INFO(source_id, layer_index, enabled, pixel_format, tile_format,
                                               source_rect_coordinates, destination_rect_coordinates,
                                               clip_rect_coordinates,
                                               hw_orientation, blend_val, path)
            planes.append(plane_attributes)
            logging.info("Plane %s" % (element.get('index')) + " :%s" % plane_attributes)

        pplanes = flip.PLANE(planes)

        ##
        # Check the hardware support for the plane
        supported = self.enable_mpo.check_mpo(pplanes)

        if (supported):
            ##
            # Present the planes on the screen
            self.enable_mpo.set_source_address_mpo(pplanes)
        else:
            logging.info("Check MPO failed")

        time.sleep(5)

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        ##
        # Disable the DFT framework and feature
        self.enable_mpo.enable_disable_mpo_dft(False, 1)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
