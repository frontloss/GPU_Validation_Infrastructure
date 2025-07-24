########################################################################################################################
# @file         pnp_id_panel_detection.py
# @brief        The file contain basic API to read and set PNP ID, and feature status
# @author       Tulika
########################################################################################################################
import logging

from Libs.Core import display_essential, driver_escape
from Libs.Core.vbt.vbt import Vbt


##
# @brief        Exposed API to compare PNP ID of eDP and VBT for given panel and index of VBT
# @param[in]    panel
# @param[in]    panel_index
# @return       True, if any pnp id match found, else None
def is_pnp_id_matching(panel, panel_index):
    if panel.is_lfp and panel.panel_type == "DP":
        panel_data_entry = Vbt(panel.gfx_index).block_42.FlatPanelDataStructureEntry[panel_index]
        mfg_name = panel_data_entry.IdMfgName.to_bytes(2, "little").hex()
        product = panel_data_entry.IdProductCode.to_bytes(2, "little").hex()
        sr_no = panel_data_entry.IDSerialNumber.to_bytes(4, "little").hex()
        week = hex(panel_data_entry.WeekOfMfg).lstrip("0x")
        year = hex(panel_data_entry.YearOfMfg).lstrip("0x")
        if panel_data_entry.WeekOfMfg == 0:
            week = "00"
        elif panel_data_entry.WeekOfMfg < 16:
            week = "0" + week
        if panel_data_entry.YearOfMfg == 0:
            year = "00"
        elif panel_data_entry.YearOfMfg < 16:
            year = "0" + year
        vbt_pnp_id = mfg_name + product + sr_no + week + year
        logging.debug(f"\tVBT PNP ID: {vbt_pnp_id}")
        result, edid_data, _ = driver_escape.get_edid_data(panel.target_id)
        if result is False:
            logging.error("Escape call failed, no EDID data found")
            return False
        panel_pnp_id = "".join(format(i, '02x') for i in edid_data[8:18])
        logging.debug(f"\tPanel PNP ID: {panel_pnp_id}")
        if vbt_pnp_id == panel_pnp_id:
            logging.debug(f"\tMatch found for PNP ID at VBT Panel Index: {panel_index}")
            return True
        logging.debug(f"NO match found for PNP ID at VBT Panel Index= {panel_index}")
        return None


##
# @brief        This function will update the PNP ID in the VBT Panel Index
# @param[in]    adapter
# @param[in]    panel
# @param[in]    vbt_panel_index
# @return       True, else False if update VBT fails
def update_vbt_pnp_id(adapter, panel, vbt_panel_index):
    gfx_vbt = Vbt(adapter.gfx_index)
    result, edid_data, _ = driver_escape.get_edid_data(panel.target_id)
    if result is False:
        assert False, "Escape call failed, no EDID data found"
    mfg_name = ("".join(format(i, '02x') for i in edid_data[8:10]))
    mfg_name = "0x" + "".join(reversed([mfg_name[i:i + 2] for i in range(0, len(mfg_name), 2)]))
    gfx_vbt.block_42.FlatPanelDataStructureEntry[vbt_panel_index].IdMfgName = int(mfg_name, 16)

    product = ("".join(format(i, '02x') for i in edid_data[10:12]))
    product = "0x" + "".join(reversed([product[i:i + 2] for i in range(0, len(product), 2)]))
    gfx_vbt.block_42.FlatPanelDataStructureEntry[vbt_panel_index].IdProductCode = int(product, 16)

    sr_no = ("".join(format(i, '02x') for i in edid_data[12:16]))
    sr_no = "0x" + "".join(reversed([sr_no[i:i + 2] for i in range(0, len(sr_no), 2)]))
    gfx_vbt.block_42.FlatPanelDataStructureEntry[vbt_panel_index].IDSerialNumber = int(sr_no, 16)

    week = ("".join(format(i, '02x') for i in edid_data[16:17]))
    week = "0x" + "".join(reversed([week[i:i + 2] for i in range(0, len(week), 2)]))
    gfx_vbt.block_42.FlatPanelDataStructureEntry[vbt_panel_index].WeekOfMfg = int(week, 16)

    year = ("".join(format(i, '02x') for i in edid_data[17:18]))
    year = "0x" + "".join(reversed([year[i:i + 2] for i in range(0, len(year), 2)]))
    gfx_vbt.block_42.FlatPanelDataStructureEntry[vbt_panel_index].YearOfMfg = int(year, 16)

    logging.debug(
        f"Updating VBT with PNP ID= {(mfg_name[2:]) + (product[2:]) + (sr_no[2:]) + (week[2:]) + (year[2:])}")
    if gfx_vbt.apply_changes() is False:
        logging.error("\tFailed to apply PNP ID changes in VBT")
        return False
    status, reboot_required = display_essential.restart_gfx_driver()
    if status is False:
        logging.error("\tFailed to restart display driver after VBT update")
        return False
    gfx_vbt.reload()
    logging.info("Step: Updating PNP ID in VBT")
    return True


