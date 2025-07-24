########################################################################################################################
# @file         mpo_ma_format_switch.py
# @brief        Basic test to flip single or multiple planes on each display across multiple adapters and perform plane
#               pixel and tile format switching. Test verifies plane programming and also checks for underrun.
#               * Parse the XML file containing plane parameters.
#               * Check for the hardware support for the plane parameters and flip the content.
# @author       Shetty, Anjali N
########################################################################################################################
from xml.etree import ElementTree as ET

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common.mpo_ma_base import *

##
# @brief    Contains function to flip planes on each display across multiple adapters and perform plane pixel and tile format switching
class MPOFormatSwitch(MPOMABase):


    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)
        test_xml = ""
        ##
        # Test XML containing plane parameters
        for index in range(0, len(self.cmd_line_param)):
            for key, value in self.cmd_line_param[index].items():
                if key == 'INPUT_XML':
                    test_xml = "Tests\Planes\MPO\XML\\" + str(value[0])

        tree = ET.parse(test_xml)
        root = tree.getroot()

        tree_root = root.findall("./PlaneInfo")

        planes = []
        gfx_index = ""
        for element in tree_root:
            planes.append([])
            plane = element.findall("./Plane")
            index = 0
            for plane_info in plane:
                gfx_index = plane_info.find("./AdapterIndex").text
                index_val = gfx_index.split('_')
                index = int(index_val[1])
                source_id = int(plane_info.find("./SourceId").text, 10)
                layer_index = int(plane_info.find("./LayerIndex").text, 10)
                enable = int(plane_info.find("./Enable").text, 10)
                pixel_format = getattr(flip.SB_PIXELFORMAT, plane_info.find("./PixelFormat").text)
                tile_format = getattr(flip.SURFACE_MEMORY_TYPE, plane_info.find("./TileFormat").text)
                rect = flip.MPO_RECT(0, 0, self.current_mode[index].HzRes, self.current_mode[index].VtRes)

                plane_attributes = flip.PLANE_INFO(source_id, layer_index, enable, pixel_format, tile_format, rect,
                                                   rect,
                                                   rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend)
                planes[index].append(plane_attributes)

            pplanes = flip.PLANE(planes[index])

            ##
            # Check for the hardware support for the plane parameters and flip the content.
            self.perform_flip(pplanes, gfx_index)


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: To flip single or multiple planes on single or multiple displays and perform plane "
                 "pixel and tile format switching. Test verifies plane programming and also checks for underrun")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
