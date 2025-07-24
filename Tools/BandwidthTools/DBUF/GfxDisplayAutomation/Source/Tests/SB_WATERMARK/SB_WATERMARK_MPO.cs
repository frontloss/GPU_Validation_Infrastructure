using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Windows.Forms;
using System.Linq;

namespace Intel.VPG.Display.Automation
{
    class SB_WATERMARK_MPO : SB_Plane_Scalar_Two_Plane
    {
        public SB_WATERMARK_MPO()
        {
            _verifyWatermark = true;
        }
    }
}
