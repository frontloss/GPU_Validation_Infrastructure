namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System.Threading;
    using System.Windows.Forms;
    using Microsoft.Win32;
    class SB_Dbuf_Base : TestBase
    {
        OverlayParams _overlay = new OverlayParams();
        public Dictionary<PLANE, List<string>> PlaneEventMap
        {
            get
            {
                //Dictionary<PIPE, List<string>> planeEvent = new Dictionary<PIPE, List<string>>() {{PIPE.PIPE_A,new List<string>(){"PLANE_1_A", "PLANE_2_A", "PLANE_3_A"}},
                //                                             {PIPE.PIPE_B,new List<string>(){"PLANE_1_B", "PLANE_2_B", "PLANE_3_B"}},
                //                                             {PIPE.PIPE_C,new List<string>(){"PLANE_1_C", "PLANE_2_C", "PLANE_3_C"}} ,
                //                                             {PIPE.PIPE_EDP,new List<string>(){"PLANE_1_A", "PLANE_2_A", "PLANE_3_A"}} };

                Dictionary<PLANE, List<string>> planeEvent = new Dictionary<PLANE, List<string>>() {{PLANE.PLANE_A,new List<string>(){"PLANE_1_A", "PLANE_2_A", "PLANE_3_A"}},
                                                             {PLANE.PLANE_B,new List<string>(){"PLANE_1_B", "PLANE_2_B", "PLANE_3_B"}},
                                                             {PLANE.PLANE_C,new List<string>(){"PLANE_1_C", "PLANE_2_C", "PLANE_3_C"}} ,
                                                             };
                return planeEvent;
            }
        }

        public Dictionary<int, List<PLANE>> ConfigPlaneMap
        {
            get
            {
                Dictionary<int, List<PLANE>> configPlane = new Dictionary<int, List<PLANE>>() { {1,new List<PLANE>(){PLANE.PLANE_A}},
                {2,new List<PLANE>(){PLANE.PLANE_A,PLANE.PLANE_B}},{3,new List<PLANE>(){PLANE.PLANE_A,PLANE.PLANE_B,PLANE.PLANE_C}}};
                return configPlane;
            }
        }
        string _hTotalEvent = "HACTIVE";
        string _mipi_hTotalEvent = "MIPI_HACTIVE";
        string _mipi_laneCount = "MIPI_LANECOUNT";
        string _mipi_Bpp = "MIPI_BitsPerPixel";
        List<PipeDbufInfo> _initialDBuf = new List<PipeDbufInfo>();
        protected List<PipeDbufInfo> ReadYTilingInfo(DisplayConfig argDispConfig)
        {
            List<PipeDbufInfo> _pipeDBufInfo = new List<PipeDbufInfo>();
            argDispConfig.DisplayList.ForEach(curDisp =>
            {

                PipeDbufInfo curPipeDbuf = new PipeDbufInfo();
                PipePlaneParams pipePlane1 = new PipePlaneParams(curDisp);
                pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);

                Log.Message(true, "The Display is {0} and the pipe is {1} and plane is {2}", curDisp, pipePlane1.Pipe, pipePlane1.Plane);
                List<string> eventList = PlaneEventMap[pipePlane1.Plane];

                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);

                curPipeDbuf.DisplayType = curDisp;
                curPipeDbuf.Pipe = pipePlane1.Pipe;
                curPipeDbuf.plane = pipePlane1.Plane;
                curPipeDbuf.DisplayConfigType = argDispConfig.ConfigType;
                eventList.ForEach(curEvent =>
                {
                    Log.Message("the event is {0}", curEvent);
                    DBufInfo DBufValue = VerifyRegisters(curEvent, pipePlane1.Pipe, displayInfo.Port, curDisp);

                    if (curEvent.Contains("1"))
                        curPipeDbuf.PlaneA = DBufValue;
                    else if (curEvent.Contains("2"))
                        curPipeDbuf.PlaneB = DBufValue;
                    else if (curEvent.Contains("3"))
                        curPipeDbuf.PlaneC = DBufValue;
                    else
                        Log.Message("in nothing");
                });
                Log.Message("adding for {0}", curPipeDbuf.DisplayType);
                _pipeDBufInfo.Add(curPipeDbuf);
            });
            return _pipeDBufInfo;
        }
        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
            {
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());
        }
        protected void PerformYTiling(DisplayConfig argDispConfig)
        {
            //List<PipeDbufInfo> dbufList = ReadYTilingInfo(argDispConfig);
            //VerifyYTilingInfo(dbufList);                         
        }

        private void VerifyYTilingInfo(List<PipeDbufInfo> argDBufList)
        {
            _initialDBuf = AccessInterface.GetFeature<List<PipeDbufInfo>, List<PipeDbufInfo>>(Features.DBuf, Action.GetMethod, Source.AccessAPI, argDBufList);
            Log.Message(true, " DBuf Details , initial dbuf count is {0}", _initialDBuf.Count());
            _initialDBuf.ForEach(curDisp =>
            {
                Log.Message("{0} {1} {2}", curDisp.DisplayType, curDisp.Pipe, curDisp.DbufAllocated);
            });
        }
        private DBufInfo VerifyRegisters(string pRegisterEvent, PIPE argPipe, PORT argPort, DisplayType argDispType)
        {
            EventInfo eventInfo = new EventInfo();
            eventInfo = new EventInfo();
            eventInfo.pipe = PIPE.NONE;
            eventInfo.plane = PLANE.NONE;
            eventInfo.port = PORT.NONE;
            eventInfo.eventName = pRegisterEvent;
            EventInfo returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);

            Log.Message("the event {0} has {1} reg events ", pRegisterEvent, returnEventInfo.listRegisters.ToList().Count());

            MMIORW mmiorwObj = new MMIORW();
            mmiorwObj.FeatureName = pRegisterEvent;
            mmiorwObj.RegInfList = returnEventInfo.listRegisters;

            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                mmiorwObj.RegInfList.Remove(mmiorwObj.RegInfList.Last());
                if (argDispType == DisplayType.MIPI)
                {
                    Log.Message("in mipi");
                    eventInfo = new EventInfo() { pipe = argPipe, plane = PLANE.NONE, port = argPort, eventName = _mipi_hTotalEvent };
                    returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
                    Log.Message("count is {0}", returnEventInfo.listRegisters.Count);
                    returnEventInfo.listRegisters.ForEach(curReg =>
                    {
                        Log.Message("The HTotal register for {0} is {1}", argPipe, curReg.Offset);
                        mmiorwObj.RegInfList.Add(curReg);
                    });

                    //lane count
                    eventInfo = new EventInfo() { pipe = argPipe, plane = PLANE.NONE, port = argPort, eventName = _mipi_laneCount };
                    returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
                    Log.Message("count is {0}", returnEventInfo.listRegisters.Count);
                    returnEventInfo.listRegisters.ForEach(curReg =>
                    {
                        Log.Message("The Lane Count register for {0} is {1}", argPipe, curReg.Offset);
                        mmiorwObj.RegInfList.Add(curReg);
                    });

                    //bits per pixel
                    eventInfo = new EventInfo() { pipe = argPipe, plane = PLANE.NONE, port = argPort, eventName = _mipi_Bpp };
                    returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
                    Log.Message("count is {0}", returnEventInfo.listRegisters.Count);
                    returnEventInfo.listRegisters.ForEach(curReg =>
                    {
                        Log.Message("The bits per pixel register for {0} is {1}", argPipe, curReg.Offset);
                        mmiorwObj.RegInfList.Add(curReg);
                    });
                }
                else
                {
                    //get the HTotal depending on the pipe.
                    eventInfo = new EventInfo();
                    eventInfo = new EventInfo();
                    eventInfo.pipe = argPipe;
                    eventInfo.plane = PLANE.NONE;
                    eventInfo.port = PORT.NONE;
                    eventInfo.eventName = _hTotalEvent;
                    returnEventInfo = AccessInterface.GetFeature<EventInfo, EventInfo>(Features.EventRegisterInfo, Action.GetMethod, Source.AccessAPI, eventInfo);
                    returnEventInfo.listRegisters.ForEach(curReg =>
                    {
                        Log.Message("The HTotal register for {0} is {1}", argPipe, curReg.Offset);
                        mmiorwObj.RegInfList.Add(curReg);
                    });
                }
            }


            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            DBufInfo dbufValue = AccessInterface.GetFeature<DBufInfo, MMIORW>(Features.YTiling, Action.GetMethod, Source.AccessAPI, mmiorwObj);
            return dbufValue;
        }
        protected List<PipeDbufInfo> CheckDbuf(DisplayConfig argDispConfig)
        {
            List<PipeDbufInfo> dbufList = ReadYTilingInfo(argDispConfig);
            VerifyYTilingInfo(dbufList);
            dbufList.ForEach(curDisp =>
            {
                Log.Message("reading initial value , count is {0}", _initialDBuf.Count());
                curDisp.DbufAllocated = _initialDBuf.Where(dI => dI.DisplayType == curDisp.DisplayType).Select(dI => dI.DbufAllocated).FirstOrDefault();
                Log.Message("{0} allocated is {1}", curDisp, curDisp.DbufAllocated);

            });
            return dbufList;
        }
        protected List<PipeDbufInfo> RedistributePlane(DisplayConfig argDispConfig, List<PipeDbufInfo> argDbufList)
        {
            List<PipeDbufInfo> dbufList = ReadYTilingInfo(argDispConfig);
            dbufList.ForEach(curDisp =>
            {
                PipeDbufInfo originalDbuf = argDbufList.Where(dI => dI.DisplayType == curDisp.DisplayType).FirstOrDefault();
                if (curDisp.PlaneA.Enabled)
                    originalDbuf.PlaneA = curDisp.PlaneA;
                if (curDisp.PlaneB.Enabled)
                    originalDbuf.PlaneB = curDisp.PlaneB;
                if (curDisp.PlaneC.Enabled)
                    originalDbuf.PlaneC = curDisp.PlaneC;
            });
            return argDbufList;
        }
        protected void checkDbufRedistribution(List<PipeDbufInfo> dbufList)
        {
            List<PipeDbufInfo> dbufInfo = AccessInterface.GetFeature<List<PipeDbufInfo>, List<PipeDbufInfo>>(Features.DBuf, Action.GetAllMethod, Source.AccessAPI, dbufList);
        }
        protected void LaunchMPO()
        {
            Log.Message(true, "Launching MPO App");
            Thread.Sleep(1000);
            SendKeys.SendWait("^{Esc}"); //ctrl + esc
            Thread.Sleep(1000);
            string str = "DirectX Foreground Swap Chains";
            for (int i = 0; i < str.Count(); i++)
            {
                string subStr = str[i].ToString();
                Thread.Sleep(500);
                Log.Message("searching for {0}", subStr);
                SendKeys.SendWait(subStr);
            }
            Thread.Sleep(1000);
            SendKeys.SendWait("{ENTER}"); //ctrl + esc           
            Thread.Sleep(2000);
            Thread.Sleep(5000);
        }
        protected void LaunchOverlay(DisplayType argDispType)
        {
            base.OverlayOperations(GetDispHierarchy(argDispType), base.CurrentConfig, OverlayPlaybackOptions.MovePlayer);
        }
        protected void CloseOverlay(DisplayType argDispType)
        {
            Log.Message(true, "Closing Overlay Application");
            base.OverlayOperations(GetDispHierarchy(argDispType), base.CurrentConfig, OverlayPlaybackOptions.ClosePlayer);
        }
        private DisplayHierarchy GetDispHierarchy(DisplayType disp)
        {
            DisplayConfig currentConfig = base.CurrentConfig;
            if (disp == currentConfig.PrimaryDisplay)
                return DisplayHierarchy.Display_1;
            else if (disp == currentConfig.SecondaryDisplay)
                return DisplayHierarchy.Display_2;
            else if (disp == currentConfig.TertiaryDisplay)
                return DisplayHierarchy.Display_3;

            Log.Alert("Display Hierarchy not found for {0}", disp);
            return DisplayHierarchy.Unsupported;
        }

        protected void SemiAutomated(string argMessage)
        {
            if (!AccessInterface.SetFeature<bool, string>(Features.PromptMessage, Action.SetMethod, argMessage))
                Log.Abort("User rejected Semi Automated Request");
            Thread.Sleep(15000);
        }
        protected void UpdateMPOFeatureEnableRegistry()
        {
            Log.Message(true, "Make changes in Registry for Enabling MPO Feature Enable");
            RegistryParams registryParams = new RegistryParams();
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.ModifyInf;

            registryParams.registryKey = Registry.LocalMachine;
            registryParams.keyName = "MPOFeatureEnable";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
    }
}