########################################################################################################################
# @file         vbt_simulation_ult.py
# @brief        ULT for vbt.py module
#
# @author       Rohit Kumar
########################################################################################################################

import logging
import os
import sys
import unittest
from typing import Union, List

from Libs.Core import display_essential
from Libs.Core import registry_access
from Libs.Core.test_env import test_context
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt import vbt
from Libs.Core.vbt import vbt_context

##
# Platform details for all connected adapters
PLATFORM_INFO = {
    gfx_index: {
        'gfx_index': gfx_index,
        'name': adapter_info.get_platform_info().PlatformName,
    }
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}


class VbtSimulationUlt(unittest.TestCase):
    gfx_index_list: List[str] = []

    # Data for manipulating DWORD registry
    dword_reg_name1 = "_DefaultVBT_Size"
    dword_reg_name2 = "_ActualVBT_Size"

    # Data for manipulating BINARY registry
    bin_reg_name1 = "_DefaultVBT"
    bin_reg_name2 = "_ActualVBT"

    ##
    # @brief    Setup class method
    # @return   None
    @classmethod
    def setUpClass(cls) -> None:
        cls.gfx_index_list = [gfx_index.replace("-", "").lower()
                              for gfx_index in sys.argv[1:]
                              if gfx_index.replace("-", "").lower().startswith("gfx_")]

    ##
    # @brief        Private method used for logging test sections
    # @param[in]    name: string, Log message
    # @return       None
    def __update_test_section(self, name: str) -> None:
        logging.info(f"{'*' * 100}")
        logging.info(f"{name:^100}")
        logging.info(f"{'*' * 100}")

    ##
    # @brief        Registry DWORD validation method
    # @param[in]    args: object, object of type either LegacyRegArgs or StateSeparationRegArgs
    # @param[in]    gfx_index: Graphics adapter index
    # @param[in]    sub_key: string, Addition key path
    # @return       None
    def __validate_dword(self, args: Union[registry_access.LegacyRegArgs, registry_access.StateSeparationRegArgs],
                         gfx_index: str, sub_key=None) -> bool:
        dword_fail_flag = False

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        # Read Registry 1 - DWORD
        logging.info("Validating Registry Read - (DWORD)")
        read_val1, reg_type1 = registry_access.read(args=args, reg_name=adapter_info.busDeviceID + self.dword_reg_name1)
        if reg_type1 == registry_access.RegDataType.DWORD.value:
            logging.info(f"\tRead registry Value : {read_val1}, Type : {registry_access.RegDataType(reg_type1).name}")
        else:
            logging.error(f"\tFailed to read registry value 1 with value: {read_val1}, {reg_type1}")
            dword_fail_flag |= True

        # Read Registry 2 - DWORD
        read_val2, reg_type2 = registry_access.read(args=args, reg_name=adapter_info.busDeviceID + self.dword_reg_name2)
        if reg_type2 == registry_access.RegDataType.DWORD.value:
            logging.info(f"\tRead registry Value : {read_val2}, Type : {registry_access.RegDataType(reg_type2).name}")
        else:
            logging.error(f"\tFailed to read registry value 2 with value: {read_val2}, {reg_type2}")
            dword_fail_flag |= True

        return dword_fail_flag

    ##
    # @brief        Registry BINARY validation method
    # @param[in]    args: object, object of type either LegacyRegArgs or StateSeparationRegArgs
    # @param[in]    gfx_index: Graphics adapter index
    # @param[in]    sub_key: string, Addition key path
    # @return       None
    def __validate_binary(self, args: Union[registry_access.LegacyRegArgs, registry_access.StateSeparationRegArgs],
                          gfx_index: str, sub_key=None) -> bool:
        binary_fail_flag = False

        adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
        # Read Registry 1 - BINARY
        logging.info("Validating Registry Read 1 - (BINARY)")
        read_val1, read_type1 = registry_access.read(args=args, reg_name=adapter_info.busDeviceID + self.bin_reg_name1)
        ls_read_val1 = list(read_val1)
        # Safety check to validate if the data obtained is of BINARY type and access them.
        # Note: This might be need in cases where certain registry data can be of any supported registry type
        if read_type1 == registry_access.RegDataType.BINARY.value:
            logging.info(f"\tRead Type : {registry_access.RegDataType(read_type1).name}, len = {len(ls_read_val1)},"
                         f" registry Value : {ls_read_val1}")
        else:
            logging.error(f"\tRead registry returned with non-binary value: {read_val1}, {read_type1}")
            binary_fail_flag |= True

        # Read Registry 1 - BINARY
        logging.info("Validating Registry Read 2 - (BINARY)")
        read_val2, read_type2 = registry_access.read(args=args, reg_name=adapter_info.busDeviceID + self.bin_reg_name2)
        ls_read_val2 = list(read_val2)
        # Safety check to validate if the data obtained is of BINARY type and access them.
        # Note: This might be need in cases where certain registry data can be of any supported registry type
        if read_type2 == registry_access.RegDataType.BINARY.value:
            logging.info(f"\tRead Type : {registry_access.RegDataType(read_type2).name}, len = {len(ls_read_val2)},"
                         f" registry Value : {ls_read_val2}")
        else:
            logging.error(f"\tRead registry returned with non-binary value: {read_val2}, {read_type2}")
            binary_fail_flag |= True
        ls = []
        for i in range(len(ls_read_val1)):
            if ls_read_val1[i] != ls_read_val2[i]:
                ls.append((i, ls_read_val1[i], ls_read_val2[i]))

        logging.info(f"Failed to match following items - (index, Default VBT, Actual VBT):\n {ls}");
        return binary_fail_flag, ls

    def test_01_init(self):
        ##
        # Make sure init is throwing exception with invalid arguments
        self.assertRaises(Exception, vbt.Vbt, None)
        self.assertRaises(Exception, vbt.Vbt, '')
        self.assertRaises(Exception, vbt.Vbt, 0)
        self.assertRaises(Exception, vbt.Vbt, [])
        self.assertRaises(Exception, vbt.Vbt, ['gfx_0'])

        ##
        # Make sure VBT read is successful, VBT version and size are coming properly
        for platform in PLATFORM_INFO.values():
            logging.info("Reading VBT for {0}".format(platform['name']))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            if gfx_vbt.size is None or gfx_vbt.size <= 0:
                self.fail("Failed to read VBT size")
            logging.info("\tSize: {0}".format(gfx_vbt.size))
            if gfx_vbt.version is None or gfx_vbt.version <= 0:
                self.fail("Failed to read VBT version")
            logging.info("\tVersion: {0}".format(gfx_vbt.version))

            for block_index in gfx_vbt.blocks_to_parse:
                vbt_block = eval("gfx_vbt.block_{0}".format(block_index))
                if vbt_block is None:
                    logging.warning("\tVBT block {0} is not present in VBT".format(block_index))

            logging.info("\tParsed all VBT blocks successfully")

    ##
    # @brief        Test to check VBT parsing for all the blocks
    def test_02_parsing(self):
        for platform in PLATFORM_INFO.values():
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            for block_index in gfx_vbt.blocks_to_parse:
                vbt_block = eval("gfx_vbt.block_{0}".format(block_index))
                if vbt_block is None:
                    continue

                block_str = 'Block{0}Vbt'.format(block_index)
                block_instances = [_ for _ in dir(vbt_context) if block_str in _ and 'Fields' not in _]
                if len(block_instances) == 0:
                    self.fail("VBT Block {0} definition not found".format(block_index))

                fields = None
                if (block_str + '{0}'.format(gfx_vbt.version)) in block_instances:
                    fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, gfx_vbt.version))
                else:
                    current_vbt_version = 0
                    for block_vbt_version in block_instances:
                        vbt_version = int(block_vbt_version.split('Vbt')[1])
                        if current_vbt_version < vbt_version < gfx_vbt.version:
                            fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, vbt_version))
                            current_vbt_version = vbt_version

                logging.info("VBT block {0}".format(block_index))
                for field in fields:
                    logging.info("\t{0:30}:{1}".format(field[0], eval("vbt_block.{0}".format(field[0]))))
                    if block_index == 2 and field[0] == 'DisplayDeviceDataStructureEntry':
                        for index in range(1, 5):
                            logging.info(
                                f"DeviceClass[{index}] = {gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass}")

    ##
    # @brief        DISS registry path test
    # @return       None
    def test_03_reg_data_before_changes(self) -> None:
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test Start : State Separation Registry Access")
        if len(self.gfx_index_list) == 0:
            self.fail("No gfx_index passed for current test.")
        for gfx_index in self.gfx_index_list:
            diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=None,
                                                                   feature=registry_access.Feature.VALSIM)

            flag |= self.__validate_dword(diss_reg_args, gfx_index)
            temp_flag, ls = self.__validate_binary(diss_reg_args, gfx_index)
            flag |= temp_flag

            self.__update_test_section(f"Test End : State Separation Registry Access")
        self.assertFalse(flag, "Failed during validating DISS Registry Operation")

    ##
    # @brief        Test to check VBT is getting dumped in a file correctly
    def test_04_dump_before_apply_changes(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Dumping VBT in file for {0}".format(platform['name']))
            vbt_file = os.path.join(test_context.LOG_FOLDER, 'original_vbt_{0}.bin'.format(platform['name'].lower()))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            try:
                gfx_vbt._dump(vbt_file)
            except Exception as e:
                logging.error(e)
                self.fail("Failed to dump VBT in file for {0}".format(platform['name']))
            logging.info("\tPASS: VBT dumped in {0} successfully".format(vbt_file))

    ##
    # @brief        Test to check VBT is getting updated correctly
    def test_05_apply_changes(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Updating VBT for {0}".format(platform['name']))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            old_value = 0
            old_index = 0
            for index in range(1, 5):
                if gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass != 0x0:
                    old_value = gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass
                    logging.info(
                        "\tBefore Update: block_2.DisplayDeviceDataStructureEntry[{0}].DeviceClass = {1}"
                        "".format(index, old_value))
                    gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass = 0
                    old_index = index
                    break

            if old_value == 0 or old_index == 0:
                return

            if gfx_vbt.apply_changes() is False:
                self.fail("Failed to update VBT")
            logging.info("\tPASS: Updated VBT successfully")
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("Failed to restart display driver")
            logging.info("\tPASS: Restarted the display driver successfully")

            gfx_vbt.reload(platform['gfx_index'])
            gfx_vbt_new = vbt.Vbt(platform['gfx_index'])

            logging.info(
                "\tAfter Update: block_2.DisplayDeviceDataStructureEntry[{0}].DeviceClass = {1}"
                "".format(old_index, gfx_vbt_new.block_2.DisplayDeviceDataStructureEntry[old_index].DeviceClass))
            '''gfx_vbt_new.block_2.DisplayDeviceDataStructureEntry[old_index].DeviceClass = old_value
            if gfx_vbt_new.apply_changes() is False:
                self.fail("Failed to update VBT")
            status, reboot_required = display_essential.restart_gfx_driver()
            if status is False:
                self.fail("Failed to restart display driver")
            gfx_vbt_new.reload(platform['gfx_index'])'''

    ##
    # @brief        DISS registry path test
    # @return       None
    def test_06_reg_data_after_changes(self) -> None:
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test Start : State Separation Registry Access")
        if len(self.gfx_index_list) == 0:
            self.fail("No gfx_index passed for current test.")
        for gfx_index in self.gfx_index_list:
            diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=None,
                                                                   feature=registry_access.Feature.VALSIM)

            flag |= self.__validate_dword(diss_reg_args, gfx_index)
            temp_flag, ls = self.__validate_binary(diss_reg_args, gfx_index)
            flag |= temp_flag

            self.__update_test_section(f"Test End : State Separation Registry Access")
        self.assertFalse(flag, "Failed during validating DISS Registry Operation")

    ##
    # @brief        Test to check VBT parsing for all the blocks
    def test_07_parsing(self):
        for platform in PLATFORM_INFO.values():
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            for block_index in gfx_vbt.blocks_to_parse:
                vbt_block = eval("gfx_vbt.block_{0}".format(block_index))
                if vbt_block is None:
                    continue

                block_str = 'Block{0}Vbt'.format(block_index)
                block_instances = [_ for _ in dir(vbt_context) if block_str in _ and 'Fields' not in _]
                if len(block_instances) == 0:
                    self.fail("VBT Block {0} definition not found".format(block_index))

                fields = None
                if (block_str + '{0}'.format(gfx_vbt.version)) in block_instances:
                    fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, gfx_vbt.version))
                else:
                    current_vbt_version = 0
                    for block_vbt_version in block_instances:
                        vbt_version = int(block_vbt_version.split('Vbt')[1])
                        if current_vbt_version < vbt_version < gfx_vbt.version:
                            fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, vbt_version))
                            current_vbt_version = vbt_version

                logging.info("VBT block {0}".format(block_index))
                for field in fields:
                    logging.info("\t{0:30}:{1}".format(field[0], eval("vbt_block.{0}".format(field[0]))))
                    if block_index == 2 and field[0] == 'DisplayDeviceDataStructureEntry':
                        for index in range(1, 5):
                            logging.info(
                                f"DeviceClass[{index}] = {gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass}")

    ##
    # @brief        Test to check VBT is getting dumped in a file correctly
    def test_08_dump(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Dumping VBT in file for {0}".format(platform['name']))
            vbt_file = os.path.join(test_context.LOG_FOLDER, 'custom_vbt_{0}.bin'.format(platform['name'].lower()))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            try:
                gfx_vbt._dump(vbt_file)
            except Exception as e:
                logging.error(e)
                self.fail("Failed to dump VBT in file for {0}".format(platform['name']))
            logging.info("\tPASS: VBT dumped in {0} successfully".format(vbt_file))

    ##
    # @brief        Test to check VBT reset is working properly
    def test_09_reset(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Resetting VBT for {0}".format(platform['name']))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            if gfx_vbt.reset() is False:
                self.fail("Failed to reset VBT")
            if display_essential.restart_display_driver(platform['gfx_index']) is False:
                self.fail("Failed to restart display driver")
            logging.info("\tPASS: VBT reset successful")

    ##
    # @brief        DISS registry path test
    # @return       None
    def test_10_reg_data_after_vbt_reset(self) -> None:
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test Start : State Separation Registry Access")
        if len(self.gfx_index_list) == 0:
            self.fail("No gfx_index passed for current test.")
        for gfx_index in self.gfx_index_list:
            diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=None,
                                                                   feature=registry_access.Feature.VALSIM)

            flag |= self.__validate_dword(diss_reg_args, gfx_index)
            temp_flag, ls = self.__validate_binary(diss_reg_args, gfx_index)
            flag |= temp_flag

            self.__update_test_section(f"Test End : State Separation Registry Access")
        self.assertFalse(flag, "Failed during validating DISS Registry Operation")

    ##
    # @brief        Test to check VBT parsing for all the blocks
    def test_11_parsing(self):
        for platform in PLATFORM_INFO.values():
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            for block_index in gfx_vbt.blocks_to_parse:
                vbt_block = eval("gfx_vbt.block_{0}".format(block_index))
                if vbt_block is None:
                    continue

                block_str = 'Block{0}Vbt'.format(block_index)
                block_instances = [_ for _ in dir(vbt_context) if block_str in _ and 'Fields' not in _]
                if len(block_instances) == 0:
                    self.fail("VBT Block {0} definition not found".format(block_index))

                fields = None
                if (block_str + '{0}'.format(gfx_vbt.version)) in block_instances:
                    fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, gfx_vbt.version))
                else:
                    current_vbt_version = 0
                    for block_vbt_version in block_instances:
                        vbt_version = int(block_vbt_version.split('Vbt')[1])
                        if current_vbt_version < vbt_version < gfx_vbt.version:
                            fields = eval('vbt_context.Block{0}Fields{1}._fields_'.format(block_index, vbt_version))
                            current_vbt_version = vbt_version

                logging.info("VBT block {0}".format(block_index))
                for field in fields:
                    logging.info("\t{0:30}:{1}".format(field[0], eval("vbt_block.{0}".format(field[0]))))
                    if block_index == 2 and field[0] == 'DisplayDeviceDataStructureEntry':
                        for index in range(1, 5):
                            logging.info(
                                f"DeviceClass[{index}] = {gfx_vbt.block_2.DisplayDeviceDataStructureEntry[index].DeviceClass}")

    ##
    # @brief        Test to check VBT is getting dumped in a file correctly
    def test_12_dump(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Dumping VBT in file for {0}".format(platform['name']))
            vbt_file = os.path.join(test_context.LOG_FOLDER, 'reset_vbt_{0}.bin'.format(platform['name'].lower()))
            gfx_vbt = vbt.Vbt(platform['gfx_index'])
            try:
                gfx_vbt._dump(vbt_file)
            except Exception as e:
                logging.error(e)
                self.fail("Failed to dump VBT in file for {0}".format(platform['name']))
            logging.info("\tPASS: VBT dumped in {0} successfully".format(vbt_file))

    ##
    # @brief        Test to check get_supported_ports API
    def test_13_supported_ports(self):
        for platform in PLATFORM_INFO.values():
            logging.info("Getting supported ports for {0}".format(platform['name']))
            supported_ports = vbt.Vbt(platform['gfx_index'])._get_supported_ports()
            if bool(supported_ports) is False:
                self.fail("Failed to get supported ports")
            logging.info("\tSupported ports: {0}".format(supported_ports))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
