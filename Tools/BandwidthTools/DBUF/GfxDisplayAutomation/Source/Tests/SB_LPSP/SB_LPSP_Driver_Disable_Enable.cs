namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class SB_LPSP_Driver_Disable_Enable : SB_LPSP_Base
    {
        
        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            foreach (KeyValuePair<System.Action, System.Action> _CurrentModeType in _applyMode)
            {
                //Step - 1 
                _CurrentModeType.Key();                

                //Step - 2
                base.AssertDriverState(Features.DisableDriver, DriverState.Disabled, new[] { 1, 1 });

                // Step - 3
                base.AssertDriverState(Features.EnableDriver, DriverState.Running, new[] { 1, 1 });
                
                System.Threading.Thread.Sleep(3000);
                
                // Step - 4
                Log.Message(true,"Verify LPSP Register");
                _CurrentModeType.Value();
            }
        }        
    }

}