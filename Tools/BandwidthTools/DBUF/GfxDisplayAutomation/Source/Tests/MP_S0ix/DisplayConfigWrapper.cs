namespace Intel.VPG.Display.Automation
{
    class DisplayConfigWrapper
    {
        private DisplayConfig dispConfig = null;

        public DisplayConfigWrapper(DisplayConfig argDispConfig)
        {
            dispConfig = argDispConfig;
        }

        public DisplayConfig DispConfig
        {
            get
            {
                return dispConfig;
            }

        }
    }
}
