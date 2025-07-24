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
    class SB_VRR_Sync_Async_Flips : SB_VRR_GenerateFlip
    {    
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            Log.Message(true, "Set Source Address");            
            uint sourceId = 0, ret= 0;       
            string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
            for (int i = 0; i < files.Count(); i++)
            {
                byte[] array = File.ReadAllBytes(files[i]);
                Marshal.Copy(array, 0, pUserVirtualAddressList[i], array.Length);
            }
            DisplayList VrrSupportedDisplayList = new DisplayList();            
            base.GetVRRCapableDisplays(VrrSupportedDisplayList);
            if (VrrSupportedDisplayList.Count == 0)
                Log.Abort("This test requires VRR capable displays. None of the connected displays are VRR capable.");

            //send sync flips and check VRR status
            Log.Message(true, "Sending sync flips");
            ULT_SETVIDPNSOURCEADDRESS_FLAGS sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync;                          
            for (int i = 0; i < files.Count(); i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmblockList[i], sourceId, 8, sourceAddressFlags);
                WaitMilliSeconds(50);
            }
            VrrSupportedDisplayList.ForEach(disp =>
            {
                ret= base.IsVRREnabled(disp);
                if (ret == 0)
                    Log.Success("With sync flips, VRR is disabled on display {0}", disp.ToString());
                else
                    Log.Fail("With sync flips, VRR is enabled on display {0}", disp.ToString());
            });


            //send async flips and check VRR status
            Log.Message(true, "Sending async flips");
            sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipImmediate;
            for (int i = 0; i < files.Count(); i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmblockList[i], sourceId, 8, sourceAddressFlags);
                WaitMilliSeconds(50);
            }
            VrrSupportedDisplayList.ForEach(disp =>
            {
                ret= base.IsVRREnabled(disp);
                if (ret == 0)
                    Log.Fail("With async flips, VRR is disabled on display {0}", disp.ToString());
                else
                    Log.Success("With async flips, VRR is enabled on display {0}", disp.ToString());
            });


            //send sync flips and check VRR status
            Log.Message(true, "Sending sync flips");
            sourceAddressFlags = ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync;
            for (int i = 0; i < files.Count(); i++)
            {
                base.ULT_FW_Set_Source_Address(pGmmblockList[i], sourceId, 8, sourceAddressFlags);
                WaitMilliSeconds(50);
            }
            VrrSupportedDisplayList.ForEach(disp =>
            {
                ret= base.IsVRREnabled(disp);
                if (ret == 0)
                    Log.Success("With sync flips, VRR is disabled on display {0}", disp.ToString());
                else
                    Log.Fail("With sync flips, VRR is enabled on display {0}", disp.ToString());
            });

        }

    }
}
