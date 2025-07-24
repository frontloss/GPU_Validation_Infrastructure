#######################################################################################################################
# @file         verify_hdcp_flow.py
# @brief        HDCP authentication flow verification
# @details       Contains HDCP 1.4 & 2.2 Flow verification APIs for DP & HDMI
#
# @author       Chandrakanth Reddy
#######################################################################################################################
import logging

from Libs.Core import registry_access
from Libs.Core import driver_escape
from Libs.Core import etl_parser
from Libs.Core.display_config import display_config
from Libs.Core.display_config import display_config_enums as cfg_enum
from Libs.Feature.display_engine.de_base.display_base import DisplayBase
from Tests.HDCP.hdcp_dpcd import *
from Tests.PowerCons.Modules import common
from registers.mmioregister import MMIORegister

__MAX_POLL_COUNT = 2

hdmi_repeater = False
dp_repeater = False
dp_mst = False
dp_2_2_repeater = False
dp_2_2_repeater_ready = False
dp_repeater_ready = False
dp_link_lost = False
dp_r_prime_ready = False
dp_2_2_re_auth = None
dp_2_2_link_lost = None
hdmi_repeater_ready = False
hdmi_link_lost = False
hdmi_r_prime_ready = None
hdmi_2_2_repeater_ready = None
hdmi_2_2_re_auth = None
hdcp_dp_legacy_device_connected = False
hdcp_hdmi_legacy_device_connected = False


##
# @brief Exposed Class for Panel with attributes
class Panel:
    name = None
    port = None
    pipe = None
    transcoder = None
    panel_type = None
    aux = None
    gfx_index = 'gfx_0'


##
# @brief Exposed enum class for HDCP 2.2 authentication steps
class HDCP2_AUTHENTICATION_STEP(enum.IntEnum):
    UNKNOWN = 0x0
    AKE_INIT = 0x2
    AKE_SEND_CERT = 0x3
    AKE_NO_STORED_KM = 0x4
    AKE_STORED_KM = 0x5
    AKE_SEND_H_PRIME = 0x7
    AKE_SEND_PAIRING_INFO = 0x8
    LC_INIT = 0x9
    LC_SEND_L_PRIME = 0xA
    SKE_SEND_EKS = 0xB
    REPEATER_AUTH_SEND_RECEIVER_ID_LIST = 0xC
    REPEATER_AUTH_SEND_ACK = 0xF
    REPEATER_AUTH_STREAM_MANAGE = 0x10
    REPEATER_AUTH_STREAM_READY = 0x11


##
# @brief Exposed enum class for supported Transcoder modes
class TRANS_DDI_MODE_SELECT(enum.IntEnum):
    TRANS_DDI_MODE_HDMI = 0x0  # Function in HDMI mode
    TRANS_DDI_MODE_DVI = 0x1  # Function in DVI mode
    TRANS_DDI_MODE_DP_SST = 0x2  # Function in DisplayPort SST mode
    TRANS_DDI_MODE_DP_MST = 0x3  # Function in DisplayPort MST mode


def __read_dpcd(panel, offset):
    target_id = None

    display_config_ = display_config.DisplayConfiguration()
    enumerated_displays = display_config_.get_enumerated_display_info()
    assert enumerated_displays

    for display_index in range(enumerated_displays.Count):
        display_info = enumerated_displays.ConnectedDisplays[display_index]
        port = cfg_enum.CONNECTOR_PORT_TYPE(display_info.ConnectorNPortType).name
        if panel.name == port and panel.gfx_index == display_info.DisplayAndAdapterInfo.adapterInfo.gfxIndex:
            target_id = display_info.TargetID
            break

    if target_id is None:
        logging.error("targetID is not found in the enumerated displays")
        return None
    ##
    # Read DPCD
    poll_count = 0
    dpcd_value = None
    while poll_count < __MAX_POLL_COUNT:
        dpcd_flag, dpcd_value = driver_escape.read_dpcd(target_id, offset)
        if dpcd_flag:
            break
        poll_count += 1

    if poll_count == __MAX_POLL_COUNT:
        logging.error("\tDPCD read failed for target id= {0} (Poll Count= {1})".format(target_id, poll_count))
        return None

    ##
    # Warn if poll count is greater than 1
    if poll_count != 0:
        logging.warning("\tDPCD read passed for target id= {0} (Poll Count= {1})".format(target_id, poll_count))

    logging.debug("\tDPCD Read: Offset={0}, Size=1 byte, Data= {1}".format(hex(offset), hex(dpcd_value[0])))
    return dpcd_value[0]


def __get_byte_val(val):
    return int(val.Data.replace('-', ''), 16)


def __get_msg_id(val):
    return int(val.Data.replace('-', '')[:NIBBLE_PER_BYTE], 16)


def __convert_to_little_endian(val):
    b = bytearray.fromhex(val.Data.replace('-', ''))
    return int.from_bytes(b, byteorder='little')


def __extract_bytes(val, start_byte, end_byte):
    start = start_byte * NIBBLE_PER_BYTE
    end = end_byte * NIBBLE_PER_BYTE
    if start:
        end = end_byte * NIBBLE_PER_BYTE + NIBBLE_PER_BYTE
    return int(val.Data.replace('-', '')[start: end], 16)


def __get_next_ksv(ksv, ksv_fifo_size):
    for i in range(0, ksv_fifo_size, KSV_SIZE):
        yield ksv[i:(i + KSV_SIZE)]


def __is_ksv_valid(ksv_list):
    count = 0
    if ksv_list is None:
        logging.error("KSV Data is Empty")
        return False
    else:
        for ksv in ksv_list:
            for bit in range(8):
                if (int(ksv, 16) >> bit) & 1:
                    count += 1
        return count == 20


def __verify_ri_prime(panel, start_time, end_time):
    prev_time_stamp = 0
    if "DP" == panel.panel_type:
        ri_data = etl_parser.get_dpcd_data(HDCP_1_4_DP_OFFSETS.RI_PRIME, channel='AUX_CHANNEL_' + panel.aux,
                                           start_time=start_time, end_time=end_time)
    else:
        ri_data = etl_parser.get_i2c_data(panel.port, I2C_RX_SLAVE_ADDRESS, HDCP_1_4_HDMI_OFFSETS.RI_PRIME,
                                          start_time=start_time, end_time=end_time)

    if ri_data is not None:
        for value in ri_data:
            if prev_time_stamp and int(value.TimeStamp - prev_time_stamp) < HDCP1_RI_PRIME_READ_TIMEOUT_IN_MS:
                continue
            if __get_byte_val(value) == 0x0:
                logging.error("RI Prime value can't be Zero")
                return False
            if prev_time_stamp and int(value.TimeStamp - prev_time_stamp) > HDCP1_RI_PRIME_READ_MAX_TIMEOUT_IN_MS:
                logging.error("RI Prime is read after {} m secs".format(HDCP1_RI_PRIME_READ_MAX_TIMEOUT_IN_MS))
                return False
            prev_time_stamp = value.TimeStamp
    else:
        logging.error("RI Prime value is not received from panel between {0} and {1}".format(start_time, end_time))
        return False
    return True


def __read_r0_prime(panel, start_time, end_time):
    if "DP" == panel.panel_type:
        data = etl_parser.get_dpcd_data(HDCP_1_4_DP_OFFSETS.RI_PRIME, channel='AUX_CHANNEL_' + panel.aux,
                                        start_time=start_time, end_time=end_time)
    else:
        data = etl_parser.get_i2c_data(panel.port, I2C_RX_SLAVE_ADDRESS, HDCP_1_4_HDMI_OFFSETS.RI_PRIME,
                                       start_time=start_time, end_time=end_time)
    if data is not None:
        value = __get_byte_val(data[0])
        if not value:
            logging.error("R0 Prime value is Zero - {}".format(value))
            return False
    else:
        logging.error("R0 Prime read doesn't Happened between {0} and {1}".format(start_time, end_time))
        return False
    return True


