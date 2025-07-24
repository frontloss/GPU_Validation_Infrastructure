namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Linq;
    using System.Windows.Forms;
    using System.Threading;
    using System.IO;
    using System.Diagnostics;
    using System.Text.RegularExpressions;

    class MP_48Hz_AC_DC : MP_48Hz_Basic
    {
        [Test(Type = TestType.Method, Order = 4)]
        public override void TestStep4()
        {
            base.TestStep4();

            Log.Message(true, "Enable DC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Online)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in DC Mode");
                else
                    Log.Fail("Fail to set DC Mode");
            }
            else
                Log.Success("System is Running in DC Mode");
            DisplayInfo displayInfo = base.CurrentConfig.EnumeratedDisplays.Where(dI => dI.DisplayType == base.GetInternalDisplay()).First();
            DisplayMode currentMode = AccessInterface.GetFeature<DisplayMode, DisplayInfo>(Features.Modes, Action.GetMethod, Source.AccessAPI, displayInfo);
            string[] rrValue = Regex.Split(currentRR.Trim(), @"\D+");
            if (rrValue.Length != 0)
            {
                currentMode.RR = Convert.ToUInt32(rrValue.First());
                if (!AccessInterface.SetFeature<bool, DisplayMode>(Features.Modes, Action.SetMethod, currentMode))
                {
                    Log.Fail("Fail to Apply Mode");
                }
            }
        }

        [Test(Type = TestType.Method, Order = 7)]
        public void TestStep7()
        {
            Log.Message(true, "Enable AC Mode");
            PowerLineStatus powerState = (PowerLineStatus)AccessInterface.GetFeature<PowerLineStatus>(Features.ACPIFunctions, Action.Get);

            if (powerState == PowerLineStatus.Offline)
            {
                if (AccessInterface.SetFeature<bool, FunctionKeys>(Features.ACPIFunctions, Action.SetMethod, FunctionKeys.F5))
                    Log.Success("System is Running in AC Mode");
                else
                    Log.Fail("Fail to set AC mode");
            }
            else
                Log.Success("System is Running in AC Mode");
            base.TestStep5();
            base.TestStep6();
        }
    }
}
