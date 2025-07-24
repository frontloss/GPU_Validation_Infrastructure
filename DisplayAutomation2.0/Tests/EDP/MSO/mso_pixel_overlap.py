########################################################################################################################
# @file         mso_pixel_overlap.py
# @addtogroup   EDP
# @section      MSO _Tests
# @brief        This file contains tests to verify mso with pixel overlap count
# @details      @ref mso_pixel_overlap.py <br>
#               Test for Pixel overlap
#               This file Verify MSO with different pixel overlap count
#
# @author       Kruti Vadhavaniya
########################################################################################################################

from Libs.Core.test_env import test_environment
from Libs.Feature.powercons import registry
from Tests.EDP.MSO.mso_base import *
from Tests.PowerCons.Modules import dpcd


##
# @brief    This file contains tests to verify mso with pixel overlap count
class TestPixelOverlap(MsoBase):
    ##
    # @brief        This test verifies mso with pixel overlap count
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_pixel_overlap(self):
        status = True

        for panel in self.mso_panels:
            logging.info("Verifying MSO pixel overlap count for Panel: {0}".format(panel.pipe))
            for i in range(8):
                status &= mso.set_pixel_overlap_count_registry(i + 1)
                status &= mso.verify_pixel_overlap_count(panel)

                status &= mso.verify_timing(panel, i+1)

        if status is False:
            self.fail("\tFAIL: MSO verification failed with Pixel overlap count")
        logging.info("\tPASS: MSO verification with Pixel overlap count")

    ##
    # @brief        This function deletes registry key DisplayOverlapValMSO
    # @details      This function deletes registry key DisplayOverlapValMSO as a WA for  (HSD : 18021670843)
    # @return       None
    @classmethod
    def tearDownClass(cls):
        # Delete pixel overlap registry key
        reg_key = 'DisplayOverlapValMSO'
        for adapter in dut.adapters.values():
            registry.delete(adapter.gfx_index, key=reg_key)

        super(TestPixelOverlap, cls).tearDownClass()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestPixelOverlap))
    test_environment.TestEnvironment.cleanup(test_result)