def __verify_dp_repeater_topology(aux, start_time, end_time):
    current_device_count = None
    current_depth = None
    binfo = DP_BINFO_REGISTER()

    topology_list = etl_parser.get_dpcd_data(binfo.offset, channel='AUX_CHANNEL_' + aux, start_time=start_time,
                                             end_time=end_time)

    if topology_list:
        for val in topology_list:
            binfo.value = __convert_to_little_endian(val)
            if current_device_count != binfo.DeviceCount:
                current_device_count = binfo.DeviceCount
                logging.info("\tCurrent No.of Downstream Devices attached = {}".format(current_device_count))
            if current_depth != binfo.Depth:
                current_depth = binfo.Depth
                logging.info("\tCurrent No.of Repeater Levels connected = {}".format(current_depth))
            if binfo.MaxDevsExceeded:
                logging.error("\tMore than 127 devices connected for the Receiver")
                return False, current_device_count
            if binfo.MaxCascadeExceeded:
                logging.error("\tMore than 7 levels of Repeater connected")
                return False, current_device_count
            if current_depth > HDCP1_MAX_DEPTH and binfo.MaxCascadeExceeded == 0:
                logging.error("\tMaxCascadeLevelExceeded bit is not set by panel for depth {}".format(current_depth))
                return False, current_device_count
            if current_device_count > HDCP1_MAX_DOWNSTREAM_DEVICES and binfo.MaxDevsExceeded == 0:
                logging.error("\tMaxDevicesExceeded bit is not set by panel for device count {}".format(current_device_count))
                return False, current_device_count
    else:
        logging.error("\tBINFO read not happened between {0} and {1}".format(start_time, end_time))
        return False, current_device_count
    return True, current_device_count


def __read_dp_bcaps(aux, start_time, end_time):
    global dp_repeater
    dp_repeater = False

    bcaps = DP_BCAPS_REGISTER()
    bcaps_data = etl_parser.get_dpcd_data(bcaps.offset, channel='AUX_CHANNEL_' + aux, start_time=start_time, end_time=end_time)
    logging.debug("\tBcaps Register Read count = {}".format(len(bcaps_data)))
    if bcaps_data:
        bcaps.value = __get_byte_val(bcaps_data[-1])
        if not bcaps.HDCPCapable:
            logging.error("\tHDCP 1.4  is not supported on the panel")
            return False
        logging.info("\tHDCP 1.4 is supported on the Panel")
        if bcaps.IsRepeater:
            dp_repeater = True
            logging.info("\tAttached Downstream device is a HDCP Repeater")
    else:
        logging.error("\tNo Bcaps read happened between {0} and {1}".format(start_time, end_time))
        return False
    return True


def __read_hdmi_bcaps(port, start_time, end_time):
    global hdmi_repeater, hdmi_repeater_ready
    hdmi_repeater, hdmi_repeater_ready = False, False

    bcaps = HDMI_BCAPS_REGISTER()
    bcaps_data = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, bcaps.offset, start_time=start_time, end_time=end_time)
    if bcaps_data:
        for val in bcaps_data:
            bcaps.value = __get_byte_val(val)
            if bcaps.IsRepeater:
                hdmi_repeater = True
                logging.info("\tAttached Downstream device is a Repeater")
            if bcaps.KSVFifoReady:
                hdmi_repeater_ready = True
                logging.info("\tRepeater READY Bit is set at {}".format(val.TimeStamp))
    else:
        logging.error("\tNo Bcaps read happened between {0} and {1}".format(start_time, end_time))
        return False
    return True


def __check_for_re_auth(start, end):
    global hdmi_2_2_re_auth
    if hdmi_2_2_re_auth and (start < hdmi_2_2_re_auth < end):
        logging.error("\tRe-auth requested by RX at {}".format(hdmi_2_2_re_auth))
        return True
    return False


def __check_dp_re_auth_link_lost(start, end):
    global dp_2_2_re_auth, dp_2_2_link_lost

    if dp_2_2_re_auth and start < dp_2_2_re_auth < end:
        logging.error("\tRe-auth requested by RX at {}".format(dp_2_2_re_auth))
        return True
    if dp_2_2_link_lost and (start < dp_2_2_link_lost < end):
        logging.error("\tLink lost reported by RX at {}".format(dp_2_2_re_auth))
        return True
    return False


def __read_i2c_offset(port, check_id, start_time, end_time, is_write=False):
    if is_write:
        offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_WRITE_OFFSET
    else:
        offset = HDCP2_HDMI_OFFSETS.HDCP2_HDMI_READ_OFFSET
    msg = "sent" if is_write else "received"
    error_msg = "\t{0} msg is not {1} with in {2} m secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, msg,
                                                                 end_time - start_time)
    res = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, offset, start_time=start_time, end_time=end_time)
    if res is None:
        logging.error(error_msg)
        return False, None
    for val in res:
        msg_id = __get_msg_id(val)
        if msg_id == check_id:
            logging.info(
                "\t{0} msg {1} with in {2} m sec".format(HDCP2_AUTHENTICATION_STEP(check_id).name, msg,
                                                         end_time - start_time))
            return True, val.TimeStamp
    logging.error(error_msg)
    return False, None


##
# @brief       Method to get the KSV list from panel for HDMI & DP
# @param[in]   offset address
# @param[in]   panel panel object
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      None if I2C read is failed otherwise ksv_list
def get_ksv_list(offset, panel, start_time=None, end_time=None):
    if "DP" == panel.panel_type:
        ksv_data = etl_parser.get_dpcd_data(offset, channel='AUX_CHANNEL_' + panel.aux, start_time=start_time,
                                            end_time=end_time)
    else:
        ksv_data = etl_parser.get_i2c_data(panel.port, I2C_RX_SLAVE_ADDRESS, offset, start_time=start_time, end_time=end_time)
    if ksv_data:
        ksv_list = ksv_data[-1].Data
        return ksv_list.split('-')
    return None


##
# @brief       Method to get the HDMI KSV list from panel
# @param[in]   port port
# @param[in]   offset I2C offset
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      None if I2C read is failed otherwise ksv_list
def get_hdmi_ksv_list(port, offset, start_time=None, end_time=None):
    ksv_data = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, offset, start_time=start_time, end_time=end_time)
    if ksv_data:
        ksv_list = ksv_data[-1].Data
        return ksv_list.split('-')
    return None


##
# @brief       Method to get the HDCP1.4 KSV FIFO from repeater
# @param[in]   offset I2C offset
# @param[in]   device_count downstream device count
# @param[in]   panel panel object
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if read is successful otherwise False
def read_ksv_fifo(offset, device_count, panel, start_time=None, end_time=None):
    ksv = get_ksv_list(offset, panel, start_time, end_time)
    if ksv:
        expected_size = device_count * KSV_SIZE
        if expected_size != len(ksv):
            logging.error("\tKSV FIFO Data doesn't match with Device count. Expected = {0} Actual = {1}".format(expected_size, len(ksv)))
            return False
        for data in __get_next_ksv(ksv, expected_size):
            if __is_ksv_valid(data) is False:
                logging.error("\tInvalid KSV List :{}".format(data))
                return False
    else:
        logging.error("\tKSV Data is Empty")
        return False
    return True


##
# @brief       Method to get & verify the HDCP1.4 Bstatus DPCD data for DP
# @param[in]   aux AUX channel A/B
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def read_dp_bstatus(aux, start_time, end_time):
    global dp_repeater_ready, dp_link_lost, dp_r_prime_ready

    dp_repeater_ready, dp_link_lost, dp_r_prime_ready = None, None, None

    bstatus = DP_BSTATUS_REGISTER()
    bstatus_data = etl_parser.get_dpcd_data(bstatus.offset, channel='AUX_CHANNEL_' + aux, start_time=start_time,
                                            end_time=end_time)
    logging.debug("\tBstatus read count = {}".format(len(bstatus_data)))

    if bstatus_data:
        for val in bstatus_data:
            bstatus.value = __get_byte_val(val)
            if bstatus.KSVFifoReady:
                dp_repeater_ready = val.TimeStamp
            if bstatus.LinkIntegrityFailed:
                logging.error("\tHDCP Receiver Link Lost at {}".format(val.TimeStamp))
                dp_link_lost = val.TimeStamp
                return False
            if bstatus.RiAvailable:
                logging.debug("\tR0' available at {}".format(val.TimeStamp))
                dp_r_prime_ready = val.TimeStamp
    else:
        logging.error("\tNo BStatus read found")
        return False
    return True


