#######################################################################################################################
# @file         vbt_context.py
# @brief        Contains structure definitions for VBT blocks
# @details      vbt_context module contains constants, VBT block structures and Enums used in vbt module for parsing.
#
#               *** How to add new VBT blocks ***
#               Make sure bit map is as per B-spec before adding
#
#               Step 1: Create a new structure class having all the block fields. Structure name must follow below
#               naming convention:
#               Block<block id>Fields<vbt version>
#               Ex: Block2Fields203, Block52Fields224, ...
#
#               Step 2: Create a new union class for block. Union name must follow below naming convention:
#               Block<block id>Vbt<vbt version>
#               Ex: Block2Vbt203, Block52Vbt224
#               Done!
#
#               *** How to add updated bit maps for existing blocks ***
#               If new field is added at the end of the block:
#                   * Search for the block structure class with latest VBT version, add the new field at the end. Done!
#
#               If a new field is added in between:
#                   * Follow the steps given for "How to add new VBT blocks"
#
#               Note:
#               The structure and union classes are not expected to be referenced directly from test scripts. Please
#               do not create object from these classes. Instead use block data members defined in Vbt class in vbt.py
#               module.
# @author       Rohit Kumar, Sri Sumanth Geesala
#######################################################################################################################

from ctypes import *

VBT_SIZE_MAX = 9216  # In bytes
BLOCK_SIZE_MAX = 4096  # In bytes
VBT_CHECKSUM_OFFSET = 26


##
# @brief        VbtData Class
class VbtData(Structure):
    _fields_ = [('Data', c_ubyte * BLOCK_SIZE_MAX)]


##
# @brief        BlockInfo Class
class BlockInfo(Structure):
    _pack_ = 1
    _fields_ = [
        ('Id', c_ubyte),
        ('Size', c_ushort)
    ]


##
# @brief        VswingPreEmpTable Class
class VswingPreEmpTable(Structure):
    _pack_ = 1
    _fields_ = [
        ('VswingPreempTableFields', c_uint32 * 110)
    ]


############################
# VBT Header
############################
##
# @brief        VbtHeaderFields Class
class VbtHeaderFields(Structure):
    _pack_ = 1
    _fields_ = [
        ('ProductString', c_ubyte * 20),
        ('Version', c_ushort),
        ('HeaderSize', c_ushort),
        ('TableSize', c_ushort),
        ('Checksum', c_ubyte),
        ('Reserved', c_ubyte),
        ('BiosDataOffset', c_ulong),
        ('AimDataOffset1', c_ulong),
        ('AimDataOffset2', c_ulong),
        ('AimDataOffset3', c_ulong),
        ('AimDataOffset4', c_ulong),
    ]


