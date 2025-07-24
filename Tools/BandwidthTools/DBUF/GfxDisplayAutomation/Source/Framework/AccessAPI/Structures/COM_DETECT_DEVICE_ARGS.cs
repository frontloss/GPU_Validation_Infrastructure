namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public class COM_DETECT_DEVICE_ARGS
    {
        public uint Command;    //Always COM_DETECT_DEVICE: 29
        public uint Flags;      //Bit0:  Do Redetect
        //Bit1:  Do Legacy Detection 
        public DISPLAY_LIST DispList;
    };
}
