namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Text.RegularExpressions;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid : SB_Hotplug_Base
    {
        protected Dictionary<uint, string> _disp_Port_CompleName = new Dictionary<uint, string>();

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (DisplayInfo curDisp in base.CurrentConfig.EnumeratedDisplays)
            {
                if (base._defaultEDIDMap.Keys.Contains(curDisp.DisplayType))
                {
                    foreach (DisplayType curHDMI in base._defaultEDIDMap.Keys)
                        base.HotUnPlug(curHDMI);
                    break;
                }
            }
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
            });
            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                
                string dispName = GetTrimmedDisplayName(curDispInfo.CompleteDisplayName); 

                _disp_Port_CompleName.Add(curDispInfo.WindowsMonitorID, dispName);
            });
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }

        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._changeEdid[curDisp]);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Verifying the change of edid");
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                
                string dispName = GetTrimmedDisplayName(curDispInfo.CompleteDisplayName); 

                if (dispName != _disp_Port_CompleName[curDispInfo.WindowsMonitorID])
                {
                    Log.Success("For {0}, edid is changed from {1} to {2}", curDispInfo.DisplayType, _disp_Port_CompleName[curDispInfo.WindowsMonitorID], dispName);
                }
                else
                    Log.Fail("For {0}, current Edid: {1} , Edid before swap {2}", curDispInfo.DisplayType, dispName, _disp_Port_CompleName[curDispInfo.WindowsMonitorID]);
            });
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message("The config after changing edid is {0}", currentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
            });
        }
    }
}

