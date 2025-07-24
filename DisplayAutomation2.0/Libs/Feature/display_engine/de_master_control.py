########################################################################################################################################################
# @file         de_master_control.py
# @brief        Python Wrapper that exposes the interface for Display Pipeline Validation
# @details     Checks for the platform and calls the correct implementation
# @author       akaleem
#########################################################################################################################################################


import ctypes
import logging
import os
from enum import IntEnum

import math
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Core.logger import html
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_context
from Libs.Feature import display_audio
from Libs.Feature.clock import display_clock
from Libs.Feature.display_engine import de_base_interface
from Libs.Feature.display_fbc import fbc
from Libs.Feature.display_powerwell import powerwell
from Libs.Feature.display_watermark import watermark as wm

FLOW_LOG = 25
logging.addLevelName(FLOW_LOG, "FLOW")

##
# @brief        flag_bits to enable/disable various verifiers
class flag_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("clock_verifier", ctypes.c_uint8, 1),  # bit0
        ("plane_verifier", ctypes.c_uint8, 1),  # bit1
        ("pipe_verifier", ctypes.c_uint8, 1),  # bit2
        ("transcoder_verifier", ctypes.c_uint8, 1),  # bit3
        ("ddi_verifier", ctypes.c_uint8, 1),  # bit4
        ("powerwell_verifier", ctypes.c_uint8, 1),  # bit5
        ("watermark_verifier", ctypes.c_uint8, 1),  # bit6
        ("dip_ctrl_verifier", ctypes.c_uint8, 1),  # bit7
        ("fbc_verifier", ctypes.c_uint8, 1),  # bit8
        ("phy_buf_verifier", ctypes.c_uint8, 1),  # bit9
        ("reserved", ctypes.c_uint8, 1)
    ]

##
# @brief        features to enable/disable
class features(ctypes.LittleEndianStructure):
    _fields_ = [
        ("skip_S3", ctypes.c_uint8, 1),  # bit0
        ("skip_S4", ctypes.c_uint8, 1),  # bit1
        ("skip_CS", ctypes.c_uint8, 1),  # bit2
        ("skip_Reboot", ctypes.c_uint8, 1),  # bit3
        ("skip_LidSwitch", ctypes.c_uint8, 1),  # bit4
        ("skip_ACDC", ctypes.c_uint8, 1),  # bit5
        ("reserved", ctypes.c_uint8, 1)
    ]

##
# @brief       flags byte union
class flags(ctypes.Union):
    _anonymous_ = ("bit",)
    _fields_ = [
        ("bit", flag_bits),
        ("asbyte", ctypes.c_uint32)
    ]

##
# @brief       VerificationMethod structure
class VerificationMethod(IntEnum):
    NONE = 0
    ALL = 1
    CLOCK = 2
    PLANE = 3
    PIPE = 4
    TRANSCODER = 5
    DDI = 6
    POWERWELL = 7
    WATERMARK = 8
    DIP_CTRL = 9
    FBC = 10
    PHY_BUF = 11