##
# @brief        VbtHeader Class
class VbtHeader(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', VbtHeaderFields),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# BDB Header
############################
##
# @brief        BdbHeaderFields class
class BdbHeaderFields(Structure):
    _pack_ = 1
    _fields_ = [
        ('Signature', c_ubyte * 16),
        ('Version', c_ushort),
        ('HeaderSize', c_ushort),
        ('BdbSize', c_ushort)
    ]


##
# @brief        BdbHeader class
class BdbHeader(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', BdbHeaderFields),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 1
############################
##
# @brief        IntegratedDisplaysSupportedFields class
class IntegratedDisplaysSupportedFields(Structure):
    _pack_ = 1
    _fields_ = [
        ('Reserved1', c_ubyte, 3),
        ("DP_SSC_Enable", c_ubyte, 1),
        ("Reserved2", c_ubyte, 1),
        ("DP_SSC_Dongle_Enable", c_ubyte, 1),
        ("Reserved3", c_ubyte, 2)
    ]


##
# @brief        IntegratedDisplaysSupported class
class IntegratedDisplaysSupported(Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", IntegratedDisplaysSupportedFields),
        ("value", c_ubyte)
    ]


##
# @brief        Block1Fields203 class
class Block1Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('BmpBits1', c_ubyte),
        ('BmpBits2', c_ubyte),
        ('BmpBits3', c_ubyte),
        ('LegacyMonitorDetect', c_ubyte),
        ('IntegratedDisplaysSupported', IntegratedDisplaysSupported)
    ]


##
# @brief        Block1Vbt203 class
class Block1Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block1Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 2
############################

##
# VBT Block 2 : DisplayDeviceDataStructure : Device Class
# A two byte number is used to set the display technology for each display device
# Source: https://gfxspecs.intel.com/Predator/Home/Index/20124
#
# 0x68C6 = Integrated DisplayPort only
# 0x1806 = Integrated eDP display
# 0x60D6 = Integrated DisplayPort with HDMI/DVI compatible
# 0x68D6 = Integrated DisplayPort with DVI compatible
# 0x60D2 = Integrated HDMI/DVI display
# 0x68D2 = Integrated DVI display
# 0x1400 = Integrated MIPI display
DEVICE_CLASS = {'LFP_MIPI': 0x1400, 'LFP_DP': 0x1806, 'HDMI': 0x60D2, 'DP': 0x68C6, 'PLUS': 0x60D6}

##
# VBT Block 2 : DisplayDeviceDataStructure : Flags2
# A one byte number is used to enable/disable TC/TBT for targeted display device
# Source: https://gfxspecs.intel.com/Predator/Home/Index/20124
#
# Bit 0: Enable/Disable support for enabling DP display through USB Type C port
# Bit 1: Enable/Disable feature flag indicating whether this port is a Thunderbolt port (applicable from ICL onwards)
FLAGS_2 = {'TC': 0x1, 'TBT': 0x2, 'TC_TBT': 0x3}

##
# VBT Block 2 : DisplayDeviceDataStructure : DVO Port
# This field specifies the port number of the display device represented in the device class.
# Source: https://gfxspecs.intel.com/Predator/Home/Index/20124
DVO_PORT_MAPPING = {
    'DP_A': 0x0A, 'DP_B': 0x07, 'DP_C': 0x08, 'DP_D': 0x09, 'DP_E': 0x0B, 'DP_F': 0x0D, 'DP_G': 0x0F, 'DP_H': 0x11,
    'DP_I': 0x13,
    'HDMI_A': 0x00, 'HDMI_B': 0x01, 'HDMI_C': 0x02, 'HDMI_D': 0x03, 'HDMI_E': 0x0C, 'HDMI_F': 0x0E, 'HDMI_G': 0x10,
    'HDMI_H': 0x12, 'HDMI_I': 0x14,
    'MIPI_A': 0x15, 'MIPI_B': 0x16, 'MIPI_C': 0x17, 'MIPI_D': 0x18
}

DVO_PORT_NAMES = {
    0x0A: 'DP_A', 0x07: 'DP_B', 0x08: 'DP_C', 0x09: 'DP_D', 0x0B: 'DP_E', 0x0D: 'DP_F', 0x0F: 'DP_G', 0x11: 'DP_H',
    0x13: 'DP_I',
    0x00: 'HDMI_A', 0x01: 'HDMI_B', 0x02: 'HDMI_C', 0x03: 'HDMI_D', 0x0C: 'HDMI_E', 0x0E: 'HDMI_F', 0x10: 'HDMI_G',
    0x12: 'HDMI_H', 0x14: 'HDMI_I',
    0x15: 'MIPI_A', 0x16: 'MIPI_B', 0x17: 'MIPI_C', 0x18: 'MIPI_D'
}

##
# VBT Block 2 : DisplayDeviceDataStructure : Aux Channel
# This field specifies the Aux channel to be used for DisplayPort. This field is applicable only for Display Port.
# Source: https://gfxspecs.intel.com/Predator/Home/Index/20124
AUX_CHANNEL_MAPPING = {
    'A': 0x40, 'B': 0x10, 'C': 0x20, 'D': 0x30, 'E': 0x50, 'F': 0x60, 'G': 0x70, 'H': 0x80, 'I': 0x90}

##
# VBT Block 2 : DisplayDeviceDataStructure : MaximumFrlRate
# This field specifies the Maximum FRL Rate supported by HDMI2.1 panel. Applicable for HDMI panel.
# Note : To limit port capability to support <= HDMI2.0 ,  IsMaxFrlRateFieldValid (Bit 4 ) should be set to 1
# and Maximum FrlRate(Bits 0 to 3) should be set to "0".
# To limit HDMI2.1 port FRL rates, IsMaxFrlRateFieldValid (Bit4) should be set to 1 and
# Bits 0 to 3 should specify the MaxFrlRate.
# Source: https://gfxspecs.intel.com/Predator/Home/Index/20124
MAX_FRL_RATE_MAPPING = {
    'FRL_NOT_SUPPORTED': 0, 'FRL_3': 1, 'FRL_6': 2, 'FRL_8': 3, 'FRL_10': 4, 'FRL_12': 5}


##
# @brief        DeviceClassFields class
class DeviceClassFields(Structure):
    _pack_ = 1
    _fields_ = [
        ('AnalogPort', c_uint16, 1),
        ("DigitalOp", c_uint16, 1),
        ("DisplayPort", c_uint16, 1),
        ("VideoSignalling", c_uint16, 1),
        ("TMDSSignalling", c_uint16, 1),
        ("LVDSSignalling", c_uint16, 1),
        ("HighSpeedLink", c_uint16, 1),
        ("ContentProtection", c_uint16, 1),
        ("DualChannel", c_uint16, 1),
        ("CompositeOp", c_uint16, 1),
        ("MipiOp", c_uint16, 1),
        ("NotHDMICapable", c_uint16, 1),
        ("InternalConnection", c_uint16, 1),
        ("HPDSignalling", c_uint16, 1),
        ("PowerMgmt", c_uint16, 1),
        ("ClassExtension", c_uint16, 1)
    ]


##
# @brief        DeviceClass class
class DeviceClass(Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", DeviceClassFields),
        ("value", c_uint16)
    ]


############################
# VBT Block 2 (General Bytes Definition)
############################
##
# @brief        DisplayDeviceDataStructure203 Initialisation
class DisplayDeviceDataStructure203(Structure):
    _pack_ = 1
    _fields_ = [
        ('DeviceHandle', c_ushort),
        ('DeviceClass', c_ushort),
        ('I2CSpeed', c_ubyte),
        ('DPOnboardRedriver', c_ubyte),
        ('DPOndockRedriver', c_ubyte),
        ('HDMILevelShifter', c_ubyte),
        ('DTDBufPtr', c_ushort),
        ('EdidlessEFPFeatureEnable', c_ubyte, 1),
        ('CompressionEnable', c_ubyte, 1),
        ('CompressionMethodSelect', c_ubyte, 1),
        ('DualPipeGangedEdpSupport', c_ubyte, 1),
        ('ReservedF4', c_ubyte, 4),
        ('CompressionStructureIndex', c_ubyte, 4),
        ('ReservedCSI4', c_ubyte, 4),
        ('MaximumFrlRate', c_ubyte, 4),
        ('IsMaxFrlRateFieldValid', c_ubyte, 1),
        ('ReservedFRL3', c_ubyte, 3),
        ('Reserved1', c_ubyte),
        ('AddInOffset', c_ushort),
        ('DVOPort', c_ubyte),
        ('I2CBus', c_ubyte),
        ('SlaveAddress', c_ubyte),
        ('DDCBus', c_ubyte),
        ('EDIDBufferPtr', c_ushort),
        ('DVOConfig', c_ubyte),
        ('Flags1', c_ubyte),
        ('Compatibility', c_ubyte),
        ('AuxChannel', c_ubyte),
        ('DongleDetect', c_ubyte),
        ('Capabilities', c_ubyte),
        ('DVOWiring', c_ubyte),
        ('MIPIBridgeType', c_ubyte),
        ('DeviceClassExtension', c_ushort),
        ('DVOFunction', c_ubyte),
        ('TypeC', c_ubyte, 1),
        ('Tbt', c_ubyte, 1),
        ('ReservedF2', c_ubyte, 6),
        ('2XDPGPIOIndex', c_ubyte),
        ('2XDPGPIOPinNumber', c_ushort),
        ('BoostLevel', c_ubyte)
    ]


##
# @brief        DisplayDeviceDataStructure216 class
class DisplayDeviceDataStructure216(DisplayDeviceDataStructure203):
    _pack_ = 1
    _fields_ = [('DpMaxLinkRate', c_ubyte)]


##
# @brief        DisplayDeviceDataStructure256 class
class DisplayDeviceDataStructure256(DisplayDeviceDataStructure216):
    _pack_ = 1
    _fields_ = [('EFPPanelIndex', c_ubyte)]


##
# @brief        Block2Fields203 class
class Block2Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('CRTDDCGmbusPinPair', c_ubyte),
        ('DPMSBits', c_ubyte),
        ('BootDeviceDefinitions', c_ushort),
        ('DisplayDeviceStructureEntrySize', c_ubyte),
        ('DisplayDeviceDataStructureEntry', DisplayDeviceDataStructure203 * 10)
    ]


