using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
namespace Intel.VPG.Display.Automation
{
    class SB_EdidMode_Basic : SB_EdidMode_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisplay =>
            {
                ApplyConfigOS(new DisplayConfig() { ConfigType = DisplayConfigType.SD, PrimaryDisplay = curDisplay });
                Thread.Sleep(3000);
                EdidInfo edidData = new EdidInfo();
                edidData.DisplayType = curDisplay;
                List<DisplayType> display = new List<DisplayType>();
                display.Add(curDisplay);
                edidData = AccessInterface.GetFeature<EdidInfo, EdidInfo>(Features.EDIDData, Action.GetMethod, Source.AccessAPI, edidData);
                List<DisplayModeList> _commonDisplayModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, display);


                Log.Message(true, "{0} edid mode verification", curDisplay);
                List<DisplayMode> osMode = _commonDisplayModeList.Where(dI => dI.display == curDisplay).Select(dI => dI.supportedModes).FirstOrDefault();
                edidData.EsatablishedTiming1.ForEach(curMode =>
                {
                    if (IsResolutionLessThan1024x768(curMode))
                    {
                        Log.Alert("Skipping {0} which is less than 1024x768.", curMode);
                    }
                    else
                    {
                        if (VerifyMode(osMode, curMode))
                        {
                            Log.Success("est timing1 {0} verified in osMode", curMode);
                        }
                        else
                        {
                            Log.Fail("est timing1 {0} not verified in osMode", curMode);
                        }
                    }
                });

                edidData.EsatablishedTiming2.ForEach(curMode =>
                {
                    if (IsResolutionLessThan1024x768(curMode))
                    {
                        Log.Alert("Skipping {0} which is less than 1024x768.", curMode);
                    }
                    else
                    {
                        if (VerifyMode(osMode, curMode))
                        {
                            Log.Success("est timing2 {0} verified in osMode", curMode);
                        }
                        else
                        {
                            Log.Fail("est timing2 {0} not verified in osMode", curMode);
                        }
                    }
                });
                edidData.StandardTiming.ForEach(curMode =>
                {
                    if (IsResolutionLessThan1024x768(curMode))
                    {
                        Log.Alert("Skipping {0} which is less than 1024x768.", curMode);
                    }
                    else
                    {
                        if (VerifyMode(osMode, curMode))
                        {
                            Log.Success("std {0} verified in osMode", curMode);
                        }
                        else
                        {
                            Log.Fail("std {0} not verified in osMode", curMode);
                        }
                    }
                });
                List<DisplayMode> dtdResolution = base.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisplay).Select(dI => dI.DTDResolutions).FirstOrDefault();
                dtdResolution.ForEach(curMode =>
                {
                    if (IsResolutionLessThan1024x768(curMode))
                    {
                        Log.Alert("Skipping {0} which is less than 1024x768.", curMode);
                    }
                    else
                    {
                        if (VerifyMode(osMode, curMode))
                        {
                            Log.Success("DTD {0} verified in osMode", curMode);
                        }
                        else
                        {
                            Log.Fail("DTD {0} not verified in osMode", curMode);
                        }
                    }
                });
            });
        }
        private bool VerifyMode(List<DisplayMode> argListMode, DisplayMode argMode)
        {
            bool match = false;
            argListMode.ForEach(curMode =>
            {
                if (curMode.HzRes == argMode.HzRes && curMode.VtRes == argMode.VtRes && curMode.RR == argMode.RR)
                    match = true;
            });
            return match;
        }

        private bool IsResolutionLessThan1024x768(DisplayMode argMode)
        {
            if (argMode.HzRes < 1024 || argMode.VtRes < 768)
            {
                return true;
            }

            return false;
        }
    }
}
