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
    using System.Runtime.InteropServices;

    public class SB_ULT_MPO_Flip : SB_ULT_Base
    {
        DisplayConfig displayConfig;
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        string escapeCodeName;
        XDocument ultParserDoc = null;
        string dumpFilepath = string.Empty;
        UInt64 pGmmBlock = 0;
        IntPtr pUserVirtualAddress;
        uint fileIndex;

        public const int MAX_PLANES = 13;
        public const int MAX_PIPES = 3;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set Config as ED EDP, DP");
            displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.ED,
                PrimaryDisplay = DisplayType.EDP,
                SecondaryDisplay = DisplayType.DP
            };
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, displayConfig))
            {
                Log.Success("{0} Applied successfully", displayConfig.GetCurrentConfigStr());
            }
            else
                Log.Abort("Failed to Apply {0}", displayConfig.GetCurrentConfigStr());
            ultParserDoc = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), "\\ULTParams.xml"));
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Enable ULT Mode");
            base.EnableDFT(true);
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Create resource for 3 planes");
            string escapeCodeName = "ULT_CREATE_RESOURCE";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            List<XElement> dumpFileElement = (from c in Element.Descendants("DumpFilePath") select c).ToList();
            List<string> dumpFilePaths = new List<string>();
            foreach (XElement dumpFilepath in dumpFileElement)
                dumpFilePaths.Add(dumpFilepath.Value);
            fileIndex = Convert.ToUInt32((from c in Element.Descendants("FileIndex")
                                          select c).FirstOrDefault().Value);
            foreach (string dump in dumpFilePaths)
            {
                ulong dataSize = 0;
                string[] splitFileName = Path.GetFileName(dump).Split('_');
                uint width = Convert.ToUInt32(splitFileName[0]);
                uint height = Convert.ToUInt32(splitFileName[1]);
                ULT_TILE_FORMATS ultTileFormat;
                ULT_PIXELFORMAT ultSourcePixelFormat;
                Enum.TryParse(String.Concat("ULT_TILE_FORMAT_", splitFileName[2]), out ultTileFormat);
                Enum.TryParse(String.Concat("ULT_PIXEL_FORMAT_", splitFileName[3].Replace('.', '_')), out ultSourcePixelFormat);
                base.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock, ref pUserVirtualAddress, ref dataSize);
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Get MPO Caps");
            escapeCodeName = "ULT_GET_MPO_CAPS";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                       where ((string)c.Attribute("name") == escapeCodeName.ToString())
                       select c).FirstOrDefault();
            uint sourceId = Convert.ToUInt32(((from c in Element.Descendants("SourceId")
                                          select c).FirstOrDefault().Value));
            base.ULT_FW_Get_MPO_Caps(sourceId, ref stMpoCaps);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Get MPO Group Caps");
            escapeCodeName = "ULT_MPO_GROUP_CAPS";
            ULT_MPO_GROUP_CAPS[] stMpoGroupCaps= new ULT_MPO_GROUP_CAPS[stMpoCaps.uiNumCapabilityGroups];
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            uint sourceId = Convert.ToUInt32(((from c in Element.Descendants("SourceId")
                                               select c).FirstOrDefault().Value));
            for (uint i = 0; i < stMpoCaps.uiNumCapabilityGroups; i++)
            {
                base.ULT_FW_MPO_Group_Caps(sourceId, i, ref stMpoGroupCaps[i]);
            }
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Check MPO");
            escapeCodeName = "ULT_CHECK_MPO";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                       where ((string)c.Attribute("name") == escapeCodeName.ToString())
                       select c).FirstOrDefault();
           
            List<XElement> pipeElement = (from c in Element.Descendants("Pipe") select c).ToList();
            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];//[pipeElement.Count];
            for (int i=0; i< pipeElement.Count; i++)
            {
                List<XElement> plane = (from c in pipeElement[i].Descendants("Plane") select c).ToList();
                stCheckMpoSupportPathInfo[i].uiPlaneCount =Convert.ToUInt32(plane.Count);
                ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[plane.Count];
                ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];//[plane.Count];
                for(int j=0; j< plane.Count; j++)
                {
                    ULT_M_RECT rectCoordinates = new ULT_M_RECT() ;
                    stMPOPlaneAttributes[j] = new ULT_MPO_PLANE_ATTRIBUTES();
                    string planePath = (from c in plane[j].Descendants("Path") select c).FirstOrDefault().Value;
                    stCheckMpoSupportPlaneInfo[j].uiLayerIndex = Convert.ToUInt32(j);
                    stCheckMpoSupportPlaneInfo[j].bEnabled = Boolean.Parse((from c in plane[j].Descendants("Enabled") select c).FirstOrDefault().Value);
                    stCheckMpoSupportPlaneInfo[j].bIsAsyncMMIOFlip = Boolean.Parse((from c in plane[j].Descendants("IsAsyncMMIOFlip") select c).FirstOrDefault().Value);
                    ULT_PIXELFORMAT pixelFormat;
                    Enum.TryParse((from c in plane[j].Descendants("PixelFormat") select c).FirstOrDefault().Value, out pixelFormat);
                    stCheckMpoSupportPlaneInfo[j].eSBPixelFormat = pixelFormat;
                    uint MpoFlags = Convert.ToUInt32((from c in plane[j].Descendants("MPOFlags") select c).FirstOrDefault().Value);
                    string[] srcRectCoordinates = (from c in plane[j].Descendants("SourceRect") select c).FirstOrDefault().Value.Split(',');
                    rectCoordinates.left = Convert.ToUInt32(srcRectCoordinates[0]);
                    rectCoordinates.top = Convert.ToUInt32(srcRectCoordinates[1]);
                    rectCoordinates.bottom = Convert.ToUInt32(srcRectCoordinates[2]);
                    rectCoordinates.right = Convert.ToUInt32(srcRectCoordinates[3]);
                    stMPOPlaneAttributes[j].MPOSrcRect = rectCoordinates;
                    string[] destRectCoordinates = (from c in plane[j].Descendants("DestRect") select c).FirstOrDefault().Value.Split(',');
                    rectCoordinates.left = Convert.ToUInt32(destRectCoordinates[0]);
                    rectCoordinates.top = Convert.ToUInt32(destRectCoordinates[1]);
                    rectCoordinates.bottom = Convert.ToUInt32(destRectCoordinates[2]);
                    rectCoordinates.right = Convert.ToUInt32(destRectCoordinates[3]);
                    stMPOPlaneAttributes[j].MPODstRect = rectCoordinates;
                    string[] clipRectCoordinates = (from c in plane[j].Descendants("ClipRect") select c).FirstOrDefault().Value.Split(',');
                    rectCoordinates.left = Convert.ToUInt32(clipRectCoordinates[0]);
                    rectCoordinates.top = Convert.ToUInt32(clipRectCoordinates[1]);
                    rectCoordinates.bottom = Convert.ToUInt32(clipRectCoordinates[2]);
                    rectCoordinates.right = Convert.ToUInt32(clipRectCoordinates[3]);
                    stMPOPlaneAttributes[j].MPOClipRect = rectCoordinates;
                    ULT_MPO_ROTATION mpoRotation;
                    Enum.TryParse((from c in plane[j].Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
                    ULT_MPO_BLEND_VAL mpoBlendVal;
                    Enum.TryParse((from c in plane[j].Descendants("MPOBlend") select c).FirstOrDefault().Value, out mpoBlendVal);
                    ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
                    Enum.TryParse((from c in plane[j].Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
                    uint ycbcr = Convert.ToUInt32((from c in plane[j].Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value );
                    ULT_MPO_STEREO_FORMAT stereoFormat;
                    Enum.TryParse((from c in plane[j].Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);
                    ULT_MPO_STEREO_FLIP_MODE stereo;
                    Enum.TryParse((from c in plane[j].Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);
                    ULT_MPO_STRETCH_QUALITY stretchquality;
                    Enum.TryParse((from c in plane[j].Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);
                    stMPOPlaneAttributes[j].eMPORotation = mpoRotation;
                    stMPOPlaneAttributes[j].eMPOBlend = mpoBlendVal;
                    stMPOPlaneAttributes[j].eMPOVideoFormat = videoFormat;
                    stMPOPlaneAttributes[j].uiMPOYCbCrFlags = ycbcr;
                    stMPOPlaneAttributes[j].eMPOStereoFormat = stereoFormat;
                    stMPOPlaneAttributes[j].eMPOStereoFlipMode = stereo;
                    stMPOPlaneAttributes[j].eStretchQuality = stretchquality;
                    stMPOPlaneAttributes[j].DIRTYRECTS = new ULT_M_RECT[8];

                    stCheckMpoSupportPlaneInfo[j].stPlaneAttributes = stMPOPlaneAttributes[j];
                    ULT_SURFACE_MEM_OFFSET_INFO surfaceMemOffsetInfo = new ULT_SURFACE_MEM_OFFSET_INFO();
                    XElement surfaceMemoryOffsetInfo = (from c in plane[j].Descendants("SurfaceMemOffsetInfo") select c).FirstOrDefault();
                    ULT_SURFACE_MEMORY_TYPE surfaceMemType;
                    Enum.TryParse((from c in surfaceMemoryOffsetInfo.Descendants("SurfaceMemoryType") select c).FirstOrDefault().Value, out surfaceMemType);
                    surfaceMemOffsetInfo.eSurfaceMemType = surfaceMemType;
                    surfaceMemOffsetInfo.ulTiledXOffset = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("TiledXOffset") select c).FirstOrDefault().Value);
                    surfaceMemOffsetInfo.ulTiledYOffset = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("TiledYOffset") select c).FirstOrDefault().Value);
                    surfaceMemOffsetInfo.ulTiledUVXOffset = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("TiledUVXOffset") select c).FirstOrDefault().Value);
                    surfaceMemOffsetInfo.ulTiledUVYOffset = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("TiledUVYOffset") select c).FirstOrDefault().Value);
                    surfaceMemOffsetInfo.ulUVDistance = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("UVDistance") select c).FirstOrDefault().Value);
                    surfaceMemOffsetInfo.ulAuxDistance = Convert.ToUInt32((from c in surfaceMemoryOffsetInfo.Descendants("AuxDistance") select c).FirstOrDefault().Value);
                    stCheckMpoSupportPlaneInfo[j].stSurfaceMemInfo = surfaceMemOffsetInfo;
                }
                stCheckMpoSupportPathInfo[i].stMPOPlaneInfo = stCheckMpoSupportPlaneInfo;
            }
            bool supported = false;
            uint failureReason = 0;
            //stCheckMpoSupportPathInfo[2].stMPOPlaneInfo = new SB_MPO_CHECKMPOSUPPORT_PLANE_INFO[12];
            CHECKMPOSUPPORT_RETURN_INFO stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            uint numPaths = Convert.ToUInt32((from c in Element.Descendants("NumPaths") select c).FirstOrDefault().Value);
            base.ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Set Source Address MPO");
            escapeCodeName = "ULT_SET_SRC_ADD_MPO";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            uint numPlanes = Convert.ToUInt32((from c in Element.Descendants("NumPlanes") select c).FirstOrDefault().Value);
            uint sourceId = Convert.ToUInt32((from c in Element.Descendants("SourceId") select c).FirstOrDefault().Value);
            string sourceFlags = (from c in Element.Descendants("SourceAddressFlags")
                                  select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            List<XElement> planeElement = (from c in Element.Descendants("Plane") select c).ToList();
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[planeElement.Count];
            for (int j = 0; j < planeElement.Count; j++)
            {
                ULT_M_RECT rectCoordinates = new ULT_M_RECT();
                mpoFlipPlaneInfo[j].uiLayerIndex = Convert.ToUInt32(j);
                mpoFlipPlaneInfo[j].bEnabled = Boolean.Parse((from c in planeElement[j].Descendants("Enabled") select c).FirstOrDefault().Value);
                mpoFlipPlaneInfo[j].bAffected = Boolean.Parse((from c in planeElement[j].Descendants("Affected") select c).FirstOrDefault().Value);
                ULT_MPO_PLANE_ATTRIBUTES mpoPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES();
                mpoPlaneAttributes.uiMPOFlags = Convert.ToUInt32((from c in planeElement[j].Descendants("MPOFlags") select c).FirstOrDefault().Value);
                string[] srcRectCoordinates = (from c in planeElement[j].Descendants("SourceRect") select c).FirstOrDefault().Value.Split(',');
                rectCoordinates.left = Convert.ToUInt32(srcRectCoordinates[0]);
                rectCoordinates.top = Convert.ToUInt32(srcRectCoordinates[1]);
                rectCoordinates.bottom = Convert.ToUInt32(srcRectCoordinates[2]);
                rectCoordinates.right = Convert.ToUInt32(srcRectCoordinates[3]);
                mpoPlaneAttributes.MPOSrcRect = rectCoordinates;
                string[] destRectCoordinates = (from c in planeElement[j].Descendants("DestRect") select c).FirstOrDefault().Value.Split(',');
                rectCoordinates.left = Convert.ToUInt32(destRectCoordinates[0]);
                rectCoordinates.top = Convert.ToUInt32(destRectCoordinates[1]);
                rectCoordinates.bottom = Convert.ToUInt32(destRectCoordinates[2]);
                rectCoordinates.right = Convert.ToUInt32(destRectCoordinates[3]);
                mpoPlaneAttributes.MPODstRect = rectCoordinates;
                string[] clipRectCoordinates = (from c in planeElement[j].Descendants("ClipRect") select c).FirstOrDefault().Value.Split(',');
                rectCoordinates.left = Convert.ToUInt32(clipRectCoordinates[0]);
                rectCoordinates.top = Convert.ToUInt32(clipRectCoordinates[1]);
                rectCoordinates.bottom = Convert.ToUInt32(clipRectCoordinates[2]);
                rectCoordinates.right = Convert.ToUInt32(clipRectCoordinates[3]);
                mpoPlaneAttributes.MPOClipRect = rectCoordinates;
                ULT_MPO_ROTATION mpoRotation;
                Enum.TryParse((from c in planeElement[j].Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
                ULT_MPO_BLEND_VAL mpoBlendVal;
                Enum.TryParse((from c in planeElement[j].Descendants("MPOBlend") select c).FirstOrDefault().Value, out mpoBlendVal);
                ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
                Enum.TryParse((from c in planeElement[j].Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
                uint ycbcr = Convert.ToUInt32((from c in planeElement[j].Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
                ULT_MPO_STEREO_FORMAT stereoFormat;
                Enum.TryParse((from c in planeElement[j].Descendants("MPOStereoFormat") select c).FirstOrDefault().Value, out stereoFormat);
                ULT_MPO_STEREO_FLIP_MODE stereo;
                Enum.TryParse((from c in planeElement[j].Descendants("MPOStereoFlipMode") select c).FirstOrDefault().Value, out stereo);
                ULT_MPO_STRETCH_QUALITY stretchquality;
                Enum.TryParse((from c in planeElement[j].Descendants("StretchQuality") select c).FirstOrDefault().Value, out stretchquality);
                mpoPlaneAttributes.eMPORotation = mpoRotation;
                mpoPlaneAttributes.eMPOBlend = mpoBlendVal;
                mpoPlaneAttributes.eMPOVideoFormat = videoFormat;
                mpoPlaneAttributes.uiMPOYCbCrFlags = ycbcr;
                mpoPlaneAttributes.eMPOStereoFormat = stereoFormat;
                mpoPlaneAttributes.eMPOStereoFlipMode = stereo;
                mpoPlaneAttributes.eStretchQuality = stretchquality;
                mpoFlipPlaneInfo[j].stPlaneAttributes = mpoPlaneAttributes;
                UInt64 hAlloc = new UInt64();
                mpoFlipPlaneInfo[j].hAllocation = hAlloc;
            }
            base.ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);

        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Free Resource");
            base.ULT_FW_Free_Resource(pGmmBlock);
        }
        [Test(Type = TestType.Method, Order = 9)]
        public void TestStep9()
        {
            Log.Message(true, "Disable ULT Mode");
            base.EnableDFT(false);
        }    
    }
}