##
# @brief        Block2Fields216 class
class Block2Fields216(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('CRTDDCGmbusPinPair', c_ubyte),
        ('DPMSBits', c_ubyte),
        ('BootDeviceDefinitions', c_ushort),
        ('DisplayDeviceStructureEntrySize', c_ubyte),
        ('DisplayDeviceDataStructureEntry', DisplayDeviceDataStructure216 * 10)
    ]


##
# @brief        Block2Fields256 class
class Block2Fields256(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('CRTDDCGmbusPinPair', c_ubyte),
        ('DPMSBits', c_ubyte),
        ('BootDeviceDefinitions', c_ushort),
        ('DisplayDeviceStructureEntrySize', c_ubyte),
        ('DisplayDeviceDataStructureEntry', DisplayDeviceDataStructure256 * 10)
    ]


##
# @brief        Block2Vbt203 class
class Block2Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block2Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block2Vbt216 class
class Block2Vbt216(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block2Fields216),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block2Vbt256 class
class Block2Vbt256(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block2Fields256),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 9 (SRD Feature Block)
############################
##
# @brief        Block9Fields205 class
class Block9Fields205(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('FeatureBit', c_ubyte),
        ('WaitTime', c_ubyte),
        ('PsrClockRecoveryTime', c_ushort),  # TP1 wake up time
        ('Psr1ChannelEqualizationTime', c_ushort),  # PSR1_TP2_TP3_TP4_Wakeup time
        ('Psr2ChannelEqualizationTime', c_ulong),  # PSR2_TP2_TP3_TP4_Wakeup time
    ]


##
# @brief        Block9Vbt205 class
class Block9Vbt205(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block9Fields205),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 12 (Driver Features Data Block)
############################
##
# @brief        Block12Fields203 class
class Block12Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('DriverBits', c_ubyte),
        ('DriverBootMode_XRes', c_ushort),
        ('DriverBootMode_YRes', c_ushort),
        ('DriverBootMode_BPP', c_ubyte),
        ('DriverBootMode_RR', c_ubyte),
        ('LfpAlwaysPrimary', c_uint16, 1),
        ('SelectiveModePruning', c_uint16, 1),
        ('DualFrequencyGraphicsTechnology', c_uint16, 1),
        ('RenderClockFrequency', c_uint16, 1),
        ('Nt40CloneSupport', c_uint16, 1),
        ('DefaultPowerSchemeUi', c_uint16, 1),
        ('SpriteDisplayAssignment', c_uint16, 1),
        ('AspectScalingEnabled', c_uint16, 1),
        ('PreserveAspectRatio', c_uint16, 1),
        ('SdvoDevicePowerDown', c_uint16, 1),
        ('CrtHotPlug', c_uint16, 1),
        ('LvdsActiveConfiguration', c_uint16, 2),
        ('TvHotPlug', c_uint16, 1),
        ('Reserved', c_uint16, 2),
        ('DriverFlags1', c_ubyte),
        ('LegacyCRTMax_X', c_ushort),
        ('LegacyCRTMax_Y', c_ushort),
        ('LegacyCRTMax_RR', c_ubyte),
        ('ExtendedDriverBits2', c_ubyte),
        ('CustomerVBTNo', c_ubyte),
        ('DriverFeatureFlags', c_ushort)
    ]


