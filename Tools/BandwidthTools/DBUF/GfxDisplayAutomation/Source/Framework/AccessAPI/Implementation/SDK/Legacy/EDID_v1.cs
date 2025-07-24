namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using IgfxExtBridge_DotNet;

    /*  Get EDID information through CUI SDK 7.0 */
    public class EDID_v1 : FunctionalBase, ISDK 
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";

        public object Get(object args)
        {
            DisplayUIDMapper argDisplay = args as DisplayUIDMapper;
            List<byte> EDIDData = new List<byte>();
            IGFX_EDID_1_0 displayEDIDData = new IGFX_EDID_1_0();

            //Log.Verbose("Reading base EDID for display with Monitor ID - {0}", argDisplay.CuiID);
            displayEDIDData.dwDisplayDevice = argDisplay.CuiID;
            APIExtensions.DisplayUtil.GetEDIDData(ref displayEDIDData, out igfxErrorCode, out errorDesc);
            if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
            {
                Log.Fail("Get EDID information failed through SDK for monitorID: {0}, Block: {1}", displayEDIDData.dwDisplayDevice, displayEDIDData.dwEDIDBlock);
                return null;
            }

            if (displayEDIDData.EDID_Data[126] == 0) //This condition is kept to be in compliant with the existing functionality of taking 256 bytes of edid.
                EDIDData.AddRange(displayEDIDData.EDID_Data);
            else
                EDIDData.AddRange(displayEDIDData.EDID_Data.Take(128));

            //Log.Verbose("Reading CEA extn EDID for display with Monitor ID - {0}", argDisplay.CuiID);
            for (uint i = 0; i < displayEDIDData.EDID_Data[126]; i++)
            {
                IGFX_EDID_1_0 ceaEDIDData = new IGFX_EDID_1_0();
                ceaEDIDData.dwDisplayDevice = argDisplay.CuiID;
                ceaEDIDData.dwEDIDBlock = i + 1;
                APIExtensions.DisplayUtil.GetEDIDData(ref ceaEDIDData, out igfxErrorCode, out errorDesc);
                if (igfxErrorCode != IGFX_ERROR_CODES.IGFX_SUCCESS)
                {
                    Log.Fail("Get EDID information failed through SDK for monitorID: {0}, Block: {1}", ceaEDIDData.dwDisplayDevice, ceaEDIDData.dwEDIDBlock);
                    return null;
                }
                EDIDData.AddRange(ceaEDIDData.EDID_Data.Take(128));
            }
            return EDIDData.ToArray();
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
