using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.IO;
using System.Xml.Linq;
using System.Xml.Serialization;
using System.Windows.Forms;
using System.Xml;
using System.Runtime.InteropServices;

namespace MPOApp
{
    class MPO
    {
        XDocument ultParserDoc = null;
        string escapeCodeName;
        ULT_MPO_CAPS stMpoCaps = new ULT_MPO_CAPS();
        string dumpFilepath = string.Empty;
        List<UInt64> pGmmBlockList = new List<UInt64>();
        List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
        uint fileIndex;

        public const int MAX_PLANES = 13;
        public const int MAX_PIPES = 3;
        public void Start()
        {
            Console.WriteLine("Hi Hi");
            while (true)
            {

                ULT_SET_SRC_ADD_MPO_ARG abc123 = new ULT_SET_SRC_ADD_MPO_ARG();
                int sizeofStrrr1s3 = Marshal.SizeOf(abc123);

                SB_MPO_CHECKMPOSUPPORT_PATH_INFO abc12 = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO();
                int sizeofStrrr1s = Marshal.SizeOf(abc12);


                SB_MPO_CHECKMPOSUPPORT_ARGS abc = new SB_MPO_CHECKMPOSUPPORT_ARGS();
                int sizeofStrrr = Marshal.SizeOf(abc);

                ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO ab = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO();
                int lane = Marshal.SizeOf(ab);

                ULT_MPO_PLANE_ATTRIBUTES abc1 = new ULT_MPO_PLANE_ATTRIBUTES();
                int sizeofStrrr1 = Marshal.SizeOf(abc1);


                ULT_SURFACE_MEM_OFFSET_INFO abc2 = new ULT_SURFACE_MEM_OFFSET_INFO();
                int sizeofStrrr2 = Marshal.SizeOf(abc2);

                
                

                Console.WriteLine("Enter the user input");
                Console.WriteLine("0: MMIO Flip.");
                Console.WriteLine("1: Single Plane MPO.");
                Console.WriteLine("2: Two Plane MPO with Clipping.");
                Console.WriteLine("3: Three Plane MPO with clipping.");
                Console.WriteLine("4: Source Buffer size not equal to destination.");
                Console.WriteLine("5: Source Buffer size less than destination -> Scaling case.");
                Console.WriteLine("6: Single Plane MPO. Down Scaling.");
                Console.WriteLine("7: Two Plane MPO. Scaling + Non-Scaling.");
                Console.WriteLine("8: NV12 Content.");
                Console.WriteLine("9: Alpha Blending.");
                Console.WriteLine("10: Hardware Rotation.");
                Console.WriteLine("11: Render Compression.");
                Console.WriteLine("13: CNL Specific : 4 plane + HW Cursor");
                Console.WriteLine("14: CNL Specific :HFLIP with Rotation");
                Console.WriteLine("15: CNL Specific :VFLIP with Rotation");
                Console.WriteLine("16: CNL Specific :HFLIP+VFLIP with Rotation");
                Console.WriteLine("17: CNL Specific :P0xx");
                Console.WriteLine("18: CNL Specific :Scalar Test");
                string st = Console.ReadLine();
                int output;
                int.TryParse(st, out output);

                if (output > 18)
                    break;

                if (output == 6)
                {
                    output = 12;
                   
                    ultParserDoc = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), "\\Config\\ULTParams" + output + ".xml"));

                    Console.WriteLine("Enable ULT Mode");
                    EnableULT(true);
                    EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);

                    GetMPOCaps();
                    GetMPOGroupCaps();
                    CheckMPO();
                    CreateResource(output);
                    SetSourceAddressMPO(output);
                    FreeResource();
                    DisableULT();

