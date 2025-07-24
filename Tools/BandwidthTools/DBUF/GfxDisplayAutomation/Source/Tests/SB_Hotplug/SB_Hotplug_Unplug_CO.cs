namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.IO;
    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_Hotplug_Unplug_CO : SB_Hotplug_Base
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
            });
            base.ApplyConfigOS(base.CurrentConfig);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public void TestStep2()
        {
            string fileCO = Path.Combine(Directory.GetCurrentDirectory(), "SB_Hotplug_CO.txt");
            string countStr = File.ReadAllText(fileCO);
            int count = Convert.ToUInt16(countStr.Trim());
            for (int index = 0; index < count; index++)
            {
                Log.Message("Performing Plug unplug count: {0}", index + 1);
                base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
                {
                    base.HotUnPlug(curDisp);
                });
                base.CurrentConfig.DisplayList.Intersect(base._defaultEDIDMap.Keys).ToList().ForEach(curDisp =>
                {
                    base.HotPlug(curDisp, base._defaultEDIDMap[curDisp]);
                });
                base.VerifyConfigOS(base.CurrentConfig);
            }
        }
    }
}
