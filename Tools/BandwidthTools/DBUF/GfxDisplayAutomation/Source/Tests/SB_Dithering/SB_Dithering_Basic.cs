using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dithering_Basic : SB_Dithering_Base
    {
        DisplayConfig edConfig = new DisplayConfig();
        DisplayConfig ddcConfig = new DisplayConfig();
        [Test(Type = TestType.Method, Order = 0)]
        public void TestPreCondition()
        {
            base.InstallDirectX();
            base.EnumeratedDisplays.ForEach(curDisp =>
            {
                Log.Message("{0}: {1}",curDisp.DisplayType , curDisp.ColorInfo.MaxDeepColorValue);
            });
        }
        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            DisplayConfig sdConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfigOS(sdConfig);
            Enable10BitScanner();
            base.CheckDithering(base.CurrentConfig.PrimaryDisplay, DeepColorAppType.N10BitScanOut);
            base.Disable10BitScanner();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            Enable10BitScanner(8);
            base.CheckDithering(base.CurrentConfig.PrimaryDisplay, DeepColorAppType.None);
            base.Disable10BitScanner();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order=3)]
        public virtual void TestStep3()
        {
            ddcConfig = new DisplayConfig() {ConfigType=DisplayConfigType.DDC , PrimaryDisplay=base.CurrentConfig.PrimaryDisplay , SecondaryDisplay=base.CurrentConfig.SecondaryDisplay};
            base.ApplyConfigOS(ddcConfig);
            Enable10BitScanner(8);
            ddcConfig.CustomDisplayList.ForEach(curDisp =>
                {
                    base.CheckDithering(curDisp, DeepColorAppType.None);
                });
            base.Disable10BitScanner();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            EnableFP16();
           ddcConfig.CustomDisplayList.ForEach(curDisp =>
            {
                base.CheckDithering(curDisp, DeepColorAppType.FP16);
            });
            base.DisableFP16();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
             edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
            base.ApplyConfigOS(edConfig);
            base.Enable10BitScanner();
            edConfig.CustomDisplayList.ForEach(curDisp =>
            {
                base.CheckDithering(curDisp, DeepColorAppType.N10BitScanOut);
            });
            base.Disable10BitScanner();
            base.CloseApp();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public virtual void TestStep6()
        {
            if (base.CurrentConfig.DisplayList.Count() == 3)
            {
                DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay , TertiaryDisplay=base.CurrentConfig.TertiaryDisplay };
                base.ApplyConfigOS(tdcConfig);
                base.Enable10BitScanner();
                base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    base.CheckDithering(curDisp, DeepColorAppType.N10BitScanOut);
                });
                base.Disable10BitScanner();
                base.CloseApp();
            }
        }
        [Test(Type = TestType.Method, Order = 7)]
        public virtual void TestStep7()
        {
            if (base.CurrentConfig.DisplayList.Count() == 3)
            {
                base.EnableFP16();
                base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    base.CheckDithering(curDisp, DeepColorAppType.FP16);
                });
                base.DisableFP16();
                base.CloseApp();
            }
        }
    }
}
