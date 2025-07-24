######################################################################################
# @file         gen11p5_powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Gen11p5 specific module for Display Power well verification
# @description  @ref gen11p5_powerwell.py contains Gen11p5 powerwell dependencies
#
# @author       Rohit Kumar
######################################################################################
import ctypes

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen11p5.DisplayPowerHandler import Gen11p5DisplayPowerRegs
from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 32-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
ENABLED_POWER_WELL_MASK_LKF1 = 0x01B0031D


##
# @brief        DisplayPowerWell for Gen11p5 platforms
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

        offset = Gen11p5DisplayPowerRegs.OFFSET_PWR_WELL_CTL.PWR_WELL_CTL2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl = Gen11p5DisplayPowerRegs.REG_PWR_WELL_CTL(offset, value)
        if powerwell_ctl is not None and powerwell_ctl.value != 0:
            self.PowerwellPG1 = powerwell_ctl.PowerWell1State
            self.PowerwellPG3 = powerwell_ctl.PowerWell3State
            self.PowerwellPG4 = powerwell_ctl.PowerWell4State
            self.PowerwellPG5 = powerwell_ctl.PowerWell5State

        offset = Gen11p5DisplayPowerRegs.OFFSET_PWR_WELL_CTL_AUX.PWR_WELL_CTL_AUX2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_aux = Gen11p5DisplayPowerRegs.REG_PWR_WELL_CTL_AUX(offset, value)
        if powerwell_ctl_aux is not None and powerwell_ctl_aux.value != 0:
            self.PowerwellAuxAIo = powerwell_ctl_aux.AuxAIoPowerState
            self.PowerwellAuxBIo = powerwell_ctl_aux.AuxBIoPowerState
            self.PowerwellAuxCIo = powerwell_ctl_aux.AuxCIoPowerState
            self.PowerwellAuxDIo = powerwell_ctl_aux.Usbc1IoPowerState
            self.PowerwellAuxEIo = powerwell_ctl_aux.Usbc2IoPowerState
            self.PowerwellAuxFIo = powerwell_ctl_aux.Usbc3IoPowerState
            self.PowerwellAuxGIo = powerwell_ctl_aux.Usbc4IoPowerState
            self.PowerwellAuxHIo = powerwell_ctl_aux.Usbc5IoPowerState
            self.PowerwellAuxIIo = powerwell_ctl_aux.Usbc6IoPowerState
            self.PowerwellAuxTBT1Io = powerwell_ctl_aux.AuxTbt1IoPowerState
            self.PowerwellAuxTBT2Io = powerwell_ctl_aux.AuxTbt2IoPowerState
            self.PowerwellAuxTBT3Io = powerwell_ctl_aux.AuxTbt3IoPowerState
            self.PowerwellAuxTBT4Io = powerwell_ctl_aux.AuxTbt4IoPowerState
            self.PowerwellAuxTBT5Io = powerwell_ctl_aux.AuxTbt5IoPowerState
            self.PowerwellAuxTBT6Io = powerwell_ctl_aux.AuxTbt6IoPowerState

        offset = Gen11p5DisplayPowerRegs.OFFSET_PWR_WELL_CTL_DDI.PWR_WELL_CTL_DDI2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_ddi = Gen11p5DisplayPowerRegs.REG_PWR_WELL_CTL_DDI(offset, value)
        if powerwell_ctl_ddi is not None and powerwell_ctl_ddi.value != 0:
            self.PowerwellDdiAIo = powerwell_ctl_ddi.DdiAIoPowerState
            self.PowerwellDdiBIo = powerwell_ctl_ddi.DdiBIoPowerState
            self.PowerwellDdiCIo = powerwell_ctl_ddi.DdiCIoPowerState
            self.PowerwellDdiDIo = powerwell_ctl_ddi.Usbc1IoPowerState
            self.PowerwellDdiEIo = powerwell_ctl_ddi.Usbc2IoPowerState
            self.PowerwellDdiFIo = powerwell_ctl_ddi.Usbc3IoPowerState
            self.PowerwellDdiGIo = powerwell_ctl_ddi.Usbc4IoPowerState
            self.PowerwellDdiHIo = powerwell_ctl_ddi.Usbc5IoPowerState
            self.PowerwellDdiIIo = powerwell_ctl_ddi.Usbc6IoPowerState


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_LKF1

##
# Pipe powerwell dependencies
# Pipe A -> PG1
# Pipe B -> PG3->PG1
# pipe C -> PG4->PG3->PG1
# pipe D -> PG5->PG4->PG3->PG1
PipePowerWellMask = [
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
# DDI powerwell dependencies
# DDI_D IO -> PG3->PG1
# DDI_E IO -> PG3->PG1
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'PowerwellDdiEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_G
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_H
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_I
    DisplayPowerWell({'value': 0}),
]

##
# AUX powerwell dependencies
# AUX_D IO -> PG3->PG1
# AUX_E IO -> PG3->PG1
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'value': 0}),
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
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxEIo': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'value': 0}),
]

##
# Feature powerwell dependencies
# Audio -> PG3->PG1
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1}),
]

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
