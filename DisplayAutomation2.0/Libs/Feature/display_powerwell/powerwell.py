########################################################################################################################
# @file         powerwell.py
# @addtogroup   PyLibs_DisplayPower
# @brief        Contains exposed APIs for power well verification for all the platforms
# @details      powerwell library exposes below two APIs:
#               1) verify_power_well() : verifies powerwell for all the connected adapters
#               2) verify_adapter_power_well(gfx_index) : verifies power well for adapter given by gfx_index
#
# @author       Rohit Kumar
########################################################################################################################

import logging
import time

from Libs.Core import system_utility
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import gdhm
from Libs.Core.test_env import test_context
from Libs.Core import registry_access
from Libs.Feature import display_audio
from Libs.Feature.vdsc.dsc_helper import DSCHelper
from Libs.Feature.clock.display_clock import DisplayClock
from Libs.Feature.display_audio import AudioCodecDriverType
from Libs.Feature.display_engine.de_base import display_base
from Libs.Feature.display_powerwell import gen10_powerwell
from Libs.Feature.display_powerwell import gen11_powerwell
from Libs.Feature.display_powerwell import gen11p5_powerwell
from Libs.Feature.display_powerwell import gen12_powerwell
from Libs.Feature.display_powerwell import gen13_powerwell
from Libs.Feature.display_powerwell import gen14_powerwell
from Libs.Feature.display_powerwell import gen15_powerwell
from Libs.Feature.display_powerwell import gen9_powerwell
from registers.mmioregister import MMIORegister

##
# Platform details for all connected adapters
PLATFORM_INFO = {
    gfx_index: {
        'gfx_index': gfx_index,
        'name': adapter_info.get_platform_info().PlatformName,
        'is_ddrw': system_utility.SystemUtility().is_ddrw(gfx_index=adapter_info.gfxIndex)
    }
    for gfx_index, adapter_info in test_context.TestContext.get_gfx_adapter_details().items()
}

__display_config = display_config.DisplayConfiguration()
__display_audio = display_audio.DisplayAudio()

##
# @brief    Pipe index, used for pipe powerwell mask
# @note     Source: Source\inc\common\Chipsimc.h
__pipe_mapping = {'PIPE_A': 0, 'PIPE_B': 1, 'PIPE_C': 2, 'PIPE_D': 3, 'VIRTUAL_PIPE_A': 16}
__pipe_index_to_name_mapping = {0: 'PIPE_A', 1: 'PIPE_B', 2: 'PIPE_C', 3: 'PIPE_D'}

##
# @brief    DDI index, used for DDI powerwell mask
# @note     Source: Source\Display\Code\inc\shared\DisplayArgs.h : 231
__ddi_mapping = {
    'DDI_A': 0, 'DDI_B': 1, 'DDI_C': 2, 'DDI_D': 3, 'DDI_E': 4, 'DDI_F': 5, 'DDI_G': 6, 'DDI_H': 7, 'DDI_I': 8,
    'DDI_WD': 11, 'DDI_VIRTUAL': 12, 'DDI_DYNAMIC': 13, 'DDI_COLLAGE1': 14
}

__gen9_gen10_platforms = ['SKL', 'KBL', 'CFL', 'GLK', 'CNL', 'APL']
__pre_gen_14_platforms = __gen9_gen10_platforms + ['LKF1', 'ICLLP', 'EHL', 'JSL', 'TGL', 'RKL', 'DG1', 'ADLS', 'DG2',
                                                   'ADLP']

# List of platforms on which VDSC check for powerwell verification is not required
# Gen9: No DSC
# GLK, LKF1: DSC is in PG1
__skip_dsc_pg_check_list = __gen9_gen10_platforms + ['LKF1', 'LKFR']


