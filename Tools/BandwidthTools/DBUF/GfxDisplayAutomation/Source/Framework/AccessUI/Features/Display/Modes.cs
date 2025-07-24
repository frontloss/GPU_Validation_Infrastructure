namespace Intel.VPG.Display.Automation
{
    public class Modes : ComboHandler, IGet, ISet, IGetAll
    {
        public Modes()
            : base(DisplaySettingsRepo.Instance.FormIntelR_Graphics_and_Medi.ComboBoxComboResolution, "ComboResolution")
        { }
    }
}
