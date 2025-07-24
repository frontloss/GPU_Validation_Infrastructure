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

    public class SB_ULT_MMIO_Flip : SB_ULT_Base
    {
        DisplayConfig displayConfig;
        XDocument ultParserDoc = null;
        string dumpFilepath = string.Empty;
        UInt64 pGmmBlock = 0;
        IntPtr pUserVirtualAddress;
        uint fileIndex;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            Log.Message(true, "Set Config as ED EDP, DP");
            displayConfig = new DisplayConfig()
            {
                ConfigType = DisplayConfigType.ED,
                PrimaryDisplay = DisplayType.EDP,
                SecondaryDisplay = DisplayType.HDMI
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
            Log.Message(true, "Create Resource");
            ulong dataSize = 0;
            string escapeCodeName = "ULT_CREATE_RESOURCE";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            dumpFilepath = (from c in Element.Descendants("DumpFilePath")
                                   select c).FirstOrDefault().Value;
            fileIndex =Convert.ToUInt32((from c in Element.Descendants("FileIndex")
                         select c).FirstOrDefault().Value);
            string[] splitFileName =Path.GetFileName(dumpFilepath).Split('_');
            uint width = Convert.ToUInt32(splitFileName[0]);
            uint height = Convert.ToUInt32(splitFileName[1]);
            ULT_TILE_FORMATS ultTileFormat;
            ULT_PIXELFORMAT ultSourcePixelFormat;
            Enum.TryParse(String.Concat("ULT_TILE_FORMAT_", splitFileName[2]), out ultTileFormat);
            Enum.TryParse(String.Concat("ULT_PIXEL_FORMAT_", splitFileName[3].Replace('.', '_')), out ultSourcePixelFormat);

            
            base.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock, ref pUserVirtualAddress, ref dataSize);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            Log.Message(true, "Set Source Address");
            string escapeCodeName = "ULT_SET_SRC_ADDRESS";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
            uint sourceId = Convert.ToUInt32(((from c in Element.Descendants("SourceId")
                                               select c).FirstOrDefault().Value));
            string sourceFlags = (from c in Element.Descendants("SourceAddressFlags")
                                  select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags;
            Enum.TryParse(sourceFlags, out sourceAddressFlags);
            Log.Verbose("Get dump data from bin file into byte array");
            string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
            byte[] array = File.ReadAllBytes(files[fileIndex]);
            Marshal.Copy(array, 0, pUserVirtualAddress, array.Length);
            Int64 a1 = Marshal.ReadByte(pUserVirtualAddress);
            IntPtr temp = new IntPtr(pUserVirtualAddress.ToInt64() + 1);
            Int64 a2 = Marshal.ReadByte(temp);
            IntPtr temp1 = new IntPtr(pUserVirtualAddress.ToInt64() + 2);
            Int64 a21 = Marshal.ReadByte(temp1);
            IntPtr temp2 = new IntPtr(pUserVirtualAddress.ToInt64() + 3);
            Int64 a22 = Marshal.ReadByte(temp2);
            IntPtr temp3 = new IntPtr(pUserVirtualAddress.ToInt64() + 4);
            Int64 a23 = Marshal.ReadByte(temp3);
            base.ULT_FW_Set_Source_Address(pGmmBlock, sourceId, 8, sourceAddressFlags);

            System.Threading.Thread.Sleep(5000);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Disable ULT Mode");
            base.EnableDFT(false);
           
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Free Resource");
            base.ULT_FW_Free_Resource(pGmmBlock);
        }    
    }
}



