namespace Intel.VPG.Display.Automation
{
    using System;
    using IgfxExtBridge_DotNet;

    /*  Get Dpcd register through CUI SDK 7.0 */
    class DpcdRegister_v1 : FunctionalBase, ISDK
    {
        private const uint IGFX_I2C_AUX_READ = 9;
        private const uint DPCD_BUFFER_SIZE = 0x0008;
        private IGFX_ERROR_CODES errorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Get(object args)
        {
            DpcdInfo dpcdInfo = args as DpcdInfo;
            IGFX_AUX_INFO InData = new IGFX_AUX_INFO();
            InData.dwDeviceUID = dpcdInfo.DispInfo.CUIMonitorID;
            InData.dwOpType = IGFX_I2C_AUX_READ;
            InData.dwSize = DPCD_BUFFER_SIZE;
            InData.dwAddress = dpcdInfo.Offset;
            InData.Data = new byte[16];
            APIExtensions.DisplayUtil.GetAuxInfo(ref InData, out errorCode, out errorDesc);
            if (errorCode == IGFX_ERROR_CODES.IGFX_SUCCESS)
                dpcdInfo.Value = InData.Data[0]; 
            else
                Log.Fail("Failed to get Aux info through SDK - Error Code: {0}  ErrorDec: {1}", errorCode, errorDesc);
            return dpcdInfo;
        }

        public object Set(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
