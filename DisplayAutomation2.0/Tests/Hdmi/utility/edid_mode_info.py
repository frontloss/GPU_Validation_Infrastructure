########################################################################################################################################################
# @file         edid_mode_info.py
# @brief        Provides HdmiEDIDInfo and TestModeInfo classes , used to store the basic hdmi edid information
#               and modes details
# @author       Girish Y D
#########################################################################################################################################################


SCANLINE_DICT = {'SCANLINE_ORDERING_UNSPECIFIED': 0, 'PROGRESSIVE': 1, 'INTERLACED': 2}
RSCANLINE_DICT = {0: 'SCANLINE_ORDERING_UNSPECIFIED', 1: 'PROGRESSIVE', 2: 'INTERLACED'}

SCALING_DICT = {'SCALING_UNSPECIFIED': 0, 'CI': 1, 'FS': 2, 'MAR': 4, 'CAR': 8, 'MDS': 64}
RSCALING_DICT = {0: 'SCALING_UNSPECIFIED', 1: 'CI', 2: 'FS', 4: 'MAR', 8: 'CAR', 64: 'MDS'}

BPP_DICT = {'BPP_UNSPECIFIED': 0, '8BPP': 1, '16BPP': 2, '24BPP': 3, '32BPP': 4}
RBPP_DICT = {0: 'BPP_UNSPECIFIED', 1: '8BPP', 2: '16BPP', 3: '24BPP', 4: '32BPP'}

ROTATION_DICT = {'ROTATE_UNSPECIFIED': 0, 'ROTATE_0': 1, 'ROTATE_90': 2, 'ROTATE_180': 3, 'ROTATE_270': 4}
RROTATION_DICT = {0: 'ROTATE_UNSPECIFIED', 1: 'ROTATE_0', 2: 'ROTATE_90', 3: 'ROTATE_180', 4: 'ROTATE_270'}


##
# @brief        Class used to store the basic edid Information
class HdmiEDIDInfo(object):
    display_type = ""
    MaxTMDSClockSupported = 0.0
    SCDCPresent = False
    RRCapable = False
    LTE340MhzScramble = False
    SCSCPresent = False

    ##
    # @brief        Overridden str function
    # @return       str - String details
    def __str__(self):
        return "MaxTMDSClockSupported: %s, SCSCPresent : %s, RRCapable :%s LTE340MhzScramble =  %s" \
               % (self.MaxTMDSClockSupported, self.SCSCPresent, self.RRCapable, self.LTE340MhzScramble)


##
# @brief        Test Mode Info class which is used across the mode set and verification
class TestModeInfo(object):
    platform = ""
    display_port = ""
    modeName = ""
    modeIndex = 0
    edidModeCategory = ""
    vic = 0
    HzRes = 0
    VtRes = 0
    refreshRate = 0
    rotation = 1
    BPP = 4
    scanlineOrdering = 0
    scaling = 1
    isNativeMode = 0
    isYUV420Mode = 0
    sourcePixelFormat = "RGB"
    sourceBPC = 8
    expectedPixelFormat = "RGB"
    expectedBPC = 8
    expectedPixelClockMHz = 0.0
    expectedSymbolClockMHz = 0.0
    Hactive = 0
    Vactive = 0
    Hblank = 0
    Vblank = 0
    Htotal = 0
    Vtotal = 0
    PictureAspectRatio = ""
    expectedPortCRC = 0

    ##
    # @brief        Constructor
    # @param[in]    hzRes - Horizontal Resolution
    # @param[in]    vtRes - Vertical Resolution
    # @param[in]    refreshRate - Refresh Rate Value
    # @param[in]    scanlineordering - Scan Line Ordering
    def __init__(self, hzRes, vtRes, refreshRate, scanlineordering):
        self.HzRes = int(hzRes)
        self.VtRes = int(vtRes)
        self.refreshRate = int(refreshRate)
        self.scanlineOrdering = int(scanlineordering)

    ##
    # @brief        print_test_mode_info
    # @return       str - String detail
    def print_test_mode_info(self):
        return "modeIndex: %s, vic : %s, HzRes :%s VtRes =  %s  refreshRate = %s  rotation = %s BPP = %s  " \
               "scanlineOrdering = %s scaling = %s  sourcePixelFormat =%s sourceBPC =%s " \
               "expectedPixelFormat = %s, expectedBPC =%s, expectedPixelClockMHz = %s  expectedSymbolClockMHz = %s, " \
               "expectedPortCRC = %s" % (self.modeIndex, self.vic, self.HzRes, self.VtRes,
                                         self.refreshRate, RROTATION_DICT[self.rotation],
                                         RBPP_DICT[self.BPP],
                                         RSCANLINE_DICT[self.scanlineOrdering],
                                         RSCALING_DICT[self.scaling], self.sourcePixelFormat, self.sourceBPC,
                                         self.expectedPixelFormat, self.expectedBPC, self.expectedPixelClockMHz,
                                         self.expectedSymbolClockMHz, self.expectedPortCRC)

    ##
    # @brief        Overridden str method
    # @return       str - String detail
    def __str__(self):
        return "ModeName: %s modeIndex: %s, vic : %s, HzRes :%s VtRes =  %s  refreshRate = %s  rotation = %s BPP = %s  " \
               "scanlineOrdering = %s scaling = %s " % (self.modeName, self.modeIndex, self.vic, self.HzRes, self.VtRes,
                                                        self.refreshRate, RROTATION_DICT[self.rotation],
                                                        RBPP_DICT[self.BPP],
                                                        RSCANLINE_DICT[self.scanlineOrdering],
                                                        RSCALING_DICT[self.scaling])