##
# @brief       DisplayEngine class has various DE verification control functions
class DisplayEngine:
    sequence_counter = 1.0
    test_sequence_format = "    Test Sequence:{seq:^5}: {msg:<35}: {res}"

    ##
    # @brief[in]       Initializes DisplayEngine object
    # @param[in]       gfx_index - Graphics adapter
    def __init__(self, gfx_index='gfx_0'):
        self.verification_list = []
        self.machine_info = SystemInfo()
        self.get_platform_verifiers(gfx_index)
        self.master_verification_list = list(self.verification_list)
        self.display_config = display_config.DisplayConfiguration()
        self.display_audio = display_audio.DisplayAudio()

    ##
    # @brief[in]        Adds to requires verifiers based on requirement
    # @param[in]        *verification_methods Methods to add
    # @return           list - list of verifications
    def add_verifiers(self, *verification_methods):
        for method in verification_methods:
            self.verification_list.append(method)
        return self.verification_list

    ##
    # @brief[in]        Removes to requires verifiers based on requirement
    # @param[in]        verification_methods Methods to remove
    # @return[in]       list - verification list
    def remove_verifiers(self, *verification_methods):
        for method in verification_methods:
            if method in self.verification_list:
                self.verification_list.remove(method)
        return self.verification_list

    ##
    # @brief        Checks for the platform and calls the correct implementation
    # @param[in]    portList - List of ports to verify
    # @param[in]    planeList - List of planes to verify
    # @param[in]    pipeList - List of pipes to verify
    # @param[in]    transcoderList - List of transcoders to verify
    # @param[in]    ddiList - List of ddis to verify
    # @param[in]    dipList - List of dips to verify
    # @param[in]    gfx_index - graphics adapter
    # @return       bool - test pass/fail
    def verify_display_engine(self, portList=None, planeList=None, pipeList=None,
                              transcoderList=None, ddiList=None, dipList=None, gfx_index='gfx_0'):
        self.final_result = []
        self.gfx_index_list = []
        self.display_list = []

        if portList is None or len(portList) == 0:
            portList = []
            self.enum_displays = self.display_config.get_enumerated_display_info()
            for i in range(self.enum_displays.Count):
                connector_port = cfg_enum.CONNECTOR_PORT_TYPE(self.enum_displays.ConnectedDisplays[i].ConnectorNPortType).name
                self.gfx_index_list.append(
                    self.enum_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
                self.display_list.append(connector_port)

                if self.enum_displays.ConnectedDisplays[i].IsActive and \
                        self.enum_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex == gfx_index :
                    portList.append(connector_port)
            gfx_display_dict = display_clock.DisplayClock.get_gfx_display_dict(self.display_list, self.gfx_index_list)
        else:  #To fill gfx_display_dict in case portList already provided as input to the API
            self.topology, self.display_list, self.display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex()
            for each_display_and_adapter_info in self.display_and_adapter_info_list:
                self.gfx_index_list.append(each_display_and_adapter_info.adapterInfo.gfxIndex)
            gfx_display_dict = {k: v for k, v in zip(self.display_list, self.gfx_index_list)}
            flipped = {}
            for key, value in gfx_display_dict.items():
                if value not in flipped:
                    flipped[value] = [key]
                else:
                    flipped[value].append(key)
            gfx_display_dict = flipped

        # To prepare a dictionary with only active displays with gfx_index mapping from dictionary with all display and gfx_index
        active_gfx_display_dict = {}
        for key,value in gfx_display_dict.items():
            for i in range(len(portList)):
                if (portList[i] in value):
                    active_gfx_display_dict.setdefault(key, []).append(portList[i])

        logging.info("Display list:{} , gfx_index_list:{}, gfx_display_dict:{}, active_gfx_display_dict:{}".format(
            self.display_list, self.gfx_index_list, gfx_display_dict, active_gfx_display_dict))
        self.topology, self.display_list, self.display_and_adapter_info_list = self.display_config.get_current_display_configuration_ex()
        # TODO: Need to get audio driver per adapter
        self.audio_driver = self.display_audio.get_audio_driver()
        logging.info('Verifying Display Engine for adapter %s with Display Config: Topology = %s Displays List = %s Audio Driver Status = %s' %
                     (gfx_index, self.topology, self.display_list, display_audio.AudioCodecDriverType(self.audio_driver).name))

        self.final_result.append('Results for Display %s' % portList)
        for method in self.verification_list:
            if method == VerificationMethod.CLOCK:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                displayClock = display_clock.DisplayClock()
                html.step_start("**************CLOCK VERIFICATION START**************")
                if False == displayClock.verify_clocks(gfx_index):
                    # GDHM handled in verify_clocks(gfx_index)
                    logging.error("FAIL : Clock Verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Clock Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : Clock Verification')
                else:
                    logging.info("PASS : Clock Verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Clock Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : clock Verification')
                logging.info("**************CLOCK VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.PLANE:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************PLANE VERIFICATION START**************")
                if False == de_base_interface.verify_plane_programming(portList, planeList, gfx_index):
                    # GDHM handled in VerifyPlaneProgramming() in display_plane.py
                    logging.error("FAIL : Plane Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Plane Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : Plane Programming verification')
                else:
                    logging.info("PASS : Plane Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Plane Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : Plane Programming verification')
                logging.info("**************PLANE VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.PIPE:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************PIPE VERIFICATION START**************")
                if False == de_base_interface.verify_pipe_programming(portList, pipeList, gfx_index):
                    # GDHM handled in VerifyPipeProgramming() in display_pipe.py
                    logging.error("FAIL : Pipe Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Pipe Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : Pipe Programming verification')
                else:
                    logging.info("PASS : Pipe Programming verification! ")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Pipe Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : Pipe Programming verification')
                logging.info("**************PIPE VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.TRANSCODER:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************TRANSCODER VERIFICATION START**************")
                if False == de_base_interface.verify_transcoder_programming(portList, transcoderList,
                                                                            gfx_index):
                    logging.error("FAIL : Port Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Port Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : Port Programming verification')
                else:
                    logging.info("PASS : Port Programming verification! ")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Port Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : Port Programming verification')
                logging.info("**************TRANSCODER VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.DDI:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************DDI VERIFICATION START**************")
                if False == de_base_interface.verify_ddi_programming(portList, ddiList, gfx_index):
                    # GDHM handled in VerifyDDIProgramming() in display_ddi.py
                    logging.error("FAIL : DDI Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='DDI Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : DDI Programming verification')
                else:
                    logging.info("PASS : DDI Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='DDI Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : DDI Programming verification')
                logging.info("**************DDI VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.DIP_CTRL:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************DIP CTRL VERIFICATION START**************")
                if False == de_base_interface.verify_videoDIPCtrl_programming(portList, dipList, gfx_index):
                    # GDHM handled in VerifyDisplayDIPControl() in display_dip_control.py
                    logging.error("FAIL : DIP CTRL Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='DIP CTRL Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : DIP CTRL Programming verification')
                else:
                    logging.info("PASS : DIP CTRL Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='DIP CTRL Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : DIP CTRL Programming verification')
                if False == de_base_interface.verify_videodipavi_infoframe(portList, dipList, gfx_index):
                    # GDHM handled in VerifyDisplayDIPAVIdata() in display_dip_control.py
                    logging.error("FAIL : DIP AVI Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                  msg='DIP AVI Programming verification', res='FAIL'))
                    self.final_result.append('FAIL : DIP AVI Programming verification')
                else:
                    logging.info("PASS : DIP AVI Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                  msg='DIP AVI Programming verification', res='PASS'))
                    self.final_result.append('PASS : DIP AVI Programming verification')
                logging.info("**************DIP CTRL VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.POWERWELL:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************POWERWELL VERIFICATION START**************")
                if powerwell.verify_adapter_power_well(gfx_index) is False:
                    logging.error("FAIL : Power well verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Power well verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : Powerwell verification')
                else:
                    logging.info("PASS : Power well verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Power well verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : Powerwell verification')
                logging.info("**************POWERWELL VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.WATERMARK:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************WATERMARK VERIFICATION START**************")
                watermark = wm.DisplayWatermark()
                if False == watermark.verify_watermarks(gfx_index=gfx_index):
                    # Adding workaround to recheck watermark with 48Hz test condition set, this will make test to
                    # get current pixel clock from transcoder and use for calculation instead of OS returned pixel
                    # clock value, needed in DRRS cases when refresh rate can dynamically reduce in the middle of the
                    # test verification
                    logging.warning("WARN : Watermark mismatch - retrying for DRRS with lower refresh rate")
                    if False == watermark.verify_watermarks(is_48hz_test=True, gfx_index=gfx_index):
                        logging.error('FAIL : Watermark verification!')
                        logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                               msg='Watermark verification',
                                                                               res='FAIL'))
                        self.final_result.append('FAIL : Watermark verification')
                else:
                    logging.info('PASS : Watermark verification!')
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='Watermark verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : Watermark verification')
                logging.info("**************WATERMARK VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.FBC:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************FBC VERIFICATION START**************")
                if fbc.verify_fbc(gfx_index) is False:
                    logging.error('FAIL : FBC verification!')
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='FBC verification', res='FAIL'))
                    self.final_result.append('FAIL : FBC verification')
                else:
                    logging.info('PASS : FBC verification!')
                    self.final_result.append('PASS : FBC verification')
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='FBC verification', res='PASS'))
                logging.info("**************FBC VERIFICATION END**************")
                html.step_end()
            if method == VerificationMethod.PHY_BUF:
                self.sequence_counter = round(self.sequence_counter + 0.1, 2)
                html.step_start("**************PHY BUFFER VERIFICATION START**************")
                if False == de_base_interface.verify_phy_buffer_programming(portList, ddiList, gfx_index):
                    # GDHM handled in VerifyPhyBufferProgramming() in display_phy_buffer.py
                    logging.error("FAIL : PHY BUFFER Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='PHY BUFFER Programming verification',
                                                                           res='FAIL'))
                    self.final_result.append('FAIL : PHY BUFFER Programming verification')
                else:
                    logging.info("PASS : PHY BUFFER Programming verification!")
                    logging.log(FLOW_LOG, self.test_sequence_format.format(seq=self.sequence_counter,
                                                                           msg='PHY BUFFER Programming verification',
                                                                           res='PASS'))
                    self.final_result.append('PASS : PHY BUFFER Programming verification')
                logging.info("**************PHY BUFFER VERIFICATION END**************")
                html.step_end()

        self.sequence_counter = math.floor(self.sequence_counter) + 1.0
        html.step_start("**************VERIFICATION RESULTS**************")
        for results in self.final_result:
            logging.info("{}".format(results))
        self.print_skip_verification_message()
        html.step_end()
        if any('FAIL' in results for results in self.final_result):
            return False
        return True

    ##
    # @brief        prints skip verification message if any verification is called and the skipped
    # @return       None
    def print_skip_verification_message(self):
        diff = list(set(self.master_verification_list) - set(self.verification_list))
        for verify_method in diff:
            if verify_method == VerificationMethod.CLOCK:
                logging.info("INFO : Clock Verification Not Tested")
            if verify_method == VerificationMethod.PLANE:
                logging.info("INFO : Plane Programming verification Not Tested")
            if verify_method == VerificationMethod.PIPE:
                logging.info("INFO : Pipe Programming verification Not Tested")
            if verify_method == VerificationMethod.TRANSCODER:
                logging.info("INFO : Port Programming verification Not Tested")
            if verify_method == VerificationMethod.DDI:
                logging.info("INFO : DDI Programming verification Not Tested")
            if verify_method == VerificationMethod.DIP_CTRL:
                logging.info("INFO : DIP CTRL Programming verification Not Tested")
            if verify_method == VerificationMethod.POWERWELL:
                logging.info("INFO : Powerwell verification Not Tested")
            if verify_method == VerificationMethod.WATERMARK:
                logging.info('INFO : Watermark verification Not Tested')
            if verify_method == VerificationMethod.FBC:
                logging.info('INFO : FBC verification Not Tested')
            if verify_method == VerificationMethod.PHY_BUF:
                logging.info('INFO : PhyBuffer verification Not Tested')

    ##
    # @brief        Checks for the platform default verifications from config.ini
    # @param[in]    gfx_index - graphics adapter
    # @return       bool - true if verifier list set properly
    def get_platform_verifiers(self, gfx_index='gfx_0'):
        config_file = os.path.join(test_context.TestContext.root_folder(), "Libs\\Core\\test_env\\config.ini")
        self.bits = None
        platform = None
        if not os.path.exists(os.path.dirname(config_file)):
            logging.error("Config.ini file not exists")
            return 0x0
        else:
            gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
            # WA : currently test are execute on single platform. so loop break after 1 st iteration.
            # once Enable MultiAdapter remove the break statement.
            platform = gfx_display_hwinfo[int(gfx_index[-1])].DisplayAdapterName

            logging.debug("Platform = {}".format(platform))
            with open(config_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if platform in line:
                        temp = line.split(" = ")
                        for counter in range(0, len(temp)):
                            if temp[counter] == platform:
                                self.bits = temp[counter + 1]
                        break
        flag = flags()
        flag.asbyte = int(self.bits, 16)
        if flag.bit.clock_verifier:
            self.add_verifiers(VerificationMethod.CLOCK)
        if flag.bit.plane_verifier:
            self.add_verifiers(VerificationMethod.PLANE)
        if flag.bit.pipe_verifier:
            self.add_verifiers(VerificationMethod.PIPE)
        if flag.bit.transcoder_verifier:
            self.add_verifiers(VerificationMethod.TRANSCODER)
        if flag.bit.ddi_verifier:
            self.add_verifiers(VerificationMethod.DDI)
        if flag.bit.powerwell_verifier:
            self.add_verifiers(VerificationMethod.POWERWELL)
        if flag.bit.watermark_verifier:
            self.add_verifiers(VerificationMethod.WATERMARK)
        if flag.bit.dip_ctrl_verifier:
            self.add_verifiers(VerificationMethod.DIP_CTRL)
        if flag.bit.fbc_verifier:
            self.add_verifiers(VerificationMethod.FBC)
        if flag.bit.phy_buf_verifier:
            self.add_verifiers(VerificationMethod.PHY_BUF)
        return True

    ##
    # @brief        Function to override the verification mechanisms
    # @param[in]    value - contains details of verifications which need to be off
    # @return       bool - true if verifier list set properly
    def modify_display_engine_verifiers(self, value):
        self.verification_list = []
        self.get_platform_verifiers()
        flag = flags()
        flag.asbyte = int(value, 16)
        if not flag.bit.clock_verifier:
            self.remove_verifiers(VerificationMethod.CLOCK)
        if not flag.bit.plane_verifier:
            self.remove_verifiers(VerificationMethod.PLANE)
        if not flag.bit.pipe_verifier:
            self.remove_verifiers(VerificationMethod.PIPE)
        if not flag.bit.transcoder_verifier:
            self.remove_verifiers(VerificationMethod.TRANSCODER)
        if not flag.bit.ddi_verifier:
            self.remove_verifiers(VerificationMethod.DDI)
        if not flag.bit.powerwell_verifier:
            self.remove_verifiers(VerificationMethod.POWERWELL)
        if not flag.bit.watermark_verifier:
            self.remove_verifiers(VerificationMethod.WATERMARK)
        if not flag.bit.dip_ctrl_verifier:
            self.remove_verifiers(VerificationMethod.DIP_CTRL)
        if not flag.bit.fbc_verifier:
            self.remove_verifiers(VerificationMethod.FBC)
        if not flag.bit.phy_buf_verifier:
            self.remove_verifiers(VerificationMethod.PHY_BUF)
        return True

    ##
    # @brief        Provide details for platform defualt features enable/disable from config.ini
    # @return       features - disable/enable bits, refer help in config.ini for more details
    def get_global_feature_control_flags(self):
        config_file = os.path.join(test_context.TestContext.root_folder(), "Libs\\Core\\test_env\\config.ini")
        platform = None
        if not os.path.exists(os.path.dirname(config_file)):
            logging.error("Config.ini file not exists")
            return 0x0
        else:
            gfx_display_hwinfo = self.machine_info.get_gfx_display_hardwareinfo()
            # WA : currently test are execute on single platform. so loop break after 1 st iteration.
            # once Enable MultiAdapter remove the break statement.
            for i in range(len(gfx_display_hwinfo)):
                platform = gfx_display_hwinfo[i].DisplayAdapterName
                break
            logging.info("Platform = {}".format(platform))
            with open(config_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if platform in line:
                        temp = line.split(" = ")
                        for counter in range(0, len(temp)):
                            if temp[counter] == platform:
                                logging.info("Global Feature Control Flag = {}".format(temp[counter + 1]))
                                return temp[counter + 1]
