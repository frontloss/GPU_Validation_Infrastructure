using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Intel.VPG.Display.Automation
{
    internal class Helper
    {
        const int DIVA_MAX_EDID_BLOCKS = 6;
        const int DIVA_MAX_DPCD_DATA = 512;
        const int DIVA_MAX_ENCODERS = 20;
        const int DIVA_EDID_BLOCK_SIZE = 128;

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
                MessageBox.Show("ERROR: Exception in Enable/Disable ULT Framework: {0}",
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
                MessageBox.Show("ERROR: Exception in Enable/Disable Feature: {0}",
                    Exp.Message);
            }
        }

        internal static bool ULT_FW_PlugDisplay(List<bool> plugList, List<DIVA_PORT_TYPE_CLR> portList, List<uint> displayUIDList, List<string> edidFileList, List<bool> lowPowerList)
        {

            DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR divaSimulationDevicesArgs = new DIVA_GET_SET_SIMULATE_DEVICE_ARGS_CLR();
            divaSimulationDevicesArgs.NumDevices = (uint)portList.Count;

            for (int i = 0; i < DIVA_MAX_ENCODERS; i++)
                divaSimulationDevicesArgs.DeviceInfo[i].DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];

            for (int j = 0; j < plugList.Count; j++)
            {
                DIVA_DEVICE_INFO_CLR ult_Device_Info = new DIVA_DEVICE_INFO_CLR();
                ult_Device_Info.Attach = plugList[j];
                ult_Device_Info.OpType = DIVA_OP_TYPE_CLR.DIVA_OP_SET;
                ult_Device_Info.DisplayUID = displayUIDList[j];
                ult_Device_Info.DisplayEdid = new byte[DIVA_MAX_EDID_BLOCKS, DIVA_EDID_BLOCK_SIZE];
                ult_Device_Info.SimConnnectionInLowPower = lowPowerList[j];
                ult_Device_Info.PortType = portList[j];

                if (plugList[j] == true)
                {
                    if (portList[j] == DIVA_PORT_TYPE_CLR.DIVA_INTDPB_PORT_CLR || portList[j] == DIVA_PORT_TYPE_CLR.DIVA_INTDPC_PORT_CLR || portList[j] == DIVA_PORT_TYPE_CLR.DIVA_INTDPD_PORT_CLR || portList[j] == DIVA_PORT_TYPE_CLR.DIVA_INTDPA_PORT_CLR)
                    {
                        //Writing DPCD Data
                        string dpcdFilePath = edidFileList[j].Substring(0, edidFileList[j].Length - Path.GetExtension(edidFileList[j]).Length) + "_DPCD.bin";
                        if (!File.Exists(dpcdFilePath))
                        {
                            MessageBox.Show("File {0} doesn't exist", dpcdFilePath);
                            //Log.Fail("File {0} doesn't exist", dpcdFilePath);
                        }
                        else
                        {
                            ProgramAllDPCDData(displayUIDList[j], dpcdFilePath);
                        }
                    }

                    byte[] array = File.ReadAllBytes(edidFileList[j]);

                    for (int i = 0; i < array.Length; i++)
                    {
                        int row = i / 128;
                        int col = i % 128;

                        ult_Device_Info.DisplayEdid[row, col] = array[i];
                    }
                }
                divaSimulationDevicesArgs.DeviceInfo[j] = ult_Device_Info;
            }

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
                MessageBox.Show(string.Format("ERROR: Exception in GetSetSimulateDevices(). {0}",
                    Exp.Message));
            }

            return false;
        }

        internal static bool ProgramAllDPCDData(uint displayUID, string dpcdFile)
        {
            bool status = true;
            List<byte> ucDPCDs_202_204 = new List<byte> { 0xFF, 0xFF, 0xFF };
            List<byte> ucDPCDs_10_1F = new List<byte> { 0xA4, 0x1F, 0xBC, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

            //Write 14 bytes of DPCD data from _DPCD.bin file.
            byte[] dpcdData = File.ReadAllBytes(dpcdFile);
            status &= ULT_FW_WriteDPCD(0, displayUID, 0x0, dpcdData.ToList());

            //write ucDPCDs_202_204[] to address 202
            status &= ULT_FW_WriteDPCD(1, displayUID, 0x202, ucDPCDs_202_204);

            //write 0 to address 101
            status &= ULT_FW_WriteDPCD(2, displayUID, 0x101, 0);

            //write 0 to address 200
            status &= ULT_FW_WriteDPCD(3, displayUID, 0x200, 0);

            //write 0 to address 206
            status &= ULT_FW_WriteDPCD(4, displayUID, 0x206, 0);

            //write ucDPCDs_10_1F[] to address 202
            status &= ULT_FW_WriteDPCD(5, displayUID, 0x10, ucDPCDs_10_1F);

            //write 0 to address 600
            status &= ULT_FW_WriteDPCD(6, displayUID, 0x600, 1);

            //write 0 to address 205
            status &= ULT_FW_WriteDPCD(7, displayUID, 0x205, 1);

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
                EnumeratedDisplays.AddRange(divaEnableDisableArgs.DisplayDetailsArgs);
            }
            catch (Exception Exp)
            {
                MessageBox.Show("ERROR: Exception in EnumDevices.: {0}",
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
                MessageBox.Show("ERROR: Exception in GetDeviceConnectivity(): {0}",
                    Exp.Message);
            }

            return status;
        }
    }
}
