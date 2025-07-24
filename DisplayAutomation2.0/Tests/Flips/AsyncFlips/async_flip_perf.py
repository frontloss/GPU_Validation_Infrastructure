########################################################################################################################
# @file         async_flip_perf.py
# @brief        Test submits async flips and computes flip to flipdone time
#               * Create planes with different plane parameters.
#               * Submit All param flip.
#               * Submit async flips.
#               * Caputre and parse the ETL to measure flip-flipdone time
# @author       Radhakrishnan, Gopikrishnan
########################################################################################################################

import time
import logging
import sys
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core import flip
from Tests.Planes.Common import flipq_base
from Tests.Planes.Common import planes_helper
from Libs.Core import etl_parser
import statistics as s


##
# @brief    Contains function to check for the hardware support for the plane parameters and flip the content
class AsyncFlipPerf(flipq_base.FlipQBase):

    ##
    # @brief            To perform flipq flips
    # @return           void
    def perform_flip(self):
        ##
        # Create resources for planes
        planes_helper.create_resource(self.pplanes)

        ##
        # Check for hardware support
        checkmpo_result = self.mpo.flipq_check_mpo3(self.pplanes)

        if checkmpo_result == flip.PLANES_ERROR_CODE.PLANES_SUCCESS:

            ##
            # Start ETL Trace
            if planes_helper.start_etl_capture() is False:
                self.fail("Failed to start GfxTrace")

            for i in range(self.flipcount):
                self.mpo.flipq_set_source_address_mpo3(self.pplanes)

            ##
            # Wait for all the flips in the queue to be executed
            time.sleep(2)

            ##
            # Free all the resources
            planes_helper.free_resource(self.pplanes)

            ##
            # Stop ETL Trace
            etl_file = planes_helper.stop_etl_capture()
            self.verify_performance(etl_file)


        else:
            logging.info("Driver did not meet hardware requirements")
            ##
            # Free all the resources in case of check mpo failure
            planes_helper.free_resource(self.pplanes)

    ##
    # @brief            verify_performance
    # @param[in]        etl_file; etl_file with async flips
    # @return           True
    def verify_performance(self,etl_file):
        if etl_parser.generate_report(etl_file) is False:
            logging.error("Failed to generate EtlParser report")

        final = []
        # flip_data - get all async flip DFT data
        flip_data = etl_parser.get_event_data(etl_parser.Events.DFT_FLIP_SYNC_ADDRESS)

        for i in flip_data:
            if i.Async:
                final.append(("ASync Flip", i.TimeStamp))
        start_time = final[0][1]
        end_time = final[-1][1] + 1000
        flip_count = len(flip_data)

        DE_PIPE_INTERRUPT_A = 0x44408

        # mmio data
        mmios = etl_parser.get_mmio_data(offset=DE_PIPE_INTERRUPT_A, is_write=False, start_time=start_time, end_time=end_time)
        for mmio in mmios:
            if mmio.Data & 8:
                final.append((f"FLIP_DONE", mmio.TimeStamp))

        # sorting the lists into one
        final.sort(key=lambda x: x[1])

        flag = 0
        times = []
        start = 0
        end = 0
        for i in final:
            if "ASync" in i[0] and not flag:
                flag = 1
                start = i[1]
            elif flag and "FLIP_DONE" in i[0]:
                end = i[1]
                times.append((end - start))
                flag = 0
        logging.info(f"Considering data from {flip_count} async flips")
        logging.info(f"Mean Flip-FlipDone time {round(s.mean(times) * 1000, 2)}us")
        logging.info(f"Median Flip-FlipDone time {round(s.median(times) * 1000, 2)}us")
        return True

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

        self.flipcount = int(self.cmd_line_param["FLIPCOUNT"][0])

        ##
        # Source, destination and clip rectangle.
        rect = flip.MPO_RECT(0, 0, self.current_mode.HzRes, self.current_mode.VtRes)

        ##
        # Blend value.
        blend = flip.MPO_BLEND_VAL(0)

        async_flip_flag = flip.MPO_PLANE_IN_FLAGS(0x2)
        ##
        # Fill plane parameters.
        for index in range(0, self.no_of_displays):
            plane1 = flip.PLANE_INFO(self.source_id[index], 0, 1, self.pixel_format[0], self.tile_format[0], rect, rect,
                                     rect, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT, blend,
                                     self.color_space[0], stmpo_plane_in_flag=async_flip_flag)
            planes.append(plane1)

        self.pplanes = flip.PLANE(planes)


        ##
        # Check for the hardware support for the plane parameters and flip the content.
        self.perform_flip()

    ##
    # @brief            Unittest tearDown function
    # @return           void
    def tearDown(self):
        super(AsyncFlipPerf, self).tearDown()
        mpo = flip.MPO()
        for i in range(0, 2):
            for plane_index in range(0, self.pplanes.uiPlaneCount):
                if self.pplanes.stPlaneInfo[plane_index].stResourceInfo[i].ullpGmmBlock != 0:
                    mpo.free_resource(self.pplanes.stPlaneInfo[plane_index].stResourceInfo[i])


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test Purpose: Submit Async flips and measure flip to flip done time")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)