def __verify_hdmi_repeater_topology(port, start_time, end_time):
    current_device_count = None
    current_depth = None

    bstatus = HDMI_BSTATUS_REGISTER()
    bstatus_data = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, bstatus.offset, start_time=start_time, end_time=end_time)
    logging.info("\tBstatus read count = {}".format(len(bstatus_data)))

    if bstatus_data:
        for val in bstatus_data:
            bstatus.value = __convert_to_little_endian(val)
            if current_device_count != bstatus.DeviceCount:
                current_device_count = bstatus.DeviceCount
                logging.info("\tCurrent No.of Downstream Devices attached = {}".format(current_device_count))
            if current_depth != bstatus.Depth:
                current_depth = bstatus.Depth
                logging.info("\tCurrent No.of Repeater Levels connected {}".format(current_depth))
            if bstatus.MaxDevsExceeded:
                logging.error("\tMore than 127 devices connected for the Receiver")
                return False, current_device_count
            if bstatus.MaxCascadeExceeded:
                logging.error("\tMore than 7 levels of Repeater connected")
                return False, current_device_count
            if current_depth > 7 and bstatus.MaxCascadeExceeded == 0:
                logging.error("\tMaxCascadeLevelExceeded bit is not set by panel for depth {}".format(current_depth))
                return False, current_device_count
            if current_device_count > 127 and bstatus.MaxDevsExceeded == 0:
                logging.error("\tMaxDevicesExceeded bit is not set by panel for device count {}".format(current_device_count))
                return False, current_device_count
    else:
        logging.error("\tNo BStatus read found")
        return False, current_device_count
    return True, current_device_count


##
# @brief       Method to get the HDCP2.2 RX Status DPCD data for DP
# @param[in]   aux AUX channel A/B
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if DPCD read is successful otherwise False
def read_dp_rx_status(aux='A', start_time=None, end_time=None):
    global dp_2_2_repeater_ready, dp_2_2_re_auth, dp_2_2_link_lost
    dp_2_2_re_auth, dp_2_2_link_lost, dp_2_2_repeater_ready = None, None, None

    rx_status = HDCP2_DP_RX_STATUS_REGISTER()
    rx_status_list = etl_parser.get_dpcd_data(rx_status.offset, channel='AUX_CHANNEL_' + aux, start_time=start_time,
                                              end_time=end_time)
    if rx_status_list:
        for val in rx_status_list:
            rx_status.value = __get_byte_val(val)
            if rx_status.Ready:
                logging.info("\tHDCP 2.3 - DP Repeater Ready set at {}".format(val.TimeStamp))
                dp_2_2_repeater_ready = val.TimeStamp
            if rx_status.ReauthReq:
                logging.error("\tRe-auth requested by Panel at {}".format(val.TimeStamp))
                dp_2_2_re_auth = val.TimeStamp
            if rx_status.LinkIntegrityFailure:
                logging.error("\tLink Integrity Failure reported by Panel at {}".format(val.TimeStamp))
                dp_2_2_link_lost = val.TimeStamp
            if rx_status.Havailable:
                logging.info("\tH available at {}".format(val.TimeStamp))
            if rx_status.PairingAvailable:
                logging.info("\tPairing available at {}".format(val.TimeStamp))
    else:
        logging.error("\tRX STATUS read not happened between {0} and {1}".format(start_time, end_time))
        return False
    return True


##
# @brief       Method to get the HDCP2.2 RX Status DPCD data for HDMI
# @param[in]   port port
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if I2C read is successful otherwise False
def read_hdmi_rx_status(port, start_time=None, end_time=None):
    global hdmi_2_2_repeater_ready, hdmi_2_2_re_auth

    hdmi_2_2_repeater_ready, hdmi_2_2_re_auth = None, None

    rx_status = HDCP2_HDMI_RX_STATUS_REGISTER()
    rx_status_list = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, rx_status.offset, start_time=start_time,
                                             end_time=end_time)
    if rx_status_list:
        for val in rx_status_list:
            rx_status.value = __convert_to_little_endian(val)  # Data format - Byte1, Byte2
            if rx_status.Ready:
                logging.info("\tHDCP 2.3 - HDMI Repeater Ready set at {}".format(val.TimeStamp))
                hdmi_2_2_repeater_ready = val.TimeStamp
            if rx_status.ReauthReq:
                logging.error("\tRe-auth request set at {}".format(val.TimeStamp))
                hdmi_2_2_re_auth = val.TimeStamp
    else:
        logging.error("\tHDMI RX STATUS read not happened between {0} and {1}".format(start_time, end_time))
        return False
    return True


##
# @brief       Method to verify the HDCP2.2 RX INFO DPCD data for DP
# @param[in]   data dpcd data
# @return      True if verification is successful otherwise False
def verify_hdcp2_rx_info(data):
    global hdcp_dp_legacy_device_connected
    device_count = 0
    hdcp_dp_legacy_device_connected = False
    rx_info = HDCP2_DP_RX_INFO_REGISTER()
    # Data ex: 02-10-00-00-00-3E-99-85-1B-00-1D-A3-1E-3A-58-9E
    rx_info.value = __get_byte_val(data)
    device_count = rx_info.DeviceCount
    if rx_info.MaxCascadeExceeded:
        logging.error("\tMore than 4 levels of repeaters are connected")
        return False, device_count
    if rx_info.MaxDeviceExceeded:
        logging.error("\tMore than 32 devices are connected to the Downstream Receiver")
        return False, device_count
    if device_count > HDCP2_MAX_DOWNSTREAM_DEVICES:
        logging.error("\tMaxDeviceExceeded bit is not set by Repeater for Device count = {}".format(rx_info.DeviceCount))
        return False, device_count
    if rx_info.Depth > HDCP2_MAX_DEPTH:
        logging.error("\tMaxCascadeExceeded bit is not set by Repeater for Depth = {}".format(rx_info.Depth))
        return False, device_count
    if rx_info.Hdcp2LegacyDeviceDownstream:
        logging.info("\tHDCP2.0 Legacy device is connected in Downstream")
        hdcp_dp_legacy_device_connected = True
    if rx_info.Hdcp1DeviceDownstream:
        logging.info("\tHDCP1.x device is connected in Downstream")
        hdcp_dp_legacy_device_connected = True
    return True, device_count


##
# @brief       This function is used to verify HDCP 2.2 Receiver Id's received from panel
# @param[in]   data DPCD data
# @param[in]   count device_count
# @return      True if verification is successful otherwise False
def verify_receiver_ids(data: str, count):
    # data ex: 29-DA-82-5E-60-74-E4-A7-0F-16-F7-42-6E-B1-FB-30
    ksv_list = data.split('-')[3:]
    length = len(ksv_list)
    logging.debug(f"KSV list = {ksv_list}")
    if length >= HDCP2_RECEIVER_IDS_MAX_LEN:
        logging.error("\tMax Receiver ID list of length {} received".format(length))
        return False
    if length != (count * 5):
        logging.error(f"\tExpected Receiver_ID's for device count : {count} Actual = {length//5}")
        return False
    for data in __get_next_ksv(ksv_list, count * 5):
        if __is_ksv_valid(data) is False:
            logging.error("\tInvalid KSV List :{}".format(data))
            return False
    return True


##
# @brief       This function is used to get hdcp 2.2 repeater topology information for HDMI
# @param[in]   val I2C read value
# @return      (True, device_count)
def verify_hdmi_2_2_rx_info(val: int):
    global hdcp_hdmi_legacy_device_connected
    device_count = 0
    rx_info = HDCP2_HDMI_RX_INFO_REGISTER()
    rx_info.value = val
    if rx_info.MaxCascadeExceeded:
        logging.error("\tMore than 4 levels of repeaters are connected")
        return False, device_count
    if rx_info.MaxDeviceExceeded:
        logging.error("\tMore than 32 devices are connected to the Downstream Receiver")
        return False, device_count
    if rx_info.DeviceCount > HDCP2_MAX_DOWNSTREAM_DEVICES:
        logging.error("\tMaxDeviceExceeded bit is not set by Repeater for Device count = {}".format(rx_info.DeviceCount))
        return False, device_count
    device_count = rx_info.DeviceCount
    if rx_info.Depth > HDCP2_MAX_DEPTH:
        logging.error("\tMaxCascadeExceeded bit is not set by Repeater for Depth = {}".format(rx_info.Depth))
        return False, device_count
    if rx_info.Hdcp2LegacyDeviceDownstream:
        logging.info("\tHDCP2Legacy Device is connected in Downstream")
        hdcp_hdmi_legacy_device_connected = True
    if rx_info.Hdcp1DeviceDownstream:
        logging.info("\tHDCP1.x Device is connected in Downstream")
        hdcp_hdmi_legacy_device_connected = True
    return True, device_count


