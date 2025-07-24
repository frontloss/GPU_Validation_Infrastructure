/**
* @file     DisplayDetectHandler.cs
* @brief    Handles all Display Detection Related Events
*
* @author   ecpabolu
*/

using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriver;
using Microsoft.Diagnostics.Tracing.Parsers.IntelGfxDriverDisplay;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.IO;

namespace EtlParser.Handlers
{
 
    public class QueryConnectionChangeEvents:CommonData
    {
        public long ConnectionChangeId;
        public uint TargetId;
        public CONNECTION_STATUS ConnectionState;
        public CONNECTOR_TYPE MonitorConnectLinkTargetType;
        public CONNECTOR_TYPE TargetConnectBaseTargetType;
        public uint TargetConnectNewTargetId;
        public CONNECTOR_TYPE TargetJoinBaseTargetType;
        public uint TargetJoinNewTargetId;
        public QCC_MONITOR_CONNECT_FLAGS MonitorConnectMonitorConnectFlags;
        public uint Usb4MonitorInfoDPInAdapterNumber;
        public uint Usb4MonitorInfoUSB4DriverID;

        public QueryConnectionChangeEvents(t_QueryConnectionChange data) : base(data)
        {
            this.ConnectionChangeId = data.ConnectionChangeId;
            this.TargetId = data.TargetId;
            this.ConnectionState = data.ConnectionState;
            this.MonitorConnectLinkTargetType = data.MonitorConnectLinkTargetType;
            this.TargetConnectBaseTargetType = data.TargetConnectBaseTargetType;
            this.TargetConnectNewTargetId = data.TargetConnectNewTargetId;
            this.TargetJoinBaseTargetType = data.TargetJoinBaseTargetType;
            this.TargetJoinNewTargetId = data.TargetJoinNewTargetId;
            this.MonitorConnectMonitorConnectFlags = data.MonitorConnectMonitorConnectFlags;
            this.Usb4MonitorInfoDPInAdapterNumber = data.Usb4MonitorInfoDPInAdapterNumber;
            this.Usb4MonitorInfoUSB4DriverID = data.Usb4MonitorInfoUSB4DriverID;
        }
    }

    public class HotPlugDetectLiveState : CommonData
    {
        public DD_PORT_TYPES Port;
        public bool Attached;
        public PORT_CONNECTOR_TYPE PortConnectorType;

        public HotPlugDetectLiveState(HPDLiveState_t data) : base(data)
        {
            this.Port = data.Port;
            this.Attached = data.Attached;
            this.PortConnectorType = data.PortConnectorType;
        }
    }

    class DisplayDetectHandler
    {
        public Queue<QueryConnectionChangeEvents> queryConnectionChangeEventQueue = new Queue<QueryConnectionChangeEvents>();
        public Queue<HotPlugDetectLiveState> hotPlugDetectLiveStateQueue = new Queue<HotPlugDetectLiveState>();

        public void Enqueue(t_QueryConnectionChange data)
        {
            this.queryConnectionChangeEventQueue.Enqueue(new QueryConnectionChangeEvents(data));
        }
        public void Enqueue(HPDLiveState_t data)
        {
            this.hotPlugDetectLiveStateQueue.Enqueue(new HotPlugDetectLiveState(data));
        }

        public void DumpJson()
        {
            String displayDetectOutputFile = Environment.CurrentDirectory + "\\" + "DisplayDetectData.json";
            // First delete the existing file
            System.IO.File.Delete(displayDetectOutputFile);

            JsonSerializer serializer = new JsonSerializer();
            serializer.Converters.Add(new JavaScriptDateTimeConverter());
            serializer.Converters.Add(new StringEnumConverter());
            serializer.NullValueHandling = NullValueHandling.Ignore;

            using (StreamWriter sw = new StreamWriter(displayDetectOutputFile))
            using (JsonWriter writer = new JsonTextWriter(sw))
            {
                serializer.Serialize(writer, this);
            }
        }
    }
}
