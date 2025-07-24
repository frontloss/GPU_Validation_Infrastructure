####################################################################################################
# @file         display_ddi.py
# @brief        Python wrapper exposes interfaces for Display DDI Verification
# @details      display_ddi.py provides interface's to Verify Display DDI Configuration
#               for EDP, DP
#               User-Input : DisplayDDI() instance - display_port to be verifed
#               DisplayDDI information mentioned below: \n
# @note         Supported display interfaces are EDP, DP\n
# @author       Aafiya Kaleem
##################################################################################################

import logging
import os

import Libs.Feature.display_port.dpcd_helper as dpcd
from Libs.Feature.display_engine.de_base import display_base
from Libs.Core.logger import gdhm
from DisplayRegs.Gen13.Ddi import Gen13DdiRegs
from DisplayRegs import DisplayArgs

from registers.mmioregister import MMIORegister


##
# @brief has functions to get DDI related Information
class DisplayDDI(display_base.DisplayBase):

    ##
    # @brief initialize DisplayDDI Base Class
    # @param[in] display_port display to verify
    # @param[in] gfx_index graphics adapter
    def __init__(self, display_port=None, gfx_index='gfx_0'):
        self.display_port = display_port
        display_base.DisplayBase.__init__(self,display_port, gfx_index=gfx_index)

logger_template = "{res:^5}: {feature:<60}: Expected: {exp:<20}  Actual: {act}"


