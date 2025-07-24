namespace AudioEndpointVerification
{
    public class DriverInfo
    {
        private AudioDriverInfo _audioDriver;
        private GfxDriverInfo _gfxDriver;

        public AudioDriverInfo AudioDriver
        {
            get { return _audioDriver; }
            set { _audioDriver = value; }
        }

        public GfxDriverInfo GfxDriver
        {
            get { return _gfxDriver; }
            set { _gfxDriver = value; }
        }
    }

    public class GfxDriverInfo
    {
        private string _status = string.Empty;
        private string _version = string.Empty;
        public string Status
        {
            get { return _status; }
            set { _status = value; }
        }
        public string Version
        {
            get { return _version; }
            set { _version = value; }
        }
    }

    public class AudioDriverInfo
    {
        private string _status = string.Empty;
        private string _version = string.Empty;
        public string Status
        {
            get { return _status; }
            set { _status = value; }
        }
        public string Version
        {
            get { return _version; }
            set { _version = value; }
        }
    }
}
