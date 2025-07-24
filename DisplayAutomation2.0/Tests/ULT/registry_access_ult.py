########################################################################################################################
# @file         registry_access_ult.py
# @brief        This module describes how to utilize exposed registry access APIs.
#               Usage: python registry_access_ult.py
# @author       Kiran Kumar Lakshmanan
########################################################################################################################

import logging
import sys
import unittest
from typing import Union, List

from Libs.Core import registry_access, system_utility
from Libs.Core.test_env.test_environment import TestEnvironment


##
# @brief    RegistryAccess class
class RegistryAccess(unittest.TestCase):
    gfx_index_list: List[str] = []

    # Data for manipulating DWORD registry
    dword_reg_name = "DwordReg"
    dword_reg_val = 10

    # Data for manipulating STRING registry
    string_reg_name = "StringReg"
    string_reg_val = "This is a test string"

    # Data for manipulating BINARY registry
    bin_reg_name = "BinaryReg"
    bin_reg_val = [0x01, 0x11, 0x10, 0x00, 0xae, 0xea, 0x1f, 0xf1]

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
    # @param[in]    sub_key: string, Addition key path
    # @return       None
    def __validate_dword(self, args: Union[registry_access.LegacyRegArgs, registry_access.StateSeparationRegArgs],
                         sub_key=None) -> bool:
        dword_fail_flag = False
        # Write Registry - DWORD
        logging.info("Validating Registry Write - (DWORD)")
        write_status = registry_access.write(args=args, reg_name=self.dword_reg_name,
                                             reg_type=registry_access.RegDataType.DWORD, reg_value=self.dword_reg_val,
                                             sub_key=sub_key)
        logging.info(f"\tWrite registry status : {write_status}")
        if write_status is False:
            logging.error(f"Failed to write registry value with given {args}")
            dword_fail_flag |= not write_status

        # Read Registry - DWORD
        logging.info("Validating Registry Read - (DWORD)")
        read_val, read_type = registry_access.read(args=args, reg_name=self.dword_reg_name, sub_key=sub_key)
        if read_val == self.dword_reg_val and read_type == registry_access.RegDataType.DWORD.value:
            logging.info(f"\tRead registry Value : {read_val}, Type : {registry_access.RegDataType(read_type).name}")
        else:
            logging.error(f"\tFailed to read registry value with value: {read_val}, {read_type}")
            dword_fail_flag |= True

        # Delete Registry - DWORD
        logging.info("Validating Registry Delete - (DWORD)")
        delete_status = registry_access.delete(args=args, reg_name=self.dword_reg_name, sub_key=sub_key)
        logging.info(f"\tDelete registry status : {delete_status}")
        if delete_status is False:
            logging.error(f"\tFailed to delete registry value with given {args}")
            dword_fail_flag |= not delete_status

        # False Read - DWORD
        reg_val, reg_type = registry_access.read(args=args, reg_name=self.dword_reg_name, sub_key=sub_key)
        if reg_val is not None and reg_type is not None:
            logging.error(f"\tDelete registry validation failed for given {args}")
            dword_fail_flag |= True
        else:
            logging.info(f"\tSuccessfully deleted the registry!!")

        return dword_fail_flag

    ##
    # @brief        Registry BINARY validation method
    # @param[in]    args: object, object of type either LegacyRegArgs or StateSeparationRegArgs
    # @param[in]    sub_key: string, Addition key path
    # @return       None
    def __validate_binary(self, args: Union[registry_access.LegacyRegArgs, registry_access.StateSeparationRegArgs],
                          sub_key=None) -> bool:
        binary_fail_flag = False
        # Write Registry - BINARY
        logging.info("Validating Registry Write - (BINARY)")
        # Convert python lists into class 'bytes' object to successfully write a binary value to registry
        write_status = registry_access.write(args=args, reg_name=self.bin_reg_name,
                                             reg_type=registry_access.RegDataType.BINARY,
                                             reg_value=bytes(self.bin_reg_val), sub_key=sub_key)
        logging.info(f"\tWrite registry status : {write_status}")
        if write_status is False:
            logging.error(f"\tFailed to write registry value with given {args}")
            binary_fail_flag |= not write_status

        # Read Registry - BINARY
        logging.info("Validating Registry Read - (BINARY)")
        read_val, read_type = registry_access.read(args=args, reg_name=self.bin_reg_name, sub_key=sub_key)
        # Safety check to validate if the data obtained is of BINARY type and access them.
        # Note: This might be need in cases where certain registry data can be of any supported registry type
        if read_val == bytes(self.bin_reg_val) and read_type == registry_access.RegDataType.BINARY.value:
            logging.info(f"\tRead registry Value : {read_val}, Type : {registry_access.RegDataType(read_type).name}")
        else:
            logging.error(f"\tRead registry returned with non-binary value: {read_val}, {read_type}")
            binary_fail_flag |= True

        # Delete Registry - BINARY
        logging.info("Validating Registry Delete - (BINARY)")
        delete_status = registry_access.delete(args=args, reg_name=self.bin_reg_name, sub_key=sub_key)
        logging.info(f"\tDelete registry status : {delete_status}")
        if delete_status is False:
            logging.error(f"\tFailed to delete registry value with given {args}")
            binary_fail_flag |= not delete_status

        # False Read - BINARY
        reg_val, reg_type = registry_access.read(args=args, reg_name=self.bin_reg_name, sub_key=sub_key)
        if reg_val is not None and reg_type is not None:
            logging.error(f"\tDelete registry validation failed for given {args}")
            binary_fail_flag |= True
        else:
            logging.info(f"\tSuccessfully deleted the registry!!")

        return binary_fail_flag

    ##
    # @brief        Registry STRING validation method
    # @param[in]    args: object, object of type either LegacyRegArgs or StateSeparationRegArgs
    # @param[in]    sub_key: string, Addition key path
    # @return       None
    def __validate_string(self, args: Union[registry_access.LegacyRegArgs, registry_access.StateSeparationRegArgs],
                          sub_key=None) -> bool:
        string_fail_flag = False
        # Write Registry - STRING
        logging.info("Validating Registry Write - (STRING)")
        write_status = registry_access.write(args=args, reg_name=self.string_reg_name,
                                             reg_type=registry_access.RegDataType.SZ, reg_value=self.string_reg_val,
                                             sub_key=sub_key)
        logging.info(f"\tWrite registry status : {write_status}")
        if write_status is False:
            logging.error(f"\tFailed to write registry value with given {args}")
            string_fail_flag |= not write_status

        # Read Registry - STRING
        logging.info("Validating Registry Read - (STRING)")
        read_val, read_type = registry_access.read(args=args, reg_name=self.string_reg_name, sub_key=sub_key)
        if read_val == self.string_reg_val and read_type == registry_access.RegDataType.SZ.value:
            logging.info(f"\tRead registry Value : {read_val}, Type : {registry_access.RegDataType(read_type).name}")
        else:
            logging.error(f"\tRead registry returned with value: {read_val}, {read_type}")
            string_fail_flag |= True

        # Delete Registry - STRING
        logging.info("Validating Registry Delete - (STRING)")
        delete_status = registry_access.delete(args=args, reg_name=self.string_reg_name, sub_key=sub_key)
        logging.info(f"\tDelete registry status : {delete_status}")
        if delete_status is False:
            logging.error(f"\tFailed to delete registry value with given {args}")
            string_fail_flag |= not delete_status

        # False Read - STRING
        reg_val, reg_type = registry_access.read(args=args, reg_name=self.string_reg_name, sub_key=sub_key)
        if reg_val is not None and reg_type is not None:
            logging.error(f"\tDelete registry validation failed for given {args}")
            string_fail_flag |= True
        else:
            logging.info(f"\tSuccessfully deleted the registry!!")

        return string_fail_flag

    ##
    # @brief        Legacy registry path test
    # @return       None
    def test_01_legacy_regpath(self) -> None:
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test: Legacy Registry Access")
        legacy_reg_args = registry_access.LegacyRegArgs(hkey=registry_access.HKey.LOCAL_MACHINE, reg_path=r"SOFTWARE")
        sub_key = r"SubKey1\SubKey2"

        flag |= self.__validate_string(legacy_reg_args)
        flag |= self.__validate_dword(legacy_reg_args, sub_key)
        flag |= self.__validate_binary(legacy_reg_args)

        self.__update_test_section(f"Test End : Legacy Registry Access")
        self.assertFalse(flag, "Failed during validating Legacy Registry Operation")

    ##
    # @brief        DISS registry path test
    # @return       None
    def test_02_diss_regpath(self) -> None:
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test Start : State Separation Registry Access")
        if len(self.gfx_index_list) == 0:
            self.fail("No gfx_index passed for current test.")
        for gfx_index in self.gfx_index_list:
            diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index)
            sub_key = r"SubKey3\SubKey4"

            flag |= self.__validate_string(diss_reg_args)
            flag |= self.__validate_dword(diss_reg_args, sub_key)
            flag |= self.__validate_binary(diss_reg_args)

            self.__update_test_section(f"Test End : State Separation Registry Access")
        self.assertFalse(flag, "Failed during validating DISS Registry Operation")

    ##
    # @brief        Audio feature registry path test
    # @return       None
    def test_03_audio_regpath(self) -> None:
        # Audio regkey path not available in Pre-Si environment
        if system_utility.SystemUtility().get_execution_environment_type() not in ['POST_SI_ENV']:
            logging.info("Skipping Audio Registry Test since it is unsupported in Pre-Si")
            return
        flag = False  # Update this flag to true if any test fails
        self.__update_test_section("Test Start : Audio State Separation Registry Access")
        if len(self.gfx_index_list) == 0:
            self.fail("No gfx_index passed for current test.")
        for gfx_index in self.gfx_index_list:
            audio_reg_args = registry_access.StateSeparationRegArgs(gfx_index=gfx_index,
                                                                    feature=registry_access.Feature.AUDIO,
                                                                    guid=registry_access.GUID_DEVCLASS_SYSTEM)
            sub_key = r"Settings"

            flag |= self.__validate_string(audio_reg_args)
            flag |= self.__validate_dword(audio_reg_args, sub_key)
            flag |= self.__validate_binary(audio_reg_args)

            self.__update_test_section(f"Test End : Audio State Separation Registry Access")
        self.assertFalse(flag, "Failed during validating Audio Registry Operation")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
