using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_modes_DisplaySwap_Hotplug_Unplug : SB_modes_DisplaySwap_Basic
    {
        protected List<DisplayType> _pluggableDisplay = null;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            _pluggableDisplay = new List<DisplayType>();

            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                    _pluggableDisplay.Add(curDisp);
                }
            });

            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
            if (_pluggableDisplay.Count() == 0)
                Log.Abort("This test requires atleast one pluggable display");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep3()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.CurrentConfig.DisplayList.Intersect(_pluggableDisplay).ToList().ForEach(curDisp =>
            {
                HotUnPlug(curDisp);
            });
        }
        protected override void VerifyMode(List<DisplayModeList> argDispModeList)
        {
            Log.Message(true, "Performing hotplug unplug");
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_pluggableDisplay.Contains(curDisp))
                    HotUnPlug(curDisp);
            });

            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {
                if (_pluggableDisplay.Contains(curDisp))
                    HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
            base.VerifyMode(argDispModeList);
        }
    }
}
