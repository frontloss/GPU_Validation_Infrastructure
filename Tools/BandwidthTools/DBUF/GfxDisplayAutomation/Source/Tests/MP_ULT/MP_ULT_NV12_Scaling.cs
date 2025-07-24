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

    public class MP_ULT_NV12_Scaling : MP_ULT_NV12_FullScreen_Basic
    {
        [Test(Type = TestType.Method, Order = 10)]
        public override void TestStep10()
        {
            Log.Message(true, "NV12 CONTENT W/O SCALING");
            base.TestStep2();
            base.TestStep3();
            base.TestStep4();
            base.TestStep5();
            base.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 11)]
        public override void TestStep11()
        {
            Log.Message(true, "Set Source Address MPO");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            uint numPlanes = planeCount;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            mpoFlipPlaneInfo[0].uiLayerIndex = 0;
            mpoFlipPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes[0];
            mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect = mpoFlipPlaneInfo[0].stPlaneAttributes.MPOSrcRect;
            mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect = mpoFlipPlaneInfo[0].stPlaneAttributes.MPOSrcRect;
            for (int j = 0; j < 3; j++)
            {
                for (int i = 0; i < fileEntries.Length; i++)
                {
                    Log.Message("{0} {1}", i, j);
                    mpoFlipPlaneInfo[0].hAllocation = pGmmBlockList[i];
                    base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                    if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                    {
                        if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                        {
                            DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, planeCount, 999);
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, 1);
                        }
                        DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, planeCount, 999);
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, 1);
                    }
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, 1);
                }
            }
        }
        [Test(Type = TestType.Method, Order = 12)]
        public override void TestStep12()
        {
            base.TestStep13();
        }
        [Test(Type = TestType.Method, Order = 13)]
        public override void TestStep13()
        {
            Log.Message(true, "Apply Lower Resolution");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            List<DisplayType> paramDispList = new List<DisplayType>() { currentOSPageConfig.PrimaryDisplay };
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);
            List<DisplayMode> SupportedModes = allMode.Where(dI => dI.display == currentOSPageConfig.PrimaryDisplay).Select(dI => dI.supportedModes).FirstOrDefault();
            DisplayMode currentMode = new DisplayMode();
            int totalmodes = SupportedModes.Count;
            currentMode = SupportedModes[totalmodes / 2];
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, currentMode))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail(false, "Fail to apply Mode");
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            Log.Message(true, "NV12 Content at Lower resolution");
            base.TestStep2();
            base.TestStep3();
            base.TestStep4();
            base.TestStep5();
            base.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message(true, "Set Source Address MPO");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            uint numPlanes = planeCount;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            mpoFlipPlaneInfo[0].uiLayerIndex = 0;
            mpoFlipPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes[0];
            mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.right = 1280;
            mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.bottom = 720;
            mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect = mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect;
            for (int j = 0; j < 3; j++)
            {
                for (int i = 0; i < fileEntries.Length; i++)
                {
                    Log.Message("{0} {1}", i, j);
                    mpoFlipPlaneInfo[0].hAllocation = pGmmBlockList[i];
                    base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                    if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                    {
                        if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                        {
                            DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, planeCount, 999);
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, 1);
                        }
                        DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, planeCount, 999);
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, 1);
                    }
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, 1);
                }
            }
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            base.TestStep13();
        }
    }
}



