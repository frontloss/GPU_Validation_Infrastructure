namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;   
    using System.IO;
    using System.Diagnostics;
    using System.Collections.Generic;

    class MP_48Hz_MinMaxResolutions : MP_48Hz_Basic
    {
        List<DisplayMode> modeList = null;
        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            List<DisplayType> paramDispList = new List<DisplayType>() { DisplayType.EDP };
            List<DisplayModeList> allMode = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, paramDispList);     
            modeList = TestModes(allMode.First().supportedModes);
            Log.Message(true, "Set Minimum Mode");
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, modeList.First()))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
            base.TestStep5();
            base.TestStep6();
        }
        [Test(Type = TestType.Method, Order = 8)]
        public void TestStep8()
        {
            Log.Message(true, "Set Intermediate Mode");
            if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, modeList.Last()))
                Log.Success("Mode applied Successfully");
            else
                Log.Fail("Fail to apply Mode");
            base.TestStep5();
            base.TestStep6();
        }
        private List<DisplayMode> TestModes(List<DisplayMode> displayModeList)
        {
            List<DisplayMode> testModes = new List<DisplayMode>();
            List<DisplayMode> modeRefreshRates = new List<DisplayMode>();
            testModes.Add(displayModeList.First());
            testModes.Add(displayModeList[displayModeList.Count / 2]);
            modeRefreshRates = ModesRefreshRates(testModes, displayModeList);
            return modeRefreshRates;
        }
        private List<DisplayMode> ModesRefreshRates(List<DisplayMode> testMode, List<DisplayMode> entireModeList)
        {
            List<DisplayMode> modeRefreshRate = new List<DisplayMode>();
            for (int i = 0; i < testMode.Count; i++)
            {
                for (int j = 0; j < entireModeList.Count; j++)
                {
                    if ((testMode[i].HzRes == entireModeList[j].HzRes) && (testMode[i].VtRes == entireModeList[j].VtRes) && (entireModeList[j].RR == 60))
                        modeRefreshRate.Add(entireModeList[j]);
                }
            }
            return modeRefreshRate;
        }
    }
}
