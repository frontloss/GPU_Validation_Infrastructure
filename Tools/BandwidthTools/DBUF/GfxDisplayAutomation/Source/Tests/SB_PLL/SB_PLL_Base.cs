namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using Microsoft.Win32;
    class SB_PLL_Base : TestBase
    {
        protected List<string> PLLRegisterList
        {
            get
            {
                List<string> pLLRegisterList = new List<string>() { "PLL", "PLL_ENABLE_STATUS" };
                return pLLRegisterList;
            }
        }
       
        protected Dictionary<DPLL, bool> _pllInUse = null;

        public SB_PLL_Base()
        {
            _pllInUse = new Dictionary<DPLL, bool>() { { DPLL.DPLL0, false }, { DPLL.DPLL1, false }, { DPLL.DPLL2, false }, { DPLL.DPLL3, false } };
        }

        protected void ApplyConfig(DisplayConfig argDispConfig)
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, argDispConfig))
                Log.Success("{0} Applied successfully", argDispConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", argDispConfig.GetCurrentConfigStr());

            //VerifyCDClockRegisters();
            //VerifyPLLRegister(argDispConfig);            
        }
        protected void GetEdpVersion()
        {
            EventInfo returnEventInfo = GetRegisterList("EDP_VERSION");
            MMIORW mmiorwObj = new MMIORW();
            mmiorwObj.FeatureName = "EDP_VERSION";
            mmiorwObj.RegInfList = returnEventInfo.listRegisters;

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            mmiorwObj.PortList = new List<PORT>();
            //currentConfig.CustomDisplayList.ForEach(curDisp =>
            //{
            //    mmiorwObj.PortList.Add(base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.Port).FirstOrDefault());
            //});
            base.EnumeratedDisplays.ForEach(curDisp =>
            {
                mmiorwObj.PortList.Add(curDisp.Port);
            });
            mmiorwObj.currentConfig = currentConfig;
            AccessInterface.GetFeature<bool, MMIORW>(Features.PLL, Action.GetMethod, Source.AccessAPI, mmiorwObj);
        }
       
        protected void VerifyPLLRegister(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Verify PLL Register");
            foreach (string curAction in PLLRegisterList)
                VerifyRegisters(curAction);

            Dictionary<DPLL, string> sscMap = new Dictionary<DPLL, string>() { { DPLL.DPLL0, "DPLL0_SSC" }, { DPLL.DPLL1, "DPLL1_SSC" }, { DPLL.DPLL2, "DPLL2_SSC" }, { DPLL.DPLL3, "DPLL3_SSC" } };
            argDispConfig.CustomDisplayList.ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                VerifyRegisters(sscMap[curDispInfo.dpll]);
            });
            Log.Message(true, "Expected PLL:");
            ResetPLL();
            argDispConfig.CustomDisplayList.ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                DPLL curDPll = GetExpectedPLL(curDispInfo);
                Log.Message("{0} {1}", curDisp, curDPll);

                if (curDPll == curDispInfo.dpll)
                    Log.Success("{0} {1}  {2} is verified", curDispInfo.DisplayType, curDispInfo.Port, curDPll);
                else
                    Log.Fail("{0} {1} Expected DPLL: {2}   current DPLL:{3}", curDispInfo.DisplayType, curDispInfo.Port, curDPll, curDispInfo.dpll);
            });

            //Dictionary<DPLL, string> cfgcrMap = new Dictionary<DPLL, string>() { { DPLL.DPLL1, "CFGCR1" }, { DPLL.DPLL2, "CFGCR2" }, { DPLL.DPLL3, "CFGCR3" } };
            //List<DisplayInfo> hdmiCFGCRList = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.ConnectorType.connectorType == "HDMI").ToList();
            //hdmiCFGCRList.ForEach(curHDMI =>
            //{
            //    if (cfgcrMap.Keys.Contains(curHDMI.dpll))
            //        VerifyRegisters(cfgcrMap[curHDMI.dpll]);
            //});          
        }
        protected void ResetPLL()
        {
            _pllInUse = new Dictionary<DPLL, bool>() { { DPLL.DPLL0, false }, { DPLL.DPLL1, false }, { DPLL.DPLL2, false }, { DPLL.DPLL3, false } };
        }
        protected DPLL GetExpectedPLL(DisplayInfo argDisInfo)
        {
            DPLL expectedPLLType = DPLL.Invalid;
            if (base.MachineInfo.PlatformDetails.Platform == Platform.SKL)
            {
                Dictionary<ConnectorType, List<DPLL>> expectedPLLMap = new Dictionary<ConnectorType, List<DPLL>>() { { new ConnectorType() { connectorType = "DisplayPort" }, new List<DPLL>() { DPLL.DPLL1,DPLL.DPLL3,DPLL.DPLL2 } },
                                                                { new ConnectorType() { connectorType = "HDMI" }, new List<DPLL>() { DPLL.DPLL1,DPLL.DPLL3,DPLL.DPLL2 } } };
                if (argDisInfo.ConnectorType.connectorType == "Embedded DisplayPort" && argDisInfo.ssc == true)
                {
                    expectedPLLMap.Add(new ConnectorType() { connectorType = "Embedded DisplayPort" }, new List<DPLL>() { DPLL.DPLL1, DPLL.DPLL3, DPLL.DPLL2 });
                }
                else
                {
                    expectedPLLMap.Add(new ConnectorType() { connectorType = "Embedded DisplayPort" }, new List<DPLL>() { DPLL.DPLL0 });
                }

                ConnectorType curDisp = expectedPLLMap.Keys.Where(dI => dI.connectorType == argDisInfo.ConnectorType.connectorType).FirstOrDefault();
                List<DPLL> dpllList = expectedPLLMap[curDisp];
                foreach (DPLL curDPLL in dpllList)
                {
                    if (!_pllInUse[curDPLL])
                    {
                        _pllInUse[curDPLL] = true;
                        return curDPLL;
                    }
                }
            }
            else if(base.MachineInfo.PlatformDetails.Platform == Platform.CNL)
            {
                List<DPLL> cnlDpll = new List<DPLL>() { DPLL.DPLL0,DPLL.DPLL1,DPLL.DPLL2};
                if (argDisInfo.DisplayType == base.CurrentConfig.PrimaryDisplay)
                   return DPLL.DPLL0;
                if (argDisInfo.DisplayType == base.CurrentConfig.SecondaryDisplay)
                    return DPLL.DPLL1;
                if (argDisInfo.DisplayType == base.CurrentConfig.TertiaryDisplay)
                    return DPLL.DPLL2;
            }

            return expectedPLLType;
        }
        protected void VerifyRegisters(string pRegisterEvent)
        {
            EventInfo returnEventInfo = GetRegisterList(pRegisterEvent);
            MMIORW mmiorwObj = new MMIORW();
            mmiorwObj.FeatureName = pRegisterEvent;
            mmiorwObj.RegInfList = returnEventInfo.listRegisters;

            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            mmiorwObj.PortList = new List<PORT>();
            //currentConfig.CustomDisplayList.ForEach(curDisp =>
            //{
            //    mmiorwObj.PortList.Add(base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.Port).FirstOrDefault());
            //});
            base.EnumeratedDisplays.ForEach(curDisp =>
                {
                    mmiorwObj.PortList.Add(curDisp.Port);
                });
            mmiorwObj.currentConfig = currentConfig;
            AccessInterface.GetFeature<bool, MMIORW>(Features.PLL, Action.GetMethod, Source.AccessAPI, mmiorwObj);
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
        protected bool CompareRegisters(uint argDriverData, RegisterInf argRegInfo)
        {
            uint bit = Convert.ToUInt32(argRegInfo.Bitmap, 16);
            Log.Verbose("Bitmap in uint = {0}, Value from register read = {1}", bit, argDriverData);
            uint hex = Convert.ToUInt32(String.Format("{0:X}", argDriverData), 16);
            Log.Verbose("value from reg read in ubit = {0}", hex);
            string valu = String.Format("{0:X}", hex & bit);
            Log.Verbose("after bitmap = {0}", valu);
            if (String.Equals(valu, argRegInfo.Value))
            {
                Log.Success("Register Values Matched");
                return true;
            }
            return false;
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
        protected void VerifyConfig(DisplayConfig argDispConfig)
        {
            Log.Message(true, "Verifying config {0} via OS", argDispConfig.GetCurrentConfigStr());
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(argDispConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is verified by OS", argDispConfig.GetCurrentConfigStr());
            }
            else
                Log.Fail("Config {0} does not match with current config {1}", currentConfig.GetCurrentConfigStr(), argDispConfig.GetCurrentConfigStr());
        }
        protected void PowerEvent(PowerStates argPowerState)
        {
            Log.Message(true, "Invoking Power event {0}", argPowerState);
            PowerParams powerParam = new PowerParams()
            {
                Delay = 30,
                PowerStates = argPowerState
            };
            base.InvokePowerEvent(powerParam, argPowerState);
        }
    }
}



