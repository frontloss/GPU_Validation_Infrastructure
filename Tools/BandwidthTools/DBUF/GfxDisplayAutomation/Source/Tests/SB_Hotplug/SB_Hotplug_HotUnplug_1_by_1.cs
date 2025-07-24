namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_HotUnplug_1_by_1 : SB_Hotplug_Base
    {
        
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayConfig pri = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.PrimaryDisplay };
            ApplyConfigOS(pri);

            base.HotPlug(base.CurrentConfig.SecondaryDisplay, _defaultEDIDMap[base.CurrentConfig.SecondaryDisplay]);
            DisplayConfig sec = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.SecondaryDisplay };
            ApplyConfigOS(sec);

            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                base.HotPlug(base.CurrentConfig.TertiaryDisplay, _defaultEDIDMap[base.CurrentConfig.TertiaryDisplay]);
                DisplayConfig ter = new DisplayConfig { ConfigType = DisplayConfigType.SD, PrimaryDisplay = base.CurrentConfig.TertiaryDisplay };
                ApplyConfigOS(ter);
            }

            InvokePowerEvent(PowerStates.S3);
            InvokePowerEvent(PowerStates.S4);
           
            base.HotUnPlug(base.CurrentConfig.SecondaryDisplay);

            if (base.CurrentConfig.TertiaryDisplay != DisplayType.None)
            {
                base.HotUnPlug(base.CurrentConfig.TertiaryDisplay);
            }
        }

     }
}
