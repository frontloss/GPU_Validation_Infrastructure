namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;


    [Test(Type = TestType.HasPlugUnPlug)]
    public class SB_ULT_ACDCSwitch_Basic : SB_ULT_Base
    {
        protected Dictionary<DisplayType, string> _defaultEDIDMap = null;
        protected Dictionary<DisplayType, string> _changeEdid = null;

        public SB_ULT_ACDCSwitch_Basic()
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

           
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.SwitchToDC();
            System.Threading.Thread.Sleep(10000);

            base.SwitchToAC();
            System.Threading.Thread.Sleep(10000);
        }       
        
    }
}
