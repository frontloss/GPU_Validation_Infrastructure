#pragma once
#include <Windows.h>
#include <stdio.h>
#include <mmreg.h>
#include "GFXMMIO.h"

#define MAX_NUM_PIN_NODES 12
#define MAX_NUM_CONVERTER_NODES 4
#define MAX_NUM_TRANSCODERS 4
#define ELD_BUFFER_SIZE 84

#define SET_DIP_INDEX_VERB_ID 0x730
#define SET_DEVICE_SELECT 0x735

#define GET_AMPLIFIER_GAIN_MUTE 0xB
#define GET_PARAM_VERB_ID 0xF00
#define GET_CONN_SELECT_CONTROL_VERB_ID 0xF01
#define GET_CONNECTION_LIST_ENTRY_VERB_ID 0xF02
#define GET_POWER_STATE_VERB_ID 0xF05
#define GET_PIN_WIDGET_CONTROL_VERB_ID 0xF07
#define GET_ELD_DATA_VERB_ID 0xF2F
#define GET_DIP_DATA_VERB_ID 0xF31
#define GET_DIP_XMIT_CTRL_VERB_ID 0xF32
#define GET_ASP_CHANNEL_MAPPING_VERB_ID 0xF34
#define GET_DEVICE_LIST_ENTRY 0xF36

#define SUB_NODE_CNT_PARAMETER_ID 0x04
#define AUDIO_WIDGET_CAPS 0x09

#define AFG_NODE_ID 2

#define NODE_TYPE_OUTPUT_CONVERTER_WIDGET 0x0
#define NODE_TYPE_PIN_COMPLEX_WIDGET 0x4
#define NODE_TYPE_VENDOR_DEFINED_WIDGET 0xF

#define KSAUDIO_SPEAKER_HBR 0xffff /**< Custom Speaker allocation used to indicate HBR 1:1 channel mapping. */

#define AIF_PACKET_INDEX 0
#define AIF_HDMI_HEADER_SIZE 4  /**< Audio InfoFrame header size for HDMI. */
#define AIF_DP_HEADER_SIZE 3    /**< Audio InfoFrame header size for DP. */
#define AIF_INFOFRAME_TYPE 0x84 /**< Infoframe type. */
#define AIF_DATA_SIZE 10
#define AIF_PACKET_SIZE (AIF_DATA_SIZE + max(AIF_HDMI_HEADER_SIZE, AIF_DP_HEADER_SIZE))

#define MAX_NUM_CHANNEL 8

#define ICL_DEVICE_ID 0x280F
#define LKF_DEVICE_ID 0x2811
#define TGL_DEVICE_ID 0x2812
#define RYF_DEVICE_ID 0x2813
#define ADL_DEVICE_ID 0x2815
#define RKL_DEVICE_ID 0x2816
#define JSL_DEVICE_ID 0x281A
#define EHL_DEVICE_ID 0x281B
#define DG1_DEVICE_ID 0x2814

#define GET_NIBBLE(data, nibbleIndex) ((data >> (nibbleIndex * 4)) & 0xF);

typedef enum
{
    CONVERTER_STREAM_TYPE_PCM        = 0, /**< PCM stream type. */
    CONVERTER_STREAM_TYPE_NONPCM     = 1, /**< Non-PCM stream type. */
    CONVERTER_STREAM_TYPE_NONPCM_HBR = 3, /**< Non-PCM HBR stream. */
    INVALID_STREAM_TYPE                   /**< Indicates an invalid stream type. Must be last element. */
} eStreamType;

#pragma pack(1)

typedef enum
{
    PIPE_A = 0,
    PIPE_B = 1,
    PIPE_C = 2,
    PIPE_D = 3,
} pipe_id;

