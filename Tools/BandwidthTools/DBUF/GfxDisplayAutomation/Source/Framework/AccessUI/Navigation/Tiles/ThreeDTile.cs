namespace Intel.VPG.Display.Automation
{
    class ThreeDTile : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting 3D Tile");
            TilesRepo.Instance.FormIntelLParenRRParen_Graph.ThreeD.Press();
        }
    }
}