##
# @brief        Block12Vbt203 class
class Block12Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block12Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# Block27 (eDP VBT Block)
############################
##
# @brief        Pps class
class Pps(Structure):
    _pack_ = 1
    _fields_ = [
        ('T3Delay', c_ushort),
        ('T7Delay', c_ushort),
        ('T9Delay', c_ushort),
        ('T10Delay', c_ushort),
        ('T12Delay', c_ushort)
    ]


##
# @brief        BacklightDelays class
class BacklightDelays(Structure):
    _pack_ = 1
    _fields_ = [
        ('PWMOntoBackLightDelay', c_ushort),
        ('BacklightOfftoPWMOffDelay', c_ushort)
    ]


##
# @brief        ApicalAssertiveDispalyIPTable class
class ApicalAssertiveDisplayIPTable(Structure):
    _pack_ = 1
    _fields_ = [
        ('PanelOUI', c_ulong),
        ('DPCDBase', c_ulong),
        ('DPCDIrdidix', c_ulong),
        ('DPCDOption', c_ulong),
        ('DPCDBacklight', c_ulong),
        ('AmbientLight', c_ulong),
        ('BacklightScale', c_ulong)
    ]


##
# @brief        Block27Field203 class
class Block27Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('PPSEntry', Pps * 16),
        ('PanelColourDepthEntry', c_ulong),
        ('FastLinkParametersEntry', c_ushort * 16),
        ('eDPsDRRSMSADelay', c_ulong),
        ('eDPS3DFeaturebits', c_ushort),
        ('eDPT3optimizations', c_ushort),
        ('VSwingPreEmphasisTableSelection', c_ubyte * 8),
        ('IsFastLinkTrainingEnabledInVbt', c_ushort),
        ('IsDPCD600hWriteRequired', c_ushort),
        ('BacklightDelaysEntry', BacklightDelays * 16),
        ('IsFullLinkTrainingStartingParameterProvided', c_ushort),
        ('eDPFulllinkparametersEntry', c_ubyte * 16),
        ('ApicalAssertiveDisplayIPEnable', c_ushort),
        ('ApicalAssertiveDisplayIPTableEnrty', ApicalAssertiveDisplayIPTable * 16)
    ]


##
# @brief        Block27Fields224 class
class Block27Fields224(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('PPSEntry', Pps * 16),
        ('PanelColourDepthEntry', c_ulong),
        ('FastLinkParametersEntry', c_ushort * 16),
        ('eDPsDRRSMSADelay', c_ulong),
        ('eDPS3DFeatureBits', c_ushort),
        ('eDPT3optimizations', c_ushort),
        ('VSwingPreEmphasisTableSelection', c_ubyte * 8),
        ('IsFastLinkTrainingEnabledInVbt', c_ushort),
        ('IsDPCD600hWriteRequired', c_ushort),
        ('BacklightDelaysEntry', BacklightDelays * 16),
        ('IsFullLinkTrainingStartingParameterProvided', c_ushort),
        ('eDPFullLinkParametersEntry', c_ubyte * 16),
        ('ApicalAssertiveDisplayIPEnable', c_ushort),
        ('ApicalAssertiveDisplayIPTableEntry', ApicalAssertiveDisplayIPTable * 16),
        ('eDPFastLinkTrainingDataRate', c_uint16 * 16)
    ]


##
# @brief        Block27Vbt203 class
class Block27Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block27Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block27Vbt224 class
class Block27Vbt224(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block27Fields224),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block27Fields260 class
class Block27Fields260(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('PPSEntry', Pps * 16),
        ('PanelColourDepthEntry', c_ulong),
        ('FastLinkParametersEntry', c_ushort * 16),
        ('eDPsDRRSMSADelay', c_ulong),
        ('eDPS3DFeatureBits', c_ushort),
        ('eDPT3optimizations', c_ushort),
        ('VSwingPreEmphasisTableSelection', c_ubyte * 8),
        ('IsFastLinkTrainingEnabledInVbt', c_ushort),
        ('IsDPCD600hWriteRequired', c_ushort),
        ('BacklightDelaysEntry', BacklightDelays * 16),
        ('IsFullLinkTrainingStartingParameterProvided', c_ushort),
        ('eDPFullLinkParametersEntry', c_ubyte * 16),
        ('ApicalAssertiveDisplayIPEnable', c_ushort),
        ('ApicalAssertiveDisplayIPTableEntry', ApicalAssertiveDisplayIPTable * 16),
        ('eDPFastLinkTrainingDataRate', c_uint16 * 16),
        ('T6DelaySupport', c_uint16 * 16),
        ('T6DelayLinkIdleTime', c_uint16 * 16)
    ]


##
# @brief        Block27Fields260 class
class Block27Vbt260(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block27Fields260),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 40 (LFP Data Block)
############################
##
# @brief        Block40Fields203 class
class Block40Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('PanelType', c_ubyte),
        ('PanelType2', c_ubyte),
        ('LfpCapabilities', c_ushort),
        ('LvdsPanelChanelBits', c_ulong),
        ('LvdsSscEnableBits', c_ushort),
        ('LvdsSscFrequencyBits', c_ushort),
        ('DisableSscInTwin', c_ushort),
        ('PanelColorDepth', c_ushort),
        ('DpsPanelType0', c_ulong, 2),
        ('DpsPanelType1', c_ulong, 2),
        ('DpsPanelType2', c_ulong, 2),
        ('DpsPanelType3', c_ulong, 2),
        ('DpsPanelType4', c_ulong, 2),
        ('DpsPanelType5', c_ulong, 2),
        ('DpsPanelType6', c_ulong, 2),
        ('DpsPanelType7', c_ulong, 2),
        ('DpsPanelType8', c_ulong, 2),
        ('DpsPanelType9', c_ulong, 2),
        ('DpsPanelType10', c_ulong, 2),
        ('DpsPanelType11', c_ulong, 2),
        ('DpsPanelType12', c_ulong, 2),
        ('DpsPanelType13', c_ulong, 2),
        ('DpsPanelType14', c_ulong, 2),
        ('DpsPanelType15', c_ulong, 2),
        ('BltControlTypeBits', c_ulong),
        ('LcdvccOnDuringS0State', c_ushort)
    ]


