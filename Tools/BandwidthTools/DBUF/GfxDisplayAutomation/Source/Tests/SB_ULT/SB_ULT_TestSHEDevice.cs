namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;


    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_ULT_TestSHEDevice : SB_ULT_Base
    {
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _changeEdid = null;

        public SB_ULT_TestSHEDevice()
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

                _defaultEDIDMap.Add(DisplayType.DP_3, "DP_HP_ZR2240W.EDID");
                _changeEdid.Add(DisplayType.DP_3, "DP_3011.EDID");
            }

            if (base.CurrentConfig.ConfigTypeCount > base.CurrentConfig.DisplayList.Count())
                Log.Abort("{0} requires atleast {1} Displays to be enumerated, current Display count: {2}", base.CurrentConfig.ConfigType, base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            if (base.CurrentConfig.DisplayList.Intersect(_defaultEDIDMap.Keys).Count() == 0)
                Log.Abort("Hotplug test needs atleast 1 pluggable display");
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            System.Threading.Thread.Sleep(10000);

            base.SwitchToDC();
            System.Threading.Thread.Sleep(10000);

            base.SwitchToAC();
            System.Threading.Thread.Sleep(10000);

            if (base.CurrentConfig.DisplayList.Contains(DisplayType.HDMI))
            {
                base.HotPlug(DisplayType.HDMI);
                System.Threading.Thread.Sleep(10000);

                DisplayConfig dispConfig_HDMI = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.HDMI };
                ApplyConfigOS(dispConfig_HDMI);
                System.Threading.Thread.Sleep(10000);


                DisplayConfig dispConfig_EDP = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.EDP };
                ApplyConfigOS(dispConfig_EDP);
                System.Threading.Thread.Sleep(10000);

                base.HotUnPlug(DisplayType.EDP);
                System.Threading.Thread.Sleep(10000);

                base.HotPlug(DisplayType.EDP);
                System.Threading.Thread.Sleep(10000);

                ApplyConfigOS(dispConfig_HDMI);
                System.Threading.Thread.Sleep(10000);

                base.HotUnPlug(DisplayType.HDMI);
                System.Threading.Thread.Sleep(10000);
            }

            if (base.CurrentConfig.DisplayList.Contains(DisplayType.DP))
            {
                base.HotPlug(DisplayType.DP);
                System.Threading.Thread.Sleep(10000);

                DisplayConfig dispConfig_DP = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.DP };
                ApplyConfigOS(dispConfig_DP);
                System.Threading.Thread.Sleep(10000);

                if (base.CurrentConfig.DisplayList.Contains(DisplayType.DP_2))
                {
                    base.HotPlug(DisplayType.DP_2);
                    System.Threading.Thread.Sleep(10000);

                    DisplayConfig dispConfig_DP_2 = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.DP_2 };
                    ApplyConfigOS(dispConfig_DP_2);
                    System.Threading.Thread.Sleep(10000);

                    if (base.CurrentConfig.DisplayList.Contains(DisplayType.DP_3))
                    {                        
                        base.HotPlug(DisplayType.DP_3);
                        System.Threading.Thread.Sleep(10000);

                        DisplayConfig dispConfig_DP_3 = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = DisplayType.DP_3 };
                        ApplyConfigOS(dispConfig_DP_3);
                        System.Threading.Thread.Sleep(10000);

                        base.HotUnPlug(DisplayType.DP_3);
                        System.Threading.Thread.Sleep(10000);
                    }
                    ApplyConfigOS(dispConfig_DP_2);
                    base.HotUnPlug(DisplayType.DP_2);
                    System.Threading.Thread.Sleep(10000);
                    
                }
                ApplyConfigOS(dispConfig_DP);
                base.HotUnPlug(DisplayType.DP);
                System.Threading.Thread.Sleep(10000);
            }       
        }
    }
}
