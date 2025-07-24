namespace Intel.VPG.Display.Automation
{
    using System.Runtime.InteropServices;

    [StructLayout(LayoutKind.Sequential)]
    public struct RxDecoderCapability
    {
        public byte ucTransactionID;
        public ReceiverInterface RxInterface;
        public AdapterCapabilites AdapCap;
        public byte ucNumberOfPrograms;
        public ProgramCababilites ProgCap;
    };
    /* STRUCT related to Receiver Capabilities ends here*/

    /* STRUCT related to Receiver Interface starts here*/
    [StructLayout(LayoutKind.Sequential)]
    public struct ReceiverInterface
    {
        public byte ucNumOfDPConnectors;
        public byte ucNumOfHDMIConnectors;
    };
    /* STRUCT related to Receiver Interface ends here*/

    /* STRUCT related to Adapter Capabilites starts here*/
    [StructLayout(LayoutKind.Sequential)]
    public struct AdapterCapabilites
    {
        public byte ucEndPointIndex;
        public byte ucVersion;
        public byte ucReserved;
        public byte ucMaxPixelClock4_11;
        public byte ucMaxPixelClock0_3;
        public byte ucMST;
        public byte ucAVSync;
        public byte ucAudio;
        public byte ucNumOfVideoStreams;
        public byte ucHDCP;
        public byte ucHBR2;
        public byte ucHBR;
        public byte ucFastAux;
        public byte ucGTCSlave;
        public byte ucGTCMaster;
        public byte ucNumOfAudioStreams;
        public byte ucYOnly;
        public byte ucYCbCr422;
        public byte ucYCbCr444;
        public byte ucHBRAudio;
        public byte ucS3D;
        public byte ucYCbCr422ColorDepth;
        public byte ucYCbCr444ColorDepth;
        public byte ucYOnlyColorDepth;
        public byte ucRGBColorDepth;
        public byte ucMaxHActive8_15;
        public byte ucMaxHActive0_7;
        public byte ucMaxVActive8_15;
        public byte ucMaxVActive0_7;
    };
    /* STRUCT related to Adapter Capabilites ends here*/

    /* STRUCT related to Program Capabilites starts here*/
    [StructLayout(LayoutKind.Sequential)]
    public struct ProgramCababilites
    {
        public Features Feature;
        public AVCodecCapabilities AVCodecCap;
        public RawCapabilities RawCap;
        public WSPCapabilities WSPCap;
        public byte ucNumberOfVendorspecificCodecs;
        public byte ucJitterHandlingCapability8_15;
        public byte ucJitterHandlingCapability0_7;
        public byte ucAudioBufferSizeCapability8_15;
        public byte ucAudioBufferSizeCapability0_7;


    };
    /* STRUCT related to Program Capabilites starts here*/

    /* STRUCT related to Feature starts here*/

    [StructLayout(LayoutKind.Sequential)]
    public struct Features
    {
        public byte ucFeature1;
        public byte ucFeature2;
    };
    /* STRUCT related to Feature ends here*/

    /* STRUCT related to AV Codec Capabilites starts here*/

    [StructLayout(LayoutKind.Sequential)]
    public struct AVCodecCapabilities
    {
        public byte ucAVBitDepthSupportYCbCr8_15;
        public byte ucAVBitDepthSupportYCbCr0_7;
        public byte ucAVBitDepthSupportRGB;
        public byte ucAVMaxWidth8_15;
        public byte ucAVMaxWidth0_7;
        public byte ucAVMaxHeight8_15;
        public byte ucAVMaxHeight0_7;
        public byte ucAVMaxFrameRate;
        public byte ucAVMaxBitRate8_15;
        public byte ucAVMaxBitRate0_7;
        public byte ucMaxMBPS24_31;
        public byte ucMaxMBPS16_23;
        public byte ucMaxMBPS8_15;
        public byte ucMaxMBPS0_7;
        public byte ucMaxFS16_23;
        public byte ucMaxFS8_15;
        public byte ucMaxFS0_7;
        public byte ucCBPSizeCapability8_15;
        public byte ucCBPSizeCapability0_7;
        public byte ucAVCConfiguration8_15;
        public byte ucAVCConfiguration0_7;
        public byte ucS3DFormat;
    };
    /* STRUCT related to AV Codec Capabilites ends here*/

    /* STRUCT related to Raw Capabilites starts here*/

    [StructLayout(LayoutKind.Sequential)]
    public struct RawCapabilities
    {
        public byte ucRawBitDepthSupportYCbCr8_15;
        public byte ucRawBitDepthSupportYCbCr0_7;
        public byte ucRawBitDepthSupportRGB;
        public byte ucRawMaxWidth8_15;
        public byte ucRawMaxWidth0_7;
        public byte ucRawMaxHeight8_15;
        public byte ucRawMaxHeight0_7;
        public byte ucRawMaxFrameRate;
        public byte ucRawMaxBitRate8_15;
        public byte ucRawMaxBitRate0_7;
    };
    /* STRUCT related to Raw Capabilites ends here*/

    /* STRUCT related to WSP Capabilites starts here*/

    [StructLayout(LayoutKind.Sequential)]
    public struct WSPCapabilities
    {
        public byte ucBitDepthSupport8_15;
        public byte ucBitDepthSupport0_7;
        public byte ucWSPMaxWidth8_15;
        public byte ucWSPMaxWidth0_7;
        public byte ucWSPMaxHeight8_15;
        public byte ucWSPMaxHeight0_7;
        public byte ucWSPMaxFrameRate;
        public byte ucWSPMaxBitRate8_15;
        public byte ucWSPMaxBitRate0_7;
        public byte ucBlockMode;
        public byte ucComponentConfig;
    };

    /* STRUCT related to WSP Capabilites ends here*/
    [StructLayout(LayoutKind.Sequential)]
    public struct WiGigEdidDetails
    {
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 128)]
        public byte[] edidBaseBlock;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 128)]
        public byte[] edidExtensionBlock;

        public byte ucEndPointIndex;
        public byte ucVersion;
        public byte ucMST;
        public byte ucReserved;
        public byte ucMaxPixelClockMSB;
        public byte ucMaxPixelClockLSB;
        public byte ucAVSync;
        public byte ucAudio;
        public byte ucNumOfVideoStreams;
        public byte ucHDCP;
        public byte ucHBR2;
        public byte ucHBR;
        public byte ucFastAux;
        public byte ucGTCSlave;
        public byte ucGTCMaster;
        public byte ucNumOfAudioSteams;
        public byte ucYOnly;
        public byte ucYCbCr422;
        public byte ucYCbCr444;
        public byte ucHBRAudio;
        public byte ucS3D;
        public byte ucYCbCr422ColorDepth;
        public byte ucYCbCr444ColorDepth;
        public byte ucYOnlyColorDepth;
        public byte ucRGBColorDepth;
        public byte ucMaxHActiveMSB;
        public byte ucMaxHActiveLSB;
        public byte ucMaxVActiveMSB;
        public byte ucMaxVActiveLSB;

        public RxDecoderCapability RxDecoderDetails;
    }
    public enum ByteArrayData
    {
        LSB = 0,
        MSB
    };
}