typedef struct
{
    UCHAR ucFLR : 1;       // Front Left and Right channels
    UCHAR ucLFE : 1;       // Low Frequency Effect channel
    UCHAR ucFC : 1;        // Center transmission channel
    UCHAR ucRLR : 1;       // Rear Left and Right channels
    UCHAR ucRC : 1;        // Rear Center channel
    UCHAR ucFLRC : 1;      // Front left and Right of Center transmission channels
    UCHAR ucRLRC : 1;      // Rear left and Right of Center transmission channels
    UCHAR ucReserved3 : 1; // Reserved
} SPEAKER_POSITIONS;

typedef union _ELDV2 {
#pragma pack(1)
    struct
    {
        UCHAR             ucReserved1 : 3;
        UCHAR             ucELDVersion : 5; // Should be 0x2
        UCHAR             ucReserved2;
        UCHAR             ucBaselineELDLength;
        UCHAR             ucReserved3;
        UCHAR             ucMNL : 5; // Monitor Name Length
        UCHAR             ucCEAEDIDVersion : 3;
        UCHAR             ucHDCP : 1;           // Indicates HDCP support
        UCHAR             ucAI : 1;             // Inidcates AI support
        UCHAR             ucConnectionType : 2; // Indicates Connection type. 00: HDMI, 01: DP, 10-11: Reserved
        UCHAR             ucSADCount : 4;       // Indicates number of 3 bytes Short Audio Descriptors. Maximum 15
        UCHAR             ucAudioSyncDelay;     // The amount of latency added by the sink in units of 2 ms.
        SPEAKER_POSITIONS stSpkrAllocation;
        UCHAR             ucPortID[8];
        UCHAR             ucManufacturerName[2];
        UCHAR             ucProductCode[2];
        UCHAR             ucMNSAndSADs[64]; // This will include: ASCII string of Monitor name, List of 3 byte SADs, Zero padding
    };
    UCHAR Raw[ELD_BUFFER_SIZE];
#pragma pack()
} ELDV2, *PELDV2;

/** Structure that defines the contents of a 'get device list entry' verb response. */
typedef struct _DpcGetDeviceListEntryResponse
{
    union {
        struct
        {
            UCHAR PresenceDetect : 1; /**< Presence Detect. */
            UCHAR EldValid : 1;       /**< ELD Valid. */
            UCHAR Inactive : 1;       /**< Inactive */
            UCHAR Reserved : 5;       /**< Reserved space. */
        } s;
        UCHAR Raw; /**< Total value of the response. */
    };
} DpcGetDeviceListEntryType, *pDpcGetDeviceListEntryType;

typedef struct _DpcEldResponse
{
    union {
        struct
        {
            ULONG EldData : 8;   /**< ELD data byte at specified offset into the ELD memory. */
            ULONG Reserved : 23; /**< Reserved space. */
            ULONG EldValid : 1;  /**< ELD Valid indication. */
        } s;
        ULONG Raw; /**< Total value of the response. */
    };
} DpcEldResponseType, *pDpcEldResponseType;

typedef struct _SubNodeCountCommandResponse
{
    union {
        struct
        {
            ULONG TotalNumNodes : 8; /**< Bits 0:7 are the total number of fxn group nodes. */
            ULONG Reserved : 8;      /**< Bits 8:15 are reserved. */
            ULONG StartNodeNum : 8;  /**< Bits 16:23 are the starting node ID. */
            ULONG Reserved1 : 8;     /**< Bits 24:31 are reserved. */
        } s;
        ULONG Raw;
    };
} SubNodeCountCommandResponseType, *pSubNodeCountCommandResponse;