##
# @brief       This function is used to verify hdcp 2.2 repeater authentication flow for HDMI
# @param[in]   panel panel object
# @param[in]   stream_status hdcp_stream_status register instance
# @param[in]   start time_stamp value
# @param[in]   end   time_stamp value
# @return      True if HDCP verification is successful else return False
def verify_hdmi_2_2_repeater(panel, stream_status, start, end=None):
    start = None
    hdcp_type = None
    port = panel.port

    logging.info("\tVerifying HDMI Repeater Authentication")
    msg_id = HDCP2_AUTHENTICATION_STEP.UNKNOWN
    end = start + HDCP2_RECEIVER_IDS_READ_TIMEOUT_IN_MS
    check_id = HDCP2_AUTHENTICATION_STEP.REPEATER_AUTH_SEND_RECEIVER_ID_LIST
    res = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_READ_OFFSET,
                                  start_time=start, end_time=end)
    if res is None:
        logging.error("\tReceiver ID List is not received with in 3 sec")
        return False
    for val in res:
        msg_id = __get_msg_id(val)
        if msg_id == check_id:
            logging.info("\tReceiver ID list is received with in 3 sec")
            start = val.TimeStamp
            rx_info = __extract_bytes(val, 1, 2)
            status, device_count = verify_hdmi_2_2_rx_info(rx_info)
            if not status:
                return status
            receiver_ids = val.Data.replace('-', '')[22*NIBBLE_PER_BYTE: 22 + 5*device_count * NIBBLE_PER_BYTE]
            expected_size = device_count * KSV_SIZE * NIBBLE_PER_BYTE
            if expected_size != len(receiver_ids):
                logging.error(
                    "\tReceiver ID's Data doesn't match with Device count. Expected = {0} Actual = {1}".format(
                        expected_size,
                        len(receiver_ids)))
                return False
            for data in __get_next_ksv(receiver_ids, expected_size):
                if __is_ksv_valid(data) is False:
                    logging.error("\tInvalid KSV List :{}".format(data))
                    return False
            break
    if msg_id != check_id:
        logging.error("\t{} is not received with in 3 sec".format(HDCP2_AUTHENTICATION_STEP(check_id).name))
        return False
    end = start + HDCP2_REPEATER_AUTH_SEND_ACK_TIMEOUT_IN_MS
    check_id = HDCP2_AUTHENTICATION_STEP.REPEATER_AUTH_SEND_ACK
    res = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_WRITE_OFFSET,
                                  start_time=start, end_time=end)
    if res is None:
        logging.error("\tTX Didn't write {} with in 2 secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name))
        return False
    for v in res:
        msg_id = __get_msg_id(v)
        if msg_id == check_id:
            logging.info("\tTx write {} with in 2secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name))
            start = v.TimeStamp
            break
    if msg_id != check_id:
        logging.error("\tTX Didn't write {} with in 2 secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name))
        return False
    end = start + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
    check_id = HDCP2_AUTHENTICATION_STEP.REPEATER_AUTH_STREAM_MANAGE
    res = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_WRITE_OFFSET,
                                  start_time=start, end_time=end)
    if res is None:
        logging.error("\tTX Didn't write {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end-start))
        return False
    for v in res:
        msg_id = __get_msg_id(v)
        if msg_id == check_id:
            logging.error("\tTX writes {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end - start))
            start = v.TimeStamp
            k = __extract_bytes(v, 4, 5)
            stream_id_length = 2 * k
            stream_id_type = __extract_bytes(v, 6, 5 + stream_id_length)
            hdcp_type = stream_id_type
            break
    # check encryption is enabled after 100m secs
    if msg_id != check_id:
        logging.error("\tTX Didn't write {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end - start))
        return False
    end = start + HDCP2_REPEATER_AUTH_STREAM_READY_READ_TIMEOUT_IN_MS
    check_id = HDCP2_AUTHENTICATION_STEP.REPEATER_AUTH_STREAM_READY
    res = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_READ_OFFSET,
                                  start_time=start, end_time=end)
    if res is None:
        logging.error("\tPanel Didn't write {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end - start))
        return False
    for v in res:
        msg_id = __get_msg_id(v)
        if msg_id == check_id:
            logging.error("\tPanel writes {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end - start))
            break
    if msg_id != check_id:
        logging.error("\tPanel Didn't write {0} in {1} secs".format(HDCP2_AUTHENTICATION_STEP(check_id).name, end-start))
        return False
    start_time = end + 100
    if check_hdcp_2_2_repeater_status(panel, stream_status, hdcp_type, start_time) is False:
        return False
    return True


##
# @brief       This function is used to verify hdcp 2.2 authentication flow for HDMI
# @param[in]   adapter platform_name
# @param[in]   panel panel object
# @param[in]   hdcp_status hdcp_status register instance
# @param[in]   stream_status hdcp_stream_status register instance
# @return      True if HDCP verification is successful else return False
def verify_hdmi_2_2(adapter, panel, hdcp_status, stream_status):
    global hdmi_2_2_re_auth, hdmi_2_2_repeater_ready

    hdcp_2_2_repeater = False
    pairing_check = False
    hdmi_mode = False
    port = panel.port
    registry_name = "HdmiNoNullPacketAndAudio"

    version = HDCP2_HDMI_VERSION_REGISTER()
    rx_caps = HDCP2_HDMI_RX_CAPS_REGISTER()

    ddi_ctl = MMIORegister.get_instance("TRANS_DDI_FUNC_CTL_REGISTER", "TRANS_DDI_FUNC_CTL_" + panel.transcoder, adapter)

    ddi_ctl_status = etl_parser.get_mmio_data(ddi_ctl.offset)

    for val in ddi_ctl_status:
        ddi_ctl.asUint = val.Data

        diss_reg_args = registry_access.StateSeparationRegArgs(gfx_index='gfx_0')
        read_val, read_type = registry_access.read(args=diss_reg_args, reg_name=registry_name)

        # If "HdmiNoNullPacketAndAudio" is set, return true because DVI mode doesnt support HDCP and no
        # further verification is needed.
        if read_val == 1:
            logging.warning("DVI modes does not support HDCP. Exiting")
            return True

        if ddi_ctl.trans_ddi_mode_select == TRANS_DDI_MODE_SELECT.TRANS_DDI_MODE_HDMI:
            hdmi_mode = True
            break
    if hdmi_mode is False:
        logging.error("\tHDCP signaling for HDMI is not enabled in TRANS_DDI_FUNC_CTL_".format(panel.transcoder))
        return False
    hdcp_ver = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, version.offset)
    if hdcp_ver:
        for val in hdcp_ver:
            version.value = __get_byte_val(val)
            if not version.Version:
                logging.error("\tHDCP 2.2 is not supported on the panel")
                return False
    read_hdmi_rx_status(port)
    write_data = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_WRITE_OFFSET)
    if write_data is None:
        logging.error("\tHDCP 2.2 Authentication Write data is empty")
        return False
    for val in write_data:
        msg_id = __get_msg_id(val)
        if msg_id == HDCP2_AUTHENTICATION_STEP.AKE_INIT:
            auth_start = val.TimeStamp
            logging.info("\tAKE INIT MSG written by TX at {}".format(auth_start))
            # STEP 2- AKE_SEND_CERT MSG will be received from RX
            cert_msg = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS,
                                               HDCP2_HDMI_OFFSETS.HDCP2_HDMI_READ_OFFSET, start_time=auth_start,
                                               end_time=auth_start + HDCP2_RX_CERT_READ_TIMEOUT_IN_MS)
            if cert_msg is None:
                logging.error("\tRX_CERT_MSG is not received with in 100 msec")
                return False
            ake_cert = cert_msg[-1].Data.replace('-', '')
            msg = __get_msg_id(cert_msg[-1])
            if msg != HDCP2_AUTHENTICATION_STEP.AKE_SEND_CERT:
                logging.error(
                    "\tAKE_SEND_CERT msg not received . Received msg_id = {}".format(
                        HDCP2_AUTHENTICATION_STEP(msg).name))
                return False
            logging.info("\tRX_CERT_MSG is received with in 100 m sec")
            rx_caps.value = int(ake_cert[-6:], 16)
            if rx_caps.Version != 0x2:
                logging.error("\tHDCP 2.2 is not supported on the connected panel")
                return False
            if rx_caps.Repeater:
                hdcp_2_2_repeater = True
                logging.info("\tAttached Downstream is a HDCP 2.2 Repeater")
            start_time = cert_msg[-1].TimeStamp
            end_time = start_time + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
            if __check_for_re_auth(start_time, end_time):
                continue
            km = etl_parser.get_i2c_data(port, I2C_RX_SLAVE_ADDRESS, HDCP2_HDMI_OFFSETS.HDCP2_HDMI_WRITE_OFFSET,
                                         start_time=start_time, end_time=end_time)
            if km is None:
                logging.error(
                    "\tAKE STORED/NO STORED KM is not written by Tx between {0} and {1}".format(start_time, end_time))
                return False
            msg_id = __get_msg_id(km[0])
            if msg_id == HDCP2_AUTHENTICATION_STEP.AKE_NO_STORED_KM:
                start_time = km[0].TimeStamp
                end_time = start_time + HDCP2_NO_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS
                pairing_check = True
                logging.info("\tAKE_NO_STORED_KM is written by Tx at {}".format(start_time))
            elif msg_id == HDCP2_AUTHENTICATION_STEP.AKE_STORED_KM:
                start_time = km[0].TimeStamp
                end_time = start_time + HDCP2_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS
                logging.info("\tAKE_STORED_KM is written by Tx at {}".format(start_time))
            else:
                continue
            if msg_id not in [HDCP2_AUTHENTICATION_STEP.AKE_NO_STORED_KM, HDCP2_AUTHENTICATION_STEP.AKE_STORED_KM]:
                logging.error("\tAKE STORED/NO STORED KM is not written by Tx")
                return False
            if __check_for_re_auth(start_time, end_time):
                continue
            check_id = HDCP2_AUTHENTICATION_STEP.AKE_SEND_H_PRIME
            status, start_time = __read_i2c_offset(port, check_id, start_time, end_time, is_write=False)
            if not status:
                return False
            if pairing_check:
                end_time = start_time + HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS
                if __check_for_re_auth(start_time, end_time):
                    continue
                check_id = HDCP2_AUTHENTICATION_STEP.AKE_SEND_PAIRING_INFO
                status, start_time = __read_i2c_offset(port, check_id, start_time, end_time, is_write=False)
                if not status:
                    return False
            if __check_for_re_auth(start_time, end_time):
                continue
            end_time = start_time + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
            check_id = HDCP2_AUTHENTICATION_STEP.LC_INIT
            status, start_time = __read_i2c_offset(port, check_id, start_time, end_time, is_write=True)
            if not status:
                return False
            if __check_for_re_auth(start_time, end_time):
                continue
            end_time = start_time + HDCP2_L_PRIME_READ_TIMEOUT_IN_MS
            check_id = HDCP2_AUTHENTICATION_STEP.LC_SEND_L_PRIME
            status, start_time = __read_i2c_offset(port, check_id, start_time, end_time, is_write=False)
            if not status:
                return False
            if __check_for_re_auth(start_time, end_time):
                continue
            end_time = start_time + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
            check_id = HDCP2_AUTHENTICATION_STEP.SKE_SEND_EKS
            status, start_time = __read_i2c_offset(port, check_id, start_time, end_time, is_write=True)
            if not status:
                return False
            if __check_for_re_auth(start_time, end_time):
                continue
            if hdcp_2_2_repeater:
                if verify_hdmi_2_2_repeater(panel, stream_status, start_time, end_time) is False:
                    return False
            # Driver will always try to enable max level requested by APP
            # In Repeater case, if any HDCP 1.x is detected in downstream topology, content type will be changed to 0
            start_time = start_time + HDCP_WAIT_TIME_FOR_ENCRYPTION_ENABLE_IN_MS
            if check_hdcp_2_2_encryption_status(panel, hdcp_status, start_time=start_time) is False:
                return False
    return True


##
# @brief       This function is used to verify hdcp protection for the given displays
# @param[in]   adapter platform_name
# @param[in]   panel panel object
# @return      True if HDCP 2.2 verification is successful else return False
def verify_hdcp_2_2(adapter, panel):
    global dp_2_2_repeater, hdcp_dp_legacy_device_connected

    index = 0
    auth_restart = None
    dp_port = False
    mst_support = False
    dp_2_2_repeater = False

    if adapter in common.GEN_11_PLATFORMS:
        hdcp_status = MMIORegister.get_instance("HDCP2_STATUS_REGISTER", "HDCP2_STATUS_DDI" + panel.pipe, adapter)
        stream_status = MMIORegister.get_instance("HDCP2_STREAM_STATUS_REGISTER", "HDCP2_STREAM_STATUS_" + panel.pipe,
                                                  adapter)
    else:
        hdcp_status = MMIORegister.get_instance("HDCP2_STATUS_REGISTER", "HDCP2_STATUS_TC" + panel.pipe, adapter)
        stream_status = MMIORegister.get_instance("HDCP2_STREAM_STATUS_REGISTER", "HDCP2_STREAM_STATUS_TC" + panel.pipe,
                                                  adapter)
    logging.info("STEP : Verifying HDCP Type 1 Authentication flow on {}".format(panel.name))
    if "DP" == panel.panel_type:
        dp_port = True
    if dp_port:
        # check MST is supported on connected DP panel
        val = __read_dpcd(panel, DP_MST_CAPS)
        if val:
            mst_support = bool((val >> 0) & 1)
            logging.info("DP {0} Panel is connected on {1}".format("MST" if mst_support else "SST", panel.name))
        rx_caps = HDCP2_DP_RX_CAPS_REGISTER()
        rx_caps_list = etl_parser.get_dpcd_data(rx_caps.offset, channel='AUX_CHANNEL_' + panel.aux)
        if rx_caps_list:
            for val in rx_caps_list:
                rx_caps.value = __get_byte_val(val)
                if dp_port and rx_caps.HdcpCapable == 0:  # Applicable for only DP port
                    logging.error("\tHDCP is not supported on the connected Panel on {}".format(panel.port))
                    return False

        # AKE_INIT is start of HDCP 2.2 Authentication
        rtx_list = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_RTX, channel='AUX_CHANNEL_' + panel.aux)
        if rtx_list is None:
            logging.error("\tAKE_INIT msg is not written by TX")
            return False
        if not read_dp_rx_status(panel.aux):
            return False
        index += 1
        for val in rtx_list:
            auth_start = val.TimeStamp
            logging.info("\tAKE_INIT MSG sent by TX at {}".format(auth_start))
            if index < len(rtx_list):
                auth_restart = rtx_list[index].TimeStamp
            end = auth_start + HDCP2_RX_CERT_READ_TIMEOUT_IN_MS
            # STEP 2- AKE_SEND_CERT MSG will be received from RX
            cert_msg = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_CERT_RX, channel='AUX_CHANNEL_' + panel.aux, start_time=auth_start, end_time=end)
            if cert_msg is None:
                logging.error("\tRX_CERT_MSG is not received with in 100 msec")
                return False
            last_cert_msg_bytes = etl_parser.get_dpcd_data(0x6921B, channel='AUX_CHANNEL_' + panel.aux, start_time=auth_start, end_time=end)
            logging.info("\tAKE_SEND_CERT MSG received from RX at {}".format(last_cert_msg_bytes[-1].TimeStamp))
            data = last_cert_msg_bytes[-1].Data
            temp = data.replace('-', '')
            rx_caps.value = int(temp[5:], 16)
            if rx_caps.Version != 0x2:
                logging.error("\tHDCP 2.2 is not supported on the connected panel")
                return False
            if rx_caps.Repeater == 1:
                dp_2_2_repeater = True
                logging.info("\tAttached Downstream is a HDCP 2.2 Repeater")
            elif mst_support and (rx_caps.Repeater == 0):
                logging.error("HDCP Repeater bit is not set for DP MST Panel(Panel Issue)")
                return False
            start = last_cert_msg_bytes[-1].TimeStamp
            end = start + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
            if __check_dp_re_auth_link_lost(start, end):
                continue
            # STEP-3 AKE_NO_STORED_KM/AKE_STORED_KM msg
            no_stored_km = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_EKPUB_KM,
                                                    channel='AUX_CHANNEL_' + panel.aux, start_time=start, end_time=end)
            if no_stored_km is None:
                # check for Stored_KM msg
                stored_km = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_EKH_KM_TX,
                                                     channel='AUX_CHANNEL_' + panel.aux, start_time=start, end_time=end)
                if stored_km is None:
                    logging.error("\tAKE_STORED_KM/AKE_NO_STORED_KM is not sent by TX")
                    return False
                km = stored_km[-1].TimeStamp
                time_out = HDCP2_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS
                logging.info("\tAKE_STORED_KM sent by TX at {}".format(km))
            else:
                km = no_stored_km[-1].TimeStamp
                time_out = HDCP2_NO_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS
                logging.info("\tAKE_NO_STORED_KM sent by TX at {}".format(km))
            # H' Prime should be available with in 1 sec after AKE_NO_STORED_KM msg
            h_prime = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_HPRIME,
                                               channel='AUX_CHANNEL_' + panel.aux, start_time=km, end_time=km + time_out)
            if h_prime is None:
                logging.error("\tH PRIME is not received with in {} m sec".format(time_out))
                return False
            logging.info("\tH PRIME is received with in {} m sec".format(time_out))
            start = h_prime[-1].TimeStamp
            end = start + HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS
            if time_out == HDCP2_NO_STORED_KM_H_PRIME_READ_TIMEOUT_IN_MS:
                # check Pairing info only when Tx sent AKE_NO_STORED_KM
                if __check_dp_re_auth_link_lost(start, end):
                    continue
                pairing_info = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_EKH_KM_RX,
                                                        channel='AUX_CHANNEL_' + panel.aux,
                                                        start_time=start, end_time=end)
                if pairing_info is None:
                    logging.error(
                        "\tAKE_SEND_PAIRING_INFO not received in {} m sec".format(HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS))
                    return False
                logging.info("\tAKE_SEND_PAIRING_INFO received in {} m sec".format(HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS))
                start_time = pairing_info[-1].TimeStamp
            else:
                start_time = h_prime[-1].TimeStamp
            end = start_time + HDCP2_PAIRING_INFO_READ_TIMEOUT_IN_MS
            if __check_dp_re_auth_link_lost(start_time, end):
                continue
            # STEP 4: verify LOCALITY CHECK
            lc_init = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_RN, channel='AUX_CHANNEL_' + panel.aux,
                                               start_time=start_time, end_time=end)
            if lc_init is None:
                logging.error("\tLC_INIT not written by TX")
                return False
            start_time = lc_init[-1].TimeStamp
            logging.info("\tLC_INIT written by TX at {}".format(start_time))
            lc_prime = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_RN, channel='AUX_CHANNEL_' + panel.aux,
                                                start_time=start_time,
                                                end_time=start_time + HDCP2_L_PRIME_READ_TIMEOUT_IN_MS)
            if lc_prime is None:
                logging.error("\tLC_PRIME not received from Panel in {} m secs".format(HDCP2_L_PRIME_READ_TIMEOUT_IN_MS))
                return False
            logging.info("\tLC_PRIME received from Panel in {} m secs".format(HDCP2_L_PRIME_READ_TIMEOUT_IN_MS))
            start_time = lc_prime[-1].TimeStamp
            end = start_time + HDCP2_COMMON_AUTHENTICATION_STEP_TIMEOUT
            if __check_dp_re_auth_link_lost(start_time, end):
                continue
            # STEP 5: verify Session Key(ks) Exchange
            ks = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_EDKEY_KS, channel='AUX_CHANNEL_' + panel.aux,
                                          start_time=start_time, end_time=end)
            if ks is None:
                logging.error("\tSession key not written by TX")
                return False
            start_time = ks[-1].TimeStamp
            logging.info("\tSession key written by TX at {}".format(start_time))
            if __check_dp_re_auth_link_lost(start_time, end):
                continue
            if dp_2_2_repeater and dp_2_2_repeater_ready:
                logging.info("\tVerifying Repeater Authentication")
                time_out = HDCP2_RECEIVER_IDS_READ_TIMEOUT_IN_MS
                rx_info_list = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_RXINFO,
                                                        channel='AUX_CHANNEL_' + panel.aux,
                                                        start_time=dp_2_2_repeater_ready,
                                                        end_time=dp_2_2_repeater_ready + time_out)
                if rx_info_list is None:
                    logging.error(
                        f"\tReceiver ID list is not received within {time_out}m secs from Panel")
                    return False
                status, device_count = verify_hdcp2_rx_info(rx_info_list[-1])
                if status is False:
                    return False
                receiver_ids = etl_parser.get_dpcd_data(0x69342, channel='AUX_CHANNEL_' + panel.aux,
                                                        start_time=dp_2_2_repeater_ready,
                                                        end_time=dp_2_2_repeater_ready + time_out)
                if receiver_ids is None:
                    logging.error("\tReceiver ID List is Empty")
                    return False
                logging.info("\tReceiver ID List received with in 3 secs")
                if not verify_receiver_ids(receiver_ids[-1].Data, device_count):
                    return False
                time_out = HDCP2_REPEATER_AUTH_READ_TIMEOUT_IN_MS
                # STEP 6 : REPEATER AUTH ACK msg check
                auth_ack = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_V_TX, channel='AUX_CHANNEL_' + panel.aux,
                                                    start_time=dp_2_2_repeater_ready,
                                                    end_time=dp_2_2_repeater_ready + time_out)
                if auth_ack is None:
                    logging.error("\tRepeaterAuthSendAck msg is not sent by TX")
                    return False
                start_time = auth_ack[-1].TimeStamp
                logging.info("\tRepeaterAuthSendAck msg is sent by TX at {}".format(start_time))
                # STEP 7 : verify REPEATER STREAM MANAGE msg
                stream_msg = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_SEQ_NUM_M,
                                                      channel='AUX_CHANNEL_' + panel.aux,
                                                      start_time=start_time, end_time=auth_restart)
                if stream_msg is None:
                    logging.error("\tRepeaterAuthStreamManage msg is not sent by TX")
                    return False
                logging.info("\tRepeaterAuthStreamManage msg is sent by TX at {}".format(stream_msg[-1].TimeStamp))
                time_out = stream_msg[-1].TimeStamp + HDCP2_REPEATER_AUTH_STREAM_READY_READ_TIMEOUT_IN_MS
                data = stream_msg[-1].Data.replace('-', '')
                k = int(data[6:10], 16)
                stream_id_length = 2*k
                # Stream ID Type can be derived by the last byte of  RepeaterAuthStreamManage message
                stream_id_type = int(data[10 + stream_id_length*2 - 2:], 16)
                logging.info("\tEnabled Content Type = {}".format(stream_id_type))
                if hdcp_dp_legacy_device_connected and (stream_id_type != 0):
                    logging.error("\tContent Type 1 is enabled when legacy HDCP device is connected")
                    return False
                hdcp_type = stream_id_type
                stream_ready = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_M_RX,
                                                        channel='AUX_CHANNEL_' + panel.aux,
                                                        start_time=stream_msg[-1].TimeStamp, end_time=time_out)
                if stream_ready is None:
                    logging.error("\tRepeaterAuthStreamReady msg is not Received with in 100 msec from Panel")
                    return False
                logging.info("\tRepeaterAuthStreamReady msg is Received with in 100 msec from Panel")
                start_time = stream_ready[-1].TimeStamp
                if check_hdcp_2_2_repeater_status(panel, stream_status, hdcp_type, start_time) is False:
                    return False
            else:
                # HDCP receiver
                end_time = start_time + HDCP2_DP_ERRATA_TYPE_WRITE_TIMEOUT_IN_MS
                content_type = etl_parser.get_dpcd_data(HDCP2_DP_OFFSETS.HDCP2_DP_ERRATA_TYPE,
                                                        channel='AUX_CHANNEL_' + panel.aux,
                                                        start_time=start_time, end_time=end_time)
                if content_type is None:
                    logging.error("\tContent Type value not written by TX with in {} m secs".format(end_time-start_time))
                    return False
                hdcp_type = __get_byte_val(content_type[-1])
                logging.info("\tContent Type {} sent to Panel".format(hdcp_type))
                start_time = end_time + HDCP_WAIT_TIME_FOR_ENCRYPTION_ENABLE_IN_MS
            if check_hdcp_2_2_encryption_status(panel, hdcp_status, hdcp_type, start_time) is False:
                return False
    else:
        if verify_hdmi_2_2(adapter, panel, hdcp_status, stream_status) is False:
            return False
    logging.info("PASS: HDCP Type 1 Authentication flow verification successful on {}".format(panel.name))
    return True


