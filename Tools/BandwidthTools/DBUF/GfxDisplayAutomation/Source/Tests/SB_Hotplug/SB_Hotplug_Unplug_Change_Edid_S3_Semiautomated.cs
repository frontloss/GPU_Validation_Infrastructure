namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid_S3_Semiautomated : SB_Hotplug_Unplug_Change_Edid_Semiautomated
    {
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._changeEdid[curDisp], true);
                base.InvokePowerEvent(PowerStates.S3);
            });

            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                {
                    string edidName = _semiAutomated_CompleteName[curDisp];
                    base.PerformSemiautomated("Plug " + curDisp + "after the system initiates S3 with an Edid other than " + edidName);
                    base.InvokePowerEvent(PowerStates.S3);
                }
            });
            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            AccessInterface.SetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.SetMethod, enumeratedDisplay);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
        }
    }
}
