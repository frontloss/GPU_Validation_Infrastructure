#######################################################################################################################
# @file         cmtg.py
# @brief        File contains all CMTG related verification APIs or wrappers
#
# @author       Bhargav Adigarla
#######################################################################################################################
import logging

from Libs.Core import etl_parser, driver_escape
from Libs.Core.logger import gdhm
from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.sw_sim import driver_interface
from Tests.PowerCons.Functional.CMTG import cmtg
display_config_ = DisplayConfiguration()
driver_interface_ = driver_interface.DriverInterface()


##
# @brief        Verify connected panels are symmetric or asymmetric
# @param[in]    panel1: Panel object
# @param[in]    panel2: Panel object
# @return       True if supported else False
def is_symmetric(panel1, panel2):
    symmetric = True
    logging.info("Target_id's panel1 {0}, panel2 {1}".format(panel1.target_id, panel2.target_id))
    panel_1 = driver_escape.get_edid_data(panel1.target_id)
    panel_2 = driver_escape.get_edid_data(panel2.target_id)

    # Check number of extension blocks
    if panel_1[126] == panel_2[126]:
        # For each extension block, verify the checksum
        for block_index in range(panel_1[126] + 1):
            checksum_index = (128 * block_index) + 127
            if panel_1[checksum_index] != panel_2[checksum_index]:
                symmetric = False
                break
    else:
        symmetric = False
    return symmetric


##
# @brief        Verify port sync functionality as below
#               1. CMTG control register verification
#               2. CMTG slave status of lfp's
#               3. PLL1 should be disabled in port sync mode
# @param[in]    adapter: Adapter object
# @param[in]    panels: Panel object
# @param[in]    expected_port_sync: port sync expected state
# @return       True if supported else False
def verify(adapter, panels, expected_port_sync=True):
    status = True
    err_msg = None
    if cmtg.verify_cmtg_status(adapter) is True:
        logging.info("\t CMTG status: enabled")
        if cmtg.verify_cmtg_slave_status(adapter, panels[0]):
            logging.info("\t {0} CMTG slave status: enabled".format(panels[0]))
            if cmtg.verify_cmtg_timing(adapter, panels[0]):
                logging.info("\t  CMTG and {0} transcoder timings are matching".format(panels[0]))
                if len(panels) == 2:
                    if expected_port_sync:
                        if cmtg.verify_cmtg_slave_status(adapter, panels[1]) is True:
                            logging.info("\t {0} CMTG slave status: enabled".format(panels[1]))
                            if cmtg.verify_cmtg_timing(adapter, panels[1]) is True:
                                logging.info("\t  CMTG and {0} transcoder timings are matching".format(panels[1]))
                                if cmtg.verify_pll_status(adapter) is False:
                                    logging.info("\t  PLL1 is disabled in port sync mode")
                                    return True
                                else:
                                    err_msg = "PLL1 is enabled in port sync mode"
                                    status = False
                            else:
                                err_msg = "CMTG and Transcoder timings are not matching in port sync mode"
                                status = False
                        else:
                            err_msg = "{0} is not slave to CMTG".format(panels[1])
                            status = False
                    else:
                        if cmtg.verify_cmtg_slave_status(adapter, panels[1]) is True:
                            err_msg = "{0} is slave to CMTG".format(panels[1])
                            status = False
                else:
                    return status
            else:
                err_msg = "CMTG and Transcoder timings are not matching in port sync mode"
                status = False
        else:
            err_msg = "{0} is not slave to CMTG".format(panels[0])
            status = False
    else:
        err_msg = "CMTG status is disabled"
        status = False

    logging.error(err_msg)
    gdhm.report_bug(
        title=err_msg,
        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
        component=gdhm.Component.Driver.DISPLAY_POWERCONS,
        priority=gdhm.Priority.P2,
        exposure=gdhm.Exposure.E2
    )
    return status


##
# @brief        Verify VBI timestamps matching in port sync mode with 1ms software delay.
# @param[in]    panels: Panel objects
# @param[in]    etl_file: ETL file path
# @return       True if timestamps matching else False
def verify_vbis(panels, etl_file):
    status = True
    count = 0
    len = 0
    etl_parser.generate_report(etl_file)

    lfp0_vbi_data = etl_parser.get_vbi_data('PIPE_' + panels[0].pipe)
    if lfp0_vbi_data is None:
        logging.error("\tVBI data is empty")
        gdhm.report_bug(
            title="[PowerCons][PORTSYNC] VBI Data is Empty in ETL",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        status = False

    lfp1_vbi_data = etl_parser.get_vbi_data('PIPE_' + panels[1].pipe)
    if lfp1_vbi_data is None:
        logging.error("\tVBI data is empty")
        gdhm.report_bug(
            title="[PowerCons][PORTSYNC] VBI Data is Empty in ETL",
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_POWERCONS,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        status = False

    for index in range(0,25):
        logging.info("VBI time stamps: lfp0 - {0} lfp1 - {1}".
                      format(lfp0_vbi_data[index].TimeStamp, lfp1_vbi_data[index].TimeStamp))

        # Keeping 120 micro sec SW delay for VBI timestamps verification
        if (abs(lfp0_vbi_data[index].TimeStamp*1000 - lfp1_vbi_data[index].TimeStamp*1000)) > 120:
            err_msg = "[PowerCons][PORTSYNC]Port sync verification failed due to VBI time stamps mismatch: lfp0 - " + \
                      str(lfp0_vbi_data[index].TimeStamp) + "lfp1 -" + str(lfp1_vbi_data[index].TimeStamp)
            status = False
            logging.error(err_msg)
            gdhm.report_bug(
                title=err_msg,
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_POWERCONS,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
    return status