##
# @brief       Method to verify DP repeater topology
# @param[in]   panel panel object
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def verify_dp_repeater(panel, start_time, end_time):
    global dp_repeater_ready

    if dp_repeater_ready is None or (dp_repeater_ready > end_time):
        logging.error("\tRepeater Ready Bit is not set within 5 secs")
        return False
    status, device_count = __verify_dp_repeater_topology(panel.aux, start_time, end_time)
    if not status:
        return False
    if not read_ksv_fifo(HDCP_1_4_DP_OFFSETS.KSV_FIFO, device_count, panel, start_time, end_time):
        return False
    return True


##
# @brief       Method to verify HDMI repeater topology
# @param[in]   panel panel object
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def verify_hdmi_repeater(panel, start_time, end_time):
    global hdmi_repeater_ready

    if hdmi_repeater_ready is None or (hdmi_repeater_ready > end_time):
        logging.error("\tRepeater Ready Bit is not set within 5 secs")
        return False
    status, device_count = __verify_hdmi_repeater_topology(panel.port, start_time, end_time)
    if not status:
        return False
    if not read_ksv_fifo(HDCP_1_4_HDMI_OFFSETS.KSV_FIFO, device_count, panel, start_time, end_time):
        return False
    return True


##
# @brief       Method to verify HDMI repeater topology
# @param[in]   panel panel object
# @param[in]   hdcp_status register instance
# @param[in]   hdcp_type 0/1
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def check_hdcp_2_2_encryption_status(panel, hdcp_status, hdcp_type=1, start_time=None, end_time=None):
    global dp_2_2_repeater, hdcp_dp_legacy_device_connected

    hdcp_data = etl_parser.get_mmio_data(hdcp_status.offset, start_time=start_time, end_time=end_time)
    if hdcp_data:
        hdcp_status.asUint = hdcp_data[-1].Data
        if not(hdcp_status.link_encryption_status and hdcp_status.link_authentication_status):
            logging.error("\tEncryption is not enabled in driver")
            return False
        logging.info("\tAuthentication completed and Encryption is enabled in driver on {}".format(panel.name))
        if hdcp_type != hdcp_status.link_type_status and (hdcp_dp_legacy_device_connected is False):
            logging.error("\tExpected content Type = {0} Actual = {1}".format(hdcp_type, hdcp_status.link_type_status))
            return False
        logging.info("\tEnabled content Type by driver = {0} on PIPE {1}".format(hdcp_status.link_type_status, panel.pipe))
    else:
        logging.error("\tHDCP2_STATUS_REGISTER mmio data not found")
        return False
    return True


