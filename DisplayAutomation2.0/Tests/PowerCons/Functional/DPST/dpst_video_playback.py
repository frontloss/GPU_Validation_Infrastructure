########################################################################################################################
# @file         dpst_video_playback.py
# @brief        Test for DPST/OPST verification during video playback
#
# @author       Ashish Tripathi
########################################################################################################################

from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.DPST.dpst_base import *
from Tests.PowerCons.Modules import workload


##
# @brief        This class contains test cases for DPST/OPST with Video Playback
class DpstVideoPlayBack(DpstBase):

    ##
    # @brief        This function verifies DPST/OPST during Video Playback
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_dpst_video_dc(self):
        status = True
        skip_report_generate = False
        video_list = [24, 30, 59.940]
        for itr in range(len(video_list)):
            offset_param = None if self.offsets is None else [self.offsets, 0.5]
            etl_file, _ = workload.run(workload.VIDEO_PLAYBACK, [video_list[itr], 30], offset_param)
            if etl_file is None:
                assert False, "Failed to run workload for Video Playback"

            for adapter in dut.adapters.values():
                for panel in adapter.panels.values():
                    # Skip the panel if not LFP
                    if panel.is_lfp is False:
                        continue
                    dpst_status = dpst.verify(adapter, panel, etl_file, skip_report_generate, self.xpst_feature, True)
                    if dpst_status is False:
                        gdhm.report_driver_bug_pc(
                            f"[PowerCons][{self.xpst_feature_str}] {self.xpst_feature_str} is not working with "
                            f"video playback {panel.port}")
                        status = False
                        logging.error(f"FAIL: {self.xpst_feature_str} is not working on "
                                      f"{panel.port}(PIPE_{panel.pipe})= NOT EXPECTED")

        if status is False:
            self.fail("FAIL: {0} feature verification".format(self.xpst_feature_str))
        logging.info("PASS: {0} feature verification".format(self.xpst_feature_str))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DpstVideoPlayBack))
    test_environment.TestEnvironment.cleanup(test_result)
