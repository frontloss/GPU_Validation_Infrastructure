namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Linq;
    using System.IO;
    using System.Threading;
    using System.Windows.Forms;
    using System.Xml;
    using System.Text.RegularExpressions;

    public class MP_S0ixBase : TestBase
    {
        private NetParam netParam;
        protected CSParam powerParam;
        internal bool Verify_C8_Plus;
        protected bool nonCS_PackageC8PlushState;
        protected bool IsResumeTimeTest = false;
        private CSVerificationTool VerificationTool;
        public NonCSPowerOption NonCSInputOption;
        private string SocWatchCmd;
        internal MonitorTurnOffParam monitorOnOffParam;
        internal PowerParams powerParams;

        public MP_S0ixBase()
        {
            netParam = new NetParam();
            powerParam = new CSParam();
            nonCS_PackageC8PlushState = false;
            SocWatchCmd = string.Empty;
            NonCSInputOption = NonCSPowerOption.MonitorOff;
        }

        #region PreCondition
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void ConnectedStandbyPrerequest()
        {
            int cmdDelay;
            GetTestAttributes();
            Log.Message(true, "Verify CS/Non CS Pre Request");
            DisplayConfig displayConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.GetInternalDisplay() };
            Log.Message("Set the initial configuration as SD {0}", displayConfig.PrimaryDisplay);
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
                Log.Message("Config (SD {0}) applied successfully", displayConfig.PrimaryDisplay);
            else
            {
                Log.Abort("Config (SD {0}) not applied!", displayConfig.PrimaryDisplay);
            }
            if (!nonCS_PackageC8PlushState)
                VerifyCSSystem();
            if (IsResumeTimeTest)
                return;
            if (VerificationTool == CSVerificationTool.BLATool)
                VerifyBLATool();
            else if (VerificationTool == CSVerificationTool.SocWatch)
            {
                powerParam.Command = SocWatchCmd;
                cmdDelay = GetTimeDelay(SocWatchCmd);
                powerParam.Delay = (cmdDelay != 0) ? cmdDelay : powerParam.Delay;
            }
        }
        #endregion

        private void GetTestAttributes()
        {
            //<Data>
                //<ConnectedStandby>
                //<Platform id ="BDW" VerificationType="BLATool"></Platform>
                //<Platform id ="BXT" VerificationType="SocWatch"></Platform>
                //</ConnectedStandby>
            //</Data>

            if (string.IsNullOrEmpty(base.MachineInfo.PlatformDetails.Platform.ToString()))
            {
                Log.Abort("Unable to find Platform information");
            }
            ProfileInfo data = new ProfileInfo();
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\S0ixdata.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/ConnectedStandby");
            foreach (XmlNode eventNode in eventBenchmarkRoot.ChildNodes)
            {
                if (eventNode.Attributes["id"].Value.Trim() == base.MachineInfo.PlatformDetails.Platform.ToString())
                {
                    string tool = eventNode.Attributes["VerificationType"].Value.Trim();
                    VerificationTool = (CSVerificationTool)Enum.Parse(typeof(CSVerificationTool), tool);
                    break;
                }
            }

            //Get the command to run SocWatch Tool.
            if (VerificationTool == CSVerificationTool.SocWatch)
            {
                eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data/SocWatch/CS");
                foreach (XmlNode eventNode in eventBenchmarkRoot.ChildNodes)
                {
                    if (eventNode.Attributes["id"].Value.Trim() == base.MachineInfo.PlatformDetails.Platform.ToString() &&
                        base.MachineInfo.PlatformDetails.FormFactor == FormFactor.Unknown)
                    {
                        SocWatchCmd = eventNode.Attributes["cmd"].Value.Trim();
                        break;
                    }
                    else if (eventNode.Attributes["id"].Value.Trim() != base.MachineInfo.PlatformDetails.Platform.ToString() &&
                            eventNode.Attributes["id"].Value.Trim() == base.MachineInfo.PlatformDetails.FormFactor.ToString())
                    {
                        SocWatchCmd = eventNode.Attributes["cmd"].Value.Trim();
                        break;
                    }
                }
            }
            if (VerificationTool == CSVerificationTool.Undefined)
            {
                Log.Abort("CS Verification tool Undefined");
            }
        }

        private void VerifyCSSystem()
        {
            ACDCSwitch(PowerLineStatus.Offline);
            if (!DisplayExtensions.VerifyCSSystem(base.MachineInfo))
            {
                Log.Abort("Connected Standby Setup is not ready for execution");
            }
            AccessInterface.SetFeature(Features.ConnectedStandby, Action.Set, "");
            Thread.Sleep(5000);
        }

        private void ACDCSwitch(PowerLineStatus powerSource)
        {
            string powerOption = powerSource == PowerLineStatus.Online ? "AC" : "DC";
            if (AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get, Source.AccessAPI) != powerSource)
            {
                if (!AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Abort("Switch to {0} power option failed", powerOption);
                else
                    Log.Message("System is in {0} power mode", powerOption);
            }
            else
                Log.Message("System is in {0} power mode", powerOption);
        }

        protected void CSCall()
        {
            if (nonCS_PackageC8PlushState)
                NonCSPackageC8Plush();
            else
                S0ixCall();
        }

        private void NonCSPackageC8Plush()
        {
            this.RunCPUStateAnalyzer();

            switch (NonCSInputOption)
            {
                case NonCSPowerOption.MonitorOff:
                Log.Message("TurnOFF state and Resume the system from Monitor TurnOFF after {0} seconds", powerParam.Delay);
                AccessInterface.SetFeature<bool, MonitorTurnOffParam>(Features.MonitorTurnOff, Action.SetMethod, monitorOnOffParam);
                break;

                case NonCSPowerOption.Sleep:
                case NonCSPowerOption.Idle:
                Log.Message("Put the system into {1} state & resume after {1} sec", powerParams.PowerStates, powerParams.Delay);
                AccessInterface.SetFeature<bool, PowerParams>(Features.PowerEvent, Action.SetMethod, powerParams);
                break;

                default:
                Log.Fail("Non CS invalid power option specified");
                break;
            }

            DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            Log.Verbose("Current display config is {0} ", osConfig.GetCurrentConfigStr());

            //CPU C8 should be non-Zer and CPU C9, C10 can zero, basically we are checking C8+
            CPUStateParam CPUState = new CPUStateParam();
            #region Check CPU C8 State
            CPUState.ValidCPUState.Add(CPU_C_STATE.C8);
            CPUState.ValidCPUState.Add(CPU_C_STATE.C9);
            CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
            CPUState.CheckState = true;
            GetCPUState(CPUState);
            #endregion
        }

        private void S0ixCall()
        {
            Log.Message(true, "Going S0ix state and Resume the system from S0i3 after {0} seconds", powerParam.Delay);
            this.RunCPUStateAnalyzer();
            AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, powerParam);
            DisplayConfig osConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            Log.Verbose("display config {0} and display list count is {1} custom display list count {2}", osConfig.ConfigType, osConfig.DisplayList.Count, osConfig.CustomDisplayList.Count);
            Log.Verbose("Current display config is {0} ", osConfig.GetCurrentConfigStr());
            GetCPUState(GetCSValid_CPUState());
        }

        private CPUStateParam GetCSValid_CPUState()
        {
            CPUStateParam CPUState = new CPUStateParam();
            switch (base.ApplicationManager.MachineInfo.PlatformDetails.Platform)
            {
                #region HSW BDW
                case Platform.BDW:
                case Platform.HSW:
                    DisplayConfig OS_Config = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
                    // if corrent display config is single internal display C10 should hit 
                    if (OS_Config.ConfigType == DisplayConfigType.SD && OS_Config.PrimaryDisplay == base.GetInternalDisplay())
                    {
                        if (Verify_C8_Plus)
                        {
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C8);
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C9);
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                            CPUState.CheckState = false;
                        }
                        else
                        {
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                            CPUState.CheckState = true;
                        }
                    }
                    else
                    {
                        bool audioflag = false;
                        List<DisplayType> secDisp = OS_Config.CustomDisplayList;
                        OS_Config.CustomDisplayList.Remove(base.GetInternalDisplay());
                        //if any external audio capable display is connected, we should check CPU C8,C9,C10 zero.
                        //if all non audio capable display is connected we should check for CPU C10 non Zero.
                        foreach (DisplayType disp in secDisp)
                        {
                            if (base.CurrentConfig.EnumeratedDisplays.Where(DT => DT.DisplayType == disp).First().isAudioCapable)
                                audioflag = true;
                        }
                        if (audioflag == true)
                        {
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C8);
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C9);
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                            CPUState.CheckState = false;
                        }
                        else
                        {
                            CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                            CPUState.CheckState = true;
                        }
                    }
                    break;
                #endregion

                #region SKL KBL
                case Platform.SKL:
                case Platform.KBL:
                    CPUState.ValidCPUState.Add(CPU_C_STATE.C9);
                    CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                    CPUState.CheckState = true;
                    break;
                #endregion

                default:
                    CPUState.ValidCPUState.Add(CPU_C_STATE.C10);
                    CPUState.CheckState = true;
                    break;
            }
            return CPUState;
        }

        private void VerifyBLATool()
        {
            if (ValidateCPU_C7State() == false)
                return;
            bool checkCPU_C7State = false;
            DateTime start = DateTime.Now;
            Log.Message("Checking CPU C7 state using BLA tool");
            Log.Verbose("Wait for 5 minute to check C7 non zero value");
            while (true)
            {
                Thread.Sleep(5000);
                DateTime startTime = start;
                DateTime endtime = DateTime.Now;
                TimeSpan diff = endtime.Subtract(startTime);
                if (diff.Days <= 0 && diff.Minutes >= 5)
                    break;
                this.RunCPUStateAnalyzer();
                powerParam.cState = CPU_C_STATE.C7;
                if (!AccessInterface.GetFeature<bool, CSParam>(Features.CPUState, Action.GetMethod, Source.AccessAPI, powerParam))
                {
                    Log.Verbose("CPU C7 State is not as expected checking again....");
                }
                else
                {
                    Log.Message("CPU C7 state as expected");
                    checkCPU_C7State = true;
                    break;
                }
            }
            if (!checkCPU_C7State)
            {
                Log.Abort("CPU dosent hit C7 state. exiting from test execution");
            }
        }

        private bool ValidateCPU_C7State()
        {
            switch (base.ApplicationManager.MachineInfo.PlatformDetails.Platform)
            {
                case Platform.BDW:
                case Platform.HSW:
                    return true;

                default:
                    return false;
            }
        }

        protected void RunCPUStateAnalyzer()
        {
            powerParam.VerificationTool = VerificationTool;
            AccessInterface.SetFeature<bool, CSParam>(Features.CPUState, Action.SetMethod, powerParam);
        }

        private bool GetCPUState(CPUStateParam CPUState)
        {
            if (CPUState == null || CPUState.ValidCPUState.Count == 0)
            {
                Log.Message("No Valid CPU State Information defined.");
                return false;
            }

            Dictionary<CPU_C_STATE, bool> CurrentCPUState = new Dictionary<CPU_C_STATE, bool>();
            string CPUStateString = string.Join(", ", CPUState.ValidCPUState.ToArray());

            string text = CPUState.CheckState ? "Non-Zero" : "Zero";
            Log.Message("Checking CPU {0} state, should be {1}.", CPUStateString, text);
            for (int eachState = 0; eachState < CPUState.ValidCPUState.Count; eachState++)
            {
                powerParam.cState = CPUState.ValidCPUState[eachState];
                if (AccessInterface.GetFeature<bool, CSParam>(Features.CPUState, Action.GetMethod, Source.AccessAPI, powerParam))
                    CurrentCPUState.Add(CPUState.ValidCPUState[eachState], true);
                else
                    CurrentCPUState.Add(CPUState.ValidCPUState[eachState], false);
            }

            if (CurrentCPUState.Values.Any(value => value.Equals(CPUState.CheckState)))
            {
                Log.Success("CPU state are as expected");
                return true;
            }
            else
                Log.Fail("CPU state are not as expected");
            return false;
        }

        protected bool GetListEnumeratedDisplays()
        {
            List<uint> winMonitorIdList = base.ListEnumeratedDisplays();
            List<uint> enumeratedWinMonIDList = base.CurrentConfig.EnumeratedDisplays.Where(dI => !dI.WindowsMonitorID.Equals(0)).Select(dI => dI.WindowsMonitorID).ToList();
            return enumeratedWinMonIDList.Count.Equals(winMonitorIdList.Count);
        }

        protected void PrintEnumeratedDisplay(List<DisplayInfo> enumeratedDisplays)
        {
            Log.Verbose("************** List Of Enumerated Display supported by System ***************");
            foreach (DisplayInfo eachEnumDisplay in enumeratedDisplays)
            {
                Log.Verbose("Enumerated {0}: {1} - Windows monitor ID: {2}, CUI SDK ID {3}", eachEnumDisplay.DisplayType, eachEnumDisplay.CompleteDisplayName, eachEnumDisplay.WindowsMonitorID, eachEnumDisplay.CUIMonitorID);
                Log.Verbose("Port information for display {0}: System port is {1} and DVMU port is {2}", eachEnumDisplay.DisplayType, eachEnumDisplay.Port, eachEnumDisplay.DvmuPort);
                Log.Verbose("Optmal Resolution is {0}x{1}x{2}{3}Hz", eachEnumDisplay.DisplayMode.HzRes, eachEnumDisplay.DisplayMode.VtRes, eachEnumDisplay.DisplayMode.RR, eachEnumDisplay.DisplayMode.InterlacedFlag.Equals(0) ? "p" : "i");
                Log.Verbose("Color support: XvYcc {0}, YcBcr {1}", eachEnumDisplay.ColorInfo.IsXvYcc, eachEnumDisplay.ColorInfo.IsYcBcr);
                Log.Verbose("------------------------------------------------------------------------------");
                Log.Verbose("");
            }
            Log.Verbose("*************** List Of Enumerated Display End ***************");
        }

        /// <summary>
        /// Get the Delay from the SocWatch command
        /// </summary>
        /// <param name="SocWatchCmd">SocWatch command</param>
        /// <returns>Delay time</returns>
        private static int GetTimeDelay(string SocWatchCmd)
        {
            int delay = 0;
            string pat = @"-t\s*(\d+)";
            Regex regSearchOption = new Regex(pat, RegexOptions.IgnoreCase);
            Match match = regSearchOption.Match(SocWatchCmd);
            for (int i = 1; i <= match.Groups.Count; i++)
            {
                Group group = match.Groups[i];
                if (!string.IsNullOrEmpty(group.Value))
                {
                    delay = Convert.ToInt16(group.Value);
                    return delay;
                }
            }
            return delay;
        }
    }
}
