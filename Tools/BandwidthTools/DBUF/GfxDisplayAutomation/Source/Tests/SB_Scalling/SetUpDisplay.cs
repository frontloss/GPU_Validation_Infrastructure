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

namespace Intel.VPG.Display.Automation
{
    public class SetUpDisplay : TestBase
    {
        string dumpFilepath = string.Empty;
        List<UInt64> pGmmBlockList = new List<UInt64>();
      
        public void Start(uint x, uint y,uint sourceID, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS ult_Tile_Format)
        {
            IntPtr pUserVirtualAddress=default(IntPtr);
            UInt64 pGmmBlock=0, surfaceSize=0;

            Console.WriteLine("Enable ULT Mode");
            EnableULT(true);

            ULT_FW_Create_Resource(x, y, SRC_Pixel_Format, ult_Tile_Format, 0, ref pGmmBlock, ref pUserVirtualAddress, ref  surfaceSize);
            pGmmBlockList.Add(pGmmBlock);

            Console.WriteLine("Set Source Address");
            ULT_FW_Set_Source_Address(pGmmBlock, sourceID, 0, ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync);            
        }

        public void End()
        {
            Console.WriteLine("Free Resource");
            ULT_FW_Free_Resource(pGmmBlockList[0]);
            pGmmBlockList.Clear();

            Console.WriteLine("Disable ULT Mode");
            EnableULT(false);
        }

        private void EnableULT(bool status)
        {
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.bEnableULT = status;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Fail("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }
      
        private bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format, uint AuxSurf, ref UInt64 pGmmBlock, ref IntPtr pUserVirtualAddress, ref UInt64 surfaceSize)
        {
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = false;
            
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Fail("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                pGmmBlock = ult_Esc_Args.pGmmBlock;
                pUserVirtualAddress = (IntPtr)ult_Esc_Args.pUserVirtualAddress;
                surfaceSize = ult_Esc_Args.u64SurfaceSize;

                string filepath = Directory.GetCurrentDirectory() + "\\DumpFiles\\" + "1920_1080_X_RGB.8.8.8.8\\Blue.bin";//string.Concat(dump, "\\rc_NEW.bin");
                byte[] array = File.ReadAllBytes(filepath);

                int arrLength = Math.Min(array.Length, (int)surfaceSize);
                //string[] files = Directory.GetFiles(dumpFilepath, "*.bin");
                //if (splitFileName[3] == "NV12")
                //    arrLength = 2334720;
                //if (count == 11)
                //    arrLength = 0x7F8001;
                Marshal.Copy(array, 0, pUserVirtualAddress, arrLength);

                return true;
            }
            return false;
        }

        private  bool ULT_FW_Free_Resource(UInt64 pGmmBlock)
        {
            ULT_FREE_RES_ARGS ult_Esc_Args = new ULT_FREE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_FREE_RESOURCE;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Fail("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                Log.Verbose("Freed the resource");
                return true;
            }
            return false;
        }
        private bool ULT_FW_Set_Source_Address(UInt64 pGmmBlock, uint sourceID, uint dataSize, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            ULT_ESC_SET_SRC_ADD_ARGS ult_Esc_Args = new ULT_ESC_SET_SRC_ADD_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulSrcID = sourceID;
            ult_Esc_Args.ulDataSize = 8294400;//dataSize;
            ult_Esc_Args.Flags = Flag;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args);
            
            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Fail("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                Log.Verbose("Set source address success.");
                return true;
            }
            return false;
        }
    }
}
