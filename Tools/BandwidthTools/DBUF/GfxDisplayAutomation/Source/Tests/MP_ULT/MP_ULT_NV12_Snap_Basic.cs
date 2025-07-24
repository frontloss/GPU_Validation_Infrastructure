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

    public class MP_ULT_NV12_Snap_Basic : MP_ULT_NV12_FullScreen_Basic
    {
        private new const int planeCount = 2;
        string dumpFilepath = string.Empty;
        ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];
        ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[planeCount];

        [Test(Type = TestType.Method, Order = 10)]
        public override void TestStep10()
        {
            Thread.Sleep(5000);
            Log.Message(true, "MPO Flips with NV12 content in snap mode");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
        }
        [Test(Type = TestType.Method, Order = 11)]
        public override void TestStep11()
        {
            base.TestStep3();
            base.TestStep4();
        }
        [Test(Type = TestType.Method, Order = 12)]
        public override void TestStep12()
        {
            Log.Message(true, "Check MPO");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();

            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            stMPOPlaneAttributes[0] = new ULT_MPO_PLANE_ATTRIBUTES();

            stCheckMpoSupportPlaneInfo[0].uiLayerIndex = 0;
            stCheckMpoSupportPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            stCheckMpoSupportPlaneInfo[0].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);
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
            stMPOPlaneAttributes[0].eMPORotation = mpoRotation;
            stMPOPlaneAttributes[0].uiMPOFlags = MpoFlags;
            stMPOPlaneAttributes[0].eMPOBlend = mpoBlendVal;
            stMPOPlaneAttributes[0].eMPOVideoFormat = videoFormat;
            stMPOPlaneAttributes[0].uiMPOYCbCrFlags = ycbcr;
            stMPOPlaneAttributes[0].eMPOStereoFormat = stereoFormat;
            stMPOPlaneAttributes[0].eMPOStereoFlipMode = stereo;
            stMPOPlaneAttributes[0].eStretchQuality = stretchquality;
            stMPOPlaneAttributes[0].DIRTYRECTS = new ULT_M_RECT[8];
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes[0];
            ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[0].stSurfaceMemInfo = surfaceMemOffsetInfo;


            ULT_M_RECT rectCoordinates = new ULT_M_RECT();
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = 800;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes[0].MPOSrcRect = rectCoordinates;
            rectCoordinates.bottom = 1080;
            rectCoordinates.left = displayMode.HzRes / 2;
            stMPOPlaneAttributes[0].MPODstRect = rectCoordinates;
            stMPOPlaneAttributes[0].MPOClipRect = rectCoordinates;
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            stMPOPlaneAttributes[1] = new ULT_MPO_PLANE_ATTRIBUTES();

            stMPOPlaneAttributes[1].eMPORotation = mpoRotation;
            stMPOPlaneAttributes[1].uiMPOFlags = MpoFlags;
            stMPOPlaneAttributes[1].eMPOBlend = mpoBlendVal;
            stMPOPlaneAttributes[1].eMPOVideoFormat = videoFormat;
            stMPOPlaneAttributes[1].uiMPOYCbCrFlags = ycbcr;
            stMPOPlaneAttributes[1].eMPOStereoFormat = stereoFormat;
            stMPOPlaneAttributes[1].eMPOStereoFlipMode = stereo;
            stMPOPlaneAttributes[1].eStretchQuality = stretchquality;
            stMPOPlaneAttributes[1].DIRTYRECTS = new ULT_M_RECT[8];
            stCheckMpoSupportPlaneInfo[1].stPlaneAttributes = stMPOPlaneAttributes[1];
            surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[1].stSurfaceMemInfo = surfaceMemOffsetInfo;


            rectCoordinates = new ULT_M_RECT();
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = 800;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes[1].MPOSrcRect = rectCoordinates;
            rectCoordinates.right = displayMode.HzRes / 2;
            rectCoordinates.bottom = 1080;
            stMPOPlaneAttributes[1].MPODstRect = rectCoordinates;
            stMPOPlaneAttributes[1].MPOClipRect = rectCoordinates;
            stCheckMpoSupportPathInfo[1].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }
        [Test(Type = TestType.Method, Order = 13)]
        public override void TestStep13()
        {
            base.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
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
                    mpoFlipPlaneInfo[count].hAllocation = base.pGmmBlockList[0];
                }
                base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, planeCount, 999);
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, 2);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, planeCount, 999);
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, 2);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, planeCount, 999);
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, 2);
            }
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message(true, "Free Resource");
            foreach (UInt64 pgmm in pGmmBlockList)
                base.ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            Log.Message(true, "Disable ULT Mode");
            base.EnableULT(false);
        }
    }
}



