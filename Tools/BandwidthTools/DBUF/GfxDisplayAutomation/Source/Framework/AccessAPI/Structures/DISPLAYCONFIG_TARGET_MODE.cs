using System.Text;
namespace Intel.VPG.Display.Automation
{
    internal struct DISPLAYCONFIG_TARGET_MODE
    {
        public DISPLAYCONFIG_VIDEO_SIGNAL_INFO targetVideoSignalInfo;
        public override string ToString()
        {
            return targetVideoSignalInfo.ToString();
        }
    }
}
