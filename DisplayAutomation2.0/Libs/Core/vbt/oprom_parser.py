###################################################################################################################
# @file         oprom_parser.py
# @brief        Python wrapper exposes API's related to Oprom Parsing
# @author       Chandrakanth, Pabolu
##########################################################################################################################
import array
import logging
import os
import struct
import subprocess

from Libs.Core import registry_access
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from TestStore.OpromSigningTools import PciHeaderPadder

UNSIGNED_OPROM_SIZE = 62 * 1024

# Registry key constant used by OPROM
REG_KEY_ACTUAL_OPROM_HEADER = "_ActualOpromHeader"
REG_KEY_ACTUAL_OPROM_FOOTER = "_ActualOpromFooter"

MEU_PACKAGE_PATH = os.path.join(test_context.TEST_STORE_FOLDER, 'OpromSigningTools')
MEU_TOOL_PATH = os.path.join(MEU_PACKAGE_PATH, 'meu.exe')
CUSTOM_OPROM_PATH = os.path.join(test_context.LOG_FOLDER, 'CustomOprom.bin')
CUSTOM_OPROM_SIG_STRIP_PATH = os.path.join(test_context.LOG_FOLDER, 'CustomOprom_signature_stripped.bin')
RAW_CUSTOM_CONFIG_DATA_PATH = os.path.join(test_context.LOG_FOLDER, 'RawCustomConfigData.bin')
MEU_SIGNED_DATA_PATH = os.path.join(test_context.LOG_FOLDER, 'MeuSignedConfigData.bin')
CUSTOM_OPROM_RESIGNED_PATH = os.path.join(test_context.LOG_FOLDER, 'CustomOprom_Resigned.bin')


##
# @brief        Oprom header and Footer in registry
# @param[in]    gfx_index - Graphics Adapter Index
# @return       bool - True if Oprom header and footer are present in registry, False otherwise
def _is_vbt_in_oprom(gfx_index):
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]

    reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)
    oprom_header_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_OPROM_HEADER
    oprom_footer_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_OPROM_FOOTER

    header_size, header_reg_type = registry_access.read(args=reg_args, reg_name=oprom_header_key)
    if header_reg_type is not None and registry_access.RegDataType(
            header_reg_type) == registry_access.RegDataType.BINARY:
        header_size = len(header_size)
    footer_size, footer_reg_type = registry_access.read(args=reg_args, reg_name=oprom_footer_key)
    if footer_reg_type is not None and registry_access.RegDataType(
            footer_reg_type) == registry_access.RegDataType.BINARY:
        footer_size = len(footer_size)

    if header_size is None and footer_size is None:  # oprom header and footer not present in registry
        logging.info("Oprom header and footer not present in registry")
        return False
    else:
        return True