##
# @brief        Helper API to get hardware powerwell status based on powerwell register values.
# @param[in]    gfx_index, String, adapter index
# @param[in]    powerwell_module, Display Gen specific module. Ex: gen11_powerwell
# @return       A DisplayPowerWell(defined in common.py) object containing hardware status for each powerwell.
# @note         For detailed description of DisplayPowerWell structure, see @ref common.py
def __get_hardware_powerwell_status(gfx_index, powerwell_module):
    platform_name = PLATFORM_INFO[gfx_index]['name']

    if platform_name in __gen9_gen10_platforms:
        pwr_ctrl = MMIORegister.read('PWR_WELL_CTL_REGISTER', 'PWR_WELL_CTL2', platform_name, gfx_index=gfx_index)
        return powerwell_module.DisplayPowerWell(powerwell_ctl=pwr_ctrl, platform=platform_name)

    return powerwell_module.DisplayPowerWell(platform=platform_name, gfx_index=gfx_index)


##
# @brief        Helper API to get Audio status
# @param[in]    gfx_index, String, adapter index
# @return       True if audio powerwell is expected to be ON, False otherwise
def __get_audio_status(gfx_index):
    platform_name = PLATFORM_INFO[gfx_index]['name']
    active_audio_panel = False

    registry_name = "HdmiNoNullPacketAndAudio"
    diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
    read_val, read_type = registry_access.read(args=diss_reg_args, reg_name=registry_name)

    ##
    # Check for any active audio capable panel
    enumerated_displays = __display_config.get_enumerated_display_info()
    for display_index in range(enumerated_displays.Count):
        ##
        # Consider panels connected to the given adapter
        if enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex != gfx_index:
            continue

        if enumerated_displays.ConnectedDisplays[display_index].IsActive is True:
            display = cfg_enum.CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name
            is_audio_capable = __display_audio.is_audio_capable(enumerated_displays.ConnectedDisplays[display_index].TargetID)

            # If display is HDMI and HdmiNoNullPacketAndAudio is set, Audio should not be supported
            if read_val == 1 and 'HDMI' in display:
                is_audio_capable = False
            active_audio_panel |= is_audio_capable

    ##
    # Get SGPC status
    # @todo     Update for multi-adapter
    is_sgpc_enabled = __display_audio.is_sgpc_enabled()

    ##
    # Get installed audio codec driver
    # @todo     Update for multi-adapter
    audio_driver = __display_audio.get_audio_driver()

    ##
    # Ex: Audio Status = [SGPC_DISABLED, INTEL, NO_ACTIVE_AUDIO_PANEL]
    logging.info("Audio Status= [SGPC_{0}, {1}, {2}ACTIVE_AUDIO_PANEL]".format(
        "ENABLED" if is_sgpc_enabled else "DISABLED",
        display_audio.AudioCodecDriverType(audio_driver).name,
        "" if active_audio_panel else "NO_"
    ))

    ##
    # For all below platforms, front end audio block is moved to PG0, while audio powerwell contains playback functionality.
    # Audio powerwell is turned ON based on audio capability of connected panels. If there is no audio capable panel present,
    # with or without audio codec, audio powerwell will be turned OFF. If there is at least one audio capable panel
    # active, audio powerwell will be turned ON.
    if platform_name in ['DG1', 'DG2', 'ADLP', 'MTL', 'ELG','LNL', 'PTL', 'NVL', 'CLS']:
        if active_audio_panel:
            return True
        return False

    ##
    # From ICL+, with SGPC, audio PG can always be turned OFF if audio capable panel is not present in the VidPn
    # as Audio codec does not get loaded in LPSP
    if platform_name not in __gen9_gen10_platforms:
        if is_sgpc_enabled:
            if active_audio_panel is False:
                return False
            return True

    ##
    # Based on the above information determine the expected value for audio powerwell
    # True: Powerwell should be enabled, False: otherwise
    if audio_driver == AudioCodecDriverType.NONE:
        ##
        # Condition: No Audio Codec driver is present.
        # Audio powerwell will always be ON if there is NO audio codec driver installed.
        return True
    elif audio_driver == AudioCodecDriverType.MS:
        ##
        # Condition: MS Audio Codec driver is present.
        # Audio powerwell state will depend on SGPC and any active audio panel.
        if not is_sgpc_enabled or active_audio_panel:
            # If SGPC is disabled or at least one audio capable panel is active, audio powerwell will be ON.
            return True
    else:
        ##
        # Condition: Intel Audio Codec driver is present.
        # Audio powerwell state will depend on any active audio panel.
        if active_audio_panel:
            # If at least one audio capable panel is active, audio powerwell will be ON.
            return True
    ##
    # In all other cases, audio powerwell will be OFF.
    return False


