########################################################################################################################
# @file     test_context.py
# @brief    TestContext API provide interface to get current test context.
# @author   Beeresh Gopal, Suraj Gaikwad, Ami Golwala, Praburaj Krishnan
########################################################################################################################
import os
import platform
import xml.etree.ElementTree as eTree

from Libs.Core.core_base import singleton

# Exposing import namespace
__all__ = ["os", "platform", "TestContext", "ROOT_FOLDER", "BIN_FOLDER", "LOG_FOLDER", "DLL_FOLDER",
           "TEST_STORE_FOLDER", "COMMON_BIN_FOLDER", "TEST_SPECIFIC_BIN_FOLDER", "PANEL_INPUT_DATA_FOLDER",
           "SHARED_BINARY_FOLDER", "TEST_TEMP_FOLDER", "TestContextPersistence", "GTA_EMULATOR_CONFIG_FILE"]

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BIN_FOLDER = os.path.join(ROOT_FOLDER, 'Bin')
LOG_FOLDER = os.path.join(ROOT_FOLDER, 'Logs')
DLL_FOLDER = os.path.join(ROOT_FOLDER, 'Bin')
TEST_STORE_FOLDER = os.path.join(ROOT_FOLDER, 'TestStore')
COMMON_BIN_FOLDER = os.path.join(TEST_STORE_FOLDER, 'CommonBin')
TEST_SPECIFIC_BIN_FOLDER = os.path.join(TEST_STORE_FOLDER, 'TestSpecificBin')
TEST_TEMP_FOLDER = os.path.join(os.getcwd()[:2], "\\Temp")
PANEL_INPUT_DATA_FOLDER = os.path.join(TEST_STORE_FOLDER, 'PanelInputData')
SHARED_BINARY_FOLDER = os.path.join(os.getcwd()[:2], '\\SHAREDBINARY\\920697932')
# Path Hard coded as per GTA plugin design requirements.
GTA_EMULATOR_CONFIG_FILE = os.path.join(r"E:\gtax-client\tests\Relay_Config", "EmulatorConfig.xml")

# Global dictionary to cache adapter details for future use
GFX_ADAPTER_DICT = {}
BDF_DICT = {}


##
# @brief  Singleton class to collect Diagnostic details
@singleton
class DiagnosticDetails:

    ##
    # @brief init function to initialize CollectData Class
    # @param[in]    save_etl - to save etl
    def __init__(self, save_etl=False):
        self._save_etl = save_etl

    ##
    # @brief getter property to get save_etl
    # @return None
    @property
    def save_etl(self):
        return self._save_etl

    ##
    # @brief setter to set save_etl
    # @param[in]    value - value of save_etl
    # @return None
    @save_etl.setter
    def save_etl(self, value):
        if type(value) is not bool:
            return  # return if set value pass apart from bool
        if value is False and self._save_etl is True:
            return  # returning if existing value true and requested value is False to avoid override in case log-level
        self._save_etl = value


