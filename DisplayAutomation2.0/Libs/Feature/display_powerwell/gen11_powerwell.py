######################################################################################
# @file         gen11_powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Gen11 specific module for Display Power well verification
# @description  @ref gen11_powerwell.py contains Gen11 powerwell dependencies
#
# @author       Rohit Kumar
######################################################################################
import ctypes

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen11.DisplayPowerHandler import Gen11DisplayPowerRegs
from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 32-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
ENABLED_POWER_WELL_MASK_ICL_LP = 0x3F3C7EF
ENABLED_POWER_WELL_MASK_JSL = 0xF001EF


##
# @brief        DisplayPowerWell for Gen11 platforms
class DisplayPowerWell(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", common.DisplayPowerWellMask),
        ("value", ctypes.c_uint64)
    ]

    ##
    # @brief        DisplayPowerWell default __init__ function
    # @param[in]    mask[optional], A dictionary indicating powerwell status separately (Ex: {'PowerwellPG1':1})
    # @param[in]    platform[optional], platform name
    # @param[in]    gfx_index[optional]
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

        offset = Gen11DisplayPowerRegs.OFFSET_PWR_WELL_CTL.PWR_WELL_CTL2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl = Gen11DisplayPowerRegs.REG_PWR_WELL_CTL(offset, value)
        if powerwell_ctl is not None and powerwell_ctl.value != 0:
            self.PowerwellPG1 = powerwell_ctl.PowerWell1State
            self.PowerwellPG2 = powerwell_ctl.PowerWell2State
            self.PowerwellPG3 = powerwell_ctl.PowerWell3State
            self.PowerwellPG4 = powerwell_ctl.PowerWell4State

        offset = Gen11DisplayPowerRegs.OFFSET_PWR_WELL_CTL_AUX.PWR_WELL_CTL_AUX2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_aux = Gen11DisplayPowerRegs.REG_PWR_WELL_CTL_AUX(offset, value)
        if powerwell_ctl_aux is not None and powerwell_ctl_aux.value != 0:
            self.PowerwellAuxAIo = powerwell_ctl_aux.AuxAIoPowerState
            self.PowerwellAuxBIo = powerwell_ctl_aux.AuxBIoPowerState
            self.PowerwellAuxCIo = powerwell_ctl_aux.AuxCIoPowerState
            self.PowerwellAuxDIo = powerwell_ctl_aux.AuxDIoPowerState
            self.PowerwellAuxEIo = powerwell_ctl_aux.AuxEIoPowerState
            self.PowerwellAuxFIo = powerwell_ctl_aux.AuxFIoPowerState
            self.PowerwellAuxTBT1Io = powerwell_ctl_aux.AuxTbt1IoPowerState
            self.PowerwellAuxTBT2Io = powerwell_ctl_aux.AuxTbt2IoPowerState
            self.PowerwellAuxTBT3Io = powerwell_ctl_aux.AuxTbt3IoPowerState
            self.PowerwellAuxTBT4Io = powerwell_ctl_aux.AuxTbt4IoPowerState

        offset = Gen11DisplayPowerRegs.OFFSET_PWR_WELL_CTL_DDI.PWR_WELL_CTL_DDI2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_ddi = Gen11DisplayPowerRegs.REG_PWR_WELL_CTL_DDI(offset, value)
        if powerwell_ctl_ddi is not None and powerwell_ctl_ddi.value != 0:
            self.PowerwellDdiAIo = powerwell_ctl_ddi.DdiAIoPowerState
            self.PowerwellDdiBIo = powerwell_ctl_ddi.DdiBIoPowerState
            self.PowerwellDdiCIo = powerwell_ctl_ddi.DdiCIoPowerState
            self.PowerwellDdiDIo = powerwell_ctl_ddi.DdiDIoPowerState
            self.PowerwellDdiEIo = powerwell_ctl_ddi.DdiEIoPowerState
            self.PowerwellDdiFIo = powerwell_ctl_ddi.DdiFIoPowerState


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_ICL_LP

##
# Pipe powerwell dependencies
# Pipe A -> PG1
# Pipe B -> PG3->PG2->PG1
# pipe C -> PG4->PG3->PG2->PG1
PipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1})
]

##
# DDI powerwell dependencies
# DDI_A IO -> PG1
# DDI_B IO -> PG3->PG2->PG1
# DDI_C IO -> PG3->PG2->PG1
# DDI_D IO -> PG3->PG2->PG1
# DDI_E IO -> PG3->PG2->PG1
# DDI_F IO -> PG3->PG2->PG1
# @note DDI_G to DDI_I not present
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'PowerwellDdiEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'PowerwellDdiFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_NOT_PRESENT
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_NOT_PRESENT
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_NOT_PRESENT
    DisplayPowerWell({'value': 0}),
]

##
# AUX powerwell dependencies
# AUX_A IO -> PG1
# AUX_B IO -> PG3->PG2->PG1
# AUX_C IO -> PG3->PG2->PG1
# AUX_D IO -> PG3->PG2->PG1
# AUX_E IO -> PG3->PG2->PG1
# AUX_F IO -> PG3->PG2->PG1
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1})
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
    DisplayPowerWell({'PowerwellAuxFIo': 1})
]

##
# Thunderbolt AUX powerwell dependencies
# TBT1 IO -> PG3->PG2->PG1
# TBT2 IO -> PG3->PG2->PG1
# TBT3 IO -> PG3->PG2->PG1
# TBT4 IO -> PG3->PG2->PG1
TbtAuxPowerWellMask = [
    # AUX_CHANNEL_A not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_B not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxTBT1Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxTBT2Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxTBT3Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxTBT4Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1})
]

##
# Feature powerwell dependencies
# Audio ->  PG3->PG2->PG1
# DSC ->    PG2->PG1
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DSC_POWERWELL (eDP and MIPI DSI)
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1})
]

##
# Bit mask to enable all powerwell for handling dual eDP scenario
EnableDualEdpPowerWellMask = DisplayPowerWell(
    {'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1, 'PowerwellAuxAIo': 1, 'PowerwellAuxBIo': 1})

##
# Bit mask to enable aux powerwell for Type-C
EnableTypeCAuxPowerWellMask = DisplayPowerWell(
    {'PowerwellAuxCIo': 1, 'PowerwellAuxDIo': 1, 'PowerwellAuxEIo': 1, 'PowerwellAuxFIo': 1})

##
# Writeback powerwell dependencies
WBPowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1}),
    # PIPE_D
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1, 'PowerwellPG5': 1})
]

##
# Non-Combo PHY ports
NonComboPhyPorts = ['C', 'D', 'E', 'F', 'G', 'H', 'I']
