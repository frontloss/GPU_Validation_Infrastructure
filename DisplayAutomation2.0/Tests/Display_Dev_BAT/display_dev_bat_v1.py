###############################################################################################
# @file         display_dev_bat_v1.py
# @brief        An occurrence of underrun leads to failure of test otherwise, test is considered to be passed.
#               in case DE Verification fails - Test will continue to run and apply all possible event selected without aborting .
# @details
# Description:
# Test steps / Test Flow
# ------------------------
#   -> 1. Enable, Disable GFX Driver
#   -> 2. Apply different Topology for connected displays ( Following sequence present in DisplaySequence.xml )
#   ->      Verify DE () Display Engine Verification
#   -> 3. Play Video Clip full screen ( Verify MPO - Plane format ++ )
#   ->      Verify DE ()
#   -> 4. Invoke and Resume from power events ( CS / S3 / S4 )
#   ->      Verify DE ()
#   -> 5. Apply Various Resolution / Mode based on L0(Limited modes only )/L1(ALL  Modes)
#   ->      Verify DE () after every ModeSet
#   -> 6. Play Video Clip ( only if Power event or Mode Set is selected )
#   ->      Verify MPO - Plane format ++ and Verify DE () after every Power Event & ModeSet
#
# CommandLine : python display_dev_bat_v1.py <-gfx_0 -edp_a -gfx_0 -hdmi_b -gfx_0 -dp_c> <-usr eve MPO1/MPO2> <-pwr_eve CS/S3/S4> <-mode_lvl L0/L1> <-SIM/-EMU>
# "-SIM" : Simulation Displays, "-EMU" : Physically connected Displays
#
# @authors      Raghupathy, Dushyanth Kumar, Balaji Gurusamy
################################################################################################
import subprocess

from Libs.Core import reboot_helper
from Libs.Core.logger import etl_tracer, html
from Tests.Display_Dev_BAT.display_dev_bat_v1_base import *

##
# STEP New log level for logging Test steps / Flow
STEP = 25
logging.addLevelName(STEP, "STEP")


