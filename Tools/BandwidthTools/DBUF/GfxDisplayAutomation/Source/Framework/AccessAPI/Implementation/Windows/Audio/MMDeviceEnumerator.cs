namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;
    [ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
    internal class _MMDeviceEnumerator
    {
    }
    internal class MMDeviceEnumerator 
    {
        private IMMDeviceEnumerator _realEnumerator = new _MMDeviceEnumerator() as IMMDeviceEnumerator;

        public MMDeviceCollection EnumerateAudioEndPoints(EDataFlow dataFlow, EDeviceState dwStateMask)
        {
            IMMDeviceCollection result;
            Marshal.ThrowExceptionForHR(_realEnumerator.EnumAudioEndpoints(dataFlow,dwStateMask,out result));
            return new MMDeviceCollection(result);
        }

        public MMDevice GetDefaultAudioEndpoint(EDataFlow dataFlow, ERole role)
        {
            IMMDevice _Device = null;
            Marshal.ThrowExceptionForHR(((IMMDeviceEnumerator)_realEnumerator).GetDefaultAudioEndpoint(dataFlow, role, out _Device));
            return new MMDevice(_Device);
        }

        public MMDevice GetDevice(string ID)
        {
            IMMDevice _Device = null;
            Marshal.ThrowExceptionForHR(((IMMDeviceEnumerator)_realEnumerator).GetDevice(ID, out _Device));
            return new MMDevice(_Device);
        }

        public MMDeviceEnumerator()
        {
            if (System.Environment.OSVersion.Version.Major < 6)
            {
                throw new NotSupportedException("This functionality is only supported on Windows Vista or newer.");
            }
        }
    }
}
