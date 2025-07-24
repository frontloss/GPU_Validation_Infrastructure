namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Text;
    using System.Threading;
    using System.Windows.Forms;

    public class ACPIFunctions : FunctionalBase, IGet, ISetMethod, IParse
    {

        private List<KeyCode> listKeyCode = new List<KeyCode>();
        KeyPress keyPress = new KeyPress();

        public object Get
        {
            get { return SystemInformation.PowerStatus.PowerLineStatus; }
        }
        public bool SetMethod(object argMessage)
        {
            
            FunctionKeys fnKey;
            if (Enum.TryParse(argMessage.ToString(), true, out fnKey))
            {
                if (fnKey == FunctionKeys.F5)
                {
                    string switchPowerOption = SystemInformation.PowerStatus.PowerLineStatus == PowerLineStatus.Online ? "DC" : "AC";
                    Log.Verbose("Switch to power source {0}. Current is {1}", switchPowerOption, SystemInformation.PowerStatus.PowerLineStatus);
                    PowerLineStatus switchState = SystemInformation.PowerStatus.PowerLineStatus == PowerLineStatus.Online ? PowerLineStatus.Offline : PowerLineStatus.Online;
                    return this.SwitchACDC(switchState);
                }
                else if(fnKey == FunctionKeys.F11)
                {
                   return ApplyScaling();
                }
                Log.Verbose("Switching using {0}", fnKey);
                Process acpiSwitchProcess = CommonExtensions.StartProcess("ACPISwitching.exe", fnKey.ToString());
                Thread.Sleep(6000);
                return acpiSwitchProcess.HasExited;
            }
            Log.Alert("FunctionKey {0} is not supported!", argMessage);
            return false;
        }

        private Boolean ApplyScaling()
        {
            Modes modes = base.CreateInstance<Modes>(new Modes());
            Config config = base.CreateInstance<Config>(new Config());
            Scaling objscaling = base.CreateInstance<Scaling>(new Scaling());
            List<ScalingOptions> allscalingOptionList =  new List<ScalingOptions>();
            //union of all supported scaling for all active display
            DisplayConfig dispconfig = (DisplayConfig)config.Get;
            foreach (DisplayType disptype in dispconfig.CustomDisplayList)
            {
                List<ScalingOptions> lstscalingoptions = (List<ScalingOptions>)objscaling.GetAllMethod(disptype);
                foreach (ScalingOptions scoption in lstscalingoptions)
                {
                    if (!allscalingOptionList.Contains(scoption) && scoption != ScalingOptions.Maintain_Aspect_Ratio)
                    {
                        allscalingOptionList.Add(scoption);
                    }
                }
            }
            Log.Message(true, "Performing ACPI Hotkey F11");
            //for loop to apply scaling from union list
            Process[] Gfxv4 = null;
            int unionscalingoptions = allscalingOptionList.Count;
            for (int scalingindex = 1; scalingindex <= unionscalingoptions; scalingindex++)
            {
                if (base.MachineInfo.OS.Type == OSType.WIN7)
                {
                    listKeyCode.Add(KeyCode.ALT);
                    listKeyCode.Add(KeyCode.CONTROL);
                    listKeyCode.Add(KeyCode.F11);
                    keyPress.SetMethod(listKeyCode);
                }
                else
                {
                    SendKeys.SendWait("%^{F11}");
                }
                Thread.Sleep(5000);
                Gfxv4 = Process.GetProcessesByName("Gfxv4_0");
                if (Gfxv4.Length > 0)
                {
                    IntPtr hPtr = Gfxv4[0].MainWindowHandle;
                    Interop.SetForegroundWindow(hPtr);
                    for (int tabcount = 0; tabcount <= scalingindex; tabcount++)
                    {
                        SendKeys.SendWait("{TAB}");
                    }
                    System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                    Thread.Sleep(3000);
                }
                foreach (DisplayType display in dispconfig.CustomDisplayList)
                {
                    DisplayScaling displayscaling = (DisplayScaling)objscaling.GetMethod(display);
                    if (displayscaling.scaling != ScalingOptions.None)
                    {
                        if (allscalingOptionList.Contains(displayscaling.scaling))
                        {
                            allscalingOptionList.Remove(displayscaling.scaling);
                        }
                    }
                }
            }

            if (Gfxv4.Length > 0)
            {
                foreach (Process Process in Gfxv4)
                {
                    Process.Close();
                }

            }
            //Check if all available scalig options are applied from the union list.
            if (allscalingOptionList.Count > 0)
            {
                foreach (ScalingOptions scaleoption in allscalingOptionList)
                {
                    Log.Fail("ACPI hotkey switch failed to apply scaling {0}", scaleoption.ToString());
                }
                return false;
            }
            else
            {
                Log.Success("ACPI hotkey switch successfully applied all scaling options");
            }
            
            return true;
        }

        
        [ParseAttribute(InterfaceName = InterfaceType.ISetMethod, InterfaceData = new string[] { "FunctionKeys:FunctionKey" }, Comment = "Performs ACPI for the key")]
        [ParseAttribute(InterfaceName = InterfaceType.IGet, Comment = "Gets the power status")]
        public void Parse(string[] args)
        {
            if (args.Length > 1)
            {
                FunctionKeys fnKey;
                if (args[0].ToLower().Contains("set") && Enum.TryParse(args[1], true, out fnKey))
                {
                    if (this.SetMethod(fnKey))
                        Log.Verbose("{0} function successful", fnKey);
                    else
                        Log.Alert("{0} function unsuccessful!", fnKey);
                }
                else if (args[0].ToLower().Contains("get"))
                {
                    PowerLineStatus state = (PowerLineStatus)this.Get;
                    if (state == PowerLineStatus.Online)
                        Log.Message("System is Running in AC Mode");
                    else if (state == PowerLineStatus.Offline)
                        Log.Message("System is Running in DC Mode");
                    else
                        Log.Alert("System power status unknown {0}", state);
                }
            }
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Execute ACPIFunctions get [applicable only to receive AC/DC state]").Append(Environment.NewLine);
            sb.Append("..\\>Execute ACPIFunctions set F1|F2|F3|F4|F5|F9|F10").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        private bool SwitchACDC(PowerLineStatus argCurrentState)
        {
            bool Status = false;
            if (base.MachineInfo.OS.Type == OSType.WIN7)
            {
                CommonExtensions.StartProcess("HotKey_ACDC.exe");
                Thread.Sleep(6000);
                if (SystemInformation.PowerStatus.PowerLineStatus == argCurrentState)
                    Status = true;
            }
            else
            {
                if (false == CommonExtensions.VerifyWDTFStatus())
                {
                    Log.Abort("Windows Driver Testing Framework (WDTF) was not installed on test machine");
                }
                if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.SimulatedBattery))
                {
                    TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.SimulatedBattery, null);
                    CommonExtensions.StartProcess(@"cscript", "SimulatedBattery_Control.vbs /setup", 0).WaitForExit();
                    Thread.Sleep(6000);
                }
                if (argCurrentState == PowerLineStatus.Offline)
                {
                    CommonExtensions.StartProcess(@"cscript", "SimulatedBattery_Control.vbs /dc", 0).WaitForExit();
                    Thread.Sleep(6000);
                    if (SystemInformation.PowerStatus.PowerLineStatus == PowerLineStatus.Offline)
                        Status = true;
                }
                else if (argCurrentState == PowerLineStatus.Online)
                {
                    CommonExtensions.StartProcess(@"cscript", "SimulatedBattery_Control.vbs /ac", 0).WaitForExit();
                    Thread.Sleep(6000);
                    if (SystemInformation.PowerStatus.PowerLineStatus == PowerLineStatus.Online)
                        Status = true;
                }
            }
            return Status;
        }
    }
}
