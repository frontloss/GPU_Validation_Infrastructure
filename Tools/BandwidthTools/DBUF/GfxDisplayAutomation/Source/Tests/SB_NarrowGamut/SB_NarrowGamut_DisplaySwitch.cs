using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
     [Test(Type = TestType.HasINFModify)]
    class SB_NarrowGamut_DisplaySwitch : SB_NarrowGamut_DisplaySwap
    {

        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            PerformDisplaySwitch();
        }
        private void PerformDisplaySwitch()
        {
            List<DisplayConfig> displaySwitch = new List<DisplayConfig>() {
            new DisplayConfig(){ConfigType=DisplayConfigType.SD, PrimaryDisplay=base.CurrentConfig.PrimaryDisplay}, 
            new DisplayConfig(){ConfigType=DisplayConfigType.DDC, PrimaryDisplay=base.CurrentConfig.PrimaryDisplay, SecondaryDisplay=base.CurrentConfig.SecondaryDisplay},
            new DisplayConfig(){ConfigType=DisplayConfigType.ED, PrimaryDisplay=base.CurrentConfig.PrimaryDisplay, SecondaryDisplay=base.CurrentConfig.SecondaryDisplay},
             };

            if (base.CurrentConfig.ConfigTypeCount > 2)
            {
                displaySwitch.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
                displaySwitch.Add(new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay });
            }
            displaySwitch.ForEach(curConfig =>
                {
                    base.ApplyConfig(curConfig);
                    base.NarrowGamutSupportedDisplays.Intersect(curConfig.DisplayList).ToList().ForEach(curDisp =>
                        {
                            base.CheckNarrowGamutRegister(curDisp, NarrowGamutOption.EnableNarrowGamut);
                        });                  
                });
        }
    }
}
