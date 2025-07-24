namespace Intel.VPG.Display.Automation
{
    using System.Windows.Forms;
    using System.Collections.Generic;
    using System.Threading;
    using System.Linq;
    using System.Text;
    using System;
    using System.IO;
    using System.Security.AccessControl;

    class MP_SwitchableGraphics_HDCP_LFP_CRT_HDMI_DP_ModeChange : MP_SwitchableGraphics_Base
    {
        private Dictionary<DisplayType, string> _myDictionary = null;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Remove any instances of OPM tester in binary");
            string[] directories = Directory.GetDirectories(Directory.GetCurrentDirectory(), "OPM*");
            foreach (string dir in directories)
            {
                string[] files = Directory.GetFiles(dir);
                foreach (string g in files)
                {
                    File.SetAttributes(g, FileAttributes.Normal);
                    Thread.Sleep(1000);
                    File.Delete(g);
                }
                Directory.Delete(dir);
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Connect all the displays planned in the grid.");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
            this._myDictionary = new Dictionary<DisplayType, string>()
            {
                 { DisplayType.EDP,"SetProtectionHDCP Failed to set HDCP" },
                 { DisplayType.CRT,"SetProtectionHDCP Failed to set HDCP" },
                 { DisplayType.HDMI,"SetProtection HDCP succeeded" },
                 { DisplayType.DP,"SetProtection HDCP succeeded" },
                 { DisplayType.WIDI, "SetProtection HDCP succeeded" }
            };
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Run OPM tester and activate HDCP on each display");
            foreach (DisplayType dT in base.CurrentConfig.CustomDisplayList)
            {
                DisplayHierarchy dH = base.GetDispHierarchy(base.CurrentConfig.CustomDisplayList, dT);
                Log.Message(true, "Run OPM Tester and choose Activate HDCP from menu");
                HDCPParams hdcpParams = new HDCPParams()
                {
                    HDCPPlayerInstance = HDCPPlayerInstance.Player_1,
                    HDCPOptions = HDCPOptions.ActivateHDCP,
                    HDCPApplication = HDCPApplication.OPMTester,
                    DisplayHierarchy = dH,
                    CurrentConfig = base.CurrentConfig
                };
                AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
                base.VerifyProtectionHDCP(dT, "ON", 1, _myDictionary);
                hdcpParams.HDCPOptions = HDCPOptions.Close;
                AccessInterface.SetFeature<HDCPParams>(Features.HDCP, Action.Set, hdcpParams);
                if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                    break;
            }
        }
    }
}