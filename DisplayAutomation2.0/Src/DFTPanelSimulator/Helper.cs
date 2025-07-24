using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Management;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    internal class Helper
    {
        const int DIVA_MAX_EDID_BLOCKS = 6;
        const int DIVA_MAX_DPCD_DATA = 512;
        const int DIVA_MAX_ENCODERS = 20;
        const int DIVA_EDID_BLOCK_SIZE = 128;


        public enum PortType
        {
            NONE = 0x00,
            PORTA,
            PORTB,
            PORTC,
            PORTD,
            PORTE,
            PORTF,
            TVPORT,
            PORTX,
            PORTY
        }

        internal static void EnableULT(bool status)
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
            {
                DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR divaEnableDisableArgs = new DIVA_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS_CLR();
                divaEnableDisableArgs.EnableFramework = status;
                // Enable Disable ULT
                DivaDisplayFeatureUtility.EnableDisableFramework(divaEnableDisableArgs);
            }
            catch (Exception Exp)
            {
                Console.WriteLine("ERROR: Exception in Enable/Disable ULT Framework: {0}",
                    Exp.Message);
            }
        }

        internal static void EnableFeature(bool status, DIVA_DISPLAY_FEATURE_TYPE_CLR featureType)
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
            {
                DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR divaEnableDisableArgs = new DIVA_ENABLE_DISABLE_FEATURE_ARGS_CLR();
                divaEnableDisableArgs.EnableFeature = status;
                divaEnableDisableArgs.FeatureType = featureType;

                // Enable Disable Feature
                DivaDisplayFeatureUtility.EnableDisableFeature(divaEnableDisableArgs);
            }
            catch (Exception Exp)
            {
                Console.WriteLine("ERROR: Exception in Enable/Disable Feature: {0}",
                    Exp.Message);
            }
        }

        internal static bool ULT_FW_PlugDisplay(bool plug, DIVA_PORT_TYPE_CLR portType, uint displayUID, string edidFile, string dpcdFile, bool lowPower)
        {
            bool status = true;
            DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR divaSimulationDevicesArgs = new DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR();
            divaSimulationDevicesArgs.NumDevices = 1;

            for (int i = 0; i < DIVA_MAX_ENCODERS; i++)
                divaSimulationDevicesArgs.DeviceInfo[i].DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];

            DIVA_DEVICE_INFO_CLR ult_Device_Info = new DIVA_DEVICE_INFO_CLR();
            ult_Device_Info.Attach = plug;
            ult_Device_Info.OpType = DIVA_OP_TYPE_CLR.DIVA_OP_SET;
            ult_Device_Info.DisplayUID = displayUID;
            ult_Device_Info.DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];
            ult_Device_Info.SimConnnectionInLowPower = lowPower;
            ult_Device_Info.PortType = portType;

            if (plug == true)
            {
                if (IsDP(portType))
                {
                    //Writing DPCD Data
                    if (ProgramAllDPCDData(displayUID, dpcdFile) != true)
                    {
                        Console.WriteLine("Error in programming DPCD Data.");
                        return false;
                    }
                }

                byte[] array = File.ReadAllBytes(edidFile);

                for (int i = 0; i < array.Length; i++)
                {
                    int row = i / 128;
                    int col = i % 128;

                    ult_Device_Info.DisplayEdid[row, col] = array[i];
                }
            }

            divaSimulationDevicesArgs.DeviceInfo[0] = ult_Device_Info;


            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();
            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
            {
                DivaDisplayFeatureUtility.SimulateDevices(divaSimulationDevicesArgs);
            }
            catch (Exception Exp)
            {
                status = false;
                Console.WriteLine(string.Format("ERROR: Exception in GetSetSimulateDevices(). {0}",
                    Exp.Message));
            }

            return status;
        }

        internal static bool ProgramAllDPCDData(uint displayUID, string dpcdFile)
        {
            uint counter = 0;
            string line;
            bool status = true;

            System.IO.StreamReader file =
               new System.IO.StreamReader(dpcdFile);
            while ((line = file.ReadLine()) != null)
            {
                if (line.StartsWith(";"))
                {
                    //comment line. Ignore and proceed.
                    continue;
                }

                Match m = Regex.Match(line, @"^(0x[\da-fA-F]{1,4})\s?:(\s?0x[\da-fA-F]{1,4}[\s,]?)+.?");
                if (!m.Success)
                {
                    Console.WriteLine("Error in dpcd address format: "+ line);
                    status = false;
                    break;
                }

                List<string> dpcddata = line.Split(':').ToList();

                uint address = Convert.ToUInt32(dpcddata[0], 16);
                List<byte> dpcds = dpcddata[1].Split(',').Select(x => x.Replace(" ", string.Empty)).ToList().
                    Select(x => x.Replace(".", string.Empty)).ToList().Select(x =>Convert.ToByte(Convert.ToUInt32(x, 16))).ToList();

                status &= ULT_FW_WriteDPCD(counter, displayUID, address, dpcds);
                counter++;
            }

            file.Close();

            if (counter == 0)
                status = false;

            return status;
        }

        internal static bool ULT_FW_WriteDPCD(uint Index, uint displayUID, uint address, byte DPCDByte)
        {
            List<byte> DPCDData = new List<byte>();
            DPCDData.Add(DPCDByte);

            return ULT_FW_WriteDPCD(Index, displayUID, address, DPCDData);
        }

        internal static bool ULT_FW_WriteDPCD(uint Index, uint displayUID, uint address, List<byte> DPCDData)
        {
            bool status = true;
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
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
            catch (Exception Exp)
            {
                Console.WriteLine("ERROR: Exception in SetDPCDData(). {0}",
                    Exp.Message);
            }

            return status;
        }

        internal static void FetchEnumeratedDisplays(ref List<DIVA_DISPLAY_DETAILS_ARGS_CLR> EnumeratedDisplays)
        {
            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
            {
                DIVA_ENUM_DEVICE_ARGS_CLR divaEnableDisableArgs = new DIVA_ENUM_DEVICE_ARGS_CLR();

                // Enumerate devices.
                DivaDisplayFeatureUtility.EnumerateDevices(divaEnableDisableArgs);

                EnumeratedDisplays.Clear();
                EnumeratedDisplays.AddRange(divaEnableDisableArgs.DisplayDetailsArgs.ToList().Take((int)divaEnableDisableArgs.NumDisplays).ToList());
            }
            catch (Exception Exp)
            {
                Console.WriteLine("ERROR: Exception in EnumDevices.: {0}",
                    Exp.Message);
            }
        }

        internal static bool GetDeviceConnectedStatus(uint displayUID)
        {
            bool status = false;

            // Create CLR-Utility handle
            DivaUtilityCLR DivaUtility = new DivaUtilityCLR();

            // Get DIVA device handle
            SafeFileHandle hDivaDevice = DivaUtility.GetDivaDeviceHandle();

            // Create 'Generic GFX Access DIVA CLR Utility'
            DivaDisplayFeatureUtilityCLR DivaDisplayFeatureUtility = new DivaDisplayFeatureUtilityCLR(hDivaDevice);

            try
            {
                DIVA_GET_DEVICE_CONNECTIVITY_ARGS_CLR divaDeviceConnectivityArgs = new DIVA_GET_DEVICE_CONNECTIVITY_ARGS_CLR();
                divaDeviceConnectivityArgs.DisplayUID = displayUID;
                // Get Device connectivity status
                DivaDisplayFeatureUtility.GetDeviceConnectivity(divaDeviceConnectivityArgs);
                status = divaDeviceConnectivityArgs.Attached;
            }
            catch (Exception Exp)
            {
                Console.WriteLine("ERROR: Exception in GetDeviceConnectivity(): {0}",
                    Exp.Message);
            }

            return status;
        }

        internal static DIVA_DISPLAY_DETAILS_ARGS_CLR GetDisplayDetailsFromPort(DIVA_PORT_TYPE_CLR portType)
        {
            DIVA_DISPLAY_DETAILS_ARGS_CLR displayDetails = new DIVA_DISPLAY_DETAILS_ARGS_CLR();

            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> EnumeratedDisplays = new List<DIVA_DISPLAY_DETAILS_ARGS_CLR>();
            Helper.FetchEnumeratedDisplays(ref EnumeratedDisplays);

            EnumeratedDisplays.ForEach(eachDisplayInfo =>
            {
                if (eachDisplayInfo.PortType == portType)
                {
                    displayDetails = eachDisplayInfo;
                }
            });

            return displayDetails;
        }

        internal static List<string> GetAvailablePorts()
        {
            List<string> ports = new List<string>();

            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> EnumeratedDisplays = new List<DIVA_DISPLAY_DETAILS_ARGS_CLR>();
            Helper.FetchEnumeratedDisplays(ref EnumeratedDisplays);

            EnumeratedDisplays.ForEach(eachDisplayInfo =>
            {
                string tempPort = ConvertToDivaPort(eachDisplayInfo.PortType);
                if (tempPort != default(string))
                {
                    if (!ports.Contains(tempPort))
                        ports.Add(tempPort);
                }
            });

            return ports;
        }

        internal static List<string> GetFreePorts()
        {
            List<string> ports = new List<string>();

            Dictionary<DIVA_PORT_TYPE_CLR, uint> portsMapper = new Dictionary<DIVA_PORT_TYPE_CLR, uint>();

            List<DIVA_DISPLAY_DETAILS_ARGS_CLR> supportedDisplaysList = new List<DIVA_DISPLAY_DETAILS_ARGS_CLR>();
            Helper.FetchEnumeratedDisplays(ref supportedDisplaysList);

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

            supportedDisplaysList.ForEach(eachDisplayInfo =>
            {
                string tempPort = ConvertToDivaPort(eachDisplayInfo.PortType);
                if (tempPort != default(string))
                {
                    if(!ports.Contains(tempPort))
                        ports.Add(tempPort);
                }
            });

            return ports;
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
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPE_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOE_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIE_PORT_CLR:
                    actualPort = PortType.PORTE;
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPF_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_DVOF_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTHDMIF_PORT_CLR:
                    actualPort = PortType.PORTF;
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

        private static string ConvertToDivaPort(DIVA_PORT_TYPE_CLR portType)
        {
            string st = default(string);
            switch (portType)
            {
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR:
                    st = "DP_A";
                    break;

                case DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR:
                    st = "DP_B";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR:
                    st = "DP_C";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR:
                    st = "DP_D";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPE_PORT_CLR:
                    st = "DP_E";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPF_PORT_CLR:
                    st = "DP_F";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_DVOB_PORT_CLR:
                    st = "HDMI_B";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_DVOC_PORT_CLR:
                    st = "HDMI_C";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_DVOD_PORT_CLR:
                    st = "HDMI_D";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_DVOE_PORT_CLR:
                    st = "HDMI_E";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_DVOF_PORT_CLR:
                    st = "HDMI_F";
                    break;

                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIA_PORT_CLR:
                    st = "MIPI_A";
                    break;
                case DIVA_PORT_TYPE_CLR.DIVA_INTMIPIC_PORT_CLR:
                    st = "MIPI_C";
                    break;
            }

            return st;
        }

        internal static bool IsDP(DIVA_PORT_TYPE_CLR port)
        {
            bool status = false;

            switch (port)
            {
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPE_PORT_CLR:
                case DIVA_PORT_TYPE_CLR.DIVA_INTDPF_PORT_CLR:
                    status = true;
                    break;
                default:
                    status = false;
                    break;
            }

            return status;
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
