namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Text;
    using System.IO;
    using System.Collections.Generic;
    using Microsoft.Win32;

    [Test(Type = TestType.HasReboot)]
    class MP_NativeCollage_EnableDisable_INF : MP_NativeCollage_BAT
    {
        protected string _infPath = string.Empty;
        private RegistryParams registryParams = new RegistryParams();
        public MP_NativeCollage_EnableDisable_INF()
        {
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
            };
            registryParams.registryKey = Registry.LocalMachine;
        }
        [Test(Type = TestType.Method, Order = 1)]
        public override void TestStep1()
        {
            Log.Message(true, "Make Inf Changes in Registry for a Collage Disabled Driver");
            registryParams.keyName = "Enable4KDisplay";
            registryParams.value = 0;
            registryParams.infChanges = InfChanges.ModifyInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
            registryParams.keyName = "CollageModeFeature";
            registryParams.value = 0;
            registryParams.infChanges = InfChanges.ModifyInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void TestStep2()
        {
            Log.Message(true, "Verify that the Collage option is disabled");
            base.collagepar.option = CollageOption.IsCollageSupported;
            CollageParam collageStatus = AccessInterface.GetFeature<CollageParam, CollageParam>(Features.Collage, Action.GetMethod, Source.AccessAPI, base.collagepar);
            if (!collageStatus.isCollageSupported)
                Log.Success("Collage option is not supported in Collage Disabled Driver");
            else
                Log.Abort("Collage option is still supported after installing Collage Disabled Driver");
        }
        [Test(Type = TestType.Method, Order = 3)]
        public void TestStep3()
        {
            Log.Message(true, "Make Inf Changes in Registry for a Collage Enabled Driver");
            registryParams.keyName = "Enable4KDisplay";
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.RevertInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestStep4()
        {
            registryParams.keyName = "CollageModeFeature";
            registryParams.value = 1;
            registryParams.infChanges = InfChanges.RevertInf;
            AccessInterface.SetFeature<bool, RegistryParams>(Features.RegistryInf, Action.SetMethod, registryParams);
        }
        [Test(Type = TestType.Method, Order = 5)]
        public void TestStep5()
        {
            foreach (DisplayType DT in base.CurrentConfig.PluggableDisplayList)
            {
                Log.Verbose("Display {0} is not enumerated after enabling Gfx Driver, plugging it back", DT);
                base.HotPlug(DT);
            }
            Log.Message(true, "Verify that the Collage option is enabled");

            base.collagepar.option = CollageOption.IsCollageSupported;
            CollageParam collageStatus = AccessInterface.GetFeature<CollageParam, CollageParam>(Features.Collage, Action.GetMethod, Source.AccessAPI, base.collagepar);
            if (collageStatus.isCollageSupported)
                Log.Success("Collage option is supported in Collage Enabled Driver");
            else
                Log.Abort("Collage option is not supported even after installing a Collage Enabled Dricer");

            base.TestStep0();
            base.TestStep1();
            base.TestStep2();
            //TestStep3();
        }
    }
}