##
# @brief        This function will read the feature status
# @param[in]    adapter
# @param[in]    feature_list
# @param[in]    vbt_panel_index
# @param[in]    vbt_feature_status
# @return       vbt_feature_status, read the status of the feature in VBT
def get_feature_status(adapter, feature_list, vbt_panel_index, vbt_feature_status):
    status = True
    gfx_vbt = Vbt(adapter.gfx_index)
    for feature in feature_list:
        if feature == 'DRRS':
            vbt_feature_status[feature] = bool((gfx_vbt.block_44.DRRSEnable[0] & (1 << vbt_panel_index)) >> vbt_panel_index)
        elif feature == 'DMRRS':
            vbt_feature_status[feature] = bool((gfx_vbt.block_44.DmrrsEnable[0] & (1 << vbt_panel_index)) >> vbt_panel_index)
        elif feature == 'PSR':
            vbt_feature_status[feature] = bool((gfx_vbt.block_44.PsrEnable[0] & (1 << vbt_panel_index)) >> vbt_panel_index)
        elif feature == 'DPST':
            vbt_feature_status[feature] = bool((gfx_vbt.block_44.DpstEnable[0] & (1 << vbt_panel_index)) >> vbt_panel_index)
        elif feature == 'LACE':
            vbt_feature_status[feature] = bool((gfx_vbt.block_44.LaceStatus[0] & (1 << vbt_panel_index)) >> vbt_panel_index)
        else:
            logging.error(f"{feature} not present in the feature list")
            status = False
    return vbt_feature_status, status


##
# @brief        This function will enable feature that are passed in the command line in VBT
# @param[in]    adapter
# @param[in]    feature_list
# @param[in]    vbt_panel_index
# @param[in]    initial_vbt_status
# @return       True, else False if driver restart or VBT reload fails
def enable_feature(adapter, feature_list, vbt_panel_index, initial_vbt_status):
    do_driver_restart = True
    gfx_vbt = Vbt(adapter.gfx_index)
    for feature in feature_list:
        logging.info(f"Step: Enabling {feature} feature in VBT")
        if feature == 'DRRS':
            if initial_vbt_status[feature] is False:
                gfx_vbt.block_44.DRRSEnable[0] |= (1 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already enabled in VBT")
                do_driver_restart = False
        elif feature == 'DMRRS':
            if initial_vbt_status[feature] is False:
                gfx_vbt.block_44.DmrrsEnable[0] |= (1 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already enabled in VBT")
                do_driver_restart = False
        elif feature == 'PSR':
            if initial_vbt_status[feature] is False:
                gfx_vbt.block_44.PsrEnable[0] |= (1 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already enabled in VBT")
                do_driver_restart = False
        elif feature == 'DPST':
            if initial_vbt_status[feature] is False:
                gfx_vbt.block_44.DpstEnable[0] |= (1 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already enabled in VBT")
                do_driver_restart = False
        elif feature == 'LACE':
            if initial_vbt_status[feature] is False:
                gfx_vbt.block_44.LaceStatus[0] |= (1 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already enabled in VBT")
                do_driver_restart = False

        if do_driver_restart is True:
            if gfx_vbt.apply_changes() is False:
                logging.error(f"{feature}Feature changes failed in VBT")
                logging.error(f"{feature} feature enabling failed")
                return False, do_driver_restart

    return True, do_driver_restart


##
# @brief        This function will disable the features not passed in the command line in VBT
# @param[in]    adapter
# @param[in]    feature_list
# @param[in]    vbt_panel_index
# @param[in]    initial_vbt_status
# @return       True, else False if driver restart or VBT reload fails
def disable_feature(adapter, feature_list, vbt_panel_index, initial_vbt_status):
    do_driver_restart = True
    gfx_vbt = Vbt(adapter.gfx_index)
    for feature in feature_list:
        logging.info(f"Step: Disabling {feature} feature in VBT")
        if feature == 'DRRS':
            if initial_vbt_status[feature] is True:
                gfx_vbt.block_44.DRRSEnable[0] = (gfx_vbt.block_44.DRRSEnable[0] & ~(1 << vbt_panel_index)) | (
                        0 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already disabled in VBT")
                do_driver_restart = False
        elif feature == 'DMRRS':
            if initial_vbt_status[feature] is True:
                gfx_vbt.block_44.DmrrsEnable[0] = (gfx_vbt.block_44.DmrrsEnable[0] & ~(1 << vbt_panel_index)) | (
                        0 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already disabled in VBT")
                do_driver_restart = False
        elif feature == 'PSR':
            if initial_vbt_status[feature] is True:
                gfx_vbt.block_44.PsrEnable[0] = (gfx_vbt.block_44.PsrEnable[0] & ~(1 << vbt_panel_index)) | (
                        0 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already disabled in VBT")
                do_driver_restart = False
        elif feature == 'DPST':
            if initial_vbt_status[feature] is True:
                gfx_vbt.block_44.DpstEnable[0] = (gfx_vbt.block_44.DpstEnable[0] & ~(1 << vbt_panel_index)) | (
                        0 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already disabled in VBT")
                do_driver_restart = False
        elif feature == 'LACE':
            if initial_vbt_status[feature] is True:
                gfx_vbt.block_44.LaceStatus[0] = (gfx_vbt.block_44.LaceStatus[0] & ~(1 << vbt_panel_index)) | (
                        0 << vbt_panel_index)
            else:
                logging.info(f"{feature} feature already disabled in VBT")
                do_driver_restart = False

        if do_driver_restart is True:
            if gfx_vbt.apply_changes() is False:
                logging.error(f"{feature}Feature changes failed in VBT")
                logging.error(f"{feature} feature enabling failed")
                return False, do_driver_restart

    return True, do_driver_restart
