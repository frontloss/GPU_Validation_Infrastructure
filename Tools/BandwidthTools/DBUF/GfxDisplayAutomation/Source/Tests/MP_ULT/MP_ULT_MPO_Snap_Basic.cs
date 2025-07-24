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

    public class MP_ULT_MPO_Snap_Basic : MP_ULT_MPO_YTiling_Snap_Basic
    {
        protected new List<UInt64> pGmmBlockList;
        private const int planeCount = 2;

        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MMIO Flips with non NV12 content");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
        }

        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateMMIOResource();
        }
        [Test(Type = TestType.Method, Order = 12)]
        public void TestStep12()
        {
            Log.Message(true, "MMIO Flips with Y-tile");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync;
            for (int i = 0; i < 3; i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmBlockList[i % 3], 0, 8, sourceAddressFlags);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, 0);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, 0);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, 0);
            }
        }
        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
        {
            Log.Message(true, "Exit ULT Mode");
            foreach (UInt64 pgmm in pGmmBlockList)
                base.ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
            pUserVirtualAddressList.Clear();
            base.EnableULT(false);
        }
    }
}



