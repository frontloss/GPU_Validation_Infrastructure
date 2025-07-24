using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_Dbuf_Resolution : SB_Dbuf_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.ApplyConfig(base.CurrentConfig);                 
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            List<DisplayMode> resolutionList = GetResolutionList(base.CurrentConfig);
            if (resolutionList.Count() > 0)
            {
                resolutionList.ForEach(curMode =>
                    {
                        Log.Message(true,"Mode to be applied {0}",curMode.GetCurrentModeStr(false));
                        if (AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, curMode))
                        {
                            Log.Success("Mode {0} applied successfully", curMode.GetCurrentModeStr(false));                           
                            base.CheckDbuf(base.CurrentConfig); 
                        }
                    });
            }
        }
        private List<DisplayMode> GetResolutionList(DisplayConfig argDispConfig)
        {
            List<DisplayMode> listDisplayMode = new List<DisplayMode>();
            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, argDispConfig.DisplayList);
            if (allModeList.Count() > 0)
            {
                if (argDispConfig.ConfigType.GetUnifiedConfig() != DisplayUnifiedConfig.Clone)
                {
                    allModeList.ForEach(curDisp =>
                    {
                        listDisplayMode.Add(GetModeFromList(curDisp.supportedModes,0));
                        listDisplayMode.Add(GetModeFromList(curDisp.supportedModes,curDisp.supportedModes.Count-1));
                        listDisplayMode.Add(GetModeFromList(curDisp.supportedModes, curDisp.supportedModes.Count() / 2));
                    });
                }
                else
                {
                    listDisplayMode.Add(GetModeFromList(allModeList.First().supportedModes, 0));
                    listDisplayMode.Add(GetModeFromList(allModeList.First().supportedModes, allModeList.First().supportedModes.Count - 1));
                    listDisplayMode.Add(GetModeFromList(allModeList.First().supportedModes, allModeList.First().supportedModes.Count() / 2));
                }
            }
            return listDisplayMode;
        }
        private DisplayMode GetModeFromList(List<DisplayMode> argDispModeList, int argIndex)
        {
            DisplayMode mode = new DisplayMode();
            if (argIndex > 0)
            {
                for (int i = argIndex; i > 0; i--)
                {
                    mode = argDispModeList.ElementAt(i);
                    if (!Convert.ToBoolean(mode.InterlacedFlag))
                    {
                        return mode;
                    }
                }
            }
            else
            {
                for (int i = argIndex; i < argDispModeList.Count; i++)
                {
                    mode = argDispModeList.ElementAt(i);
                    if (!Convert.ToBoolean(mode.InterlacedFlag))
                    {
                        return mode;
                    }
                }
            }
            Log.Fail("Cannot find mode at index {0}",argIndex);
            return mode;
        }
    }
}
