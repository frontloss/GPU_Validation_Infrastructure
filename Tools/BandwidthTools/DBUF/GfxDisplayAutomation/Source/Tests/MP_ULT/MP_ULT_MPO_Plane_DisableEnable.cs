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

    public class MP_ULT_MPO_Plane_DisableEnable : MP_ULT_Base
    {
        ULT_MPO_PLANE_ATTRIBUTES stMPOPlaneAttributes;
        string dumpFilepath = string.Empty;
        uint sourceId = 0;
        const uint SPI_SETCURSORS = 0X0057;
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        XElement planeAttributes;
        //    MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes;
        protected List<UInt64> pGmmBlockList;
        protected List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
        //private const int planeCount = 1;
        protected ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo;

        [DllImport("user32.dll", EntryPoint = "SystemParametersInfo")]
        internal static extern bool SystemParametersInfo(uint uiAction, uint uiParam, string pvParam, uint fWinIni);

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.DisableCursor();
            Log.Message(true, "Enable ULT Mode");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            ultParserDoc = XDocument.Load(_paramsDictionary["YTile"]);
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

            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = 1;

            ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];
            stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();

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
            stMPOPlaneAttributes.eMPORotation = mpoRotation;
            stMPOPlaneAttributes.uiMPOFlags = MpoFlags;
            stMPOPlaneAttributes.eMPOBlend = mpoBlendVal;
            stMPOPlaneAttributes.eMPOVideoFormat = videoFormat;
            stMPOPlaneAttributes.uiMPOYCbCrFlags = ycbcr;
            stMPOPlaneAttributes.eMPOStereoFormat = stereoFormat;
            stMPOPlaneAttributes.eMPOStereoFlipMode = stereo;
            stMPOPlaneAttributes.eStretchQuality = stretchquality;
            stMPOPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];
            stCheckMpoSupportPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes;
            ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
            stCheckMpoSupportPlaneInfo[0].stSurfaceMemInfo = surfaceMemOffsetInfo;

            ULT_M_RECT rectCoordinates = new ULT_M_RECT();
            Log.Alert("Source Rect == Dest Rect == Clip Rect");
            rectCoordinates.left = 0;
            rectCoordinates.top = 0;
            rectCoordinates.bottom = displayMode.VtRes;
            rectCoordinates.right = displayMode.HzRes;
            stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;
            stMPOPlaneAttributes.MPODstRect = rectCoordinates;
            stMPOPlaneAttributes.MPOClipRect = rectCoordinates;

            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }

        [Test(Type = TestType.Method, Order = 6)]
        public virtual void TestStep6()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateYTileResource();
        }
        [Test(Type = TestType.Method, Order = 7)]
        public virtual void TestStep7()
        {
            Log.Message(true, "Set Source Address MPO");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            uint numPlanes = 1;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            mpoFlipPlaneInfo[0].uiLayerIndex = 0;
            mpoFlipPlaneInfo[0].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
            mpoFlipPlaneInfo[0].stPlaneAttributes = stMPOPlaneAttributes;
            for (int j = 0; j < 3; j++)
            {
                for (int i = 0; i < fileEntries.Length; i++)
                {
                    mpoFlipPlaneInfo[0].hAllocation = pGmmBlockList[j % 3];
                    base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                    if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                    {
                        if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                        {
                            DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                            base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, 1, 999);
                        }
                        DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, 1, 999);
                    }
                    base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, 1, 999);
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
        //     [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Disable ULT Mode");
            base.EnableULT(false);
        }

        [Test(Type = TestType.Method, Order = 10)]
        public void TestStep10()
        {
            base.EnableFeature(false, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
            Thread.Sleep(5000);
            Log.Message(true, "Single Plane MMIO    ");
            //   base.EnableULT(true);
            ultParserDoc = XDocument.Load(_paramsDictionary["YTile"]);
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
            Log.Message("MMIO Flip");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags); ;
            for (uint i = 0; i < 3; i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmBlockList[0], sourceId, 8, sourceAddressFlags);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, 1, 999);
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, 1, 0);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, 1, 999);
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, 1, 0);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, 1, 999);
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, 1, 0);
            }
        }
        [Test(Type = TestType.Method, Order = 13)]
        public void TestStep13()
        {
            //Log.Message(true, "Exit ULT Framework");
            this.TestStep8();
            //base.TestStep9();
            //Thread.Sleep(5000);
        }
        [Test(Type = TestType.Method, Order = 14)]
        public void TestStep14()
        {
            
            Log.Message(true, "Two Plane MPO");
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            //this.TestStep6();
            //CheckTwoPlaneMPO();
            //this.TestStep8();
            //base.TestStep9();
            //Thread.Sleep(5000);
        }
        [Test(Type = TestType.Method, Order = 15)]
        public void TestStep15()
        {
            Log.Message(true, "Three Plane MPO    ");
            //base.EnableULT(true);
            this.TestStep6();
            CheckThreePlaneMPO();
            this.TestStep8();
            //base.TestStep9();
            //Thread.Sleep(5000);
        }
        [Test(Type = TestType.Method, Order = 16)]
        public void TestStep16()
        {
            //base.EnableULT(true);
            this.TestStep6();
            CheckTwoPlaneMPO();
            this.TestStep8();
            //base.TestStep9();
            //Thread.Sleep(5000);
        }

        [Test(Type = TestType.Method, Order = 17)]
        public void TestStep17()
        {
            Log.Message(true, "Exit ULT Framework");
            this.TestStep8();
            base.EnableULT(false);
            Thread.Sleep(5000);
            string tempStr = null;
            SystemParametersInfo(SPI_SETCURSORS, 0, tempStr, 0);
        }

        private void CheckTwoPlaneMPO()
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
            stCheckMpoSupportPathInfo[0].uiPlaneCount = 2;

            stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];


            for (int j = 0; j < 2; j++)
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
                if (j == 0)
                {
                    rectCoordinates.right = displayMode.HzRes / 2;
                }
                else
                {
                    rectCoordinates.left = displayMode.HzRes / 2;
                }
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



            Log.Message(true, "Set Source Address MPO");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            uint numPlanes = 2;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            for (int j = 0; j < 3; j++)
            {
                for (int count = 0; count < 2; count++)
                {
                    mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                    mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;
                    mpoFlipPlaneInfo[count].hAllocation = this.pGmmBlockList[(count + j) % 3];
                }
                base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, 2, 999);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, 2, 999);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, 2, 999);
            }
            // this.TestStep13();
        }

        private void CheckThreePlaneMPO()
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
            stCheckMpoSupportPathInfo[0].uiPlaneCount = 3;

            stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];


            for (int j = 0; j < 3; j++)
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
                if (j == 0)
                {
                    rectCoordinates.right = displayMode.HzRes / 3;
                }
                if (j == 1)
                {
                    rectCoordinates.left = displayMode.HzRes / 3;
                    rectCoordinates.right = displayMode.HzRes - rectCoordinates.left;
                }
                if (j == 2)
                {
                    rectCoordinates.left = displayMode.HzRes - displayMode.HzRes / 3;
                    rectCoordinates.right = displayMode.HzRes;
                }
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

            //base.TestStep6();

            Log.Message(true, "Set Source Address MPO");
            DisplayConfig currentOSPageConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get, Source.AccessAPI);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.PrimaryDisplay).First();
            uint numPlanes = 3;
            uint sourceId = 0;
            string sourceFlags = (from c in planeAttributes.Descendants("SourceAddressFlags") select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
            for (int j = 0; j < 1; j++)
            {
                //if (j == 9)
                //    Log.Message("Hi");
                for (int count = 0; count < 3; count++)
                {
                    mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                    mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                    mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;
                    mpoFlipPlaneInfo[count].hAllocation = this.pGmmBlockList[(count) % 3];
                }
                base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
                {
                    if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                    {
                        DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                        base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, MPORegisterEvent, 3, 999);
                    }
                    DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, MPORegisterEvent, 3, 999);
                }
                base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, MPORegisterEvent, 3, 999);
            }
            for (int count = 0; count < 3; count++)
            {
                if (count == 0)
                {
                    mpoFlipPlaneInfo[count].bEnabled = false;
                }
                else
                {
                    mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                }
                mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;
                mpoFlipPlaneInfo[count].hAllocation = this.pGmmBlockList[count];
            }
            base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
            // this.TestStep13();
        }

    }
}


