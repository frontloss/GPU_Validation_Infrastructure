namespace Intel.VPG.Display.Automation
{
    public class Home : INavigate
    {
        public void Navigate()
        {
            Log.Verbose("Clicking BackButton");
            HomeRepo.Instance.FormIntelLParenRRParen_Graph.BackButtonItem.Press();
        }
    }
}