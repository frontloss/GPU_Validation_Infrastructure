########################################################################################################################
# @file         mpo_format_switch.py
# @brief        To flip single or multiple planes on single or multiple displays and perform plane pixel and tile format
#               switching. Test verifies plane programming and also checks for underrun.
#               * Parse the XML file containing plane parameters.
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Shetty, Anjali N
########################################################################################################################
from xml.etree import ElementTree as ET

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common.mpo_base import *

##
# @brief    Contains function to flip single or multiple planes and perform plane pixel and tile format switching
class MPOFormatSwitch(MPOBase):

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Source, destination and clip rectangle.
        rect = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Test XML containing plane parameters
        test_xml = "Tests\Planes\MPO\XML\\" + str(self.cmd_line_param['INPUT_XML'][0])

        tree = ET.parse(test_xml)
        root = tree.getroot()

        tree_root = root.findall("./PlaneInfo")

        for element in tree_root:
            planes = []
            plane = element.findall("./Plane")
            for plane_info in plane:
                source_id = int(plane_info.find("./SourceId").text, 10)
                layer_index = int(plane_info.find("./LayerIndex").text, 10)
                enable = int(plane_info.find("./Enable").text, 10)
                pixel_format = getattr(flip.SB_PIXELFORMAT, plane_info.find("./PixelFormat").text)
                tile_format = getattr(flip.SURFACE_MEMORY_TYPE, plane_info.find("./TileFormat").text)

                plane_attributes = flip.PLANE_INFO(source_id, layer_index, enable, pixel_format, tile_format, rect,
                                                   rect,
                                                   rect,
                                                   flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
                planes.append(plane_attributes)

            pplanes = flip.PLANE(planes)

            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip single or multiple planes on single or multiple displays and perform plane "
                 "pixel and tile format switching. Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
