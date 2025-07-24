namespace AudioEndpointVerification
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
                    CommonExtension.RegisterDll("IgfxExtBridge.dll");
                    Thread.Sleep(3000);
                    RegDispUtil();
                }
                return _displayUtil;
            }
        }

        private static void RegDispUtil()
        {
            _displayUtil = new DisplayUtil();
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
            Dictionary<DTDCategory, byte[]> dtdBlockData = new Dictionary<DTDCategory, byte[]>();
            byte[] blockData = new byte[TOTAL_DESCRIPTOR_BLOCK_SIZE];
            bool hasTimingInfo = false;
            bool hasMachineInfo = false;
            Enum.GetValues(typeof(DTDBlockInit)).Cast<DTDBlockInit>().ToList().ForEach(dtdEnum =>
            {
                blockData = GetDTDBlock(argEDIDData, dtdEnum, out hasTimingInfo, out hasMachineInfo);
                if (hasTimingInfo && !dtdBlockData.ContainsKey(DTDCategory.Timing))
                    dtdBlockData.Add(DTDCategory.Timing, blockData);
                if (hasMachineInfo && !dtdBlockData.ContainsKey(DTDCategory.MachineName))
                    dtdBlockData.Add(DTDCategory.MachineName, blockData);
            });
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
                    displayInfo.CompleteDisplayName = GetMachineName(dtdBlockData[DTDCategory.MachineName], argDisplayType);
                else
                {
                    Console.WriteLine("EDID for {0} does not have machine name block!", argDisplayType);
                }
            }
            displayInfo.DisplayName = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argDisplayType).Select(dI => dI.DisplayName).FirstOrDefault();
            if (string.IsNullOrEmpty(displayInfo.CompleteDisplayName))
                displayInfo.CompleteDisplayName = displayInfo.DisplayName;
            displayInfo.SerialNum = GetMonitorSerial(argEDIDData);
            CrossRefDisplayInfoColn(displayInfo);
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

        private static void CrossRefDisplayInfoColn(DisplayInfo argEnumeratedDisplay)
        {
            DisplayInfo displayInfo = DisplayInfoCollection.Collection.Where(dI => dI.DisplayType == argEnumeratedDisplay.DisplayType).FirstOrDefault();
            displayInfo.CompleteDisplayName = argEnumeratedDisplay.CompleteDisplayName;
            displayInfo.WindowsMonitorID = argEnumeratedDisplay.WindowsMonitorID;
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
    }
}
