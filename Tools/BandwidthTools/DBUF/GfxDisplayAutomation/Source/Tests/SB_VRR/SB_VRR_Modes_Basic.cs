using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Intel.VPG.Display.Automation
{
    class SB_VRR_Modes_Basic : SB_VRR_Base
    {
        [Test(Type = TestType.PreCondition, Order = 0)]
        public virtual void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());
        }
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            DisplayList VrrSupportedDisplayList = new DisplayList();
            GetVRRCapableDisplays(VrrSupportedDisplayList);
            if (VrrSupportedDisplayList.Count == 0)
                Log.Abort("This test requires VRR capable displays. None of the connected displays are VRR capable.");
            
            base.ApplyConfigOS(base.CurrentConfig);
            base.VerifyConfigOS(base.CurrentConfig);

            List<DisplayModeList> allModeList = AccessInterface.GetFeature<List<DisplayModeList>, List<DisplayType>>(Features.Modes, Action.GetAllMethod, Source.AccessAPI, base.CurrentConfig.DisplayList);
            allModeList.ForEach(modeList =>
                {
                    List<DisplayMode> supportedModes = modeList.supportedModes;
                    if (supportedModes.Count() != 0)
                    {
                        Log.Message(true, "Applying modes on disp: {0}", modeList.display.ToString());
                        base.ApplyModeOS(supportedModes.First(), modeList.display);
                        base.VerifyModeOS(supportedModes.First(), modeList.display);
                        VrrSupportedDisplayList.ForEach(disp =>
                        {
                            base.VerifyVRR(disp);
                        });


                        base.ApplyModeOS(supportedModes.Last(), modeList.display);
                        base.VerifyModeOS(supportedModes.Last(), modeList.display);
                        VrrSupportedDisplayList.ForEach(disp =>
                        {
                            base.VerifyVRR(disp);
                        });


                        if (supportedModes.Count() != 1)
                        {
                            base.ApplyModeOS(supportedModes.ElementAt(supportedModes.Count() / 2), modeList.display);
                            base.VerifyModeOS(supportedModes.ElementAt(supportedModes.Count() / 2), modeList.display);
                            VrrSupportedDisplayList.ForEach(disp =>
                            {
                                base.VerifyVRR(disp);
                            });
                        }
                        base.ApplyModeOS(supportedModes.Last(), modeList.display);
                    }
                });
        }
      
    }
}
