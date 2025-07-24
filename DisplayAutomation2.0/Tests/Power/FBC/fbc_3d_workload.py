######################################################################################
# @file         fbc_3d_workload.py
# @brief        To verify FBC with media workload.
# @details      Execution Command(s) :
#                       python fbc_3d_workload.py -edp_a -power_event S3
#               Test Failure Case(s) :
#                       FBC verification failure.
#                       Failed to open directx app and generate async/sync flips
# @author Suraj Gaikwad, Amit Sau
######################################################################################
import datetime
import importlib
import os
import time
from subprocess import Popen

from Libs.Core.display_config.display_config_enums import DisplayConfigTopology
from Libs.Core import display_power
from Libs.Core.logger import gdhm
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Power.FBC.fbc_base import *
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

DIRECTX_APP_LOCATION = 'C:\\Program Files (x86)\\Microsoft DirectX SDK (June 2010)\\Samples\\C++\\Direct3D\\Bin\\x64\\'


class Fbc3DWorkload(FbcBase):
    display_power = display_power.DisplayPower()
    directx_app = os.path.join(DIRECTX_APP_LOCATION, 'MultiAnimation.exe')
    app_handle = None
    status = True
    duration = 60

    directx_args_dict = {
        'fullscreen': '-fullscreen',
        'windowed': '',
        'vsync': '-forcevsync:1',
        'async': '-forcevsync:0'
    }

    ##
    # @brief        Launch the DirectX app
    # @param[in]    sync_mode
    # @param[in]    window_size
    # @return       void
    def fbc_verification_with_directx_app(self, sync_mode, window_size):

        app_args = [self.directx_app, self.directx_args_dict[sync_mode], self.directx_args_dict[window_size]]

        logging.info("============= FBC with 3D {} {} WORKLOAD ============="
                     .format(window_size.upper(), sync_mode.upper()))

        ##
        # Launch the DirectX app with the given sync mode and window size
        self.app_handle = Popen(app_args)
        time.sleep(5)

        ##
        # Verify the Sync mode is as expected or not
        if self.verify_sync_mode(sync_mode, window_size) is False:
            self.fail('Mismatch in expected and actual Sync Mode type. Aborting the test')

        # Verify FBC without power event
        result = fbc.verify_fbc(is_display_engine_test=False)
        if result is False:
            logging.error('FAIL : FBC verification with DirectX App running in {} {} mode'
                          .format(window_size.upper(), sync_mode.upper()))
            self.status = False
        else:
            logging.info('PASS : FBC verification with DirectX App running in {} {} mode'
                         .format(window_size.upper(), sync_mode.upper()))
        
        # Close the app before power event and re-open it after power event as the app might get minimized when the power event is invoked
        # This issue was observed with Power State S3. Link to the issue : https://hsdes.intel.com/appstore/article/#/18025978322
        self.app_handle.terminate()

        # Invoke power event
        if self.display_power.invoke_power_event(self.power_event, self.duration) is False:
            self.fail('Test failed to invoke %s power event' % self.power_event.name)

        # Re-Open the App with given sync mode and window size after Power Event
        self.app_handle = Popen(app_args)
        time.sleep(5)

        # Verify the Sync mode is as expected or not
        if self.verify_sync_mode(sync_mode, window_size) is False:
            self.fail('Mismatch in expected and actual Sync Mode type after power event. Aborting the test')

        ##
        # Verify FBC after power event
        result = fbc.verify_fbc(is_display_engine_test=False)
        if result is False:
            logging.error('FAIL : FBC verification with DirectX App running in {} {} mode after {} power event'
                          .format(window_size.upper(), sync_mode.upper(), self.power_event.name))
            self.status = False
        else:
            logging.info('PASS : FBC verification with DirectX App running in {} {} mode after {} power event'
                         .format(window_size.upper(), sync_mode.upper(), self.power_event.name))

        self.app_handle.terminate()
        self.app_handle = None

    ##
    # @brief        Verify the expected and actual sync modes
    # @param[in]    sync_mode
    # @param[in]    window_size
    # @return       Bool
    def verify_sync_mode(self, sync_mode, window_size):
        # wait for plane to enable
        status = self.contiguous_wait_for_update('plane_enable', 'plane_enable_ENABLE')
        if status is False:
            self.fail('PLANE_CTL_1_A: expected plane enable (Bit31:1) actual plane disable (Bit31:0)')

        # wait for expected flip (sync/async) to enable
        if sync_mode == 'async' and window_size == 'fullscreen':
            fields_expected_value = 'async_address_update_enable_ASYNC'
        else:
            fields_expected_value = 'async_address_update_enable_SYNC'
        status = self.contiguous_wait_for_update('async_address_update_enable', fields_expected_value)
        expected_val = fields_expected_value.split('_')[-1]
        if status is False:
            if expected_val == 'SYNC':
                actual_val = 'ASYNC'
            else:
                actual_val = 'SYNC'
            logging.error(f"SYNC mode -> Expected :{expected_val} actual :{actual_val}")
            gdhm.report_driver_bug_pc(f"[PowerCons][FBC] {expected_val} Flips are not coming with DirectX App")
        return status

    ##
    # @brief        Contiguous wait for update function
    # @param[in]    bit_fields_name
    # @param[in]    fields_expected_value
    # @return       Bool
    def contiguous_wait_for_update(self, bit_fields_name, fields_expected_value):
        retry_count = 0
        status = False
        while True:
            plane_ctl = MMIORegister.read('PLANE_CTL_REGISTER', 'PLANE_CTL_1_A', common.PLATFORM_NAME)
            plane_ctl_value = importlib.import_module("registers.%s.PLANE_CTL_REGISTER" % common.PLATFORM_NAME.lower())
            if plane_ctl.__getattribute__(bit_fields_name) == getattr(plane_ctl_value, fields_expected_value):
                status = True
                break
            else:
                retry_count += 1
            time.sleep(5)
            if retry_count > 6:  # Wait for 30 sec delay to enable plane
                break
        return status

    ##
    # @brief    Function to perform FBC verification
    # @return   void
    def performTest(self):

        ##
        # FBC verification with 3D app in VSync Fullscreen mode
        self.fbc_verification_with_directx_app('vsync', 'fullscreen')

        ##
        # FBC verification with 3D app in VSync Windowed mode
        self.fbc_verification_with_directx_app('vsync', 'windowed')

        ##
        # FBC verification with 3D app in ASync Fullscreen mode
        self.fbc_verification_with_directx_app('async', 'fullscreen')

        ##
        # FBC verification with 3D app in ASync Windowed mode
        self.fbc_verification_with_directx_app('async', 'windowed')

    ##
    # @brief    Run test function
    # @return   void
    def runTest(self):

        # check FBC status if PSR2 edp panel is connected
        if self.check_psr2_support():
            return

        if self.power_event is None:
            self.fail('-POWER_EVENT CS/S3 not mentioned in the command-line. Aborting the test')

        cs_status = self.display_power.is_power_state_supported(display_power.PowerEvent.CS)

        ##
        # Verify system support for the power event specified
        if self.power_event == display_power.PowerEvent.CS:
            self.assertEquals(cs_status, True, 'System does not supports Connected Standby.')
        else:
            self.assertEquals(cs_status, False, 'System does not supports S3 sleep.')

        ##
        # Fetch all possible configs lists based on displays attached
        config_list = display_utility.get_possible_configs(self.display_list)

        ##
        # Iterate through all the possible configs list. Apply the configs one-by-one and then verify FBC
        for config, display_list in config_list.items():
            topology = eval("%s" % config)
            for displays in display_list:
                time.sleep(30)
                ##
                # Set display config
                if self.display_config.set_display_configuration_ex(topology, displays,
                                                                    self.enumerated_displays) is False:
                    self.fail('Failed to apply display configuration %s %s' %
                              (DisplayConfigTopology(topology).name, displays))
                logging.info('Successfully applied the display configuration as %s %s' %
                             (DisplayConfigTopology(topology).name, displays))

                ##
                # Verify FBC in all possible combinations
                self.performTest()

                ##
                # Check the status of FBC verification
                if self.status is False:
                    self.fail("FAIL: FBC verification with 3D Workload")
                logging.info("PASS: FBC verification with 3D Workload")

    ##
    # @brief    Tear Down method
    # @return   None ##
    # @brief    Tear Down method
    # @return   None
    def tearDown(self):
        ##
        # Close the app, if it is still open
        if self.app_handle is not None:
            self.app_handle.terminate()

        ##
        # Inherit tearDown from the base class
        super(Fbc3DWorkload, self).tearDown()


if __name__ == '__main__':
    TestEnvironment.initialize()
    suite = unittest.TestLoader().loadTestsFromTestCase(Fbc3DWorkload)
    result = unittest.TextTestRunner().run(suite)
    TestEnvironment.cleanup(result)
