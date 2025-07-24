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

    public class MP_ULT_MPO_TwoPlane : MP_ULT_MPO_Single_Plane_Basic
    {
        protected XElement planeAttributes;
        protected ULT_MPO_PLANE_ATTRIBUTES stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
        string dumpFilepath = string.Empty;
        private const int planeCount = 2;
        protected ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo;

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

            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];


            for (int j = 0; j < planeCount; j++)
            {
                stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
                stCheckMpoSupportPlaneInfo[j].uiLayerIndex = Convert.ToUInt32(j);
                stCheckMpoSupportPlaneInfo[j].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                stCheckMpoSupportPlaneInfo[j].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);

                stCheckMpoSupportPlaneInfo[j].eSBPixelFormat = pixelFormat;

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
                stCheckMpoSupportPlaneInfo[j].stSurfaceMemInfo = surfaceMemOffsetInfo;

                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                rectCoordinates.left = 0;
                rectCoordinates.top = 0;
                rectCoordinates.bottom = displayMode.VtRes;
                rectCoordinates.right = displayMode.HzRes;
                stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;
                stMPOPlaneAttributes.MPODstRect = rectCoordinates;
                if (j == 0)
                {
                    rectCoordinates.left = displayMode.HzRes / 2;
                }
                else
                {
                    rectCoordinates.right = displayMode.HzRes / 2;
                }
                stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
                stCheckMpoSupportPlaneInfo[j].stPlaneAttributes = stMPOPlaneAttributes;
            }
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
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
                    mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[(count + j) % 3];
                }
                base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, planeCount, 999);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, planeCount, 999);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
            }
        }


        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            Log.Message("Non NV12 content with charms");
            base.TestStep2();
            base.TestStep3();
            base.TestStep4();

        }
        [Test(Type = TestType.Method, Order = 11)]
        public void TestStep11()
        {
            Log.Message(true, "Check MPO");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();

            ULT_PIXELFORMAT pixelFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
            uint MpoFlags = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOFlags") select c).FirstOrDefault().Value);
            ULT_MPO_ROTATION mpoRotation;
            Enum.TryParse((from c in planeAttributes.Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
            ULT_MPO_BLEND_VAL mpoBlendVal = ULT_MPO_BLEND_VAL.AlphaBlend;
            ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
            uint ycbcr = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
            ULT_MPO_STEREO_FORMAT stereoFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);
            ULT_MPO_STEREO_FLIP_MODE stereo;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);
            ULT_MPO_STRETCH_QUALITY stretchquality;
            Enum.TryParse((from c in planeAttributes.Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);

            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];


            for (int j = 0; j < planeCount; j++)
            {
                stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
                stCheckMpoSupportPlaneInfo[j].uiLayerIndex = Convert.ToUInt32(j);
                stCheckMpoSupportPlaneInfo[j].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                stCheckMpoSupportPlaneInfo[j].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);

                stCheckMpoSupportPlaneInfo[j].eSBPixelFormat = pixelFormat;

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
                stCheckMpoSupportPlaneInfo[j].stSurfaceMemInfo = surfaceMemOffsetInfo;



                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                rectCoordinates.left = 0;
                rectCoordinates.top = 0;
                rectCoordinates.bottom = displayMode.VtRes;
                rectCoordinates.right = displayMode.HzRes;
                stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;

                //if (j == 0)
                //{
                //    rectCoordinates.right = displayMode.HzRes / 2;
                //}
                //if (j == 1)
                //{
                //    rectCoordinates.left = displayMode.HzRes / 2;
                //}
                stMPOPlaneAttributes.MPODstRect = rectCoordinates;
                stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
                stCheckMpoSupportPlaneInfo[j].stPlaneAttributes = stMPOPlaneAttributes;
            }
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }
        [Test(Type = TestType.Method, Order = 12)]
        public void TestStep12()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateYTileResource();
            List<UInt64> pCharmGmmBlockList = new List<UInt64>();
            pCharmGmmBlockList = base.CreateCharmResource();
            pGmmBlockList.AddRange(pCharmGmmBlockList);
        }

        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
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
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[3];

                    if (count == 1)
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[j % 3];
                }
                base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, planeCount, 999);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, planeCount, 999);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
            }
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            base.TestStep8();
            base.TestStep9();
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message("NV12 content with charms");
            ultParserDoc = XDocument.Load(_paramsDictionary["NV12"]);
            base.TestStep2();
            base.TestStep3();
            base.TestStep4();
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            Log.Message(true, "Check MPO");


            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();

            ultParserDoc = XDocument.Load(_paramsDictionary["YTile"]);
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();
            stCheckMpoSupportPlaneInfo[0].uiLayerIndex = 0;
            stCheckMpoSupportPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            stCheckMpoSupportPlaneInfo[0].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);
            ULT_PIXELFORMAT pixelFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
            stCheckMpoSupportPlaneInfo[0].eSBPixelFormat = pixelFormat;
            uint MpoFlags = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOFlags") select c).FirstOrDefault().Value);
            ULT_MPO_ROTATION mpoRotation;
            Enum.TryParse((from c in planeAttributes.Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
            ULT_MPO_BLEND_VAL mpoBlendVal = ULT_MPO_BLEND_VAL.AlphaBlend;
            ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
            uint ycbcr = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
            ULT_MPO_STEREO_FORMAT stereoFormat;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);
            ULT_MPO_STEREO_FLIP_MODE stereo;
            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);
            ULT_MPO_STRETCH_QUALITY stretchquality;
            Enum.TryParse((from c in planeAttributes.Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);
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
            stMPOPlaneAttributes.MPODstRect = rectCoordinates;
            stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes;
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
            ultParserDoc = XDocument.Load(_paramsDictionary["NV12"]);
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();
            stCheckMpoSupportPlaneInfo[1].uiLayerIndex = 1;
            stCheckMpoSupportPlaneInfo[1].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            stCheckMpoSupportPlaneInfo[1].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);

            Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
            stCheckMpoSupportPlaneInfo[0].eSBPixelFormat = pixelFormat;
            MpoFlags = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOFlags") select c).FirstOrDefault().Value);

            Enum.TryParse((from c in planeAttributes.Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
            mpoBlendVal = ULT_MPO_BLEND_VAL.AlphaBlend;

            Enum.TryParse((from c in planeAttributes.Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
            ycbcr = Convert.ToUInt32((from c in planeAttributes.Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);

            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);

            Enum.TryParse((from c in planeAttributes.Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);

            Enum.TryParse((from c in planeAttributes.Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);
            stMPOPlaneAttributes.eMPORotation = mpoRotation;
            stMPOPlaneAttributes.uiMPOFlags = MpoFlags;
            stMPOPlaneAttributes.eMPOBlend = mpoBlendVal;
            stMPOPlaneAttributes.eMPOVideoFormat = videoFormat;
            stMPOPlaneAttributes.uiMPOYCbCrFlags = ycbcr;
            stMPOPlaneAttributes.eMPOStereoFormat = stereoFormat;
            stMPOPlaneAttributes.eMPOStereoFlipMode = stereo;
            stMPOPlaneAttributes.eStretchQuality = stretchquality;
            stMPOPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];

            surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[1].stSurfaceMemInfo = surfaceMemOffsetInfo;


            rectCoordinates = new ULT_M_RECT();
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = 800;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;
            rectCoordinates.bottom = 1080;
            stMPOPlaneAttributes.MPODstRect = rectCoordinates;
            stMPOPlaneAttributes.MPOClipRect = rectCoordinates;
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes = stMPOPlaneAttributes;
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;



            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);

        }

        [Test(Type = TestType.Method, Order = 17)]
        public void TestStep17()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateNV12Resource();
            List<UInt64> pCharmsGmmBlockList = new List<UInt64>();
            pCharmsGmmBlockList = base.CreateCharmResource();
            pGmmBlockList.AddRange(pCharmsGmmBlockList);
        }
        [Test(Type = TestType.Method, Order = 18)]
        public void TestStep18()
        {

            Log.Message(true, "Set Source Address MPO snap Mode with  NV12");
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
                    if (count == 1)

                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[0];
                    else
                        mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[1];
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
        [Test(Type = TestType.Method, Order = 19)]
        public void TestStep19()
        {
            base.TestStep8();
            base.TestStep9();
        }
    }
}



