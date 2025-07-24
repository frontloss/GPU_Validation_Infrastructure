using System;
using System.Collections.Generic;

namespace Intel.VPG.Display.Automation
{
    public static class StubDriverInterop
    {
        private static Dictionary<StubDriverServiceType, IntPtr> ServiceHandle = new Dictionary<StubDriverServiceType, IntPtr>();
        public static void Register(StubDriverServiceType Type, string DLLFullPath)
        {
            if (ServiceHandle.ContainsKey(Type) == false)
            {
                IntPtr pDll = Interop.LoadLibrary(DLLFullPath);
                ServiceHandle.Add(Type, pDll);
            }
        }

        public static IntPtr GetAddress(StubDriverServiceType Type, string functionName)
        {
            IntPtr ptr;
            ServiceHandle.TryGetValue(Type, out ptr);
            return Interop.GetProcAddress(ptr, functionName);
        }

        public static void UnRegister()
        {
            foreach (KeyValuePair<StubDriverServiceType, IntPtr> KV in ServiceHandle)
            {
                Interop.FreeLibrary(KV.Value);
            }
        }
    }
}
