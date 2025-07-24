namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Port_Swap : SB_Hotplug_Base
    {
        protected Dictionary<uint, string> _dispCompleName_Port = new Dictionary<uint, string>();
        protected Dictionary<DisplayType, string> _portSwapEDIDMap = new Dictionary<DisplayType,string>();

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (!((base.CurrentConfig.DisplayList.Contains(DisplayType.DP) && base.CurrentConfig.DisplayList.Contains(DisplayType.DP_2)) ||
                (base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI) && base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI_2))))
                Log.Abort("The test needs either both pluggable hdmi and hdmi_2 displays or pluggable dp and dp_2 displays connected.");

            base.TestStep0();

            _portSwapEDIDMap.Add(DisplayType.HDMI, _defaultEDIDMap[DisplayType.HDMI_2]);
            _portSwapEDIDMap.Add(DisplayType.HDMI_2, _defaultEDIDMap[DisplayType.HDMI]);

            _portSwapEDIDMap.Add(DisplayType.DP, _defaultEDIDMap[DisplayType.DP_2]);
            _portSwapEDIDMap.Add(DisplayType.DP_2, _defaultEDIDMap[DisplayType.DP]);
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
            });
            base.ApplyConfigOS(base.CurrentConfig);
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                 string dispName = GetTrimmedDisplayName(curDispInfo.CompleteDisplayName);
                _dispCompleName_Port.Add(curDispInfo.WindowsMonitorID, dispName);
            });
        }
        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            List<DisplayType> tempList=new List<DisplayType>(base.CurrentConfig.DisplayList);
            tempList.Reverse();
            tempList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp);
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, _portSwapEDIDMap[curDisp]);
            });
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep4()
        {
            Log.Message(true, "Verifying port via OS");
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo curDispInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).FirstOrDefault();
                string dispName = GetTrimmedDisplayName(curDispInfo.CompleteDisplayName);
                if (dispName != _dispCompleName_Port[curDispInfo.WindowsMonitorID])
                    Log.Success("For Port: {0}, display switched from {1} to {2}", curDispInfo.Port, _dispCompleName_Port[curDispInfo.WindowsMonitorID], dispName);
                else
                    Log.Fail("Display swap Error. Observed display is : {0} for Port: {1}.", dispName, curDispInfo.Port);
            });
            DisplayConfig currentConfig = AccessInterface.GetFeature<DisplayConfig>(Features.Config, Action.Get);
            Log.Message("The config after changing edid is {0}", currentConfig.GetCurrentConfigStr());
        }
        [Test(Type = TestType.Method, Order = 5)]
        public virtual void TestStep5()
        {
            TestStep2();
        }

        //private Dictionary<uint, string> GetSwappedEDID(Dictionary<uint, string> dispCompleName_Port)
        //{
        //    Dictionary<uint, string> swappedEDID = new Dictionary<uint, string>(dispCompleName_Port);
            
        //    for (int i = 0; i < dispCompleName_Port.Count/2; i++)
        //    {
        //        KeyValuePair<uint, string> temp1 = swappedEDID.ElementAt(i);
        //        KeyValuePair<uint, string> temp2 = swappedEDID.ElementAt(dispCompleName_Port.Count - i - 1);

        //        string tempString = temp1.Value;
        //        swappedEDID[temp1.Key] = temp2.Value;
        //        swappedEDID[temp2.Key] = tempString;
        //    }
        //    return swappedEDID;

        //}
    }
}
