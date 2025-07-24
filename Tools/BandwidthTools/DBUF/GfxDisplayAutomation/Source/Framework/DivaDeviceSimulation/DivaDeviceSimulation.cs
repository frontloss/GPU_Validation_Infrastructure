using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Management;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    public static class DivaDeviceSimulation
    {
        const int DIVA_MAX_EDID_BLOCKS = 6;
        const int DIVA_MAX_DPCD_DATA = 512;
        const int DIVA_MAX_ENCODERS = 20;
        const int DIVA_EDID_BLOCK_SIZE = 128;

        static DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility;

        public enum PortType
        {
            NONE = 0x00,
            PORTA,
            PORTB,
            PORTC,
            PORTD,
            PORTE,
            TVPORT,
            PORTX,
            PORTY
        }

        public enum DisplayType
        {
            None = 0,
            EDP,
            CRT,
            DP,
            HDMI,
            MIPI,
            WIDI,
            DVI
        }

        static DivaDeviceSimulation()
        {
            if (DivaDisplayFeatureUtility == null)
                DivaDisplayFeatureUtility = GetDivaDisplayFeatureUtility();

            EnableFramework(true);
            EnableFeature(true, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);
        }

        public static uint Plug(DisplayType display, List<byte> EdidData, List<byte> dpcdData, bool isLowPowerState)
        {
            uint windowsID = 0;
            DIVA_PORT_TYPE_CLR portType = DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR;

            if (GetAvailableDisplayUID(display, ref windowsID, ref portType) != true)
                throw new Exception("Unable to find free WindowsID.");

            Plug(display, windowsID, portType, EdidData, dpcdData, isLowPowerState);

            return windowsID;
        }

        public static void Plug(DisplayType display, uint windowsID, DIVA_PORT_TYPE_CLR portType, List<byte> EdidData, List<byte> dpcdData, bool isLowPowerState)
        {
            int maxEDIDBytes = DIVA_MAX_EDID_BLOCKS * DIVA_EDID_BLOCK_SIZE;

            if (windowsID == 0)
                throw new Exception("WindowsID Should not be 0.");

            if (EdidData.Count == 0)
            {
                throw new Exception("EDID Data not passed.");
            }
            else if (maxEDIDBytes < EdidData.Count)
            {
                throw new Exception(string.Format("EDID Data size {0} passed exceeds expected size {1}.", EdidData.Count, maxEDIDBytes));
            }

            if (display == DisplayType.DP)
            {
                if (dpcdData.Count == 0)
                {
                    throw new Exception("DPCD Data not passed.");
                }
                else if (DIVA_MAX_DPCD_DATA < dpcdData.Count)
                {
                    throw new Exception(string.Format("DPCD Data size {0} passed exceeds expected size {1}.", dpcdData.Count, DIVA_MAX_DPCD_DATA));
                }
            }

            PlugDisplay(windowsID, portType, true, EdidData, dpcdData, isLowPowerState);
        }

        public static void UnPlug(uint windowsID, bool isLowPowerState)
        {
            List<byte> EdidData = new List<byte>();
            List<byte> dpcdData = new List<byte>();
            DIVA_PORT_TYPE_CLR portType = DIVA_PORT_TYPE_CLR.DIVA_NULL_PORT_TYPE_CLR;

            PlugDisplay(windowsID, portType, false, EdidData, dpcdData, isLowPowerState);
        }

        public static void CleanUp()
        {
            EnableFeature(false, DIVA_DISPLAY_FEATURE_TYPE_CLR.DEV_SIM);
        }

        private static bool GetAvailableDisplayUID(DisplayType display, ref uint displayUID, ref DIVA_PORT_TYPE_CLR portType)
        {
            bool status = false;
            DIVA_ENUM_DEVICE_ARGS_CLR enumDeviceArgs = new DIVA_ENUM_DEVICE_ARGS_CLR();

            // Enumerate devices.
            DivaDisplayFeatureUtility.EnumerateDevices(enumDeviceArgs);

            //supported displays for device simulation.
            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> supportedDisplaysList = enumDeviceArgs.DisplayDetailsArgs.ToList().Take((int)enumDeviceArgs.NumDisplays).ToList();

            //Getting all displays which were currently attached.
            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> attachedDisplays = supportedDisplaysList.Where(item => GetDeviceConnectedStatus(item.DisplayUID) && !IsRaritanEdid(item.DisplayUID)).ToList();

            //Removing attached displays from list
            supportedDisplaysList.RemoveAll(item => attachedDisplays.Contains(item));

            //Fetching attached displays to the same port. And remove it from the list.
            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> ToRemove = new List<DIVA_DISPLAY_DETAILS_ARGS_CLR>();

            attachedDisplays.ForEach(attachedItem =>
            {
                ToRemove.AddRange(supportedDisplaysList.Where(item => GetPhysicalPortConnected(item.PortType) == GetPhysicalPortConnected(attachedItem.PortType)));
            });
            supportedDisplaysList.RemoveAll(item => ToRemove.Contains(item));

            if (supportedDisplaysList.Count == 0)
            {
                return false;
            }

            //get the difference of the displays and return a display.
            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> displaysSamePort = supportedDisplaysList.Where(eachElement => supportedDisplaysList.Where(item => GetPhysicalPortConnected(item.PortType) == GetPhysicalPortConnected(eachElement.PortType)).ToList().Count == 1).ToList();
            foreach (DIVA_DISPLAY_DETAILS_ARGS_CLR dispDetails in displaysSamePort)
            {
                if (GetConnectorType(dispDetails.PortType) == display)
                {
                    status = true;
                    displayUID = dispDetails.DisplayUID;
                    portType = dispDetails.PortType;
                    break;
                }
            }

            if (displayUID == 0)
            {
                //get any display matching to the displaytype.
                foreach (DIVA_DISPLAY_DETAILS_ARGS_CLR dispDetails in supportedDisplaysList)
                {
                    if (GetConnectorType(dispDetails.PortType) == display)
                    {
                        status = true;
                        displayUID = dispDetails.DisplayUID;
                        portType = dispDetails.PortType;
                        break;
                    }
                }
            }

            return status;
        }

        private static PortType GetPhysicalPortConnected(DIVA_PORT_TYPE_CLR displayPort)
        {
            PortType actualPort = PortType.NONE;

            switch (displayPort)
            {
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOA_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIA_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_LVDS_PORT_CLR:
                    actualPort = PortType.PORTA;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIB_PORT_CLR:
                    actualPort = PortType.PORTB;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIC_PORT_CLR:
                    actualPort = PortType.PORTC;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOD_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMID_PORT_CLR:
                    actualPort = PortType.PORTD;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_ANALOG_PORT_CLR:
                    actualPort = PortType.PORTE;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_TPV_PORT_CLR:
                    actualPort = PortType.TVPORT;
                    break;
                default:
                    actualPort = PortType.NONE;
                    break;
            }

            return actualPort;
        }

        internal static DisplayType GetConnectorType(DIVA_PORT_TYPE_CLR displayPort)
        {
            switch (displayPort)
            {
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR:
                    return DisplayType.DP;
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMID_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOD_PORT_CLR:
                    return DisplayType.HDMI;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR:
                    return DisplayType.EDP;
                case DIVA_PORT_TYPE_CLR.DIVA_ANALOG_PORT_CLR:
                    return DisplayType.CRT;
                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIA_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIC_PORT_CLR:
                    return DisplayType.MIPI;
                default:
                    return DisplayType.None;
            }
        }

        private static bool GetDeviceConnectedStatus(uint displayUID)
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            DIVA_GET_DEVICE_CONNECTIVITY_ARGS_CLR divaDeviceConnectivityArgs = new DIVA_GET_DEVICE_CONNECTIVITY_ARGS_CLR();
            divaDeviceConnectivityArgs.DisplayUID = displayUID;

            // Get Device connectivity status
            DivaDisplayFeatureUtility.GetDeviceConnectivity(divaDeviceConnectivityArgs);

            return divaDeviceConnectivityArgs.Attached;

        }

        private static void PlugDisplay(uint displayUID, DIVA_PORT_TYPE_CLR portType, bool plugType, List<byte> EdidData, List<byte> dpcdData, bool IslowPower = false)
        {
            DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR divaSimulationDevicesArgs = new DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR();

            for (int i = 0; i < DIVA_MAX_ENCODERS; i++)
                divaSimulationDevicesArgs.DeviceInfo[i].DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];

            DIVA_DEVICE_INFO_CLR DeviceInfo = new DIVA_DEVICE_INFO_CLR();
            DeviceInfo.Attach = plugType;
            DeviceInfo.OpType = DIVA_OP_TYPE_CLR.DIVA_OP_SET;
            DeviceInfo.DisplayUID = displayUID;
            DeviceInfo.DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];
            DeviceInfo.SimConnnectionInLowPower = IslowPower;
            DeviceInfo.PortType = portType;

            if (plugType == true)
            {
                for (int i = 0; i < EdidData.Count; i++)
                {
                    int row = i / 128;
                    int col = i % 128;

                    DeviceInfo.DisplayEdid[row, col] = EdidData[i];
                }

                //writing DPCD Data
                if (dpcdData.Count != 0)
                {
                    ProgramAllDPCDData(displayUID, dpcdData);
                }
            }

            divaSimulationDevicesArgs.NumDevices = 1;
            divaSimulationDevicesArgs.DeviceInfo[0] = DeviceInfo;

            //Simulate Devices
            DivaDisplayFeatureUtility.SimulateDevices(divaSimulationDevicesArgs);
        }

        private static void ProgramAllDPCDData(uint displayUID, List<byte> dpcdData)
        {
            List<byte> ucDPCDs_202_204 = new List<byte> { 0xFF, 0xFF, 0xFF };
            List<byte> ucDPCDs_10_1F = new List<byte> { 0xA4, 0x1F, 0xBC, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

            //Write 14 bytes of DPCD data from _DPCD.bin file.
            WriteDPCD(0, displayUID, 0x0, dpcdData);

            //write ucDPCDs_202_204[] to address 202
            WriteDPCD(1, displayUID, 0x202, ucDPCDs_202_204);

            //write 0 to address 101
            WriteDpcdData(2, displayUID, 0x101, 0);

            //write 0 to address 200
            WriteDpcdData(3, displayUID, 0x200, 0);

            //write 0 to address 206
            WriteDpcdData(4, displayUID, 0x206, 0);

            //write ucDPCDs_10_1F[] to address 202
            WriteDPCD(5, displayUID, 0x10, ucDPCDs_10_1F);

            //write 0 to address 600
            WriteDpcdData(6, displayUID, 0x600, 1);

            //write 0 to address 205
            WriteDpcdData(7, displayUID, 0x205, 1);
        }

        private static void WriteDpcdData(uint Index, uint displayUID, uint address, byte DPCDByte)
        {
            List<byte> DPCDData = new List<byte>();
            DPCDData.Add(DPCDByte);

            WriteDPCD(Index, displayUID, address, DPCDData);
        }

        private static void WriteDPCD(uint Index, uint displayUID, uint address, List<byte> DPCDData)
        {
            DIVA_DEV_SIM_CACHE_DPCD_DATA_ARGS_CLR divaDPCDArgs = new DIVA_DEV_SIM_CACHE_DPCD_DATA_ARGS_CLR();
            divaDPCDArgs.DisplayUID = displayUID;
            divaDPCDArgs.DPCDAddress = address;
            divaDPCDArgs.Size = (uint)DPCDData.Count;
            divaDPCDArgs.DPCDData = new byte[512];
            divaDPCDArgs.Index = Index;

            for (int i = 0; i < DPCDData.Count; i++)
            {
                divaDPCDArgs.DPCDData[i] = DPCDData[i];
            }

            // Set DPCD data
            DivaDisplayFeatureUtility.SetDpcdData(divaDPCDArgs);
        }

        public static void EnableFramework(bool status)
        {
            DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR divaEnableDisableArgs = new DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR();
            divaEnableDisableArgs.EnableFramework = status;
            // Enable Disable ULT
            DivaDisplayFeatureUtility.EnableDisableFramework(divaEnableDisableArgs);
        }

        public static void EnableFeature(bool status, DIVA_DISPLAY_FEATURE_TYPE_CLR featureType)
        {
            DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR divaEnableDisableArgs = new DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR();
            divaEnableDisableArgs.EnableFeature = status;
            divaEnableDisableArgs.FeatureType = featureType;

            // Enable Disable Feature
            DivaDisplayFeatureUtility.EnableDisableFeature(divaEnableDisableArgs);
        }

        private static DivaDisplayFeatureUtilityCLR GetDivaDisplayFeatureUtility()
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();
            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            return DivaDisplayFeatureUtility;
        }

        private static bool IsRaritanEdid(uint displayUID)
        {
            bool status = false;
            ManagementClass mgntClass = new ManagementClass(string.Format(@"\\{0}\root\wmi:WmiMonitorDescriptorMethods", Environment.MachineName));
            foreach (ManagementObject mgntObj in mgntClass.GetInstances())
            {
                if (mgntObj.Path.Path.Contains(displayUID.ToString()))
                {
                    ManagementBaseObject inParams = mgntObj.GetMethodParameters("WmiGetMonitorRawEEdidV1Block");
                    inParams["BlockId"] = 0;
                    ManagementBaseObject outParams = null;
                    outParams = mgntObj.InvokeMethod("WmiGetMonitorRawEEdidV1Block", inParams, null);
                    byte[] blockContent = outParams["BlockContent"] as byte[];
                    if (blockContent != null && blockContent.Length >= 128)
                    {
                        //Ignore RAR display interface.
                        if (blockContent[8] == 0x48 && blockContent[9] == 0x32) status = true;
                    }
                }
            }
            return status;
        }
    }
}
