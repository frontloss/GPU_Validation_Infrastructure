namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Text.RegularExpressions;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_ULT_ChangeEDID_In_S3 : SB_ULT_Hotplug_Unplug_Basic
    {
        int displaysCountBeforePlug = 0;
        protected Dictionary<uint, string> _disp_CompleName = new Dictionary<uint, string>();
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            displaysCountBeforePlug = base.EnumeratedDisplays.Count;

            base.CurrentConfig.DisplayList.Intersect(base._changeEdid.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();
                string observedString = GetQualifiedString(displayInfo.CompleteDisplayName);
                _disp_CompleName.Add(displayInfo.WindowsMonitorID, observedString);
            });

            //unplug in LowPowerState.
            base.CurrentConfig.DisplayList.Intersect(base._changeEdid.Keys).ToList().ForEach(curDisp =>
           {
               base.HotUnPlug(curDisp, true);
           });

            //Plug in LowPowerState.
            base.CurrentConfig.DisplayList.Intersect(base._changeEdid.Keys).ToList().ForEach(curDisp =>
            {
                DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();
                base.HotPlug(curDisp, true, displayInfo.WindowsMonitorID, base._changeEdid[curDisp], true);
            });
        }

        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            InvokePowerEvent(PowerStates.S3);
        }

        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            DisplayType display = base.CurrentConfig.DisplayList.Intersect(base._changeEdid.Keys).First();

            if (displaysCountBeforePlug == base.EnumeratedDisplays.Count)
            {
                base.CurrentConfig.DisplayList.Intersect(base._changeEdid.Keys).ToList().ForEach(curDisp =>
                {
                    DisplayInfo displayInfo = base.EnumeratedDisplays.Where(item => item.DisplayType == curDisp).FirstOrDefault();

                    string observedString = GetQualifiedString(displayInfo.CompleteDisplayName);
                    if (observedString.Contains(_disp_CompleName[displayInfo.WindowsMonitorID]))
                    {
                        Log.Fail("Change of EDID in Low Power is not happened.");
                    }
                    else
                    {
                        Log.Success("Change of EDID in Low Power is successful.");
                    }
                });

            }
            else
            {
                Log.Fail("Mismatch in no. of displays. Expected: {0} Observed: {1}",
                    displaysCountBeforePlug, base.EnumeratedDisplays.Count);
                Log.Abort("Aborting test");
            }
        }

        private string GetQualifiedString(string st)
        {
             string dispName = Regex.Replace(st, "Digital Television", " ");
            dispName = Regex.Replace(dispName, "Digital Display", " ");
            dispName = Regex.Replace(dispName, " 2", " ");
            dispName = dispName.Trim();

            return dispName;
        }
    }
}
