namespace Intel.VPG.Display.Automation
{
    using Microsoft.Win32;
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    class EDIDData : FunctionalBase, IParse, IGetMethod
    {
        List<string> monitorDetails;
        RegistryKey Key;
        public List<string> MonitorDetails
        {
            get { return monitorDetails; }
        }
        private string[] DisplaySerialNo;
        public EDIDData()
        {
            monitorDetails = GetMonitorDetails();
        }
        private List<string> GetMonitorDetails()
        {
            List<string> MonitorIDs = new List<string>();
            Process monitorID_process = CommonExtensions.StartProcess("devcon.exe", "find = port *monitor*");
            while (!monitorID_process.StandardOutput.EndOfStream)
            {
                string line = monitorID_process.StandardOutput.ReadLine().ToLower().Trim();
                if (line.ToLower().Contains("display"))
                {
                    string[] Info = line.Split(':');
                    MonitorIDs.Add(Info.First().Trim());
                }
            }
            return MonitorIDs;
        }
        public object GetEDIDDetails(object windowsMonID)
        {
            foreach (string eachMonDetails in monitorDetails)
            {
                if (eachMonDetails.Contains(Convert.ToString(windowsMonID)))
                {
                    Log.Verbose("Fetching Monitor Details for {0} ", eachMonDetails);
                    if (Verify(eachMonDetails, true))
                        return GetEDIDRawData(eachMonDetails);
                    else
                    {
                        GetDisplayModels();
                        string[] monIDData = eachMonDetails.Split('\\');
                        foreach (string temp in DisplaySerialNo)
                        {
                            monIDData[1] = temp;
                            if (Verify(string.Join("\\", monIDData), true))
                                return GetEDIDRawData(string.Join("\\", monIDData));
                        }
                    }
                }
            }
            return null;
        }
        private object GetEDIDRawData(string MonDetails)
        {
            string Path = @"SYSTEM\CurrentControlSet\Enum\" + MonDetails + @"\Device Parameters";
            Key = Registry.LocalMachine.OpenSubKey(Path);
            byte[] edidData = Key.GetValue("EDID") as byte[];
            byte[] nullData = new byte[256 - edidData.Length];
            byte[] newData = edidData.Concat(nullData).ToArray();
            return newData;
        }

        private void GetDisplayModels()
        {
            string Path = @"SYSTEM\CurrentControlSet\Enum\Display";
            Key = Registry.LocalMachine.OpenSubKey(Path);
            DisplaySerialNo = Key.GetSubKeyNames();
        }

        private bool Verify(string MonDetails, bool getEDID = false)
        {
            Key = Registry.LocalMachine.OpenSubKey(@"SYSTEM\CurrentControlSet\Enum\" + MonDetails + @"\Device Parameters");
            if (Key == null)
                return false;
            else
            {
                if (getEDID)
                {
                    byte[] edidData = Key.GetValue("EDID") as byte[];
                    if (edidData != null)
                        return true;
                    else
                        return false;
                }
            }
            return true;
        }

        public void Parse(string[] args)
        {
            base.EnumeratedDisplays.ForEach(curDisp =>
                {
                   uint monitorId= curDisp.WindowsMonitorID;
                   object details = GetEDIDDetails(monitorId);
                   byte[] edid = details as byte[];
                   Log.Message(true,"\n -------{0} Edid Details----------",curDisp.DisplayType);
                   Log.Message("Display Name: {0} ,  WindowMonitor Id: {1} cuiMonitorId: {2}",curDisp.CompleteDisplayName,curDisp.WindowsMonitorID , curDisp.CUIMonitorID);
                   Log.Message("DTD Resolution");
                    curDisp.DTDResolutions.ForEach(curMode =>
                       {
                           Log.Message("\t HActive: {0} VActive: {1}  Pixel Clock: {2} Refresh Rate:{3} ",curMode.HzRes, curMode.VtRes,curMode.pixelClock,curMode.RR);
                       });
                    Log.Message("Edid Block");
                   for (int i = 0; i < 16; i++)
                   {
                       string str = "";
                       for (int j = 0; j < 16; j++)
                       {
                           str = str +" "+ edid[(i*16) + j];

                       }
                       Log.Message("{0}",str);
                   }
                });
        }
        private List<DisplayMode> GetEstablishedTiming1(byte[] argEdid)
        {
            int count = 0;
            byte block = argEdid[35];
            List<DisplayMode> estTiming1 = new List<DisplayMode>();
            while (count < 8)
            {
                if ((1 << count & block) != 0)
                {
                    switch (count)
                    {
                        //case 7: estTiming1.Add(new DisplayMode() { HzRes = 720, VtRes = 400, RR = 70 }); break; not considerding below 640x480
                       // case 6: estTiming1.Add(new DisplayMode() { HzRes = 720, VtRes = 400, RR = 88 }); break;
                        case 5: estTiming1.Add(new DisplayMode() { HzRes = 640, VtRes = 480, RR = 60 }); break;
                        case 4: estTiming1.Add(new DisplayMode() { HzRes = 640, VtRes = 480, RR = 67 }); break;
                        case 3: estTiming1.Add(new DisplayMode() { HzRes = 640, VtRes = 480, RR = 72 }); break;
                        case 2: estTiming1.Add(new DisplayMode() { HzRes = 640, VtRes = 480, RR = 75 }); break;
                        case 1: estTiming1.Add(new DisplayMode() { HzRes = 800, VtRes = 600, RR = 56 }); break;
                        case 0: estTiming1.Add(new DisplayMode() { HzRes = 800, VtRes = 600, RR = 60 }); break;
                    }

                }
                count++;
            }
            return estTiming1;
        }
        private List<DisplayMode> GetEstablishedTiming2(byte[] argEdid)
        {
            int count = 0;
            byte block = argEdid[36];
            List<DisplayMode> estTiming2 = new List<DisplayMode>();
            while (count < 8)
            {
                if ((1 << count & block) != 0)
                {
                    switch (count)
                    {

                        case 7: estTiming2.Add(new DisplayMode() { HzRes = 800, VtRes = 600, RR = 72 }); break;
                        case 6: estTiming2.Add(new DisplayMode() { HzRes = 800, VtRes = 600, RR = 75 }); break;
                        case 5: estTiming2.Add(new DisplayMode() { HzRes = 832, VtRes = 624, RR = 75 }); break;
                        case 4: estTiming2.Add(new DisplayMode() { HzRes = 1024, VtRes = 768, RR = 87 }); break;
                        case 3: estTiming2.Add(new DisplayMode() { HzRes = 1024, VtRes = 768, RR = 60 }); break;
                        case 2: estTiming2.Add(new DisplayMode() { HzRes = 1024, VtRes = 768, RR = 70 }); break;
                        case 1: estTiming2.Add(new DisplayMode() { HzRes = 1024, VtRes = 768, RR = 75 }); break;
                        case 0: estTiming2.Add(new DisplayMode() { HzRes = 1280, VtRes = 1024, RR = 75 }); break;
                    }
                }
                count++;
            }
            return estTiming2;
        }
        private List<DisplayMode> GetStandardTiming(byte[] argEdid)
        {
            List<DisplayMode> StandardTimings = new List<DisplayMode>();
            byte[] stdTimingBytes = GetArraySegment(argEdid, 38, (53 - 38) + 1);
            byte aspectRatioMask = 192; //"1100 0000"
            byte refreshRateMask = 63;//"0011 1111"
            DisplayMode resolution;

            for (int i = 0; i < stdTimingBytes.Length; i += 2)
            {
                byte firstByte = stdTimingBytes[i];
                byte secondByte = stdTimingBytes[i + 1];

                if (firstByte == 1 && secondByte == 1)
                {
                    //Reached the end of the valid mode list. Return
                    break;
                }
                uint XResolution = (uint)(firstByte * 8 + 248);
                uint YResolution;
                switch (aspectRatioMask & secondByte)
                {
                    //00 ->0
                    //01 ->64
                    //10 ->128
                    //11 ->192
                    case 0: YResolution = ((uint)((10.0 / 16.0) * XResolution)); break;
                    case 64: YResolution = ((uint)((3.0 / 4.0) * XResolution)); break;
                    case 128: YResolution = ((uint)((4.0 / 5.0) * XResolution)); break;
                    case 192: YResolution = ((uint)((9.0 / 16.0) * XResolution)); break;
                    default: throw new Exception("Invalid aspect ratio mask");
                }

                uint refreshRate = (uint)((refreshRateMask & secondByte) + 60);
                resolution = new DisplayMode() { HzRes = XResolution, VtRes = YResolution, RR = refreshRate };
                StandardTimings.Add(resolution);
            }
            return StandardTimings;
        }
        public T[] GetArraySegment<T>(T[] sourceArray, int startIndex, int length)
        {
            T[] newArray = new T[length];
            for (int i = startIndex; i < startIndex + length; i++)
            {
                newArray[i - startIndex] = sourceArray[i];
            }
            return newArray;
        }
        public object GetMethod(object argMessage)
        {
            EdidInfo edidList = argMessage as EdidInfo;
            DisplayType curDisp = edidList.DisplayType;

            EdidInfo edidInfo = new EdidInfo();
            uint monitorId = base.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.WindowsMonitorID).FirstOrDefault();
            object details = GetEDIDDetails(monitorId);
            byte[] edid = details as byte[];
            List<DisplayMode> estTiming1 = GetEstablishedTiming1(edid);
            List<DisplayMode> estTiming2 = GetEstablishedTiming2(edid);
            List<DisplayMode> standardTiming = GetStandardTiming(edid);

            //Log.Message(true, "Edid Info {0}", curDisp);
            //Log.Message("Established Timing1");
            //estTiming1.ForEach(curmode =>
            //{
            //    Log.Message("{0}", curmode.GetCurrentModeStr(false));
            //});
            //Log.Message("Established Timing2");
            //estTiming2.ForEach(curmode =>
            //{
            //    Log.Message("{0}", curmode.GetCurrentModeStr(false));
            //});
            //Log.Message("standard Timing");
            //standardTiming.ForEach(curmode =>
            //{
            //    Log.Message("{0}", curmode.GetCurrentModeStr(false));
            //});
            edidInfo.DisplayType = curDisp;
            edidInfo.EsatablishedTiming1 = estTiming1;
            edidInfo.EsatablishedTiming2 = estTiming2;
            edidInfo.StandardTiming = standardTiming;
            edidInfo.RawEdid = edid;

            return edidInfo;
        }

        public EdidInfo GetEdidInfo(DisplayType argDisplay, byte[] argEDIDData)
        {
            EdidInfo edidInfo = new EdidInfo();
            List<DisplayMode> estTiming1 = GetEstablishedTiming1(argEDIDData);
            List<DisplayMode> estTiming2 = GetEstablishedTiming2(argEDIDData);
            List<DisplayMode> standardTiming = GetStandardTiming(argEDIDData);

            //Log.Verbose(false, "Edid Info {0}", argDisplay);
            //Log.Verbose("Established Timing1");
            //estTiming1.ForEach(curmode =>
            //{
            //    Log.Verbose("{0}", curmode.GetCurrentModeStr(false));
            //});
            //Log.Verbose("Established Timing2");
            //estTiming2.ForEach(curmode =>
            //{
            //    Log.Verbose("{0}", curmode.GetCurrentModeStr(false));
            //});
            //Log.Verbose("standard Timing");
            //standardTiming.ForEach(curmode =>
            //{
            //    Log.Verbose("{0}", curmode.GetCurrentModeStr(false));
            //});
            edidInfo.DisplayType = argDisplay;
            edidInfo.EsatablishedTiming1 = estTiming1;
            edidInfo.EsatablishedTiming2 = estTiming2;
            edidInfo.StandardTiming = standardTiming;
            edidInfo.RawEdid = argEDIDData;
            return edidInfo;
        }
    }
}
