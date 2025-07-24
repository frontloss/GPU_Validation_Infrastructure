namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Linq;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.IO;

    using Ranorex;
    using System.Diagnostics;

    public class LaunchCUI : FunctionalBase, ISetNoArgs, IVisible, IParse, ISetMethod
    {
        private DecisionActions _decisionActions = DecisionActions.Yes;

        public bool SetMethod(object argMessage)
        {
            Enum.TryParse(argMessage.ToString(), true, out this._decisionActions);
            return this.SetNoArgs();
        }
        public bool SetNoArgs()
        {
            Process.GetProcesses().Where(p => p.ProcessName.StartsWith("Gfx")).ToList().ForEach(p =>
            {
                Log.Verbose("Close CUI");
                p.Kill();
                Log.Verbose("Closing CUI");
                    p.Kill();
            });

            Log.Verbose("Launching CUI using Hotkeys");
            Keyboard.Press("{LControlKey down}{LMenu down}{F12}{LMenu up}{LControlKey up}");
            if (this.Visible)
            {
                CUIHeaderOptions cuiHeaderOptions = new CUIHeaderOptions();
                base.CopyOver(cuiHeaderOptions);
                cuiHeaderOptions.Set = CUIWindowOptions.Maximize;
                return true;
            }
            else
            {
                if (this._decisionActions == DecisionActions.No)
                    return false;
                else
                {
                    Log.Sporadic(false, "CUI not launched using Hot Keys!");
                    DTCMShowDesktop dtcmShowDesktop = new DTCMShowDesktop() { Set = "DTCMDesktop" };
                    base.CopyOver(dtcmShowDesktop);
                    DTCMFeature dtcmFeature = new DTCMFeature();
                    base.CopyOver(dtcmFeature);
                    Log.Verbose("Preparing Navigation List for {0}", Features.DTCMHotKeys);
                    List<string> navList = Features.DTCMHotKeys.GetNavigationList().Values.Select(i => i.Replace("_", " ")).ToList();
                    if (dtcmFeature.SetMethod(navList))
                    {
                        if (dtcmFeature.Get.ToString().ToLower().Contains("disable"))
                        {
                            Log.Sporadic(false, "Hot Keys is not enabled in DTCM! Enabling Hot Keys via DTCM");
                            dtcmShowDesktop.Set = "DTCMDesktop";
                            dtcmFeature.ClearContext();
                            dtcmFeature.SetMethod(navList);
                            dtcmFeature.Set = "Enable";
                        }
                        else
                            Log.Verbose("Hotkey is enabled");
                        Log.Verbose("Trying to launch CUI using Hot Keys once again!");
                        Keyboard.Press("{LControlKey down}{LMenu down}{F12}{LMenu up}{LControlKey up}");
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
                    else
                    {
                        Log.Sporadic(false, "CUI not launched using Hot Keys! A reboot might be required.");
                        if (!CommonExtensions.HasRetryThruRebootFile())
                        {
                            CommonExtensions.WriteRetryThruRebootInfo();
                            return AccessUIExtensions.RebootHandler(base.CurrentMethodIndex);
                        }
                        else
                            CommonExtensions.ClearRetryThruRebootFile();
                        return false;
                    }
                }
            }
        }
        public bool Visible
        {
            get 
            {
                try { return TilesRepo.Instance.FormIntelLParenRRParen_Graph.Display.Visible; }
                catch { return false; }
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
