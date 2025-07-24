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

    public class SB_ULT_SymmetricScalar_TwoPlane_NV12 : SB_ULT_Base
    {
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        uint sourceId = 0;
        string dumpFilepath = string.Empty;
        protected List<UInt64> pGmmBlockList;
        protected List<IntPtr> pUserVirtualAddressList;
        protected const int planeCount = 2;
        protected System.Action _performAction = null;
        protected XElement planeAttributes;
        protected XDocument ultParserDoc = null;
        private DisplayMode displayMode;
        protected ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[planeCount];
        protected SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
        protected ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            base.TestStep0();

            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("Config:{0} applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
            {
                base.ListEnumeratedDisplays();
                Log.Abort("Config:{0} not applied!", base.CurrentConfig.GetCurrentConfigStr());
            }
        }
        [Test(Type = TestType.PreCondition, Order = 1)]
        public void TestStep1()
        {
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.PrimaryDisplay).First();
            if (base.CurrentConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, displayInfo.DisplayMode))
                    Log.Success("Mode applied Successfully");
            }
            Log.Message(true, "Get mode of Primary Display");
            displayMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            ultParserDoc = XDocument.Load(_paramsDictionary["NV12"]);
            base.EnableDFT(true);
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
            int maxScalarsAvailable = GetMaxScalarsAvailable(base.CurrentConfig, base.CurrentConfig.PrimaryDisplay);
            Log.Message("Max scalars available for {0} is {1}", base.CurrentConfig.PrimaryDisplay, maxScalarsAvailable);

            for (int i = 0; i < planeCount; i++)
            {
                stMPOPlaneAttributes[i] = new ULT_MPO_PLANE_ATTRIBUTES();
                stCheckMpoSupportPlaneInfo[i].uiLayerIndex = Convert.ToUInt32(i); ;
                stCheckMpoSupportPlaneInfo[i].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                stCheckMpoSupportPlaneInfo[i].bIsAsyncMMIOFlip = Boolean.Parse((from c in planeAttributes.Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);
                ULT_PIXELFORMAT pixelFormat;
                Enum.TryParse((from c in planeAttributes.Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
                stCheckMpoSupportPlaneInfo[i].eSBPixelFormat = pixelFormat;
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
                
                ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
                stCheckMpoSupportPlaneInfo[i].stSurfaceMemInfo = surfaceMemOffsetInfo;

                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                rectCoordinates.left = 0;
                rectCoordinates.top = 0;
                rectCoordinates.bottom = 800;
                rectCoordinates.right = displayMode.HzRes;
                stMPOPlaneAttributes[i].MPOSrcRect = rectCoordinates;
                stMPOPlaneAttributes[i].MPODstRect = rectCoordinates;

                rectCoordinates.top = 0;
                rectCoordinates.bottom = displayMode.VtRes;
                rectCoordinates.left = (uint)i * (displayMode.HzRes / planeCount);
                rectCoordinates.right = (uint)(i + 1) * (displayMode.HzRes / planeCount);
                
                if (i >= (planeCount - maxScalarsAvailable))
                    stMPOPlaneAttributes[i].MPODstRect = rectCoordinates;

                stMPOPlaneAttributes[i].MPOClipRect = rectCoordinates;

                Log.Message("For plane {0} dest coordinates are: left:{1}, top:{2}, right:{3}, bottom:{4}", i, stMPOPlaneAttributes[i].MPODstRect.left,
                    stMPOPlaneAttributes[i].MPODstRect.top, stMPOPlaneAttributes[i].MPODstRect.right, stMPOPlaneAttributes[i].MPODstRect.bottom);

                stCheckMpoSupportPlaneInfo[i].stPlaneAttributes = stMPOPlaneAttributes[i];
            }
            stCheckMpoSupportPathInfo[0].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;

            bool supported = false;
            uint failureReason = 0;
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = 1;
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);

            if (supported == true)
                Log.Message("This configuration is feasible");
            else
            {
                Log.Fail("This configuration of 2Plane NV12 MPO is not feasible");
            }
        }

        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateNV12Resource(displayMode.HzRes, displayMode.VtRes);
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
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];
         
            for (int count = 0; count < planeCount; count++)
            {
                mpoFlipPlaneInfo[count].uiLayerIndex = Convert.ToUInt32(count);
                mpoFlipPlaneInfo[count].bEnabled = Boolean.Parse((from c in planeAttributes.Descendants("Enabled") select c).FirstOrDefault().Value);
                mpoFlipPlaneInfo[count].bAffected = Boolean.Parse((from c in planeAttributes.Descendants("Affected") select c).FirstOrDefault().Value);
                mpoFlipPlaneInfo[count].stPlaneAttributes = stCheckMpoSupportPlaneInfo[count].stPlaneAttributes;

                mpoFlipPlaneInfo[count].hAllocation = pGmmBlockList[count];
            }

            base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
            if (currentOSPageConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Clone)
            {
                if (currentOSPageConfig.TertiaryDisplay != DisplayType.None)
                {
                    DisplayInfo displayInfoTer = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.TertiaryDisplay).First();
                    base.RegisterCheck(currentOSPageConfig.TertiaryDisplay, displayInfoTer, NV12RegisterEvent, planeCount, planeCount);

                    int currentScalarsTer = GetScalarsAvailable(base.CurrentConfig.TertiaryDisplay);
                    if (0 == currentScalarsTer)
                        Log.Success("All the scalars are utilized properly for {0}", base.CurrentConfig.TertiaryDisplay);
                    else
                        Log.Fail("Scalars are not used as expected. Still:{0} are available for {1}.", currentScalarsTer, base.CurrentConfig.TertiaryDisplay);
                }
                DisplayInfo displayInfoSec = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == currentOSPageConfig.SecondaryDisplay).First();
                base.RegisterCheck(currentOSPageConfig.SecondaryDisplay, displayInfoSec, NV12RegisterEvent, planeCount, planeCount);
                int currentScalarsSec = GetScalarsAvailable(base.CurrentConfig.SecondaryDisplay);
                if (0 == currentScalarsSec)
                    Log.Success("All the scalars are utilized properly for {0}", base.CurrentConfig.SecondaryDisplay);
                else
                    Log.Fail("Scalars are not used as expected. Still:{0} are available for {1}.", currentScalarsSec, base.CurrentConfig.SecondaryDisplay);
            }
            base.RegisterCheck(currentOSPageConfig.PrimaryDisplay, displayInfo, NV12RegisterEvent, planeCount, planeCount);

            int currentScalars = GetScalarsAvailable(base.CurrentConfig.PrimaryDisplay);
            if (0 == currentScalars)
                Log.Success("All the scalars are utilized properly for {0}", base.CurrentConfig.PrimaryDisplay);
            else
                Log.Fail("Scalars are not used as expected. Still:{0} are available for {1}.", currentScalars, base.CurrentConfig.PrimaryDisplay);
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
            base.EnableDFT(false);
        }
    }
}