##
# @brief        Merging vbt with oprom header and footer
# @param[in]    adapter_info - Graphics Adapter Info
# @param[in]    custom_vbt - Custom VBT block data
# @return       (status,final_data) - (oprom read status, list of VBT Blocks)
def __merge_vbt_with_oprom_header_and_footer(adapter_info, custom_vbt):
    status = False
    final_data = []  # array.array('B', [])

    reg_args = registry_access.StateSeparationRegArgs(gfx_index=None, feature=registry_access.Feature.VALSIM)
    oprom_header_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_OPROM_HEADER
    oprom_footer_key = str(adapter_info.busDeviceID) + REG_KEY_ACTUAL_OPROM_FOOTER

    header_size, header_reg_type = registry_access.read(args=reg_args, reg_name=oprom_header_key)
    if header_reg_type is not None and registry_access.RegDataType(
            header_reg_type) == registry_access.RegDataType.BINARY:
        header_size = len(header_size)
    footer_size, footer_reg_type = registry_access.read(args=reg_args, reg_name=oprom_footer_key)
    if footer_reg_type is not None and registry_access.RegDataType(
            footer_reg_type) == registry_access.RegDataType.BINARY:
        footer_size = len(footer_size)
    logging.info(f"Oprom header size:{header_size}, footer_size : {footer_size}")

    if not (header_size is None or header_size == 0):
        header_data, header_reg_type = registry_access.read(args=reg_args, reg_name=oprom_header_key)
        if header_reg_type is not None and registry_access.RegDataType(
                header_reg_type) == registry_access.RegDataType.BINARY:
            header_data = list(header_data)
        else:
            logging.error(f"Failed to convert Oprom Header data to list!!! {type(header_data)}")
        if header_data is None:
            gdhm.report_bug(
                "[OpromParserLib] Failed to read Oprom Header",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            logging.error("Failed to read Oprom Header")
            status = False
        else:
            # header_data = array.array('B', header_data)
            final_data = header_data
            status = True

    final_data += custom_vbt
    # final_data += array.array('B', custom_vbt)

    if not (footer_size is None or footer_size == 0):
        footer_data, footer_reg_type = registry_access.read(args=reg_args, reg_name=oprom_footer_key)
        if footer_reg_type is not None and registry_access.RegDataType(
                footer_reg_type) == registry_access.RegDataType.BINARY:
            footer_data = list(footer_data)
        if footer_data is None:
            gdhm.report_bug(
                "[OpromParserLib] Failed to read Oprom Footer",
                gdhm.ProblemClassification.FUNCTIONALITY,
                gdhm.Component.Test.DISPLAY_INTERFACES
            )
            logging.error("Failed to read Oprom Footer")
            status = False
        else:
            # footer_data = array.array('B', footer_data)
            final_data += footer_data
            status = status and True

    return status, final_data


##
# @brief        Perform meu signing
# @param[in]    platform_name - Platform Name
# @param[in]    input_file_path - Input file path for MEU signing
# @param[in]    output_file_path - Output file path or MEU signing
# @return       bool - True if signing successful, False otherwise
def __perform_meu_signing(platform_name, input_file_path, output_file_path):
    version = "19.0.0.0" if platform_name.upper() == "DG1" else "20.0.0.0"
    status_code = subprocess.call([MEU_TOOL_PATH, "-f", '.\ConfigData.xml', "-mndebug", "true",
                                   "-o", output_file_path, "-u1", input_file_path, "-mnver", version],
                                  cwd=MEU_PACKAGE_PATH)
    if status_code != 0:
        gdhm.report_bug(
            "[OpromParserLib] MEU signing failed!",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Test.DISPLAY_INTERFACES
        )
        logging.error("MEU signing failed!")
        return False
    return True


##
# @brief        Get the merged oprom data
# @param[in]    gfx_index - Graphics Adapter Index
# @param[in]    custom_vbt - Custom vbt Information
# @return       (status,final_data) - (oprom read status, list of VBT Blocks)
def _get_merged_oprom_data(gfx_index, custom_vbt):
    adapter_info = test_context.TestContext.get_gfx_adapter_details()[gfx_index]
    platform_name = adapter_info.get_platform_info().PlatformName
    status, final_data = __merge_vbt_with_oprom_header_and_footer(adapter_info, custom_vbt)

    if status is True:
        if len(final_data) <= UNSIGNED_OPROM_SIZE:
            logging.info("Current Oprom is Unsigned.")
        else:
            logging.info(f"Current Oprom is signed with total size:{len(final_data)}. Resigning it.")

            s = struct.pack('B' * len(final_data), *final_data)
            with open(CUSTOM_OPROM_PATH, 'wb') as f:  # creating binary file from buffer data
                f.write(s)

            PciHeaderPadder.StripSignatureBlob(CUSTOM_OPROM_PATH, CUSTOM_OPROM_SIG_STRIP_PATH)
            PciHeaderPadder.StripPaddingFromConfigData(CUSTOM_OPROM_SIG_STRIP_PATH, RAW_CUSTOM_CONFIG_DATA_PATH)
            __perform_meu_signing(platform_name, RAW_CUSTOM_CONFIG_DATA_PATH, MEU_SIGNED_DATA_PATH)
            PciHeaderPadder.ConstructSingleBinary(MEU_SIGNED_DATA_PATH, CUSTOM_OPROM_RESIGNED_PATH, 65536,
                                                  PciHeaderPadder.gSizeOfSignatureBlob, PciHeaderPadder.FileType)

            if os.path.exists(CUSTOM_OPROM_RESIGNED_PATH):
                with open(CUSTOM_OPROM_RESIGNED_PATH, "rb") as f:
                    final_data = f.read()
                final_data = array.array('B', final_data)
                if len(final_data) == 0:
                    gdhm.report_bug(
                        f"[OpromParserLib] Failed to read Signed Oprom from file {CUSTOM_OPROM_RESIGNED_PATH}",
                        gdhm.ProblemClassification.FUNCTIONALITY,
                        gdhm.Component.Test.DISPLAY_INTERFACES
                    )
                    raise Exception(f"Failed to read Signed Oprom from file {CUSTOM_OPROM_RESIGNED_PATH}")
                status = True

    return status, final_data
