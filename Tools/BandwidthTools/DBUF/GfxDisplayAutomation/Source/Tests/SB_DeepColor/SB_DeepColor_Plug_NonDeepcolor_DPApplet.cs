namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;

    [Test(Type = TestType.HasPlugUnPlug)]
    class SB_DeepColor_Plug_NonDeepcolor_DPApplet : SB_Deepcolor_DisplayConfig_DPApplet
    {
        public SB_DeepColor_Plug_NonDeepcolor_DPApplet()
            : base()
        {
            base._actionAfterEnable = this.ActionAfterEnable;
        }

        private void ActionAfterEnable()
        {
            Log.Message(true, "UnPlug Deepcolor panels and plug Non-DeepColor panels.");

            base.CurrentConfig.PluggableDisplayList.Intersect(_nonDeepColorEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                Log.Message("UnPlugging Deepcolor supported panel {0}.", curDisp);
                base.HotUnPlug(curDisp);

                Log.Message("Hotplug Non Deepcolor supported panel {0}.", curDisp);
                base.HotPlug(curDisp, _nonDeepColorEDIDMap[curDisp]);
            });

            AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig);

            base.TestStep2();

            base.CurrentConfig.PluggableDisplayList.Intersect(_nonDeepColorEDIDMap.Keys).ToList().ForEach(curDisp =>
            {
                Log.Message("Unplugging Non Deepcolor supported panel {0}.", curDisp);
                base.HotUnPlug(curDisp);

                Log.Message("Hotplug Deepcolor supported panel {0}.", curDisp);
                base.HotPlug(curDisp, _defaultEDIDMap[curDisp]);
            });
        }
    }
}