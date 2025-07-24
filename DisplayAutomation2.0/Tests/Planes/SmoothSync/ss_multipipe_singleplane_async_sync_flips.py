########################################################################################################################
# @file         ss_multipipe_singleplane_async_sync_flips.py
# @brief        This script contains test to generate a series of async-sync-async flips and check if Smooth Sync is
#               getting enabled or not.
# @author       Gaikwad Suraj
########################################################################################################################
import logging
import sys
import unittest

from Libs.Core import flip
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Planes.Common import smooth_sync_base

##
# @brief    Contains function to generate a series of async-sync-async flips and check if Smooth Sync is getting enabled
#           or not
class SmoothSyncSinglePlane(smooth_sync_base.SmoothSyncBase):
    
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
        # ==============================================================================================================
        # Submit series of Async flips
        # ==============================================================================================================
        ##
        # First flip will be AllParams
        self.performFlip(planes)

        ##
        # Do Async flips
        for index in range(0, 5):
            self.performFlip(planes)
            if self.verify_smooth_sync(planes) is False:
                logging.error("Smooth Sync verification failed for the async flip No. %s" % index)
                self.fail()
        logging.info("Smooth Sync verification passed ")

        # ==============================================================================================================
        # Submit Sync flips
        # ==============================================================================================================
        ##
        # Do Sync flips
        for index in range(0, planes.uiPlaneCount):
            planes.stPlaneInfo[index].stMPOPlaneInFlags = self.sync_flip_flag
        for index in range(0, 2):
            self.performFlip(planes)
            if self.verify_smooth_sync(planes) is True:
                logging.error("Smooth Sync verification for the sync flip No. %s: Actual-Passed, Expected-Fail" % index)
                self.fail()

        # ==============================================================================================================
        # Submit series of Async flips
        # ==============================================================================================================
        for index in range(0, planes.uiPlaneCount):
            planes.stPlaneInfo[index].stMPOPlaneInFlags = self.async_flip_flag

        ##
        # First flip will be AllParams
        self.performFlip(planes)

        ##
        # Do Async flips
        for index in range(0, 5):
            self.performFlip(planes)
            if self.verify_smooth_sync(planes) is False:
                logging.error("Smooth Sync verification failed for the async flip No. %s" % index)
                self.fail()
        logging.info("Smooth Sync verification passed ")
        # ==============================================================================================================


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info('Test purpose: Flips a series of async-sync-async planes on multiple displays and checks Smooth Sync')
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
