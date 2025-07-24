#######################################################################################################################
# @file         alrr.py
# @brief        APIs to enable, disable ALRR
#
# @author       Ravichandran M
#######################################################################################################################
import logging
from Libs.Core import etl_parser
from Libs.Feature.powercons import registry
from Tests.PowerCons.Modules import dpcd
from Tests.PowerCons.Modules.dut_context import Adapter, Panel


##
# @brief        This is a helper function to enable alrr
# @param[in]    adapter - adapter object
# @return       status Boolean, True enabled & restart required, None enabled & no restart required, False otherwise


def enable(adapter):
    idt_alrr = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if idt_alrr.DisableAlrr != 0:
        idt_alrr.DisableAlrr = 0
        status = idt_alrr.update(adapter.gfx_index)
        if status is False:
            logging.error("\tFAILED to enable ALRR(30th bit) via DisplayPcFeatureControl registry")
            return False
    logging.info("\tSuccessfully enabled ALRR(30th bit) via DisplayPcFeatureControl registry")
    return status


##
# @brief        This is a helper function to disable alrr
# @param[in]    adapter - adapter object
# @return       status Boolean, True disabled & restart required, None disabled & no restart required, False otherwise


def disable(adapter):
    idt_alrr = registry.DisplayPcFeatureControl(adapter.gfx_index)
    status = None
    if idt_alrr.DisableAlrr != 1:
        idt_alrr.DisableAlrr = 1
        status = idt_alrr.update(adapter.gfx_index)
        if status is False:
            logging.error("\tFAILED to Disable ALRR(30th bit) via DisplayPcFeatureControl registry")
            return False
    logging.info("\tSuccessfully disabled ALRR(30th bit) via DisplayPcFeatureControl registry")
    return status


##
# @brief        Exposed API to verify ALRR
# @param[in]    adapter - object of Adapter
# @param[in]    panel - object of Panel
# @param[in]    etl_file String
# @param[in]    expect_alrr Boolean - True if ALRR should not work, False otherwise
# @return       True if operation is successful, False otherwise


def verify(adapter: Adapter, panel: Panel, etl_file: str, expect_alrr=False):
    dpcd_data = None
    etl_parser_config = etl_parser.EtlParserConfig()
    etl_parser_config.dpcdData = 1
    if etl_parser.generate_report(etl_file, etl_parser_config) is False:
        logging.error(f"\tFAILED to generate EtlParser report {etl_file}")
        return False
    logging.info(f"\tSuccessfully generated EtlParser report for {etl_file}")

    psr_dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.PSR_CONFIGURATION, is_write=True)
    if psr_dpcd_data is None:
        logging.error("\t0x170H DPCD data not found in ETL")
        return False

    for psr_data in psr_dpcd_data:
        psr_config_dpcd = dpcd.SinkPsrConfiguration(panel.target_id)
        psr_config_dpcd.value = int(psr_data.Data.split('-')[0], 16)
        if psr_config_dpcd.psr_enable_in_sink:
            dpcd_data = etl_parser.get_dpcd_data(dpcd.Offsets.ALRR_UBRR_CONFIG, is_write=True,
                                                 start_time=psr_data.TimeStamp)
    # ALRR DPCD verification from ETL.

    if dpcd_data is None:
        if expect_alrr is True:
            logging.debug("\tNo ALRR DPCD programming found which is expected in negative case")
            return True
        logging.error("\tNo ALRR DPCD programming found which is not expected")
        return False

    if expect_alrr is True:
        logging.error("\tALRR DPCD programming found which is not expected in negative case")
        return False

    status_val = True
    logging.info("Starting ALRR DPCD verification...")
    for dpcd_entry in dpcd_data:
        # Convert from byte to little indian uint8
        b = bytearray.fromhex(dpcd_entry.Data.replace('-', ''))
        dpcd_val = int.from_bytes(b, byteorder='little')
        logging.info(f"\tDPCD Address: {hex(int(dpcd_entry.Address))}= {hex(int(dpcd_entry.Data))} at "
                     f"{dpcd_entry.TimeStamp} ms")
        alrr_config_dpcd = dpcd.AlrrUbrrConfig(panel.target_id, dpcd_val)
        if alrr_config_dpcd.enable_alrr == dpcd.AlrrStatus.DISABLE and expect_alrr:
            logging.debug(f"\tALRR programmed to disable in DPCD for port {panel.port} on {adapter.name}")
        elif alrr_config_dpcd.enable_alrr == dpcd.AlrrStatus.ENABLE:
            logging.debug(f"\tALRR programmed to enable ALRR in DPCD for port {panel.port} on {adapter.name}")
        else:
            logging.error(f"\tMismatch seen in ALRR programming in DPCD Status={alrr_config_dpcd.enable_alrr}")
            status_val = False
        return status_val
