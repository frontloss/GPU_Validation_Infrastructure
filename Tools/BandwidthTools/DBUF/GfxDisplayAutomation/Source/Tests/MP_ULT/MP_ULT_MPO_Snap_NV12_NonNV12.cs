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

    public class MP_ULT_MPO_Snap_NV12_NonNV12 : MP_ULT_MPO_Single_Plane_Basic
    {
        protected XElement planeAttributes;
        protected XElement planeAttributesNv12;
        protected ULT_MPO_PLANE_ATTRIBUTES stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
        string dumpFilepath = string.Empty;
        private const int planeCount = 2;
        protected ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo;
        protected XDocument ultParserDocNV12 = null;
        protected string[] fileEntriesNV12;

        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            ultParserDocNV12 = XDocument.Load(_paramsDictionary["NV12"]);
            fileEntriesNV12 = Directory.GetFiles(_dumpsDictionary["NV12"]);
            base.TestStep2();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public override void TestStep5()
        {
            Log.Message(true, "Check MPO");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();

            ULT_PIXELFORMAT pixelFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
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


            planeAttributesNv12 = ultParserDocNV12.Descendants("PlaneAttributes").FirstOrDefault();

            ULT_PIXELFORMAT pixelFormatNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormatNV12);
            uint MpoFlagsNV12 = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOFlags") select c).FirstOrDefault().Value);
            ULT_MPO_ROTATION mpoRotationNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotationNV12);
            ULT_MPO_BLEND_VAL mpoBlendValNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("MPOBlend") select c).FirstOrDefault().Value, out mpoBlendValNV12);
            ULT_MPO_VIDEO_FRAME_FORMAT videoFormatNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormatNV12);
            uint ycbcrNV12 = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
            ULT_MPO_STEREO_FORMAT stereoFormatNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormatNV12);
            ULT_MPO_STEREO_FLIP_MODE stereoNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereoNV12);
            ULT_MPO_STRETCH_QUALITY stretchqualityNV12;
            Enum.TryParse((from c in planeAttributesNv12.Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchqualityNV12);


            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];

            #region fillYtiledata

            stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
            stCheckMpoSupportPlaneInfo[0].uiLayerIndex = Convert.ToUInt32(0);
            stCheckMpoSupportPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            stCheckMpoSupportPlaneInfo[0].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);

            stCheckMpoSupportPlaneInfo[0].eSBPixelFormat = pixelFormat;

            stMPOPlaneAttributes.eMPORotation = mpoRotation;
            stMPOPlaneAttributes.uiMPOFlags = MpoFlags;
            stMPOPlaneAttributes.eMPOBlend = mpoBlendVal;
            stMPOPlaneAttributes.eMPOVideoFormat = videoFormat;
            stMPOPlaneAttributes.uiMPOYCbCrFlags = ycbcr;
            stMPOPlaneAttributes.eMPOStereoFormat = stereoFormat;
            stMPOPlaneAttributes.eMPOStereoFlipMode = stereo;
            stMPOPlaneAttributes.eStretchQuality = stretchquality;
            stMPOPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];
            ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[0].stSurfaceMemInfo = surfaceMemOffsetInfo;
            ULT_M_RECT rectCoordinates = new ULT_M_RECT();
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = displayMode.VtRes;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;
            rectCoordinates.left = 960;
            stMPOPlaneAttributes.MPODstRect = rectCoordinates;
            stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes;
            #endregion

            #region fillNv12Data

            stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
            stCheckMpoSupportPlaneInfo[1].uiLayerIndex = Convert.ToUInt32(1);
            stCheckMpoSupportPlaneInfo[1].bEnabled = Boolean.Parse((from c in planeAttributesNv12.Descendants("Enabled") select c).FirstOrDefault().Value);
            stCheckMpoSupportPlaneInfo[1].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributesNv12.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);

            stCheckMpoSupportPlaneInfo[1].eSBPixelFormat = pixelFormatNV12;

            stMPOPlaneAttributes.eMPORotation = mpoRotationNV12;
            stMPOPlaneAttributes.uiMPOFlags = MpoFlagsNV12;
            stMPOPlaneAttributes.eMPOBlend = mpoBlendValNV12;
            stMPOPlaneAttributes.eMPOVideoFormat = videoFormatNV12;
            stMPOPlaneAttributes.uiMPOYCbCrFlags = ycbcrNV12;
            stMPOPlaneAttributes.eMPOStereoFormat = stereoFormatNV12;
            stMPOPlaneAttributes.eMPOStereoFlipMode = stereoNV12;
            stMPOPlaneAttributes.eStretchQuality = stretchqualityNV12;
            stMPOPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];
            surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[1].stSurfaceMemInfo = surfaceMemOffsetInfo;
            rectCoordinates = new ULT_M_RECT();
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = 800;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;
            rectCoordinates.bottom = displayMode.VtRes;
            rectCoordinates.right = 960;
            stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
            stMPOPlaneAttributes.MPODstRect = rectCoordinates;
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes = stMPOPlaneAttributes;

            #endregion


            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public override void TestStep6()
        {
            base.TestStep6();
            List<UInt64> pNV12GmmBlockList = new List<UInt64>();
            pNV12GmmBlockList = base.CreateNV12Resource();
            pGmmBlockList.AddRange(pNV12GmmBlockList);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public override void TestStep7()
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
            for (int j = 0; j < 3; j++)
            {
                for (int count = 0; count < planeCount; count++)
                {
                    mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                    mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;

                    if (count == 0)
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[(count + j) % 3];
                    else
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[3];
                }
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
        [Test(Type = TestType.Method, Order = 10)]
        public virtual void TestStep10()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MMIO Flips with non NV12 content");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
        }

        [Test(Type = TestType.Method, Order = 11)]
        public virtual void TestStep11()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateMMIOResource();
        }
        [Test(Type = TestType.Method, Order = 12)]
        public virtual void TestStep12()
        {
            Log.Message(true, "MMIO Flips with Y-tile");
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

        [Test(Type = TestType.Method, Order = 14)]
        public virtual void TestStep14()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MPO Flips with Switched NV12 and Non NV12 content");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
        }
        [Test(Type = TestType.Method, Order = 15)]
        public virtual void TestStep15()
        {
            base.TestStep3();
            base.TestStep4();
            this.TestStep5();
            this.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 16)]
        public virtual void TestStep16()
        {
            Log.Message(true, "Set Source Address MPO after switching NV12 and Non NV12 Content");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            uint numPlanes = planeCount;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes.MPODstRect.left = 0;
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes.MPOClipRect.left = 0;
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes.MPODstRect.right = displayMode.HzRes / 2;
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes.MPOClipRect.right = displayMode.HzRes / 2;

            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes.MPODstRect.left = displayMode.HzRes / 2;
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes.MPOClipRect.left = displayMode.HzRes / 2;
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes.MPODstRect.right = displayMode.HzRes;
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes.MPOClipRect.right = displayMode.HzRes;

            for (int j = 0; j < 3; j++)
            {
                for (int count = 0; count < planeCount; count++)
                {
                    mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                    mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;
                    if (count == 0)
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[(count + j) % 3];
                    else
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[3];
                }
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
        [Test(Type = TestType.Method, Order = 17)]
        public virtual void TestStep17()
        {
            this.TestStep13();
            base.EnableULT(false);
        }
    }
}



