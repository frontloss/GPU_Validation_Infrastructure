#######################################################################################################################
# @file         system_utility_ult_2.0.py
# @brief        Each function in this base will verify the functionality of system_utility.py
# @details      Commandline : python Tests\ULT\system_utility_ult_2.0.py -gfx_index_1
#               Example : python Tests\ULT\system_utility_ult_2.0.py -gfx_0 -edp_a
#               Example : python Tests\ULT\system_utility_ult_2.0.py -gfx_1 -dp_b
#
# @author       Raghupathy
#######################################################################################################################
import unittest

from Libs.Core.wrapper.driver_escape_args import MiscEscProductFamily, MiscEscPlatformType, MiscEscCpuType

from Libs.Core import display_essential
from Libs.Core import enum
from Libs.Core.cmd_parser import parse_cmdline, display_key_pattern
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_utility import plug
from Libs.Core.system_utility import *
from Libs.Core.test_env.test_environment import *
from Libs.Feature.display_engine.de_master_control import *


##
# @brief        IsPostSi Check
# @return       bool - True if PostSi False otherwise
def is_postSi():
    try:
        exec_env = SystemUtility().get_execution_environment_type()
        if exec_env and exec_env.upper() == "SIMENV_FULSIM":
            return False
    except Exception as e:
        logging.warning(str(e))
    return True


