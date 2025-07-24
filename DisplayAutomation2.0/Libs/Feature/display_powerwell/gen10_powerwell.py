######################################################################################
# @file         gen10_powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Gen10 specific module for Display Power well verification
# @description  @ref gen10_powerwell.py contains Gen10 powerwell dependencies
#
# @note         In legacy platforms, Aux powerwells are turned on only at the time of Aux transactions. Currently we are
#               not verifying aux powerwell programming.
# @author       Rohit Kumar
######################################################################################
import ctypes

from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 32-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
# GLK mask changed from 0x3F00023 to 0x3D00023. Removing DdiBIo from powerwell check as a part of HSD-1607334918
ENABLED_POWER_WELL_MASK_GLK = 0x3D00023


##
# @brief        DisplayPowerWell for Gen10 platforms
class DisplayPowerWell(ctypes.Union):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u", common.DisplayPowerWellMask),
        ("value", ctypes.c_uint64)
    ]

    ##
    # @brief        DisplayPowerWell default __init__ function
    # @param[in]    mask[optional], A dictionary indicating powerwell status separately (Ex: {'PowerwellPG1':1})
    # @param[in]    powerwell_ctl[optional], PWR_WELL_CTL register instance
    # @param[in]    powerwell_ctl_aux[optional], PWR_WELL_CTL_AUX register instance
    # @param[in]    powerwell_ctl_ddi[optional], PWR_WELL_CTL_DDI register instance
    # @param[in]    platform[optional], platform name
    def __init__(self, mask=None, powerwell_ctl=None, powerwell_ctl_aux=None, powerwell_ctl_ddi=None, platform=None):
        super(DisplayPowerWell, self).__init__()
        self.value = 0
        self.active_power_wells = []

        if mask is not None:
            if 'value' not in mask.keys():
                self.active_power_wells = mask.keys()
                for key, value in mask.items():
                    setattr(self, key, value)

        if powerwell_ctl is not None and powerwell_ctl.asUint != 0:
            self.PowerwellPG1 = powerwell_ctl.power_well_1_state
            self.PowerwellPG2 = powerwell_ctl.power_well_2_state
            self.PowerwellDdiAIo = powerwell_ctl.ddi_a_io_power_state
            self.PowerwellDdiBIo = powerwell_ctl.ddi_b_io_power_state
            self.PowerwellDdiCIo = powerwell_ctl.ddi_c_io_power_state
            ##
            # @note In legacy driver, Aux A is always kept as ON even if EDP_A is not active. Need to fix this from
            # driver side.
            # self.PowerwellAuxAIo = powerwell_ctl.aux_a_io_power_state


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_GLK

##
# Pipe powerwell dependencies
# Pipe A -> PG1
# Pipe B -> PG2->PG1
# Pipe C -> PG2->PG1
PipePowerWellMask = [
    # PIPE_A
    DisplayPowerWell({'PowerwellPG1': 1}),
    # PIPE_B
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # PIPE_C
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1})
]

##
# DDI powerwell dependencies
# DDI_A IO -> PG1
# DDI_B IO -> PG2->PG1
# DDI_C IO -> PG2->PG1
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# AUX powerwell dependencies
# AUX_A IO -> PG1
# AUX_B IO -> PG2->PG1
# AUX_C IO -> PG2->PG1
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'value': 0}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'value': 0}),
]

##
# Feature powerwell dependencies
# Audio ->  PG2->PG1
# DSC ->    PG1
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DSC_POWERWELL (eDP and MIPI DSI)
    DisplayPowerWell({'PowerwellPG1': 1})
]
