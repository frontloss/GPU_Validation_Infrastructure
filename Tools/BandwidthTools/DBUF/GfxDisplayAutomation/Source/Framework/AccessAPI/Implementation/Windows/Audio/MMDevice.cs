namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;
    internal class MMDevice
    {
        #region Variables
        private IMMDevice _RealDevice;
        private PropertyStore _PropertyStore;
        #endregion

        #region Init
        private void GetPropertyInformation()
        {
            IPropertyStore propstore;
            Marshal.ThrowExceptionForHR(_RealDevice.OpenPropertyStore(EStgmAccess.STGM_READ, out propstore));
            _PropertyStore = new PropertyStore(propstore);
        }
        #endregion

        #region Properties

        public PropertyStore Properties
        {
            get
            {
                if (_PropertyStore == null)
                    GetPropertyInformation();
                return _PropertyStore;
            }
        }

        public string FriendlyName
        {
            get
            {
                if (_PropertyStore == null)
                    GetPropertyInformation();
                if (_PropertyStore.Contains(PKEY.PKEY_DeviceInterface_FriendlyName))
                {
                   return (string)_PropertyStore[PKEY.PKEY_DeviceInterface_FriendlyName].Value;
                }
                else
                    return "Unknown";
            }
        }


        public string ID
        {
            get
            {
                string Result;
                Marshal.ThrowExceptionForHR(_RealDevice.GetId(out Result));
                return Result;
            }
        }

        public EDataFlow DataFlow
        {
            get
            {
                EDataFlow Result;
                IMMEndpoint ep =  _RealDevice as IMMEndpoint ;
                ep.GetDataFlow(out Result);
                return Result;
            }
        }

        public EDeviceState State
        {
            get
            {
                EDeviceState Result;
                Marshal.ThrowExceptionForHR(_RealDevice.GetState(out Result));
                return Result;

            }
        }
        #endregion

        #region Constructor
        internal MMDevice(IMMDevice realDevice)
        {
            _RealDevice = realDevice;
        }
        #endregion

    }
}
