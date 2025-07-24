########################################################################################################################
# @file         gfx_assistant.py
# @brief        Python library containing Gfx Assistant related APIs.
# @author       Rohit Kumar
########################################################################################################################
import base64
import json
import logging
import os
import subprocess

URL_PANEL_GET = "http://10.235.18.70:7001/panel/"


def _dump_edid(edid, output_path):
    if os.path.exists(output_path):
        return

    decoded_string = base64.b64decode(edid)

    logging.debug(decoded_string)

    with open(output_path, "wb") as f:
        f.write(decoded_string)


def _dump_dpcd(dpcd, output_path):
    if os.path.exists(output_path):
        return

    output = ""
    for offset, value in dpcd.items():
        output += f"{offset}: {value}.\n"

    logging.debug(output)

    with open(output_path, "w") as f:
        f.write(output)


def _add_simulation_files(panel_input_data_dir, panel_id):
    output = subprocess.run(f"curl {URL_PANEL_GET}" + panel_id + "?source=gta > panel.json", universal_newlines=True,
                            shell=True, capture_output=True)
    logging.info(output)
    if os.path.exists("panel.json") is False:
        logging.error("Failed to download data from Gfx Assistant server")
        return False
    try:
        with open("panel.json", "r") as f:
            panel = json.load(f)
    except Exception as e:
        logging.error(panel)
        logging.error(e)
        return False

    if panel['vot'] not in ['eDP', 'DP', 'HDMI', 'MIPI']:
        logging.error(f"Unsupported VOT: {panel['vot']}")
        return False

    vot = 'eDP_DPSST'
    if panel['vot'] in ['HDMI', 'MIPI']:
        vot = panel['vot']
    output_path = os.path.join(panel_input_data_dir, vot, panel['_id'])

    _dump_edid(panel['edid'], output_path + "_EDID.bin")
    if panel['dpcd']:
        _dump_dpcd(panel['dpcd'], output_path + "_DPCD.txt")


def add_simulation_files(panel_input_data_dir, panel_id):
    try:
        _add_simulation_files(panel_input_data_dir, panel_id)
    except Exception as e:
        logging.warning(e)
