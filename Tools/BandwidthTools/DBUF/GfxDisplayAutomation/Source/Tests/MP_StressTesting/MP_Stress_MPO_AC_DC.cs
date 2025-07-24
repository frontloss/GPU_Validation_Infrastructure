namespace Intel.VPG.Display.Automation
{
    using System.Threading.Tasks;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Xml;
    using System.Text.RegularExpressions;
    using System.IO;
    using System.Xml.Linq;
    using System.Xml.Serialization;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;

    class MP_Stress_MPO_AC_DC : MP_ULT_Base
    {
        internal int StressCycle = 0;
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        XElement planeAttributes;
        ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[planeCount];
        string dumpFilepath = string.Empty;
        protected List<UInt64> pGmmBlockList;
        private uint sourceId = 0;
        protected List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
        protected PowerParams _powerParams = null;
        private const int planeCount = 1;

        internal string TestName = string.Empty;
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            GetTestAttribute();
           Log.Message(true, "Running AC-DC Stress Test for {0}", StressCycle);
           
           for (int i = 0; i < StressCycle; i++)
           {
               Log.Message(true, "Cycle --- {0} ", i);
          
                   TestStep3();
                   TestStep4();
                   TestStep5();
                   TestStep6();
                   TestStep7();
                   TestStep8();
                   TestStep9();
                   this._powerParams = new PowerParams() { Delay = 30 };
                   if (i % 2 == 0)
                   {
                       Log.Message(true, "Enable AC Mode");
                       PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

                       if (powerState == PowerLineStatus.Offline)
                       {
                           if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                               Log.Success("System is Running in AC Mode");
                           else
                               Log.Fail("Fail to set AC mode");
                       }
                       else
                           Log.Success("System is Running in AC Mode");
                   }
                   else
                   {
                       Log.Message(true, "Enable DC Mode");
                       PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

                       if (powerState == PowerLineStatus.Online)
                       {
                           if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                               Log.Success("System is Running in DC Mode");
                           else
                               Log.Fail("Fail to set DC Mode");
                       }
                       else
                           Log.Success("System is Running in DC Mode");
                   }
           

           }
        }
        private void GetTestAttribute()
        {
            TestName = base.ApplicationManager.ParamInfo.Get<String>(ArgumentType.TestName);
            XmlDocument benchmarkValue = new XmlDocument();
            benchmarkValue.Load("Mapper\\StressParam.map");
            XmlNode eventBenchmarkRoot = benchmarkValue.SelectSingleNode("/Data");
            foreach (XmlNode chNode in eventBenchmarkRoot.ChildNodes)
            {
                if (TestName.Equals(Convert.ToString(chNode.Attributes["name"].Value)))
                {
                    StressCycle = Convert.ToInt32(chNode.Attributes["cycle"].Value);
                    break;
                }
            }
            if (StressCycle == 0)
            {
                Log.Abort("Could not found stress test attribute in StressParam.map file");
            }
        }

        public virtual void TestStep3()
        {
            base.EnableULT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            ultParserDoc = XDocument.Load(_paramsDictionary["YTile"]);
            fileEntries = Directory.GetFiles(_dumpsDictionary["YTile"]);
        }
        public void TestStep4()
        {
            base.ULT_FW_Get_MPO_Caps(sourceId, ref stMpoCaps);
        }

        public void TestStep5()
        {
            //ULT_MPO_GROUP_CAPS[] stMpoGroupCaps = new ULT_MPO_GROUP_CAPS[stMpoCaps.uiNumCapabilityGroups];
            //for (uint i = 0; i < stMpoCaps.uiNumCapabilityGroups; i++)
            //{
            //    base.ULT_FW_MPO_Group_Caps(sourceId, i, ref stMpoGroupCaps[i]);
            //}
        }

        public virtual void TestStep6()
        {
            Log.Message(true, "Check MPO");
            planeAttributes = ultParserDoc.Descendants("PlaneAttributes").FirstOrDefault();

            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];
            stCheckMpoSupportPathInfo[0].uiPlaneCount = planeCount;

            ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];
            for (int i = 0; i < planeCount; i++)
            {
                stMPOPlaneAttributes[i] = new ULT_MPO_PLANE_ATTRIBUTES();

                stCheckMpoSupportPlaneInfo[i].uiLayerIndex = Convert.ToUInt32(i);
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
                stCheckMpoSupportPlaneInfo[i].stPlaneAttributes = stMPOPlaneAttributes[0];
                ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
                stCheckMpoSupportPlaneInfo[i].stSurfaceMemInfo = surfaceMemOffsetInfo;

                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                Log.Alert("Source Rect == Dest Rect == Clip Rect");
                rectCoordinates.left = 0;
                rectCoordinates.top = 0;
                rectCoordinates.bottom = displayMode.VtRes;
                rectCoordinates.right = displayMode.HzRes;
                stMPOPlaneAttributes[i].MPOSrcRect = rectCoordinates;
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

        public virtual void TestStep7()
        {
            pGmmBlockList = new List<UInt64>();
            pGmmBlockList = base.CreateYTileResource();
         }
        public virtual void TestStep8()
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

            int i = 0;

            Log.Message("File Entry - {0}", i);
            mpoFlipPlaneInfo[0].hAllocation = pGmmBlockList[i];
            base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);     
        }

        public void TestStep9()
        {
            Log.Message(true, "Free Resource");
            foreach (UInt64 pgmm in pGmmBlockList)
                base.ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
            pUserVirtualAddressList.Clear();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep10()
        {
            base.EnableFeature(false, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);
            base.EnableULT(false);
        }
    }
}
