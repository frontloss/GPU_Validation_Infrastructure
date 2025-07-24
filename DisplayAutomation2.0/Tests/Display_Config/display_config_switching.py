######################################################################################
# @file
# @section display_config_switching
# @remarks
# <b> Test Name: DisplayConfigSwitch </b> <br>
# @ref display_config_switching.py
# <ul>
# <li> <b> Description: </b> <br>
# @brief Common test to verify the following for various display switching sequences mentioned in the DisplaySequence.xml<br>
# 1. Config<br>
# 2. Clock<br>
# 3. Display Engine (Pipe, Port, Plane Trtanscoder Programming)
# 4. Underrun
# </li>
#
# <li> <b> Execution Command(s) : </b> <br>
# <ul>
# <li> python display_switching.py -edp_a -dp_b
# </li>
# <li> python display_switching.py -edp_a -dp_b -hdmi_c - seq seq1
# </li>
# <li> python display_config_switching.py -edp_a -hdmi_b -dp_d -dp_e -select_group3 True
# </li>
# </ul>
# </li>
# @author rradhakr
######################################################################################
import copy
import os
import re

from Libs.Core.logger import html
from Libs.Feature.display_engine import de_master_control
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_engine.de_base import display_base
from Tests.Display_Config.display_config_base import *


##
# @brief Display Config Switching Base class : Test Class to run Config tests
class DisplayConfigSwitch(DisplayConfigBase):
    dfc_key_name = "DisplayFeatureControl"
    dfc_default_value = []
    dfc_type = []
    for index in range(len(DisplayConfigBase.platform_dict)):
        value, reg_type = registry_access.read(args=DisplayConfigBase.ss_reg_args[index], reg_name=dfc_key_name)
        dfc_default_value.append(value)
        dfc_type.append(reg_type)

    ##
    # @brief pre setup function. Sets the port based on the displays passed in the command line and reboot
    # @return  None
    def test_pre_test_setup(self):
        system_reboot_required = False
        driver_restart_required = []

        for index in range(len(self.platform_dict)):
            driver_restart_required.append(False)

        # Check for Dynamic CD clk flag
        for flag, index in [(self.controlFlag.data.dynamic_cd_clk_gfx_0, 0), (self.controlFlag.data.dynamic_cd_clk_gfx_1, 1)]:
            if flag:
                gfx_index = 'gfx_' + str(index)
                gfx_vbt = Vbt(gfx_index)
                gfx_vbt.block_1.BmpBits2 |= 0x40
                logging.info("Enabling Dynamic CD CLK in VBT for {}".format(gfx_index))
                if gfx_vbt.apply_changes() is False:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Config] Failure in setting VBT Block 1 for Dynamic CD Clock enabling "
                              "in {}".format(gfx_index),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    logging.error('Setting VBT block 1 for Dynamic CD CLK failed for {}'.format(gfx_index))
                system_reboot_required = True

        # enable DP SSC if user flag is set
        for flag, index in [(self.controlFlag.data.enable_efp_ssc_gfx_0, 0), (self.controlFlag.data.enable_efp_ssc_gfx_1, 1)]:
            if flag:
                gfx_index = 'gfx_' + str(index)
                gfx_vbt = Vbt(gfx_index)
                gfx_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Enable = 1
                gfx_vbt.block_1.IntegratedDisplaysSupported.DP_SSC_Dongle_Enable = 1
                logging.info("Enabling DP SSC (both regular and dongle) in VBT")
                if gfx_vbt.apply_changes() is False:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Config] Failure in setting VBT Block 1 for DP SSC enabling in {}".format(gfx_index),
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail('Setting VBT block 1 failed, after enabling DP SSC')
                driver_restart_required[index] = True

        # Disable MPO if user flag is set
        for flag, index in [(self.controlFlag.data.disable_mpo_gfx_0, 0), (self.controlFlag.data.disable_mpo_gfx_1, 1)]:
            if flag:
                gfx_index = 'gfx_' + str(index)
                if self.dfc_default_value[index] is None:  # unexpected
                    logging.error('Error while reading registry')
                    self.fail()
                logging.debug('Initial value of registry : {0}'.format(hex(self.dfc_default_value[index])))
                new_value = self.dfc_default_value[index] & 0xFFFFFFDF  # Clear bit 5 to disable MPO
                if new_value == self.dfc_default_value[index]:
                    logging.info(
                        'MPO already disabled in display feature control for {}, so skipping registry write operation'.format(
                            gfx_index))
                else:
                    logging.info('Disabling MPO in display feature control reg key')
                    if registry_access.write(args=self.ss_reg_args[index], reg_name=self.dfc_key_name,
                                             reg_type=registry_access.RegDataType.DWORD, reg_value=new_value) is False:
                        logging.error('Error while writing registry')
                        self.fail()
                    logging.debug('New registry value :{0} for adapter {1}'.format(hex(new_value), gfx_index))
                    driver_restart_required[index] = True

        # Do system reboot when required
        if system_reboot_required:
            if reboot_helper.reboot(self, 'test_apply_and_save_config') is False:
                logging.error("Failed to reboot the system")
        # Restart the display driver when required. If system reboot is going to happen, driver restart not required.

        elif True in driver_restart_required:
            for index in range(len(self.platform_dict)):
                gfx_index = "gfx_" + str(index)
                if driver_restart_required[index] is True:
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        self.fail('Failed to restart Display driver {}'.format(gfx_index))
                        # GDHM handled in enable_driver() & disable_driver()
                    logging.info('Display driver restarted successfully for {}'.format(gfx_index))


    ##
    # @brief start execution of test apply and save config.
    # @details Apply all the Configs in the sequence and save the scenarios for each sequence.
    # @return None
    def test_apply_and_save_config(self):
        is_pipe_joiner = False
        ##
        # Unplug the displays and restore the configuration to the initial configuration
        self.unplug_displays()

        # Check if the commandline has 3 DP display port's. If more than 3 DP requested use Group2 Panel list
        # to accommodate DisplayBW
        dp_group = {'gfx_0': []}
        for k in self.display_edid_dpcd.keys():
            port_regex = re.search("(DP).*", k)
            index_regex = re.search("^(GFX_).[0-9]*", k)
            index_regex = index_regex.group(0).lower() if index_regex else 'gfx_0'
            if port_regex:
                if (index_regex in dp_group.keys()) and (type(dp_group[index_regex]) == list):
                    dp_group[index_regex].append(port_regex.group(0))
                else:
                    dp_group[index_regex] = [port_regex.group(0)]

        # Verify and plug the display
        for count, (port, edid_dpcd) in enumerate(self.display_edid_dpcd.items()):
            gfx_index = str(port.split("_")[0] + "_"+port.split("_")[1]).lower()
            connector_port = port.split("_")[2]+"_"+port.split("_")[3]
            connector_type = port.split("_")[4]
            if display_utility.get_vbt_panel_type(connector_port, gfx_index) not in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                # If user wants to run test with 19x10 resolution, this custom flag is used.
                # Main intension is to use 19x10 EDID on P2D to reduce execution time.
                if self.selected_group3:
                    logging.info(
                        "User has selected Group3 data using custom flag. All panels will be plugged with 19x10")
                    edid = edid_dpcd[2][0]
                    dpcd = edid_dpcd[2][1]

                # we can't have max resolution on 3 DP (or more) due to limitation.
                # If three or more DP ports are passed in command line, use group 2 data (lesser resolution)
                if (gfx_index in dp_group.keys()) and (len(dp_group[gfx_index]) >= 3):
                    logging.debug(
                        "Three or more DP ports passed in command line, replace edid/dpcd with Group2 data - %s %s" % (
                            edid_dpcd[1][0], edid_dpcd[1][1]))
                    edid = edid_dpcd[1][0]
                    dpcd = edid_dpcd[1][1]

                ## for platforms ICLLP and TGL, DP on combo phy doesn't support HBR3. In this case, select group 2 data (HBR2)
                elif (self.platform_dict[gfx_index] in ['ICLLP', 'TGL', 'ADLP'] and self.phy_type(self.platform_dict[gfx_index], (port.split("_")[3])) == COMBO_PHY):
                    edid = edid_dpcd[1][0]
                    dpcd = edid_dpcd[1][1]

                else:
                    edid = edid_dpcd[0][0]
                    dpcd = edid_dpcd[0][1]

                if not display_utility.plug(connector_port, edid, dpcd, is_low_power=False, port_type=connector_type,
                                            panelindex=None, gfx_index=gfx_index.lower()):
                    # Gdhm hanled in display_utility.plug()
                    self.fail('Aborting test as failed to plug {} on gfx_adapter {}'.format(connector_port, gfx_index))
        # Creating text file for saving config and test result
        file_path = os.path.join(test_context.TestContext.root_folder(),
                                 'Tests\\Display_Config\\' + 'display_config.txt')

        with open(file_path, "a+") as f:
            f.writelines("test_result:" + "\n") if self.controlFlag.asbyte else f.writelines("test_result:")

        new_display_sequence = []
        gfx_0_counter = 1
        gfx_1_counter = 1

        logging.info(self.adapter_list)

        for i in range(len(self.adapter_list)):
            if (self.adapter_list[i].lower() == 'gfx_0'):
                new_display_sequence.insert(i, 'a' + str(gfx_0_counter))
                gfx_0_counter += 1
            elif (self.adapter_list[i].lower() == 'gfx_1'):
                new_display_sequence.insert(i, 'b' + str(gfx_1_counter))
                gfx_1_counter += 1
            else:
                logging.info("Adapter is not expected")


        for sequence in self.sequence_list:
            config = list(dict(sequence))[0]
            flag = True

            current_config_adapter = []
            for disp in str(list(dict(sequence).values())[0]).split(","):
                if (disp not in new_display_sequence):
                    flag = False

            if flag:
                adapters, displays, display_type = self.map_seq_displays(list(dict(sequence).values())[0], new_display_sequence)
                html.step_start(
                    "-------------Setting {0} with displays: {1} --> {2} --> {3}-----------------".format(config,
                                                                                                          adapters,
                                                                                                          displays,
                                                                                                          display_type))
                self.set_and_validate_config(config, displays, adapters)
                html.step_end()
                if self.controlFlag.asbyte:
                    #Saving applied sequence to file
                    with open(file_path, "a+") as f:
                        #Saving applied sequence to file
                        applied_sequence = [str(adapters), ":", str(config), ":", str(displays), "\n"]
                        f.writelines(applied_sequence)
                else:
                    pipe_dict= {} # Pipe dict containing - key = gfx_index (Adapter name), value = [pipe_obj]. E.g: {'gfx_0':[DisplayPipe(), DisplayPipe()] }
                    plane_dict = {} # Plane dict containing - key = gfx_index (Adapter name), value = [plane_obj]. E.g: {'gfx_0':[DisplayPlane(), DisplayPlane()] }

                    for adapter, display in zip(adapters, displays):
                        pipe_obj = de_base_interface.DisplayPipe(display_port=display, gfx_index=adapter)
                        pipe_dict.setdefault(adapter, []).append(pipe_obj)
                        plane_obj = de_base_interface.DisplayPlane(display_port=display, gfx_index=adapter)
                        plane_dict.setdefault(adapter, []).append(plane_obj)

                        # Check pipe_joiner case
                        is_pipe_joiner_required, no_of_pipe_required = DisplayClock.is_pipe_joiner_required(
                            adapter, display)

                        if is_pipe_joiner_required:
                            logging.info("Pipe Joiner is enabled")
                            # create pipe and plane lists accordingly to pass it to DE Verification
                            for i in range(1, no_of_pipe_required):
                                # Append Pipe Obj
                                pipe_obj_copy = copy.deepcopy(pipe_obj)
                                pipe_dict[adapter].append(pipe_obj_copy)
                                adjacent_pipe = chr(ord(pipe_obj.pipe[-1]) + 1)  # If PIPE_B is assigned, we have to assign adjacent PIPE_C for pipe joiner display.
                                pipe_dict[adapter][i].pipe = "PIPE_" + adjacent_pipe
                                pipe_suffix = display_base.GetPipeSuffix(pipe_obj.pipe)
                                pipe_dict[adapter][i].pipe_suffix = pipe_suffix

                                # Append Plane Obj
                                plane_obj_copy = copy.deepcopy(plane_obj)
                                plane_dict[adapter].append(plane_obj_copy)
                                plane_dict[adapter][i].pipe = "PIPE_" + adjacent_pipe
                                plane_dict[adapter][i].pipe_suffix = pipe_suffix

                    for adapter in set(adapters):
                        display_engine = de_master_control.DisplayEngine(adapter)
                        self.disable_powerwell_verifier_for_TGL_EMU(display_engine, adapter)
                        ports = []
                        self.enum_displays = self.display_config.get_enumerated_display_info()
                        for i in range(self.enum_displays.Count):
                            connector_port = CONNECTOR_PORT_TYPE(
                                self.enum_displays.ConnectedDisplays[i].ConnectorNPortType).name
                            if self.enum_displays.ConnectedDisplays[i].IsActive and \
                                    self.enum_displays.ConnectedDisplays[
                                        i].DisplayAndAdapterInfo.adapterInfo.gfxIndex == adapter:
                                ports.append(connector_port)

                        if self.platform_dict[adapter] in ['MTL', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
                            logging.info(f"Verifying Voltage Level notified to PCode for {self.platform_dict[adapter]}")
                            if DisplayClock.verify_voltage_level_notified_to_pcode(adapter, ports) is False:
                                logging.error(f"FAIL: DVFS VoltageLevel verification failed for {ports} on {adapter}")
                                gdhm.report_driver_bug_pc("[Interfaces][Display_Engine][CD Clock] Failed to verify "
                                                          "Voltage level during Display Config switching",
                                                          gdhm.ProblemClassification.FUNCTIONALITY)
                            else:
                                logging.info("PASS: DVFS VoltageLevel verification successful")
                        else:
                            logging.warning(f"Skipping DVFS VoltageLevel verification for unsupported platform"
                                            f" {self.platform_dict[adapter]}.")
                        verification_result = display_engine.verify_display_engine(ports,
                                                                                   planeList= plane_dict[adapter],
                                                                                   pipeList= pipe_dict[adapter],
                                                                                   gfx_index=adapter)
                        with open(file_path, "a+") as f:
                            f.writelines(str(verification_result) + "-display_engine_verification:")

    ##
    # @brief start execution of power events.
    # @details Apply all power events CS,S3,S4,S5as per input
    #         the scenarios for each sequence
    # @return None
    def test_run_powerevents(self):
        if self.controlFlag.asbyte:
            test_result = True
            # Performing power events
            test_result &= self.set_and_validate_powerevents()
            # Saving power event results to file
            file_path = os.path.join(test_context.TestContext.root_folder(),
                                     'Tests\\Display_Config\\' + 'display_config.txt')
            with open(file_path, "a+") as f:
                power_event_test_result = str("test_result:" + str(test_result) + ":")
                f.writelines(power_event_test_result+"-power_event_test")
            if self.controlFlag.data.reboot:
                if reboot_helper.reboot(self, 'test_verify_applied_config') is False:
                    logging.error("Failed to reboot the system")
                    # Gdhm handled in reboot_helper.reboot()

    ##
    # @brief start execution of verifying saved and applied configurations after power eventor in case of user_event set.
    # @details Verifies the scenarios for each sequence
    # @return None
    def test_verify_applied_config(self):
        current_adapter_list = []
        display_adapter_details = []

        if self.controlFlag.asbyte & 0xF != 0: #Any Power event is set
            file_path = os.path.join(test_context.TestContext.root_folder(),
                                     'Tests\\Display_Config\\' + 'display_config.txt')
            with open(file_path, "r+") as f:
                read_file = f.readlines()
                count = 0
                logging.info("File contents: Saved Config Before PowerEvents")
                for line in read_file:
                    logging.info("\tLine {} - {}".format(count, line))
                    count = count + 1

            with open(file_path, "r+") as f:
                saved_sequence = f.readlines()[-2].strip()
                saved_config = saved_sequence.split(":")

            current_config = self.display_config.get_current_display_configuration_ex()
            self.enumerated_displays = self.display_config.get_enumerated_display_info()
            display_adapter_details = current_config[2]
            for each_display_and_adapter_info in display_adapter_details:
                current_adapter_list.append(each_display_and_adapter_info.adapterInfo.gfxIndex)

            n = len(current_config[1])
            current_adapter_list = current_adapter_list[:n]

            logging.info("Before all power events, Saved config is {0}:{1}: {2}".format(saved_config[0].lower(), saved_config[1], str(saved_config[2])))
            logging.info("After all power events, Current config is {0}:{1}:{2}".format(current_adapter_list, current_config[0], current_config[1]))

            adapter_list = saved_config[0].replace("\'","").strip('][').split(', ')
            display_list = saved_config[2].replace("\'","").strip('][').split(', ')
            if (adapter_list.sort() == current_adapter_list.sort() and (saved_config[1] == str(current_config[0]))):
                if (saved_config[2] == str(current_config[1])):
                    logging.info("Current configuration and saved configuration are same!")
                elif len(self.platform_dict) > 1 and display_list.sort() == current_config[1].sort():
                    logging.warning("Order of displays returned by OS from get config is different than that of set config,"
                                    " for Multi adapter scenario")
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Config] Displays in current config and saved config are not same",
                        problem_classification=gdhm.ProblemClassification.OTHER,
                        component=gdhm.Component.Test.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P3,
                        exposure=gdhm.Exposure.E3
                    )
                    self.fail('Displays in current config and saved config are not same')
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Config] Current and saved configuration are not same! ",
                    problem_classification=gdhm.ProblemClassification.OTHER,
                    component=gdhm.Component.Test.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("Current configuration and saved configuration are not same!")

    ##
    # @brief start execution of display engine verification after power events or in case of user_event set.
    # @details Verifies the scenarios for each sequence
    # @return None
    def test_display_engine_verification(self):
        if self.controlFlag.asbyte:
            test_result = True
            display_engine = de_master_control.DisplayEngine()
            self.disable_powerwell_verifier_for_TGL_EMU(display_engine)
            test_result &= display_engine.verify_display_engine()
            logging.info("Verifying Display Engine in case of User Events passed in cmdline")
            file_path = os.path.join(test_context.TestContext.root_folder(),
                                     'Tests\\Display_Config\\' + 'display_config.txt')

            f = open(file_path, "a+")
            current_config = self.display_config.get_current_display_configuration_ex()
            display_adapter_details = current_config[2]
            for each_display_and_adapter_info in display_adapter_details:
                adapter = str(each_display_and_adapter_info.adapterInfo.gfxIndex).lower()
                display_engine = de_master_control.DisplayEngine(adapter)
                self.disable_powerwell_verifier_for_TGL_EMU(display_engine, adapter)
                verification_result = display_engine.verify_display_engine(gfx_index=adapter)
                # Saving display engine verification result into file
                with open(file_path, "a+") as f:
                    f.write(str(verification_result)+"-display_engine_verification_after_power_event")

    ##
    # @brief        Helper function to disable powerwell verifier in display engine, for TGL emulation tests.
    # @details      This is required as we saw PG status is not clearing even after unplug EFP on some TGL systems
    # @param[in]    display_engine object of the class DisplayEngine. It is modified in-place.
    # @param[in]    gfx_index Graphics index for current adapter
    # @return       None
    def disable_powerwell_verifier_for_TGL_EMU(self, display_engine: de_master_control.DisplayEngine,
                                               gfx_index='gfx_0'):
        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        platform = adapter_info.get_platform_info().PlatformName.upper()
        simulation_type = env_settings.get('SIMULATION', 'simulation_type')

        # skip powerwell verification for SHE emulator tests on TGL, as we saw PG status
        # is not clearing even after unplug EFP on some TGL systems
        if platform == 'TGL' and simulation_type == 'SHE':
            display_engine.remove_verifiers(de_master_control.VerificationMethod.POWERWELL)

    ##
    # @brief start execution of resetting dynamic CD clk if set by user.
    # @return None
    def test_reset_dynamic_cd_clk(self):
        for flag, index in [(self.controlFlag.data.dynamic_cd_clk_gfx_0, 0), (self.controlFlag.data.dynamic_cd_clk_gfx_1, 1)]:
            if flag:
                gfx_index = 'gfx_' + str(index)
                logging.info("INFO : End of test - Dynamic CD CLK is set in VBT,Resetting it")
                if flag:
                    gfx_vbt = Vbt(gfx_index)
                    gfx_vbt.block_1.BmpBits2 |= 0xBF
                    if (gfx_vbt.apply_changes() is False):
                        gdhm.report_bug(
                            title="[Interfaces][Display_Config] Setting VBT block 1 for Dynamic CD CLK failed in {}".format(gfx_index),
                            problem_classification=gdhm.ProblemClassification.OTHER,
                            component=gdhm.Component.Test.DISPLAY_INTERFACES,
                            priority=gdhm.Priority.P3,
                            exposure=gdhm.Exposure.E3
                        )
                        logging.error('Setting VBT block 1 for Dynamic CD CLK failed')
                    if reboot_helper.reboot(self, 'test_unplug_ext_displays') is False:
                        logging.error("Failed to reboot the system")
                        # Gdhm handled in reboot_helper.reboot()

    ##
    # @brief unplug the external Displays
    # @return None
    def test_unplug_ext_displays(self):
        # unplug external displays
        logging.debug("Removing attached external displays")
        self.unplug_displays()

    ##
    # @brief start execution of resetting mpo in registry.
    # @return None
    def test_reset_mpo_registry(self):
        for flag, index in [(self.controlFlag.data.disable_mpo_gfx_0, 0), (self.controlFlag.data.disable_mpo_gfx_1, 1)]:
            if flag:
                gfx_index = 'gfx_' + str(index)
                # Revert back the initial registry value
                new_value, reg_type = registry_access.read(args=self.ss_reg_args[index], reg_name=self.dfc_key_name)
                if new_value is None:  # Call failed if value is NULL
                    logging.error('Error while reading registry for {}'.format(gfx_index))
                    self.fail()
                if new_value == self.dfc_default_value[index]:
                    logging.info(
                        'Setup did not disable MPO as it was already disabled in registry for {}, so skipping reset'.format(
                            gfx_index))
                else:
                    if registry_access.write(args=self.ss_reg_args[index], reg_name=self.dfc_key_name,
                                             reg_type=registry_access.RegDataType.DWORD,
                                             reg_value=self.dfc_default_value[index]) is False:
                        logging.error('Error while writing registry for {}'.format(gfx_index))
                        self.fail()
                    logging.debug(
                        'Reset value of registry : {0} for {1}'.format(hex(self.dfc_default_value[index]), gfx_index))
                    # Restart the display driver to apply the reset/default value
                    status, reboot_required = display_essential.restart_gfx_driver()
                    if status is False:
                        logging.error("Failed to restart Display driver")
                        self.fail()
                        # gdhm already handled in enable_driver() & disable_driver()
                    logging.info(
                        'Display driver {} restarted successfully after reset of DisplayFeatureControl regkey bit 5'.format(
                            gfx_index))

    ##
    # @brief start execution of test for printing final result.
    # @return None
    def test_print_test_result(self):
        test_result = []
        file_path = os.path.join(test_context.TestContext.root_folder(),
                                 'Tests\\Display_Config\\' + 'display_config.txt')
        if os.path.exists(file_path):
            if os.stat(file_path).st_size != 0:
                with open(file_path, "r+") as f:
                    for line in f:
                        if "test_result" in line:
                            test_result = line.split(":")

                os.remove(file_path)
                for result_and_feature in test_result[1:]:
                    logging.info(result_and_feature)
                    result_feature_list = result_and_feature.split("-")
                    if result_feature_list[0] == 'False':
                        self.fail(f"FAIL: Display Config Switching due to failure in {result_feature_list[1]}")
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Config] Display Config Switching failed as display_config.txt doesnt exist",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P3,
                exposure=gdhm.Exposure.E3
            )
            self.fail(f"FAIL: Display Config Switching failed as display_config.txt doesnt exist")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(verbosity=2, failfast=True)
    results = runner.run(reboot_helper.get_test_suite('DisplayConfigSwitch'))
    TestEnvironment.cleanup(results)
