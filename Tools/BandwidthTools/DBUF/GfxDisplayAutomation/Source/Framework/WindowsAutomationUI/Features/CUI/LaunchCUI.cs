namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Collections.Generic;
    using System.Windows.Automation;
    using System.Windows.Forms;
    using System.Runtime.InteropServices;
    using System.Threading;
    using System.Timers;
    using System.Diagnostics;
    using System.IO;

    public class LaunchCUI : FunctionalBase, ISetNoArgs, IVisible, IParse, ISetMethod
    {
        private DecisionActions _decisionActions = DecisionActions.Yes;
        private List<KeyCode> listKeyCode = new List<KeyCode>();
        private UIABaseHandler uiaBaseHandler = new UIABaseHandler();
        KeyPress keyPress = new KeyPress();

        public bool SetMethod(object argMessage)
        {
            Enum.TryParse(argMessage.ToString(), true, out this._decisionActions);
            return this.SetNoArgs();
        }
        public bool SetNoArgs()
        {
            Log.Abort("Not Launching CUI since, Since we migrated to CUI SDK");

            Process.GetProcesses().Where(p => p.ProcessName.StartsWith("Gfx")).ToList().ForEach(p =>
            {
                Log.Verbose("Close CUI");
                p.Kill();
            });
            Log.Verbose("Launching CUI using Hotkeys (in Windows Automation UI)");
            listKeyCode.Add(KeyCode.ALT);
            listKeyCode.Add(KeyCode.CONTROL);
            listKeyCode.Add(KeyCode.F12);
            keyPress.SetMethod(listKeyCode);
            Thread.Sleep(3000);
            DateTime startTime = DateTime.Now;
            while (startTime.AddSeconds(50) > DateTime.Now)
            {
                if (this.Visible)
                {
                    Log.Verbose("Driver.baseline:: {0}", base.MachineInfo.Driver.DriverBaseLine);
                    UIExtensions.Load(base.AppSettings, base.MachineInfo.Driver.DriverBaseLine);
                    CommonExtensions.Init(base.MachineInfo.Driver.DriverBaseLine);

                    CUIHeaderOptions cuiHeaderOptions = base.CreateInstance<CUIHeaderOptions>(new CUIHeaderOptions());
                    cuiHeaderOptions.Set = CUIWindowOptions.Maximize;
                    return true;
                }
            }
            if (this._decisionActions == DecisionActions.No)
                return false;
            else
            {
                Log.Sporadic(false, "CUI not launched using Hot Keys!");
                DTCMShowDesktop dtcmShowDesktop = base.CreateInstance<DTCMShowDesktop>(new DTCMShowDesktop());
                dtcmShowDesktop.Set = "DTCMDesktop";

                DTCMFeature dtcmFeature = base.CreateInstance<DTCMFeature>(new DTCMFeature());
                Log.Verbose("Preparing Navigation List for {0}", Features.DTCMHotKeys);
                Dictionary<string, string> navigationList = CommonExtensions.GetNavigationList(Features.DTCMHotKeys);
                navigationList.ToList().ForEach(kV =>
                {
                    UIExtensions.setUIAEntity(kV.Key);
                });
                navigationList.ToList().ForEach(kV =>
                {
                    if (dtcmFeature.SetMethod(kV.Key))
                        Log.Verbose("Successfully moved to {0}", kV.Key);
                });
                Log.Verbose("Trying to launch CUI using Hot Keys once again!");
                keyPress.SetMethod(listKeyCode);
                if (!this.Visible && !CommonExtensions.HasRetryThruRebootFile())
                {
                    Log.Sporadic(false, "CUI not launched again using Hot Keys! A reboot might be required.");
                    CommonExtensions.WriteRetryThruRebootInfo();
                    return AccessUIExtensions.RebootHandler(base.CurrentMethodIndex);
                }
                else
                    CommonExtensions.ClearRetryThruRebootFile();
                return true;
            }

        }
        public bool Visible
        {
            get
            {
                AutomationElement displayTile = UIABaseHandler.SelectElementNameAutomationId(AutomationElement.RootElement, "Display", "TextOnTile");
                if (displayTile != null)
                {
                    string[] driverBaselineFiles = Directory.GetFiles(Directory.GetCurrentDirectory());
                    if (Path.GetFileNameWithoutExtension(driverBaselineFiles.First()).StartsWith("15."))
                        return true;
                    else
                    {
                        Log.Verbose("Get Driver Version from CUI");
                        uiaBaseHandler.TilesInvoke(displayTile);
                        AutomationElement colorSettings = UIABaseHandler.SelectElementAutomationIdControlType("MenuList_1", ControlType.RadioButton);
                        if (colorSettings != null)
                        {
                            System.IO.File.Create(string.Concat(Directory.GetCurrentDirectory(), "\\15.40.tmp"));
                            if (!(base.MachineInfo.Driver.DriverBaseLine.Equals("15.40")))
                            {
                                base.MachineInfo.Driver.DriverBaseLine = "15.40";
                            }
                        }
                        else
                        {
                            colorSettings = UIABaseHandler.SelectElementNameControlType("Color Settings", ControlType.RadioButton);
                            if (colorSettings != null)
                            {
                                System.IO.File.Create(string.Concat(Directory.GetCurrentDirectory(), "\\15.36.tmp"));
                                if (!(base.MachineInfo.Driver.DriverBaseLine.Equals("15.36")))
                                {
                                    base.MachineInfo.Driver.DriverBaseLine = "15.36";
                                }
                            }
                            else
                            {
                                System.IO.File.Create(string.Concat(Directory.GetCurrentDirectory(), "\\15.33.tmp"));
                                if (!(base.MachineInfo.Driver.DriverBaseLine.Equals("15.33")))
                                {
                                    base.MachineInfo.Driver.DriverBaseLine = "15.33";
                                }
                            }
                        }
                        Log.Verbose("Return to Home Button");
                        AutomationElement backButton = UIABaseHandler.SelectElementAutomationIdControlType("HomeButton", ControlType.Button);
                        if (backButton != null)
                            uiaBaseHandler.SendKey(backButton);
                        return true;
                    }
                }
                else
                    return false;
            }
        }
        public void Parse(string[] args)
        {
            if (args.Length > 0 && args[0].Equals("set"))
                this.SetNoArgs();
            else
                this.HelpText();
        }

        private void HelpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append(@"..\>Execute LaunchCUI set").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
    }
}
