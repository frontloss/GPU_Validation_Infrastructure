namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Runtime.InteropServices;
    [ComImport, Guid("294935CE-F637-4E7C-A41B-AB255460B862")]
    internal class _PolicyConfigVista
    {
    }
    internal class PolicyConfigVista
    {
        private IPolicyConfigVista _policy = new _PolicyConfigVista() as IPolicyConfigVista;
        public int SetAudioEndpoint(string strId, ERole role)
        {
            int result;
            Marshal.ThrowExceptionForHR(_policy.SetDefaultEndpoint(strId, role, out result));
            return result;
        }
    }
}
