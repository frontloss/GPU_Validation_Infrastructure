##############################################################################################
# \file         hdr_singleplane_fullscreen.py
# \addtogroup   Test_Planes_HDR
# \section      hdr_singleplane_fullscreen
# \remarks      To flip single plane on single or multiple displays with different plane parameters
#               Test verifies display color pipeline programming and also checks for underrun.
# \ref          hdr_singleplane_fullscreen.py \n
# CommandLine   python Tests\Planes\HDR\hdr_singleplane_fullscreen.py -EDP_A -INPUTFILE NON_LINEAR_SRGB_709_SinglePlane_001.xml
# \author       Soorya R
###############################################################################################
from Tests.Color.Features.Planes_DFT.dft_hdr_test_base import *
from Tests.Color.Common import common_utility


class SinglePlane(DFT_HDRBase):

    def runTest(self):
        pyPlanes = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for panel_name, panel_attributes in adapter.panels.items():
                stMPOBlend = flip.MPO_BLEND_VAL(0)
                tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
                sdimension = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes, self.panel_mode_dict[gfx_index, panel_name].VtRes)
                ddimension = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes, self.panel_mode_dict[gfx_index, panel_name].VtRes)

                if not planes_verification.check_layer_reordering(gfx_index) and self.pixel_format[0] in self.planar_formats:
                    plane1_layer = 1
                else:
                    plane1_layer = 0

                out_file0 = self.convert_png_to_bin(self.path[0], self.panel_mode_dict[gfx_index, panel_name].HzRes,
                                                    self.panel_mode_dict[gfx_index, panel_name].VtRes,
                                                    self.pixel_format[0], plane1_layer, panel_name)
                Plane1 = flip.PLANE_INFO(panel_attributes.source_id, plane1_layer, 1, self.pixel_format[0], tiling,
                                         sdimension, ddimension, ddimension,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                         stMPOBlend, self.color_space[0], out_file0)

                pyPlanes.append(Plane1)

        planes = flip.PLANE(pyPlanes, self.hdr_metadata)

        ##
        # Perform the DFT Flip and verify the Plane and Pipe Registers
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if common_utility.perform_flip(planes, gfx_index) is False:
                    self.fail()
                for index in range(0, planes.uiPlaneCount):
                    plane_count = self.get_plane_count_for_source_id(planes.stPlaneInfo[index].iPathIndex, planes)
                    plane_id = self.get_plane_id_from_layerindex(plane_count, planes.stPlaneInfo[index].uiLayerIndex, gfx_index)
                    if self.plane_verification(gfx_index, adapter.platform, panel, plane_id, self.pixel_format,
                                               planes.stPlaneInfo[index].eColorSpace) is False:
                        self.fail()

                # Iterate through active pipes to perform pipe verification
                if self.pipe_verification(gfx_index, adapter.platform, port, panel, self.panel_caps[0],
                                                            self.output_range[gfx_index, port]) is False:
                    self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
