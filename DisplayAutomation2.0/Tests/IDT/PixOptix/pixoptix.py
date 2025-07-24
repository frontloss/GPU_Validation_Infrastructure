#######################################################################################################################
# @file         pixoptix.py
# @brief        APIs to enable, disable and verify pixoptix
#
# @author       Ravichandran M
#######################################################################################################################

import ctypes
import logging
from Libs.Core import etl_parser
from Libs.Core.logger import gdhm, html
from Tests.PowerCons.Modules import dpcd
from Tests.PowerCons.Modules.dut_context import Adapter, Panel
from Libs.Core.vbt import vbt
from Libs.Core.wrapper import control_api_args, control_api_wrapper


##
# @brief        Exposed API to verify PixOptix
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @param[in]    etl_file String
# @param[in]    negative Boolean - True if PixOptix should not work, False otherwise
# @return       True if operation is successful, False otherwise


def verify(adapter: Adapter, panel: Panel, etl_file: str, negative=False):
    dpcd_data = None
    etl_parser_config = etl_parser.EtlParserConfig()
    etl_parser_config.dpcdData = 1
    if etl_parser.generate_report(etl_file, etl_parser_config) is False:
        logging.error(f"\tFAILED to generate EtlParser report {etl_file}")
        return False
    logging.info(f"\tSuccessfully generated EtlParser report for {etl_file}")

    # PixOptix DPCD verification from ETL.
    dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.EDP_BRIGHTNESS_OPTIMIZATION, is_write=True)
    if dpcd_data is None:
        if negative is True:
            logging.debug("\tNo PixOptix DPCD programming found which is expected in negative case")
            return True
        logging.error("\tNo PixOptix DPCD programming found which is not expected")
        gdhm.report_driver_bug_pc("[PowerCons][IDT-PixOptix] No PixOptix DPCD programming found which is not expected")
        return False

    if negative is True:
        logging.error("\tPixOptix DPCD programming found which is not expected in negative case")
        return False

    status_val = True
    logging.info("Starting PixOptix DPCD verification...")
    logging.info(f"\tDPCD Address: {hex(int(dpcd_data[-1].Address))}= {dpcd_data[-1].Data} at "
                 f"{dpcd_data[-1].TimeStamp} ms")

    # Convert from byte to little indian uint8
    b = bytearray.fromhex(dpcd_data[-1].Data.replace('-', ''))
    dpcd_val = int.from_bytes(b, byteorder='little')

    pixoptix_config_dpcd = dpcd.EdpBrightnessOptimization(panel.target_id, dpcd_val)

    if pixoptix_config_dpcd.optimization_strength == dpcd.PixOptixStatus.DISABLE and negative:
        logging.debug(f"\tPixOptix programmed to disable in DPCD for port {panel.port} on {adapter.name}")
    elif pixoptix_config_dpcd.optimization_strength == dpcd.PixOptixStatus.ENABLE:
        logging.debug(f"\tPixOptix programmed to enable PixOptix in DPCD for port {panel.port} on {adapter.name}")
    else:
        logging.error(
            f"\tMismatch seen in PixOptix programming in DPCD Status={pixoptix_config_dpcd.optimization_strength}")
        gdhm.report_driver_bug_pc("[PowerCons][IDT-PixOptix] Mismatch seen in PixOptix DPCD programming")
        status_val = False
    return status_val


