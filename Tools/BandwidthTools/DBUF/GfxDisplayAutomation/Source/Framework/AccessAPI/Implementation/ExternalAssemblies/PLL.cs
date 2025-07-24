using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Diagnostics;
using System.Text.RegularExpressions;
namespace Intel.VPG.Display.Automation
{
    public class PLL : FunctionalBase, IGetMethod
    {
        private uint _cfgcrValue;
        public uint CfgcrValue
        {
            get { return _cfgcrValue; }
            set { _cfgcrValue = value; }
        }
        private string displayMessage;

        public string DisplayMessage
        {
            get { return displayMessage; }
            set { displayMessage = value; }
        }
        public Dictionary<Platform, List<double>> PlatformCDClock
        {
            get
            {
                Dictionary<Platform, List<double>> platCDClock = new Dictionary<Platform, List<double>>()
                { 
                     {Platform.SKL,new List<double>(){337.5 ,450,540,675}}
                      // {Platform.SKL,new List<double>(){308.57,337.5 ,432,450,540,617.14,675}}
                };
                return platCDClock;
            }
        }
        public Dictionary<Platform, List<double>> PlatformCDClockIntermediate
        {
            get
            {
                Dictionary<Platform, List<double>> platCDClock = new Dictionary<Platform, List<double>>()
                { 
                       {Platform.SKL,new List<double>(){308.57,337.5 ,432,450,540,617.14,675}}
                };
                return platCDClock;
            }
        }
        public object GetMethod(object argMessage)
        {
            MMIORW mmioData = argMessage as MMIORW;
            Dictionary<string, System.Action<MMIORW>> featureMap = new Dictionary<string, Action<MMIORW>>() {{"CDCLK_CTL",GetCDClockCTLInfo},{"PLL_ENABLE_STATUS",GetPLLEnableInfo},
            {"PLL",GetPLLInfo},{"DPLL0_SSC",GetSSCInfo},{"DPLL1_SSC",GetSSCInfo},{"DPLL2_SSC",GetSSCInfo},{"DPLL3_SSC",GetSSCInfo}
            };
            List<string> cfgcrEvents = new List<string>() { "CFGCR1", "CFGCR2", "CFGCR3" };
            if (featureMap.Keys.Contains(mmioData.FeatureName))
            {
                featureMap[mmioData.FeatureName](mmioData);
            }
            if (cfgcrEvents.Contains(mmioData.FeatureName))
            {
                GetCFGCRInfo(mmioData);
            }
            return true;
        }
       
