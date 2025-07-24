namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using System;
    using System.Threading;
    using System.Windows.Forms;
    using System.IO;
    using System.Diagnostics;
    using System.Drawing;
    using Microsoft.Win32;

    class SB_DisplayCStates_MBO : SB_DisplayCStates_BasicFeature
    {
        private bool isProcessExitReq = true;
        private uint DMCVersion = 0;
        [Test(Type = TestType.PreCondition, Order = 0)]
        public void DC_State()
        {
            DMCVersion = GetRegisterValue("DMC_VERSION", PIPE.NONE, PLANE.NONE, PORT.NONE);
            Log.Message(true, "DMC Version for {0}", DMCVersion);
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
        }
        [Test(Type = TestType.Method, Order = 2)]
        public override void Method()
        {
            PlayVideo();

        }

        [Test(Type = TestType.Method, Order = 3)]
        public void DCState()
        {
            Log.Message(true, "Verify DC-State on the system with MBO clip playing for 2 minutes.");
            List<DCStateOutput> returnType = new List<DCStateOutput>();
            if (isEDP)
                returnType = base.DisplayCStateEDP(isBXT, true, false);
            else
                returnType = base.DisplayCStateMIPI(isVideo, true);
            if (returnType.Count == 0)
            {
                Log.Success("Display C State not switched");
            }
            else
            {
                if (returnType.Contains(DCStateOutput.DC9) || returnType.Contains(DCStateOutput.DC6))
                    Log.Fail("DC6/DC9 state achieved");
                else
                    if (returnType.Contains(DCStateOutput.DC5))
                        Log.Fail("System Enabled upto DC5 only");
            }
        }
        [Test(Type = TestType.Method, Order = 4)]
        public void TestPostCondition()
        {
            StopVideo();
            base.TestPreCondition();
            base.Method();
        }
        private void PlayVideo()
        {
            Log.Message(true, "Play clip");
            if (!Directory.Exists(base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO"))
            {
                Log.Abort("Coun't find {0} SB to run the test", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");
            }
            if (isProcessExitReq)
            {
                Process[] explorerProcess = Process.GetProcessesByName("explorer");
                if (explorerProcess.Length > 0)
                {
                    foreach (Process p in explorerProcess)
                        p.Kill();
                }
            }
            CommonExtensions.StartProcess("explorer.exe", base.ApplicationManager.ApplicationSettings.DisplayToolsPath + "\\MBO");

            string fileName = Path.GetFileName("Wildlife.wmv");

            if (base.MachineInfo.OS.Type == OSType.WINTHRESHOLD)
                SendKeys.SendWait("{F11}");
            Thread.Sleep(3000);
            AccessInterface.SetFeature<bool, string>(Features.PlayMPOClip, Action.SetMethod, fileName);
            Thread.Sleep(3000);
        }
        private void StopVideo()
        {
            SendKeys.SendWait("%{F4}");
            Thread.Sleep(1000);
            Process[] explorerProcess = Process.GetProcessesByName("explorer");
            if (explorerProcess.Length > 0)
            {
                foreach (Process p in explorerProcess)
                    p.Kill();
            }
            isProcessExitReq = false;
        }
    }
}