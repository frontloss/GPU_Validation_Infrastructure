using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    class SB_Overlay_DisplaySwap : SB_Overlay_Base
    {
        protected List<DisplayConfig> _dispSwitchOrder = null;
        protected DisplayHierarchy dh;
        protected System.Action _actionBeforelaunch = null;

        public SB_Overlay_DisplaySwap()
            : base()
        {
            this._actionBeforelaunch = this.InitilizeSwitch;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.DisplayList.Count()<2)
                Log.Abort("This test requires atleast 2 displays , current display count: {0}", base.CurrentConfig.DisplayList.Count());
            if (this._actionBeforelaunch != null)
                this._actionBeforelaunch();
        }

        private void InitilizeSwitch()
        {
            switch (base.CurrentConfig.ConfigType)
            {
                case DisplayConfigType.TED:
                case DisplayConfigType.TDC:
                    {
                        DisplayConfig Config1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                        DisplayConfig Config2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
                        DisplayConfig Config3 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
                        DisplayConfig Config4 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.TertiaryDisplay, TertiaryDisplay = base.CurrentConfig.SecondaryDisplay };
                        DisplayConfig Config5 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.PrimaryDisplay };
                        DisplayConfig Config6 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };

                        _dispSwitchOrder = new List<DisplayConfig>() { Config1, Config2, Config3, Config4, Config5, Config6 };
                        break;
                    }
                case DisplayConfigType.DDC:
                case DisplayConfigType.ED:
                    {
                        DisplayConfig Config1 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                        DisplayConfig Config2 = new DisplayConfig() { ConfigType = base.CurrentConfig.ConfigType, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay, SecondaryDisplay = base.CurrentConfig.PrimaryDisplay };

                        _dispSwitchOrder = new List<DisplayConfig>() { Config1, Config2 };
                        break;
                    }
            } 
       
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            _dispSwitchOrder.ForEach(curConfig =>
            {
                base.ApplyConfig(curConfig);
                base.VerifyConfig(curConfig);
                
                dh = DisplayExtensions.GetDispHierarchy(curConfig, curConfig.PrimaryDisplay);
                base.StopVideo();
                base.PlayAndMoveVideo(dh, curConfig);
                
                if (curConfig.PrimaryDisplay != DisplayType.None)
                {
                    base.VerifyRegisterForDisplay(curConfig.PrimaryDisplay, false);
                }
                if (curConfig.SecondaryDisplay != DisplayType.None)
                {
                    base.VerifyRegisterForDisplay(curConfig.SecondaryDisplay, true);
                }
                if (curConfig.TertiaryDisplay != DisplayType.None)
                {
                    base.VerifyRegisterForDisplay(curConfig.TertiaryDisplay, true);
                }
            });

            base.StopVideo();
        }

      }    
}
