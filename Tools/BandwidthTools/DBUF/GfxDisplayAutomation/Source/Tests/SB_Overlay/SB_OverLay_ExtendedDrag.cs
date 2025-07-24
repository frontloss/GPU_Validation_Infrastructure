using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    public class SB_Overlay_ExtendedDrag:SB_Overlay_Base
    {
        protected List<DisplayConfig> _dispSwitchOrder = null;
        protected DisplayHierarchy dh;
        protected System.Action _actionAfterVerify = null;
        protected DisplayType displayType;
        protected DisplayInfo displayInfo;

        public SB_Overlay_ExtendedDrag():base()
        {
            _actionAfterVerify = null;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (!(base.CurrentConfig.ConfigType == DisplayConfigType.TED || base.CurrentConfig.ConfigType == DisplayConfigType.ED || base.CurrentConfig.ConfigType == DisplayConfigType.SD))
                Log.Abort("This test requires the config mode to be in TED or ED or SD, current display mode: {0}", base.CurrentConfig.ConfigType);
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
            
            ApplyConfig(base.CurrentConfig);
            VerifyConfig(base.CurrentConfig);
  
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.StopVideo();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            foreach (DisplayType display in base.CurrentConfig.DisplayList)
            {
                Log.Message(true, "Moving Overlay to {0}", display);
                displayType = display;
                dh = DisplayExtensions.GetDispHierarchy(base.CurrentConfig, display);
                base.PlayAndMoveVideo(dh, base.CurrentConfig);

                ///Verify register
                base.VerifyRegisterForDisplay(display, false);
                if (this._actionAfterVerify != null)
                    this._actionAfterVerify();
                base.CurrentConfig.DisplayList.ForEach(otherDisp =>
                {
                    if (display != otherDisp)
                        base.VerifyRegisterForDisplay(otherDisp, true);
                });

            }

            base.StopVideo();
        }      
    }
}
