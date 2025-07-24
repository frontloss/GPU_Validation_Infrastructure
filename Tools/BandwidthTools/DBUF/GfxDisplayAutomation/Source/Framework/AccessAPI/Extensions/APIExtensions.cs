namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using System.Text.RegularExpressions;

    using IgfxExtBridge_DotNet;
    using System.Threading;

    internal static class APIExtensions
    {
        private static List<long> _initEventIDList = null;
        private static List<long> _resumeEventIDList = null;
        private static List<string> _initSourceList = null;
        private static List<string> _resumeSourceList = null;
        private static List<string> _initDescriptionList = null;
        private static List<string> _resumeDescriptionList = null;
        private static DisplayUtil _displayUtil = null;

        private const int TOTAL_DESCRIPTOR_BLOCK_SIZE = 18;
        private const byte MONITOR_NAME_EXISTS = 252;
        private const string EDP_Machine_Name = "Built-in Display";

        static APIExtensions()
        {
            _initEventIDList = new List<long>() { 42, 506 };
            _resumeEventIDList = new List<long>() { 1, 507 };
            _initSourceList = new List<string>() { "Microsoft-Windows-Kernel-Power" };
            _resumeSourceList = new List<string>() { "Microsoft-Windows-Kernel-Power", "Microsoft-Windows-Power-Troubleshooter" };
            _initDescriptionList = new List<string>() { "The system is entering connected standby", "The system is entering sleep" };
            _resumeDescriptionList = new List<string>() { "The system has resumed from sleep", "The system is exiting connected standby", "The system has returned from a low power state" };
        }

        internal static DisplayUtil DisplayUtil
        {
            get
            {
                if (null == _displayUtil)
                {
                    CommonExtensions.RegisterDll("IgfxExtBridge.dll");
                    Thread.Sleep(3000);
                    RegDispUtil();
                }
                return _displayUtil;
            }
        }

        private static void RegDispUtil()
        {
            Log.Verbose("Creating DisplayUtil reference");
            _displayUtil = new DisplayUtil();
            if (null == _displayUtil)
            {
                Log.Sporadic(false, "SDK:: DisplayUtil instance not created! A reboot might be required.");
                PowerEvent powerEvent = new PowerEvent();
                powerEvent.SetMethod(new PowerParams() { PowerStates = PowerStates.S5, Delay = 5 });
            }
            else
            {
                Log.Verbose("SDK:: DisplayUtil instance created");
                string pErrorDescription = "";
                IGFX_SYSTEM_CONFIG_DATA_N_VIEWS sysConfig = new IGFX_SYSTEM_CONFIG_DATA_N_VIEWS();
                IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.UNKNOWN_ERROR;
                _displayUtil.GetSystemConfigDataNViews(ref sysConfig, out igfxErrorCode, out pErrorDescription);

                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Alert(String.Format("{0}:Unable to get system configuration data-{1}", igfxErrorCode.ToString(), pErrorDescription));
                }
                else
                {
                    if (sysConfig.uiNDisplays != 0)
                        Log.Message("{0} no of display active", sysConfig.uiNDisplays);
                    else
                        Log.Message("GetSystemConfiguration Returned 0 displays");
                }
            }
        }

        internal static List<long> InitEventIDList
        {
            get { return _initEventIDList; }
        }
        internal static List<long> ResumeEventIDList
        {
            get { return _resumeEventIDList; }
        }
        internal static List<string> InitSourceList
        {
            get { return _initSourceList; }
        }
        internal static List<string> ResumeSourceList
        {
            get { return _resumeSourceList; }
        }
        internal static List<string> InitDescriptionList
        {
            get { return _initDescriptionList; }
        }
        internal static List<string> ResumeDescriptionList
        {
            get { return _resumeDescriptionList; }
        }
        internal static int BufferResumeDelay
        {
            get { return 5; }
        }
        internal static List<string> GetDisplayAdapters()
        {
            List<string> displayAdaptersList = new List<string>();
            DISPLAY_DEVICE deviceName = new DISPLAY_DEVICE();
            deviceName.cb = Marshal.SizeOf(deviceName);
            uint devId = 0;
            while (Interop.EnumDisplayDevices(null, devId++, ref deviceName, 0))
                displayAdaptersList.Add(deviceName.DeviceName);
            return displayAdaptersList;
        }
        internal static void SetMonitorNameNOptimalMode(List<DisplayInfo> argEnumeratedDisplays, DisplayType argDisplayType, byte[] argEDIDData)
        {
            Dictionary<DTDCategory, List<byte[]>> dtdBlockData = new Dictionary<DTDCategory, List<byte[]>>();
            byte[] blockData = new byte[TOTAL_DESCRIPTOR_BLOCK_SIZE];
            bool hasTimingInfo = false;
            bool hasMachineInfo = false;
            List<byte[]> timingBlockList = new List<byte[]>();
            int ExtensionBlockCount = argEDIDData[126];
            Log.Verbose("Display {0} has {1} extension block", argDisplayType, ExtensionBlockCount);
            Enum.GetValues(typeof(DTDBlockInit)).Cast<DTDBlockInit>().ToList().ForEach(dtdEnum =>
            {
                blockData = GetDTDBlock(argEDIDData, dtdEnum, out hasTimingInfo, out hasMachineInfo);
                if (hasTimingInfo)
                {
                    timingBlockList.Add(blockData);

                }
                if (hasMachineInfo && !dtdBlockData.ContainsKey(DTDCategory.MachineName))
                {
                    List<byte[]> tempData = new List<byte[]>();
                    tempData.Add(blockData);
                    dtdBlockData.Add(DTDCategory.MachineName, tempData);
                }
            });

            if (ExtensionBlockCount != 0 && argEDIDData.Length > 128) //Start of extension block
            {
                int extensionBlockBase = 128;

                int d = argEDIDData[extensionBlockBase + 2];
                if (d != 0)
                {
                    //Log.Verbose("DTD block in extension block start from {0} th byte", d);

                    int bytePosition = extensionBlockBase + d;
                    for (; (bytePosition + TOTAL_DESCRIPTOR_BLOCK_SIZE) < argEDIDData.Length; )
                    {
                        byte[] dtdBaseBlock = argEDIDData.Skip(bytePosition).Take(2).ToArray();
                        if (!dtdBaseBlock.First().Equals(0) && !dtdBaseBlock.Skip(1).First().Equals(0))
                        {
                            byte[] dtdBlock = argEDIDData.Skip(bytePosition).Take(TOTAL_DESCRIPTOR_BLOCK_SIZE).ToArray();
                            timingBlockList.Add(dtdBlock);
                        }
                        bytePosition += TOTAL_DESCRIPTOR_BLOCK_SIZE;
                    }
                }
            }

            DisplayInfo displayInfo = argEnumeratedDisplays.Where(cI => cI.DisplayType == argDisplayType).FirstOrDefault();

            #region check for Audio capable pannel
            if (argEDIDData[126] == 0)
                displayInfo.isAudioCapable = false;
            else
            {
                if ((argEDIDData[131] & 64) == 64)
                    displayInfo.isAudioCapable = true;
                else
                    displayInfo.isAudioCapable = false;
            }
            #endregion

            if (argDisplayType == DisplayType.EDP)
                displayInfo.CompleteDisplayName = EDP_Machine_Name;
            else
            {
                if (dtdBlockData.ContainsKey(DTDCategory.MachineName))
                    displayInfo.CompleteDisplayName = GetMachineName(dtdBlockData[DTDCategory.MachineName][0], argDisplayType);
                else
                    Log.Sporadic(false, "EDID for {0} does not have machine name block!", argDisplayType);
            }
            displayInfo.DisplayName = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayType).Select(dI => dI.DisplayName).FirstOrDefault();
            displayInfo.ConnectorType = DisplayInfoCollection.Collection.Where(DI => DI.DisplayType == argDisplayType).Select(CT => CT.ConnectorType).FirstOrDefault();
            if (string.IsNullOrEmpty(displayInfo.CompleteDisplayName))
                displayInfo.CompleteDisplayName = displayInfo.DisplayName;
            displayInfo.SerialNum = GetMonitorSerial(argEDIDData);

            CrossRefDisplayInfoColn(displayInfo);
            GetColorimetry(argEDIDData, argDisplayType, displayInfo);
            GetVRRInfo(argEDIDData, argDisplayType, displayInfo);

            if (timingBlockList.Count != 0)
            {
                displayInfo.DTDResolutions = GetDTDResolutions(timingBlockList, argDisplayType);
                displayInfo.EdidResolutions = GetEDIDResolutions(displayInfo, argEDIDData);
                displayInfo.DisplayMode = displayInfo.DTDResolutions.First();
                displayInfo.IsPortraitPanel = displayInfo.DisplayMode.HzRes < displayInfo.DisplayMode.VtRes;
            }
        }
        internal static byte[] GetDataBytes(object InputData)
        {
            uint dataSize = (uint)Marshal.SizeOf(InputData);

            IntPtr ptr = Marshal.AllocHGlobal((int)dataSize);
            byte[] byteData = new byte[dataSize];
            Marshal.StructureToPtr(InputData, ptr, true);
            Marshal.Copy(ptr, byteData, 0, (int)dataSize);
            return byteData;
        }
        internal static void GetDataFromBytes(byte[] InputData, ref object OutputData)
        {
            int OutputDataSize = Marshal.SizeOf(OutputData);
            IntPtr ptr = Marshal.AllocHGlobal(OutputDataSize);

            Marshal.Copy(InputData, 0, ptr, OutputDataSize);

            Marshal.PtrToStructure(ptr, OutputData);
            Marshal.FreeHGlobal(ptr);
        }
        internal static byte[] GetMagicDataBytes(object InputData)
        {
            byte[] byteData = APIExtensions.GetDataBytes(InputData);
            byte magicNumber = 0xAA;

            for (int count = 0; count < byteData.Length; count++)
            {
                byteData[count] ^= magicNumber;
            }

            return byteData;
        }

        private static void GetVRRInfo(byte[] argEDIDData, DisplayType argDisplayType, DisplayInfo argEnumeratedDisplay)
        {
            if (argDisplayType == DisplayType.EDP || argDisplayType == DisplayType.DP)
            {
                byte val = argEDIDData[24]; //feature support
                argEnumeratedDisplay.VRRInfo.ContFreqSup = ((val & 0x1) == 1);

                if (argEnumeratedDisplay.VRRInfo.ContFreqSup)
                {
                    uint index = 54; //start of 1st 18 byte descriptor
                    for (; index < 126; index += 18)
                    {
                        if (argEDIDData[index + 3] != 0xFD) continue;

                        argEnumeratedDisplay.VRRInfo.RR_min = argEDIDData[index + 5];
                        argEnumeratedDisplay.VRRInfo.RR_max = argEDIDData[index + 6];
                    }
                }
            }
        }

        private static void GetColorimetry(byte[] argEDIDData, DisplayType argDisplayType, DisplayInfo argEnumeratedDisplay)
        {
            argEnumeratedDisplay.ColorInfo.MaxDeepColorValue = GetMaxDeepColorValue(argEDIDData, argEnumeratedDisplay);

            if (argEDIDData.Length <= 128)
                return;
            byte[] ceaBlockEDID = argEDIDData.Skip(128).ToArray();
            byte[] block = ceaBlockEDID.Skip(4).Take(ceaBlockEDID[2] - 4).ToArray();
            byte totalBytesMask = 31;
            List<byte> colorimetryBlock = new List<byte>();
            for (int i = 0; i < block.Length; i++)
            {
                if ((block[i] >> 5) != (byte)7)//colorimetry descriptor block
                {
                    i = i + (block[i] & totalBytesMask);
                    continue;
                }
                else
                {
                    for (int j = 0; j < (block[i] & totalBytesMask); j++)
                    {
                        colorimetryBlock.Add(block[i + j + 1]);
                    }
                    break;
                }
            }
            // check xvYcc & YcBcr only for HDMI display.
          if (argEnumeratedDisplay.DisplayType==DisplayType.HDMI )
            {
                argEnumeratedDisplay.ColorInfo.IsYcBcr = ((ceaBlockEDID[3] & 48) == 48);
                argEnumeratedDisplay.ColorInfo.IsXvYcc = (colorimetryBlock.Count > 0 && argEnumeratedDisplay.ColorInfo.IsYcBcr && ((colorimetryBlock[1] & 3) == 3));
            }
        }
        private static int GetMaxDeepColorValue(byte[] argEDIDData, DisplayInfo argEnumeratedDisplay)
        {
            int maxDeepColorValue = 8;
            int tempDeepcolorValue = 0;

            //page24 in edid1.4 spec
            if ((argEDIDData[20] & 135) == 133)//Bit7==1:Digital display, Bit0==1,Bit1==0,Bit2==1 represents DP display
            {
                tempDeepcolorValue = argEDIDData[20] & 0x70;
                if (!(tempDeepcolorValue == 0 || tempDeepcolorValue == 7))
                {
                    maxDeepColorValue = 4 + ((argEDIDData[20] & 0x70) >> 4) * 2;
                }
            }

            //CEA extension block
            if (argEDIDData.Length > 128)
            {
                byte[] block = argEDIDData.Skip(132).Take(argEDIDData[130] - 4).ToArray();//128+4
                byte totalBytesMask = 31;
                List<byte> vendorBlock = new List<byte>();
                for (int i = 0; i < block.Length; i++)
                {
                    if ((block[i] >> 5) != (byte)3)//vendor descriptor block
                    {
                        i = i + (block[i] & totalBytesMask);
                        continue;
                    }
                    else
                    {
                        for (int j = 0; j < (block[i] & totalBytesMask); j++)
                        {
                            vendorBlock.Add(block[i + j + 1]);
                        }
                        break;
                    }
                }

                //HDMI Licencing
                if ((vendorBlock.Count >= 6) && vendorBlock[0] == 3 && vendorBlock[1] == 12 && vendorBlock[2] == 0)
                {
                    if ((vendorBlock[5] & 0x10) == 0x10)
                    {
                        maxDeepColorValue = 10;
                    }
                    if ((vendorBlock[5] & 0x20) == 0x20)
                    {
                        maxDeepColorValue = 12;
                    }
                    if ((vendorBlock[5] & 0x40) == 0x40)
                    {
                        maxDeepColorValue = 16;
                    }
                }
            }
            return maxDeepColorValue;
        }
        private static void CrossRefDisplayInfoColn(DisplayInfo argEnumeratedDisplay)
        {
            DisplayInfo displayInfo = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argEnumeratedDisplay.DisplayType).FirstOrDefault();
            displayInfo.CompleteDisplayName = argEnumeratedDisplay.CompleteDisplayName;
            displayInfo.WindowsMonitorID = argEnumeratedDisplay.WindowsMonitorID;
            displayInfo.DisplayMode = argEnumeratedDisplay.DisplayMode;
        }
        private static byte[] GetDTDBlock(byte[] argEdidRaw, DTDBlockInit argStart, out bool argHasTimingInfo, out bool argHasMachineInfo)
        {
            byte[] dtdBlock = argEdidRaw.Skip((int)argStart).Take(TOTAL_DESCRIPTOR_BLOCK_SIZE).ToArray();
            argHasTimingInfo = !dtdBlock.First().Equals(0) && !dtdBlock.Skip(1).First().Equals(0);
            argHasMachineInfo = dtdBlock.Contains(MONITOR_NAME_EXISTS);
            return dtdBlock;
        }
        private static string GetMachineName(byte[] argDTDData, DisplayType argDisplayType)
        {
            string machineName = string.Concat(
                 DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayType).Select(dI => dI.DisplayName).FirstOrDefault(),
                 " ",
                 ASCIIEncoding.ASCII.GetString(argDTDData.Skip(5).Take(13).ToArray())).Trim();
            return new Regex("\\n").Replace(machineName, string.Empty).Trim();
        }
        private static DisplayMode GetOptimalResolution(byte[] argDTDData, DisplayType argDisplayType)
        {
            DTD dtd = new DTD(argDTDData, argDisplayType);
            return dtd.DisplayMode;
        }
        private static string GetMonitorSerial(byte[] argDTDData)
        {
            string monitorSerial = string.Empty;
            UInt16 wmodelNum = 0;
            UInt16 wManfProdId = 0;
            byte byASCII_Offset = 0;

            wmodelNum = MakeWord(argDTDData[9], argDTDData[8]);
            wmodelNum <<= 1;

            for (int index = 0; index < 3; index++)
            {
                byASCII_Offset = (byte)GetBits(wmodelNum, 15, 5);
                String tempStr = new String((char)('A' + (byASCII_Offset - 1)), 1);
                monitorSerial += tempStr;
                wmodelNum <<= 5;
            }

            wManfProdId = MakeWord(argDTDData[10], argDTDData[11]);
            monitorSerial += wManfProdId.ToString("X4");
            return monitorSerial;
        }
        private static UInt16 MakeWord(byte LSByte, byte MSByte)
        {
            UInt16 u16Word = (UInt16)(MSByte << 8);
            return (UInt16)(u16Word | LSByte);
        }
        private static UInt32 GetBits(UInt32 x, byte p, byte n)
        {
            return ((UInt32)(x >> (p + 1 - n))) & ((UInt32)(~(~0 << n)));
        }
        private static List<DisplayMode> GetDTDResolutions(List<byte[]> argDTDData, DisplayType argDisplayType)
        {
            List<DisplayMode> dtdResolutions = new List<DisplayMode>();
            argDTDData.ForEach(DTDData =>
            {
                DTD dtd = new DTD(DTDData, argDisplayType);
                dtdResolutions.Add(dtd.DisplayMode);
            });
            return dtdResolutions;
        }

        private static List<DisplayMode> GetEDIDResolutions(DisplayInfo argDisplayInfo, byte[] argEDIDData)
        {
            List<DisplayMode> EdidResolutions = new List<DisplayMode>();
            EDIDData edidData = new EDIDData();
            EdidInfo edidInfo = new EdidInfo();
            edidInfo = edidData.GetEdidInfo(argDisplayInfo.DisplayType, argEDIDData);

            EdidResolutions.AddRange(argDisplayInfo.DTDResolutions);
            EdidResolutions.AddRange(edidInfo.EsatablishedTiming1);
            EdidResolutions.AddRange(edidInfo.EsatablishedTiming2);
            EdidResolutions.AddRange(edidInfo.StandardTiming);
            return EdidResolutions;
        }
    }
}
