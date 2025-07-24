######################################################################################
# @file         gen13_powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Gen13 specific module for Display Power well verification
#               gen13_powerwell.py contains Gen13 powerwell dependencies
#
# @author       Rohit Kumar
######################################################################################
import ctypes

from DisplayRegs import DisplayArgs
from Libs.Feature.display_powerwell import common
from DisplayRegs.Gen13.DisplayPowerHandler import Gen13DisplayPowerRegs

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 64-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
ENABLED_POWER_WELL_MASK_DG2 = 0x1FFF03FE3
ENABLED_POWER_WELL_MASK_ADLP = 0x1FE33FC63


##
# @brief        DisplayPowerWell for Gen13 platforms
class DisplayPowerWell(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", common.DisplayPowerWellMask),
        ("value", ctypes.c_uint64)
    ]

    ##
    # @brief        DisplayPowerWell default __init__ function
    # @param[in]    mask [optional], A dictionary indicating powerwell status separately (Ex: {'PowerwellPG1':1})
    # @param[in]    platform [optional], platform name
    # @param[in]    gfx_index [optional]
    def __init__(self, mask=None, platform=None, gfx_index='gfx_0'):
        super(DisplayPowerWell, self).__init__()
        self.value = 0
        self.active_power_wells = []

        if mask is not None:
            if 'value' not in mask.keys():
                self.active_power_wells = mask.keys()
                for key, value in mask.items():
                    setattr(self, key, value)

        if platform is None:
            return

        offset = Gen13DisplayPowerRegs.OFFSET_PWR_WELL_CTL.PWR_WELL_CTL2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl = Gen13DisplayPowerRegs.REG_PWR_WELL_CTL(offset, value)
        if powerwell_ctl is not None and powerwell_ctl.value != 0:
            self.PowerwellPG1 = powerwell_ctl.PowerWell1State
            self.PowerwellPG2 = powerwell_ctl.PowerWell2State
            self.PowerwellPGA = powerwell_ctl.PowerWellAState
            self.PowerwellPGB = powerwell_ctl.PowerWellBState
            self.PowerwellPGC = powerwell_ctl.PowerWellCState
            self.PowerwellPGD = powerwell_ctl.PowerWellDState

        offset = Gen13DisplayPowerRegs.OFFSET_PWR_WELL_CTL_AUX.PWR_WELL_CTL_AUX2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_aux = Gen13DisplayPowerRegs.REG_PWR_WELL_CTL_AUX(offset, value)
        if powerwell_ctl_aux is not None and powerwell_ctl_aux.value != 0:
            self.PowerwellAuxAIo = powerwell_ctl_aux.AuxAIoPowerState
            self.PowerwellAuxBIo = powerwell_ctl_aux.AuxBIoPowerState

            if platform in ['DG2']:
                self.PowerwellAuxCIo = powerwell_ctl_aux.AuxCIoPowerState
                self.PowerwellAuxDIo = powerwell_ctl_aux.AuxDIoPowerState

            self.PowerwellAuxFIo = powerwell_ctl_aux.Usbc1IoPowerState

            if platform in ['ADLP']:
                self.PowerwellAuxGIo = powerwell_ctl_aux.Usbc2IoPowerState
                self.PowerwellAuxHIo = powerwell_ctl_aux.Usbc3IoPowerState
                self.PowerwellAuxIIo = powerwell_ctl_aux.Usbc4IoPowerState
                self.PowerwellAuxTBT1Io = powerwell_ctl_aux.AuxTbt1IoPowerState
                self.PowerwellAuxTBT2Io = powerwell_ctl_aux.AuxTbt2IoPowerState
                self.PowerwellAuxTBT3Io = powerwell_ctl_aux.AuxTbt3IoPowerState
                self.PowerwellAuxTBT4Io = powerwell_ctl_aux.AuxTbt4IoPowerState

        offset = Gen13DisplayPowerRegs.OFFSET_PWR_WELL_CTL_DDI.PWR_WELL_CTL_DDI2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_ddi = Gen13DisplayPowerRegs.REG_PWR_WELL_CTL_DDI(offset, value)
        if powerwell_ctl_ddi is not None and powerwell_ctl_ddi.value != 0:
            self.PowerwellDdiAIo = powerwell_ctl_ddi.DdiAIoPowerState
            self.PowerwellDdiBIo = powerwell_ctl_ddi.DdiBIoPowerState

            if platform in ['DG2']:
                self.PowerwellDdiCIo = powerwell_ctl_ddi.DdiCIoPowerState
                self.PowerwellDdiDIo = powerwell_ctl_ddi.DdiDIoPowerState

            self.PowerwellDdiFIo = powerwell_ctl_ddi.Usbc1IoPowerState

            if platform in ['ADLP']:
                self.PowerwellDdiGIo = powerwell_ctl_ddi.Usbc2IoPowerState
                self.PowerwellDdiHIo = powerwell_ctl_ddi.Usbc3IoPowerState
                self.PowerwellDdiIIo = powerwell_ctl_ddi.Usbc4IoPowerState


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_DG2

##
# Pipe powerwell dependencies
PipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPGA': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGB': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGC': 1}),
    # PIPE_D
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGD': 1})
]

##
# DDI powerwell dependencies
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'PowerwellDdiFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_G
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_H
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_I
    DisplayPowerWell({'value': 0}),
]

# DDI powerwell dependencies
ADLPDdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'PowerwellDdiFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_G
    DisplayPowerWell({'PowerwellDdiGIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_H
    DisplayPowerWell({'PowerwellDdiHIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_I
    DisplayPowerWell({'PowerwellDdiIIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# AUX powerwell dependencies
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'value': 0}),
]

##
# AUX only powerwell dependencies for TypeC
AuxOnlyPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxEIo': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1})
]

##
# AUX powerwell dependencies
ADLPAuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# Thunderbolt AUX powerwell dependencies
TbtAuxPowerWellMask = [
    # AUX_CHANNEL_A not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_B not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_E not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxTBT1Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxTBT2Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxTBT3Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxTBT4Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# Feature powerwell dependencies
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # PIPE_A DSC POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1})
]

##
# Writeback powerwell dependencies
WBPowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPGA': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGB': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGC': 1}),
    # PIPE_D
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPGD': 1})
]

##
# Non-Combo PHY ports
NonComboPhyPorts = ['E', 'F', 'G', 'H', 'I']
