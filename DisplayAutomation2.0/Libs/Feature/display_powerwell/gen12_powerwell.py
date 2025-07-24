######################################################################################
# @file         gen12_powerwell.py
# @brief        Gen12 specific module for Display Power well verification
#               gen12_powerwell.py contains Gen12 powerwell dependencies
#
# @author       Rohit Kumar
######################################################################################
import ctypes

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen12.DisplayPowerHandler import Gen12DisplayPowerRegs
from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 32-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
ENABLED_POWER_WELL_MASK_TGL = 0x1FFFFFFF
ENABLED_POWER_WELL_MASK_DG1 = 0x00F001FF
ENABLED_POWER_WELL_MASK_RKL = 0x00F001ED
ENABLED_POWER_WELL_MASK_LKFR = 0x01B0037D
ENABLED_POWER_WELL_MASK_ADLS = 0x01F003FF


##
# @brief        DisplayPowerWell for Gen12 platforms
class DisplayPowerWell(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", common.DisplayPowerWellMask),
        ("value", ctypes.c_uint64)
    ]

    ##
    # @brief        DisplayPowerWell default __init__ function
    # @param[in]    mask A dictionary indicating powerwell status separately (Ex: {'PowerwellPG1':1})
    # @param[in]    platform platform name
    # @param[in]    gfx_index
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

        offset = Gen12DisplayPowerRegs.OFFSET_PWR_WELL_CTL.PWR_WELL_CTL2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl = Gen12DisplayPowerRegs.REG_PWR_WELL_CTL(offset, value)
        if powerwell_ctl is not None and powerwell_ctl.value != 0:
            self.PowerwellPG1 = powerwell_ctl.PowerWell1State
            self.PowerwellPG2 = powerwell_ctl.PowerWell2State
            self.PowerwellPG3 = powerwell_ctl.PowerWell3State
            self.PowerwellPG4 = powerwell_ctl.PowerWell4State
            self.PowerwellPG5 = powerwell_ctl.PowerWell5State

        offset = Gen12DisplayPowerRegs.OFFSET_PWR_WELL_CTL_AUX.PWR_WELL_CTL_AUX2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_aux = Gen12DisplayPowerRegs.REG_PWR_WELL_CTL_AUX(offset, value)
        if powerwell_ctl_aux is not None and powerwell_ctl_aux.value != 0:
            self.PowerwellAuxAIo = powerwell_ctl_aux.AuxAIoPowerState

            if platform in ['ADLS']:
                self.PowerwellAuxBIo = powerwell_ctl_aux.Usbc1IoPowerState
                self.PowerwellAuxCIo = powerwell_ctl_aux.Usbc2IoPowerState
                self.PowerwellAuxDIo = powerwell_ctl_aux.Usbc3IoPowerState
                self.PowerwellAuxEIo = powerwell_ctl_aux.Usbc4IoPowerState
            else:
                self.PowerwellAuxBIo = powerwell_ctl_aux.AuxBIoPowerState

                ##
                # DashG and RKL are using DDI TC1 / USB C1 for port C and DDI TC2 / USB C2 for port D
                if platform in ['DG1', 'RKL']:
                    self.PowerwellAuxCIo = powerwell_ctl_aux.Usbc1IoPowerState
                    self.PowerwellAuxDIo = powerwell_ctl_aux.Usbc2IoPowerState
                else:
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

        offset = Gen12DisplayPowerRegs.OFFSET_PWR_WELL_CTL_DDI.PWR_WELL_CTL_DDI2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl_ddi = Gen12DisplayPowerRegs.REG_PWR_WELL_CTL_DDI(offset, value)
        if powerwell_ctl_ddi is not None and powerwell_ctl_ddi.value != 0:
            self.PowerwellDdiAIo = powerwell_ctl_ddi.DdiAIoPowerState

            if platform in ['ADLS']:
                self.PowerwellDdiBIo = powerwell_ctl_ddi.Usbc1IoPowerState
                self.PowerwellDdiCIo = powerwell_ctl_ddi.Usbc2IoPowerState
                self.PowerwellDdiDIo = powerwell_ctl_ddi.Usbc3IoPowerState
                self.PowerwellDdiEIo = powerwell_ctl_ddi.Usbc4IoPowerState
            else:
                self.PowerwellDdiBIo = powerwell_ctl_ddi.DdiBIoPowerState

                ##
                # DashG and RKL are using DDI TC1 / USB C1 for port C and DDI TC2 / USB C2 for port D
                if platform in ['DG1', 'RKL']:
                    self.PowerwellDdiCIo = powerwell_ctl_ddi.Usbc1IoPowerState
                    self.PowerwellDdiDIo = powerwell_ctl_ddi.Usbc2IoPowerState
                else:
                    self.PowerwellDdiCIo = powerwell_ctl_ddi.DdiCIoPowerState
                    self.PowerwellDdiDIo = powerwell_ctl_ddi.Usbc1IoPowerState
                    self.PowerwellDdiEIo = powerwell_ctl_ddi.Usbc2IoPowerState
                    self.PowerwellDdiFIo = powerwell_ctl_ddi.Usbc3IoPowerState
                    self.PowerwellDdiGIo = powerwell_ctl_ddi.Usbc4IoPowerState
                    self.PowerwellDdiHIo = powerwell_ctl_ddi.Usbc5IoPowerState
                    self.PowerwellDdiIIo = powerwell_ctl_ddi.Usbc6IoPowerState


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_TGL