##
# @brief       Method to verify HDCP 2.2 repeater stream encryption status using MMIO
# @param[in]   panel panel object
# @param[in]   stream_status register instance
# @param[in]   hdcp_type  0/1
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def check_hdcp_2_2_repeater_status(panel, stream_status, hdcp_type, start_time=None, end_time=None):
    if end_time is None:
        start_time = start_time + 1000
    stream_data = etl_parser.get_mmio_data(stream_status.offset, start_time=start_time, end_time=end_time)
    if stream_data:
        stream_status.asUint = stream_data[-1].Data
        if stream_status.stream_encryption_status:
            logging.info("\tPIPE {} Stream is encrypting".format(panel.pipe))
        else:
            logging.error("\tPIPE {} Stream is not encrypting".format(panel.pipe))
            return False
        if stream_status.stream_type_status != hdcp_type:
            logging.error("\tExpected stream type = {0} Actual = {1}".format(hdcp_type, stream_status.stream_type_status))
            return False
        logging.info("\tType {} stream is getting encrypted".format(stream_status.stream_type_status))
    else:
        logging.error("\tHDCP2_STREAM_STATUS_{} MMIO data not found".format(panel.pipe))
        return False
    return True


##
# @brief       Method to verify HDCP 1.4 encryption status using MMIO
# @param[in]   adapter platform_name
# @param[in]   panel panel object
# @param[in]   hdcp_status register instance
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def check_hdcp_encryption_status(adapter, panel, hdcp_status, start_time=None, end_time=None):
    global dp_repeater, dp_mst
    ri_mismatch_count = 0

    pipe = []
    hdcp_data = etl_parser.get_mmio_data(hdcp_status.offset, start_time=start_time, end_time=end_time)
    if hdcp_data:
        for status in hdcp_data:
            hdcp_status.asUint = status.Data
            if hdcp_status.link_encryption_status and hdcp_status.authentication_status:
                if hdcp_status.ri_prime_match_status == 0:
                    logging.debug("\tRI Prime mismatch at {}".format(status.TimeStamp))
                    ri_mismatch_count += 1
                else:
                    # reset the count
                    ri_mismatch_count = 0
        # After three continuous mismatch treat as a failure
        if ri_mismatch_count >= HDCP1_MAX_RI_RETRY:
            logging.error("\tRI Prime mismatch count".format(ri_mismatch_count))
            return False
        hdcp_status.asUint = hdcp_data[-1].Data
        if not (hdcp_status.link_encryption_status and hdcp_status.authentication_status):
            logging.error("\tHDCP encryption is not enabled by driver")
            return False
        logging.info("\tHDCP authentication completed and encryption is enabled by driver")
        # check stream encryption if both MST & Repeater are set
        if dp_repeater and dp_mst:
            if adapter not in common.GEN_11_PLATFORMS and hdcp_status.stream_encryption_status_d:
                logging.info("\tStream is getting encrypted on PIPE D")
                pipe.append('D')
            if hdcp_status.stream_encryption_status_c:
                logging.info("\tStream is getting encrypted on PIPE C")
                pipe.append('C')
            if hdcp_status.stream_encryption_status_b:
                logging.info("\tStream is getting encrypted on PIPE B")
                pipe.append('B')
            if hdcp_status.stream_encryption_status_a:
                logging.info("\tStream is getting encrypted on PIPE A")
                pipe.append('A')
            if panel.pipe not in pipe:
                logging.error("\tStream Encryption is not enabled on PIPE {}".format(panel.pipe))
                return False
    else:
        logging.error("\tHDCP STATUS Register Data is empty")
        return False
    return True


