######################################################################################
# @file     usb4.py
# @brief    Python Wrapper exposes interfaces for USB4 feature testing
# @author   Chandrakanth Pabolu
######################################################################################

import logging
from Libs.Core import etl_parser


##
# @brief        Get Connected USB4 displays from passed ETL
# @param[in]    etl_file_path - ETL File Path
# @return       usb4_display_list - of format {target_id, "USB4_DP_MONITOR"}
#                ex: {8257:"USB4_DP_MONITOR" ,36931: "USB4_DP_MONITOR"}
def get_connected_usb4_displays(etl_file_path):
    usb4_display_list = {}
    etl_parser.generate_report(etl_file_path)

    connect_data = etl_parser.get_query_connection_change_event_data(etl_parser.Events.QUERY_CONNECTION_CHANGE_EVENT)

    if connect_data is not None:
        for client_event in connect_data:
            logging.info(f"{client_event}")
            if client_event.ConnectionState == "CSMonitorStatusConnected" \
                    and client_event.MonitorConnectLinkTargetType == "DP_EXTERNAL":
                usb4_display_list[client_event.TargetId] = client_event.MonitorConnectMonitorConnectFlags

    return usb4_display_list