##
# @brief Verify if DP_TP_CTL_REGISTER is programmed as per bspec for EDP,DP display.
# @param[in] ddiObj DisplayDDI() object instance
# @param[in] gfx_index graphics adapter
# @return Bool Return true if MMIO programming is correct, else return false
def VerifyConnectedDDIPort(ddiObj, gfx_index='gfx_0'):
    if (ddiObj.platform in ['JSL', 'ICLLP', 'GLK', 'SKL', 'KBL', 'CFL', 'CNL']):
        ddi = ddiObj.ddi.split("_")
    else:
        ddi = ddiObj.pipe.split("_")

        # To check TypeC PHY Ownership
        if ddiObj.platform == 'ADLP':
            ddi_name = ddiObj.ddi.split("_")[-1]
            if ddi_name in ['F', 'G', 'H', 'I']:
                if ddi_name == 'F':
                    offset = Gen13DdiRegs.OFFSET_DDI_BUF_CTL.DDI_BUF_CTL_USBC1
                elif ddi_name == 'G':
                    offset = Gen13DdiRegs.OFFSET_DDI_BUF_CTL.DDI_BUF_CTL_USBC2
                elif ddi_name == 'H':
                    offset = Gen13DdiRegs.OFFSET_DDI_BUF_CTL.DDI_BUF_CTL_USBC3
                elif ddi_name == 'I':
                    offset = Gen13DdiRegs.OFFSET_DDI_BUF_CTL.DDI_BUF_CTL_USBC4

                value = DisplayArgs.read_register(offset, gfx_index)
                ddi_buf_ctl_value = Gen13DdiRegs.REG_DDI_BUF_CTL(offset, value)
                typec_phy_ownership = ddi_buf_ctl_value.TypecPhyOwnership
                if typec_phy_ownership == 1:
                    logging.info(
                        logger_template.format(res="PASS", feature="DDI_BUF_CTL TypecPHYOwnership",
                                               exp="{}".format(1), act=typec_phy_ownership))
                else:
                    logging.error(
                        logger_template.format(res="FAIL", feature="DDI_BUF_CTL TypecPHYOwnership",
                                               exp="{}".format(1), act=typec_phy_ownership))
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][DDI]: TypeC PHY Ownership failed. Expected: 1(Enabled)"
                              "Actual:{}".format(typec_phy_ownership),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )

    reg = MMIORegister.read("DP_TP_CTL_REGISTER", "DP_TP_CTL_%s" % (ddi[1]), ddiObj.platform, gfx_index=gfx_index)
    logging.debug("DP_TP_CTL_" + ddi[1] + "--> Offset : " + format(reg.offset, '08X')
                  + " Value :" + format(reg.asUint, '08X'))

    if not reg.transport_enable:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DDI]: Transport Enable failed! Expected: 1(Enabled) "
                  "Actual:{}".format(reg.transport_enable),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Driver.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error(logger_template.format(res="FAIL", feature="DDI Transport Enable", exp="1(Enabled)",
                                             act=reg.transport_enable))
        return False

    mode_select = dpcd.DPCD_getTransportModeSelect(ddiObj.display_and_adapter_info)
    framing = dpcd.DPCD_checkEnhancedFraming(ddiObj.display_and_adapter_info)
    str_framing = 'ENABLED' if framing == 1 else 'DISABLED'
    assr = dpcd.DPCD_checkASSR(ddiObj.display_and_adapter_info)
    str_assr = 'ENABLED' if assr == 1 else 'DISABLED'

    if (mode_select == "SST"):
        if (reg.transport_mode_select == 0):
            if (reg.enhanced_framing_enable == framing):

                logging.info(
                    logger_template.format(res="PASS", feature="DP_TP_CTL_{} - Enhanced Framing".format(ddi[1]),
                                           exp="{}({})".format(framing, str_framing), act=reg.enhanced_framing_enable))
                if (reg.alternate_sr_enable == assr):
                    logging.info(
                        logger_template.format(res="PASS", feature="DPCD_ASSR_CHECK - ASSR (Alternate SR Enable)",
                                               exp="{}({})".format(assr, str_assr), act=reg.alternate_sr_enable))
                    logging.debug("PASS : " + ddiObj.display_port + " Configured to SST Mode")
                    return True
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][DDI]: DPCD_ASSR_CHECK-Alternate SR Enable failed for SST! "
                              "Expected:{0}({1}) Actual:{2}".format(assr, str_assr, reg.alternate_sr_enable),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(
                        logger_template.format(res="FAIL", feature="DPCD_ASSR_CHECK - ASSR (Alternate SR Enable)",
                                               exp="{}({})".format(assr, str_assr), act=reg.alternate_sr_enable))
                    return False
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][DDI]:DP_TP_CTL_{0} - Enhanced Framing failed for SST! "
                          "Expected:{1}({2}) Actual:{3}".format(ddi[1], framing, str_framing,
                                                                reg.enhanced_framing_enable),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template.format(res="FAIL", feature="DP_TP_CTL_{} - Enhanced Framing".format(ddi[1]),
                                           exp="{}({})".format(framing, str_framing), act=reg.enhanced_framing_enable))
                return False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DDI]:Transport Mode Selection failed for SST! Expected:0(SST Mode)"
                      " Actual:{}".format(reg.transport_mode_select),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="DDI Transport Mode Select", exp="0(SST Mode)",
                                                 act=reg.transport_mode_select))
            return False

    elif (mode_select == "MST") or (mode_select == "DP_128_132_BIT_SYMBOL_MODE"):
        if (reg.transport_mode_select == 1):
            if ((reg.enhanced_framing_enable == 0)):
                logging.info(
                    logger_template.format(res="PASS", feature="DP_TP_CTL_{} - Enhanced Framing".format(ddi[1]),
                                           exp="0(DISABLED)", act=reg.enhanced_framing_enable))
                if ((reg.alternate_sr_enable == assr == 0)):
                    logging.info(
                        logger_template.format(res="PASS", feature="DPCD_ASSR_CHECK - ASSR (Alternate SR Enable)",
                                               exp="{}({})".format(assr, str_assr), act=reg.alternate_sr_enable))
                    logging.debug("PASS : " + ddiObj.display_port + " Configured to MST Mode")
                    return True
                else:
                    gdhm.report_bug(
                        title="[Interfaces][Display_Engine][DDI]:DPCD_ASSR_CHECK - Alternate SR Enable failed for MST! "
                              "Expected:{0}({1}) Actual:{2}".format(assr, str_assr, reg.alternate_sr_enable),
                        problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                        component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                        priority=gdhm.Priority.P2,
                        exposure=gdhm.Exposure.E2
                    )
                    logging.error(
                        logger_template.format(res="FAIL", feature="DPCD_ASSR_CHECK - ASSR (Alternate SR Enable)",
                                               exp="{}({})".format(assr, str_assr), act=reg.alternate_sr_enable))
                    return False
            else:
                gdhm.report_bug(
                    title="[Interfaces][Display_Engine][DDI]:DP_TP_CTL_{0} - Enhanced Framing failed for MST! Expected:"
                          "{1}({2}) Actual:{3}".format(ddi[1], framing, str_framing, reg.enhanced_framing_enable),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                logging.error(
                    logger_template.format(res="FAIL", feature="DP_TP_CTL_{} - Enhanced Framing".format(ddi[1]),
                                           exp="{}({})".format(framing, str_framing), act=reg.enhanced_framing_enable))
                return False
        else:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DDI]:Transport Mode Selection failed for MST! Expected:"
                      "1(MST Mode) Actual:{}".format(reg.transport_mode_select),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error(logger_template.format(res="FAIL", feature="DDI Transport Mode Select", exp="1 (MST Mode)",
                                                 act=reg.transport_mode_select))
            return False
    else:
        gdhm.report_bug(
            title="[Interfaces][Display_Engine][DDI]:Transport Mode Select is not supported for {}".format(
                ddiObj.display_port),
            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
            component=gdhm.Component.Test.DISPLAY_INTERFACES,
            priority=gdhm.Priority.P2,
            exposure=gdhm.Exposure.E2
        )
        logging.error("ERROR: DDI Transport Mode Select for %s NOT Supported" % (ddiObj.display_port))
        return False


