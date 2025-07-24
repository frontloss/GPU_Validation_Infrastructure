namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_S0ix_S4 : MP_WIDIBase
    {
        private NetParam netParam;
        private CSParam powerParam;
        private bool DisableLANStatus = false;

        [Test(Type = TestType.PreCondition, Order = 1)]
        public void ConnectedStandbyPrerequest()
        {
            netParam = new NetParam();
            powerParam = new CSParam();

            List<string> fileInfos = new List<string>();
            List<string> searchPattern = new List<string> { "*.html", "*.xml", "*.jpg" };
            foreach (string eachSearchString in searchPattern)
            {
                fileInfos.AddRange(Directory.EnumerateFiles(Directory.GetCurrentDirectory(), eachSearchString).ToList());
            }
            foreach (string file in fileInfos)
                File.Delete(file);
            Log.Message(true, "Checking CS test pre condition");
            netParam.adapter = Adapter.LAN;
            netParam.netWorkState = NetworkState.Disable;
            if (AccessInterface.SetFeature<bool, NetParam>(Features.NetworkConnection, Action.SetMethod, netParam))
                DisableLANStatus = true;
            Log.Verbose("Checking WLAN is enabled or not");
            if (!AccessInterface.GetFeature<bool>(Features.NetworkConnection, Action.Get))
                Log.Alert("WLAN is not enabled!!!");

            Log.Verbose("checking connected standby system using powercfg.exe /a");
            Process pwrCfgProcess = new Process();
            pwrCfgProcess = CommonExtensions.StartProcess("powercfg.exe", " /a");
            bool testSetup = false;
            while (!pwrCfgProcess.StandardOutput.EndOfStream)
            {
                string line = pwrCfgProcess.StandardOutput.ReadLine();
                if (line == "The following sleep states are not available on this system:")
                    break;
                if (line.Trim().ToLower().Contains("standby (connected)"))
                {
                    Log.Verbose("Connected Standby Setup Ready for execution");
                    testSetup = true;
                }
            }
            if (!testSetup)
            {
                this.CleanUP();
                Log.Abort("Connected Standby Setup is not ready for execution");
            }
            pwrCfgProcess.Close();
            AccessInterface.SetFeature(Features.ConnectedStandby, Action.Set, "");
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void SetConfigMethod()
        {
            base.SetNValidateConfig(base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void SendSysytemToS0ix()
        {
            Log.Message(true, "Going S0ix state and Resume the system from S0i3 after {0} seconds", powerParam.Delay);
            this.RunCPUStateAnalyzer();
            AccessInterface.SetFeature<bool, CSParam>(Features.ConnectedStandby, Action.SetMethod, powerParam);
            this.GetCPUC10State();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void VerifySystemState()
        {
            if (!base.IsWiDiConnected())
            {
                Log.Message("Try to reconnect WiDi display");
                CleanUP();
                if (!WiDiReConnect())
                    CheckWiDiStatus();
            }
            else
            {
                Log.Message("WiDi display is connected after resume from S0ix");
                CleanUP();
            }
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void SendSystemToS4()
        {
            PowerStates powerState = PowerStates.S4;
            Log.Message(true, "4. Put the system into {0} state & resume", powerState);
            PowerParams powerParams = new PowerParams() { Delay = 30 };
            base.EventResult(powerState, base.InvokePowerEvent(powerParams, powerState));
            VerifySystemState();
        }

        private void CleanUP()
        {
            if (DisableLANStatus)
            {
                Log.Message(true, "Test cleanup");
                Log.Message("Enabling LAN connection again...");
                netParam.adapter = Adapter.LAN;
                netParam.netWorkState = NetworkState.Enable;
                if (!AccessInterface.SetFeature<bool, NetParam>(Features.NetworkConnection, Action.SetMethod, netParam))
                    Log.Abort("Unable to enable LAN connectuion");
            }
        }

        private void RunCPUStateAnalyzer()
        {
            AccessInterface.SetFeature<bool, int>(Features.CPUState, Action.SetMethod, powerParam.Delay);
        }

        private void GetCPUC10State()
        {
            if (AccessInterface.GetFeature<bool>(Features.CPUState, Action.Get))
                Log.Success("S0ix% residency value as expected");
            else
                Log.Fail("S0ix% residency value dosent expected");
        }
    }
}
