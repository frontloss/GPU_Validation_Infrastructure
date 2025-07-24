namespace Intel.VPG.Display.Automation
{
    using System;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Collections.Generic;
    using System.Windows.Forms;

    [Test(Type = TestType.HasReboot)]
    class MP_SmartFrame_Media : MP_SmartFrame_Base
    {

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestPreCondition()
        {
            Log.Message(true, "Set config SD {0} via OS", base.GetInternalDisplay());
            DisplayConfig config = new DisplayConfig();
            config.ConfigType = DisplayConfigType.SD;
            config.PrimaryDisplay = base.GetInternalDisplay();
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, config))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Enable Smart Frame");
            base.EnableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.EnableSF();
            base.VerifySmartFrameStatus(true, SmartFrameRegistryEvent);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Play XBOX Clip");
            string[] files = Directory.GetFiles(base.ApplicationManager.ApplicationSettings.MPOClipPath);
            string fileName = Path.GetFileName(files[0]);
            CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.MPOClipPath);
            SendKeys.SendWait("{F11}");
            Thread.Sleep(10000);
            AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
            Thread.Sleep(10000);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Verify media is playing using register values");
            base.VerifySmartFrameStatus(true, SmartFrameMediaEvent);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Disable Smart Frame");
            base.DisableSF();
            base.DisableRegistryForSF();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            base.VerifySmartFrameStatus(false, SmartFrameRegistryEvent);
        }
    }
}