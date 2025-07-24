namespace Intel.VPG.Display.Automation
{
    using System.Threading;
    using System.Diagnostics;
    using System.Windows.Forms;
    using System;

    internal class MonitorTurnOff : FunctionalBase, ISetMethod
    {
        private const int MOUSEEVENTF_LEFTDOWN = 0x02;
        private const int MOUSEEVENTF_LEFTUP = 0x04;
        private const int MOUSEEVENTF_MOVE = 0x01;
        public bool SetMethod(object argMessage)
        {
            // Verify System is CS/S0ix Enable system or not. If System is CS enable system
            // we should not perform monitor turn off, because once monitor if off system will
            // go to low power state. and Automation application can not resume from CS state.
            // So system will remain in CS state forever unless we manually do keyboard or mouse event.

            if (DisplayExtensions.VerifyCSSystem(base.AppManager.MachineInfo))
            {
                Log.Abort("Monitor turn off/on will not work on CS enable system");
                return false;
            }

            MonitorTurnOffParam monitorOffOnParam = argMessage as MonitorTurnOffParam;
            if (monitorOffOnParam.onOffParam == MonitorOnOff.Off)
            {
                TurnOffMonitor(monitorOffOnParam);
                DisplayExtensions.EnableMonitorTurnOff = true;
            }
            else if (monitorOffOnParam.onOffParam == MonitorOnOff.On)
            {
                Log.Verbose("Turning on monitor and verify");
                TurnOnMonitor();
                DisplayExtensions.EnableMonitorTurnOff = false;
                Thread.Sleep(6000);
            }
            else if (monitorOffOnParam.onOffParam == MonitorOnOff.OffOn)
            {
                TurnOffMonitor(monitorOffOnParam);
                DisplayExtensions.EnableMonitorTurnOff = true;
                Log.Verbose("Turning on monitor and verify");
                TurnOnMonitor();

                DisplayExtensions.EnableMonitorTurnOff = false;
                Thread.Sleep(6000);
            }

            if (base.AppManager.HotplugUnplugCntx.PlugUnplugInLowPower == true)
            {
                PlugUnPlugEnumeration plugUnPlugEnum = base.CreateInstance<PlugUnPlugEnumeration>(new PlugUnPlugEnumeration());
                foreach (HotPlugUnplug HT in base.AppManager.HotplugUnplugCntx.HotPlugUnPlugInfo)
                {
                    plugUnPlugEnum.SetMethod(HT);
                }
            }
            return true;
        }

        private void TurnOnMonitor()
        {
            int MOUSEEVENTF_MOVE = 0x01;
            Interop.mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0);
        }

        private void TurnOffMonitor(MonitorTurnOffParam monitorOffOnParam)
        {
            const int SC_MONITORPOWER = 0xF170;
            const int WM_SYSCOMMAND = 0x0112;
            const int MONITOR_OFF = 2;

            Form tempWindow = new Form();
            if (tempWindow.Handle != null)
            {
                Log.Verbose("Turning off monitor for {0} sec", monitorOffOnParam.waitingTime);
                Interop.SendMessage(tempWindow.Handle, WM_SYSCOMMAND, (IntPtr)SC_MONITORPOWER, (IntPtr)MONITOR_OFF);
                if (monitorOffOnParam.waitingTime != 0)
                    Thread.Sleep((monitorOffOnParam.waitingTime * 1000));
                else
                    Thread.Sleep(60000); //else wait for 60 Sec
            }
            else
            {
                Log.Abort("Fail to get current window Handle");
            }
        }
    }
}