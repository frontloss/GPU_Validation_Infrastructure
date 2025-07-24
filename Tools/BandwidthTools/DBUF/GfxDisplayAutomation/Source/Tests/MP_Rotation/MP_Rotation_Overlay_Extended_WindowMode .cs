using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class MP_Rotation_Overlay_Extended_WindowMode : MP_Rotation_Basic
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
            if (base.CurrentConfig.ConfigType == DisplayConfigType.ED)
            {
                if (base.CurrentConfig.SecondaryDisplay != DisplayType.None)
                {
                    curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.ED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay };
                    base.ApplyConfig(curAppliedConfig);
                    base._angle = new List<uint>() { 90, 180 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_2, curAppliedConfig);
                    base.FullScreen(DisplayHierarchy.Display_2, curAppliedConfig);
                    base.StopVideo();


                    base._angle = new List<uint>() { 270, 90 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    base.PlayAndMoveVideo(DisplayHierarchy.Display_2, curAppliedConfig);

                    base.StopVideo();
                }
            }
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            if (base.CurrentConfig.ConfigType == DisplayConfigType.TED)
            {
                if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
                {
                    curAppliedConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TED, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
                    base.ApplyConfig(curAppliedConfig);
                    base._angle = new List<uint>() { 90, 180, 270 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    Log.Message(true,"Dragging overlay app to secondary {0}",curAppliedConfig.SecondaryDisplay);
                    base.PlayAndMoveVideo(DisplayHierarchy.Display_2, curAppliedConfig);
                    Log.Message(true, "Dragging overlay app to tertiary {0}", curAppliedConfig.TertiaryDisplay);
                    base.PlayAndMoveVideo(DisplayHierarchy.Display_3, curAppliedConfig);
                    base.StopVideo();

                    base._angle = new List<uint>() { 180, 270, 90 };
                    base._rotate[curAppliedConfig.ConfigType.GetUnifiedConfig()]();

                    base.PlayAndMoveVideo(DisplayHierarchy.Display_1, curAppliedConfig);
                    Log.Message(true, "Dragging overlay app to secondary {0}", curAppliedConfig.SecondaryDisplay);
                    base.PlayAndMoveVideo(DisplayHierarchy.Display_2, curAppliedConfig);
                    Log.Message(true, "Dragging overlay app to tertiary {0}", curAppliedConfig.TertiaryDisplay);
                    base.PlayAndMoveVideo(DisplayHierarchy.Display_3, curAppliedConfig);
                    base.StopVideo();
                }
            }
        }
    }
}
