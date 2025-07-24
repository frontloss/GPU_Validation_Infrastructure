namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Threading;
    using System.Diagnostics;
    using System.Xml.Serialization;

    internal class PowerEvent : FunctionalBase, ISetMethod, IParse
    {
        public bool SetMethod(object argMessage)
        {
            PowerParams powerEvent = argMessage as PowerParams;
            if (powerEvent.PowerStates == PowerStates.S5)
            {
                int rebootIdx = -1;
                if (!base.CurrentMethodIndex.Equals(-1))
                    rebootIdx = base.CurrentMethodIndex;
                CommonExtensions._rebootAnalysysInfo.rebootReason = powerEvent.rebootReason;
                CommonExtensions.DoSinchorize(rebootIdx);
                Thread.Sleep(powerEvent.Delay * 1000);
                if (CommonExtensions.HasDTMProcess())
                {
                    Log.Verbose("Initiated Environment.Exit(0) on DTM Infrastructure @ {0}", DateTime.Now);
                    CommonExtensions.ExitProcess(0);
                }

                VerifyLANStatus();
                Log.Verbose("Initiated S5 @ {0}", DateTime.Now);
                Process process = CommonExtensions.StartProcess("shutdown", string.Format("/f /r /t {0}", powerEvent.Delay));
                process.WaitForExit();
                Thread.Sleep(60000);
                return process.HasExited;
            }
            else if (powerEvent.PowerStates == PowerStates.IdleDesktop)
            {
                return IdleDesktop(powerEvent);
            }
            else
                return this.PerformSleep(powerEvent);
        }
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "PowerStates:PoweState" }, Comment = "Performs power event(S5 not supported)")]
        public void Parse(string[] args)
        {
            PowerStates powerState;
            if (args.Length > 1 && args[0].ToLower().Contains("set") && Enum.TryParse(args[1], true, out powerState))
            {
                PowerParams powerParams = new PowerParams();
                powerParams.PowerStates = powerState;
                int delay = 30;
                if (args.Length.Equals(3))
                    Int32.TryParse(args[2], out delay);
                powerParams.Delay = delay;
                if (!this.SetMethod(powerParams))
                    Log.Alert("{0} not successful!", powerState);
            }
            else
                this.HelpText();
        }

        private bool PerformSleep(PowerParams argPowerParams)
        {
            string sleepArg  = string.Empty;
            if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.ValidatePowerScheme))
            {
                TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.ValidatePowerScheme, null);
            }
            DisplayExtensions.ValidatePowerScheme();
            if (argPowerParams.PowerStates == PowerStates.S4)
            {
                if (!CheckNValidateS4())
                {
                    Log.Alert("System dose't support configuration S3/S4");
                    return false;
                }
            }

            if ((base.MachineInfo.PlatformDetails.IsLowpower) && (DisplayExtensions.VerifyCSSystem(base.MachineInfo)) &&
                ((argPowerParams.PowerStates == PowerStates.CS) || (argPowerParams.PowerStates == PowerStates.S3)))
            {
                if (CommonExtensions.VerifyWDTFStatus())
				{
					Log.Verbose("WDTF framework installed successfully");
                    Log.Message("Invoking CS -- LowPower CS Enabled System");
					argPowerParams.PowerStates = PowerStates.CS;
				}
				else
                    Log.Abort("WDTF not installed...Exiting");
                
                sleepArg = string.Format("/cs /c:1 /p:{0}", argPowerParams.Delay);
            }
            else
                sleepArg = string.Format("/sleep /s:{0} /c:1 /p:{1}", argPowerParams.PowerStates.ToString().ToLower().Split('s').Last(), argPowerParams.Delay);
            
            Log.Verbose("Initiated {0} @ {1} for {2}", argPowerParams.PowerStates, DateTime.Now, sleepArg);
            CommonExtensions.StartProcess("pwrtest.exe", sleepArg).WaitForExit();
            Log.Verbose("Resumed from {0} @ {1}", argPowerParams.PowerStates, DateTime.Now);
            if (base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower == true)
            {
                PlugUnPlugEnumeration plugUnPlugEnum = base.CreateInstance<PlugUnPlugEnumeration>(new PlugUnPlugEnumeration());
                foreach (HotPlugUnplug HT in base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo)
                {
                    plugUnPlugEnum.SetMethod(HT);
                }
            }
            return this.AssertEventEntry(argPowerParams.Delay, argPowerParams.PowerStates);
        }
        private bool CheckNValidateS4()
        {
            if (!ChecksystemConfig())
            {
                Log.Message("Enabling S4 into the test system");
                Process sysCfg = CommonExtensions.StartProcess("powercfg.exe", "/hibernate on");
                Thread.Sleep(3000);
            }
            return ChecksystemConfig();
        }
        private bool ChecksystemConfig()
        {
            Process sysCfg = CommonExtensions.StartProcess("powercfg.exe", "/a");
            while (!sysCfg.StandardOutput.EndOfStream)
            {
                string line = sysCfg.StandardOutput.ReadLine();
                if (line == "The following sleep states are not available on this system:")
                    break;
                if (line.ToLower().Contains("hibernate"))
                    return true;
            }
            return false;
        }
        private bool AssertEventEntry(int argSetDelay, PowerStates argState)
        {
            Thread.Sleep(5000);
            DateTime initTime = DateTime.Now;
            DateTime resumeTime = DateTime.Now;

            EventLog eventLog = new EventLog("System", Environment.MachineName);

            EventLogEntry logEntry = (from EventLogEntry currentEntry in eventLog.Entries
                                      where APIExtensions.InitEventIDList.Contains(currentEntry.InstanceId) && currentEntry.EntryType == EventLogEntryType.Information && APIExtensions.InitSourceList.Contains(currentEntry.Source)
                                      select currentEntry).LastOrDefault();
            if (null != logEntry)
            {
                initTime = logEntry.TimeGenerated;
                Log.Verbose("Initiated {0}. Time Generated @ {1}", argState, initTime);
                if (APIExtensions.InitDescriptionList.Contains(logEntry.Message))
                    Log.Verbose("Message {0}", argState, logEntry.Message.Split('\r').First());

                logEntry = (from EventLogEntry currentEntry in eventLog.Entries
                            where APIExtensions.ResumeEventIDList.Contains(currentEntry.InstanceId) && currentEntry.EntryType == EventLogEntryType.Information && APIExtensions.ResumeSourceList.Contains(currentEntry.Source)
                            select currentEntry).LastOrDefault();
                resumeTime = logEntry.TimeGenerated;
                Log.Verbose("Resume {0} message {1} Time Generated @ {2}", argState, logEntry.Message.Split('\r').First(), resumeTime);

                TimeSpan diffTime = resumeTime.Subtract(initTime);
                Log.Verbose("Total time taken to resume {0}secs", diffTime.TotalSeconds);

                double actualDelay = diffTime.TotalSeconds;
                if (actualDelay < argSetDelay)
                {
                    Log.Verbose("Actual resume-delay {0}secs is lesser than original requested-delay {1}secs. Adding buffer {2}secs to actual resume-delay", actualDelay, argSetDelay, APIExtensions.BufferResumeDelay);
                    actualDelay += APIExtensions.BufferResumeDelay;
                }
                return (actualDelay >= argSetDelay);
            }
            else
                Log.Fail("Could not find any power event entry in Event Viewer");
            return false;
        }
        private void VerifyLANStatus()
        {
            if (NetworkExtensions.GetLANUPStatus() == false)
            {
                NetParam netParam;
                netParam = new NetParam();
                netParam.adapter = Adapter.LAN;
                netParam.netWorkState = NetworkState.Enable;
                NetworkExtensions.SetNetworkConnection(netParam);
            }
        }

        private bool IdleDesktop(PowerParams argPowerParams)
        {
            const int WM_COMMAND = 0x111;
            const int MIN_ALL = 419;
            const int MIN_ALL_UNDO = 416;

            IntPtr LhWND = Interop.FindWindow("Shell_TrayWnd", null);
            Log.Verbose("Minimize all open active windows");
            Interop.SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL, IntPtr.Zero);

            Log.Message("Wait in idle desktop for {0} sec ", argPowerParams.Delay);
            Thread.Sleep(1000 * argPowerParams.Delay);

            Log.Verbose("Maximize all opened active windows");
            LhWND = Interop.FindWindow("Shell_TrayWnd", null);
            Interop.SendMessage(LhWND, WM_COMMAND, (IntPtr)MIN_ALL_UNDO, IntPtr.Zero);
            return true;
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Execute PowerEvent set S3|S4 30").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}