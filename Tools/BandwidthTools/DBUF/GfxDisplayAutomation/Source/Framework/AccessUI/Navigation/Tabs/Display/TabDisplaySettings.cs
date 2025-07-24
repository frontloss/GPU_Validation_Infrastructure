namespace Intel.VPG.Display.Automation
{
    public class TabDisplaySettings : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting DisplaySettings Tab");
            DisplayTabsRepo.Instance.IntelRHDGraphicsControlPanel.DisplaySettings.Select();
        }
    }
}
