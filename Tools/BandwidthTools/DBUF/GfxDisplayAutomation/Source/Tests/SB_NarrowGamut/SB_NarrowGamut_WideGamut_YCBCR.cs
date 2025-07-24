using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    [Test(Type = TestType.HasINFModify)]
    class SB_NarrowGamut_WideGamut_YCBCR:SB_NarrowGamut_WideGamut_XVYCC
    {
        public SB_NarrowGamut_WideGamut_YCBCR()
        {
            base._colorType = ColorType.YCbCr;
            base._wGLevel = WideGamutLevel.LEVEL4;
            base._availableEDIDMap = new Dictionary<DisplayType, string>();
            base._availableEDIDMap.Add(DisplayType.HDMI, "HDMI_Dell_U2709_YCBCR.EDID");
            base._availableEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_U2709_YCBCR.EDID");

            base._availableEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
            base._availableEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");            
        }
       protected  override void VerifyColor(DisplayType argDispType)
        {
            Log.Message(true, "Verify {0} for {1}", _colorType, _xvycc_YcbcrDisplay);
            XvYccYcbXr xvyccObject = new XvYccYcbXr()
            {
                displayType = DisplayType.HDMI,
                currentConfig = base.CurrentConfig,
                colorType = ColorType.YCbCr,
                isEnabled = 1
            };
            if (AccessInterface.SetFeature<bool, XvYccYcbXr>(Features.YCbCr, Action.SetMethod, xvyccObject))
            {
                Log.Success("ycbcr is enabled on hdmi");
                DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == DisplayType.HDMI).FirstOrDefault();

                base.RegisterCheck(displayInfo.DisplayType, displayInfo, "YCBCR_ENABLE");

            }
            else
                Log.Fail("xvycc is not enabled on hdmi");
        }     
    }
}