                    output = 6;
                }
                else if (output == 0)
                {
                    ultParserDoc = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), "\\Config\\ULTParams" + output + ".xml"));

                    Console.WriteLine("Enable ULT Mode");
                    EnableULT(true);
                    EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
                    
                    CreateResource(output);
                    SetSourceAddress(output);
                    FreeResource();
                    DisableULT();
                }
                else
                {
                    ultParserDoc = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), "\\Config\\ULTParams" + output + ".xml"));

                    Console.WriteLine("Enable ULT Mode");

                    EnableULT(true);
                    EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_MPOFLIP);

                    GetMPOCaps();
                    GetMPOGroupCaps();
                    CheckMPO();
                    CreateResource(output);
                    SetSourceAddressMPO(output);
                    FreeResource();
                    DisableULT();

                    if (output == 6)
                    {
                        MessageBox.Show("Apply Resolution");
                        Console.WriteLine("Press any key after resolution has been changed");
                        string key = Console.ReadLine();
                    }
                }
            }
        }
        private void EnableULT(bool status)
        {
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.bEnableULT = status;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) -16 ;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }
        private void EnableFeature(bool status, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE featureType)
        {
            ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS ult_Esc_Args = new ULT_ESC_ENABLE_DISABLE_FEATURE_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE;
            ult_Esc_Args.bEnableFeature = status;
            ult_Esc_Args.eFeatureEnable = featureType;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_DISABLE_FEATURE, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }
        public void GetMPOCaps()
        {
            Console.WriteLine( "Get MPO Caps");
            escapeCodeName = "ULT_GET_MPO_CAPS";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            uint sourceId = Convert.ToUInt32(((from c in Element.Descendants("SourceId")
                                               select c).FirstOrDefault().Value));
            ULT_FW_Get_MPO_Caps(sourceId, ref stMpoCaps);
        }

        public void GetMPOGroupCaps()
        {
            Console.WriteLine("Get MPO Group Caps");
            escapeCodeName = "ULT_MPO_GROUP_CAPS";
            ULT_MPO_GROUP_CAPS[] stMpoGroupCaps = new ULT_MPO_GROUP_CAPS[stMpoCaps.uiNumCapabilityGroups];
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            uint sourceId = Convert.ToUInt32(((from c in Element.Descendants("SourceId")
                                               select c).FirstOrDefault().Value));
            for (uint i = 0; i < stMpoCaps.uiNumCapabilityGroups; i++)
            {
                ULT_FW_MPO_Group_Caps(sourceId, i, ref stMpoGroupCaps[i]);
            }
        }

        public void CheckMPO()
        {
            Console.WriteLine("Check MPO");
            escapeCodeName = "ULT_CHECK_MPO";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();

            List<XElement> pipeElement = (from c in Element.Descendants("Pipe") select c).ToList();
            SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] stCheckMpoSupportPathInfo = new SB_MPO_CHECKMPOSUPPORT_PATH_INFO[MAX_PIPES];//[pipeElement.Count];
            for (int i = 0; i < pipeElement.Count; i++)
            {
                List<XElement> plane = (from c in pipeElement[i].Descendants("Plane") select c).ToList();
                stCheckMpoSupportPathInfo[i].uiPlaneCount = Convert.ToUInt32(plane.Count);
                // stCheckMpoSupportPathInfo[i].ucPipeIndex = (char)i;
                //MessageBox.Show("Enter Windows monitor ID of primary Display");
                //uint st = Convert.ToUInt32( Console.ReadLine());
                //stCheckMpoSupportPathInfo[i].ulDisplayUID = st; ;
                //stCheckMpoSupportPathInfo[i].ulDisplayUID = CurrentConfig.EnumeratedDisplays[0].WindowsMonitorID; 
                ULT_MPO_PLANE_ATTRIBUTES[] stMPOPlaneAttributes = new ULT_MPO_PLANE_ATTRIBUTES[plane.Count];
                ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[] stCheckMpoSupportPlaneInfo = new ULT_MPO_CHECKMPOSUPPORT_PLANE_INFO[MAX_PLANES];//[plane.Count];
                for (int j = 0; j < plane.Count; j++)
                {
                    ULT_M_RECT rectCoordinates = new ULT_M_RECT();
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
                    rectCoordinates.bottom = Convert.ToUInt32(srcRectCoordinates[3]);
                    rectCoordinates.right = Convert.ToUInt32(srcRectCoordinates[2]);
                    stMPOPlaneAttributes[j].MPOSrcRect = rectCoordinates;
                    stMPOPlaneAttributes[j].uiMPOFlags = MpoFlags;
                    string[] destRectCoordinates = (from c in plane[j].Descendants("DestRect") select c).FirstOrDefault().Value.Split(',');
                    rectCoordinates.left = Convert.ToUInt32(destRectCoordinates[0]);
                    rectCoordinates.top = Convert.ToUInt32(destRectCoordinates[1]);
                    rectCoordinates.bottom = Convert.ToUInt32(destRectCoordinates[3]);
                    rectCoordinates.right = Convert.ToUInt32(destRectCoordinates[2]);
                    stMPOPlaneAttributes[j].MPODstRect = rectCoordinates;
                    string[] clipRectCoordinates = (from c in plane[j].Descendants("ClipRect") select c).FirstOrDefault().Value.Split(',');
                    rectCoordinates.left = Convert.ToUInt32(clipRectCoordinates[0]);
                    rectCoordinates.top = Convert.ToUInt32(clipRectCoordinates[1]);
                    rectCoordinates.bottom = Convert.ToUInt32(clipRectCoordinates[3]);
                    rectCoordinates.right = Convert.ToUInt32(clipRectCoordinates[2]);
                    stMPOPlaneAttributes[j].MPOClipRect = rectCoordinates;
                    ULT_MPO_ROTATION mpoRotation;
                    Enum.TryParse((from c in plane[j].Descendants("MPORotation") select c).FirstOrDefault().Value, out mpoRotation);
                    ULT_MPO_BLEND_VAL mpoBlendVal;
                    Enum.TryParse((from c in plane[j].Descendants("MPOBlend") select c).FirstOrDefault().Value, out mpoBlendVal);
                    ULT_MPO_VIDEO_FRAME_FORMAT videoFormat;
                    Enum.TryParse((from c in plane[j].Descendants("MPOVideoFormat") select c).FirstOrDefault().Value, out videoFormat);
                    uint ycbcr = Convert.ToUInt32((from c in plane[j].Descendants("MPOYCbCrFlags") select c).FirstOrDefault().Value);
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
            ULT_FW_Check_MPO(stCheckMpoSupportPathInfo, numPaths, 1, ref supported, ref failureReason, ref stMPOCheckSuppReturnInfo);
            if (supported == false)
            {
                Console.WriteLine("Check MPO-Failed-MPO Not supported on plane index {0}", stMPOCheckSuppReturnInfo.uiValue);
            }
        }

        public void CreateResource(int count)
        {
            //Log.Message(true, "Create resource for 1 planes");
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
                UInt64 pGmmBlock_temp = 0;
                IntPtr pUserVirtualAddress_temp = default(IntPtr);
                string[] splitPath = dump.Split('\\');
                string[] splitFileName = splitPath[1].Split('_');
                uint width = Convert.ToUInt32(splitFileName[0]);
                uint height = Convert.ToUInt32(splitFileName[1]);
                ULT_TILE_FORMATS ultTileFormat;
                ULT_PIXELFORMAT ultSourcePixelFormat;
                bool AuxSurf = false;
                UInt64 SurfaceSize = 0;
                Enum.TryParse(String.Concat("ULT_TILE_FORMAT_", splitFileName[2]), out ultTileFormat);
                if (splitFileName[3] == "NV12")
                    ultSourcePixelFormat = ULT_PIXELFORMAT.SB_NV12YUV420;
                else if (splitFileName[3] == "P010")
                    ultSourcePixelFormat = ULT_PIXELFORMAT.SB_P010YUV420;
                else if (splitFileName[3] == "P012")
                    ultSourcePixelFormat = ULT_PIXELFORMAT.SB_P012YUV420;
                else if (splitFileName[3] == "P016")
                    ultSourcePixelFormat = ULT_PIXELFORMAT.SB_P016YUV420;
                else
                    ultSourcePixelFormat = ULT_PIXELFORMAT.SB_B8G8R8A8;
                    //Enum.TryParse(String.Concat("ULT_PIXEL_FORMAT_", splitFileName[3].Replace('.', '_')), out ultSourcePixelFormat);

                if (count == 11)
                    AuxSurf = true;
                string filepath = Directory.GetCurrentDirectory() + "\\" + dump;//string.Concat(dump, "\\rc_NEW.bin");
                byte[] array = File.ReadAllBytes(filepath);

                ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, AuxSurf, ref pGmmBlock_temp, ref pUserVirtualAddress_temp, ref SurfaceSize);
                pGmmBlockList.Add(pGmmBlock_temp);
                pUserVirtualAddressList.Add(pUserVirtualAddress_temp);

                int arrLength = Math.Min(array.Length, (int)SurfaceSize); //(int)SurfaceSize;//
                //string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
                //if (splitFileName[3] == "NV12")
                //    arrLength = 2334720;
                //if (count == 11)
                //    arrLength = 0x7F8001;
                //Marshal.Copy(array, 0, pUserVirtualAddress_temp, arrLength);
                Marshal.Copy(array, 0, pUserVirtualAddress_temp, arrLength);
            }
        }
        public void SetSourceAddress(int output)
        {
            Console.WriteLine("Set Source Address");

            ULT_FW_Set_Source_Address(pGmmBlockList[0], 0, 0, ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync);

            Console.WriteLine("press any key to continue.");
            string st = Console.ReadLine();
        }
        public void SetSourceAddressMPO(int output)
        {
            Console.WriteLine("Set Source Address MPO");
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
            MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo = new MPO_FLIP_PLANE_INFO[MAX_PLANES];//[planeElement.Count];
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
                rectCoordinates.bottom = Convert.ToUInt32(srcRectCoordinates[3]);
                rectCoordinates.right = Convert.ToUInt32(srcRectCoordinates[2]);
                mpoPlaneAttributes.MPOSrcRect = rectCoordinates;
                string[] destRectCoordinates = (from c in planeElement[j].Descendants("DestRect") select c).FirstOrDefault().Value.Split(',');
                rectCoordinates.left = Convert.ToUInt32(destRectCoordinates[0]);
                rectCoordinates.top = Convert.ToUInt32(destRectCoordinates[1]);
                rectCoordinates.bottom = Convert.ToUInt32(destRectCoordinates[3]);
                rectCoordinates.right = Convert.ToUInt32(destRectCoordinates[2]);
                mpoPlaneAttributes.MPODstRect = rectCoordinates;
                string[] clipRectCoordinates = (from c in planeElement[j].Descendants("ClipRect") select c).FirstOrDefault().Value.Split(',');
                rectCoordinates.left = Convert.ToUInt32(clipRectCoordinates[0]);
                rectCoordinates.top = Convert.ToUInt32(clipRectCoordinates[1]);
                rectCoordinates.bottom = Convert.ToUInt32(clipRectCoordinates[3]);
                rectCoordinates.right = Convert.ToUInt32(clipRectCoordinates[2]);
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
                mpoFlipPlaneInfo[j].stPlaneAttributes.DIRTYRECTS = new ULT_M_RECT[8];
                //stMPOPlaneAttributes[j].DIRTYRECTS = new M_RECT[8];
                //IntPtr hAlloc = IntPtr.Zero;
                mpoFlipPlaneInfo[j].hAllocation = pGmmBlockList[j];
            }

            if (output == 6)
            {
                MessageBox.Show("Apply Native Resolution");
                Console.WriteLine("Press any key after Resolution has been changed");
                string key = Console.ReadLine();
            }

            ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);

            if (output == 5)
            {
                int loopCount = 8;
                for (int i = 1; i <= loopCount; i++)
                {
                    System.Threading.Thread.Sleep(500);

                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.left -= 50;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.top -= 15;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.right += 50;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.bottom += 10;

                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.left -= 50;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.top -= 15;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.right += 50;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.bottom += 10;
                    ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                }

                System.Threading.Thread.Sleep(500);

                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.left = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.top = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.right = 1920;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.bottom = 1080;

                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.left = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.top = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.right = 1920;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.bottom = 1080;
                ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
            }

            if (output == 4)
            {
                int loopCount = 9;
                for (int i = 1; i <= loopCount; i++)
                {
                    System.Threading.Thread.Sleep(500);

                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.left += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.top += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.right += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.bottom += 30;

                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.left += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.top += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.right += 30;
                    mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.bottom += 30;
                    ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
                }
                System.Threading.Thread.Sleep(500);

                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.left = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.top = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.right = 1360;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPODstRect.bottom = 768;

                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.left = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.top = 0;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.right = 1360;
                mpoFlipPlaneInfo[0].stPlaneAttributes.MPOClipRect.bottom = 768;
                ULT_FW_Set_Source_Address_MPO(mpoFlipPlaneInfo, numPlanes, sourceAddressFlags, sourceId);
            }
            Console.WriteLine("press any key to continue.");
            string st = Console.ReadLine();
        }
        public void FreeResource()
        {
            Console.WriteLine("Free Resource");
            foreach (UInt64 pgmm in pGmmBlockList)
                ULT_FW_Free_Resource(pgmm);

            pGmmBlockList.Clear();
            pUserVirtualAddressList.Clear();
        }
        public void DisableULT()
        {
            Console.WriteLine("Disable ULT Mode");
            EnableULT(false);
        }
        private bool ULT_FW_Get_MPO_Caps(uint sourceID, ref ULT_MPO_CAPS argMpoCaps)
        {
            ULT_ESC_MPO_CAPS_ARGS ult_Esc_Args = new ULT_ESC_MPO_CAPS_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_Framework u = new ULT_Framework();
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_GET_MPO_CAPS, ult_Esc_Args);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                argMpoCaps = ult_Esc_Args.stMPOCaps;
                return true;
            }
            return false;
        }
        private bool ULT_FW_MPO_Group_Caps(uint sourceID, uint groupIndex, ref ULT_MPO_GROUP_CAPS argMpoGroupCaps)
        {
            ULT_MPO_GROUP_CAPS_ARGS ult_Esc_Args = new ULT_MPO_GROUP_CAPS_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS;
            ult_Esc_Args.ulVidpnSourceID = sourceID;
            ult_Esc_Args.uiGroupIndex = groupIndex;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_MPO_GROUP_CAPS, ult_Esc_Args);
            ULT_Framework u = new ULT_Framework();
            //if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            //    Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                argMpoGroupCaps = ult_Esc_Args.stMPOGroupCaps;
                return true;
            }
            return false;
        }
        internal bool ULT_FW_Check_MPO(SB_MPO_CHECKMPOSUPPORT_PATH_INFO[] sbMpoCheckMpoSupportPathInfo, uint numPaths, uint config, ref bool supported, ref uint failureReason, ref CHECKMPOSUPPORT_RETURN_INFO checkMpoSupportReturnInfo)
        {
            SB_MPO_CHECKMPOSUPPORT_ARGS ult_Esc_Args = new SB_MPO_CHECKMPOSUPPORT_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.dwSourceID = 0;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CHECK_MPO;
            ult_Esc_Args.stCheckMPOPathInfo = sbMpoCheckMpoSupportPathInfo;
            ult_Esc_Args.ulNumPaths = numPaths;
            ult_Esc_Args.ulConfig = config;
            ult_Esc_Args.stMPOCheckSuppReturnInfo = new CHECKMPOSUPPORT_RETURN_INFO();
            ULT_Framework u = new ULT_Framework();
            //for (int i = 0; i < 8; i++)
            //{
            //    ult_Esc_Args.stCheckMPOPathInfo[1].stMPOPlaneInfo[0].stPlaneAttributes.DIRTYRECTS[i] = new M_RECT();
            //}

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CHECK_MPO, ult_Esc_Args);

            //if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            //    Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                failureReason = ult_Esc_Args.ulFailureReason;
                supported = ult_Esc_Args.bSupported;
                checkMpoSupportReturnInfo = ult_Esc_Args.stMPOCheckSuppReturnInfo;
                return true;
            }
            return false;
        }
        private bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format, bool AuxSurf, ref UInt64 pGmmBlock, ref IntPtr pUserVirtualAddress, ref UInt64 surfaceSize)
        {
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = AuxSurf;
            ULT_Framework u = new ULT_Framework();
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args);

            //if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            //    Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                pGmmBlock = ult_Esc_Args.pGmmBlock;
                pUserVirtualAddress = (IntPtr)ult_Esc_Args.pUserVirtualAddress;
                surfaceSize = ult_Esc_Args.u64SurfaceSize;
                return true;
            }
            return false;
        }

        protected bool ULT_FW_Free_Resource(UInt64 pGmmBlock)
        {
            ULT_FREE_RES_ARGS ult_Esc_Args = new ULT_FREE_RES_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_FREE_RESOURCE;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ULT_Framework u = new ULT_Framework();
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args);

            //if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            //    Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                Console.WriteLine("Freed the resource");
                return true;
            }
            return false;
        }
        internal bool ULT_FW_Set_Source_Address(UInt64 pGmmBlock, uint sourceID, uint dataSize, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            ULT_ESC_SET_SRC_ADD_ARGS ult_Esc_Args = new ULT_ESC_SET_SRC_ADD_ARGS();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulSrcID = sourceID;
            ult_Esc_Args.ulDataSize = 0x7f8000;//dataSize;
            ult_Esc_Args.Flags = Flag;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args);
            
            ULT_Framework u = new ULT_Framework();
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                return true;
            }
            return false;
        }
        internal bool ULT_FW_Set_Source_Address_MPO(MPO_FLIP_PLANE_INFO[] mpoFlipPlaneInfo, uint numPlanes, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag, uint sourceId)
        {
            ULT_SET_SRC_ADD_MPO_ARG ult_Esc_Args = new ULT_SET_SRC_ADD_MPO_ARG();
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO;
            ult_Esc_Args.stDxgkMPOPlaneArgs = mpoFlipPlaneInfo;
            ult_Esc_Args.ulNumPlanes = numPlanes;
            ult_Esc_Args.ulFlags = Flag;
            ult_Esc_Args.dwSourceID = sourceId;
            ULT_Framework u = new ULT_Framework();
            int sizeofsetsource = Marshal.SizeOf(ult_Esc_Args);

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADD_MPO, ult_Esc_Args);

            //if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
            //    Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            if (!u.SetMethod(escapeParams))
                Console.WriteLine("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                return true;
            }
            return false;
        }

    }
    class MPOApp
    {
       
        static void Main(string[] args)
        {
            MPO mpo = new MPO();
            mpo.Start();
            Console.ReadLine();
        }
    }
}
