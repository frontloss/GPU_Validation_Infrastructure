#################################################################################################
# @file         gen_verify_plane.py
# @brief        This script comprises of Plane Verification Modules specific to each Generation
#               under respective Gen class definition.
#               All the Gen Classes inherit from the Base Class PlaneColorVerifier
#               The AutoGen register interface will be instantiated and initialized based on platform
#               and gfx_index.
#               APIs exposed :
#               1. get_plane_verifier_instance()
#               In addition, APIs from the BaseClass can be overloaded and exposed as required
# @author       Smitha B
#################################################################################################
from Tests.Color.Verification.verify_plane import *


##
# @brief        Exposed API to get the plane verifier instance based on Platform and GfxIndex
# @param[in]    platform, str - Ex: 'ICLLP', 'JSL', 'EHL'
# @param[in]    gfx_index, str - Ex: 'gfx_0', 'gfx_1'
# @return       PlaneColorVerifier object based on Platform and GfxIndex
def get_plane_verifier_instance(platform: str, gfx_index: str) -> PlaneColorVerifier:
    if platform in ['ICLLP', 'JSL', 'EHL']:
        return Gen11PlaneColorVerifier(platform, gfx_index)

    if platform in ['LKF1']:
        return Gen11PlaneColorVerifier(platform, gfx_index)

    if platform in ['TGL', 'DG1', 'RKL', 'ADLS']:
        return Gen12PlaneColorVerifier(platform, gfx_index)

    if platform in ['DG2', 'ADLP']:
        return Gen13PlaneColorVerifier(platform, gfx_index)

    if platform in ['DG3', 'MTL', 'ELG']:
        return Gen14PlaneColorVerifier(platform, gfx_index)

    if platform in ['LNL']:
        return Gen15PlaneColorVerifier(platform, gfx_index)

    if platform in ['PTL', 'CLS']:
        return Gen16PlaneColorVerifier(platform, gfx_index)

##
# @brief        PlaneColorVerifier class for Gen11 derived from PlaneColorVerifier
class Gen11PlaneColorVerifier(PlaneColorVerifier):
    plane_csc_scalefactor = 1.661

    def __init__(self, platform, gfx_index):
        self.regs = DisplayRegs.get_interface(platform, gfx_index)
        self.gfx_index = gfx_index
        self.platform = platform

    def verify_fp16_normalizer_programming(self, pipe, pixel_normalizer_info):
        is_hdr_enabled = feature_basic_verify.hdr_status(self.gfx_index, self.platform, pipe)
        if is_hdr_enabled:
            ref_hdr_normalizing_factor = 0x1CEF
            logging.debug("Blending Mode is Linear")
            if pixel_normalizer_info.NormalizationFactor != ref_hdr_normalizing_factor:
                logging.error("FAIL: FP16 Normalizer value not matching: Expected = {0} Actual = {1}".format(
                    ref_hdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                return False
            else:
                logging.info("PASS: FP16 Normalizer value matching: Expected = {0} Actual = {1}".format(
                    ref_hdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
        else:
            ref_sdr_normalizing_factor = 0x38D1
            if pixel_normalizer_info.NormalizationFactor != ref_sdr_normalizing_factor:
                logging.error(
                    "FAIL: FP16 Normalizer value not matching: Expected = {0} Actual = {1}".format(
                        ref_sdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
                return False
            else:
                logging.info(
                    "PASS: FP16 Normalizer value matching: Expected = {0} Actual = {1}".format(
                        ref_sdr_normalizing_factor, pixel_normalizer_info.NormalizationFactor))
            return True


##
# @brief        PlaneColorVerifier class for Gen12 derived from PlaneColorVerifier
class Gen12PlaneColorVerifier(PlaneColorVerifier):
    # @todo: Attributes wrt CSC, Gamma to be added
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)


##
# @brief        PlaneColorVerifier class for Gen13 derived from PlaneColorVerifier
class Gen13PlaneColorVerifier(PlaneColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)


##
# @brief        PlaneColorVerifier class for Gen14 derived from PlaneColorVerifier
class Gen14PlaneColorVerifier(PlaneColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)


##
# @brief        PlaneColorVerifier class for Gen14 derived from PlaneColorVerifier
class Gen15PlaneColorVerifier(PlaneColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)


##
# @brief        PlaneColorVerifier class for Gen14 derived from PlaneColorVerifier
class Gen16PlaneColorVerifier(PlaneColorVerifier):
    def __init__(self, platform, gfx_index):
        self.gfx_index = gfx_index
        self.platform = platform
        self.regs = DisplayRegs.get_interface(platform, gfx_index)

