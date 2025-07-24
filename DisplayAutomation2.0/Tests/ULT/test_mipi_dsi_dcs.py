######################################################################################
# @file     test_mipi_dsi_dcs.py
# @brief    This script is to verify MIPI DSI DCS Functionalities like DCS caps and Transmission.
#           Commandline : python Tests\ULT\test_mipi_dsi_dcs.py -gfx_index_0 Display1
# @author   Chandrakanth Pabolu
######################################################################################
import unittest
import time
import logging
from Libs.Core.enum import *
from Libs.Core.test_env.test_environment import *
from Libs.Core.test_env.test_context import *
from Libs.Core.display_config.display_config import *
from Libs.Feature.mipi.mipi_dsi_dcs import *

##
# @brief This class helps to verify MIPI DSI DCS functionalities
class MipiDsiDcsRead(unittest.TestCase):

    ##
    # @brief        This class method helps to load the dependancy library
    # @return       pass
    def setUp(self):
        load_library()
        pass

    ##
    # @brief        Teardown function
    # @return       pass
    def tearDown(self):
        pass

    ##
    # @brief        This function helps to parse commandline and verify the MIPI DSI DCS caps and transmission
    # @return       pass
    def runTest(self):
        current_port = None
        cmd_line_param = parse_cmdline(sys.argv)

        for key, value in cmd_line_param.items():
            if display_key_pattern.match(key) is not None:
                if value['connector_port'] is not None and 'MIPI' in value['connector_port']:
                    current_port = value['connector_port']

        if current_port is None:
            self.fail("MIPI display is not passed in command line.")

        self.display_config = DisplayConfiguration()
        self.enumerated_displays = self.display_config.get_enumerated_display_info()
        display_target_id = self.display_config.get_target_id(current_port, self.enumerated_displays)
        logging.info("target_id for {0} = {1}".format(current_port, display_target_id))

        logging.info("Getting MIPI DSI DCS Caps for {0} with target_id: {1}".format(current_port, display_target_id))
        self.read_dsi_caps('gfx_0', display_target_id)

        logging.info("Perform MIPI DSI DCS Transmission sequentially for {0},target_id: {1}".format(current_port, display_target_id))
        self.perform_dsi_read_write_sequentially('gfx_0', display_target_id)

        logging.info("Perform MIPI DSI DCS Transmission in single packet for {0},target_id: {1}".format(current_port,
                                                                                                    display_target_id))
        self.verify_dsi_multi_packet_read_write('gfx_0', display_target_id)

    ##
    # @brief        dump function
    # @param[in]    obj is dsi_cap
    # @return       None
    def dump(self, obj):
        for attr in dir(obj):
            if hasattr(obj, attr):
                logging.info("obj.%s = %s" % (attr, getattr(obj, attr)))

    ##
    # @brief        reads MIPI DSI caps
    # @param[in]    gfx_index : Graphics index of graphics adapter
    # @param[in]    target_id : target id of display
    # @return       None
    def read_dsi_caps(self, gfx_index, target_id):

        dsi_caps = DXGK_DSI_CAPS()

        get_mipi_dsi_caps('gfx_0', target_id, dsi_caps)
        self.dump(dsi_caps)

    ##
    # @brief        This function will read and write to DSI
    # @param[in]    gfx_index : Graphics index of graphics adapter
    # @param[in]    target_id : target id of display
    # @return       None
    def perform_dsi_read_write_sequentially(self, gfx_index, target_id):

        #read 1st byte of 0x36 from bridge
        dsi_transmission_read = DXGK_DSI_TRANSMISSION()
        dsi_transmission_read.TotalBufferSize = 12
        dsi_transmission_read.PacketCount = 1
        dsi_transmission_read.DsiTransmissionMode.TransmissionMode = 1
        dsi_transmission_read.DsiPacket[0].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_GENERIC_READ_2_PARAM
        dsi_transmission_read.DsiPacket[0].DsiDatatype.VirtualChannel = 0
        dsi_transmission_read.DsiPacket[0].DsiData.Data0 = 0x36
        dsi_transmission_read.DsiPacket[0].DsiData.Data1 = 0

        perform_mipi_dsi_transmission(gfx_index, target_id, dsi_transmission_read)
        logging.info("read: DeviceId: {}".format(dsi_transmission_read.DsiPacket[0].Payload[0]))
        read_value= dsi_transmission_read.DsiPacket[0].Payload[0]

        # write 1st byte of 0x36 to 0x14 from bridge
        dsi_transmission_write = DXGK_DSI_TRANSMISSION()
        dsi_transmission_write.TotalBufferSize = 12
        dsi_transmission_write.PacketCount = 1
        dsi_transmission_write.DsiTransmissionMode.TransmissionMode = 1
        dsi_transmission_write.DsiPacket[0].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_GENERIC_SHORT_WRITE_2_PARAM
        dsi_transmission_write.DsiPacket[0].DsiDatatype.VirtualChannel = 0
        dsi_transmission_write.DsiPacket[0].DsiData.Data0 = 0x36
        dsi_transmission_write.DsiPacket[0].DsiData.Data1 = read_value + 1

        logging.info("Write: DeviceId: {}".format(dsi_transmission_write.DsiPacket[0].DsiData.Data1))
        perform_mipi_dsi_transmission(gfx_index, target_id, dsi_transmission_write)

        #read 1st byte of 0x36 again from bridge
        dsi_transmission_read = DXGK_DSI_TRANSMISSION()
        dsi_transmission_read.TotalBufferSize = 12
        dsi_transmission_read.PacketCount = 1
        dsi_transmission_read.DsiTransmissionMode.TransmissionMode = 1
        dsi_transmission_read.DsiPacket[0].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_GENERIC_READ_2_PARAM
        dsi_transmission_read.DsiPacket[0].DsiDatatype.VirtualChannel = 0
        dsi_transmission_read.DsiPacket[0].DsiData.Data0 = 0x36
        dsi_transmission_read.DsiPacket[0].DsiData.Data1 = 0

        perform_mipi_dsi_transmission(gfx_index, target_id, dsi_transmission_read)
        logging.info("Read: DeviceId: {}".format(dsi_transmission_read.DsiPacket[0].Payload[0]))

    ##
    # @brief        This function will read and write of DSI of multiple packet
    # @param[in]    gfx_index : Graphics index of graphics adapter
    # @param[in]    target_id : target id of display
    # @return       None
    def verify_dsi_multi_packet_read_write(self, gfx_index, target_id):
        #1 Preparing to call Caps data

        #write 1 byte and write one of 0x36 from bridge
        dsi_transmission = DXGK_DSI_TRANSMISSION()
        dsi_transmission.TotalBufferSize = 12
        dsi_transmission.PacketCount = 3
        dsi_transmission.DsiTransmissionMode.TransmissionMode = 1
        dsi_transmission.DsiPacket[0].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_GENERIC_SHORT_WRITE_2_PARAM
        dsi_transmission.DsiPacket[0].DsiData.Data0 = 0x36
        dsi_transmission.DsiPacket[0].DsiData.Data1 = 0x13
        dsi_transmission.DsiPacket[1].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_DCS_LONG_WRITE_OR_WRITE_LUT
        dsi_transmission.DsiPacket[1].LongWriteWordCount = 0x4
        dsi_transmission.DsiPacket[1].Payload[0] = 0x1
        dsi_transmission.DsiPacket[1].Payload[1] = 0x2
        dsi_transmission.DsiPacket[1].Payload[2] = 0x3
        dsi_transmission.DsiPacket[1].Payload[3] = 0x4
        dsi_transmission.DsiPacket[2].DsiDatatype.DataType = MIPI_DSI_DCS_DATATYPE_GENERIC_READ_2_PARAM
        dsi_transmission.DsiPacket[2].DsiData.Data0 = 0x36
        dsi_transmission.DsiPacket[2].DsiData.Data1 = 0x0

        perform_mipi_dsi_transmission(gfx_index, target_id, dsi_transmission)
        logging.info("After multi packet write & read : DeviceId: {}".format(dsi_transmission.DsiPacket[2].Payload[0]))


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
