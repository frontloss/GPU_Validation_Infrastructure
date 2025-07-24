using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_ColorConversion_RGB_YUV_Overlay:TestBase
    {
        protected string _eventName = "PIPE_ENABLE";
        protected string _sprite1 = "SPRITE1";
        protected string _sprite2 = "SPRITE2";
        protected Dictionary<DisplayConfigType, List<DisplayType>> _dispList = null;
        OverlayParams _overlay = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            _dispList = new Dictionary<DisplayConfigType, List<DisplayType>>()
        {
            {DisplayConfigType.SD , new List<DisplayType>(){base.CurrentConfig.PrimaryDisplay}},
            {DisplayConfigType.DDC , new List<DisplayType>(){base.CurrentConfig.PrimaryDisplay}},
            {DisplayConfigType.ED , new List<DisplayType>(){base.CurrentConfig.PrimaryDisplay,base.CurrentConfig.SecondaryDisplay}},            
            {DisplayConfigType.TDC , new List<DisplayType>(){base.CurrentConfig.PrimaryDisplay}},
            {DisplayConfigType.TED , new List<DisplayType>(){base.CurrentConfig.PrimaryDisplay , base.CurrentConfig.SecondaryDisplay , base.CurrentConfig.TertiaryDisplay}}
        };
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
                Log.Success("{0} Applied successfully", base.CurrentConfig.GetCurrentConfigStr());
            else
                Log.Fail("Failed to Apply {0}", base.CurrentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            _dispList[base.CurrentConfig.ConfigType].ForEach(curDisp =>
            {
                DisplayHierarchy dispHierarchy = GetDispHierarchy(curDisp);
                if (dispHierarchy != DisplayHierarchy.Display_1)
                {
                    _overlay = new OverlayParams()
                    {
                        PlaybackOptions = OverlayPlaybackOptions.MovePlayer,
                        DisplayHierarchy = dispHierarchy,
                        CurrentConfig = base.CurrentConfig,
                        overlayApp = OverlayApp.MovingWorld,
                        colorFormat = ColorFormat.RGB
                    };
                    AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, _overlay);
                }
                CheckColorCondition(curDisp);
            });
        }
        private void CheckColorCondition(DisplayType argDispType)
        {
            _overlay = new OverlayParams()
            {
                PlaybackOptions = OverlayPlaybackOptions.FullScreen,
                DisplayHierarchy = GetDispHierarchy(argDispType),
                CurrentConfig = base.CurrentConfig,
                overlayApp = OverlayApp.MovingWorld,
                colorFormat = ColorFormat.RGB
            };
            AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, _overlay);
            CheckColorRegister(ColorFormat.RGB, argDispType);

            _overlay = new OverlayParams()
            {
                PlaybackOptions = OverlayPlaybackOptions.ChangeFormat,
                DisplayHierarchy = GetDispHierarchy(argDispType),
                CurrentConfig = base.CurrentConfig,
                overlayApp = OverlayApp.MovingWorld,
                colorFormat = ColorFormat.YUV
            };
            AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, _overlay);
            CheckColorRegister(ColorFormat.YUV, argDispType);

            _overlay = new OverlayParams()
            {
                PlaybackOptions = OverlayPlaybackOptions.ClosePlayer,
                DisplayHierarchy = GetDispHierarchy(argDispType),
                overlayApp = OverlayApp.MovingWorld,
                CurrentConfig = base.CurrentConfig,
            };
            AccessInterface.SetFeature<OverlayParams>(Features.Overlay, Action.Set, _overlay);
        }
        private void CheckColorRegister(ColorFormat argColorFormat, DisplayType argispType)
        {
            PipePlaneParams pipePlane1 = new PipePlaneParams(argispType);
            pipePlane1 = AccessInterface.GetFeature<PipePlaneParams, PipePlaneParams>(Features.PipePlane, Action.GetMethod, Source.AccessAPI, pipePlane1);
            Log.Message("For display : {0}  @@@  PIPE : {1} @@@ PLANE : {2}", argispType, pipePlane1.Pipe, pipePlane1.Plane);

            Log.Message(true, "Verifying event {0} for {1} {2}", _eventName, argColorFormat, argispType);
            if (base.VerifyRegisters(_eventName, pipePlane1.Pipe, PLANE.NONE, PORT.NONE, true))
            {
                Log.Success("{0} is enabled", pipePlane1.Pipe);
            }
            else
            {
                Log.Fail("{0} is not enabled", pipePlane1.Pipe);
            }
            bool condition = true;
            if (argColorFormat == ColorFormat.RGB)
                condition = false;

            Log.Message(true, "Verifying Sprite registers for {0} {1}", argColorFormat, argispType);
            bool status = base.VerifyRegisters(_sprite1, pipePlane1.Pipe, PLANE.NONE, PORT.NONE, false);
            if (status == condition)
            {
                Log.Success("{0} is verified for {1}", argColorFormat, _sprite1);
            }
            else
            {
                status = base.VerifyRegisters(_sprite2, pipePlane1.Pipe, PLANE.NONE, PORT.NONE, true);
                if (status == condition)
                    Log.Success("{0} is verified for {1}", argColorFormat, _sprite2);
                else
                    Log.Fail("{0} conditions are not verified", argColorFormat);
            }
        }
        private DisplayHierarchy GetDispHierarchy(DisplayType disp)
        {
            DisplayConfig currentConfig = base.CurrentConfig;
            if (disp == currentConfig.PrimaryDisplay)
                return DisplayHierarchy.Display_1;
            else if (disp == currentConfig.SecondaryDisplay)
                return DisplayHierarchy.Display_2;
            else if (disp == currentConfig.TertiaryDisplay)
                return DisplayHierarchy.Display_3;

            Log.Alert("Display Hierarchy not found for {0}", disp);
            return DisplayHierarchy.Unsupported;
        }
    }
}