##
# @brief        TestContextPersistence has modules for remembering and getting the context for each test.
# @details      testcontext.xml contains the context of the current test like plugged ports for each adapter.
@singleton
class TestContextPersistence(object):

    ##
    # @brief        Constructor
    # @details      Creates the required node in the test context xml.
    def __init__(self):
        # type: () -> None

        self.test_context_xml_name = r"testcontext.xml"
        self.test_context_xml_path = os.path.join(TestContext.logs_folder(), self.test_context_xml_name)
        root = eTree.Element('DisplayAutomation_2.0')
        command_line = eTree.SubElement(root, 'CommandLine')
        reboot_scenario = eTree.SubElement(root, 'RebootScenario')
        command_line.text = reboot_scenario.text = " "
        eTree.SubElement(root, 'PluggedDisplays')
        test_context_tree = eTree.ElementTree(root)
        test_context_tree.write(self.test_context_xml_path)

    ##
    # @brief        Gets the port and adapter info and writes to a file in the form of xml
    # @details      Note: Do not use this method within tests or feature modules.
    # @param[in]    port_name - connector port
    # @param[in]    port_type - connector port type
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       None
    def _record_plugged_port(self, gfx_index, port_name, port_type):
        # type: (str, str, str) -> None

        test_context_tree = eTree.parse(self.test_context_xml_path)
        test_context_root_node = test_context_tree.getroot()
        plugged_display_node = test_context_root_node.find('PluggedDisplays')
        eTree.SubElement(plugged_display_node, "Port", type=port_type, gfx_index=gfx_index).text = port_name
        test_context_tree.write(self.test_context_xml_path)

    ##
    # @brief        Removes the entry from the test context xml based on the port name and adapter name
    # @details      Note: Do not use this method within tests or feature modules.
    # @param[in]    port_name - connector port
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       None
    def _record_unplugged_port(self, gfx_index, port_name):
        # type: (str, str) -> None

        test_context_tree = eTree.parse(self.test_context_xml_path)
        root_node = test_context_tree.getroot()
        plugged_display_node = root_node.find('PluggedDisplays')

        '''
            Iterate through all the port node and identify the nod which has to be removed using the port_name and 
            gfx_index
        '''

        for port_node in plugged_display_node.findall('Port'):
            if port_node.text == port_name and port_node.get('gfx_index') == gfx_index:
                plugged_display_node.remove(port_node)
                break

        test_context_tree.write(self.test_context_xml_path)

    ##
    # @brief        Gets the plugged ports of a particular adapter by reading the test context xml.
    # @details      Note: Do not use this method within tests or feature modules.
    # @param[in]    gfx_index - Graphics Adapter Index
    # @return       port_info_dict - contains port information about each adapter.
    #               Eg: {  "gfx_0": { "dp_b": "NATIVE"}} or  {"gfx_1": { "dp_b": "NATIVE"}}
    def _get_plugged_ports(self, gfx_index):
        # type: (str) -> {}

        port_info_dict = dict.fromkeys([gfx_index], {})

        test_context_tree = eTree.parse(self.test_context_xml_path)
        root_node = test_context_tree.getroot()
        plugged_display_node = root_node.find('PluggedDisplays')

        '''
            Iterate through the plugged ports and filter out the ports plugged that belongs to the specified adapter
            and create dict with key as adapter name and values as dict containing port_name and port_type.
        '''
        for port_node in plugged_display_node.findall('Port'):
            if port_node.get('gfx_index') == gfx_index:
                port_type = port_node.get('type')
                if gfx_index in port_info_dict:
                    port_info_dict[gfx_index].update({port_node.text: port_type})
                else:
                    port_info_dict[gfx_index] = {port_node.text: port_type}

        return port_info_dict


