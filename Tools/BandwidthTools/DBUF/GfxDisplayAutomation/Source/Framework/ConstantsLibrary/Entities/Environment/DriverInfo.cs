namespace Intel.VPG.Display.Automation
{
    using System.Linq;
    using System.Collections.Generic;

    public class DriverInfo
    {
        private string _status = string.Empty;
        private string _name = string.Empty;
        private string _deviceID = string.Empty;
        private string _vendorID = string.Empty;
        private string _oemFile = string.Empty;
        private string _version = string.Empty;
        private string _driverBaseLine = string.Empty;
        private string _audioDriverName = string.Empty;
        private string _audioDriverStatus = string.Empty;
        private string _driverDescription = string.Empty;
        private string _gfxDriverRegistryPath = string.Empty;
        public string DriverDescription
        {
            get { return _driverDescription; }
            set { _driverDescription = value; }
        }

        public string DriverBaseLine
        {
            get { return _driverBaseLine; }
            set { _driverBaseLine = value; }
        }

        public string OEMFile
        {
            get { return _oemFile; }
            set { _oemFile = value; }
        }
        public string VendorID
        {
            get { return _vendorID; }
            set { _vendorID = value; }
        }
        public string DeviceID
        {
            get { return _deviceID; }
            set { _deviceID = value; }
        }
        public string Name
        {
            get { return _name; }
            set { _name = value; }
        }
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
        public string AudioDriverName
        {
            get { return _audioDriverName; }
            set { _audioDriverName = value; }
        }

        public string AudioDriverStatus
        {
            get { return _audioDriverStatus; }
            set { _audioDriverStatus = value; }
        }

        public string GfxDriverRegistryPath
        {
            get { return _gfxDriverRegistryPath; }
            set { _gfxDriverRegistryPath = value; }
        }
    }
}