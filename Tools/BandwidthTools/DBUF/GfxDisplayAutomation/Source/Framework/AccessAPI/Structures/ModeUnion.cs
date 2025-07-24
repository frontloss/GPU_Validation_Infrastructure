namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;
    using System.Text;

    [StructLayout(LayoutKind.Explicit)]
    internal struct ModeUnion
    {
        [FieldOffset(0)]
        public DISPLAYCONFIG_TARGET_MODE targetMode;
        [FieldOffset(0)]
        public DISPLAYCONFIG_SOURCE_MODE sourceMode;

        public override string ToString()
        {
            StringBuilder PrintConfig = new StringBuilder(string.Empty);
            PrintConfig.Append(targetMode.ToString());
            PrintConfig.Append(sourceMode.ToString());

            return PrintConfig.ToString();
        }
    }
}
