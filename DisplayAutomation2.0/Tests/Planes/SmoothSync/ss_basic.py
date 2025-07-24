########################################################################################################################
# @file         ss_basic.py
# @brief        This script contains test to generate async flips and check if Smooth Sync is getting enabled or not.
# @author       Gaikwad, Suraj
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import flip
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common import smooth_sync_base

##
# @brief    Contains function to generate async flips and check if Smooth Sync is getting enabled or not
class SmoothSyncBasic(smooth_sync_base.SmoothSyncBase):
    
    NoLayers = [1, 1, 1, 1]

    ##
    # @brief     Unittest runTest function
    # @return    None
    def runTest(self):
        st_mpo_blend = flip.MPO_BLEND_VAL(0)
        if self.cmd_line_param['PIXELFORMAT'] != "NONE":
            self.pixel_format = []
            self.pixel_format.append(getattr(flip.SB_PIXELFORMAT, ''.join(self.cmd_line_param['PIXELFORMAT'])))
        self.color_space.append(self.get_color_space_for_pixel_format(self.pixel_format[0]))

        sdimension = flip.MPO_RECT(0, 0, self.src_list[0][0], self.src_list[0][1])
        ddimension = flip.MPO_RECT(0, 0, self.dest_list[0][0], self.dest_list[0][1])
        py_planes = []

        for index in range(0, self.NoOfDisplays):
            plane_1 = flip.PLANE_INFO(self.sourceID[index], 0, 1, self.pixel_format[0], self.tiling, sdimension,
                                      ddimension, ddimension, flip.MPO_PLANE_ORIENTATION.MPO_ORIENTATION_DEFAULT,
                                      st_mpo_blend, self.color_space[0], stmpo_plane_in_flag=self.async_flip_flag)
            py_planes.append(plane_1)

        planes = flip.PLANE(py_planes)

        # First flip will be AllParams
        self.performFlip(planes)

        for index in range(0, 20):
            self.performFlip(planes)
            if self.verify_smooth_sync(planes) is False:
                logging.error("Smooth Sync verification failed for the async flip No. %s" % index)
                self.fail()
        logging.info("Smooth Sync verification passed ")


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Generate Async flips and checks for Smooth Sync getting enabled or not')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
