using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Win32;
namespace Intel.VPG.Display.Automation
{
    class SB_CDClock_Base:TestBase
    {
        protected List<string> CDClockRegisterList
        {
            get
            {
                List<string> CDClockRegisterList = new List<string>() { "EDP_VERSION", "DPCD", "CDCLK_CTL" };
                return CDClockRegisterList;
            }
        }
        public Dictionary<Platform, List<double>> PlatformCDClock
        {
            get
            {
                Dictionary<Platform, List<double>> platCDClock = new Dictionary<Platform, List<double>>()
                { 
                     {Platform.SKL,new List<double>(){337.5 ,450,540,675}}
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
        protected void VerifyCDClockRegisters()
        {
            if (base.MachineInfo.PlatformDetails.Platform == Platform.CNL)
            {
                Log.Abort("Skipping CD Clock check for CNL");
                return;
            }

            Log.Message(true, "Verify CD Clock");
            List<double> platformLinkRate = new List<double>();
            string edpVersionEvent = CDClockRegisterList.First();
            EventInfo eventList = GetRegisterList(edpVersionEvent);
            if (GetEdpVersion(eventList))
            {
                Log.Message("EDP Version is 1.4");
                string dpcdEvent = CDClockRegisterList.ElementAt(1); //dpcdEvent
                EventInfo dpcdEventList = GetRegisterList(dpcdEvent);
                if (GetResolutionList(dpcdEventList))
                {
                    platformLinkRate = PlatformCDClockIntermediate[base.MachineInfo.PlatformDetails.Platform];
                }
                else
                {
                    platformLinkRate = PlatformCDClock[base.MachineInfo.PlatformDetails.Platform];
                }
            }
            else
            {
                Log.Message("EDP Version is not 1.4");
                platformLinkRate = PlatformCDClock[base.MachineInfo.PlatformDetails.Platform];
            }
            //pixel clock
            Log.Message(true, "Calculate Pixel Clock");
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            double expectedCdClockValue = 0;

            if (currentConfig.ConfigType == DisplayConfigType.SD && currentConfig.PrimaryDisplay == DisplayType.EDP)
            {
                List<double> pixelClockList = new List<double>();
                currentConfig.CustomDisplayList.ForEach(curDisp =>
                {
                    DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).First();
                    DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                    pixelClockList.Add(actualMode.pixelClock);
                });

                double maxPixelClock = pixelClockList.Max();
                Log.Message("The max Pixel clock is {0}.", maxPixelClock);

                platformLinkRate.Sort();
                if (maxPixelClock <= platformLinkRate.First())
                    expectedCdClockValue = platformLinkRate.First();
                else if (maxPixelClock > platformLinkRate.Last())
                    Log.Fail("MaxPixelClock exceeding max supported by platform.");
                else
                {
                    for (int i = 0; i < platformLinkRate.Count - 1; i++)
                    {
                        if (maxPixelClock >= platformLinkRate[i] && maxPixelClock <= platformLinkRate[i + 1])
                        {
                            expectedCdClockValue = platformLinkRate[i + 1];
                        }
                    }
                }
            }
            else //other than SD-EDP configurations.
            {
                expectedCdClockValue = platformLinkRate.Max();
            }

            Log.Message("The expected CD Freqeuncy is {0}", expectedCdClockValue);
            Dictionary<double, string> cdClockEventList = new Dictionary<double, string>() {
            {308.57,"LINKRATE308"},{337.5,"LINKRATE337"},{432,"LINKRATE432"},{450,"LINKRATE450"},{540,"LINKRATE540"},
            {617.14,"LINKRATE617"},{675,"LINKRATE675"}
            };
            if (cdClockEventList.Keys.Contains(expectedCdClockValue))
            {
                if(VerifyRegisters(cdClockEventList[expectedCdClockValue], PIPE.NONE, PLANE.NONE, PORT.NONE, true))
                {
                    Log.Success("CD Clock:{0} is programmed as expected.", expectedCdClockValue);
                }
                else
                {
                    Log.Fail("Can be driven with CD Clock: {0}", expectedCdClockValue);
                }
            }
            else
            {
                Log.Fail("Computed PixelClock:{0} not present in the expected CdClockEventList.", expectedCdClockValue);
            }
        }

        protected bool GetEdpVersion(EventInfo eventList)
        {
            
            foreach (RegisterInf reginfo in eventList.listRegisters)
            {
                DpcdInfo dpcd = new DpcdInfo();
                dpcd.Offset = Convert.ToUInt32(reginfo.Offset, 16);
                dpcd.DispInfo = base.EnumeratedDisplays.Find(dI => dI.DisplayType == DisplayType.EDP);
                AccessInterface.GetFeature<DpcdInfo, DpcdInfo>(Features.DpcdRegister, Action.GetMethod, Source.AccessAPI, dpcd);
                if (CompareRegisters(dpcd.Value, reginfo))
                {
                    return true;
                }
            }
            return false;
        }
        protected bool ReadRegister(EventInfo argEventInfo, bool compare = true)
        {
            bool regValueMatched = true;
            foreach (RegisterInf reginfo in argEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (!CompareRegisters(driverData.output, reginfo))
                    {
                        if (compare)
                            Log.Fail("Register with offset {0} doesnot match required values", reginfo.Offset);
                        regValueMatched = false;
                    }
            }
            return regValueMatched;
        }
        protected EventInfo GetRegisterList(string argResgiterEvent)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = PLANE.NONE;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = argResgiterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
            return returnEventInfo;
        }
        protected bool GetResolutionList(EventInfo argEventInfo)
        {
            bool interRes = false;
            List<double> intermediateResolutionList = new List<double>();
            foreach (RegisterInf reginfo in argEventInfo.listRegisters)
            {
                Log.Message("Offset being checked = {0} Bitmap being checked {1}  Value to be got = {2}", reginfo.Offset, reginfo.Bitmap, reginfo.Value);
                DriverEscapeData<uint, uint> driverData = new DriverEscapeData<uint, uint>();
                driverData.input = Convert.ToUInt32(reginfo.Offset, 16);
                DriverEscapeParams driverParams = new DriverEscapeParams(DriverEscapeType.Register, driverData);
                if (!AccessInterface.SetFeature<bool, DriverEscapeParams>(Features.DriverEscape, Action.SetMethod, driverParams))
                    Log.Abort("Failed to read Register with offset as {0}", driverData.input);
                else
                    if (driverData.output != 0)
                    {
                        uint regOutput = driverData.output;
                        uint value = regOutput * 200;
                        intermediateResolutionList.Add(value);
                        Log.Message("The Intermediate resolution , link rate is {0}", value);
                        interRes = true;
                    }
            }
            return interRes;
        }
        protected void UpdateDisableCDClockChangeRegistry()
        {
            if (base.MachineInfo.PlatformDetails.Platform == Platform.SKL)
            {
                Log.Message(true, "Make changes in Registry for DisableCDClockChange");
                RegistryParams registryParams = new RegistryParams();
                registryParams.value = 0;
                registryParams.infChanges = InfChanges.ModifyInf;

                registryParams.registryKey = Registry.LocalMachine;
                registryParams.keyName = "DisableCDClockChange";
                AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
            }
        }
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());           
        }
    }
}
