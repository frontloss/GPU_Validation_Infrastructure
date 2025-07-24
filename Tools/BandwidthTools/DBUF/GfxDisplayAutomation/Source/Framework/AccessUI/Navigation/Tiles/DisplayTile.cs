namespace Intel.VPG.Display.Automation
{
    class DisplayTile : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting Display Tile");
            TilesRepo.Instance.FormIntelLParenRRParen_Graph.Display.Press();
        }
    }
}