        private List<double> GetDPCDInfo(MMIORW argMMIOData)
        {
            List<double> linkRate = new List<double>();
            for (int i = 0; i < 8; i++)
            {
                RegisterInf reg = argMMIOData.RegInfList.ElementAt(i);
                string regValue = ReadMMIORW(reg.Offset, true);
                uint value = CompareRegValue(regValue, reg.Bitmap);
                Log.Message("{0} :{1} and multiplied by 200 {2}", reg.Offset, value, value * 200);
                if (value != 0)
                {
                    linkRate.Add(value * 200);
                }
            }
            return linkRate;
        }
        #region CDClock
        private void GetCDClockCTLInfo(MMIORW argMMIOData)
        {
            Log.Message(true, "CD Clock Data");

            List<double> linkRate = GetDPCDInfo(argMMIOData);
            List<double> pixelClockList = new List<double>();
            base.EnumeratedDisplays.ForEach(curDisp =>
            {
                List<DisplayMode> modeList = curDisp.DTDResolutions;
                Log.Message("{0}", curDisp.DisplayType);
                if (modeList != null)
                {
                    modeList.ForEach(curMode =>
                    {
                        pixelClockList.Add(curMode.pixelClock);
                        Log.Message("pixel clock : {0}", curMode.pixelClock);
                    });
                }
                else
                {
                    Log.Message("No mode");
                }
            });
            double maxPixelClock = pixelClockList.Max();
            double pixelClockValue = 0;

            List<double> platValue = new List<double>();
            if (linkRate.Count == 0)
                platValue = PlatformCDClock[base.MachineInfo.PlatformDetails.Platform]; //change teh platform
            else
                platValue = PlatformCDClockIntermediate[base.MachineInfo.PlatformDetails.Platform];

            //  List<double> platValue = PlatformCDClock[Platform.SKL];
            platValue.Sort();
            if (maxPixelClock <= platValue.First())
                pixelClockValue = platValue.First();
            else if (maxPixelClock > platValue.Last())
                Log.Fail("MaxPixelClock exceeding max supported by platform");
            else
            {
                for (int i = 0; i < platValue.Count - 1; i++)
                {
                    if (maxPixelClock >= platValue[i] && maxPixelClock <= platValue[i + 1])
                    {
                        pixelClockValue = platValue[i + 1];
                    }
                }
            }
            Log.Message("The expected CD Freqeuncy is {0}", pixelClockValue);

            Dictionary<string, System.Action<RegisterInf>> cdClockCTL = new Dictionary<string, Action<RegisterInf>>() { { "CD Freq Select", GetCDFreqSelectInfo }, { "DE CD2X Divider Select", GetDividerSelectInfo },
            { "DE CD2X Pipe Select", GetPipeSelectInfo }, { "Divmux CD Override", GetRegisterBitmap }, 
            { "Par0 CD Source Override", GetRegisterBitmap }, { "CD2X Source",GetRegisterBitmap }, {"CD Frequency Decimal",GetCDFreqDecimalInfo } };

            int index = 8;
            Log.Message("The count is {0}", argMMIOData.RegInfList.Count);
            foreach (string curEvent in cdClockCTL.Keys)
            {
                RegisterInf regInf = argMMIOData.RegInfList.ElementAt(index);
                cdClockCTL[curEvent](regInf);
                Log.Message("{0} :{1}", curEvent, DisplayMessage);

                if (curEvent == "CD Freq Select" || curEvent == "CD Frequency Decimal")
                {
                    if (pixelClockValue.ToString() == DisplayMessage)
                        Log.Success("Pixel clock {0} value matches with {1}", pixelClockValue, curEvent);
                    else
                        Log.Fail("{0} {1} does not match with Pixel clock {2}", curEvent, DisplayMessage, pixelClockValue);
                }

                index++;
            }
        }
        #endregion
        private void GetPLLEnableInfo(MMIORW argMMIOData)
        {
            Log.Message(true, "DPLL Enable Status");
            int index = 0;
            bool dispRegValue = true;
            List<int> enabledPLLList = new List<int>();
            argMMIOData.RegInfList.ForEach(curRegInf =>
            {
                string pllEnable = ReadMMIORW(curRegInf.Offset, dispRegValue);
                uint pllEnableValue = CompareRegValue(pllEnable, curRegInf.Bitmap);
                Log.Message("DPLL{0} enable status:{1}", index, pllEnableValue);
                if (pllEnableValue == 1)
                {
                    if (enabledPLLList.Contains(index))
                    {
                        Log.Alert("Multiple Displays assigned to DPLL {0} , verify Display PORT DPLL map",index);
                    }
                    enabledPLLList.Add(index);
                   
                    DPLL dpll;
                    Enum.TryParse<DPLL>(index.ToString(), true, out dpll);
                    if (base.EnumeratedDisplays.Where(dI => dI.dpll == dpll).ToList().Count > 1)
                    {
                        Log.Alert("Multiple Displays using {0}", dpll);
                        base.EnumeratedDisplays.ForEach(curDisp =>
                            {
                                if (curDisp.dpll == dpll)
                                    Log.Message("{0} using {1}", curDisp.DisplayType, dpll);
                            });
                    }
                }
                index++; dispRegValue = false;
            });
            List<DPLL> dpllList = new List<DPLL>();
            argMMIOData.currentConfig.CustomDisplayList.ForEach(curDisp =>
            {
                DisplayInfo display = base.EnumeratedDisplays.Where(dI=> dI.DisplayType==curDisp).Select(dI=> dI).FirstOrDefault();
                dpllList.Add(display.dpll);
            });
            if (dpllList.Count == enabledPLLList.Count)
                Log.Success("No extra PLL is enabled");
            else
            {
                Log.Fail("Mistmatch in No of display enumerated and PLL enabled");               
            }
            Log.Message("Enumerated Display Details:");
            base.EnumeratedDisplays.ForEach(curDisp =>
            {
                Log.Message("{0} : {1}", curDisp.DisplayType, curDisp.dpll);
            });
            Log.Message("The Enabled PLL Details:");
            enabledPLLList.ForEach(curPLL =>
            {
                Log.Message("DPLL {0} is enabled", curPLL);
            });
        }
        private void GetPLLInfo(MMIORW argMMIOData)
        {
            Log.Message(true, "DDI PORT Map");
            List<PORT> portMap = new List<PORT>() { {PORT.PORTA},{PORT.PORTB},{PORT.PORTC},
            {PORT.PORTD},{PORT.PORTE}};

            bool dispRegValue = true;
            argMMIOData.RegInfList.ForEach(curMMIO =>
            {
                string data = ReadMMIORW(curMMIO.Offset, dispRegValue);

                if (portMap.Count() != 0)
                {
                    PORT curPort = portMap.First();
                    if (argMMIOData.PortList.Contains(curPort))
                    {
                        DisplayInfo curDispInfo = base.EnumeratedDisplays.Where(dI => dI.Port == curPort).FirstOrDefault();
                        if (curDispInfo != null)
                        {
                            uint value = CompareRegValue(data, curMMIO.Bitmap);
                            DPLL dpll;
                            Enum.TryParse<DPLL>(value.ToString(), true, out dpll);
                            curDispInfo.dpll = dpll;
                            Log.Message("{0} {1}= {2}", curDispInfo.DisplayType, curDispInfo.Port, dpll);
                        }
                    }
                }
                portMap.RemoveAt(0);
                dispRegValue = false;
            });
        }
        private void GetSSCInfo(MMIORW argMMIOData)
        {
            Log.Message(true, "{0}  Register Data", argMMIOData.FeatureName);
            RegisterInf enable = argMMIOData.RegInfList.First();
            RegisterInf ssc = argMMIOData.RegInfList.ElementAt(1);
            RegisterInf hdmiMode = argMMIOData.RegInfList.ElementAt(2);
            RegisterInf linkRate = argMMIOData.RegInfList.Last();

            Dictionary<uint, string> linkRateMap = new Dictionary<uint, string>()
            {
                {0,"2700"},{1,"1350"},{2,"810"},{3,"1620"},{4,"1080"},{5,"2160"},{6,"reserved"},{7,"reserved"}
            };
            string data = ReadMMIORW(enable.Offset, true);
            uint enableBit = CompareRegValue(data, enable.Bitmap);
            if (enableBit == 1)
            {
                string sscValue = ReadMMIORW(ssc.Offset, false);
                uint sscValueInt = CompareRegValue(sscValue, ssc.Bitmap);
                Log.Message("SSC Enabled: {0}", sscValueInt);
                UpdateSSCInfo(argMMIOData.FeatureName, sscValueInt);

                string hdmiModeValue = ReadMMIORW(hdmiMode.Offset, false);
                uint hdmiModeInt = CompareRegValue(hdmiModeValue, hdmiMode.Bitmap);
                Log.Message("HDMI Enabled: {0}", hdmiModeInt);

                string linkRateValue = ReadMMIORW(linkRate.Offset, false);
                uint linkRateValueInt = CompareRegValue(linkRateValue, linkRate.Bitmap);
                if (linkRateMap.Keys.Contains(linkRateValueInt))
                    Log.Message("Link Rate: {0}", linkRateMap[linkRateValueInt]);
            }

        }
        private void UpdateSSCInfo(string argFeatureName, uint argValue)
        {
            Dictionary<string, DPLL> featureDpllMap = new Dictionary<string, DPLL>() { { "DPLL0_SSC", DPLL.DPLL0 }, { "DPLL1_SSC",DPLL.DPLL1 },
            {"DPLL2_SSC",DPLL.DPLL2},{"DPLL3_SSC",DPLL.DPLL3}};
            if (featureDpllMap.Keys.Contains(argFeatureName))
            {
                DPLL dpll = featureDpllMap[argFeatureName];
                DisplayInfo curDispInfo = base.EnumeratedDisplays.Where(dI => dI.dpll == dpll).FirstOrDefault();
                curDispInfo.ssc = Convert.ToBoolean(argValue);
                Log.Message("{0} SSC : {1}", curDispInfo.DisplayType, curDispInfo.ssc);
            }

        }

