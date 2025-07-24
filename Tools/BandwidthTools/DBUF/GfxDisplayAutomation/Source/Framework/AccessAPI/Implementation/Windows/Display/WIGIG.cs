namespace Intel.VPG.Display.Automation
{
    using Microsoft.Win32;
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;
    using System.Threading;
    using System.Xml;

    public class WIGIG : FunctionalBase, ISetMethod , IGetMethod
    {
        WiGigEdidDetails edidData;
        WiGigParams wigigInputData = new WiGigParams();
        RegistryParams registryParams = new RegistryParams();

        string valueName = "EnableQuickCapture";
        //Register Offsets for reading the resolution in hardware
        private string FrameCounter = "FrameCounter";

        /************************************************************************************/
        // Function name: SetMethod
        // Parameters: true/false depending on result 
        // Description: In this function we call respective test scenario, based on the 
        // test name. For example, Receiver_Arrival will initiate WiGig receiver arrival mode
        // set and so on.
        // Return type: bool
        /***********************************************************************************/
        public bool SetMethod(object argMessage)
        {
            wigigInputData = (WiGigParams)argMessage;
            switch (wigigInputData.wigigSyncInput)
            {
                case WIGIG_SYNC.Receiver_Arrival:
                    return ReceiverArrival();
                case WIGIG_SYNC.RF_Kill:
                    return ReceiverKill();
                case WIGIG_SYNC.RF_LinkLost:
                    return RFLinkLost();
                case WIGIG_SYNC.QuickCapture:
                    return QuickCapture();
                default:
                    break;
            }

            return false;
        }

        public object GetMethod(object argMessage)
        {
            wigigInputData = (WiGigParams)argMessage;
            if(wigigInputData.wigigSyncInput== WIGIG_SYNC.WiGigDisplayPipe)
            {
                return GetPipeAssignedtoWiGig();
            }
            return false;
        }

        /************************************************************************************/
        // Function name: ReceiverArrival
        // Parameters: None
        // Description: Initiates Receiver Arrival by calling SetVxdWNICReceiverArival which 
        // is exposed in the DLL file WiGig.dll. 
        // Return type: bool
        /***********************************************************************************/
        private bool ReceiverArrival()
        {
            Log.Message("Simulating WiGig Receiver Arrival with Display {0} ...", wigigInputData.wigigDisplay);

            // Populate the EDID details in data-structure edidData 
            FillEdidDetails();

            // Call the interface SetVxdWNICReceiverArival which is exposed by DLL Utilties.dll
            Interop.SetVxdWNICReceiverArival(edidData);

            // Validate here whether plug of WiGig display successfull or not.
            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());

            Thread.Sleep(2000); // Wait for few seconds since Receiver arrival mode set will take 1 or 2 seconds due to WNIC dependencies.

            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;
            //WD0 Transcoder Register Validation
                       
            if ((enumeratedDisplay.Any(DI => (DisplayExtensions.GetDisplayType(DI.DisplayType) == DisplayType.WIGIG_DP))))
            {
                if (!TestPostProcessing.RegisterCleanupRequest.ContainsKey(TestCleanUpType.WiGig))
                {
                    TestPostProcessing.RegisterCleanupRequest.Add(TestCleanUpType.WiGig, null);
                }
                return true;
            }
         return false;
        }

        /************************************************************************************/
        // Function name: ReceiverKill
        // Parameters: None
        // Description: Initiates Receiver Kill by calling SetVxdWNICRFKill which 
        // is exposed in the DLL file WiGig.dll. 
        // Return type: bool
        /***********************************************************************************/
        private bool ReceiverKill()
        {
            Log.Message("Simulating WiGig Receiver Kill");

            // Call the interface SetVxdWNICRFKill which is exposed by DLL Utilties.dll
            
            Interop.SetVxdWNICRFKill();

            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());

            Thread.Sleep(2000); // Wait for few seconds since Receiver kill mode set will take 1 or 2 seconds due to WNIC dependencies.

            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;

            if (!(enumeratedDisplay.Any(DI => DisplayExtensions.GetDisplayType(DI.DisplayType) == DisplayType.WIGIG_DP)))
            {
                Log.Message("RF Kill happened successfully...");
                Log.Verbose("WD Function is disabled");
                return true;
            }
            else
            {
                Log.Verbose("WD Function is not disabled");
            }

            return false;
        }

        /************************************************************************************/
        // Function name: FillEdidDetails
        // Parameters: None 
        // Description: Copy EDID details into data-structure edidData from the EDID file.
        // Return type: void
        /***********************************************************************************/
        private void FillEdidDetails()
        {
            int iNoOfBlocks = 0;
            edidData = new WiGigEdidDetails();
            edidData.edidBaseBlock = new byte[128];
            edidData.edidExtensionBlock = new byte[128];
            byte[] edidRawDataBlock = new byte[256];

            string path = string.Concat(Directory.GetCurrentDirectory(), @"\EDIDFiles\",DisplayExtensions.GetEdidFile(wigigInputData.wigigDisplay));
            edidRawDataBlock = File.ReadAllBytes(path);

            if ((edidRawDataBlock.Length) == 128)
            {
                iNoOfBlocks = 1;
            }
            else if ((edidRawDataBlock.Length) == 256)
            {
                iNoOfBlocks = 2;
            }

            Array.Copy(edidRawDataBlock, 0, edidData.edidBaseBlock, 0, 128);

            // Copy extension block only if it is available in the EDID file
            if (iNoOfBlocks == 2)
            {
                Array.Copy(edidRawDataBlock, 128, edidData.edidExtensionBlock, 0, 128);
            }

            #region EDID Data Hard Code Value
            edidData.ucEndPointIndex = 0; // 1;
            edidData.ucVersion = 1;
            edidData.ucMST = 1;
            edidData.ucReserved = 0;
            edidData.ucAVSync = 0;
            edidData.ucAudio = 0;
            edidData.ucNumOfVideoStreams = 1;
            edidData.ucHDCP = 0;
            edidData.ucHBR2 = 1;
            edidData.ucHBR = 1;
            edidData.ucFastAux = 1;
            edidData.ucGTCSlave = 1;
            edidData.ucGTCMaster = 1;
            edidData.ucNumOfAudioSteams = 0;

            edidData.ucYOnly = 0;
            edidData.ucYCbCr422 = 0;
            edidData.ucYCbCr444 = 1;
            edidData.ucHBRAudio = 1;

            edidData.ucS3D = 0;
            edidData.ucYCbCr422ColorDepth = 0;
            edidData.ucYCbCr444ColorDepth = 1;
            edidData.ucYOnlyColorDepth = 0;

            edidData.ucRGBColorDepth = 6;
            #endregion

            edidData.ucMaxHActiveLSB = edidData.edidBaseBlock[56];
            edidData.ucMaxHActiveMSB = (byte)TakeOneByteData(ByteArrayData.LSB, edidData.edidBaseBlock[58]);

            edidData.ucMaxVActiveLSB = edidData.edidBaseBlock[59];
            edidData.ucMaxVActiveMSB = (byte)TakeOneByteData(ByteArrayData.LSB, edidData.edidBaseBlock[61]);
            edidData.ucMaxPixelClockLSB = edidData.edidBaseBlock[54];
            edidData.ucMaxPixelClockMSB = edidData.edidBaseBlock[55];
             XmlDocument doc = new XmlDocument();
             doc.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\WiGig.map"));
             foreach (XmlNode node in doc.GetElementsByTagName("Dock"))
              {
                edidData.RxDecoderDetails.ucTransactionID = Convert.ToByte(Convert.ToInt32(node["TransactionID"].InnerText, 16));
                //Fill Receiver Interface
                edidData.RxDecoderDetails.RxInterface.ucNumOfDPConnectors = Convert.ToByte(Convert.ToInt32(node["NumOfDPConnectors"].InnerText, 16));
                edidData.RxDecoderDetails.RxInterface.ucNumOfHDMIConnectors = Convert.ToByte(Convert.ToInt32(node["NumOfHDMIConnectors"].InnerText, 16));
                //Fill Adapter Capability
                edidData.RxDecoderDetails.AdapCap.ucEndPointIndex = Convert.ToByte(Convert.ToInt32(node["EndPointIndex"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucVersion = Convert.ToByte(Convert.ToInt32(node["Version"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucReserved = Convert.ToByte(Convert.ToInt32(node["Reserved"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxPixelClock4_11 = Convert.ToByte(Convert.ToInt32(node["MaxPixelClock4_11"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxPixelClock0_3 = Convert.ToByte(Convert.ToInt32(node["MaxPixelClock0_3"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMST = Convert.ToByte(Convert.ToInt32(node["MST"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucAVSync = Convert.ToByte(Convert.ToInt32(node["AVSync"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucAudio = Convert.ToByte(Convert.ToInt32(node["Audio"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucNumOfVideoStreams = Convert.ToByte(Convert.ToInt32(node["NumOfVideoStreams"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucHDCP = Convert.ToByte(Convert.ToInt32(node["HDCP"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucHBR2 = Convert.ToByte(Convert.ToInt32(node["HBR2"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucHBR = Convert.ToByte(Convert.ToInt32(node["HBR"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucFastAux = Convert.ToByte(Convert.ToInt32(node["FastAux"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucGTCSlave = Convert.ToByte(Convert.ToInt32(node["GTCSlave"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucGTCMaster = Convert.ToByte(Convert.ToInt32(node["GTCMaster"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucNumOfAudioStreams = Convert.ToByte(Convert.ToInt32(node["NumOfAudioStreams"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYOnly = Convert.ToByte(Convert.ToInt32(node["YOnly"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYCbCr422 = Convert.ToByte(Convert.ToInt32(node["YCbCr422"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYCbCr444 = Convert.ToByte(Convert.ToInt32(node["YCbCr444"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucHBRAudio = Convert.ToByte(Convert.ToInt32(node["HBRAudio"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYCbCr422ColorDepth = Convert.ToByte(Convert.ToInt32(node["YCbCr422ColorDepth"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYCbCr444ColorDepth = Convert.ToByte(Convert.ToInt32(node["YCbCr444ColorDepth"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucYOnlyColorDepth = Convert.ToByte(Convert.ToInt32(node["YOnlyColorDepth"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucRGBColorDepth = Convert.ToByte(Convert.ToInt32(node["RGBColorDepth"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxHActive8_15 = Convert.ToByte(Convert.ToInt32(node["MaxHActive8_15"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxHActive0_7 = Convert.ToByte(Convert.ToInt32(node["MaxHActive0_7"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxVActive8_15 = Convert.ToByte(Convert.ToInt32(node["MaxVActive8_15"].InnerText, 16));
                edidData.RxDecoderDetails.AdapCap.ucMaxVActive0_7 = Convert.ToByte(Convert.ToInt32(node["MaxVActive0_7"].InnerText, 16));

                edidData.RxDecoderDetails.ucNumberOfPrograms = Convert.ToByte(Convert.ToInt32(node["NumberOfPrograms"].InnerText, 16));

                /*Fill Program Capability*/

                //Fill Feature
                edidData.RxDecoderDetails.ProgCap.Feature.ucFeature1 = Convert.ToByte(Convert.ToInt32(node["Feature1"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.Feature.ucFeature2 = Convert.ToByte(Convert.ToInt32(node["Feature2"].InnerText, 16));

                //Fill AV Codec Capability
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVBitDepthSupportYCbCr8_15 = Convert.ToByte(Convert.ToInt32(node["AVBitDepthSupportYCbCr8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVBitDepthSupportYCbCr0_7 = Convert.ToByte(Convert.ToInt32(node["AVBitDepthSupportYCbCr0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVBitDepthSupportRGB = Convert.ToByte(Convert.ToInt32(node["AVBitDepthSupportRGB"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxWidth8_15 = Convert.ToByte(Convert.ToInt32(node["AVMaxWidth8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxWidth0_7 = Convert.ToByte(Convert.ToInt32(node["AVMaxWidth0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxHeight8_15 = Convert.ToByte(Convert.ToInt32(node["AVMaxHeight8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxHeight0_7 = Convert.ToByte(Convert.ToInt32(node["AVMaxHeight0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxMBPS24_31 = Convert.ToByte(Convert.ToInt32(node["MaxMBPS24_31"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxMBPS16_23 = Convert.ToByte(Convert.ToInt32(node["MaxMBPS16_23"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxMBPS8_15 = Convert.ToByte(Convert.ToInt32(node["MaxMBPS8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxMBPS0_7 = Convert.ToByte(Convert.ToInt32(node["MaxMBPS0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxFS16_23 = Convert.ToByte(Convert.ToInt32(node["MaxFS16_23"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxFS8_15 = Convert.ToByte(Convert.ToInt32(node["MaxFS8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucMaxFS0_7 = Convert.ToByte(Convert.ToInt32(node["MaxFS0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxFrameRate = Convert.ToByte(Convert.ToInt32(node["AVMaxFrameRate"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxBitRate8_15 = Convert.ToByte(Convert.ToInt32(node["AVMaxBitRate8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVMaxBitRate0_7 = Convert.ToByte(Convert.ToInt32(node["AVMaxBitRate0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucCBPSizeCapability8_15 = Convert.ToByte(Convert.ToInt32(node["CBPSizeCapability8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucCBPSizeCapability0_7 = Convert.ToByte(Convert.ToInt32(node["CBPSizeCapability0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVCConfiguration8_15 = Convert.ToByte(Convert.ToInt32(node["AVCConfiguration8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucAVCConfiguration0_7 = Convert.ToByte(Convert.ToInt32(node["AVCConfiguration0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.AVCodecCap.ucS3DFormat = Convert.ToByte(Convert.ToInt32(node["S3DFormat"].InnerText, 16));

                //Fill Raw Capability
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawBitDepthSupportYCbCr8_15 = Convert.ToByte(Convert.ToInt32(node["RawBitDepthSupportYCbCr8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawBitDepthSupportYCbCr0_7 = Convert.ToByte(Convert.ToInt32(node["RawBitDepthSupportYCbCr0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawBitDepthSupportRGB = Convert.ToByte(Convert.ToInt32(node["RawBitDepthSupportRGB"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxWidth8_15 = Convert.ToByte(Convert.ToInt32(node["RawMaxWidth8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxWidth0_7 = Convert.ToByte(Convert.ToInt32(node["RawMaxWidth0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxHeight8_15 = Convert.ToByte(Convert.ToInt32(node["RawMaxHeight8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxHeight0_7 = Convert.ToByte(Convert.ToInt32(node["RawMaxHeight0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxFrameRate = Convert.ToByte(Convert.ToInt32(node["RawMaxFrameRate"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxBitRate8_15 = Convert.ToByte(Convert.ToInt32(node["RawMaxBitRate8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.RawCap.ucRawMaxBitRate0_7 = Convert.ToByte(Convert.ToInt32(node["RawMaxBitRate0_7"].InnerText, 16));

                //Fill WSP Capability
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucBitDepthSupport8_15 = Convert.ToByte(Convert.ToInt32(node["BitDepthSupport8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucBitDepthSupport0_7 = Convert.ToByte(Convert.ToInt32(node["BitDepthSupport0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxWidth8_15 = Convert.ToByte(Convert.ToInt32(node["WSPMaxWidth8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxWidth0_7 = Convert.ToByte(Convert.ToInt32(node["WSPMaxWidth0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxHeight8_15 = Convert.ToByte(Convert.ToInt32(node["WSPMaxHeight8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxHeight0_7 = Convert.ToByte(Convert.ToInt32(node["WSPMaxHeight0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxFrameRate = Convert.ToByte(Convert.ToInt32(node["WSPMaxFrameRate"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxBitRate8_15 = Convert.ToByte(Convert.ToInt32(node["WSPMaxBitRate8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucWSPMaxBitRate0_7 = Convert.ToByte(Convert.ToInt32(node["WSPMaxBitRate0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucBlockMode = Convert.ToByte(Convert.ToInt32(node["BlockMode"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.WSPCap.ucComponentConfig = Convert.ToByte(Convert.ToInt32(node["ComponentConfig"].InnerText, 16));

                edidData.RxDecoderDetails.ProgCap.ucNumberOfVendorspecificCodecs = Convert.ToByte(Convert.ToInt32(node["NumberOfVendorspecificCodecs"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.ucJitterHandlingCapability8_15 = Convert.ToByte(Convert.ToInt32(node["JitterHandlingCapability8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.ucJitterHandlingCapability0_7 = Convert.ToByte(Convert.ToInt32(node["JitterHandlingCapability0_7"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.ucAudioBufferSizeCapability8_15 = Convert.ToByte(Convert.ToInt32(node["AudioBufferSizeCapability8_15"].InnerText, 16));
                edidData.RxDecoderDetails.ProgCap.ucAudioBufferSizeCapability0_7 = Convert.ToByte(Convert.ToInt32(node["AudioBufferSizeCapability0_7"].InnerText, 16));
            }
        }

        /// <summary>
        /// Function to get one byte of data
        /// </summary>
        /// <param name="argByteData">Holds whether the byte required is LSB/MSB</param>
        /// <param name="data">Holds the actual data</param>
        /// <returns>One byte of integer data</returns>
        private int TakeOneByteData(ByteArrayData argByteData, int data)
        {
            if (argByteData == ByteArrayData.MSB)
                return ((data >> 8) & 0xff) >> 4;
            else
                return (data & 0xff) >> 4;
        }

        private bool RFLinkLost()
        {
            Log.Message("Performing Link Lost...");

            DisplayEnumeration enumDisplay = base.CreateInstance<DisplayEnumeration>(new DisplayEnumeration());

            // Call the interface SetVxdWNICRFKill which is exposed by DLL Utilties.dll
           
            Interop.SetVxdWNICRFLinkLost();

            Thread.Sleep(2000);
            
            List<DisplayInfo> enumeratedDisplay = enumDisplay.GetAll as List<DisplayInfo>;

            if (!(enumeratedDisplay.Any(DI => (DisplayExtensions.GetDisplayType(DI.DisplayType) == DisplayType.WIGIG_DP)))) 
            {
                Log.Verbose("RF LinkLost successfully happened...");
                return true;
            }
            else
            {
                Log.Verbose("LinkLost didn't happen...");
            }

            return false;

        }

        /// <summary>
        /// Read the WD transcoder register to check on which pipe the WIGIG display is active
        /// </summary>
        /// <returns>bool</returns>
        private bool GetPipeAssignedtoWiGig()
        {
            Config getCurrentConfig = base.CreateInstance<Config>(new Config());
            DisplayConfig currentCfg = getCurrentConfig.Get as DisplayConfig;
            DisplayHierarchy getDispHierarchy = currentCfg.GetDispHierarchy(wigigInputData.wigigDisplay);
            PipePlaneParams pipeinfo = new PipePlaneParams(wigigInputData.wigigDisplay);
            PipePlane pipe = base.CreateInstance<PipePlane>(new PipePlane());
            pipe.GetMethod(pipeinfo);
            switch(getDispHierarchy)
            {
                case DisplayHierarchy.Display_1:
                    if (pipeinfo.Pipe == PIPE.PIPE_A)
                    {
                        Log.Message("WiGig active on primary");
                        return true;
                    }
                    else
                    {
                        Log.Message("WiGig on Pipe A register check failed");
                        return false;
                    }
               case DisplayHierarchy.Display_2:
                    if (pipeinfo.Pipe == PIPE.PIPE_B)
                    {
                        Log.Message("WiGig active on secondary");
                        return true;
                    }
                    else
                    {
                        Log.Message("WiGig on Pipe B register check failed");
                        return false;
                    }
               case DisplayHierarchy.Display_3:
                    if (pipeinfo.Pipe == PIPE.PIPE_C)
                    {
                        Log.Message("WiGig active on tertiary");
                        return true;
                    }
                    else
                    {
                        Log.Message("WiGig on Pipe C register check failed");
                        return false;
                    }
                default:
                    Log.Verbose("Not Valid Pipe");
                    return false;
            }
        }

        /************************************************************************************/
        // Function name: IsQuickCaptureEnabled
        // Parameters   : None 
        // Description  : Verifies QuickCapture enabled or not in the INF/Registry.
        // Return type : Void
        /************************************************************************************/
        private bool IsQuickCaptureEnabled()
        {
            if (Registry.GetValue(base.MachineInfo.Driver.GfxDriverRegistryPath, valueName, null) != null)
                return true;
            else
                return false;
        }
        /************************************************************************************/
        // Function name: MonitorQuickCaptureEntryExit
        // Parameters   : time 
        // Description  : Verifies QuickCapture feature working or not. Logs FrameLine counter,
        //                Video tail pointer and Static bit registers values and Parses the log
        //                to determine QuickCapture working or not
        // Return type  : Void
        /************************************************************************************/
        public bool QuickCapture()
        {
            List<RegisterInf> FrameCountInitial = FetchEventInfo(FrameCounter, PIPE.NONE, PLANE.NONE, PORT.NONE).listRegisters;
            PowerEvent powEvent = base.CreateInstance<PowerEvent>(new PowerEvent());
            XmlDocument doc = new XmlDocument();
            doc.Load(string.Concat(Directory.GetCurrentDirectory(), @"\Mapper\WiGig.map"));
            XmlNode tnode = doc.SelectSingleNode(("/Data[@*]/time"));
            PowerParams powParams = new PowerParams();
            powParams.Delay = (int.Parse(tnode.Attributes["value"].Value) * 60);
            powParams.PowerStates = PowerStates.IdleDesktop;
            powEvent.SetMethod(powParams);

            List<RegisterInf> FrameCountFinal = FetchEventInfo(FrameCounter, PIPE.NONE, PLANE.NONE, PORT.NONE).listRegisters;
             if (IsQuickCaptureEnabled() == true)
              {
                Int32 framelimit =0;
                Log.Verbose("Quick Capture enabled by the graphics driver in the registry");
                Log.Verbose("Quick Capture monitored for {0} min(s)", int.Parse(tnode.Attributes["value"].Value));
                Log.Message("Number of frames updated = {0}", (FrameCountFinal[0].BitmappedValue - FrameCountInitial[0].BitmappedValue));
                XmlNodeList filename = doc.GetElementsByTagName("MaxQCFlipsThreshold");
                foreach (XmlNode node in filename)
                Int32.TryParse(node.Attributes["value"].Value,out framelimit);
                if ((FrameCountFinal[0].BitmappedValue - FrameCountInitial[0].BitmappedValue) <= framelimit)
                {
                    Log.Message("Quick Capture feature is working properly");
                    return true;
                }
                else
                    Log.Message("Quick Capture feature is not working properly");
               }
               else
                {
                  Log.Alert("Quick Capture NOT enabled by the graphics driver in the registry");

                  Log.Message("Number of frames updated = {0}", (FrameCountFinal[0].BitmappedValue - FrameCountInitial[0].BitmappedValue));
                }
           return false;
        }

        private EventInfo FetchEventInfo(string registerEvent, PIPE pipe, PLANE plane, PORT port)
        {
            EventInfo eventInfo = new EventInfo();
            EventRegisterInfo eventRegisterInfo = base.CreateInstance<EventRegisterInfo>(new EventRegisterInfo());
            Log.Verbose("Fetching Registers for event:{0} with factors:{1},{2},{3}", registerEvent, pipe, plane, port);
            eventInfo.pipe = pipe;
            eventInfo.plane = plane;
            eventInfo.port = port;
            eventInfo.eventName = registerEvent;
            eventRegisterInfo.MachineInfo = base.MachineInfo;
            EventInfo returnEventInfo = (EventInfo)eventRegisterInfo.GetMethod(eventInfo);
            return returnEventInfo;
       }
    }
}