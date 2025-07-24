using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class WideGamut_Slider_Persistence_Before_After_PM_Events_Mode_Change : SB_WideGamut_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigType.GetDisplaysCount() != 3)
            {
                Log.Abort("The test needs atleast 3 displays");
            }
            base.WideGamutDriver(7);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig CurrentConfig = new DisplayConfig() { ConfigType = DisplayConfigType.TDC, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay, SecondaryDisplay = base.CurrentConfig.SecondaryDisplay, TertiaryDisplay = base.CurrentConfig.TertiaryDisplay };
            base.ApplyConfigOS(CurrentConfig);

            base.CurrentConfig.DisplayList.ForEach(curDisp =>
                {
                    base.ApplyWideGamutToDisplay(curDisp, WideGamutLevel.LEVEL4);
                    base.VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL4);
                });
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            base.InvokePowerEvent(PowerStates.S3);
            VerifyPostPowerEvent();
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            base.InvokePowerEvent(PowerStates.S4);
            VerifyPostPowerEvent();
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            base.InvokePowerEvent(PowerStates.S5);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            if (currentConfig.GetCurrentConfigStr().Equals(base.CurrentConfig.GetCurrentConfigStr()))
            {
                Log.Success("{0} is retained after restart", base.CurrentConfig.GetCurrentConfigStr());
            }
            else
            {
                Log.Fail("{0} is not retained after restart, current config is {1}",base.CurrentConfig.GetCurrentConfigStr(),currentConfig.GetCurrentConfigStr());
            }
            VerifyPostPowerEvent();
        }
        [Test(Type = TestType.Method, Order = 6)]
        public void TestStep6()
        {
            List<DisplayModeList> modeList = GetModePerDisplay(base.CurrentConfig);
            modeList.ForEach(curDisp =>
                {
                    curDisp.supportedModes.ForEach(curMode=>
                        {
                            this.ApplyModeOS(curMode, curDisp.display);
                            this.VerifyModeOS(curMode, curDisp.display);
                            base.VerifyWideGamutValue(curDisp.display, WideGamutLevel.LEVEL4);
                        });
                });

        }
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
          List<DisplayType> pluggable=  _pluggableDisplay.Keys.ToList().Intersect(base.CurrentConfig.DisplayList).ToList();
            pluggable.ForEach(curDisp=>
                {
                    base.HotUnPlug(curDisp);
                    base.HotPlug(curDisp);
                    base.VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL4);
                });
        }
        private void VerifyPostPowerEvent()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                base.VerifyWideGamutValue(curDisp, WideGamutLevel.LEVEL4);
            });
        }
        private List<DisplayModeList> GetModePerDisplay(DisplayConfig argDispConfig)
        {
            List<DisplayModeList> modeList=new List<DisplayModeList>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDispConfig.CustomDisplayList);           
            DisplayModeList curMode = new DisplayModeList();
            
            curMode.display = allModeList.First().display;
            curMode.supportedModes = new List<DisplayMode>();
            curMode.supportedModes.Add(allModeList.First().supportedModes.First());
            curMode.supportedModes.Add(allModeList.First().supportedModes.ElementAt(allModeList.First().supportedModes.Count / 2));
            curMode.supportedModes.Add(allModeList.First().supportedModes.Last());
            modeList.Add(curMode);

            allModeList.RemoveAt(0);
            if (argDispConfig.ConfigType.GetUnifiedConfig() == DisplayUnifiedConfig.Extended)
            {
                allModeList.ForEach(curDisp =>
                    {
                        DisplayModeList mode = new DisplayModeList();
                        mode.display = curDisp.display;
                        mode.supportedModes = new List<DisplayMode>();
                        mode.supportedModes.Add(curDisp.supportedModes.First());
                        mode.supportedModes.Add(curDisp.supportedModes.ElementAt(curDisp.supportedModes.Count/2));
                        mode.supportedModes.Add(curDisp.supportedModes.Last());

                        modeList.Add(mode);
                    });
            }
            return modeList;
        }
        protected void ApplyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Set supported mode {0} for {1}", argSelectedMode.GetCurrentModeStr(false), argDisplayType);
            argSelectedMode.display = argDisplayType;
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, argSelectedMode))
            {
                Log.Success("Mode applied Successfully");
            }
            else
                Log.Fail("Fail to apply Mode");
        }
        protected void VerifyModeOS(DisplayMode argSelectedMode, DisplayType argDisplayType)
        {
            Log.Message(true, "Verify the  mode  for {0} through OS", argDisplayType);
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == argDisplayType).First();
            DisplayMode actualMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            if (actualMode.GetCurrentModeStr(true).Equals(argSelectedMode.GetCurrentModeStr(true)))
            {
                Log.Success("Mode {0} is verified for {1}", actualMode.GetCurrentModeStr(false), argDisplayType);
            }
            else
                Log.Fail("Mode chosen {0} is not applied for {1}! Actual is {2}", argSelectedMode.GetCurrentModeStr(false), argDisplayType, actualMode.GetCurrentModeStr(false));
        }
    }
}