##
# @brief       Method to verify HDCP 1.4 repeater status using MMIO
# @param[in]   adapter platform_name
# @param[in]   panel panel object
# @param[in]   hdcp_rep register instance
# @param[in]   start_time time_stamp value
# @param[in]   end_time port time_stamp value
# @return      True if verification is successful otherwise False
def check_repeater_status(adapter, panel, hdcp_rep, start_time=None, end_time=None):
    repeater = []
    hdcp_rep_ctl = etl_parser.get_mmio_data(hdcp_rep.offset, start_time=start_time, end_time=end_time)
    if hdcp_rep_ctl:
        for val in hdcp_rep_ctl:
            hdcp_rep.asUint = val.Data
            if hdcp_rep.sha1_status == 0x4:
                logging.error("\tVPRIME Mismatch happened")
                return False
        hdcp_rep.asUint = hdcp_rep_ctl[-1].Data
        if adapter in common.GEN_11_PLATFORMS:
            if M0_SELECT_GEN11[hdcp_rep.sha1_m0_select] != panel.aux:
                logging.error(
                    "\tSHA-1 M0 value Expected = {0} Actual = {1}".format(M0_SELECT_GEN11[hdcp_rep.sha1_m0_select],
                                                                          panel.aux))
                return False
            if hdcp_rep.ddie_repeater_present:
                logging.info("\tREPEATER is connected to DDI E")
                repeater.append('E')
            if hdcp_rep.ddif_repeater_present:
                logging.info("\tREPEATER is connected to DDI F")
                repeater.append('F')
            if hdcp_rep.ddid_repeater_present:
                logging.info("\tREPEATER is connected to DDI D")
                repeater.append('D')
            if hdcp_rep.ddic_repeater_present:
                logging.info("\tREPEATER is connected to DDI C")
                repeater.append('C')
            if hdcp_rep.ddia_repeater_present:
                logging.info("\tREPEATER is connected to DDI A")
                repeater.append('A')
            if hdcp_rep.ddib_repeater_present:
                logging.info("\tREPEATER is connected to DDI B")
                repeater.append('B')
        else:
            if M0_SELECT[hdcp_rep.sha1_m0_select] != panel.transcoder:
                logging.error(
                    "\tSHA-1 M0 value Expected = {0} Actual = {1}".format(M0_SELECT[hdcp_rep.sha1_m0_select],
                                                                          panel.transcoder))
                return False
            if hdcp_rep.transcoder_d_repeater_present:
                logging.info("\tREPEATER is connected to transcoder D")
                repeater.append('D')
            if hdcp_rep.transcoder_c_repeater_present:
                logging.info("\tREPEATER is connected to transcoder C")
                repeater.append('C')
            if hdcp_rep.transcoder_b_repeater_present:
                logging.info("\tREPEATER is connected to transcoder B")
                repeater.append('B')
            if hdcp_rep.transcoder_a_repeater_present:
                logging.info("\tREPEATER is connected to transcoder A")
                repeater.append('A')
        if panel.transcoder not in repeater:
            logging.error("\tExpected repeater on transcoder = {0} Actual = {1}".format(panel.transcoder, repeater))
            return False
    else:
        logging.error("\tHDCP_REP_CONTROL data is empty")
        return False
    return True


