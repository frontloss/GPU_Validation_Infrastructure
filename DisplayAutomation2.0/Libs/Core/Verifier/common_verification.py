########################################################################################################################
# @file         common_verification.py
# @brief        Contains initialize , Update_verify_config, Verify and clean up.
# @author       Nainesh Doriwala
########################################################################################################################
import logging
import os
from configparser import ConfigParser

from Libs.Core.Verifier import assert_verification
from Libs.Core.Verifier import bspec_mmio_dpcd_verification
from Libs.Core.Verifier import diana_analysis
from Libs.Core.Verifier import sensor_verification
from Libs.Core.Verifier import tdr_verification
from Libs.Core.Verifier import underrun_verification
from Libs.Core.Verifier.common_verification_args import VerifierCfg, VerifierConfigFlags, GEN9_10_PLATFORM, Verify
from Libs.Core.Verifier.framebuffer_verification import framebuffer_verification
from Libs.Core.test_env import test_context


##
# @brief        API to initialize all required verification module
# @return       None
def initialize():
    # update VerificationCfg skip_under-run and skip_tdr based on config.init file
    update_verifier_cfg()
    # initialize under-run verifier
    underrun_verification.initialize()
    # initialize TDR verifier
    tdr_verification.initialize()
    # initialize assert verification
    assert_verification.initialize()
    # initialize framebuffer verification
    framebuffer_verification.initialize_and_cleanup("initialize")
    sensor_verification.initialize()


##
# @brief    API to update verifier configurations
# @return   None
def update_verifier_cfg():
    _configParser = ConfigParser()
    override_verify_cfg = 0xFF
    add_verify_cfg = 0x0
    platform_bits = 0x00
    flag = VerifierConfigFlags()

    # For multi-adapter update verifier cfg based on base platform(gfx_0).
    adapter_info = test_context.TestContext.get_gfx_adapter_details()['gfx_0']
    VerifierCfg.platform = adapter_info.get_platform_info().PlatformName.upper()

    logging.debug("Platform name = {}".format(VerifierCfg.platform))

    if os.path.exists(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini")):
        _configParser.read(os.path.join(test_context.TEST_TEMP_FOLDER, "config.ini"))
        if _configParser.has_option('VERIFIER_CFG', 'override_verifier_cfg'):
            override_verify_cfg = int(_configParser.get('VERIFIER_CFG', 'override_verifier_cfg'), 16)
        if _configParser.has_option('VERIFIER_CFG', 'add_verifier_cfg'):
            add_verify_cfg = int(_configParser.get('VERIFIER_CFG', 'add_verifier_cfg'), 16)
        if _configParser.has_option('VERIFIER_CFG', VerifierCfg.platform):
            platform_bits = int(_configParser.get('VERIFIER_CFG', VerifierCfg.platform), 16)

    # check and update VerifierCfg based on override_verify_cfg
    if override_verify_cfg != 0xFF:
        platform_bits = override_verify_cfg
        logging.debug("updated override_cfg:{}, platform_cfg:{}".format(override_verify_cfg, platform_bits))
    if add_verify_cfg != 0x0:
        platform_bits |= add_verify_cfg
        logging.info(f"updated platform_cfg:{hex(platform_bits)} with add_verify_cfg:{hex(add_verify_cfg)}")
    flag.asbyte = platform_bits
    if not flag.underrun or VerifierCfg.underrun == Verify.SKIP:
        VerifierCfg.underrun = Verify.SKIP
    if not flag.tdr or VerifierCfg.tdr == Verify.SKIP:
        VerifierCfg.tdr = Verify.SKIP
    if not flag.bspec_violation or VerifierCfg.bspec_violation == Verify.SKIP:
        VerifierCfg.bspec_violation = Verify.SKIP
    if not flag.dpcd_violation or VerifierCfg.dpcd_violation == Verify.SKIP:
        VerifierCfg.dpcd_violation = Verify.SKIP
    if flag.audio_playback_verification or VerifierCfg.audio_playback_verification is True:
        VerifierCfg.audio_playback_verification = True
    if not flag.is_diana_analysis:
        logging.info("updated diana analysis to false")
        VerifierCfg.is_diana_verification = False
    if flag.sensor_verification:
        VerifierCfg.sensor_verification = Verify.SKIP_FAILURE


##
# @brief        Wrapper to perform required verification methods (platform-wise)
# @details      Created to avoid duplicate code.
# @param[in]    result -  Test Result object
# @param[in]    etl_file_name - ETL file name
# @param[in]    is_gen_11plus - pass True to perform all verifications, False to perform only underrun/TDR verifications
#               This parameter is specific to gen9 platforms. Need to check if these are still required
# @return       None
def __invoke_verifiers(result, etl_file_name, is_gen_11plus=True):
    # Verify under-run
    underrun_verification.verify(result)

    # Verify TDR
    tdr_verification.verify(result)

    if is_gen_11plus:
        # Verify Assert
        assert_verification.verify(etl_file_name)

        # Verify Bspec and DPCD Violation
        bspec_mmio_dpcd_verification.verify(result)


##
# @brief        API to verify basic display driver verification.
# @param[in]    result - Test Result object
# @return       None
def verify(result):
    sensor_verification.verify()

    if VerifierCfg.platform in GEN9_10_PLATFORM or VerifierCfg.is_diana_verification is False:
        VerifierCfg.diana_status_code = False
        logging.debug("verification with existing method status:{0},is_diana{1}"
                      .format(VerifierCfg.diana_status_code, VerifierCfg.is_diana_verification))
        __invoke_verifiers(result, None, is_gen_11plus=False)
    else:
        diana_cmd = "-dispdiag"

        for etl_file_name in os.listdir(test_context.LOG_FOLDER):
            if etl_file_name.endswith('.etl'):
                logging.info("DiAna analysis for etl_file:{}".format(etl_file_name))
                logging.info("Identified BDFs = {}".format(test_context.BDF_DICT))

                if bool(test_context.BDF_DICT):
                    # If BDF(s) is/are detected this will parse ETLs with -BDF parameter
                    for _, bdf in test_context.BDF_DICT.items():
                        # Run Diana Analyzer for etl analysis
                        VerifierCfg.diana_status_code = diana_analysis.analyze(etl_file_name, diana_cmd, bdf=bdf)
                        __invoke_verifiers(result, etl_file_name)
                else:
                    # Fallback case when failed to detect display adapter BDF information
                    # Run Diana Analyzer for etl analysis
                    VerifierCfg.diana_status_code = diana_analysis.analyze(etl_file_name, diana_cmd)
                    __invoke_verifiers(result, etl_file_name)


##
# @brief    API to cleanup common verifications
# @return   None
def cleanup():
    underrun_verification.cleanup()
    tdr_verification.cleanup()
    assert_verification.cleanup()
    framebuffer_verification.initialize_and_cleanup("cleanup")
    sensor_verification.cleanup()
