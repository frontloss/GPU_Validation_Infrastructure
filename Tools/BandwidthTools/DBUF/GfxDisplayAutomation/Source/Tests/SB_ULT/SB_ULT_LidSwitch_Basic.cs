namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
   

    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_ULT_LidSwitch_Basic : SB_ULT_Base
    {
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _changeEdid = null;

        public SB_ULT_LidSwitch_Basic()
        {
            _defaultEDIDMap = new Dictionary<DisplayType, string>();
            _changeEdid = new Dictionary<DisplayType, string>();

            _defaultEDIDMap.Add(DisplayType.HDMI, "HDMI_DELL.EDID");
            _changeEdid.Add(DisplayType.HDMI, "HDMI_DELL_U2711_XVYCC.EDID");
            _defaultEDIDMap.Add(DisplayType.HDMI_2, "HDMI_Dell_3011.EDID");
            _changeEdid.Add(DisplayType.HDMI_2, "HDMI_HP.EDID");
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public override void TestStep0()
        {
            if (ApplicationManager.ApplicationSettings.UseDivaFramework || ApplicationManager.ApplicationSettings.UseULTFramework || ApplicationManager.ApplicationSettings.UseSHEFramework)
            {
                _defaultEDIDMap.Add(DisplayType.DP, "DP_3011.EDID");
                _changeEdid.Add(DisplayType.DP, "DP_HP_ZR2240W.EDID");
                _defaultEDIDMap.Add(DisplayType.DP_2, "DP_HP_ZR2240W.EDID");
                _changeEdid.Add(DisplayType.DP_2, "DP_3011.EDID");
            }

            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            if (base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).Count() == 0)
                Log.Abort("Hotplug test needs atleast 1 pluggable display");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.DisplayList.ForEach(curDisp =>
            {



                if (base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == curDisp).Select(dI => dI.DisplayType).FirstOrDefault() == DisplayType.None)
                {
                    base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
                    //SHE_HotPlug(curDisp);
                    System.Threading.Thread.Sleep(5000);
                }
            });

            base.ApplyConfigOS(base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 2)]
        public virtual void TestStep2()
        {
            base.HotUnPlug(DisplayType.EDP);
            System.Threading.Thread.Sleep(10000);

            base.HotPlug(DisplayType.EDP);
            System.Threading.Thread.Sleep(10000);
        }
       
        [Test(Type = TestType.Method, Order = 3)]
        public virtual void TestStep4()
        {
            
            base.VerifyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public virtual void TestStep5()
        {
            Log.Message(true, "Test clean up- Unplug all displays");
            base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotUnPlug(curDisp);
                //SHE_HotUnplug(curDisp);
            });
        }
    }
}
