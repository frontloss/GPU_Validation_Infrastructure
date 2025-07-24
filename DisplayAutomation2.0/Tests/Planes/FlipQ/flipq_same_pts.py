########################################################################################################################
# @file         flipq_same_pts.py
# @brief        Test submits queued flips with multiple elements having same PTS and verify that all the elements with
#               same PTS are executed.
#               * Create planes with different plane parameters.
#               * Submit All param flip.
#               * Submit 8 address only flips in which 2 flips are executed with same PTS.
#               * Verify for flip presentation time stamp and flip queuing.
# @author       Shetty, Anjali N
########################################################################################################################
import ctypes
import ctypes.wintypes
import time
import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip
from Libs.Core.logger import gdhm
from Tests.Planes.Common import flipq_base
from Tests.Planes.Common import planes_helper
from Tests.Planes.Common import planes_verification


##
# @brief    Contains function to check for the hardware support for the plane parameters and flip the content
class FlipQSamePTS(flipq_base.FlipQBase):

    ##
    # @brief            To perform flipq flips
    # @param[in]        pplanes; details of the plane
    # @return           void
    def flipq_perform_flip(self, pplanes):
        presentation_delay = []
        target_flip_time = []
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        flip_time = ctypes.wintypes.LARGE_INTEGER()

        ##
        # Create resources for planes
        planes_helper.create_resource(pplanes)

        ##
        # Check for hardware support
        checkmpo_result = self.mpo.flipq_check_mpo3(pplanes)

        if (checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS):

            ##
            # Start ETL Trace
            if planes_helper.start_etl_capture() is False:
                self.fail("Failed to start GfxTrace")

            ##
            # Perform all param flip
            resource_in_use = 0
            for plane_index in range(0, pplanes.uiPlaneCount):
                pplanes.stPlaneInfo[plane_index].iResourceInUse = resource_in_use
            self.mpo.flipq_set_source_address_mpo3(pplanes)

            ##
            # Target flip time list with same PTS values
            kernel32.QueryPerformanceCounter(ctypes.byref(flip_time))
            tft = flip_time.value + 100000000
            delay_list = [100, 200, 300, 300, 500, 600, 700, 800, 900, 1000, 2000, 3000, 3000, 3000, 4000, 5000]
            for index in range(0, planes_helper.SIMPLE_FLIPQ_DEPTH):
                target_flip_time.append(tft + delay_list[index])

            logging.info("Target time list {}".format(target_flip_time))

            ##
            # Queue the flips
            for index in range(0, planes_helper.SIMPLE_FLIPQ_DEPTH):
                resource_in_use = (1, 0)[resource_in_use]
                time.sleep(planes_helper.SINGLE_FRAME_DELAY)
                for plane_index in range(0, pplanes.uiPlaneCount):
                    pplanes.stPlaneInfo[plane_index].iResourceInUse = resource_in_use
                pplanes.ulTargetFlipTime = target_flip_time[index]
                ssa_result = self.mpo.flipq_set_source_address_mpo3(pplanes)
                if ssa_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:
                    logging.info("Successfully queued the flips")
                    for display_index in range(0, self.no_of_displays):
                        presentation_delay.append(pplanes.ulDelay)
                else:
                    logging.error("Failed to queue flips")

            ##
            # Wait till the last queue element is executed
            while True:
                kernel32.QueryPerformanceCounter(ctypes.byref(flip_time))
                if flip_time.value >= pplanes.ulTargetFlipTime:
                    break

            ##
            # Wait for all the flips in the queue to be executed
            time.sleep(2)

            ##
            # Free all the resources
            planes_helper.free_resource(pplanes)

            ##
            # Stop ETL Trace
            etl_file = planes_helper.stop_etl_capture()

            ##
            # Verify queuing of flips
            for display in self.connected_list:
                if planes_helper.verify_flipq_mmio(etl_file, display, 0, planes_helper.SIMPLE_FLIPQ_DEPTH):
                    logging.info("MMIO verification passed")
                else:
                    gdhm.report_bug(
                        title="[FlipQ] MMIO Verification failed for FlipQ",
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_OS_FEATURES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    self.fail("MMIO verification failed")

        else:
            logging.info("Driver did not meet hardware requirements")

            ##
            # Free all the resources in case of check mpo failure
            planes_helper.free_resource(pplanes)

    ##
    # @brief            Unittest runTest function
    # @return           void
    def runTest(self):
        planes = []

        ##
        # Pixel format of the plane, which is input from the command line.
        self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['INPUT_PIXELFORMAT'])))

        ##
        # Color space of the plane, obtained from the input pixel format.
        self.color_space.append(planes_helper.get_color_space_for_pixel_format(self.pixel_format[0]))

        ##
        # Tile format of the plane, which is input from the command line.
        self.tile_format.append(getattr(flip.SURFACE_MEMORY_TYPE, ''.join(self.cmd_line_param['INPUT_TILEFORMAT'])))

        ##
        # Source, destination and clip rectangle.
        rect = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            if not planes_verification.check_layer_reordering() and self.pixel_format[0] in self.planar_formats:
                plane1_layer = 1
            else:
                plane1_layer = 0

            plane1 = flip.PLANE_INFO(self.source_id[index], plane1_layer, 1, self.pixel_format[0], self.tile_format[0],
                                     rect,
                                     rect, rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0])
            planes.append(plane1)

        self.pplanes = flip.PLANE(planes)

        pmpocaps_args_ddrw = flip.MPO_CAPS_ARGS_DDRW(0, 0)
        mpocaps_result = self.mpo.get_mpo_caps(pmpocaps_args_ddrw)
        if mpocaps_result and pmpocaps_args_ddrw.MaxFlipQueueDepth != 0:
            planes_helper.SIMPLE_FLIPQ_DEPTH = pmpocaps_args_ddrw.MaxFlipQueueDepth

        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.flipq_perform_flip(self.pplanes)

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        super(FlipQSamePTS, self).tearDown()
        mpo = flip.MPO()
        for i in range(0, 2):
            for plane_index in range(0, self.pplanes.uiPlaneCount):
                if self.pplanes.stPlaneInfo[plane_index].stResourceInfo[i].ullpGmmBlock != 0:
                    mpo.free_resource(self.pplanes.stPlaneInfo[plane_index].stResourceInfo[i])


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Submit queued flips with multiple elements having same PTS and "
                 "verify that all the elements with same PTS are executed.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
