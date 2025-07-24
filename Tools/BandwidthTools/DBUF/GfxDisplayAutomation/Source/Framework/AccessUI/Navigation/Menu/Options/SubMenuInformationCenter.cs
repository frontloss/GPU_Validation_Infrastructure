namespace Intel.VPG.Display.Automation
{
    public class SubMenuInformationCenter : MainMenu, INavigate
    {
        public void Navigate()
        {
            base.SelectMainMenu();
            base.Navigate(MenuRepo.Instance.FormIntelLParenRRParen_Graph.MenuItemInformation_Center);
        }
    }
}
