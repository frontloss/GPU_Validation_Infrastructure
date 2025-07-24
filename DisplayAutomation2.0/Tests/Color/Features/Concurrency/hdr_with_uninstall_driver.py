#######################################################################################################################
# @file                 hdr_with_uninstall_driver.py
# @addtogroup           Test_Color
# @section              hdr_with_uninstall_driver
# @remarks              @ref hdr_with_uninstall_driver.py \n
#                       The test script enables HDR on the displays supporting HDR.
#                       Uninstall all the drivers and collect the ETLs to perform Post processing
#                       Install all the drivers back and process the ETLs to verify if Pipe Blocks have been programmed
#                       with the correct values.
#                       Verification Details:
#                       The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#                       Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#                       Pipe_Misc register is also verified for HDR_Mode
#                       Plane and Pipe Verification is performed by iterating through each of the displays
#                       Metadata verification, by comparing the Default and Flip Metadata is performed,
#                       along with register verification
# Sample CommandLines:  python hdr_with_uninstall_driver.py -edp_a SINK_EDP50 -config SINGLE
# Sample CommandLines:  python hdr_with_uninstall_driver.py -edp_a SINK_EDP76 -config SINGLE
# @author       Smitha B
#######################################################################################################################
from Tests.Color.Features.E2E_HDR.hdr_test_base import *
from Tests.Install_Uninstall2.install_uninstall2_base import *


class HDRWithUninstallDriver(HDRTestBase, InstallUninstall2Base):
    gfx_driver_uninstall_path = None

    @reboot_helper.__(reboot_helper.setup)
    def setUp(self):
        HDRTestBase().setUp()

    def test_1_step(self):
        ##
        # Enable HDR on all the supported panels and perform verification
        if self.enable_hdr_and_verify() is False:
            self.fail()

        ##
        # Uninstall and Install the primary graphics driver
        for gfx_index, adapter in self.context_args.adapters.items():
            self.assertEquals(self.uninstall_graphics_driver(gfx_index=gfx_index), False,
                              "Aborting the test as primary graphics driver uninstallation is unsuccessful")
            logging.info("PASS: Graphics driver {0} is uninstalled".format(gfx_index))
        logging.info("System Reboot is required after uninstalling all the drivers")
        if reboot_helper.reboot(self, 'test_2_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 4 - Verify Driver is uninstalled or not;
    #                 Capture the ETLs when the driver is not installed for post processing
    #                 Install all the drivers post collection of the ETLs
    # @return None
    def test_2_step(self):
        for gfx_index, adapter in self.context_args.adapters.items():
            self.assertEquals(self.is_driver_installed(gfx_index=gfx_index), True,
                              "Aborting the test as graphics driver {0} is not uninstalled".format(gfx_index))
            logging.info("PASS: {0} graphics driver is not available after un-installation".format(gfx_index))
        logging.debug("Exit: test_3_step()")

        gfx_driver_uninstall = "After_Uninstalling_Driver_TimeStamp_"
        self.gfx_driver_uninstall_path = color_etl_utility.stop_etl_capture(gfx_driver_uninstall)
        ##
        # Start the ETL again for capturing other events
        if color_etl_utility.start_etl_capture() is False:
            logging.error("Failed to Start Gfx Tracer")
            return False

        logging.info("Step-Install: Install primary graphics driver")
        self.assertEquals(
            self.install_graphics_driver_through_device_manager(dvr_path=DRIVER_PATH, driver_type=self.driver_type),
            False,
            "Aborting the test as primary graphics driver installation unsuccessful")
        logging.info("PASS: Primary graphics driver installed, Rebooting system")
        if reboot_helper.reboot(self, 'test_3_step') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief step 4 - Verify Driver is installed and perform verification
    # @return None
    def test_3_step(self):
        self.assertEquals(self.is_driver_installed(gfx_index='gfx_0'), False,
                          "Aborting the test as graphics driver is not installed")
        logging.info("PASS: Graphics driver has been successfully installed")

        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if feature_basic_verify.hdr_status(gfx_index, adapter.platform, panel.pipe) is False:
                    logging.error("FAIL : HDR is enabled after performing Driver Uninstall-Install on {0} conncected "
                                  "to Pipe {1} on Adapter {2}".format(port, panel.pipe, gfx_index))
                    gdhm.report_driver_bug_os("HDR is enabled after performing Driver Uninstall-Install on {0} conncected "
                                  "to Pipe {1} on Adapter {2}".format(port, panel.pipe, gfx_index))
                    self.fail()
                logging.info(
                    "PASS : HDR is disabled after performing Driver Uninstall-Install on {0} conncected to Pipe {1} "
                    "on Adapter {2}".format(
                        port, panel.pipe, gfx_index))

                if self.pipe_verification(gfx_index, adapter.platform, port,
                                          panel) is False:
                    self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('HDRWithUninstallDriver'))
    TestEnvironment.cleanup(outcome)
