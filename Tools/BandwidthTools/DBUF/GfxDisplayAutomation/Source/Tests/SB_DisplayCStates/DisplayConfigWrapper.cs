namespace Intel.VPG.Display.Automation
{
    class DisplayConfigWrapper
    {
        private DisplayConfig dispConfig = null;
        private bool useCUI = false;

        public DisplayConfigWrapper(DisplayConfig argDispConfig)
        {
            dispConfig = argDispConfig;
        }

        public DisplayConfigWrapper(DisplayConfig argDispConfig, bool argUseCUI)
        {
            dispConfig = argDispConfig;
            useCUI = argUseCUI;
        }

        public DisplayConfig DispConfig
        {
            get
            {
                return dispConfig;
            }

        }
        public bool UseCUI
        {
            get
            {
                return useCUI;
            }

        }
		
    }
}
