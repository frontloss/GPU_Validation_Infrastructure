namespace Intel.VPG.Display.Automation
{
    class VideoTile : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Selecting Video Tile");
            TilesRepo.Instance.FormIntelLParenRRParen_Graph.Video.Press();
        }
    }
}
