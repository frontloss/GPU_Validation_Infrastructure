namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;
    using System.IO;
    using System.Diagnostics;
    using System.Drawing;
    using Microsoft.Win32;
    using System.Collections.Generic;

    [Test(Type = TestType.HasReboot)]
    class MP_48Hz_Basic : MP_48Hz_Base
    {
        private PowerParams _powerParams = null;
        private DisplayType _displayType = DisplayType.None;
        protected string currentRR = string.Empty;
        private RegistryParams registryParams = new RegistryParams();
        private Point point = new Point();
       
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {          
            Log.Message(true,"Verify EDP is connected ");
            this._displayType = base.CurrentConfig.DisplayList.FirstOrDefault(dT => (dT == DisplayType.EDP));
            if (this._displayType != DisplayType.None)
                Log.Success("{0} is connected..test continues", this._displayType);
            else
                Log.Abort("EDP is not connected..Aborting the test"); 
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set SD EDP via OS call");
            DisplayConfig currentConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.SD,
                PrimaryDisplay = DisplayType.EDP
            };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, currentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Fail("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Verify EDP Capabilities");
            List<DisplayType> paramDispList = new List<DisplayType>() { DisplayType.EDP };
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);
            bool edpCapabilityFlag = false;
            foreach (DisplayMode mode in allMode[0].supportedModes)
            {
                if ((mode.HzRes == 1920) && (mode.VtRes == 1080))
                {
                    edpCapabilityFlag = true;
                    Log.Message("Set {0}x{1} on EDP", mode.HzRes, mode.VtRes);
                    if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, mode))
                        Log.Success("Mode applied Successfully");
                    else
                        Log.Fail("Fail to apply Mode");
                }
            }
            if(edpCapabilityFlag == false)
                    Log.Abort("EDP Panel doesnot support 48Hz..Aborting the test");
            
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Disable help pop ups occuring in metro mode and Restart the machine");
            Log.Message("Add key to registry");
            registryParams.keyName = "DisableHelpSticker";
            registryParams.value = 1;
            registryParams.registryKey = Registry.CurrentUser;
            registryParams.path = "Software\\Policies\\Microsoft\\Windows\\EdgeUI";
            AccessInterface.SetFeature<bool, RegistryParams>(Features.AddToRegistry, Action.SetMethod, registryParams);
            registryParams.registryKey = Registry.LocalMachine;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.AddToRegistry, Action.SetMethod, registryParams);
            Log.Message("Restart Machine");
            this._powerParams = new PowerParams();
            this._powerParams.Delay = 5;
            base.InvokePowerEvent(this._powerParams, PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Get current refresh rate from OS and verify with CUI");
            currentRR = base.GetCurrentRRFromCUIandOS();
            if (currentRR.Equals(string.Empty))
                Log.Abort("OS and CUI reporting different RR");
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Play 24 fps MPO Clip");
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.MPOClipPath))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.MPOClipPath);
            }
            CommonExtensions.KillProcess("explorer");

            string[] files = Directory.GetFiles(base.ApplicationManager.ApplicationSettings.MPOClipPath);
            string fileName;
            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
            {
                fileName = Path.GetFileNameWithoutExtension(files[0]);
            }
            else
                fileName = Path.GetFileName(files[0]);

            CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.MPOClipPath);
            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
                SendKeys.SendWait("{F11}");
            Thread.Sleep(3000);

            AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
            Thread.Sleep(15000); // 48Hz will kick-in after 15-20sec of video playback. Known OS erratas
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Check for change in RR while clip is playing");
            bool status = AccessInterface.GetFeature<bool, string>(Features.MDRRS_48Hz, Action.GetMethod, Source.AccessAPI, currentRR);
            if (status)
                Log.Success("Refresh rate switched");
            else
                Log.Fail("Refresh rate didnt Switch");
            ClosePlayerNExplorer();
        }
        protected void ClosePlayerNExplorer()
        {
            SendKeys.SendWait("%{F4}");
            Thread.Sleep(1000);
            Process[] explorerProcess = Process.GetProcessesByName("explorer");
            if (explorerProcess.Length > 0)
            {
                foreach (Process p in explorerProcess)
                {
                    p.Close();
                }
            }
        }
    }
}
