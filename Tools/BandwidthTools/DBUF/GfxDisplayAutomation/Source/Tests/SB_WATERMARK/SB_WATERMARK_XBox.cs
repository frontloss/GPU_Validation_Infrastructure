using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Windows.Forms;
using System.Linq;

namespace Intel.VPG.Display.Automation
{
    class SB_WATERMARK_XBox : SB_MODES_Base
    {
        public SB_WATERMARK_XBox()
        {
            base._verifyWatermark = true;
        }

        [Test(Type = TestType.PreCondition, Order = 0)]
        public void TestStep0()
        {
            if (base.CurrentConfig.ConfigTypeCount != base.CurrentConfig.DisplayList.Count())
                Log.Abort("This test requires atleast {0} displays , current display count: {1}", base.CurrentConfig.ConfigTypeCount, base.CurrentConfig.DisplayList.Count());

            ApplyConfigOS(base.CurrentConfig);
        }

        [Test(Type = TestType.Method, Order = 1)]
        public void TestStep1()
        {
            PlayVideo();

            base.CurrentConfig.CustomDisplayList.ForEach(disp => base.CheckWatermark(disp));

            StopVideo();
        }

        protected void PlayVideo()
        {
            Log.Message(true, "Play clip");
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO"))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");
            }
            CommonExtensions.KillProcess("explorer");

            CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");

            string fileName = Path.GetFileName("Wildlife.wmv");

            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
                SendKeys.SendWait("{F11}");
            Thread.Sleep(3000);
            AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
            Thread.Sleep(3000);
        }
        protected void StopVideo()
        {
            Log.Message("Stopping Video");
            SendKeys.SendWait("%{F4}");
            Thread.Sleep(1000);
            Process[] explorerProcess = Process.GetProcessesByName("explorer");
            if (explorerProcess.Length > 0)
            {
                foreach (Process p in explorerProcess)
                    p.Kill();
            }
        }

    }
}
