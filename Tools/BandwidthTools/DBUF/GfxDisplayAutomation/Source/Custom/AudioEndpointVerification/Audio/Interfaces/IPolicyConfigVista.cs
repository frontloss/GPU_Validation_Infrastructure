namespace AudioEndpointVerification
{
    using System;
    using System.Runtime.InteropServices;
    [Guid("568b9108-44bf-40b4-9006-86afe5b5a620"),
    InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    internal interface IPolicyConfigVista
    {
        [PreserveSig]
        int SetDefaultEndpoint(string pwstrId, ERole role, out int result);
    }
}