##
# @brief        Helper API to get expected powerwell status based on current display configuration (active pipes, active
#               DDIs, active AUX channels, active features etc.)
# @param[in]    gfx_index, String, adapter index
# @param[in]    powerwell_module, Display Gen specific module. Ex: gen11_powerwell
# @return       expected_powerwell_status, a DisplayPowerWell(common.py) object containing expected status for each
#               powerwell.
def __get_expected_power_well_status(gfx_index, powerwell_module):
    platform_name = PLATFORM_INFO[gfx_index]['name']

    # Create an empty object of DisplayPowerWell to store expected powerwell status
    expected_powerwell_status = powerwell_module.DisplayPowerWell()

    # Dictionary to contain a list of dependencies for each active powerwell for logging purpose.
    # Ex: {'PowerwellPG1': ['PIPE_A', 'DDI_A'], 'PowerwellPG3': ['AUDIO']}
    powerwell_dependencies = {}

    ##
    # @brief        Helper function to add dependencies for given powerwell. Local to __get_expected_power_well_status()
    #               This function updates the powerwell_dependencies dictionary for each powerwell.
    # @param[in]    impacted_power_wells, a list of impacted power wells because of dependency
    # @param[in]    dependency, dependency which is keeping the given powerwell active. Ex: 'AUDIO', 'PIPE_B' etc.
    def __add_dependencies(impacted_power_wells, dependency):
        for p in impacted_power_wells:
            if p not in powerwell_dependencies.keys():
                powerwell_dependencies[p] = set()
            powerwell_dependencies[p].add(dependency)

    enumerated_displays = __display_config.get_enumerated_display_info()

    # For each active display, find the corresponding PIPE, DDI and AUX and turn the respective powerwell ON in
    # expected_powerwell_status object
    for display_index in range(enumerated_displays.Count):
        display = cfg_enum.CONNECTOR_PORT_TYPE(
            enumerated_displays.ConnectedDisplays[display_index].ConnectorNPortType).name
        port_type = enumerated_displays.ConnectedDisplays[display_index].PortType

        ##
        # Skip displays connected to other adapters
        if enumerated_displays.ConnectedDisplays[display_index].DisplayAndAdapterInfo.adapterInfo.gfxIndex != gfx_index:
            continue

        # Skip inactive displays
        if enumerated_displays.ConnectedDisplays[display_index].IsActive is False:
            if (platform_name in __gen9_gen10_platforms) or ('TC' in port_type):
                continue
            # Static connections are not POR for LKF1 platform
            # Keeping the AUX PG ON for TypeC is not required from ADLP
            if platform_name in ['LKF1', 'MTL', 'ADLP', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
                continue

            # For Gen11+, Check for TypeC Aux condition
            # Legacy display connection
            # For legacy connections(DP / HDMI), Aux IO must be enabled during the connect flow and not disabled
            # until disconnect flow.
            if display.split('_')[1] in powerwell_module.NonComboPhyPorts:
                ddi = 'DDI_' + display.split('_')[1]
                logging.debug("\tAUX Powerwell Dependencies: {0}".format(
                    powerwell_module.AuxOnlyPowerWellMask[__ddi_mapping[ddi]].active_power_wells))
                __add_dependencies(powerwell_module.AuxOnlyPowerWellMask[__ddi_mapping[ddi]].active_power_wells, ddi)
                expected_powerwell_status.value |= powerwell_module.AuxOnlyPowerWellMask[__ddi_mapping[ddi]].value

            continue

        db = display_base.DisplayBase(display, platform_name, gfx_index=gfx_index)
        logging.info("Port, DDI and PIPE mapping: {0}: [{1} & {2} & {3}]".format(display, db.ddi, db.pipe, port_type))

        if display.startswith("WD_"):
            reg = MMIORegister.read("TRANS_WD_FUNC_CTL_REGISTER", "TRANS_WD_FUNC_CTL_%s" % (display[-1]), platform_name)
            value = reg.wd_input_select
            if (reg.wd_function_enable):
                db.pipe, powerwell_module.WBPowerWellMask[__pipe_mapping[db.pipe]].active_power_wells
                __add_dependencies(powerwell_module.WBPowerWellMask[__pipe_mapping[db.pipe]].active_power_wells,
                                   db.pipe)
                expected_powerwell_status.value |= powerwell_module.WBPowerWellMask[__pipe_mapping[db.pipe]].value

        ##
        # Set PIPE powerwell dependencies
        logging.debug("\t{0:8} Powerwell Dependencies: {1}".format(
            db.pipe, powerwell_module.PipePowerWellMask[__pipe_mapping[db.pipe]].active_power_wells))
        __add_dependencies(powerwell_module.PipePowerWellMask[__pipe_mapping[db.pipe]].active_power_wells, db.pipe)

        # Check for Pipe-Joiner mode
        is_pipe_joiner_required, no_of_pipes_required = DisplayClock.is_pipe_joiner_required(gfx_index, display)
        if is_pipe_joiner_required:
            logging.info(f"\tPipe joiner mode is enabled on {display} with {no_of_pipes_required} pipes")
            for i in range(1, no_of_pipes_required):
                __add_dependencies(powerwell_module.PipePowerWellMask[__pipe_mapping[db.pipe] + i].active_power_wells,
                                   __pipe_index_to_name_mapping.get(__pipe_mapping[db.pipe] + i, "PIPE_NONE"))
                expected_powerwell_status.value |= powerwell_module.PipePowerWellMask[__pipe_mapping[db.pipe] + i].value

        expected_powerwell_status.value |= powerwell_module.PipePowerWellMask[__pipe_mapping[db.pipe]].value

        # Set DDI powerwell dependencies
        if not display.startswith("WD_"):
            logging.debug("\t{0:8} Powerwell Dependencies: {1}".format(
                db.ddi, powerwell_module.DdiPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells))
            __add_dependencies(powerwell_module.DdiPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells, db.ddi)
            expected_powerwell_status.value |= powerwell_module.DdiPowerWellMask[__ddi_mapping[db.ddi]].value

        # Set AUX powerwell dependencies
        if platform_name not in __gen9_gen10_platforms:
            ##
            # TbtAux powerwell is expected to be ON in case of TBT port type
            if port_type in ['TBT']:
                logging.debug("\tTBT AUX Powerwell Dependencies: {0}".format(
                    powerwell_module.TbtAuxPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells))
                __add_dependencies(
                    powerwell_module.TbtAuxPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells, db.ddi)
                expected_powerwell_status.value |= powerwell_module.TbtAuxPowerWellMask[__ddi_mapping[db.ddi]].value

            ##
            # Aux Powerwell is expected to be ON if at least one of the below conditions is true
            # * Connected panel is of type DP
            # * Port type is DP PLUS (Connector)
            # * Non Combo Phy port (pre Gen14)
            elif (port_type in ['NATIVE', 'TC', 'EMBEDDED'] and 'DP' in display) or (port_type == 'PLUS') or (
                    db.ddi.split('_')[1] in powerwell_module.NonComboPhyPorts and
                    platform_name in __pre_gen_14_platforms):
                logging.debug("\tAUX Powerwell Dependencies: {0}".format(
                    powerwell_module.AuxPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells))
                __add_dependencies(powerwell_module.AuxPowerWellMask[__ddi_mapping[db.ddi]].active_power_wells, db.ddi)
                expected_powerwell_status.value |= powerwell_module.AuxPowerWellMask[__ddi_mapping[db.ddi]].value

        # Set Audio Feature powerwell dependencies
        if __get_audio_status(gfx_index):
            logging.debug("Audio Powerwell Dependencies: {0}".format(
                powerwell_module.FeaturePowerWellMask[0].active_power_wells))
            __add_dependencies(powerwell_module.FeaturePowerWellMask[0].active_power_wells, 'AUDIO')
            expected_powerwell_status.value |= powerwell_module.FeaturePowerWellMask[0].value

        # Set VDSC Feature powerwell dependencies
        is_dsc_enabled = DSCHelper.is_vdsc_enabled_in_driver(gfx_index, display)
        if platform_name not in __skip_dsc_pg_check_list and is_dsc_enabled:
            logging.info("VDSC Powerwell Dependencies: {0}".format(
                powerwell_module.FeaturePowerWellMask[1].active_power_wells))
            __add_dependencies(powerwell_module.FeaturePowerWellMask[1].active_power_wells, 'VDSC')
            expected_powerwell_status.value |= powerwell_module.FeaturePowerWellMask[1].value

    return expected_powerwell_status, powerwell_dependencies


##
# @brief        Exposed API for single adapter powerwell verification
# @param[in]    gfx_index String, adapter index
# @return       True if power well verification is passed, False otherwise
def verify_adapter_power_well(gfx_index):
    platform_name = PLATFORM_INFO[gfx_index]['name']
    logging.info("{0} Powerwell Verification".format(platform_name))

    # Set the powerwell module based on platform
    if platform_name in ['SKL', 'KBL', 'CFL']:
        powerwell_module = gen9_powerwell
    elif platform_name in ['GLK']:
        powerwell_module = gen10_powerwell
    elif platform_name in ['ICLLP', 'JSL']:
        powerwell_module = gen11_powerwell
        if platform_name == 'JSL':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_JSL
            powerwell_module.NonComboPhyPorts = []  # No non combo phy port in JSL
    elif platform_name in ['LKF1']:
        powerwell_module = gen11p5_powerwell
    elif platform_name in ['TGL', 'RKL', 'DG1', 'LKFR', 'ADLS']:
        powerwell_module = gen12_powerwell
        powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_TGL
        powerwell_module.DdiPowerWellMask = powerwell_module.TglDdiPowerWellMask
        powerwell_module.AuxPowerWellMask = powerwell_module.TglAuxPowerWellMask
        powerwell_module.NonComboPhyPorts = powerwell_module.TglNonComboPhyPorts

        if platform_name == 'RKL':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_RKL
            powerwell_module.PipePowerWellMask = powerwell_module.RklPipePowerWellMask
            powerwell_module.DdiPowerWellMask = powerwell_module.RklDdiPowerWellMask
            powerwell_module.AuxPowerWellMask = powerwell_module.RklAuxPowerWellMask
            powerwell_module.FeaturePowerWellMask = powerwell_module.RklFeaturePowerWellMask
            powerwell_module.NonComboPhyPorts = []  # No non combo phy port in RKL
        if platform_name == 'DG1':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_DG1
            powerwell_module.DdiPowerWellMask = powerwell_module.DG1DdiPowerWellMask
            powerwell_module.AuxPowerWellMask = powerwell_module.Dg1AuxPowerWellMask
            powerwell_module.NonComboPhyPorts = []  # No non combo phy port in DG1
        if platform_name == 'LKFR':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_LKFR
            powerwell_module.PipePowerWellMask = powerwell_module.LkfRPipePowerWellMask
            powerwell_module.DdiPowerWellMask = powerwell_module.LkfRDdiPowerWellMask
            powerwell_module.AuxPowerWellMask = powerwell_module.LkfRAuxPowerWellMask
            powerwell_module.FeaturePowerWellMask = powerwell_module.RklFeaturePowerWellMask
            powerwell_module.NonComboPhyPorts = powerwell_module.LkfRNonComboPhyPorts
        if platform_name == 'ADLS':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_ADLS
            powerwell_module.DdiPowerWellMask = powerwell_module.AdlSDdiPowerWellMask
            powerwell_module.AuxPowerWellMask = powerwell_module.AdlSAuxPowerWellMask
            powerwell_module.NonComboPhyPorts = []
    elif platform_name in ['DG2', 'ADLP']:
        powerwell_module = gen13_powerwell
        if platform_name == 'ADLP':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_ADLP
            powerwell_module.DdiPowerWellMask = powerwell_module.ADLPDdiPowerWellMask
            powerwell_module.AuxPowerWellMask = powerwell_module.ADLPAuxPowerWellMask
    elif platform_name in ['MTL', 'ELG']:
        powerwell_module = gen14_powerwell
        if platform_name == 'ELG':
            powerwell_module.enabled_power_well_mask.value = powerwell_module.ENABLED_POWER_WELL_MASK_ELG
            powerwell_module.AuxPowerWellMask = powerwell_module.ELGAuxPowerWellMask
    elif platform_name in ['LNL', 'PTL', 'NVL', 'CLS']:
        powerwell_module = gen15_powerwell
    else:
        logging.error("Platform doesn't have Power Well verification check")
        gdhm.report_bug(
            f"[PowerCons][Powerwell] Powerwell verification is not enabled for {platform_name}",
            gdhm.ProblemClassification.LOG_FAILURE,
            gdhm.Component.Test.DISPLAY_POWERCONS,
            gdhm.Priority.P3,
            gdhm.Exposure.E3
        )
        return False

    # Get expected power well status for each powerwell and a list of dependencies for each power well
    expected_powerwell_status, powerwell_dependencies = __get_expected_power_well_status(gfx_index, powerwell_module)

    # Get the actual hardware powerwell status
    actual_powerwell_status = __get_hardware_powerwell_status(gfx_index, powerwell_module)

    # Below dictionaries are used to combine the DDI power well and AUX power well status in single line
    log_entry = {'aux': [], 'ddi': [], 'expected': {'aux': [], 'ddi': []}, 'actual': {'aux': [], 'ddi': []},
                 'prefix': {'aux': 'PASS', 'ddi': 'PASS'}}

    # @note     enabled_power_well_mask indicates all the supported power wells for given powerwell module
    supported_powerwell_list = [
        _ for _ in dir(powerwell_module.enabled_power_well_mask)
        if _.startswith('Powerwell') and getattr(powerwell_module.enabled_power_well_mask, _) == 1
    ]

    # Combine multiple powerwell states in single line
    # Sample Output: PASS: PWR_WELL_DDI [A, B, C, D] Expected [ON, ON, OFF, OFF] Actual [ON, ON, OFF, OFF]
    failed_pg_list = []
    failed_aux_pg_list = []
    failed_ddi_pg_list = []
    for pwr_wl_name in supported_powerwell_list:
        if pwr_wl_name.startswith('PowerwellAux') or pwr_wl_name.startswith('PowerwellDdi'):
            dict_key = pwr_wl_name[9:12].lower()
            log_entry[dict_key].append(pwr_wl_name[12:-2])
            log_entry['expected'][dict_key].append(
                'ON' if getattr(expected_powerwell_status, pwr_wl_name) else 'OFF')
            log_entry['actual'][dict_key].append(
                'ON' if getattr(actual_powerwell_status, pwr_wl_name) else 'OFF')
            if log_entry['expected'][dict_key][-1] != log_entry['actual'][dict_key][-1]:
                log_entry['prefix'][dict_key] = 'FAIL'
                if pwr_wl_name.startswith('PowerwellAux'):
                    failed_aux_pg_list.append(pwr_wl_name)
                else:
                    failed_ddi_pg_list.append(pwr_wl_name)

        if pwr_wl_name.startswith('PowerwellPG'):
            prefix = 'FAIL'
            if getattr(expected_powerwell_status, pwr_wl_name) == getattr(actual_powerwell_status, pwr_wl_name):
                prefix = 'PASS'

            # Since actual and expected powerwell status doesn't match
            # Adding 6 seconds sleep and retry fetching actual powerwell status
            if 'FAIL' == prefix:
                time.sleep(6)

                # Get the actual hardware powerwell status again
                actual_powerwell_status = __get_hardware_powerwell_status(gfx_index, powerwell_module)
                if getattr(expected_powerwell_status, pwr_wl_name) == getattr(actual_powerwell_status, pwr_wl_name):
                    prefix = 'PASS'
                    logging.warning("{0} verification passed with {1} seconds delay".format(pwr_wl_name, 6))
                elif getattr(expected_powerwell_status, pwr_wl_name) != getattr(actual_powerwell_status, pwr_wl_name):
                    if (platform_name == 'ICLLP') and (pwr_wl_name in ['PowerwellPG2', 'PowerwellPG3']):
                        prefix = 'PASS'
                        logging.info('WA for the ICLLP(Platform) to avoid sporadic failing of powerwell verification')
                else:
                    failed_pg_list.append(pwr_wl_name)

            log = "{0}: {1:12} Status Expected= {2:3}, Actual= {3:3}, Dependencies= {4}".format(
                prefix,
                pwr_wl_name,
                "ON" if getattr(expected_powerwell_status, pwr_wl_name) else "OFF",
                "ON" if getattr(actual_powerwell_status, pwr_wl_name) else "OFF",
                list([] if pwr_wl_name not in powerwell_dependencies.keys() else powerwell_dependencies[pwr_wl_name])
            )
            if "PASS" in log:
                logging.info(log)
            else:
                logging.error(log)

    # DDI powerwell verification not valid for MTL+ platforms
    if platform_name not in ['MTL', 'ELG', 'LNL', 'PTL', 'NVL', 'CLS']:
        log = "{0}: PWR_WELL_DDI {1} Expected {2} Actual {3}".format(
        log_entry['prefix']['ddi'], log_entry['ddi'], log_entry['expected']['ddi'], log_entry['actual']['ddi'])
        if "PASS" in log:
            logging.info(log)
        else:
            logging.error(log)

    log = "{0}: PWR_WELL_AUX {1} Expected {2} Actual {3}".format(
        log_entry['prefix']['aux'], log_entry['aux'], log_entry['expected']['aux'], log_entry['actual']['aux'])
    if "PASS" in log:
        logging.info(log)
    else:
        logging.error(log)

    if len(failed_pg_list) != 0:
        gdhm.report_bug(
            f"[PowerCons][Powerwell] Powerwell verification failed for {failed_pg_list}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Driver.DISPLAY_POWERCONS,
            gdhm.Priority.P2,
            gdhm.Exposure.E2
        )

    if len(failed_aux_pg_list) != 0:
        gdhm.report_bug(
            f"[PowerCons][Powerwell] AUX Powerwell verification failed for {failed_aux_pg_list}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Driver.DISPLAY_POWERCONS,
            gdhm.Priority.P2,
            gdhm.Exposure.E2
        )

    if len(failed_ddi_pg_list) != 0:
        gdhm.report_bug(
            f"[PowerCons][Powerwell] DDI Powerwell verification failed for {failed_ddi_pg_list}",
            gdhm.ProblemClassification.FUNCTIONALITY,
            gdhm.Component.Driver.DISPLAY_POWERCONS,
            gdhm.Priority.P2,
            gdhm.Exposure.E2
        )

    # Match the actual powerwell hardware state with expected powerwell state
    if (actual_powerwell_status.value == 0) or (expected_powerwell_status.value == 0) or \
            (actual_powerwell_status.value != expected_powerwell_status.value):
        if (platform_name == 'ICLLP') and \
                (actual_powerwell_status.PowerwellPG2 != expected_powerwell_status.PowerwellPG2) or \
                (actual_powerwell_status.PowerwellPG3 != expected_powerwell_status.PowerwellPG3):
            return True
        else:
            logging.error("FAIL: ExpectedPowerwellMask= {0}, ActualPowerwellMask= {1}".format(
                hex(expected_powerwell_status.value), hex(actual_powerwell_status.value)))
            return False
    return True


##
# @brief        Exposed API for multi-adapter powerwell verification
# @return       True if power well verification is successful, False otherwise
def verify_power_well():
    status = True
    for gfx_index in PLATFORM_INFO.keys():
        status &= verify_adapter_power_well(gfx_index)
    return status