##
# @brief        Block40Vbt203 class
class Block40Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block40Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 42 (LFP Data Tables)
############################
##
# @brief        FlatPanelDataStructure class
class FlatPanelDataStructure(Structure):
    _pack_ = 1
    _fields_ = [('XRes', c_ushort),
                ('YRes', c_ushort),
                ('LVDSPortControlReg', c_ulong),
                ('LVDSPortControlRegData', c_ulong),
                ('PanelPowerOnReg', c_ulong),
                ('PanelPowerOnRegData', c_ulong),
                ('PanelPowerOffReg', c_ulong),
                ('PanelPowerOffRegData', c_ulong),
                ('PanelPowerCycleReg', c_ulong),
                ('PanelPowerCycleRegData', c_ulong),
                ('EndOfTable', c_ushort),

                # DTD Table
                ('PixelClock', c_ushort),
                ('HActiveLo', c_ubyte),
                ('HBlankLo', c_ubyte),
                ('HBlankHi', c_ubyte, 4),
                ('HActiveHi', c_ubyte, 4),
                ('VActiveLo', c_ubyte),
                ('VBlankLo', c_ubyte),
                ('VBlankHi', c_ubyte, 4),
                ('VActiveHi', c_ubyte, 4),
                ('HSyncOffsetLo', c_ubyte),
                ('HSyncWidthLo', c_ubyte),
                ('VSyncWidthLo', c_ubyte, 4),
                ('VSyncOffsetLo', c_ubyte, 4),
                ('VSyncWidthHi', c_ubyte, 2),
                ('VSyncOffsetHi', c_ubyte, 2),
                ('HSyncWidthHi', c_ubyte, 2),
                ('HSyncOffsetHi', c_ubyte, 2),
                ('HImgSizeLo', c_ubyte),
                ('VImgSizeLo', c_ubyte),
                ('VImgSizeHi', c_ubyte, 4),
                ('HImgSizeHi', c_ubyte, 4),
                ('HBorder', c_ubyte),
                ('VBorder', c_ubyte),
                ('Flags', c_ubyte),

                # PNP ID Table
                ('IdMfgName', c_ushort),
                ('IdProductCode', c_ushort),
                ('IDSerialNumber', c_ulong),
                ('WeekOfMfg', c_ubyte),
                ('YearOfMfg', c_ubyte)
                ]


##
# @brief        LFPPanelName class
class LFPPanelName(Structure):
    _pack_ = 1
    _fields_ = [('Name', c_ubyte * 13)
                ]


##
# @brief        DualLFPHingeAlignmentParameter class
class DualLfpHingeAlignmentParam(Structure):
    _pack_ = 1
    _fields_ = [('TopBorder', c_ubyte),
                ('BottomBorder', c_ubyte),
                ('Reserved', c_ushort)
                ]


##
# @brief        Block42Fields203 class
class Block42Fields203(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('FlatPanelDataStructureEntry', FlatPanelDataStructure * 16),
                ('LFPPanelNameEntry', LFPPanelName * 16),
                ('ScalingEnableFlags', c_ushort),
                ('SeamlessDrrsMinRR', c_ubyte * 16),
                ('PixelOverlapCount', c_ubyte * 16),
                ('DualLfpHingeAlignmentParamEntry', DualLfpHingeAlignmentParam * 16),
                ('DualLfpPortSyncEnablingBits', c_ushort)
                ]


##
# @brief        Block42Vbt203 Structure
class Block42Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [('u', Block42Fields203),
                ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
                ]


##
# @brief        Block42Fields245 class
class Block42Fields245(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('FlatPanelDataStructureEntry', FlatPanelDataStructure * 16),
                ('LFPPanelNameEntry', LFPPanelName * 16),
                ('ScalingEnableFlags', c_ushort),
                ('SeamlessDrrsMinRR', c_ubyte * 16),
                ('PixelOverlapCount', c_ubyte * 16),
                ('DualLfpHingeAlignmentParamEntry', DualLfpHingeAlignmentParam * 16),
                ('DualLfpPortSyncEnablingBits', c_ushort),
                ('GPUDitheringForBandingArtifacts', c_ushort)
                ]


##
# @brief        Block42Vbt245 Structure
class Block42Vbt245(Union):
    _anonymous_ = ('u',)
    _fields_ = [('u', Block42Fields245),
                ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
                ]


