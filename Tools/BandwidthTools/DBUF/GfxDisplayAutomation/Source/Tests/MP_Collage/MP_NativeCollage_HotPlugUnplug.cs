namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;
    using System;
    
    [Test(Type = TestType.HasPlugUnPlug)]
    class MP_NativeCollage_HotPlugUnplug : MP_NativeCollage_BAT
    {
        public MP_NativeCollage_HotPlugUnplug()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
                DisplayConfigType.Vertical
            };
            
        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Message("{0} is not enumerated..Plugging it", DT);
                if (base.HotPlug(DT))
                {
                    Log.Success("Display {0} is plugged successfully", DT);
                }
            }
            base.TestStep1();
        }
        private void PerformAction()
        {
            Log.Message(true, "Hotunplug and Hot plug the panel");
            foreach (DisplayType display in DisplayExtensions.pluggedDisplayList.Reverse<DisplayType>())
            {
                displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == display).First();
                if (displayInfo != null)
                {
                    if (base.HotUnPlug(displayInfo.DisplayType))
                    {
                        Log.Success("Display {0} is unplugged successfully", displayInfo.DisplayType);
                    }
                    else
                        Log.Fail("Failed to unplug display {0}", displayInfo.DisplayType);
                    if (base.HotPlug(displayInfo.DisplayType))
                    {
                        Log.Success("Display {0} is plugged successfully", displayInfo.DisplayType);
                    }
                    else
                        Log.Fail("Failed to plug display {0}", displayInfo.DisplayType);
                }
            }                  
        }   
    }
}