##
# @brief       This function is used to verify hdcp protection for the given displays
# @param[in]   adapter platform_name
# @param[in]   panel panel object
# @return      True if HDCP 1.4 verification is successful else return False
def verify_hdcp_1_4(adapter, panel):
    global dp_repeater_ready, dp_repeater, dp_r_prime_ready, dp_link_lost, dp_mst
    global hdmi_repeater

    auth_restart = None
    index = 0
    dp_port = False

    logging.info("STEP : Verify HDCP 1.4 Authentication flow on {}".format(panel.name))
    if adapter in common.GEN_11_PLATFORMS:
        hdcp_status = MMIORegister.get_instance("HDCP_STATUS_REGISTER", "HDCP_STATUS_DDI" + panel.pipe, adapter)
    else:
        hdcp_status = MMIORegister.get_instance("HDCP_STATUS_REGISTER", "HDCP_STATUS_TC" + panel.pipe, adapter)
    rep_ctl = MMIORegister.get_instance("HDCP_REP_CONTROL_REGISTER", "HDCP_REP_CONTROL", adapter)

    if 'DP' == panel.panel_type:
        dp_port = True
        # check MST is supported on connected DP panel
        val = __read_dpcd(panel, DP_MST_CAPS)
        if val:
            dp_mst = bool((val >> 0) & 1)
            logging.info("DP {0} Panel is connected on {1}".format("MST" if dp_mst else "SST", panel.name))
    if dp_port:
        aksv_data = etl_parser.get_dpcd_data(HDCP_1_4_DP_OFFSETS.AKSV, channel='AUX_CHANNEL_' + panel.aux)
    else:
        aksv_data = etl_parser.get_i2c_data(panel.port, I2C_RX_SLAVE_ADDRESS, HDCP_1_4_HDMI_OFFSETS.AKSV)

    if aksv_data:
        for ksv in aksv_data:
            index += 1
            auth_start = ksv.TimeStamp
            logging.info("\tIteration {0} verification started on PIPE {1}".format(index, panel.pipe))
            logging.info("\tAKSV Written by TX at {}".format(auth_start))
            if index < len(aksv_data):
                auth_restart = aksv_data[index].TimeStamp
            if dp_port:
                if __read_dp_bcaps(panel.aux, start_time=auth_start, end_time=auth_restart) is False:
                    return False
                bksv = get_ksv_list(HDCP_1_4_DP_OFFSETS.BKSV, panel, start_time=auth_start, end_time=auth_restart)
            else:
                if __read_hdmi_bcaps(panel.port, start_time=auth_start, end_time=auth_restart) is False:
                    return False
                bksv = get_ksv_list(HDCP_1_4_HDMI_OFFSETS.BKSV, panel, start_time=auth_start, end_time=auth_restart)
            if __is_ksv_valid(bksv) is False:
                logging.error("\tInvalid BKSV - {} received from the panel".format(bksv))
                return False
            logging.info("\tValid BKSV received from Panel")
            if dp_port:
                if read_dp_bstatus(panel.aux, start_time=auth_start, end_time=auth_restart) is False:
                    return False
                if dp_mst and (dp_repeater is False):
                    logging.error("HDCP repeater bit is not set for DP MST Panel(Panel Issue)")
                    return False
            # TX should read R0' after 100 msecs
            start_time = auth_start + HDCP1_R0_READ_TIMEOUT_IN_MS
            if not __read_r0_prime(panel, start_time=start_time, end_time=auth_restart):
                return False
            logging.info("\tValid R0' value received and First Stage of authentication successful")
            # check encryption is enabled or not
            if check_hdcp_encryption_status(adapter, panel, hdcp_status, start_time) is False:
                return False
            if dp_port and dp_repeater:
                if dp_mst is False:
                    logging.error("Panel Issue : MST is not supported in panel but still repeater bit is set in Bcaps")
                logging.info("\tSTEP: Verify DP Repeater Authentication")
                if verify_dp_repeater(panel, start_time=start_time,
                                      end_time=start_time + HDCP1_REPEATER_STEP_TIMEOUT_IN_MS) is False:
                    return False
                start_time = dp_repeater_ready
                end_time = start_time + HDCP_WAIT_TIME_FOR_ENCRYPTION_ENABLE_IN_MS
                if check_repeater_status(adapter, panel, rep_ctl, start_time, end_time=end_time) is False:
                    return False
                logging.info("\tPASS: DP Repeater Authentication successful")
            elif hdmi_repeater:
                logging.info("\tSTEP: Verify HDMI Repeater Authentication")
                if verify_hdmi_repeater(panel, start_time=start_time,
                                        end_time=start_time + HDCP1_REPEATER_STEP_TIMEOUT_IN_MS) is False:
                    return False
                start_time = hdmi_repeater_ready
                end_time = start_time + HDCP_WAIT_TIME_FOR_ENCRYPTION_ENABLE_IN_MS
                if check_repeater_status(adapter, panel, rep_ctl, start_time, end_time) is False:
                    return False
                logging.info("\tPASS: HDMI Repeater Authentication successful")
            if dp_port is False:
                logging.info("\tSTEP: Read and verify RI' prime values")
                if __verify_ri_prime(panel, start_time=start_time, end_time=auth_restart) is False:
                    return False
                logging.info("\tPASS : Valid RI' values received from Panel")
        logging.info("\tIteration {0} verification completed on PIPE {1}".format(index, panel.pipe))

    else:
        logging.error("\tTx didn't write AKSV")
        return False
    logging.info("PASS : HDCP 1.4 Authentication flow verification successful on {}".format(panel.name))
    return True


##
# @brief       This function is used to verify hdcp protection for the given displays
# @param[in]   adapter platform_name
# @param[in]   port_list list of ports
# @param[in]   etl_file etl_file_path
# @param[in]   hdcp_type 0/1
# @return      True if HDCP verification is successful else return False
def verify_hdcp(adapter, port_list, etl_file, hdcp_type):
    status = True
    etl_parser.generate_report(etl_file)
    for port in port_list:
        panel = Panel()
        display_base = DisplayBase(port)
        panel.name = port
        trans, pipe = display_base.get_transcoder_and_pipe(port)
        panel.transcoder = 'EDP' if trans == 0 else chr(int(trans) + 64)
        panel.pipe = chr(int(pipe) + 65)
        panel.port = 'PORT_' + port.split("_")[1]  # I2C Format -> "Port": "PORT_C"
        panel.panel_type = port.split("_")[0]
        panel.aux = port.split("_")[1]
        if hdcp_type:
            status &= verify_hdcp_2_2(adapter, panel)
        else:
            status &= verify_hdcp_1_4(adapter, panel)
    return status


if __name__ == '__main__':
    etl = r"C:\Users\gta\Downloads\DisplayAutomation2.0_x64\Traces\GfxTrace.etl"
    verify_hdcp('LKF1', ['DP_D_TC'], etl, hdcp_type=0)
