namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
     [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_Change_Edid_Semiautomated:SB_Hotplug_Unplug_Change_Edid
    {
       protected  Dictionary<DisplayType, string> _semiAutomated_CompleteName = null;
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            base.TestStep2();
            _semiAutomated_CompleteName = new Dictionary<DisplayType, string>();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                {
                  string dispCompleteName=  base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                  _semiAutomated_CompleteName.Add(curDisp, dispCompleteName);
                    base.PerformSemiautomated("Unplug " + curDisp);
                }
            });
        }
        [Test(Type = TestType.Method, Order = 3)]
        public override void TestStep3()
        {
            base.TestStep3();
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_semiAutomatedDispList.Contains(curDisp))
                {
                    string edidName = _semiAutomated_CompleteName[curDisp];
                    base.PerformSemiautomated("Plug "+curDisp+" with an Edid other than "+edidName);
                }
            });
            List<DisplayInfo> enumeratedDisplay = AccessInterface.GetFeature<List<DisplayInfo>>(Features.DisplayEnumeration, Action.GetAll);
            AccessInterface.SetFeature<bool, List<DisplayInfo>>(Features.DisplayEnumeration, Action.SetMethod, enumeratedDisplay);
            base.CurrentConfig.EnumeratedDisplays.Clear();
            base.CurrentConfig.EnumeratedDisplays.AddRange(enumeratedDisplay);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.TestStep4();
            Log.Message(true, "Verifying the change of edid for semi automated displays");
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
           {
               if (_semiAutomatedDispList.Contains(curDisp))
               {
                 string dispCompleteName=base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.CompleteDisplayName).FirstOrDefault();
                 if (_semiAutomated_CompleteName.Keys.Contains(curDisp))
                 {
                     if (_semiAutomated_CompleteName[curDisp] != dispCompleteName)
                     {
                         Log.Success("{0} is switched from {1} to {2}", curDisp, _semiAutomated_CompleteName[curDisp], dispCompleteName);
                     }
                     else
                     {
                         Log.Fail("{0}: Current edid: {1} , edid before swap {2}", curDisp, dispCompleteName, _semiAutomated_CompleteName[curDisp]);
                     }
                 }
               }
           });          
        }
    }
}
