namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Text.RegularExpressions;
    using System.IO;
    using System.Runtime.InteropServices;
    public class SB_Modes_ApplyModes_Basic_ULT_Framework : SB_Modes_ApplyModes_Basic
    {

        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            //Assuming we will set the extended desktop
            //Enable the feature in the secondary display

            EnableULT(true);
            UInt64 pGmmBlock = 0, pUserVirtualAddress = 0;
            ULT_FW_Create_Resource(1920, 1080, ULT_PIXELFORMAT.SB_B8G8R8A8, ULT_TILE_FORMATS.ULT_TILE_FORMAT_X, ref pGmmBlock, ref pUserVirtualAddress);

            FillFrameBuffer(pUserVirtualAddress);

            ULT_FW_Set_Source_Address(pGmmBlock, (uint)DisplayHierarchy.Display_2 , 8, ULT_SETVIDPNSOURCEADDRESS_FLAGS.FlipOnNextVSync);

            ULT_FW_Free_Resource(pGmmBlock);

            EnableULT(false);
        }

        private void FillFrameBuffer(UInt64 pVirtualAddress)
        {
            byte[] array = File.ReadAllBytes("memoryDump_Red.bin");

            IntPtr p = new IntPtr((Int64)pVirtualAddress);
            Marshal.Copy(array, 0, p, array.Length);
        }

        private void EnableULT(bool status)
        {
            ULT_ESC_ENABLE_ULT_ARG ult_Esc_Args = new ULT_ESC_ENABLE_ULT_ARG();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT;
            ult_Esc_Args.bEnableULT = status;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;
            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_ESC_ENABLE_ULT, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
        }

        internal bool ULT_FW_Create_Resource(uint x, uint y, ULT_PIXELFORMAT SRC_Pixel_Format, ULT_TILE_FORMATS Tile_Format, ref UInt64 pGmmBlock, ref UInt64 pUserVirtualAddress)
        {
            ULT_CREATE_RES_ARGS ult_Esc_Args = new ULT_CREATE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE;
            ult_Esc_Args.ulBaseWidth = x;
            ult_Esc_Args.ulBaseHeight = y;
            ult_Esc_Args.Format = SRC_Pixel_Format;
            ult_Esc_Args.TileFormat = Tile_Format;
            ult_Esc_Args.AuxSurf = false;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_CREATE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                pGmmBlock = ult_Esc_Args.pGmmBlock;
                pUserVirtualAddress = ult_Esc_Args.pUserVirtualAddress;
                return true;
            }
            return false;
        }

        internal bool ULT_FW_Free_Resource(UInt64 pGmmBlock)
        {
            ULT_FREE_RES_ARGS ult_Esc_Args = new ULT_FREE_RES_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_FREE_RESOURCE;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_FREE_RESOURCE, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                Log.Message("Freed the resource");
                return true;
            }
            return false;
        }

        internal bool ULT_FW_Set_Source_Address(UInt64 pGmmBlock, uint sourceID, uint dataSize, ULT_SETVIDPNSOURCEADDRESS_FLAGS Flag)
        {
            ULT_ESC_SET_SRC_ADD_ARGS ult_Esc_Args = new ULT_ESC_SET_SRC_ADD_ARGS();
            ult_Esc_Args.eULTEscapeCode = ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS;
            ult_Esc_Args.pGmmBlock = pGmmBlock;
            ult_Esc_Args.ulSrcID = sourceID;
            ult_Esc_Args.ulDataSize = dataSize;
            ult_Esc_Args.Flags = Flag;
            ult_Esc_Args.ulEscapeDataSize = (uint)Marshal.SizeOf(ult_Esc_Args) - 16;

            ULT_FW_EscapeParams escapeParams = new ULT_FW_EscapeParams(ULT_ESCAPE_CODE.ULT_SET_SRC_ADDRESS, ult_Esc_Args);

            if (!AccessInterface.SetFeature<bool, ULT_FW_EscapeParams>(Features.ULT_Framework, Action.SetMethod, escapeParams))
                Log.Abort("Failed to enable {0}", ult_Esc_Args.eULTEscapeCode);
            else
            {
                Log.Message("Freed the resource");
                return true;
            }
            return false;
        }
    }
}



