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
using System.Threading;
using System.Diagnostics;
using System.Windows.Forms;
namespace Intel.VPG.Display.Automation
{
    class SB_VRR_GenerateFlip:SB_VRR_GenerateFlip_Base
    {
        [DllImport("Kernel32.dll", CallingConvention = CallingConvention.Winapi)]
        private static extern void GetSystemTimePreciseAsFileTime(out long filetime);
               
        protected XDocument ultParserDoc = null;
        protected string dumpFilepath = string.Empty;
        protected uint sourceId = 0;
        UInt64 pGmmBlock = 0;
        UInt64 pGmmBlock1 = 0;
        UInt64 pGmmBlock2 = 0;
        protected List<UInt64> pGmmblockList = new List<UInt64>();
        IntPtr pUserVirtualAddress;
        IntPtr pUserVirtualAddress1;
        IntPtr pUserVirtualAddress2;
        protected List<IntPtr> pUserVirtualAddressList = new List<IntPtr>();
        uint fileIndex;

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplicationManager.VerifyTDR = false;
            ultParserDoc = XDocument.Load(string.Concat(Directory.GetCurrentDirectory(), "\\ULTParams.xml"));            
            //if its extended mode, assume to generate flips on secondary display
            if (base.CurrentConfig.ConfigType == DisplayConfigType.ED)
                sourceId = 1;
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            Log.Message(true, "Enable ULT Mode");
            base.EnableDFT(true);
            base.EnableFeature(true, ULT_ESC_ENABLE_DISABLE_ULT_FEATURE.ULT_FEATURE_PRIVATE_FLIP);
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
            
            dumpFilepath = string.Concat(base.ApplicationManager.ApplicationSettings.ULTDumpFiles, "\\FlipDumpData");
            dumpFilepath = Directory.GetDirectories(dumpFilepath).FirstOrDefault();
            fileIndex = Convert.ToUInt32((from c in Element.Descendants("FileIndex")
                                          select c).FirstOrDefault().Value);
            Log.Message("the file index is {0}", fileIndex);
            string[] splitFileName = Path.GetFileName(dumpFilepath).Split('_');
            uint width = Convert.ToUInt32(splitFileName[0]);
            uint height = Convert.ToUInt32(splitFileName[1]);
            ULT_TILE_FORMATS ultTileFormat;
            ULT_PIXELFORMAT ultSourcePixelFormat;
            Enum.TryParse(String.Concat("ULT_TILE_FORMAT_", splitFileName[2]), out ultTileFormat);
            Enum.TryParse(String.Concat("ULT_PIXEL_FORMAT_", splitFileName[3].Replace('.', '_')), out ultSourcePixelFormat);


            base.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock, ref pUserVirtualAddress, ref dataSize);
            base.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock1, ref pUserVirtualAddress1, ref dataSize);
            base.ULT_FW_Create_Resource(width, height, ultSourcePixelFormat, ultTileFormat, false, ref pGmmBlock2, ref pUserVirtualAddress2, ref dataSize);

            pGmmblockList.Add(pGmmBlock);
            pGmmblockList.Add(pGmmBlock1);
            pGmmblockList.Add(pGmmBlock2);

            pUserVirtualAddressList.Add(pUserVirtualAddress);
            pUserVirtualAddressList.Add(pUserVirtualAddress1);
            pUserVirtualAddressList.Add(pUserVirtualAddress2);

        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Set Source Address");
            string escapeCodeName = "ULT_SET_SRC_ADDRESS";
            XElement Element = (from c in ultParserDoc.Elements("ULTFrameworkParams").Descendants("ULTEscapeCode")
                                where ((string)c.Attribute("name") == escapeCodeName.ToString())
                                select c).FirstOrDefault();
                        
            string sourceFlags = (from c in Element.Descendants("SourceAddressFlags")
                                  select c).FirstOrDefault().Value;
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags= ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipImmediate;
            //Enum.TryParse(sourceFlags, out sourceAddressFlags);
            Log.Verbose("Get dump data from bin file into byte array");

            string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
            for (int i = 0; i < files.Count(); i++)
            {
                byte[] array = File.ReadAllBytes(files[i]);
                Marshal.Copy(array, 0, pUserVirtualAddressList[i], array.Length);
            }
            Int64 a1 = Marshal.ReadByte(pUserVirtualAddress);
            IntPtr temp = new IntPtr(pUserVirtualAddress.ToInt64() + 1);
            Int64 a2 = Marshal.ReadByte(temp);
            IntPtr temp1 = new IntPtr(pUserVirtualAddress.ToInt64() + 2);
            Int64 a21 = Marshal.ReadByte(temp1);
            IntPtr temp2 = new IntPtr(pUserVirtualAddress.ToInt64() + 3);
            Int64 a22 = Marshal.ReadByte(temp2);
            IntPtr temp3 = new IntPtr(pUserVirtualAddress.ToInt64() + 4);
            Int64 a23 = Marshal.ReadByte(temp3);

            TimeSpan time = DateTime.Now.TimeOfDay;
            Log.Message(true, "{0} :{1} : {2} :{3} -(Flip Start)", time.Hours, time.Minutes, time.Seconds, time.Milliseconds);

            string arguments = "Dxgkrnl -DWM Core -Trace.bat";
            int argDelay = 2;
            ProcessStartInfo processStartInfo = new ProcessStartInfo();
            processStartInfo.CreateNoWindow = true;
            processStartInfo.WindowStyle = ProcessWindowStyle.Normal;
            processStartInfo.FileName = arguments;
            Process process = new Process();
            process.StartInfo = processStartInfo;
            process.Start();

            if (!argDelay.Equals(0))
                process.WaitForExit(argDelay * 1000);

            
            for (int j = 0; j < 25; j++)
            {
                for (int i = 0; i < files.Count(); i++)
                {                    
                    base.ULT_FW_Set_Source_Address(pGmmblockList[i], sourceId, 8, sourceAddressFlags);
                    WaitMilliSeconds(13);
                }
            }
            SendKeys.SendWait("a");
            TimeSpan timeEnd = DateTime.Now.TimeOfDay;
            Log.Message(true, "{0} :{1} : {2} : {3} -(Flip End)", timeEnd.Hours, timeEnd.Minutes, timeEnd.Seconds, timeEnd.Milliseconds);

        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            Log.Message(true, "Free Resources");
            foreach (var item in pGmmblockList)
                base.ULT_FW_Free_Resource(item);
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            Log.Message(true, "Disable ULT Mode");
            base.EnableDFT(false);
        }
        public void WaitMilliSeconds(int argMilliSecond)
        {
            long time;
            GetSystemTimePreciseAsFileTime(out time);
            DateTime OriginaldateTime = DateTime.FromFileTimeUtc(time);
            DateTime dateTime = DateTime.FromFileTimeUtc(time);

            int millisecond = (OriginaldateTime.Millisecond + argMilliSecond) % 1000;
            int second = OriginaldateTime.Second + ((OriginaldateTime.Millisecond + argMilliSecond) / 1000);
            bool loop = true;

            while (loop)
            {
                long newTime;
                loop= false;
                GetSystemTimePreciseAsFileTime(out newTime);
                dateTime = DateTime.FromFileTimeUtc(newTime);
                if(dateTime.Second < second)
                    loop= true;
                else if(dateTime.Second == second)
                {
                    if(dateTime.Millisecond < millisecond)
                        loop= true;
                }
            }

        }  
    }
}