##
# @brief        This function verify pixOptix status in the VBT; If enabled nothing Otherwise enables it
# @param[in]    adapter
# @param[in]    panel
# @return       True, else False if driver restart or VBT reload fails
def enable_pixoptix_in_vbt(adapter: Adapter, panel: Panel):

    html.step_start(f"Enabling PixOptix feature in VBT for {panel.port}")

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    if panel.is_lfp is False:
        logging.info("\tPanel is not LFP. Skip Vbt update")
        return True

    # Skip VBT update for unsupported VBT version
    if gfx_vbt.version < 253:
        logging.error(f"VBT version of PixOptix Expected: >253 and current:{gfx_vbt.version}")
        html.step_end()
        return False
    # Fetching the initial VBT status
    if bool((gfx_vbt.block_44.PixOptix[0] & (1 << panel_index)) >> panel_index) is True:
        logging.info("PixOptix feature already enabled in VBT")
        html.step_end()
        return None
    gfx_vbt.block_44.PixOptix[0] |= (1 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("PixOptix Feature changes failed in VBT")
        html.step_end()
        return False

    html.step_end()
    return True


##
# @brief        This function verify PixOptix status in the VBT; If enabled nothing Otherwise enables it
# @param[in]    panel
# @param[in]    adapter
# @return       True, else False if driver restart or VBT reload fails
def disable_pixoptix_in_vbt(adapter, panel):

    html.step_start(f"Disabling PixOptix feature in VBT for {panel.port}")

    gfx_vbt = vbt.Vbt(adapter.gfx_index)
    panel_index = gfx_vbt.get_lfp_panel_type(panel.port)

    if gfx_vbt.version < 253:
        logging.error(f"VBT version of PixOptix Expected: >253 and current:{gfx_vbt.version}")
        html.step_end()
        return False
    # Fetching the initial VBT status
    if bool((gfx_vbt.block_44.PixOptix[0] & (1 << panel_index)) >> panel_index) is False:
        logging.info("PixOptix feature already disabled in VBT")
        html.step_end()
        return None
    gfx_vbt.block_44.PixOptix[0] &= (0 << panel_index)

    if gfx_vbt.apply_changes() is False:
        logging.error("PixOptix Feature changes failed in VBT")
        html.step_end()
        return False

    html.step_end()
    return True


##
# @brief         Exposed API to get power caps
# @param[in]     target_id - Target_id of the display
# @return        pixoptix status if success, otherwise None
def is_enabled_in_igcl(target_id):
    html.step_start("Fetching PixOptix Status using Control API")

    pixoptix_flag = control_api_args.ctl_power_optimization_dpst_flags_v.PIXOPTIX.value
    pixoptix_args = control_api_args.ctl_power_optimization_settings_t()
    pixoptix_args.Size = ctypes.sizeof(pixoptix_args)
    pixoptix_args.PowerOptimizationFeature = pixoptix_flag
    pixoptix_args.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
    pixoptix_args.PowerSource = control_api_args.ctl_power_source_v.DC.value

    if control_api_wrapper.get_dpst(pixoptix_args, target_id) is False:
        logging.error("FAILED to get PixOptix via Control API")
        html.step_end()
        return None

    html.step_end()
    return pixoptix_flag == (pixoptix_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value & pixoptix_flag)


##
# @brief         Exposed API to set pixoptix
# @param[in]     panel object, Panel
# @param[in]     enable_status bool, to enable or disable the feature
# @return        True if Pass, otherwise False
def set_in_igcl(panel: Panel, enable_status: bool):

    html.step_start(f"Setting PixOptix status to= {enable_status} for DC Mode with BALANCED")
    logging.info(f"Requested for PixOptix Feature to set Status= {enable_status}")

    pixoptix_flag = control_api_args.ctl_power_optimization_dpst_flags_v.PIXOPTIX.value
    pixoptix_args = control_api_args.ctl_power_optimization_settings_t()
    pixoptix_args.Size = ctypes.sizeof(pixoptix_args)
    pixoptix_args.PowerOptimizationFeature = pixoptix_flag
    pixoptix_args.PowerOptimizationPlan = control_api_args.ctl_power_optimization_plan_v.BALANCED.value
    pixoptix_args.PowerSource = control_api_args.ctl_power_source_v.DC.value

    if control_api_wrapper.get_dpst(pixoptix_args, panel.target_id) is False:
        logging.error("\tFAILED to Get PixOptix via Control Library")
        html.step_end()
        return False

    pixoptix_flag = control_api_args.ctl_power_optimization_dpst_flags_v.PIXOPTIX.value

    current_status = (pixoptix_flag == (pixoptix_flag & pixoptix_args.FeatureSpecificData.
                                        DPSTInfo.EnabledFeatures.value))

    if enable_status == current_status:
        logging.info(f"Requested setting is already set PixOptix Status= {current_status}")
        html.step_end()
        return True

    pixoptix_args.Enable = enable_status
    pixoptix_args.FeatureSpecificData.DPSTInfo.EnabledFeatures.value |= pixoptix_flag
    logging.info(f"\t{'Enabling' if enable_status else 'Disabling'} pixoptix feature")

    if control_api_wrapper.set_dpst(pixoptix_args, panel.target_id) is False:
        logging.error(f"\tFAILED to {'Enable' if enable_status else 'Disable'} PixOptix feature via Control API")
        html.step_end()
        return False

    logging.info(f"\tSuccessfully {'Enabled' if enable_status else 'Disabled'} PixOptix feature via Control API")

    logging.info(f"\tValidating that PixOptix feature is {'Enabled' if enable_status else 'Disabled'}")

    pixoptix_status = is_enabled_in_igcl(panel.target_id)

    if pixoptix_status is None:
        logging.error(f"\tFAILED to get status of PixOptix feature")
        html.step_end()
        return False

    is_status_correct = False

    if pixoptix_status == enable_status:
        logging.info(f"\tPixOptix feature is {'Enabled' if enable_status else 'Disabled'}")
        is_status_correct = True
    else:
        logging.error(f"\tPixOptix feature is NOT {'Enabled' if enable_status else 'Disabled'}")

    html.step_end()
    return is_status_correct