##
# Pipe powerwell dependencies
# Pipe A -> PG1
# Pipe B -> PG3->PG2->PG1
# pipe C -> PG4->PG3->PG1
# pipe D -> PG5->PG4->PG3->PG1
PipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1}),
    # PIPE_D
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1, 'PowerwellPG5': 1})
]

##
# Pipe powerwell dependencies for RocketLake
# Pipe A -> PG1
# Pipe B -> PG3->PG1
# Pipe C -> PG4->PG3->PG1
RklPipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1}),
]

##
# Pipe powerwell dependencies
# Pipe A -> PG1
# Pipe B -> PG3->PG1
# Pipe C -> PG4->PG3->PG1
# Pipe D -> PG5->PG4->PG3->PG1
LkfRPipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1}),
    # PIPE_D
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1, 'PowerwellPG4': 1, 'PowerwellPG5': 1})
]

DdiPowerWellMask = []

##
# DDI powerwell dependencies
# DDI_A IO -> PG1
# DDI_B IO -> PG1
# DDI_C IO -> PG1
# DDI_D IO -> PG3->PG1
# DDI_E IO -> PG3->PG1
# DDI_F IO -> PG3->PG1
# DDI_G IO -> PG3->PG1
# DDI_H IO -> PG3->PG1
# DDI_I IO -> PG3->PG1
TglDdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'PowerwellDdiEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'PowerwellDdiFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_G
    DisplayPowerWell({'PowerwellDdiGIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_H
    DisplayPowerWell({'PowerwellDdiHIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_I
    DisplayPowerWell({'PowerwellDdiIIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
]

##
# DDI powerwell dependencies for DG1
# DDI_A IO -> PG1
# DDI_B IO -> PG1
# DDI_C IO -> PG3->PG1
# DDI_D IO -> PG3->PG1
DG1DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
]

##
# DDI powerwell dependencies for RocketLake
# DDI_A IO -> PG1
# DDI_B IO -> PG1
# DDI_C IO -> PG3->PG1
# DDI_D IO -> PG3->PG1
RklDdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
]

##
# DDI powerwell dependencies
# DDI_D IO -> PG3->PG1
# DDI_E IO -> PG3->PG1
LkfRDdiPowerWellMask = [
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
# DDI powerwell dependencies
AdlSDdiPowerWellMask = [
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
]

AuxPowerWellMask = []

##
# AUX powerwell dependencies
# AUX_D IO -> PG3->PG1
# AUX_E IO -> PG3->PG1
TglAuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxEIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
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
# DG1 AUX powerwell dependencies
Dg1AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
]

##
# AUX powerwell dependencies
# AUX_D IO -> PG3->PG1
# AUX_E IO -> PG3->PG1
RklAuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG3': 1}),
]

##
# AUX powerwell dependencies
# AUX_D IO -> PG3->PG1
# AUX_E IO -> PG3->PG1
LkfRAuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1, 'PowerwellPG1': 1}),
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
# AUX powerwell dependencies
AdlSAuxPowerWellMask = [
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
    # AUX_CHANNEL_C not used for TBT
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxTBT1Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxTBT2Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxTBT3Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxTBT4Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxTBT5Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxTBT6Io': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
]

##
# Feature powerwell dependencies
# Audio -> PG3->PG1
# DSC -> PG2->PG1
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1, 'PowerwellPG3': 1}),
    # PIPE_A DSC POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# Feature powerwell dependencies for RocketLake
# Audio -> PG3->PG1
RklFeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG3': 1}),
    # PIPE_A DSC POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1})
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
NonComboPhyPorts = []
TglNonComboPhyPorts = ['D', 'E', 'F', 'G', 'H', 'I']
LkfRNonComboPhyPorts = ['C', 'D', 'E', 'F', 'G', 'H', 'I']
