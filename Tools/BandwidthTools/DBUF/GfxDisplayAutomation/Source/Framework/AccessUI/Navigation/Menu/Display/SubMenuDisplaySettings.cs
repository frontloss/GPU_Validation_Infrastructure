namespace Intel.VPG.Display.Automation
{
    public class SubMenuDisplaySettings : MainMenu, INavigate
    {
        public void Navigate()
        {
            base.SelectMainMenu();
            base.Navigate(MenuRepo.Instance.FormIntelLParenRRParen_Graph.MenuItemDisplay_Settings);
        }
    }
}
