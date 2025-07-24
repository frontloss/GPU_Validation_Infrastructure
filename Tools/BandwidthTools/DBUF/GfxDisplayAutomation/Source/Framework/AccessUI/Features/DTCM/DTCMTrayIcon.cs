namespace Intel.VPG.Display.Automation
{
    using System;

    using Ranorex;
    using Ranorex.Core;

    class DTCMTrayIcon : FunctionalBase, ISet
    {
        public object Set
        {
            set
            {
                CUIHeaderOptions cuiHeaderOptions = new CUIHeaderOptions();
                cuiHeaderOptions.Set = CUIWindowOptions.Minimize;

                try
                {
                    Ranorex.Button button = DTCMRepo.Instance.MenuBarexplorer.ButtonIntelLParenRRParen_HD_Gr;
                    if (null == button)
                    {
                        Log.Verbose("TrayIcon button is null!");
                        this.LaunchViaDesktopMenu(value);
                    }
                    else
                    {
                        Log.Verbose("Launching Tray Icon menu");
                        button.Press(); //.Click();
                    }
                }
                catch (Exception ex)
                {
                    Log.Sporadic("{0}", ex.Message);
                    this.LaunchViaDesktopMenu(value);
                }
                Delay.Seconds(2);
            }
        }

        private void LaunchViaDesktopMenu(object argValue)
        {
            DTCMShowDesktop dtcmShowDesktop = new DTCMShowDesktop();
            dtcmShowDesktop.Set = argValue;
        }
    }
}