##
# @brief        SystemUtility ULT class
class SystemUtilityULT(unittest.TestCase):
    display_dict = {}
    internal_displays_list = {}
    reg_name1 = 'Temp_DWORD_RegistryKey'
    reg_datatype1 = registry_access.RegDataType.DWORD
    data1 = 1

    reg_name2 = 'Temp_Binary_RegistryKey'
    reg_datatype2 = registry_access.RegDataType.BINARY
    data2 = bytes([0, 1, 0, 1, 0, 1])

    ##
    # @brief        SetupClass
    # @return       None
    @classmethod
    def setUpClass(cls):
        logging.info("******************** System Utility ULT 2.0 *************************\n")
        cls.display_config = DisplayConfiguration()
        cls.system_utility = SystemUtility()
        cls.display_engine = DisplayEngine()
        cls.cmd_line_param = parse_cmdline(sys.argv)
        cls.de_result = True

        def add_or_append(dictionary, key, value):
            if key not in dictionary:
                dictionary[key] = []
            dictionary[key].append(value)

        ##
        # connected_list[] is a list of Port Names of the connected Displays
        for index in range(len(cls.cmd_line_param)):
            for key, value in cls.cmd_line_param[index].items():
                if display_key_pattern.match(key) is not None:
                    if value['connector_port'] is not None:
                        add_or_append(cls.display_dict, value['gfx_index'], value['connector_port'])
                        if value['is_lfp'] is True:
                            add_or_append(cls.internal_displays_list, value['gfx_index'], value['connector_port'])

        for key, value in cls.display_dict.items():
            if key in cls.internal_displays_list:
                value = set(cls.internal_displays_list[key]).symmetric_difference(cls.display_dict[key])
            for port in value:
                assert plug(port, gfx_index=str(key).lower()), "Failed to plug the display"

        display_and_adapter_info_list = []
        for key, value in cls.display_dict.items():
            for port in value:
                display_and_adapter_info = cls.display_config.get_display_and_adapter_info_ex(port, key)
                if type(display_and_adapter_info) is list:
                    display_and_adapter_info = display_and_adapter_info[0]
                display_and_adapter_info_list.append(display_and_adapter_info)
        if len(display_and_adapter_info_list) > 0:
            cls.display_config.set_display_configuration_ex(enum.SINGLE, [display_and_adapter_info_list[0]])

    ##
    # @brief    Verifying MMIO Read
    # @return   None
    def test_0_2(self):
        logging.info("******************** TEST_2: START **********************************")
        logging.info("************** mmio_read() & dpcd_read() ****************************")
        logging.info(
            "Now Calling Display_Engine_Verification Which Internally call's and Verify's MMIO Read and DPCD Read ")
        logging.info("Only Subset of Display_Engine_Verification is Called Verify Transcoder () for ULT Purpose ")
        self.display_engine.modify_display_engine_verifiers("0x8")
        self.display_engine.verify_display_engine()
        logging.info("******************** TEST_2: END ************************************\n")

    ##
    # @brief    MMIO Write
    # @return   None
    def test_0_3(self):
        logging.info("******************** TEST_3: START **********************************")
        offset = 0x70180
        reg_value = 2
        logging.info("******************** mmio_write() ***********************************")
        for key, value in self.display_dict.items():
            logging.info("INFO : MMIO Offset : {0}, gfx_index : {1} Read Before write the Register".
                         format(hex(offset), key))
            read_reg_value_before = driver_interface.DriverInterface().mmio_read(offset, str(key).lower())
            logging.info("INFO : Before write the MMIO Register Offset : {0}, gfx_index : {1}, Value is :{2}".
                         format(hex(offset), key, read_reg_value_before))
            logging.info("MMIO write Register Offset: {0}, Value: {1}, Gfx_Index: {2}".
                         format(hex(offset), reg_value, key))
            status = driver_interface.DriverInterface().mmio_write(offset, reg_value, str(key).lower())
            self.assertTrue(status, "FAIL : Write MMIO Failed Status return {}".format(status))
            logging.info("PASS : MMIO write Register Offset: {0} Value: {1} success".format(hex(offset), reg_value))
            read_reg_value_after = driver_interface.DriverInterface().mmio_read(offset, str(key).lower())
            self.assertIsNotNone(reg_value, " FAIL : Return value is none")
            logging.info(
                "INFO : After write the MMIO Register Offset : {0}, gfx_index : {1}, Value is :{2}".format(hex(offset),
                                                                                                           key,
                                                                                                           read_reg_value_after))
            if read_reg_value_before != read_reg_value_after:
                logging.info(
                    "PASS : MMIO Write Offset: {} Value: {} Successfully verified".format(hex(offset), reg_value))
        logging.info("******************** TEST_3: END ************************************\n")

    ##
    # @brief    Get EDID Data
    # @return   None
    def test_0_4(self):
        logging.info("******************** TEST_4: START **********************************")
        logging.info("******************* get_edid_data() *********************************")
        for key, value in self.display_dict.items():
            for port in value:
                logging.info("Get EDID Data of: [{0},{1}]".format(port, key))
                display_and_adapter_info = DisplayConfiguration().get_display_and_adapter_info_ex(port, key)
                if type(display_and_adapter_info) is list:
                    display_and_adapter_info = display_and_adapter_info[0]
                edid_data = SystemUtility().get_edid_data(display_and_adapter_info)
                self.assertIsNotNone(edid_data, "FAIL : Return value is none")
                no_of_extension_blocks = edid_data[126]
                logging.info(
                    "INFO : Port:{0} Gfx_index:{1} No.of.Ext Blocks:{2}".format(port, key, no_of_extension_blocks))
                if port == "DP_A" and no_of_extension_blocks == 0:
                    no_of_extension_blocks = 1
                else:
                    no_of_extension_blocks = no_of_extension_blocks + 1
                logging.info("PASS : Port:{0} Gfx_index:{1} RAW EDID Data is\n".format(port, key))
                hex_dump = ""
                counter = 0
                for index in range(128 * no_of_extension_blocks):
                    if counter != 0 and counter % 16 == 0:
                        logging.info("INFO : {0}".format(hex_dump))
                        hex_dump = ""
                        # hex_dump += "\n"
                    hex_dump += "{:02X} ".format(int(edid_data[index]))
                    counter += 1
                logging.info("INFO : {0}".format(hex_dump))
            logging.info("PASS : Successfully get the EDID of Port:{0} Gfx_index:{1}".format(port, key))
        logging.info("******************** TEST_4: END ************************************\n")

    ##
    # @brief    Disable / Enable LAN
    # @return   None
    @unittest.skipUnless(is_postSi(), "Disable/Enable LAN Not supported on PreSi environment")
    def test_0_5(self):
        logging.info("******************** TEST_5: START **********************************")
        logging.info("**************disable_LAN() & enable_LAN() **************************")
        return_code = SystemUtility().disable_LAN()
        self.assertTrue(return_code, "FAIL : Disabling LAN failed")
        logging.info("PASS : LAN Disabled Successfully")

        return_code = SystemUtility().enable_LAN()
        self.assertTrue(return_code, "FAIL : Enabling LAN failed")
        logging.info("PASS : LAN Enabled Successfully")
        logging.info("******************** TEST_5: END ************************************\n")

    ##
    # @brief        Read Registry
    # @param[in]    adapter - adapter index
    # @param[in]    reg_datatype - Registry Datatype
    # @param[in]    reg_name - Registry Name
    # @return       None
    def read_registry(self, adapter, reg_datatype, reg_name):
        logging.info("Reading Registry Key {0} in {1} Hive".format(reg_name, adapter))
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=adapter)
        value, _ = registry_access.read(args=reg_args, reg_name=reg_name)
        self.assertIsNotNone(value, "FAIL : Read Registry {0} {1} Failed".format(reg_name, adapter))
        logging.info("PASS : Read Registry {0} success".format(reg_name))
        return value

    ##
    # @brief        Write Registry
    # @param[in]    adapter - adapter index
    # @param[in]    reg_datatype - Registry Datatype
    # @param[in]    reg_name - Registry Name
    # @param[in]    reg_data_list - Data
    # @return       None
    def write_registry(self, adapter, reg_datatype, reg_name, reg_data_list=None):
        logging.info("Writing Registry Key {0} in {1} Hive".format(reg_name, adapter))
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=adapter)
        status = registry_access.write(args=reg_args, reg_name=reg_name, reg_type=reg_datatype, reg_value=reg_data_list)
        self.assertTrue(status, "FAIL : Write Registry {0} {1} failed".format(reg_name, adapter))
        logging.info("PASS : Write Registry Key {0} success".format(reg_name))

    ##
    # @brief        Delete Registry
    # @param[in]    adapter - adapter index
    # @param[in]    reg_name - Registry Name
    # @return       None
    def delete_registry(self, adapter, reg_name):
        logging.info("Deleting Registry Key {0} from {1}".format(reg_name, adapter))
        reg_args = registry_access.StateSeparationRegArgs(gfx_index=adapter)
        status = registry_access.delete(args=reg_args, reg_name=reg_name)
        self.assertTrue(status, "FAIL : Delete Registry Key {0} {1} failed".format(reg_name, adapter))
        logging.info("PASS : Delete Registry Key {0}success".format(reg_name))

    ##
    # @brief    Write Registry
    # @return   None
    def test_0_6(self):
        logging.info("******************** TEST_6: START **********************************")
        logging.info("******************* write_registry() ********************************")
        for key, value in self.display_dict.items():
            self.write_registry(str(key).lower(), self.reg_datatype1, self.reg_name1, self.data1)
            value = self.read_registry(str(key).lower(), self.reg_datatype1, self.reg_name1)
            if value == self.data1[0]:
                logging.info("PASS : Registry {} Successfully Verified ".format(self.reg_name1))
            self.write_registry(str(key).lower(), self.reg_datatype2, self.reg_name2, self.data2)
            value = self.read_registry(str(key).lower(), self.reg_datatype2, self.reg_name2)
            if len(value) == len(self.data2) and len(value) == sum([1 for i, j in zip(value, self.data2) if i == j]):
                logging.info("PASS : Registry {} Successfully Verified ".format(self.reg_name2))
        logging.info("******************** TEST_6: END ************************************\n")

    ##
    # @brief    Read Registry
    # @return   None
    def test_0_7(self):
        logging.info("******************** TEST_7: START **********************************")
        logging.info("******************* read_registry() *********************************")
        for key, value in self.display_dict.items():
            self.read_registry(str(key).lower(), self.reg_datatype1, self.reg_name1)
            self.read_registry(str(key).lower(), self.reg_datatype2, self.reg_name2)
        logging.info("******************** TEST_7: END ************************************\n")

    ##
    # @brief    Delete Registry
    # @return   None
    def test_0_8(self):
        logging.info("******************** TEST_8: START **********************************")
        logging.info("*******************delete_registry() ********************************")
        for key, value in self.display_dict.items():
            self.delete_registry(str(key).lower(), self.reg_name1)
            self.delete_registry(str(key).lower(), self.reg_name2)
        logging.info("******************** TEST_8: END ************************************\n")

    ##
    # @brief    TDR Generate / Detect
    # @return   None
    @unittest.skipUnless(is_postSi(), "INFO : Not supported on PreSi environment")
    def test_0_9(self):
        logging.info("******************** TEST_9: START **********************************")
        logging.info("**********generate_TDR() & detect_system_TDR() **********************")
        logging.info("Generate TDR")
        return_code = display_essential.generate_tdr('gfx_0', True)
        self.assertTrue(return_code, "FAIL : Failed to generate TDR")
        logging.info("PASS : Generate TDR success")

        logging.info("Detect TDR")
        return_code = display_essential.detect_system_tdr('gfx_0')
        self.assertTrue(return_code, "FAIL : Failed to detect TDR")
        logging.info("PASS : Detect TDR success")
        logging.info("******************** TEST_9: END ************************************\n")

    ##
    # @brief    Checking the Driver is DOD or Not
    # @return   None
    @unittest.skipUnless(is_postSi(), "INFO : Not supported on PreSi environment")
    def test_1_0(self):
        logging.info("******************** TEST_10: START *********************************")
        logging.info("******Is_DOD_Driver_Path(), enable_DoD() & disable_DoD() ************")
        status = env_settings.is_dod_driver_path()
        self.assertIsNotNone(status, "FAIL : Invalid WinDoD value")
        # Enable DoD path
        if status is False:
            return_status_enable_DoD = env_settings.switch_dod_path(True)
            if return_status_enable_DoD is False:
                logging.info("FAIL : Enable DoD API failed!!")
            else:
                driver_restart, reboot_required = display_essential.restart_gfx_driver()
                self.assertTrue(driver_restart, "Driver restart failed after DOD enable")
                logging.info("PASS : Enable DoD API Success")
        # Disable DoD path
        return_status_disable_DoD = env_settings.switch_dod_path(False)
        if return_status_disable_DoD is True:
            driver_restart, reboot_required = display_essential.restart_gfx_driver()
            self.assertTrue(driver_restart, "Driver restart failed after DOD disable")
            logging.info("PASS : Disable DoD API Success")
        else:
            logging.info("FAIL: Disable DoD API failed!!")
        logging.info("******************** TEST_10: END ***********************************\n")

    ##
    # @brief    Is_DDRW
    # @return   None
    def test_1_1(self):
        logging.info("******************** TEST_11: START *********************************")
        logging.info("************************Is_DDRW() ***********************************")
        for key, value in self.display_dict.items():
            if self.system_utility.is_ddrw(str(key).lower()) is False:
                logging.info("PASS : {} is a LEGACY Platform".format(key))
            else:
                logging.info("PASS : {} is a YANGRA Platform".format(key))
        logging.info("******************** TEST_11: END ***********************************\n")

    ##
    # @brief    Get Execution Environment Type
    # @return   None
    def test_1_2(self):
        logging.info("******************** TEST_12: START *********************************")
        logging.info("***********get_execution_environment_type() *************************")
        exec_env = self.system_utility.get_execution_environment_type()
        self.assertIsNotNone(exec_env, "FAIL : Failed to Get Execution Environment Type")
        logging.info("PASS : Environment Type is {0}".format(exec_env))
        logging.info("******************** TEST_12: END ***********************************\n")

    ##
    # @brief    Get Miscellaneous  System Information
    # @return   None
    def test_1_3(self):
        logging.info("******************** TEST_13: START *********************************")
        logging.info("*****************get_misc_system_info() *****************************")
        for key, value in self.display_dict.items():
            misc_system_info = self.system_utility.get_misc_system_info(str(key).lower())
            self.assertIsNotNone(misc_system_info, "FAIL : Failed to Get Miscellaneous System Information")
            logging.info("PASS : Miscellaneous System Information for {}".format(key))
            logging.info("       INFO : GopVersion          : {}".format(misc_system_info.GopVersion))
            logging.info("       INFO : IsS0ixCapable       : {}".format(misc_system_info.IsS0ixCapable))
            logging.info("       INFO : WDDMVer             : {}".format(misc_system_info.OSInfo.WDDMVer))
            logging.info("       INFO : ProductFamily       : {}".format(
                MiscEscProductFamily(misc_system_info.PlatformInfo.ProductFamily.value).name))
            logging.info("       INFO : PlatformType        : {}".format(
                MiscEscPlatformType(misc_system_info.PlatformInfo.PlatformType.value).name))
            logging.info("       INFO : CPUType             : {}".format(
                MiscEscCpuType(misc_system_info.PlatformInfo.CPUType.value).name))
            logging.info(
                "       INFO : MaxSupportedPipes   : {}".format(misc_system_info.PlatformInfo.MaxSupportedPipes))
        logging.info("******************** TEST_13: END ***********************************\n")

    ##
    # @brief    Restart Driver
    # @return   None
    @unittest.skipUnless(is_postSi(), "INFO : Not supported on PreSi environment")
    def test_1_4(self):
        logging.info("******************** TEST_14: START *********************************")
        logging.info("****************restart_gfx_driver() ****************************")
        for key, value in self.display_dict.items():
            disable_enable_status, reboot_required = display_essential.restart_gfx_driver()
            self.assertTrue(disable_enable_status,
                            "FAIL : API for Disabled and Enabled Gfx driver : {} ..failed".format(key))
            logging.info("PASS : Successfully Disabled and Enabled the Gfx Driver : {}".format(key))
        logging.info("******************** TEST_14: END ***********************************\n")

    ##
    # @brief    VRR test
    # @return   None
    @unittest.skipUnless(is_postSi(), "INFO : Not supported on PreSi environment")
    def test_1_5(self):
        from Libs.Core import system_utility
        logging.info("******************** TEST_15: START *********************************")
        logging.info("**********************get_set_vrr() *********************************")
        for key, value in self.display_dict.items():
            if self.system_utility.is_ddrw(str(key).lower()):
                vrr_args = system_utility.DdCuiEscGetSetVrrArgs()
                vrr_args.Operation = system_utility.DdCuiEscVrrOperation.GET_INFO
                system_utility.SystemUtility().get_set_vrr('gfx_0', vrr_args)
                logging.info("INFO : DdCuiEscGetSetVrrArgs Information for {}".format(key))
                logging.info("       INFO : Operation               : {}".format(vrr_args.Operation))
                logging.info("       INFO : VrrSupported            : {}".format(vrr_args.VrrSupported))
                logging.info("       INFO : VrrEnabled              : {}".format(vrr_args.VrrEnabled))
                logging.info("       INFO : VrrHighFpsSolnEnabled   : {}".format(vrr_args.VrrHighFpsSolnEnabled))
                logging.info("       INFO : VrrLowFpsSolnEnabled    : {}".format(vrr_args.VrrLowFpsSolnEnabled))
                logging.info("       INFO : NumDisplays             : {}".format(vrr_args.NumDisplays))
                for count in range(vrr_args.NumDisplays + 1):
                    logging.info(
                        "       INFO : EscVrrInfo TargetId     : {}".format(vrr_args.EscVrrInfo[count].TargetId))
                    logging.info("       INFO : EscVrrInfo MinRr        : {}".format(vrr_args.EscVrrInfo[count].MinRr))
                    logging.info("       INFO : EscVrrInfo MaxRr        : {}".format(vrr_args.EscVrrInfo[count].MaxRr))
                if vrr_args.VrrEnabled is False:
                    logging.info("PASS: VRR Status is DISABLED")
                else:
                    logging.info("PASS: VRR Status is ENABLED")
            else:
                logging.info("INFO : VRR feature not support for LEGACY")
        logging.info("******************** TEST_15: END ***********************************\n")


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_result = display_logger.log_test_result(script_name, outcome.result)
    TestEnvironment.cleanup(outcome.result)