##
# @brief        Exposes API for getting different folders and exe file paths used in DisplayAutomation2.0
class TestContext:

    ##
    # @brief        API to get cached graphics adapter details
    # @return       GFX_ADAPTER_DICT - Adapter details dictionary
    @staticmethod
    def get_gfx_adapter_details():
        global GFX_ADAPTER_DICT
        global BDF_DICT
        from Libs.Core.display_config.display_config import DisplayConfiguration

        # return gfx adapter dict if already filled
        if len(GFX_ADAPTER_DICT):
            # If False return existing dictionary, else update adapter info for each gfx_index
            force_enumeration = False
            for gfx_index, adapter_info in GFX_ADAPTER_DICT.items():
                if adapter_info.adapterLUID.LowPart == 0 and adapter_info.adapterLUID.HighPart == 0:
                    force_enumeration = True
                    break
            if force_enumeration is False:
                return GFX_ADAPTER_DICT

        display_config_ = DisplayConfiguration()
        gfx_adapter_details = display_config_.get_all_gfx_adapter_details()

        # Optimize this fetch since we will get bdf info during get all gfx adapter details
        # Alternate approach - Add new field within GfxAdapterInfo class and fill this data
        status, bdf_data, adapter_count = display_config_.get_bdf_info()
        if status is True:
            for adapter_index in range(adapter_count):
                gfx_pci_str = str(bdf_data[adapter_index].busDeviceID)
                BDF_DICT[gfx_pci_str] = str(bdf_data[adapter_index])

        # Fill all gfx adapter details
        for adapter_index in range(gfx_adapter_details.numDisplayAdapter):
            gfx_str = str(gfx_adapter_details.adapterInfo[adapter_index].gfxIndex)
            GFX_ADAPTER_DICT[gfx_str] = gfx_adapter_details.adapterInfo[adapter_index]
        return GFX_ADAPTER_DICT

    ##
    # @brief        API to update graphics adapter status for a given gfx_index
    # @details      Note: Do not use this method within tests or feature modules.
    # @param[in]    gfx_index - Graphics Adapter Index
    # @param[in]    adapter_status - Graphics Adapter status
    # @return       None
    @staticmethod
    def _update_gfx_active_status(gfx_index, adapter_status):
        global GFX_ADAPTER_DICT
        from Libs.Core.display_config.display_config import DisplayConfiguration
        adapter_info = TestContext.get_gfx_adapter_details()[gfx_index]
        # Update Adapter active status and LUID based on adapter_status
        if adapter_status == 'disable':
            adapter_info.isActive = False
        elif adapter_status == 'enable':
            adapter_info.isActive = True
        adapter_info.adapterLUID = DisplayConfiguration().get_adapter_luid(adapter_info)
        GFX_ADAPTER_DICT[gfx_index] = adapter_info

    ##
    # @brief        API for getting the absolute path of the Root folder of automation package.
    # @return       str - root folder of the automation package.
    @staticmethod
    def root_folder():
        # type: () -> str

        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    ##
    # @brief        Will get purged soon- For any new development use test_context.SHARED_BINARY_FOLDER variable
    # @return       str - absolute path of the TestStore folder.
    @staticmethod
    def test_store():
        # type: () -> str

        return os.getcwd()[:2] + "\\SHAREDBINARY\\920697932"

    ##
    # @brief        API for getting the absolute path of the bin folder
    # @return       str - absolute path of bin folder.
    @staticmethod
    def bin_store():
        # type: () -> str

        return os.path.join(ROOT_FOLDER, "bin")

    ##
    # @brief        API for getting the absolute path of PanelInputData folder, where EDID/DPCD are stored.
    # @return       str - absolute path of PanelInputData folder.
    @staticmethod
    def panel_input_data():
        # type: () -> str

        return os.path.join(ROOT_FOLDER, "TestStore", "PanelInputData")

    ##
    # @brief        API for getting the absolute path of config.ini file.
    # @return       str - absolute path of config.ini file.
    @staticmethod
    def config_ini_file():
        # type: () -> str

        return os.path.join(TestContext.root_folder(), "Libs\\Core\\test_env", "config.ini")

    ##
    # @brief        API for getting the absolute path of the Logs folder path.
    # @return       str - absolute path of Log folder.
    @staticmethod
    def logs_folder():
        # type: () -> str

        # Create log folder, if it doesn't exists.
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        return LOG_FOLDER

    ##
    # @brief        Helper API to get the devcon file path
    # @return       str - devcon file path
    @staticmethod
    def devcon_path():
        # type: () -> str
        SETUP_PATH = os.path.join(TEST_STORE_FOLDER, "Setup")
        exe_path = os.path.join(SETUP_PATH, "devcon_x64.exe")
        return exe_path


if __name__ == '__main__':
    test_context_persistence = TestContextPersistence()
    test_context_persistence._record_plugged_port('gfx_0', 'dp_b', 'NATIVE')
    test_context_persistence._record_plugged_port('gfx_1', 'hdmi_b', 'NATIVE')
    test_context_persistence._record_plugged_port('gfx_0', 'dp_c', 'NATIVE')

    print("GFX_0 plugged ports: %s" % test_context_persistence._get_plugged_ports('gfx_0'))
    print("GFX_1 plugged ports: %s" % test_context_persistence._get_plugged_ports('gfx_1'))

    plugged_ports_dict = test_context_persistence._get_plugged_ports('gfx_0')
    plugged_ports = plugged_ports_dict['gfx_0'].keys()
    print("Plugged ports: %s" % plugged_ports)

    test_context_persistence._record_unplugged_port('gfx_0', 'dp_b')
    print("GFX_1 plugged ports: %s" % test_context_persistence._get_plugged_ports('gfx_1'))