        private string ReadMMIORW(string argOffset, bool argDispValue)
        {
            DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
            driverData.input = Convert.ToUInt32(argOffset, 16);
            DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
            DriverEscape driverEscapeObj = new DriverEscape();
            bool status = driverEscapeObj.SetMethod(driverParams);
            string hexValue = driverData.output.ToString("X");
            Log.Message("The {0} :{1}", argOffset, hexValue);

            return hexValue;

            //Process regValue = CommonExtensions.StartProcess("MMIORW.exe", " r " + argOffset);//6C05C  70080           
            //string data = regValue.StandardOutput.ReadLine();  //Value:0x
            //if (argDispValue)
            //    Log.Verbose("Reg {0} : {1}", argOffset, data);
            //data = data.Substring(8, (data.Length - 8));
            //return data;
        }
        private uint CompareRegValue(string argRegValue, string argBitmap)
        {
            uint regValue = Convert.ToUInt32(argRegValue, 16);
            uint bitmap = Convert.ToUInt32(argBitmap, 16);

            string regValueBinary = Convert.ToString(regValue, 2);
            while (regValueBinary.Count() < 32)
            {
                regValueBinary = "0" + regValueBinary;
            }

            string bitmapBinary = Convert.ToString(bitmap, 2);
            while (bitmapBinary.Count() < 32)
            {
                bitmapBinary = "0" + bitmapBinary;
            }

            int startIndex = bitmapBinary.IndexOf('1');
            int lastIndex = bitmapBinary.LastIndexOf('1');

            string value = regValueBinary.Substring(startIndex, lastIndex - startIndex + 1);
            return Convert.ToUInt32(value, 2);
            //  return regValue & bitmap;
        }
        private void GetCFGCRInfo(MMIORW argMMIORW)
        {
            Log.Message(true, "CFGCR Register Data");
            Dictionary<string, System.Action<RegisterInf>> cfgcrMap = new Dictionary<string, Action<RegisterInf>>() { 
                {"DCOFraction",GetRegisterBitmap},{"DCOInteger",GetRegisterBitmap},{"Central Freq",GetCentralFrequency},
                {"pDiv",GetRegisterBitmap}, {"kDiv",GetkDiv} , {"qDivMode",GetRegisterBitmap},{"qDivValue",GetRegisterBitmap}
            };
            int index = 0;
            foreach (string curEvent in cfgcrMap.Keys)
            {
                RegisterInf regInf = argMMIORW.RegInfList.ElementAt(index);
                cfgcrMap[curEvent](regInf);
                Log.Message("{0}  : {1}", curEvent, DisplayMessage);
                index++;
            }
        }
        private void GetRegisterBitmap(RegisterInf argRegInf)
        {
            string dcoFraction = ReadMMIORW(argRegInf.Offset, false);
            CfgcrValue = CompareRegValue(dcoFraction, argRegInf.Bitmap);
            DisplayMessage = CfgcrValue.ToString();
        }
        private void GetCentralFrequency(RegisterInf argRegInf)
        {
            Dictionary<uint, string> centralFreq = new Dictionary<uint, string>() { { 0, "9600 MHz" }, { 1, "9000 MHz" }, { 2, "Reserved" }, { 3, "8400 MHz" } };
            GetRegisterBitmap(argRegInf);
            if (centralFreq.Keys.Contains(CfgcrValue))
                DisplayMessage = centralFreq[CfgcrValue];
        }
        private void GetkDiv(RegisterInf argRegInf)
        {
            Dictionary<uint, string> centralFreq = new Dictionary<uint, string>() { { 0, "K(P2) 5" }, { 1, "K(P2) 2" }, { 2, "K(P2) 3" }, { 3, "K(P2) 1" } };
            GetRegisterBitmap(argRegInf);
            if (centralFreq.Keys.Contains(CfgcrValue))
                DisplayMessage = centralFreq[CfgcrValue];
        }
        private void GetCDFreqSelectInfo(RegisterInf argRegInf)
        {
            Dictionary<uint, string> cdFreqSelect = new Dictionary<uint, string>() { { 0x0, "450 or 432 MHz" }, { 0x1, "540 MHz" }, { 0x2, "337.5 or 308.57 MHz[Default]" }, { 0x3, "675 or 617.14 MHz" } };
            string cdFreqValue = ReadMMIORW(argRegInf.Offset, true);
            uint cdFreqValueInt = CompareRegValue(cdFreqValue, argRegInf.Bitmap);
            if (cdFreqSelect.Keys.Contains(cdFreqValueInt))
                DisplayMessage = cdFreqSelect[cdFreqValueInt];
        }
        private void GetDividerSelectInfo(RegisterInf argRegInf)
        {
            Dictionary<uint, string> dividerSelect = new Dictionary<uint, string>() { { 0x0, "Divide by 1" }, { 0x1, "Divide by 1.5" }, { 0x2, "Divide by 2" }, { 0x3, "Divide by 4" } };
            string dividerSelectValue = ReadMMIORW(argRegInf.Offset, false);
            uint dividerSelectValueInt = CompareRegValue(dividerSelectValue, argRegInf.Bitmap);
            if (dividerSelect.Keys.Contains(dividerSelectValueInt))
                DisplayMessage = dividerSelect[dividerSelectValueInt];
        }
        private void GetPipeSelectInfo(RegisterInf argRegInf)
        {
            Dictionary<uint, string> pipeSelect = new Dictionary<uint, string>() { { 0x0, "PIPE_A" }, { 0x1, "PIPE_B" }, { 0x2, "PIPE_C" }, { 0x3, "NONE" } };
            string pipeSelectValue = ReadMMIORW(argRegInf.Offset, false);
            uint pipeSelectValueInt = CompareRegValue(pipeSelectValue, argRegInf.Bitmap);
            if (pipeSelect.Keys.Contains(pipeSelectValueInt))
                DisplayMessage = pipeSelect[pipeSelectValueInt];
        }
        private void GetCDFreqDecimalInfo(RegisterInf argRegInf)
        {
            Dictionary<uint, string> cdFreqDecimal = new Dictionary<uint, string>() { { 0X11E, "144 MHz CD" }, { 0X23E, "288 MHz CD" }, { 0X47E, "576 MHz CD" }, { 0X2FE, "384 MHz CD" },
            {0X4DE,"624 MHz CD"},{0X267,"308.57 MHz CD"},{0X2A1,"337.5 MHz CD [Default]"},{0X35E,"432 MHz CD"},{0X382,"450 MHz CD"},{0X436,"540 MHz CD"},
            {0X4D0,"617.14 MHz CD"},{0X544,"675 MHz CD"}};
            string cdFreqDecimalValue = ReadMMIORW(argRegInf.Offset, false);
            uint cdFreqDecimalValueInt = CompareRegValue(cdFreqDecimalValue, argRegInf.Bitmap);
            if (cdFreqDecimal.Keys.Contains(cdFreqDecimalValueInt))
            {
                DisplayMessage = cdFreqDecimal[cdFreqDecimalValueInt];
            }
            else
            {
                DisplayMessage = "Invalid CD Freq Decimal" + cdFreqDecimalValueInt;
            }
        }
    }
}


