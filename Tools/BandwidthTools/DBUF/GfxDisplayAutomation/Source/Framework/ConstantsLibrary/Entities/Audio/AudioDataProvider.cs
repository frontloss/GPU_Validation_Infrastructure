namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    public class AudioDataProvider
    {
        public int MaxSupportedAudioEndpoint;
        public int ActiveAudioEndpointDevice;
        public List<AudioDisplayInfo> ListAudioDisplayInfo;
        public List<string> ListAudioEndpointDevice;
        public AudioDataProvider()
        {
            ListAudioEndpointDevice = new List<string>();
            ListAudioDisplayInfo = new List<AudioDisplayInfo>();
        }
    }
    public class AudioDisplayInfo
    {
        public string displayFriendlyName;
        public DisplayType dispType;
        public PLANE planeInfo;
        public string PlaneRegValue;
        public string expectedRegValue;
        public bool isValidRegisterEntry;
        public bool isAudioCapablePannel;
        public string AUD_PIN_ELD_Reg_Value;
    }
    public class AudioMMDeviceData
    {
        public string FriendlyName;
        public string ID;
        public EDeviceState State;
    }

    public class SetAudioParam
    {
        public SetAudioSource setAudioInfo;
        public AudioInputSource audioTopology;
        public AudioWTVideo audioWTVideo;
        public string ID;
    }
}
