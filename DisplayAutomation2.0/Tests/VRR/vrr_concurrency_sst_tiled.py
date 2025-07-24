########################################################################################################################
# @file         vrr_concurrency_sst_tiled.py
# @brief        Contains concurrency tests for VRR with sst tiled panel
# @details      Concurrency tests are covering below scenarios:
#               * VRR on Tiled panel should work in case of windowed and full screen
#
# @author       Nainesh Doriwala
########################################################################################################################
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.machine_info.machine_info import SystemInfo
from Tests.Display_Port.DP_Tiled import display_port_base
from Tests.VRR.vrr_base import *


##
# @brief        Exposed Class to write VRR concurrency tests. This class inherits the VrrBase class.
#               Any new concurrency test can inherit this class to use common setUp and tearDown functions.
class ConcurrencySstTiled(VrrBase):
    sst_base = display_port_base.DisplayPortBase()

    ############################
    # Default UnitTest Functions
    ############################

    ##
    # @brief        This class method is the entry point for any VRR concurrency test cases. Helps to initialize some of
    #               the parameters required for VRR the test execution.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(ConcurrencySstTiled, cls).setUpClass()

        cls.machine_info = SystemInfo()
        cls.gfx_display_hwinfo = cls.machine_info.get_gfx_display_hardwareinfo()
        for i in range(len(cls.gfx_display_hwinfo)):
            cls.sst_base.platform_list.append(str(cls.gfx_display_hwinfo[i].DisplayAdapterName).upper())
            cls.sst_base.adapter_list_to_verify.append(cls.gfx_display_hwinfo[i].gfxIndex)
        if len(cls.sst_base.platform_list) > 1:
            cls.sst_base.ma_flag = True

        # Get the DP panel details from the command line
        cls.sst_base.process_cmdline()

        # Plug tiled display
        cls.sst_base.tiled_display_helper("Plug")

        # Set display configuration
        cls.sst_base.set_config(cls.sst_base.config, no_of_combinations=1)

        # Set tiled max mode
        cls.sst_base.apply_tiled_max_modes()

        for adapter in dut.adapters.values():
            dut.refresh_panel_caps(adapter=adapter)

    ############################
    # Test Functions
    ############################

    ##
    # @brief        Test function to check if VRR is working on Tiled display
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS", "TILED"])
    # @endcond
    def t_41_sst_tiled(self):
        status = True

        etl_file_path = etl_tracer.GFX_TRACE_ETL_FILE
        etl_tracer.stop_etl_tracer()
        if os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
            etl_file_path = os.path.join(
                test_context.LOG_FOLDER, 'GfxTraceDuringModeSet.' + str(time.time()) + '.etl')
            os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)
        status &= self.verify_vrr_during_modeset(etl_file_path)
        if etl_tracer.start_etl_tracer() is False:
            logging.error("Failed to start ETL Tracer")
            return False

        status &= self.verify_vrr(True)
        if status is False:
            self.fail("VRR verification failed in FULL_SCREEN mode with LOW_HIGH_FPS setting")
        logging.info("\tPASS: VRR verification passed successfully in FULL_SCREEN mode")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(ConcurrencySstTiled))
    TestEnvironment.cleanup(test_result)
