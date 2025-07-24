namespace Intel.VPG.Display.Automation
{
    public class SubMenuMultipleDisplays : MainMenu, INavigate
    {
        public void Navigate()
        {
            base.SelectMainMenu();
            base.Navigate(MenuRepo.Instance.FormIntelLParenRRParen_Graph.MenuItemMultiple_Displays);
        }
    }
}
