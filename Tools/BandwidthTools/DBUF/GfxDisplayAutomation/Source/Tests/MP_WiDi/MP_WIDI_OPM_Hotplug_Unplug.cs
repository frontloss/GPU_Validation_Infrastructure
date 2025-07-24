namespace Intel.VPG.Display.Automation
{
    using System.Linq;

    [Test(Type = TestType.WiDi)]
    class MP_WIDI_OPM_Hotplug_Unplug : MP_WIDIBase
    {
         DisplayConfig config = new DisplayConfig();

         [Test(Type = TestType.Method, Order = 1)]
         public void InstallMEDrv()
         {
             if(VerifyMEDriver() == false)
                InstallMEDriver();   
         }

         [Test(Type = TestType.Method, Order = 2)]
         public void SetConfigMethod()
         {
             if (!base.CurrentConfig.CustomDisplayList.Any(D => D.Equals(DisplayType.WIDI)))
             {
                 Log.Abort("Command line dose not contains WIDI display, Hence Aborting test execution");
             }
             base.GetExternalDisplay();
             config.ConfigType = base.CurrentConfig.ConfigType;
             config.PrimaryDisplay = DisplayType.WIDI;
             if(base.CurrentConfig.DisplayList.Count == 2)
                 config.SecondaryDisplay = base.pDisplayList.First();
             else if (base.CurrentConfig.DisplayList.Count == 3)
             {
                 config.SecondaryDisplay = base.pDisplayList.First();
                 config.TertiaryDisplay = base.pDisplayList.Last();
             }

             Log.Message(true, "Set display Config using Windows API");
             this.SetNValidateConfig(config);
         }

         [Test(Type = TestType.Method, Order = 3)]
         public void RunOPMTesterNVerify()
         {
             base.RunOPMTester(config);
         }

         [Test(Type = TestType.Method, Order = 4)]
         public void UnPlugWIDIDisplayNPlugItback()
         {
             Log.Message(true, "Disconnect WIDI display and connect it back");
             DisplayConfig temp = new DisplayConfig();
             temp.ConfigType = DisplayConfigType.SD;
             temp.PrimaryDisplay = base.GetInternalDisplay();

             Log.Message(true, "Set Current config via OS call");
             if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, temp))
                 Log.Success("Config applied successfully");
             else
                 Log.Fail("Config not applied!");

             this.SetNValidateConfig(config);
             RunOPMTesterNVerify();
         }

         [Test(Type = TestType.Method, Order = 5)]
         public void HotUnplugNPlug()
         {
             if (base.externalDisplayList.Count > 0)
             {
                 Log.Message(true, "Hot unplug all external display and plug it back");
                 foreach (DisplayType DT in base.externalDisplayList)
                 {
                     if (base.HotUnPlug(DT))
                         Log.Success("Successfully hot unplug external display {0}", DT);
                     else
                         Log.Fail("Unable to hot unplug external display {0}", DT);
                 }
                 foreach (DisplayType DT in base.externalDisplayList)
                 {
                     if(base.HotPlug(DT))
                         Log.Success("Successfully hotplug external display {0}", DT);
                     else
                         Log.Fail("Unable to hotplug external display {0}", DT);
                 }

                 this.SetNValidateConfig(config);
                 RunOPMTesterNVerify(); 
             }
         }
    }
}
