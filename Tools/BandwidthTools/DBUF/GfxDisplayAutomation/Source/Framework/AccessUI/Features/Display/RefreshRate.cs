namespace Intel.VPG.Display.Automation
{
    public class RefreshRate : ComboHandler, IGet, ISet, IGetAll
    {
        public RefreshRate()
            : base(DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboRefreshRate, "ComboRefreshRate")
        { }
    }
}
