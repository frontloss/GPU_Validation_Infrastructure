using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Overlay_Clone_WindowMode:MP_Rotation_Basic
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestPreCondition()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.SD)
            {
                base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = curDisp };
                    base.ApplyConfig(curAppliedConfig);
                    base._angle = new List<uint>() { 90 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();

                    base._angle = new List<uint>() { 270 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();
                });
            }
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.DDC)
            {
                if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
                {
                    curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.DDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                    base.ApplyConfig(curAppliedConfig);
                    base._angle = new List<uint>() { 270 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();

                    base._angle = new List<uint>() { 180 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();
                }
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.TDC)
            {
                if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
                {
                    curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                    base.ApplyConfig(curAppliedConfig);
                    base._angle = new List<uint>() { 90 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();

                    base._angle = new List<uint>() { 180 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.StopVideo();
                }
            }
        }
    }
}
