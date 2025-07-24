namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;
    using System.Linq;
    using igfxSDKLib;
    using System;

    /*  Get EDID information through CUI SDK 8.0 */
    public class EDID_v2 : FunctionalBase, ISDK
    {
        private IDisplay Display;
        public object Get(object args)
        {
            DisplayUIDMapper argDisplay = args as DisplayUIDMapper;
            byte[] _EDID = { 0 };
            List<byte> EdidData = new List<byte>();
            uint _block = 0;

            GfxSDKClass GfxSDK = new GfxSDKClass();
            Display = GfxSDK.Display;

            IConnectedDisplays[] ConnectedDisplays = (IConnectedDisplays[])Display.GetConnectedDisplays();
            if (Display.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
            {
                IConnectedDisplays display = ConnectedDisplays.Where(ID => ID.DisplayID.Equals(argDisplay.WindowsID)).FirstOrDefault();
                Log.Verbose("DisplayID = {0} , DisplayType ={1} - Status {2}", display.DisplayID, display.DisplayType, display.Status);
                _EDID = (byte[])Display.GetEDID(display.DisplayID, _block);
                if (Display.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
                {
                    EdidData.AddRange(_EDID);
                    Log.Verbose("Get EDID Success for Display : {0} , BlockNUMBER : {1}", display.DisplayID, _block);
                    //Extension blocks 
                    uint noOfExtensionBlocks = _EDID[126];
                    for (uint _extensioBlockNumber = 1; _extensioBlockNumber <= noOfExtensionBlocks; _extensioBlockNumber++)
                    {
                        Log.Verbose("Extension Blocks  available - NO OF EXTENSIOSN BLOCK : {0} ", noOfExtensionBlocks);
                        _EDID = (byte[])Display.GetEDID(display.DisplayID, _extensioBlockNumber);
                        if (Display.Error == (uint)DISPLAY_ERROR_CODES.DISPLAY_SUCCESS)
                        {
                            Log.Message("Get EDID SCUCCESS for Display : {0} , BlockNumber : {1}", display.DisplayID, _extensioBlockNumber);
                            EdidData.AddRange(_EDID);
                        }

                        else
                            Log.Fail("Failed to get EDID for Display : {0} ,  BlockNumber : {1}  with Error code : {2}", display.DisplayID, _extensioBlockNumber, Display.Error);
                    }
                }
                else
                    Log.Fail("Failed to get EDID for Display : {0} ,  BLOCK {0}  with Error code : {1}", display.DisplayID, _block, Display.Error);
            }
            else
                Log.Fail("Failed to GetConnectedDisplays : errorCode : {0}", Display.Error);
            return EdidData.ToArray();
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