##
# @brief Verify display DDI programming for the passed display_port.
# @param[in] ddiList list of DisplayDDI() object instances to specify port_name
# @param[in] gfx_index
# @return bool Return true if MMIO programming is correct, else return false
def VerifyDDIProgramming(ddiList, gfx_index='gfx_0'):
    status = True

    for ddiObj in ddiList:
        logging.info(
            "******* DDI Verification for " + ddiObj.display_port + " (Tagrget ID : {}) - {} Connected to {},{},{} *******".format(
                ddiObj.targetId, ddiObj.display_port, gfx_index, ddiObj.pipe, ddiObj.ddi))
        if ddiObj.pipe is None:
            gdhm.report_bug(
                title="[Interfaces][Display_Engine][DDI]:ERROR : {} port is NOT Connected to any Pipe during DDI "
                      "Verification".format(ddiObj.display_port),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Driver.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            logging.error("ERROR : " + ddiObj.display_port + " is NOT Connected to any Pipe. Check if it is Connected")
            return False
        if ddiObj.display_port.startswith("DP"):
            status = VerifyConnectedDDIPort(ddiObj, gfx_index)
            if status is False:
                # GDHM handled in VerifyConnectedDDIPort(ddiObj, gfx_index)
                return status
        else:
            logging.info("INFO : DDI Verification NOT Supported for " + ddiObj.display_port)
    return status


if __name__ == "__main__":
    scriptName = os.path.basename(__file__).replace(".py", "")
    FORMAT = '%(asctime)-15s %(levelname)s  [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=FORMAT,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=scriptName + '.log',
                        filemode='w')

    ddiList = []
    # ddiList.append(DisplayDDI("HDMI_C"))
    ddiList.append(DisplayDDI("DP_A"))
    # ddiList.append(DisplayDDI("DP_C"))

    result = VerifyDDIProgramming(ddiList, 'gfx_0')
    if result is False:
        # GDHM handled in VerifyConnectedDDIPort(ddiObj, gfx_index)
        logging.error("FAIL : verifyPortProgramming")
    else:
        logging.info("PASS : verifyPortProgramming")