############################
# VBT Block 43 (LFP Backlight Control Data Block)
############################
##
# @brief        BacklightFeatures class
class BacklightFeatures(Structure):
    _pack_ = 1
    _fields_ = [('InverterType', c_ubyte, 2),  # only PWM back-light method is supported
                ('InverterPolarity', c_ubyte, 1),
                ('GPIOPinPair', c_ubyte, 3),  # this field is obsolete
                ('GMBusSpeed', c_ubyte, 2),  # this field is obsolete
                ('PWMFrequency', c_ushort),
                ('MinimumBrightness', c_ubyte),  # obsolete from TGL+
                ('I2CAddress', c_ubyte),  # this field is obsolete
                ('I2CCommand', c_ubyte),  # this field is obsolete
                ]


##
# @brief        BrightnessControlMethod class
class BrightnessControlMethod(Structure):
    _pack_ = 1
    _fields_ = [('PwmSourceSelection', c_ubyte, 4),
                ('PwmControllerSelection', c_ubyte, 4),
                ]


##
# @brief        Block43Fields191 class
class Block43Fields191(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('BacklightStructureSize', c_ubyte),
        ('BacklightFeaturesEntry', BacklightFeatures * 16),
        ('POSTBacklightBrightnessEntry', c_ubyte * 16),
        ('BrightnessControlMethodEntry', BrightnessControlMethod * 16),
    ]


##
# @brief        Block43Vbt191 class
class Block43Vbt191(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block43Fields191),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block43Vbt234 class
class Block43Fields234(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('BacklightStructureSize', c_ubyte),
        ('BacklightFeaturesEntry', BacklightFeatures * 16),
        ('POSTBacklightBrightnessEntry', c_ubyte * 16),  # obsolete from TGL+
        ('BrightnessControlMethodEntry', BrightnessControlMethod * 16),
        ('POSTBrightnessValue', c_uint32 * 16),
        ('MinBrightnessValue', c_uint32 * 16),
    ]


##
# @brief        Block43Vbt234 class
class Block43Vbt234(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block43Fields234),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block43Vbt236 class
class Block43Fields236(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('BacklightStructureSize', c_ubyte),
        ('BacklightFeaturesEntry', BacklightFeatures * 16),
        ('POSTBacklightBrightnessEntry', c_ubyte * 16),  # obsolete from TGL+
        ('BrightnessControlMethodEntry', BrightnessControlMethod * 16),
        ('POSTBrightnessValue', c_uint32 * 16),
        ('MinBrightnessValue', c_uint32 * 16),
        ('BrightnessPrecisionBits', c_ubyte * 16),  # 8 = Range 0 to 255, 16 = Range 0 to 65535
    ]


##
# @brief        Block43Vbt236 class
class Block43Vbt236(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block43Fields236),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block43Vbt259 class
class Block43Fields259(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('BacklightStructureSize', c_ubyte),
        ('BacklightFeaturesEntry', BacklightFeatures * 16),
        ('POSTBacklightBrightnessEntry', c_ubyte * 16),  # obsolete from TGL+
        ('BrightnessControlMethodEntry', BrightnessControlMethod * 16),
        ('POSTBrightnessValue', c_uint32 * 16),
        ('MinBrightnessValue', c_uint32 * 16),
        ('BrightnessPrecisionBits', c_ubyte * 16),  # 8 = Range 0 to 255, 16 = Range 0 to 65535
    ]


