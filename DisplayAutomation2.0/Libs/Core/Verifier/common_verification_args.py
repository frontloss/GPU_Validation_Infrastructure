########################################################################################################################
# @file         common_verification_args.py
# @brief        Contains Diana error-code class , Verifier_config class, Verifier_config_Flags
# @author       Nainesh Doriwala
########################################################################################################################
import ctypes
import os
from enum import Enum

DIANA_ERROR_JSON_FILE = os.path.join(os.getcwd(), "ErrorTagReport.json")
GEN9_10_PLATFORM = ["GLK", "KBL", "CNL", "CFL", "SKL", "APL", "HSW"]


##
# @brief        ErrorCode Enum
# @details      DiAna return error code
class ErrorCode(Enum):
    SUCCESSFUL = 0x00000000
    UNSUCCESSFUL = 0x00000001
    DPCD_VIOLATION = 0x08000000
    ASSERT = 0x10000000
    BSPEC_VIOLATION = 0x20000000
    TDR = 0x40000000
    UNDERRUN = 0x80000000


##
# @brief        Verify Enum
# @details      SKIP            - Skip Verification in current test
#               LOG_CRITICAL    - Logs failure and Fails the test
#               SKIP_FAILURE    - Logs failure and does not fail the test
class Verify(Enum):
    SKIP = 0
    LOG_CRITICAL = 1
    SKIP_FAILURE = 2


##
# @brief        VerifierBits Structure
class VerifierBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("underrun", ctypes.c_uint8, 1),  # bit0
        ("tdr", ctypes.c_uint8, 1),  # bit1
        ("bspec_violation", ctypes.c_uint8, 1),  # bit2
        ("audio_playback_verification", ctypes.c_uint8, 1),  # bit3
        ("dpcd_violation", ctypes.c_uint8, 1),  # bit4
        ("sensor_verification", ctypes.c_uint8, 1),  # bit5
        ("reserved", ctypes.c_uint8, 1),  # bit 6
        ("is_diana_analysis", ctypes.c_uint8, 1)  # bit7
    ]


##
# @brief        VerifierConfigFlags Union
class VerifierConfigFlags(ctypes.Union):
    _anonymous_ = ("bit",)
    _fields_ = [
        ("bit", VerifierBits),
        ("asbyte", ctypes.c_uint8)
    ]


##
# @brief        class use to store verifier context , which can be called by test to disable particular verification.
# @details      Setting underrun to False will disable under-run verification.
class VerifierCfg(object):
    _timeout = [20, 60, 250, 600]
    platform = None
    diana_status_code = False
    max_timeout = 20  # timeout for Diana analysis
    tdr = Verify.LOG_CRITICAL  # tdr verification
    underrun = Verify.LOG_CRITICAL  # under-run verification
    bspec_violation = Verify.LOG_CRITICAL  # Bspec violation verification
    dpcd_violation = Verify.LOG_CRITICAL  # DPCD violation verification
    audio_playback_verification = False
    assert_verification = Verify.LOG_CRITICAL
    is_diana_verification = True
    diana_return_error_code = 0x00  # Diana return code in case of under-run, tdr, diana exit unsuccessful.
    sensor_verification = Verify.SKIP

    ##
    # @brief        Returns timeout based on ETL File Size in GB
    # @details      Note: Do not use this method within tests/feature modules.
    # @param[in]    file_size - size of the ETL file
    # @return       (index, val) - (index of timeout value, max timeout)
    @staticmethod
    def _get_max_timeout(file_size: float):
        index, val = None, 0
        if file_size < 1:
            index = 0
        elif file_size < 5:
            index = 1
        elif file_size < 10:
            index = 2
        elif file_size < 25:
            index = 3
        val = VerifierCfg._timeout[index] if index is not None else 0  # Set timeout to 0 for Registry based analysis
        return index, val
