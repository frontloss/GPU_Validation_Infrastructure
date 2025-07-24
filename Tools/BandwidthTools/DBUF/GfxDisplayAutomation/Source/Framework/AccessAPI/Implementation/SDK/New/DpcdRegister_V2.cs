namespace Intel.VPG.Display.Automation
{
    using System;
    using igfxSDKLib;

    /*  Get Dpcd register through CUI SDK 8.0 */
    class DpcdRegister_v2 : FunctionalBase, ISDK
    {
        private const uint DPCD_BUFFER_SIZE = 0x0008;
        private IDataChannel DataChannel;
        public object Get(object args)
        {
            GfxSDKClass GfxSDK = new GfxSDKClass();
            DataChannel = GfxSDK.Display.DataChannel;

            DpcdInfo dpcdInfo = args as DpcdInfo;
            DataChannel.Aux.Address = dpcdInfo.Offset;
            DataChannel.Aux.DeviceID = dpcdInfo.DispInfo.WindowsMonitorID;
            DataChannel.Aux.OperationType = AUX_OPERATION_TYPE.I2C_AUX_READ;
            DataChannel.Aux.Size = DPCD_BUFFER_SIZE;
            byte[] data = (byte[])DataChannel.Aux.Read();

            if (DataChannel.Aux.Error == (uint)AUX_ERROR_CODES.AUX_SUCCESS)
            {
                dpcdInfo.Value = data[0]; 
                Log.Success("Successfully read DPCD Data through SDK");
            }
            else
                Log.Fail("Fail to read DPCD Data through SDK");
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
