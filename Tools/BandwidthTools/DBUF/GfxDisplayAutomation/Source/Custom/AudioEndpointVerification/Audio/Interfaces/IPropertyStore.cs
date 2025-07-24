namespace AudioEndpointVerification
{
    using System;
    using System.Runtime.InteropServices;
    [Guid("886d8eeb-8cf2-4446-8d02-cdba1dbdcf99"),
     InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    internal interface IPropertyStore  
    {
        [PreserveSig]
        int GetCount( out Int32 count);
        [PreserveSig]
        int GetAt( int iProp, out PropertyKey pkey);
        [PreserveSig]
        int GetValue(ref PropertyKey key, out PropVariant pv);
        [PreserveSig]
        int SetValue(ref PropertyKey key, ref PropVariant propvar);
        [PreserveSig]
        int Commit( );
    };
}
