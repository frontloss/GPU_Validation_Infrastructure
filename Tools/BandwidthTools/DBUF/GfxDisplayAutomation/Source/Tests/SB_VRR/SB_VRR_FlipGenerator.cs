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
    class SB_VRR_FlipGenerator : SB_VRR_GenerateFlip
    {
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            Log.Message(true, "Set Source Address");            
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipImmediate;
            
            string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
            for (int i = 0; i < files.Count(); i++)
            {
                byte[] array = File.ReadAllBytes(files[i]);
                Marshal.Copy(array, 0, pUserVirtualAddressList[i], array.Length);
            }
            
            TimeSpan time = DateTime.Now.TimeOfDay;
            Log.Message(true, "{0} :{1} : {2} :{3} -(Flip Start)", time.Hours, time.Minutes, time.Seconds, time.Milliseconds);

            
            for(int maxIter = 0; maxIter < 50; maxIter++)
            {                
                for (int i = 0; i < files.Count(); i++)
                {
                    base.ULT_FW_Set_Source_Address(pGmmblockList[i], sourceId, 8, sourceAddressFlags);
                    WaitMilliSeconds(500);
                }
                
				//Generate flips till there's a test running
                if (Process.GetProcessesByName("execute").Count() == 1)
                    break;                
            }
            TimeSpan timeEnd = DateTime.Now.TimeOfDay;
            Log.Message(true, "{0} :{1} : {2} : {3} -(Flip End)", timeEnd.Hours, timeEnd.Minutes, timeEnd.Seconds, timeEnd.Milliseconds);
        }
    }
}
