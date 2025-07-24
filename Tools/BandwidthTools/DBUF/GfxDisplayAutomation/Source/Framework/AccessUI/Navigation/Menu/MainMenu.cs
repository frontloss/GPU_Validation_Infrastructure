namespace Intel.VPG.Display.Automation
{
    using Ranorex;

    public class MainMenu
    {
        private MenuItem _menuItem = null;

        protected MenuItem MenuItem
        {
            get
            {
                Log.Verbose("Selecting {0} menu item", this._menuItem.Text);
                return this._menuItem;
            }
            set { this._menuItem = value; }
        }
        protected void SelectMainMenu()
        {
            this.MenuItem = MenuRepo.Instance.FormIntelLParenRRParen_Graph.MainMenuItem;
            this.MenuItem.FocusEnter();
        }
        protected void Navigate(MenuItem argContext)
        {
            this.MenuItem = argContext;
            this.MenuItem.FocusEnter();
            this.MenuItem.Retry(this.SelectMainMenu, MenuRepo.Instance.FormIntelLParenRRParen_Graph.TitleBlock);
        }
    }
}