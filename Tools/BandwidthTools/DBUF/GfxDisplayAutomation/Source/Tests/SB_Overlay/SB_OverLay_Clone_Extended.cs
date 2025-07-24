using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_Overlay_Clone_Extended : SB_Overlay_DisplaySwap
    {
        public SB_Overlay_Clone_Extended()
            : base()
        {
            this._actionBeforelaunch = this.InitilizeSwitch;
        }

        private void InitilizeSwitch()
        {
            switch(base.CurrentConfig.ConfigType)
            {
                case DisplayConfigType.TDC:
                case DisplayConfigType.TED:
                    {
                        DisplayConfig ddcConfig1 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay};
                        DisplayConfig tedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay,SecondaryDisplay=base.CurrentConfig.SecondaryDisplay,TertiaryDisplay=base.CurrentConfig.PrimaryDisplay };
                        DisplayConfig tdcConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                        DisplayConfig edConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                                   
                        _dispSwitchOrder = new List<DisplayConfig>() { ddcConfig1, tedConfig, tdcConfig, edConfig };      
                        break;
                    }
                case DisplayConfigType.DDC:
                case DisplayConfigType.ED:
                    {
                        DisplayConfig ddcConfig1 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                        DisplayConfig edConfig1 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay,SecondaryDisplay=base.CurrentConfig.PrimaryDisplay };
                        DisplayConfig ddcConfig2 = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };
                        DisplayConfig edConfig2 = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };

                        _dispSwitchOrder = new List<DisplayConfig>() { ddcConfig1, edConfig1, ddcConfig2, edConfig2 };
                        break;
                    }
            } 
       
        } 
      }    
}
