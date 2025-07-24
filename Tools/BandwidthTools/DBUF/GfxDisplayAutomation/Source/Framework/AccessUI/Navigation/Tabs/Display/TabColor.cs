namespace Intel.VPG.Display.Automation
{
    public class TabColor : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting DisplayColor Tab");
            DisplayTabsRepo.Instance.IntelRHDGraphicsControlPanel.Color.Select();
        }
    }
}
