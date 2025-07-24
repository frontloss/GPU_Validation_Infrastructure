########################################################################################################################
# @file         gen9_powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Gen9 specific module for Display Power well verification
# @description  @ref gen9_powerwell.py contains Gen9 powerwell dependencies
#
# @author       Rohit Kumar
########################################################################################################################
import ctypes

from Libs.Feature.display_powerwell import common

##
# Below masked are used to indicate which powerwell are available on give platform. It's a 32-bit mask. Each bit
# represents one powerwell from DisplayPowerWellMask structure. 1 means powerwell is available in the platform 0
# otherwise.
ENABLED_POWER_WELL_MASK_SKL = 0x1F00023


##
# @brief        DisplayPowerWell for Gen9 platforms
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
            self.PowerwellDdiAIo = powerwell_ctl.ddi_a_and_ddi_e_io_power_state
            self.PowerwellDdiBIo = powerwell_ctl.ddi_b_io_power_state
            self.PowerwellDdiCIo = powerwell_ctl.ddi_c_io_power_state
            self.PowerwellDdiDIo = powerwell_ctl.ddi_d_io_power_state
            ##
            # @note In legacy driver, Aux A is always kept as ON even if EDP_A is not active. Need to fix this from
            # driver side.
            # self.PowerwellAuxAIo = powerwell_ctl.misc_io_power_state


enabled_power_well_mask = DisplayPowerWell()
enabled_power_well_mask.value = ENABLED_POWER_WELL_MASK_SKL

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
# DDI_D IO -> PG2->PG1
# DDI_E IO -> PG2->PG1
DdiPowerWellMask = [
    # DD_PORT_TYPE_DIGITAL_PORT_A
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_B
    DisplayPowerWell({'PowerwellDdiBIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_C
    DisplayPowerWell({'PowerwellDdiCIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_D
    DisplayPowerWell({'PowerwellDdiDIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # DD_PORT_TYPE_DIGITAL_PORT_E
    DisplayPowerWell({'PowerwellDdiAIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]

##
# AUX powerwell dependencies
# AUX_A IO -> PG1
# AUX_E IO -> PG2->PG1
# @note     Gen9 PWR_WELL_CTL register has a single bit indicating Misc IO power state which contains all AUX, hence
#           considering PowerwellAuxAIo as MiscIO
AuxPowerWellMask = [
    # AUX_CHANNEL_A
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
    # AUX_CHANNEL_B
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_C
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_D
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1, 'PowerwellPG2': 1}),
    # AUX_CHANNEL_E
    DisplayPowerWell({'PowerwellAuxAIo': 1, 'PowerwellPG1': 1}),
]

##
# Feature powerwell dependencies
# Audio ->  PG2->PG1
FeaturePowerWellMask = [
    # AUDIO_POWERWELL
    DisplayPowerWell({'PowerwellPG1': 1, 'PowerwellPG2': 1}),
]
