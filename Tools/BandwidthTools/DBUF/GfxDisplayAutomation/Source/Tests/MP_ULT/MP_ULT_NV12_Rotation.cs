namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    using System.IO;
    using System.Xml.Linq;
    using System.Xml.Serialization;
    using System.Xml;
    using System.Threading;
    using System.Runtime.InteropServices;

    public class MP_ULT_NV12_Rotation : MP_ULT_NV12_FullScreen_Basic
    {
        public MP_ULT_NV12_Rotation()
        {
            base._performAction = this.PerformAction;
        }
        [Test(Type = TestType.Method, Order = 10)]
        public override void TestStep10()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MPO Flips with NV12 content on rotated display");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
        }
        [Test(Type = TestType.Method, Order = 11)]
        public override void TestStep11()
        {
            Log.Message(true, "Rotate primary display by 90 degree");
            base.RotateDisplay(90);
        }
        [Test(Type = TestType.Method, Order = 12)]
        public override void TestStep12()
        {
            base.TestStep3();
            base.TestStep4();
            base.TestStep5();
            base.TestStep6();
            base.TestStep7();
        }
        [Test(Type = TestType.Method, Order = 13)]
        public override void TestStep13()
        {
            base.TestStep8();
            base.TestStep9();
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            this.TestStep10();
            Log.Message(true, "Rotate primary display by 180 degree");
            base.RotateDisplay(180);
            this.TestStep12();
            this.TestStep13();
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            this.TestStep10();
            Log.Message(true, "Rotate primary display by 270 degree");
            base.RotateDisplay(270);
            this.TestStep12();
            this.TestStep13();
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            Log.Message("Return system to default config");
            Log.Message(true, "Set config to SD/ED");
            if (base.CurrentConfig.CustomDisplayList.Count < 2)
                base.CurrentConfig.ConfigType = DisplayConfigType.SD;
            else
                base.CurrentConfig.ConfigType = DisplayConfigType.ED;
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config applied successfully");
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config not applied!");
            }
        }
        private void PerformAction()
        {
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            base.VerifyRotation(currentOSPageConfig.PrimaryDisplay, actualMode.Angle);
        }
    }
}



