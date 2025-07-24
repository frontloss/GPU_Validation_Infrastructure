namespace Intel.VPG.Display.Automation
{
    class OptionsTile : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting Options Tile");
            TilesRepo.Instance.FormIntelLParenRRParen_Graph.Options.Press();
        }
    }
}