##
# Display Dev Bat V1 class : Inherited Display DEV BAT Base test script
class DisplayDevBatV1(DisplayDevBatV1Base):
    config = ''
    displays = []
    gfx_port_adapter_info_list = []

    ##
    # @brief    Disable/Enable Driver and Verify it's running or not
    # @return   None
    def test_disable_enable_driver(self):
        html.step_start("Driver Restart")
        status, reboot_required = display_essential.restart_gfx_driver()
        if status is False:
            self.fail("Display driver restart test failed")
        html.step_end()

    ##
    # @brief    Test steps BAT, refer doc string
    # @return   None
    def test_display_bat(self):

        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        if self.environment_mode == 'SIM':
            html.step_start("Simulating required panels")
            # Unplug all External Displays
            self.unplug_all_external_displays()
            internal_display_list = self.display_config.get_internal_display_list(self.enumerated_displays)
            # Plug all required Displays
            for key, value in self.displays_dict.items():
                for index in range(len(value)):
                    if value[index][0] not in (x[1] for x in internal_display_list):
                        assert display_utility.plug(port=value[index][0], panelindex=value[index][1],
                                                    gfx_index=key.lower()), \
                            "Failed to plug the display"
                        time.sleep(5)
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            logging.info("Simulated Displays : {}".format(self.enumerated_displays.to_string()))
            html.step_end()
        else:
            html.step_start("Checking physical panel requirements for the test")
            ##
            # Block for checking physical panel connectivity. Port name and gfx index can be obtained from
            # display_list
            logging.info("Enumerated Displays : {}".format(self.enumerated_displays.to_string()))
            for display in self.display_list:
                port_and_gfx = display.split(' ')
                check_port = False
                for display_count in range(self.enumerated_displays.Count):
                    con_enum_display = self.enumerated_displays.ConnectedDisplays[display_count]
                    if port_and_gfx[0] == (CONNECTOR_PORT_TYPE(con_enum_display.ConnectorNPortType)).name and \
                            port_and_gfx[1].lower() == con_enum_display.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
                        check_port = True
                        break
                if not check_port:
                    logging.error("Please Check Display Port : {} Physically Connected or NOT".format(display))
                    self.fail("Issues with Physically Connected Displays")
            html.step_end()
        
        # Creating list of list with GFX_index, port and corresponding display adapter info
        for key, value in self.displays_dict.items():
            for index in range(len(value)):
                self.buffer_list = []
                self.buffer_list.append(key)
                self.buffer_list.append(value[index][0])
                display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(value[index][0], key)
                if type(display_and_adapter_info) is list:
                    display_and_adapter_info = display_and_adapter_info[0]
                self.buffer_list.append(display_and_adapter_info)
                self.gfx_port_adapter_info_list.append(self.buffer_list)

        # Apply Config from Sequence XML for Connected Display Ports
        for sequence in self.sequence_list:
            self.config = list(dict(sequence))[0]
            flag = True
            for disp in str(list(dict(sequence).values())[0]).split(","):
                if len(self.display_list) < int(disp):
                    flag = False
            if flag:
                self.seq_counter += 1
                # Replace display list from Setup phase with gfx - port - adapter info.
                self.display_list = self.gfx_port_adapter_info_list
                self.displays = self.map_seq_displays(list(dict(sequence).values())[0])
                # Adapter info lists are created along with port with gfx list.
                displays_adapters = []
                displays_with_gfx = []

                for index in range(0, len(self.displays)):
                    displays_adapters.append(self.displays[index][2])
                    displays_with_gfx.append(str(self.displays[index][1]) + " with " + str(self.displays[index][0]))

                self.apply_config_and_verify(self.config, displays_adapters, True, displays_with_gfx)

                ##
                # Play Video clips and Verify MPO, DE Verification
                if self.user_mpo_events != 'NONE':
                    self.play_video_clip_and_verify_mpo(self.displays[0][1], self.config)

                # ##
                # # Trigger Power Events and DE Verification
                # if self.power_events != 'NONE':
                #     self.seq_counter += 1
                #     logging.log(STEP, "Test Sequence: {0} : Triggering Power Events".format(self.seq_counter))
                #     self.trigger_powerevents_and_verify()

                ##
                # Apply ModeSet and DE Verification
                if self.mode_level != 'NONE':
                    # Seperate Adapter info list for mode level is created , due to dependency on Config.
                    adapter_info_list = []
                    for index in range(len(self.displays)):
                        display_and_adapter_info = self.display_config.get_display_and_adapter_info_ex(
                            self.displays[index][1], self.displays[index][0])
                        if type(display_and_adapter_info) is list:
                            display_and_adapter_info = display_and_adapter_info[0]

                        adapter_info_list.append(display_and_adapter_info)

                    self.apply_modes_and_verify(adapter_info_list, self.enumerated_displays, self.mode_level)

                ##
                # Play Video clips and Verify MPO, DE Verification, only when Power or User Events Enabled.
                if self.power_events != 'NONE' or self.mode_level != 'NONE':
                    if self.user_mpo_events != 'NONE':
                        self.play_video_clip_and_verify_mpo(self.displays[0][1], self.config)

        # Re iterate for Power Events and DE Verification
        for sequence in self.sequence_list:
            self.config = list(dict(sequence))[0]
            flag = True
            for disp in str(list(dict(sequence).values())[0]).split(","):
                if len(self.display_list) < int(disp):
                    flag = False
            if flag:
                # Replace display list from Setup phase with gfx - port - adapter info.
                self.display_list = self.gfx_port_adapter_info_list
                self.displays = self.map_seq_displays(list(dict(sequence).values())[0])
                # Adapter info lists are created along with port with gfx list.
                displays_adapters = []
                displays_with_gfx = []
                powerevent_display_list = []
                for index in range(0, len(self.displays)):
                    displays_adapters.append(self.displays[index][2])
                    displays_with_gfx.append(str(self.displays[index][1]) + " with " + str(self.displays[index][0]))

                powerevent_display_list.append('DP_A with GFX_0')
                if self.config == 'SINGLE' and displays_with_gfx == powerevent_display_list:

                    self.seq_counter += 1
                    self.apply_config_and_verify(self.config, displays_adapters, False, displays_with_gfx)

                    ##
                    # Trigger Power Events and DE Verification
                    if self.power_events != 'NONE':
                        self.trigger_powerevents_and_verify()
                        break
                    html.step_end()

        if 'OFF' not in self.de_verify:
            logging.info("******************** DE Test Results : {} ******************** ".format(self.de_result))
        else:
            logging.info("******************** DE Test Results : DE is OFF ********************")

        # Enable Driver Disable/Enable as part of last step
        self.test_disable_enable_driver()

        # Final Test Result's based on DisplayEngine verification and other's
        if self.de_result is False or self.test_results is False:
            self.fail("FAIL : Display Dev Bat Failed")


##
# @brief        Helper function to run and upload DiAna telemetry data to server
# @return       None
def upload_diana_telemetry():
    # Check if DiAna is downloaded with display tools
    diana_path = os.path.join(test_context.SHARED_BINARY_FOLDER, "DiAna", "DiAna.exe")
    if not os.path.exists(diana_path):
        # If not, don't do anything
        return

    html.step_start("Upload telemetry data")
    # Stop ETL tracing and check for GfxTrace.etl
    etl_tracer.stop_etl_tracer()
    if not os.path.exists(etl_tracer.GFX_TRACE_ETL_FILE):
        # Don't do anything if ETL tracer failed to dump any ETL file
        return

    # rename the file to avoid rewriting
    etl_file_path = os.path.join(
        test_context.LOG_FOLDER, 'GfxTraceDevBAT.' + str(time.time()) + '.etl')
    os.rename(etl_tracer.GFX_TRACE_ETL_FILE, etl_file_path)

    etl_tracer.start_etl_tracer()

    # Run DiAna with special keyword, and a timeout of 10 minutes
    # Redirect the console output to a file to save some time
    with open("temp.txt", "w") as f:
        subprocess.call([diana_path, etl_file_path, "-__DEV_BAT__"], stdout=f, timeout=600)
    html.step_end()


if __name__ == '__main__':
    TestEnvironment.initialize()
    results = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DisplayDevBatV1'))
    try:
        upload_diana_telemetry()
    except Exception as e:
        logging.error(e)
    TestEnvironment.cleanup(results)