##
# @brief        Block43Vbt259 class
class Block43Vbt259(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block43Fields259),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 44 (LFP Power Conservation Features Block)
############################
##
# @brief        Block44Vbt228 class
class Block44Fields228(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('LaceEnable', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('LaceStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),  # DPST/ LACE
    ]


##
# @brief        Block44Vbt228 class
class Block44Vbt228(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields228),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block44Fields232 class
class Block44Fields232(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('LaceEnable', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('LaceStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),  # DPST/ LACE
        ('Edp_4k_2k_hobl', c_ubyte * 2)
    ]


##
# @brief        Block44Vbt232 class
class Block44Vbt232(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields232),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block44Fields233 class
class Block44Fields233(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('LaceEnable', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('LaceStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),
        ('Edp_4k_2k_hobl', c_ubyte * 2),
        ('VRR', c_ubyte * 2),
    ]


##
# @brief        Block44Vbt233 class
class Block44Vbt233(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields233),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block44Fields247 class
class Block44Fields247(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('LaceEnable', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('LaceStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),
        ('Edp_4k_2k_hobl', c_ubyte * 2),
        ('VRR', c_ubyte * 2),
        ('ELP', c_ubyte * 2),
        ('OPST', c_ubyte * 2),
        ('AgressivenessProfile2', c_ubyte * 16),
    ]


##
# @brief        Block44Vbt247 class
class Block44Vbt247(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields247),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block44Fields253 class
class Block44Fields253(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('LaceEnable', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('LaceStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),  # 0:3 DPST, 4:7 LACE
        ('Edp_4k_2k_hobl', c_ubyte * 2),
        ('VRR', c_ubyte * 2),
        ('ELP', c_ubyte * 2),
        ('OPST', c_ubyte * 2),
        ('AgressivenessProfile2', c_ubyte * 16),  # 0:3 OPST, 4:7 ELP
        ('APD', c_ubyte * 2),
        ('PixOptix', c_ubyte * 2),
        ('AggressivenessProfile3', c_ubyte * 16)  # 0:3 APD, 4:7 PixOptix
    ]


##
# @brief        Block44Vbt253 class
class Block44Vbt253(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields253),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


##
# @brief        Block44Fields257 class
class Block44Fields257(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('LfpFeatureBits', c_ubyte),  # this field is obsolete
        ('ALS_Response_Data', c_ubyte * 20),
        ('Reserved', c_ubyte),
        ('DpstEnable', c_ubyte * 2),  # this field is obsolete
        ('PsrEnable', c_ubyte * 2),
        ('DRRSEnable', c_ubyte * 2),
        ('DisplayLaceSupport', c_ubyte * 2),
        ('AdtEnable', c_ubyte * 2),
        ('DmrrsEnable', c_ubyte * 2),
        ('AdbEnable', c_ubyte * 2),
        ('DefaultDisplayLaceEnabledStatus', c_ubyte * 2),
        ('AggressivenessProfile', c_ubyte * 16),  # this field is obsolete
        ('Edp_4k_2k_hobl', c_ubyte * 2),
        ('VRR', c_ubyte * 2),
        ('ELP', c_ubyte * 2),  # this field is obsolete
        ('OPST', c_ubyte * 2),  # this field is obsolete
        ('AgressivenessProfile2', c_ubyte * 16),  # this field is obsolete
        ('APD', c_ubyte * 2),  # this field is obsolete
        ('PixOptix', c_ubyte * 2),  # this field is obsolete
        ('AggressivenessProfile3', c_ubyte * 16),  # this field is obsolete
        ('PanelIdentification', c_ubyte * 16),  # 0:3 LCD, OLED 4:7 Reserved
        ('XPSTSupport', c_ubyte * 2),
        ('TconBasedBacklightOptimization', c_ubyte * 2),
        ('AgressivenessProfile4', c_ubyte * 16),  # 0:3 XPST Aggressiveness, 4:7 TCON Aggressiveness
        ('TconBasedBacklightOptimizationCoExistenceWithXPST', c_ubyte * 2),
    ]


##
# @brief        Block44Vbt257 class
class Block44Vbt257(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block44Fields257),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 46 (Chromaticity for Narrow Gamut Panel Configuration Block)
############################
##
# @brief        Block46Vbt203 class
class Block46Fields203(Structure):
    _pack_ = 1
    _fields_ = [
        ('BlockInfo', BlockInfo),
        ('ChromaticityFeatures', c_ubyte),
        ('RedGreen', c_ubyte),
        ('RedWhite', c_ubyte),
        ('RedX', c_ubyte),
        ('RedY', c_ubyte),
        ('GreenX', c_ubyte),
        ('GreenY', c_ubyte),
        ('BlueX', c_ubyte),
        ('BlueY', c_ubyte),
        ('WhiteX', c_ubyte),
        ('WhiteY', c_ubyte),
    ]


##
# @brief        Block46Vbt203 class
class Block46Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block46Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 52 (MIPI Configuration Block)
############################
##
# @brief        MipiDataStructure class
class MipiDataStructure(Structure):
    _pack_ = 1
    _fields_ = [('PanelIdentifier', c_ushort),

                # General params: 4 bytes
                ('Dithering', c_ulong, 1),
                ('ReservedGP1', c_ulong, 1),
                ('PanelType', c_ulong, 1),
                ('PanelArchitectureType', c_ulong, 2),
                ('CommandMode', c_ulong, 1),
                ('VideoTransferMode', c_ulong, 2),
                ('CABCSupport', c_ulong, 1),
                ('PPSGPIOPins', c_ulong, 1),
                ('VideoModeColorFormat', c_ulong, 4),
                ('PanelRotationConfiguration', c_ulong, 2),
                ('BTADisable', c_ulong, 1),
                ('ReservedGP17', c_ulong, 15),

                # Port Desc: 2 bytes
                ('DualLinkSupport', c_ushort, 2),
                ('NumberOfLanes', c_ushort, 2),
                ('PixelOverlapCount', c_ushort, 3),
                ('RGBFlip', c_ushort, 1),
                ('CABCCtrlPorts', c_ushort, 2),
                ('PWMBkltCtrlPorts', c_ushort, 2),
                ('PortSyncFeature', c_ushort, 1),
                ('ReservedPD13', c_ushort, 3),

                # DSI Controller Parameters: 2 bytes
                ('DSIUsage', c_ushort, 1),
                ('ReservedDCP1', c_ushort, 15),

                ('Reserved1', c_ubyte),
                ('RequiredBurstModeFreq', c_ulong),
                ('DSIDDRClock', c_ulong),
                ('BridgeRefClock', c_ulong),

                # LP Byte Clock: 1 byte
                ('ByteClockSelect', c_ubyte, 2),
                ('ReservedLBC2', c_ubyte, 6),

                # Dphy Flags: 2 bytes
                ('DphyParamValid', c_ushort, 1),
                ('EOTDisabled', c_ushort, 1),
                ('ClockStop', c_ushort, 1),
                ('BlankingPacketsDuringBLLP', c_ushort, 1),
                ('LPClockDuringLPM', c_ushort, 1),
                ('ReservedDF5', c_ushort, 11),

                ('HSTxTimeOut', c_ulong),
                ('LPRXTimeOut', c_ulong),
                ('TurnAroundTimeOut', c_ulong),
                ('DeviceResetTimer', c_ulong),
                ('MasterinitTimer', c_ulong),
                ('DBIBandwidthTimer', c_ulong),
                ('LpByteClkValue', c_ulong),

                # DPhyParam: 4 bytes
                ('PrepareCount', c_ulong, 6),
                ('ReservedDP6', c_ulong, 2),
                ('ClkZeroCount', c_ulong, 8),
                ('TrailCount', c_ulong, 5),
                ('ReservedDP21', c_ulong, 3),
                ('ExitZeroCount', c_ulong, 6),
                ('ReservedDP30', c_ulong, 2),

                ('ClockLaneSwitchingCount', c_ulong),
                ('HighToLowSwitchingCount', c_ulong),
                ('Reserved2', c_ulong * 6),
                ('TClkMiss', c_ubyte),
                ('TClkPost', c_ubyte),
                ('Reserved3', c_ubyte),
                ('TClkPre', c_ubyte),
                ('TClkPrepare', c_ubyte),
                ('TClkSettle', c_ubyte),
                ('TClkTermEnable', c_ubyte),
                ('TClkTrail', c_ubyte),
                ('TClkPrepareClkZero', c_ushort),
                ('Reserved4', c_ubyte),
                ('TDTermEnable', c_ubyte),
                ('TEOT', c_ubyte),
                ('THSExit', c_ubyte),
                ('THSPrepare', c_ubyte),
                ('THSPrepareHSZero', c_ushort),
                ('Reserved5', c_ubyte),
                ('THSSettle', c_ubyte),
                ('THSSkip', c_ubyte),
                ('THSTrail', c_ubyte),
                ('TInit', c_ubyte),
                ('TLPX', c_ubyte),
                ('Reserved6', c_ubyte * 3),
                ('GPIOIndexes', c_ubyte * 6)
                ]


##
# @brief        MipiPps class
class MipiPps(Structure):
    _pack_ = 1
    _fields_ = [('PanelPowerONDelay', c_ushort),
                ('PanelPowerOnToBacklightEnableDelay', c_ushort),
                ('BacklightDisableToPanelPowerOFFDelay', c_ushort),
                ('PanelPowerOFFDelay', c_ushort),
                ('PanelPowerCycleDelay', c_ushort)
                ]


##
# @brief        MipiPwm class
class MipiPwm(Structure):
    _pack_ = 1
    _fields_ = [('PWMOnToBacklightEnableDelay', c_ushort),
                ('BacklightDisableToPWMOffDelay', c_ushort)
                ]


##
# @brief        MipiPmic class
class MipiPmic(Structure):
    _pack_ = 1
    _fields_ = [('PMICI2CBus', c_ubyte)
                ]


##
# @brief        Block52Fields203 class
class Block52Fields203(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('MipiDataStructureEntry', MipiDataStructure * 6),
                ('MipiPpsEntry', MipiPps * 6),
                ('MipiPwmEntry', MipiPwm * 6),
                ('MipiPmicEntry', MipiPmic * 6)
                ]


##
# @brief        Block52Vbt203 class
class Block52Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block52Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 56 (Compression Parameters)
############################
##
# @brief        CompressionParameterDataStruct class
class CompressionParamDataStruct(Structure):
    _pack_ = 1
    _fields_ = [('DSCAlgorithmRevision', c_ubyte),
                ('DSCRCBufferBlockSize', c_ubyte),
                ('DSCRCBufferSize', c_ubyte),
                ('DSCSlicesPerLine', c_ulong),
                ('DSCLineBufferDepth', c_ubyte),

                # Flag Bits 1: 1 byte
                ('BlockPredictionEnable', c_ubyte, 1),
                ('ReservedFB1', c_ubyte, 7),

                ('DSCMaximumBitsPerPixel', c_ubyte),
                ('DSCColorDepthCapabilities', c_ubyte),
                ('DSCSliceHeight', c_ushort)
                ]


##
# @brief        Block56Fields203 class
class Block56Fields203(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('CompressionParamStructEntrySize', c_ushort),
                ('CompressionParamDataStructEntry', CompressionParamDataStruct * 16)
                ]


##
# @brief        Block56Vbt203 class
class Block56Vbt203(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block56Fields203),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 57 (PHY Vswing Tables Block)
############################
##
# @brief        Block57Fields218 class
class Block57Fields218(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('NumVswingTables', c_ubyte),
                ('NumVswingColumns', c_ubyte),
                ('VSwingPreempTables', VswingPreEmpTable * 6)  # each uint32 value represents one phy buffer parameter
                ]


##
# @brief        Block57Vbt218 class
class Block57Vbt218(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block57Fields218),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]


############################
# VBT Block 58 (Generic DTD Block)
############################
##
# @brief        GenericDisplayTimingData class
class GenericDisplayTimingData(Structure):
    _pack_ = 1
    _fields_ = [
        ('PixelClockKhz', c_ulong),
        ('HActive', c_ushort),
        ('HBlank', c_ushort),
        ('HFrontPorch', c_ushort),
        ('HSync', c_ushort),
        ('VActive', c_ushort),
        ('VBlank', c_ushort),
        ('VFrontPorch', c_ushort),
        ('VSync', c_ushort),
        ('HorizontalImageSize', c_ushort),
        ('VerticalImageSize', c_ushort),
        ('Flags', c_ubyte),
        ('Reserved1', c_ubyte * 3),
    ]


##
# @brief        Block58Fields229 class
class Block58Fields229(Structure):
    _pack_ = 1
    _fields_ = [('BlockInfo', BlockInfo),
                ('TimingInfoSize', c_ushort),
                ('GenericDisplayTimingDataEntry', GenericDisplayTimingData * 24)
                ]


##
# @brief        Block58Vbt229 class
class Block58Vbt229(Union):
    _anonymous_ = ('u',)
    _fields_ = [
        ('u', Block58Fields229),
        ('byte_data', c_ubyte * BLOCK_SIZE_MAX)
    ]