typedef struct _GetCapsResponse
{
    union {
        struct
        {
            ULONG NumChannelsLSB : 1;   /**< less significant bit of number of supported audio channels minus one. */
            ULONG InAmp : 1;            /**< Indicates that widget contains an input amplifier. */
            ULONG OutAmp : 1;           /**< Indicates that widget contains an output amplifier. */
            ULONG AmpParamOverride : 1; /**< If the widget contains its own amplifier parameters. */
            /**< Indicates that widget contains format information,
            and the “Supported Formats” and “Supported PCM Bits, Rates”
            should be queried for the widget’s format capabilities. */
            ULONG FormatOverride : 1;
            ULONG Stripe : 1; /**< Indicates whether the widget supports striping. Sec. 5.3.2.3. */
            /**< “Processing Controls” parameter should be queried for more
            information about the widget’s processing controls. */
            ULONG ProcWidget : 1;
            ULONG UnsolCapable : 1;      /**< Indicates whether audio widget supports unsolicited responses. */
            ULONG ConnList : 1;          /**< Indicates whether a connection list is present on the widget. */
            ULONG IsDigital : 1;         /**< Indicates digital capabilities. */
            ULONG PowerCntrl : 1;        /**< Indicates that the Power State control is supported on this widget. */
            ULONG LRSwap : 1;            /**< indicates the capability of swapping the left and right channels . */
            ULONG ProtectionCapable : 1; /**< Indicates if content protection is capable on the link. */
            ULONG NumChannelsExt : 3;    /**< high part of number of supported audio channels minus one. */
            ULONG Delay : 4;             /**< indicates the number of sample delays through the widget. */
            ULONG WidgetType : 4;        /**< Value that indicates what type of widget this is. */
            ULONG Reserved : 8;          /**< We dont care about these bits. */
        } s;
        ULONG Raw; /**< Total value of the response. */
    };
} GetCapsResponseType;

typedef struct _ConnectionListEntryResponse
{
    union {
        UCHAR ListEntry[4]; /**< Connection List Entry - Short version. */
        ULONG Raw;          /**< Total value of the response. */
    };
} ConnectionListEntryResponseType;

typedef struct _ConnectionSelectControlResponse
{
    union {
        struct
        {
            UCHAR ConnectionIndex : 8; /**< The index is in relation to the Connection List associated with the widget. */
            ULONG Reserved : 24;
        } s;
        ULONG Raw; /**< Total value of the payload. */
    };
} ConnectionSelectControlResponseType;

typedef struct _PowerStateResponse
{
    union {
        struct
        {
            ULONG PSSet : 4;           /**< Defines the current power setting of the node. */
            ULONG PSAct : 4;           /**< Indicates the actual power state of the node. */
            ULONG PSError : 1;         /**< is reported as set to 1, when the power state requested by the host is not possible at this time */
            ULONG PSClkStopOK : 1;     /**< (FG only) is FG capable of continuing proper operation even when the clock has been stopped */
            ULONG PSSettingsReset : 1; /**< 1 if settings reset occured in low power state */
            ULONG Reserved : 21;       /**< Reserved space - zeros. */
        } s;
        ULONG Raw; /**< Total value of the response. */
    };
} PowerStateResponseType, *pPowerStateResponseType;

typedef struct _AmplifierGainMutePayload
{
    union {
        struct
        {
            USHORT Index : 4; /**< Corresponds to the input’s offset in the Connection List. */
            USHORT reserved1 : 9;
            USHORT GetLeftRight : 1; /**< Indicated which amplifier is being affected. */
            USHORT reserved2 : 1;
            USHORT GetOutputInput : 1; /**< Indicates whether value programmed refers to output. */
        } s;
        USHORT Raw; /**< Total value of the payload. */
    };
} AmplifierGainMutePayload;

typedef struct _AmplifierGainMuteResponse
{
    union {
        struct
        {
            ULONG AmplifierGain : 7;
            ULONG AmplifierMute : 1;
            ULONG reserved : 24;
        } s;
        ULONG Raw; /**< Total value of the payload. */
    };
} AmplifierGainMuteResponse;

typedef struct _PinWidgetControlParams
{
    union {
        struct
        {
            /**< Encoded Packet Type controls the packet type used to transmit
            the audio stream on the associated digital Pin Widget. */
            UCHAR EPT : 3;
            UCHAR Reserved : 2;  /**< Reserved space - zeros. */
            UCHAR InEnable : 1;  /**< Allows the input path of the Pin Widget to be shut off. */
            UCHAR OutEnable : 1; /**< Allows the output path of the Pin Widget to be shut off. */
            UCHAR Reserved2 : 1; /**< Reserved space - zeros. */
        } digital;
        ULONG Raw; /**< Total value of the payload. */
    };
} PinWidgetControlParamsType, *pDpcPinWidgetControlParamsType;

