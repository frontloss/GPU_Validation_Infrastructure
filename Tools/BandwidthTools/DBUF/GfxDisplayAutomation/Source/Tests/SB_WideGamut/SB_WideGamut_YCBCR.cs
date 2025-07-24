using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasReboot)]
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_WideGamut_YCBCR : SB_WideGamut_XVYCC
    {
        public SB_WideGamut_YCBCR()
        {
            _feature = Features.YCbCr;
            _colorType = ColorType.YCbCr;
            _enableEvent = "YCBCR_ENABLE";
            _disableEvent = "YCBCR_DISABLE";
            _edidFile = "HDMI_DELL.EDID";
        }
    }
}
