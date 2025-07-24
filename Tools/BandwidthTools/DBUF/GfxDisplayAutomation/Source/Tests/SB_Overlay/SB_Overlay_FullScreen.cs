namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Xml.Linq;
    using System.IO;
    using System.Text;
    using System;
    using System.Threading;

    class SB_OverLay_FullScreen : SB_Overlay_ExtendedDrag
    {
        private string eventSpriteHorizontal = "SPRITE_SIZE";
        private string eventSpriteVertical = "SPRITE_VERTICAL_SIZE";

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!(base.CurrentConfig.ConfigType == DisplayConfigType.TED || base.CurrentConfig.ConfigType == DisplayConfigType.ED || base.CurrentConfig.ConfigType == DisplayConfigType.SD))
                Log.Abort("This test requires the config mode to be in TED/ED/SD , current display mode: {0}", base.CurrentConfig.ConfigType);
            ApplyConfig(base.CurrentConfig);
            VerifyConfig(base.CurrentConfig);

        }
        public SB_OverLay_FullScreen()
            : base()
        {
            base._actionAfterVerify = this.ActionAfterVerify;
        }

        private void ActionAfterVerify()
        {   
            base.FullScreen(dh, base.CurrentConfig);
            base.VerifyRegisterForDisplay(displayType, false);
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, base.CurrentConfig.EnumeratedDisplays.Find(dispInfo => dispInfo.DisplayType == displayType));
            PipePlaneParams pipePlaneObject = new PipePlaneParams(base.displayType);
            PipePlaneParams pipePlaneParams = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlaneObject);
            uint spriteSurfaceWidth = base.ReadRegister(eventSpriteHorizontal, PIPE.NONE, pipePlaneParams.Plane, PORT.NONE) + 1;
            uint spriteSurfaceHeight = base.ReadRegister(eventSpriteVertical, PIPE.NONE, pipePlaneParams.Plane, PORT.NONE) + 1;
            if(spriteSurfaceWidth== actualMode.HzRes && spriteSurfaceHeight==actualMode.VtRes)
                Log.Success("Overlay is running on Fullscreen successfully on display: {0}",base.displayType);
            else
                Log.Fail("Overlay is not running on Fullscreen on display: {0}",base.displayType);
            base.FullScreen(dh, base.CurrentConfig);
        }
        
    }
}