typedef struct _ASPChannelMappingPayload
{
    union {
        struct
        {
            UCHAR ASPSlotNumber : 4; /**< ASP slot number. */
            UCHAR reserved : 4;      /**< Converter Channel Number. */
        } s;
        UCHAR Raw; /**< Total value of the payload. */
    };
} ASPChannelMappingPayload;

typedef struct _ASPChannelMappingResp
{
    union {
        struct
        {
            UCHAR ASPSlotNumber : 4; /**< ASP slot number. */
            UCHAR ChannelNumber : 4; /**< Converter Channel Number. */
            ULONG Reserved : 24;
        } s;
        ULONG Raw; /**< Total value of the payload. */
    };
} ASPChannelMappingResp;

typedef struct AifPacketHdmiHeader
{
    union {
        struct
        {
            UCHAR InfoFrameType : 8;    /**< Frame type */
            UCHAR InfoFrameVersion : 8; /**< InfoFrame Version. */
            UCHAR InfoFrameLength : 5;  /**< Reserved space. */
            UCHAR Reserved1 : 3;        /**< Reserved space, needs to be set 0. */
            UCHAR Checksum : 8;         /**< Checksum for the packet. */
        } s;
        UCHAR Raw[AIF_HDMI_HEADER_SIZE]; /**< Raw packet data. */
    };
} AifPacketHdmiHeaderType, *pAifPacketHdmiHeaderType;

typedef struct AifPacketDpHeader
{
    union {
        struct
        {
            UCHAR PacketType : 8;       /**< Frame type */
            UCHAR DataByteCountLSB : 8; /**< Databyte size (LSB part). */
            UCHAR DataByteCountMSB : 2; /**< Databyte size (MSB part). */
            UCHAR DpVersion : 6;        /**< Display Port version 0x11 - 1.1a. */
        } s;
        UCHAR Raw[AIF_DP_HEADER_SIZE]; /**< Raw packet data. */
    };
} AifPacketDpHeaderType, *pAifPacketDpHeaderType;

typedef struct AifPacketData
{
    union {
        struct
        {
            UCHAR ChannelCount : 3;       /**< Number of channels being rendered. */
            UCHAR Reserved : 1;           /**< Reserved space.*/
            UCHAR CodingType : 4;         /**< HDMI spec says this is always 0. */
            UCHAR SampleSize : 2;         /**< HDMI spec says this is always 0. */
            UCHAR SamplingFrequency : 3;  /**< HDMI spec says this is always 0. */
            UCHAR Reserved1 : 3;          /**< Reserved space. */
            UCHAR Reserved2 : 8;          /**< Reserved space. */
            UCHAR ChannelAllocation : 8;  /**< Specifies how various speaker locations are allocated to transmission channels. */
            UCHAR Reserved3 : 3;          /**< Reserved space. */
            UCHAR LevelShiftInfo : 4;     /**< Indicates downmix attenuation values. */
            UCHAR DownMixInhibitFlag : 1; /**< 1 indicates downmixing is prohibited, 0 otherwise. */
            UCHAR Reserved4[5];           /**< Reserved space. */
        } s;
        UCHAR Raw[AIF_DATA_SIZE]; /**< Raw packet data. */
    };
} AifPacketDataType, *pAifPacketDataType;

typedef struct _DIPIndexParams
{
    union {
        struct
        {
            UCHAR ByteIndex : 5; /**< Byte Index pointer in this packet. */
            /**< selects the target Data Island Packet buffer
            for subsequent DIP-Data and DIP-XmitCtrl control verbs. */
            UCHAR PacketIndex : 3;
        } s;
        UCHAR Raw; /**< Total value of the payload. */
    };
} DIPIndexParamsType, *pDpcDIPIndexParamsType;

