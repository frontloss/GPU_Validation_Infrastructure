######################################################################################
# @file
# @addtogroup Test_Power_FBC
# @section FBC_Plane_Resize
# @remarks
# <b> Test Name: fbc_plane_resize </b> <br>
# @ref fbc_plane_resize.py
# <ul>
# <li> <b> Description: </b> <br>
# To verify FBC restriction check with different plane size.
# </li>
# <li> <b> Execution Command(s) : </b> <br>
# <ul>
# <li> python fbc_plane_resize.py -edp_a</li>
# </ul>
# </li>
# <li> <b> Test Failure Case(s) : </b> <br>
# <ul>
# <li> FBC verification failure.
# </li>
# <li> Flip Generation failed.
# </li>
# </ul>
# </li>
# </ul>
# @author Suraj Gaikwad, Amit Sau
######################################################################################
import time

from Libs.Core import flip
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Power.FBC.fbc_base import *
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

##
# FBC should be enabled for plane size between (200,30) and (4095, 4095), both inclusive
FBC_PLANE_SIZE_VERIFICATION_LIST = [(195, 30),  # (X, Y)
                                    (195, 32),
                                    (200, 32),  # (Min X, Min Y)
                                    (200, 30),
                                    (500, 500),
                                    (4095, 4095)  # (Max X, Max Y)
                                    ]


class FbcPlaneResize(FbcBase):
    enable_mpo = None
    planes = []
    source_rect_coordinates = None
    destination_rect_coordinates = None
    clip_rect_coordinates = None

    def setUp(self):
        ##
        # Inherit setup from the base class
        super(FbcPlaneResize, self).setUp()

        self.enable_mpo = flip.MPO()

    ##
    # Generate Flip
    def generate_flip(self, width, height):
        source_rect_coordinates = flip.MPO_RECT(0, 0, width, height)
        destination_rect_coordinates = flip.MPO_RECT(0, 0, width, height)
        clip_rect_coordinates = flip.MPO_RECT(0, 0, width, height)

        for adapter in fbc.PLATFORM_INFO.values():
            gfx_index = adapter['gfx_index']
            # Y tiling is not supported for DG2 & DG3
            # Refer : https://gfxspecs.intel.com/Predator/Home/Index/49251
            if adapter['name'] in ['DG2', 'DG3', 'MTL', 'LNL']:
                surface_memory_type = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_TILE4
            else:
                surface_memory_type = flip.SURFACE_MEMORY_TYPE.SURFACE_MEMORY_Y_LEGACY_TILED

            plane_attributes = flip.PLANE_INFO(0, 0, 1, flip.PIXEL_FORMAT.PIXEL_FORMAT_B8G8R8A8,
                                               surface_memory_type, source_rect_coordinates,
                                               destination_rect_coordinates,
                                               clip_rect_coordinates,
                                               flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                               flip.MPO_BLEND_VAL(0))
            self.planes.append(plane_attributes)

            pplanes = flip.PLANE(self.planes)

            ##
            # Check the hardware support for the plane
            supported = self.enable_mpo.check_mpo3(pplanes, gfx_adapter_index=gfx_index)

            ##
            # Present the planes on the screen
            if supported == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                result = self.enable_mpo.set_source_address_mpo3(pplanes, gfx_adapter_index=gfx_index)
                if result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                    logging.info("Successfully generated flip on adapter %s" % gfx_index)
                elif result == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                    logging.error("Resource creation failed")
                    return False
                else:
                    logging.error("Failed to generate the flip on adapter %s" % gfx_index)
                    return False
            elif supported == flip.PLANES_ERROR_CODE.PLANES_RESOURCE_CREATION_FAILURE:
                logging.error("Resource creation failed")
                return False
            else:
                logging.info("Failed to generate the flip on adapter %s" % gfx_index)

            time.sleep(5)

            ##
            # Verify if the plane was generated successfully or not
            plane_size = MMIORegister.read('PLANE_SIZE_REGISTER', 'PLANE_SIZE_1_A', common.PLATFORM_NAME,
                                           gfx_index=gfx_index)

            plane_size_x = plane_size.__getattribute__('width') + 1
            plane_size_y = plane_size.__getattribute__('height') + 1

            if (plane_size_x != width) and (plane_size_y != height):
                logging.error('Test Failed to generate a flip with plane size as %sx%s on adapter %s' % (width, height,
                                                                                                         gfx_index))
                return False
        return True

    ##
    # FBC restriction check with different plane size
    def runTest(self):

        status = True
        # check FBC status if PSR2 edp panel is connected
        if self.check_psr2_support():
            return
        ##
        # Currently the test is applicable for single display only
        # TODO: Extend the test for multi-display scenarios
        for adapter in fbc.PLATFORM_INFO.values():
            gfx_index = adapter['gfx_index']
            targetid_dict = self.get_port_targetid_map(gfx_index)
            pipe_data = display_base.get_port_to_pipe(gfx_index=gfx_index).items()
            if adapter['name'] in ['MTL', 'ELG', 'LNL']:
                port = [key for key, value in pipe_data
                        if value in ['PIPE_A', 'PIPE_B']][0]
            else:
                port = [key for key, value in pipe_data if value == 'PIPE_A'][0]
            current_mode = self.display_config.get_current_mode(targetid_dict[port])
            ##
            # Enable the DFT framework and feature
            self.enable_mpo.enable_disable_mpo_dft(True, 1, gfx_adapter_index=gfx_index)
            for plane_size in FBC_PLANE_SIZE_VERIFICATION_LIST:
                width = plane_size[0]
                height = plane_size[1]

                logging.info(
                    "============== FBC with PLANE SIZE Width=%s & Height=%s) ==============" % (width, height))

                ##
                # Check if restriction is valid for the current resolution
                if current_mode.HzRes > width and current_mode.VtRes > height:

                    self.planes = []

                    ##
                    # generate flip of the required size on all adapters
                    if self.generate_flip(width, height) is False:
                        ##
                        # Try to generate flip again, if it fails for the first time.
                        if self.generate_flip(width, height) is False:
                            self.fail("Test failed to generate the required flip")
                    # verify fbc on all adapters
                    fbc_result = fbc.verify_fbc(is_display_engine_test=False)

                    if fbc_result is False:
                        logging.error('FAIL : FBC verification with flips generated in %s x %s resolution' % (width,
                                                                                                              height))
                        status = False
                    else:
                        logging.info('PASS : FBC verification with flips generated in %s x %s resolution' % (width,
                                                                                                             height))

            if status is False:
                self.fail('FAIL : FBC plane size restrictions fail')
            logging.info('PASS : FBC plane size restrictions success')

    def tearDown(self):
        ##
        # Disable the DFT framework and feature
        for adapter in fbc.PLATFORM_INFO.values():
            self.enable_mpo.enable_disable_mpo_dft(False, 1, gfx_adapter_index=adapter['gfx_index'])
        ##
        # Inherit tearDown from the base class
        super(FbcPlaneResize, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(FbcPlaneResize)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
