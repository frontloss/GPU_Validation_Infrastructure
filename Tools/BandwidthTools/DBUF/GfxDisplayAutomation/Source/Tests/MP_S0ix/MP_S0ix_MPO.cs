namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using System.Threading.Tasks;
    using System.Windows.Forms;

    [Test(Type = TestType.ConnectedStandby)]
    class MP_S0ix_MPO : MP_S0ixBase
    {
        [Test(Type = TestType.Method, Order = 1)]
        public void SetConfigMethod()
        {
            Log.Message(true, "Set display Config using Windows API");
            if (AccessInterface.SetFeature<bool, DisplayConfig>(Features.Config, Action.SetMethod, base.CurrentConfig))
            {
                Log.Success("Config applied successfully");
                Log.Message("Set the maximum display mode on all the active displays");
            }
            else
            {
                Log.Abort("Config not applied!");
            }
        }

        [Test(Type = TestType.Method, Order = 2)]
        public void RunMPO()
        {
            Log.Message(true, "Play MPO Clip");
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.MPOClipPath))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.MPOClipPath);
            }
            string[] files = Directory.GetFiles(base.ApplicationManager.ApplicationSettings.MPOClipPath);
            string fileName = Path.GetFileName(files[0]);
            CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.MPOClipPath);
            SendKeys.SendWait("{F11}");
            Thread.Sleep(10000);
            AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
            Thread.Sleep(15000);
        }

        [Test(Type = TestType.Method, Order = 3)]
        public void RunMPOInSnapeMode()
        {
            Log.Message(true, "Play MPO Clip in Snape mode");
            Process mpoSnapBasicProcess = new Process();
            Process.Start("Execute.exe", " MP_ULT_MPO_Snap_Basic SD EDP").WaitForExit();
        }

        [Test(Type = TestType.Method, Order = 4)]
        public void SendSystemToS0ix()
        {
            Log.Message(true, "Go to S0i3 & wait for 30 sec and resume");
            base.CSCall();
        }

        [Test(Type = TestType.Method, Order = 5)]
        public void RunMPOAgain()
        {
            RunMPO();
        }
    }
}
