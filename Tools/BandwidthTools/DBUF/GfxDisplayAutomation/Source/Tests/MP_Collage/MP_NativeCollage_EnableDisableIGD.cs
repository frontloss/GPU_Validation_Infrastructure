namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    class MP_NativeCollage_EnableDisableIGD : MP_NativeCollage_BAT
    {
        public MP_NativeCollage_EnableDisableIGD()
        {
            base._performAction = this.PerformAction;
            _myList = new List<DisplayConfigType>()
            {
                DisplayConfigType.Horizontal,
            };
        }
        private void PerformAction()
        {
            Log.Message(true, "Disable IGD from Device Manager");
            base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });
            Log.Message(true, "Enable the driver from Device manager.");
            base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });
            //Log.Message(true, "Verify that the display comes back in the same configuration after Disabling and Enabling the driver");
            
            //base.VerifyCollagePersistence(setConfigString, 0);
            if (base.CheckCollageThruResolution(displayConfig.ConfigType, currentMode, base.CurrentConfig.DisplayList.Count))
                Log.Success("{0} is verified to be successfully set using Resolutions after re-enabling driver", displayConfig.ConfigType);
            else
                Log.Fail("{0} is not verified using Resolutions after re-enabling driver", displayConfig.ConfigType);
        }
    }
}