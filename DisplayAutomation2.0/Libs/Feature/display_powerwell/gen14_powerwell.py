######################################################################################
# @file         gen14_powerwell.py
# @brief        Gen14 specific module for Display Power well verification
# @author       Rohit Kumar
######################################################################################
import ctypes
import logging
from enum import Enum

from DisplayRegs import DisplayArgs
from DisplayRegs.Gen14.Ddi import Gen14DdiRegs
from DisplayRegs.Gen14.DisplayPowerHandler import Gen14DisplayPowerRegs
from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 64-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.

ENABLED_POWER_WELL_MASK_MTL = 0x1E0003C63
ENABLED_POWER_WELL_MASK_ELG = 0x1E0003C23


##
# @brief        C10_PHY_POWERDOWN_STATE for Gen14 platforms
class C10_PHY_POWERDOWN_STATE(Enum):
    ACTIVE_STATE = 0x0
    READY_STATE = 0x2
    RESET_STATE = 0x2
    DISABLE_STATE = 0x9


##
# @brief        DisplayPowerWell for Gen14 platforms
class DisplayPowerWell(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", common.DisplayPowerWellMask),
        ("value", ctypes.c_uint64)
    ]

    ##
    # @brief        DisplayPowerWell default __init__ function
    # @param[in]    mask : a dictionary indicating powerwell status separately (Ex: {'PowerwellPG1':1}) (optional)
    # @param[in]    platform : platform name (optional)
    # @param[in]    gfx_index : gfx index (optional)
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

        offset = Gen14DisplayPowerRegs.OFFSET_PWR_WELL_CTL.PWR_WELL_CTL2
        value = DisplayArgs.read_register(offset, gfx_index)
        powerwell_ctl = Gen14DisplayPowerRegs.REG_PWR_WELL_CTL(offset, value)
        self.PowerwellPG1 = powerwell_ctl.PowerWell1State
        self.PowerwellPG2 = powerwell_ctl.PowerWell2State
        self.PowerwellPGA = powerwell_ctl.PowerWellAState
        self.PowerwellPGB = powerwell_ctl.PowerWellBState
        self.PowerwellPGC = powerwell_ctl.PowerWellCState
        self.PowerwellPGD = powerwell_ctl.PowerWellDState

        offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_A
        value = DisplayArgs.read_register(offset, gfx_index)
        port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
        self.PowerwellAuxAIo = port_aux_ctl.PhyPowerRequest

        # ELG does not have Port B
        if platform in ['MTL']:
            offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_B
            value = DisplayArgs.read_register(offset, gfx_index)
            port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
            self.PowerwellAuxBIo = port_aux_ctl.PhyPowerRequest

        offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_USBC1
        value = DisplayArgs.read_register(offset, gfx_index)
        port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
        self.PowerwellAuxFIo = port_aux_ctl.PhyPowerRequest

        offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_USBC2
        value = DisplayArgs.read_register(offset, gfx_index)
        port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
        self.PowerwellAuxGIo = port_aux_ctl.PhyPowerRequest

        offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_USBC3
        value = DisplayArgs.read_register(offset, gfx_index)
        port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
        self.PowerwellAuxHIo = port_aux_ctl.PhyPowerRequest

        offset = Gen14DdiRegs.OFFSET_PORT_AUX_CTL.PORT_AUX_CTL_USBC4
        value = DisplayArgs.read_register(offset, gfx_index)
        port_aux_ctl = Gen14DdiRegs.REG_PORT_AUX_CTL(offset, value)
        self.PowerwellAuxIIo = port_aux_ctl.PhyPowerRequest

        def get_ddi_io(port_buf_ctl_reg: Gen14DdiRegs.REG_PORT_BUF_CTL2):
            # For mtl+ platforms DDI powerwell verification is not valid, hence skipping
            if platform in ['MTL', 'ELG']:
                return 0
            state = None
            if (port_buf_ctl_reg.Lane0PowerdownCurrentState == C10_PHY_POWERDOWN_STATE.READY_STATE.value) and (
                    port_buf_ctl_reg.Lane1PowerdownCurrentState == C10_PHY_POWERDOWN_STATE.READY_STATE.value):
                state = 1
            if (port_buf_ctl_reg.Lane0PowerdownCurrentState == C10_PHY_POWERDOWN_STATE.DISABLE_STATE.value) and (
                    port_buf_ctl_reg.Lane1PowerdownCurrentState == C10_PHY_POWERDOWN_STATE.DISABLE_STATE.value):
                state = 0
            if state is None:
                logging.debug(f"Invalid DDI IO State. "
                              f"Offset={hex(port_buf_ctl_reg.offset)} Value={hex(port_buf_ctl_reg.value)} "
                              f"Lane0PowerDownCurrentState={hex(port_buf_ctl_reg.Lane0PowerdownCurrentState)} "
                              f"Lane1PowerDownCurrentState={hex(port_buf_ctl_reg.Lane1PowerdownCurrentState)}")
                state = 0
            return state

        # https://gfxspecs.intel.com/Predator/Home/Index/65450
        # DDI powerwell verification is not direct in MTL+ pkatforms as in previous platforms. There is no DDI Powerwell here,
        # It is controlled by Main link IO power through Port_buf_ctl2, which is programmed by Hw. 
        # Disabled the verification for now(by disabling powerwell mask), Below values will not be verified. 
        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_A
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiAIo = get_ddi_io(port_buf_ctl)

        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_B
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiBIo = get_ddi_io(port_buf_ctl)

        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_USBC1
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiFIo = get_ddi_io(port_buf_ctl)

        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_USBC2
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiGIo = get_ddi_io(port_buf_ctl)

        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_USBC3
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiHIo = get_ddi_io(port_buf_ctl)

        offset = Gen14DdiRegs.OFFSET_PORT_BUF_CTL2.PORT_BUF_CTL2_USBC4
        value = DisplayArgs.read_register(offset, gfx_index)
        port_buf_ctl = Gen14DdiRegs.REG_PORT_BUF_CTL2(offset, value)
        self.PowerwellDdiIIo = get_ddi_io(port_buf_ctl)


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_MTL

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

# DDI powerwell dependencies
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'value': 0}),
    # DD_PORT_TYPE_DIGITAL_PORT_F
    DisplayPowerWell({'PowerwellDdiFIo': 0, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_G
    DisplayPowerWell({'PowerwellDdiGIo': 0, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_H
    DisplayPowerWell({'PowerwellDdiHIo': 0, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_I
    DisplayPowerWell({'PowerwellDdiIIo': 0, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# AUX powerwell dependencies
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxBIo': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1}),
]

##
# ELG AUX powerwell dependencies
ELGAuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_F
    DisplayPowerWell({'PowerwellAuxFIo': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1}),
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
    DisplayPowerWell({'PowerwellAuxFIo': 1}),
    # AUX_CHANNEL_G
    DisplayPowerWell({'PowerwellAuxGIo': 1}),
    # AUX_CHANNEL_H
    DisplayPowerWell({'PowerwellAuxHIo': 1}),
    # AUX_CHANNEL_I
    DisplayPowerWell({'PowerwellAuxIIo': 1}),
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
# Non-Combo PHY ports
NonComboPhyPorts = ['E', 'F', 'G', 'H', 'I']
