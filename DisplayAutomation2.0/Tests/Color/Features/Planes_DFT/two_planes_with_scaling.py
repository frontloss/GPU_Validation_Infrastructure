##############################################################################################
# @file         hdr_two_planes_with_scaling.py
# @addtogroup   Test_Planes_HDR
# @section      hdr_two_planes_with_scaling
# @remarks      To flip two planes on single or multiple displays with different plane parameters
#               Test verifies display color pipeline programming and also checks for underrun.
# @ref          hdr_two_planes_with_scaling.py \n
# CommandLine   python Tests\Color\Features\DFT_HDR\hdr_two_planes_with_scaling.py -EDP_A -INPUTFILE NON_LINEAR_SRGB_709_SinglePlane_001.xml
# @author       Smitha B
###############################################################################################
from Tests.Color.Features.Planes_DFT.dft_hdr_test_base import *
from Tests.Color.Common import common_utility


class TwoPlaneWithScaling(DFT_HDRBase):

    def runTest(self):
        pyPlanes = []
        for gfx_index, adapter in self.context_args.adapters.items():
            for panel_name, panel_attributes in adapter.panels.items():
                stMPOBlend = flip.MPO_BLEND_VAL(0)
                tiling = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_LINEAR
                sdimension1 = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes, self.panel_mode_dict[gfx_index, panel_name].VtRes)
                ##
                # Downscaling is supported only upto a shrink factor of 2 and not beyond
                ddimension1 = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes - 2, self.panel_mode_dict[gfx_index, panel_name].VtRes)
                sdimension2 = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes // 3,
                                            self.panel_mode_dict[gfx_index, panel_name].VtRes // 3)
                ##
                # Upscaling
                ddimension2 = flip.MPO_RECT(0, 0, self.panel_mode_dict[gfx_index, panel_name].HzRes // 2,
                                            self.panel_mode_dict[gfx_index, panel_name].VtRes // 2)

                pyPlanes = []

                if not planes_verification.check_layer_reordering(gfx_index) and self.pixel_format[1] in self.planar_formats:
                    plane1_layer = 0
                    plane2_layer = 1
                else:
                    plane1_layer = 1
                    plane2_layer = 0

                out_file0 = self.convert_png_to_bin(self.path[0], self.panel_mode_dict[gfx_index, panel_name].HzRes,
                                                    self.panel_mode_dict[gfx_index, panel_name].VtRes,
                                                    self.pixel_format[0], plane1_layer, panel_name)
                out_file1 = self.convert_png_to_bin(self.path[1], self.panel_mode_dict[gfx_index, panel_name].HzRes / 2,
                                                    self.panel_mode_dict[gfx_index, panel_name].VtRes / 2,
                                                    self.pixel_format[1], plane2_layer, panel_name)
                Plane1 = flip.PLANE_INFO(panel_attributes.source_id, plane1_layer, 1, self.pixel_format[0], tiling,
                                         sdimension1, ddimension1, ddimension1,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                         stMPOBlend, self.color_space[0], out_file0)
                Plane2 = flip.PLANE_INFO(panel_attributes.source_id, plane2_layer, 1, self.pixel_format[1], tiling,
                                         sdimension2, ddimension2, ddimension2,
                                         flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                         stMPOBlend, self.color_space[1], out_file1)
                pyPlanes.append(Plane1)
                pyPlanes.append(Plane2)
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
                logging.info("Verifying HDR Pipe programming for Pipe : {0} ".format(panel.pipe))
                if self.pipe_verification(gfx_index, adapter.platform, port, panel,
                                          self.panel_caps[0],
                                          self.output_range[gfx_index, port]) is False:
                    self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
