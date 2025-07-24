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

    public class MP_ULT_NV12_FullScreen_Basic : MP_ULT_Base
    {
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        uint sourceId = 0;
        protected XElement planeAttributes;
        protected ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[planeCount];
        protected SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
        protected ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];
        string dumpFilepath = string.Empty;
        protected List<UInt64> pGmmBlockList;
        protected List<IntPtr> pUserVirtualAddressList;
        protected const int planeCount = 1;
        protected System.Action _performAction = null;

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            ultParserDoc = XDocument.Load(_paramsDictionary["NV12"]);
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.ULT_FW_Get_MPO_Caps(sourceId, ref stMpoCaps);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            ULT_MPO_GROUP_CAPS[] stMpoGroupCaps = new ULT_MPO_GROUP_CAPS[stMpoCaps.uiNumCapabilityGroups];
            for (uint i = 0; i < stMpoCaps.uiNumCapabilityGroups; i++)
            {
                base.ULT_FW_MPO_Group_Caps(sourceId, i, ref stMpoGroupCaps[i]);
            }
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Check MPO");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            for (int i = 0; i < planeCount; i++)
            {
                stMPOPlaneAttributes[i] = new ULT_MPO_PLANE_ATTRIBUTES();
                stCheckMpoSupportPlaneInfo[i].uiLayerIndex = Convert.ToUInt32(i); ;
                stCheckMpoSupportPlaneInfo[i].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                stCheckMpoSupportPlaneInfo[i].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);
                ULT_PIXELFORMAT pixelFormat;
                Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
                stCheckMpoSupportPlaneInfo[0].eSBPixelFormat = pixelFormat;
                uint MpoFlags = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOFlags") select c).FirstOrDefault().Value);
                ULT_MPO_ROTATION mpoRotation;
                Enum.TryParse((from c in planeAttributes.Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
                ULT_MPO_BLEND_VAL mpoBlendVal;
                Enum.TryParse((from c in planeAttributes.Descendants("MPOBlend") select c).FirstOrDefault().Value, out mpoBlendVal);
                ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
                Enum.TryParse((from c in planeAttributes.Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
                uint ycbcr = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
                ULT_MPO_STEREO_FORMAT stereoFormat;
                Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);
                ULT_MPO_STEREO_FLIP_MODE stereo;
                Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);
                ULT_MPO_STRETCH_QUALITY stretchquality;
                Enum.TryParse((from c in planeAttributes.Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);
                stMPOPlaneAttributes[i].eMPORotation = mpoRotation;
                stMPOPlaneAttributes[i].uiMPOFlags = MpoFlags;
                stMPOPlaneAttributes[i].eMPOBlend = mpoBlendVal;
                stMPOPlaneAttributes[i].eMPOVideoFormat = videoFormat;
                stMPOPlaneAttributes[i].uiMPOYCbCrFlags = ycbcr;
                stMPOPlaneAttributes[i].eMPOStereoFormat = stereoFormat;
                stMPOPlaneAttributes[i].eMPOStereoFlipMode = stereo;
                stMPOPlaneAttributes[i].eStretchQuality = stretchquality;
                stMPOPlaneAttributes[i].DIRTYRECTS = new ULT_M_RECT[8];
                stCheckMpoSupportPlaneInfo[i].stPlaneAttributes = stMPOPlaneAttributes[0];
                ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
                stCheckMpoSupportPlaneInfo[i].stSurfaceMemInfo = surfaceMemOffsetInfo;

                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                rectCoordinates.left = 0;
                rectCoordinates.top = 0;
                rectCoordinates.bottom = 800;
                rectCoordinates.right = displayMode.HzRes;
                stMPOPlaneAttributes[i].MPOSrcRect = rectCoordinates;
                rectCoordinates.bottom = 1080;
                stMPOPlaneAttributes[i].MPODstRect = rectCoordinates;
                stMPOPlaneAttributes[i].MPOClipRect = rectCoordinates;
            }
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateNV12Resource();
        }
        [Test(Type = TestType.Method, Order = 7)]
        public virtual void TestStep7()
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
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, 1);
                        }
                        DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, 1);
                    }
                    //     base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, 1);
                    if (null != this._performAction)
                        this._performAction();
                }
            }
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Free Resource");
            foreach (UInt64 pgmm in pGmmBlockList)
                base.ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            base.EnableFeature(false, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            base.EnableULT(false);
        }
        [Test(Type = TestType.Method, Order = 10)]
        public virtual void TestStep10()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MMIO Flips with NV12 content");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
            
        }

        [Test(Type = TestType.Method, Order = 11)]
        public virtual void TestStep11()
        {
            this.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 12)]
        public virtual void TestStep12()
        {
            Log.Message(true, "MMIO Flips with NV12");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync;
            for (int i = 0; i < 3; i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmBlockList[0], 0, 8, sourceAddressFlags);
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
        public virtual void TestStep13()
        {
            Log.Message(true, "Exit ULT Mode");
            foreach (UInt64 pgmm in pGmmBlockList)
                base.ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
            base.EnableULT(false);
        }

    }
}