typedef struct _DIPXmitCtlResp
{
    union {
        struct
        {
            UCHAR reserved1 : 6;
            UCHAR XmitCtl : 2;
            ULONG reserved2 : 24;
        } s;
        ULONG Raw;
    };
} DIPXmitCtlResp;

#pragma pack()

class DACVerifier
{
  public:
    DACVerifier();
    ~DACVerifier();

    HRESULT Initialize(WCHAR *pAudioDevName, PORT_TYPE portType, PGFX_ADAPTER_INFO pAdapterInfo);
    HRESULT GetDeviceAndRevisionIds();
    HRESULT VerifyDacProgramming(WAVEFORMATEXTENSIBLE *pFmt);
    HRESULT VerifyFinalState(UINT64 NumSamplesPlayed);
    HRESULT VerifyTC(DWORD Offset);
    HRESULT VerifyTC2(DWORD Offset);
    HRESULT VerifyMCTS(DWORD Offset);
    HRESULT VerifyMCTSEnable(DWORD Offset);

  private:
    DWORD mDeviceId;
    DWORD mRevisionId;
    DWORD mPipeId;
    DWORD mTranscoderId;
    INT32 mPinNodeInUse;
    INT32 mDEInUse;
    INT32 mConverterNodeInUse;
    INT32 mConverterIndexInUse;
    DWORD mLPIBRegOffset;
    DWORD mLPIBInitialCount;
    DWORD mLPIBFinalCount;

    DWORD mNumWidgets;
    DWORD mNumPinNodes;
    DWORD mNumConverterNodes;

    DWORD mPinNodeIds[MAX_NUM_PIN_NODES];
    DWORD mConverterNodeIds[MAX_NUM_CONVERTER_NODES];
    INT32 mVendorNodeId;

    DWORD mMonitorNameLen;
    CHAR  mAudioEndpointName[32];

    DWORD mDmaCounterValuesInitial[MAX_NUM_CONVERTER_NODES];
    DWORD mDmaCounterValueInUseInitial;
    DWORD mDmaCounterValueInUseFinal;

    PORT_TYPE mPortType;

    GFXMMIO *mGfxMMIO = NULL;

    WAVEFORMATEXTENSIBLE mWaveFmt;

    ELDV2       mEld;
    eStreamType mStreamType;
    ULONG       mChannelMask;
    pipe_id     mPIPEID;

    UCHAR mAifPacket[AIF_PACKET_SIZE];
    DWORD mInfoFrameSize;

    HRESULT ListNodes();
    HRESULT FindAssociatedConverterNode();
    HRESULT FindAssociatedPinNode();
    HRESULT FindPipeAndTranscoder();
    HRESULT GetELdFromPin(DWORD PinNodeId, DWORD DE);
    HRESULT GetELdFromTranscoder(DWORD TxId);
    HRESULT VerifyTranscoderConfig();
    HRESULT VerifyConfigBE();
    HRESULT VerifyConverterProgramming();
    HRESULT VerifyPinProgramming();
    HRESULT VerifyAspChannelMapping();
    HRESULT VerifyPowerState();
    HRESULT VerifyAudioInfoFrame();
    HRESULT VerifyOverAndUnderRunHDMI();
    HRESULT VerifyOverAndUnderRunDP();
    HRESULT GetDmaCounters();
    HRESULT GetSampligRateBaseMultDivFactors(DWORD &base, DWORD &mult, DWORD &div);

    DWORD GetConnectedAudioDeviceCount(DWORD PinNodeId, DWORD DE[MAX_NUM_TRANSCODERS]);
    UCHAR CalculateAifChecksum(const AifPacketDataType *_pAifData);
    void  MapChannelMaskToChannelAllocation(ULONG channelMask, UCHAR &channelAllocation);
    void  CreateAudioDeviceName(WCHAR *pAudioDevName);
    void  GetStreamProperties();
    void  CreateAudioInfoFrame();
    void  BuildAudioInfoFrame(AifPacketDataType &aifData);
};
