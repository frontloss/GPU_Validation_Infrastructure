namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
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

    public class SB_Plane_Scalar_Two_Plane:SB_Plane_Scalar_Single_Plane
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

            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.CurrentConfig.PrimaryDisplay).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            

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
                rectCoordinates.bottom = 1080;
                rectCoordinates.right = 1920;
                stMPOPlaneAttributes.MPOSrcRect = rectCoordinates;

                rectCoordinates.bottom = currentMode.VtRes;
                if (j == 0)
                {
                    rectCoordinates.left = currentMode.HzRes/2;
                    rectCoordinates.right = currentMode.HzRes;
                }
                else
                {
                    rectCoordinates.left = 0;
                    rectCoordinates.right = currentMode.HzRes / 2;
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
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];
            for (int j = 0; j < 1; j++)
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
                base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    uint totalScalar = CheckRegisters(curDisp);
                    if (totalScalar == 2)
                    {
                        Log.Success("Total Scalar enabled for {0} : {1}", curDisp, totalScalar);
                        base.CurrentConfig.CustomDisplayList.ForEach(eachDisplay => CheckWatermark(eachDisplay));
                    }
                    else
                        Log.Fail("Total Scalar enabled for {0} : {1} , Expected 2", curDisp, totalScalar);
                });
            }
        }
    }
}
