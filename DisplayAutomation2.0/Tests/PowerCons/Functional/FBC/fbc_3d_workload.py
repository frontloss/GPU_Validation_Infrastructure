##########################################################################################################################################################################
# @file         fbc_3d_workload.py
# @brief        Intention of this test is to verify whether FBC is working as expected with 3D workload App
# @details      
#               * Test steps are as follows
#               * Open FlipAt App in different window sizes(FullScreen, Windowed) and sync modes (VSYNC, ASYNC)
#               * Verify whether the sync mode is as expected
#               * Verify FBC when the App is open
#               * Close the FlipAt App and verify FBC again
#
# @author       Gowtham K L
##########################################################################################################################################################################
import importlib
import time

from Libs.Core.logger import gdhm, html
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.PowerCons.Functional.FBC.fbc_base import *
from Tests.PowerCons.Modules import workload
from Tests.Planes.Common import planes_verification

##
# @brief        This class contains FBC 3D workload test
class Fbc3DWorkload(FbcBase):

    ##
    # @brief    Run test function
    # @return   void
    def runTest(self):
        for adapter in dut.adapters.values():
            platform_name = adapter.name.lower()
            # Verify FBC with 3D app in different sync modes(VSYNC, ASYNC) and window sizes (FullScreen, Windowed)
            self.fbc_verification_with_FlipAt_app('vsync', 'fullscreen', platform_name)

            self.fbc_verification_with_FlipAt_app('vsync', 'windowed', platform_name)

            self.fbc_verification_with_FlipAt_app('async', 'fullscreen', platform_name)

            self.fbc_verification_with_FlipAt_app('async', 'windowed', platform_name)


    ##
    # @brief        API to verify FBC with FlipAt App
    # @param[in]    sync_mode       Expected SYNC mode based on the requirement
    # @param[in]    window_size     Size at which the FlipAt App should be opened (FullScreen/Windowed)
    # @param[in]    platform_name   Adapter Name
    # @return       Void
    def fbc_verification_with_FlipAt_app(self, sync_mode, window_size, platform_name):
        sync_mode_verification_status = True
        logging.info("=================================================================================================")
        html.step_start(f"FBC with 3D {window_size.upper()} {sync_mode.upper()} WORKLOAD")
        logging.info("=================================================================================================")

        is_full_screen = True if window_size == "fullscreen" else False
        is_async_mode = True if sync_mode == "async" else False
        app_config = workload.FlipAtAppConfig()
        app_config.v_sync = False if is_async_mode else True

        # Open the FlipAt App
        if workload.open_gaming_app(workload.Apps.FlipAt, is_full_screen, 0, app_config) is False:
            self.fail(f"\tFailed to open {workload.Apps.FlipAt} app(Test Issue)")
        time.sleep(5)

        # Verify whether the sync mode is as expected or not
        html.step_start("Verifying SYNC Mode")
        if self.verify_sync_mode(sync_mode, platform_name, is_full_screen) is False:
            sync_mode_verification_status = False
        else:
            logging.info("\tPASS : SYNC mode verification")

        html.step_start(f"Verify FBC when {workload.Apps.FlipAt} is open")
        fbc_status_with_3d_app = fbc.verify_fbc(is_display_engine_test=False)
        if fbc_status_with_3d_app is False:
            logging.error(f"FBC verification failed when FlipAt App is running")

        html.step_end()

        # Close the APP
        if workload.close_gaming_app() is False:
            self.fail(f"\tFailed to close {workload.Apps.FlipAt} app(Test Issue)")
        time.sleep(5)

        # Verify FBC after closing FlipAt
        html.step_start(f"Verify FBC after closing {workload.Apps.FlipAt}")
        fbc_status_after_3d_app = fbc.verify_fbc(is_display_engine_test=False)
        if fbc_status_after_3d_app is False:
            logging.error(f"FBC verification failed after closing FlipAt App")
        html.step_end()

        if not sync_mode_verification_status:
            gdhm.report_driver_bug_pc("[FBC] Sync mode verification failed with 3D App")
            self.fail(f"Mismatch in expected and actual Sync modes while FlipAt App is running in {window_size.upper()} {sync_mode.upper()} mode")

        if not fbc_status_with_3d_app or not fbc_status_after_3d_app:
            self.fail(f"FAIL : FBC verification with FlipAt App running in {window_size.upper()} {sync_mode.upper()} mode")
        logging.info(f"PASS: FBC verification with FlipAt App running in {window_size.upper()} {sync_mode.upper()} mode")


    ##
    # @brief        API to verify the SYNC modes
    # @param[in]    sync_mode       Expected SYNC mode based on the requirement
    # @param[in]    platform_name   Adapter Name
    # @param[in]    is_full_screen  Full screen mode or windowed mode
    # @return       True if the SYNC mode verification is successful, False otherwise 
    def verify_sync_mode(self, sync_mode, platform_name, is_full_screen):
        # Wait for the plane to get enabled
        plane_enable_status = self.check_sync_mode_and_plane_enable('plane_enable', 'plane_enable_ENABLE', platform_name, is_full_screen)
        if plane_enable_status is False:
            gdhm.report_driver_bug_pc("[PowerCons][FBC] PLANE_CTL_1_A/PLANE_CTL_3A did not get enabled during 3D workload")
            logging.error("PLANE_CTL_1_A/PLANE_CTL_2_A did not get enabled during 3D workload")

        # Wait for expected flip (sync/async)
        fields_expected_value = "async_address_update_enable_ASYNC" if sync_mode == 'async' else 'async_address_update_enable_SYNC'

        sync_mode_status = self.check_sync_mode_and_plane_enable('async_address_update_enable', fields_expected_value, platform_name, is_full_screen)
        expected_val = fields_expected_value.split('_')[-1]
        if sync_mode_status is False:
            actual_val = "ASYNC" if expected_val == "SYNC" else "SYNC"
            logging.error(f"SYNC mode -> Expected :{expected_val} actual :{actual_val}")
        return plane_enable_status and sync_mode_status


    ##
    # @brief        API to check plane enable and SYNC mode
    # @param[in]    bit_fields_name        Bit fields to check in PLANE_CTsL_REGISTER
    # @param[in]    fields_expected_value  Expected value for the field according to the requirement
    # @param[in]    platform_name   Adapter Name
    # @param[in]    is_full_screen  Full screen mode or windowed mode
    # @return       True for plane_enable/expected fields matching
    def check_sync_mode_and_plane_enable(self, bit_fields_name, fields_expected_value, platform_name, is_full_screen):
        # Wait for 30 seconds for plane enable and expected SYNC mode
        layer_reordering_status = planes_verification.check_layer_reordering()
        max_retry_count = 6 
        retry_count = 0
        status = False
        plane_ctl_register = importlib.import_module(f"registers.{platform_name}.PLANE_CTL_REGISTER")
        while True:
            # Plane enable considerations
            # Layer re-ordering enabled case - PLANE 1
            # Layer re-ordering disabled case - GAME/VIDEO Fullscreen - PLANE 2 | Windowed - PLANE 3
            if layer_reordering_status:
                plane_ctl_mmio = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_1_A', platform_name)
            elif layer_reordering_status is False:
                if is_full_screen:
                    plane_ctl_mmio = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_2_A', platform_name)
                else:
                    plane_ctl_mmio = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_3_A', platform_name)

            if plane_ctl_mmio.__getattribute__(bit_fields_name) == getattr(plane_ctl_register, fields_expected_value):
                status = True
                break
            retry_count += 1
            time.sleep(5)
            if retry_count > max_retry_count:
                break
        return status


if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(Fbc3DWorkload)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)

