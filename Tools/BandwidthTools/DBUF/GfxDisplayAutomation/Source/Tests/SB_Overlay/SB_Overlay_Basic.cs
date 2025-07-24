using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;

namespace Intel.VPG.Display.Automation
{
    public class SB_Overlay_Basic : SB_Overlay_Base
    {
        protected System.Action _actionAfterVerify = null;

        public SB_Overlay_Basic()
            : base()
        {
            _actionAfterVerify = null;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            ApplyConfig(base.CurrentConfig);
            VerifyConfig(base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 1)]
        public virtual void TestStep1()
        {
            base.StopVideo();

            Log.Message(true, "Moving Overlay to {0}", base.CurrentConfig.PrimaryDisplay);
            base.PlayAndMoveVideo(DisplayHierarchy.Display_1, base.CurrentConfig);

            VerifyRegisters(base.CurrentConfig);

            if (this._actionAfterVerify != null)
                this._actionAfterVerify();
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.StopVideo();
        }

        protected void VerifyRegisters(DisplayConfig currentConfig)
        {
            bool OverlayPlaying = true;
            foreach (DisplayType display in currentConfig.CustomDisplayList)
            {
                if (currentConfig.GetDispHierarchy(display) == DisplayHierarchy.Display_1)
                    OverlayPlaying = true;
                else
                    OverlayPlaying = false;

                ///Verify register
                base.VerifyRegistersForDisplay(display, OverlayPlaying);
            }
        }
    }

}
