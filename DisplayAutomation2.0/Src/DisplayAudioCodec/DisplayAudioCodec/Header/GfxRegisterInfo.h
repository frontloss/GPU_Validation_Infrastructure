#pragma once
#include <Windows.h>
#include "GFXMMIO.h"

#define RESERVED2(x, y) x##y
#define RESERVED1(x, y) RESERVED2(x, y)
#define BITFIELD_BIT(bit) 1
#define BITFIELD_RANGE(ulLowBit, ulHighBit) ((ulHighBit) - (ulLowBit) + 1)
#define RANDOMNUMBER __LINE__
#define UNIQUENAME(ValueName) RESERVED1(ValueName, RANDOMNUMBER)

// Audio control state register
#define AUD_DIP_ELD_CTL_TRANSA_REG 0x650B4
#define AUD_DIP_ELD_CTL_TRANSB_REG 0x651B4
#define AUD_DIP_ELD_CTL_TRANSC_REG 0x652B4
#define AUD_DIP_ELD_CTL_TRANSD_REG 0x653B4

// ELD buffer register
#define AUD_HDMIW_HDMIEDID_TRANSA_REG 0x65050
#define AUD_HDMIW_HDMIEDID_TRANSB_REG 0x65150
#define AUD_HDMIW_HDMIEDID_TRANSC_REG 0x65250
#define AUD_HDMIW_HDMIEDID_TRANSD_REG 0x65350

#define AUD_C1_MISC_CTRL 0x65010
#define AUD_C2_MISC_CTRL 0x65110
#define AUD_C3_MISC_CTRL 0x65210
#define AUD_C4_MISC_CTRL 0x65310
#define AUD_HDA_DMA_REG 0x65E00
#define AUD_PIN_ELD_CP_VLD_REG 0x650C0
#define AUD_PIN_PIPE_CONN_SEL_CTRL_RO_REG 0x650AC
#define AUD_TCA_PIN_PIPE_CONN_ENTRY_LNGTH_RO_REG 0x650A8
#define AUD_TCB_PIN_PIPE_CONN_ENTRY_LNGTH_RO_REG 0x651A8
#define AUD_TCC_PIN_PIPE_CONN_ENTRY_LNGTH_RO_REG 0x652A8
#define AUD_TCD_PIN_PIPE_CONN_ENTRY_LNGTH_RO_REG 0x653A8
#define AUD_PIPE_CONV_CFG_RO_REG 0x6507C
#define AUD_DP_DIP_STATUS_REG 0x65F20
#define AUD_OUT_CHAN_MAP_REG 0x65088
#define AUD_C1_STR_DESC_RO_REG 0x65084
#define AUD_C2_STR_DESC_RO_REG 0x65184
#define AUD_C3_STR_DESC_RO_REG 0x65284
#define AUD_C4_STR_DESC_RO_REG 0x65384
#define AUD_C1_DIG_CNVT_RO_REG 0x65080
#define AUD_C2_DIG_CNVT_RO_REG 0x65180
#define AUD_C3_DIG_CNVT_RO_REG 0x65280
#define AUD_C4_DIG_CNVT_RO_REG 0x65380
#define AUD_TCA_DIP_ELD_CTRL_ST_REG 0x650B4
#define AUD_TCB_DIP_ELD_CTRL_ST_REG 0x651B4
#define AUD_TCC_DIP_ELD_CTRL_ST_REG 0x652B4
#define AUD_TCD_DIP_ELD_CTRL_ST_REG 0x653B4
#define AUD_TCA_VRR_COUNTER 0x650B8
#define AUD_TCB_VRR_COUNTER 0x651B8
#define AUD_TCC_VRR_COUNTER 0x652B8
#define AUD_TCD_VRR_COUNTER 0x653B8
#define AUD_HDA_LPIB0_ 0x65E04
#define AUD_CHICKEN_BIT_REG 0x65F10
#define AUD_CHICKENBIT_REG_2 0x65F0C
#define AUD_PWRST_REG 0x6504C
#define AUDIO_PIN_BUF_CTL_REG 0x48414
#define AUD_FREQ_CNTRL_REG 0x65900
#define AUD_VID_DID_RO 0x65020
#define AUD_RID_RO 0x65024
#define CDCLK_CTL 0x46000
#define AUD_CONFIG_TRANSA 0x65000
#define AUD_CONFIG_TRANSB 0x65100
#define AUD_CONFIG_TRANSC 0x65200
#define AUD_CONFIG_TRANSD 0x65300
#define AUD_CONFIG_2_TRANSA 0x65004
#define AUD_CONFIG_2_TRANSB 0x65104
#define AUD_CONFIG_2_TRANSC 0x65204
#define AUD_CONFIG_2_TRANSD 0x65304
#define AUD_TCA_M_CTS_ENABLE 0x65028
#define AUD_TCB_M_CTS_ENABLE 0x65128
#define AUD_TCC_M_CTS_ENABLE 0x65228
#define AUD_TCD_M_CTS_ENABLE 0x65328
#define AUD_C1_MISC_CTRL 0x65010
#define AUD_C2_MISC_CTRL 0x65110
#define AUD_C3_MISC_CTRL 0x65210
#define AUD_C4_MISC_CTRL 0x65310
#define AUD_TCA_INFOFR_REG 0x65054
#define AUD_TCB_INFOFR_REG 0x65154
#define AUD_TCC_INFOFR_REG 0x65254
#define AUD_TCD_INFOFR_REG 0x65354
#define AUD_TCA_EDID_DATA 0x65050
#define AUD_TCB_EDID_DATA 0x65150
#define AUD_TCC_EDID_DATA 0x65250
#define AUD_TCD_EDID_DATA 0x65350
#define AUD_ICW_REG 0x65F00
#define AUD_IRR_REG 0x65F04
#define AUD_ICS_REG 0x65F08
#define PWR_WELL_CTL1 0x45400
#define PWR_WELL_CTL2 0x45404
#define PWR_WELL_CTL 0x45408
#define CDCLK_CTL 0x46000
#define CDCLK_CTL_PLL_ENABLE 0x46070
#define TRANS_DDI_FUNC_CTLA 0x60400
#define TRANS_DDI_FUNC_CTLB 0x61400
#define TRANS_DDI_FUNC_CTLC 0x62400
#define TRANS_DDI_FUNC_CTLD 0x63400
#define AUD_HDA_LPIB0_REG 0x65E04
#define AUD_HDA_LPIB1_REG 0x65E08
#define AUD_HDA_LPIB2_REG 0x65E0C
#define AUD_HDA_LPIB3_REG 0x65E14
#define Audio_M_CTS_TCA 0x65F44
#define Audio_M_CTS_TCB 0x65F54
#define Audio_M_CTS_TCC 0x65F64
#define Audio_M_CTS_TCD 0x65F74
#define AUD_CONFIG_BE_REG 0x65EF0

/*Register detail: AUD_HDMI_FIFO_STATUS
 * Audio function reset
 * Underrun: underrun after the Stream ID is set in the Converter and Controller is not sending any data to the codec
 * Overflow: overrun in the FIFO inside the clock crossing logic between CDCLK and DOTCLK.
 */
#define AUD_HDMI_FIFO_STATUS_RO 0x650D4
/*Register detail: AUD_PIPE_CONV_CFG
 * Amp Mute Status
 * Converter stream ID
 * Digital transmission enable - digital data can be blocked from passing through the node
 * State of the output path of the Pin Widget
 */
#define AUD_PIPE_CONV_CFG_RO 0x6507C

#define CODEC_SLEEP_STATE_ACTIVE_STATE 0x0 // If it is zero, codec is not in sleep state.
#define CODEC_SLEEP_STATE_SLEEP_STATE 0x1  // When set the Codec is in sleep state.

typedef union _AUD_VID_DID {
    struct
    {
        UINT32 DeviceID : BITFIELD_RANGE(0, 15);
        UINT32 VendorID : BITFIELD_RANGE(16, 31);
    };
    UINT32 ulValue;
} AUD_VID_DID;

typedef enum _CODEC_SLEEP_STATE_SKL
{
    CODEC_SLEEP_STATE_ACTIVE_STATE_SKL = 0x0, // If it is zero, codec is not in sleep state.
    CODEC_SLEEP_STATE_SLEEP_STATE_SKL  = 0x1, // When set the Codec is in sleep state.
} CODEC_SLEEP_STATE_SKL;

typedef enum _ENABLE_MMIO_PROGRAMMING_SKL
{
    ENABLE_MMIO_PROGRAMMING_HDAUDIO_SKL = 0x0, // Programming through HDAudio Azalia
    ENABLE_MMIO_PROGRAMMING_MMIO_SKL    = 0x1, // Programming through MMIO PIO Debug registers
} ENABLE_MMIO_PROGRAMMING_SKL;

typedef unsigned int SIZE32BITS;

typedef union _HSW_AUD_CNTL_STRUCT {
    SIZE32BITS ulValue;
    struct
    {
        SIZE32BITS ulDipRamAcessAddress : 4;  // bit 3:0
        SIZE32BITS bEldAck : 1;               // bit 4
        SIZE32BITS ulEldAccessAddress : 5;    // bit 9:5
        SIZE32BITS ulEldBufferSize : 5;       // bit 14:10
        SIZE32BITS UNIQUENAME(Reserved) : 1;  // bit 15
        SIZE32BITS ulDipTransmissionFreq : 2; // bit 17:16
        SIZE32BITS ulDipBufferIndex : 3;      // bit 20:18
        SIZE32BITS ulDipTypeEnableStatus : 4; // bit 24:21 ; gives the status of various data island pkts
        SIZE32BITS UNIQUENAME(Reserved) : 4;  // bit 28:25
        SIZE32BITS ulDipPortSelect : 4;       // bit 31:28 (r)
    };

} AUD_CNTL_ST, *PAUD_CNTL_ST;

typedef union _HSW_AUD_HDMIW_HDMIEDID_STRUCT {
    SIZE32BITS ulValue;
    struct
    {
        SIZE32BITS ulEdidHdmiDataBlk : 32; // bit 31:0
    };
} HSW_AUD_HDMIW_HDMIEDID_ST, *PHSW_AUD_HDMIW_HDMIEDID_ST;

typedef union _HSW_AUD_PIN_ELD_CP_VLD_STRUCT {
    SIZE32BITS ulValue;
    struct
    {
        SIZE32BITS bEldValidA : 1;            // bit 0
        SIZE32BITS bCPReadyA : 1;             // bit 1
        SIZE32BITS bAudioOutputEnableA : 1;   // bit 2
        SIZE32BITS bAudioInActiveA : 1;       // bit 3
        SIZE32BITS bEldValidB : 1;            // bit 4
        SIZE32BITS bCPReadyB : 1;             // bit 5
        SIZE32BITS bAudioOutputEnableB : 1;   // bit 6
        SIZE32BITS bAudioInActiveB : 1;       // bit 7
        SIZE32BITS bEldValidC : 1;            // bit 8
        SIZE32BITS bCPReadyC : 1;             // bit 9
        SIZE32BITS bAudioOutputEnableC : 1;   // bit 10
        SIZE32BITS bAudioInActiveC : 1;       // bit 11
        SIZE32BITS bEldValidD : 1;            // bit 12
        SIZE32BITS bCPReadyD : 1;             // bit 13
        SIZE32BITS bAudioOutputEnableD : 1;   // bit 14
        SIZE32BITS bAudioInActiveD : 1;       // bit 15
        SIZE32BITS UNIQUENAME(Reserved) : 16; // bit 31:16
    };
} AUD_PIN_ELD_CP_VLD_ST, *PAUD_PIN_ELD_CP_VLD_ST;

typedef union _AUD_CHICKENBIT_REG_SKL {
    struct
    {
        UINT32 EnableMmioProgramming : BITFIELD_BIT(0);                                   // ENABLE_MMIO_PROGRAMMING_SKL
        UINT32 AudioTimestampTestMode : BITFIELD_BIT(1);                                  // AUDIO_TIMESTAMP_TEST_MODE_SKL
        UINT32 EpssDisable : BITFIELD_BIT(2);                                             // EPSS_DISABLE_SKL
        UINT32 Fabrication3244Disable : BITFIELD_BIT(3);                                  // FABRICATION_32_44_DISABLE_SKL
        UINT32 PatternGen2ChEn : BITFIELD_BIT(4);                                         // PATTERN_GEN_2CH_EN_SKL
        UINT32 PatternGen8ChEn : BITFIELD_BIT(5);                                         // PATTERN_GEN_8CH_EN_SKL
        UINT32 DisableTimestampFixForDphbr : BITFIELD_BIT(6);                             // DISABLE_TIMESTAMP_FIX_FOR_DPHBR_SKL
        UINT32 DisableTimestampDeltaErrorFor32_44Khz : BITFIELD_BIT(7);                   // DISABLE_TIMESTAMP_DELTA_ERROR_FOR_32_44_KHZ_SKL
        UINT32 DisablePresenceDetectPulseTransitionWhenUnsolIsDisabled : BITFIELD_BIT(8); // DISABLE_PRESENCE_DETECT_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_SKL
        UINT32 DisableEldValidPulseTransitionWhenUnsolIsDisabled : BITFIELD_BIT(9);       // DISABLE_ELD_VALID_PULSE_TRANSITION_WHEN_UNSOL_IS_DISABLED_SKL
        UINT32 BlockAudioDataFromReachingThePort : BITFIELD_BIT(10);                      // BLOCK_AUDIO_DATA_FROM_REACHING_THE_PORT_SKL
        UINT32 UNIQUENAME(Reserved) : BITFIELD_RANGE(11, 13);                             // MBZ
        UINT32 iDispLinkSleepState : BITFIELD_BIT(14);                                    // CODEC_SLEEP_STATE

        /*****************************************************************************\
        When set the Codec wake signal will be generated. It overwrites the internal logic to generate the codec wake to controller.
        \*****************************************************************************/
        UINT32 CodecWakeOverwriteToDacfeunit : BITFIELD_BIT(15); //

        /*****************************************************************************\
        Reserved for future use.
        \*****************************************************************************/
        UINT32 ChickenBitsForDacbeUnit : BITFIELD_RANGE(16, 17); //

        /*****************************************************************************\
        When set disables the fix for the corner case of data flit error at the end of frame with all 1's on data follwoed by sync.
        \*****************************************************************************/
        UINT32 DisableDacfeProtocolFixForDataFlitErrorInTheEndOfFrame : BITFIELD_BIT(18); //

        /*****************************************************************************\
        When set the the fix to report the default value of 3 in the device index in DP1.2 mode will b removed.
        \*****************************************************************************/
        UINT32 Dp12DeviceIndexFixDisable : BITFIELD_BIT(19); //

        /*****************************************************************************\
        When set enables the 20bit support reporting in the Converter widgets capabilities .
        \*****************************************************************************/
        UINT32 Enable20BitSupportForSampleRate : BITFIELD_BIT(20); //

        /*****************************************************************************\
        When set disables the bclk frame sync fix on bclk counter.
        \*****************************************************************************/
        UINT32 DisableBclkFrameSyncFixOnBclkCounter : BITFIELD_BIT(21); //
        UINT32 SamplePresentEnableChickenBitDACBE : BITFIELD_BIT(22);
        UINT32 ECCOverwriteEnableChickenBitDACBE : BITFIELD_BIT(23);

        /*****************************************************************************\
        Reserved for future use.
        \*****************************************************************************/
        UINT32 ChickenBits25To24ForDacfpUnit : BITFIELD_RANGE(24, 25); //

        /*****************************************************************************\
        Reserved for future use.
        \*****************************************************************************/
        UINT32 ChickenBits26ForDacfpUnit : BITFIELD_BIT(26); // MBZ

        /*****************************************************************************\
        Reserved for future use.
        \*****************************************************************************/
        UINT32 ChickenBits29To27ForDacfpUnit : BITFIELD_RANGE(27, 29); //

        /*****************************************************************************\
        Its a read only bit to indicate the vanilla bit setting of vendor verb.
        \*****************************************************************************/
        UINT32 VanillaBitEnableForThreeWidgets : BITFIELD_BIT(30); //

        /*****************************************************************************\
        Its a read only bit to indicate the vanilla bit setting of vendor verb.
        \*****************************************************************************/
        UINT32 VanillaBitEnableForDp12 : BITFIELD_BIT(31); //
    };
    UINT32 ulValue;

} AUD_CHICKENBIT_REG_SKL, *PAUD_CHICKENBIT_REG_SKL;

typedef union _AUD_CHICKENBIT_REG_2 {
    struct
    {
        UINT32 EnableVariableRefreshRateCounter : BITFIELD_BIT(0);
        UINT32 EnableResponsetoinvalidverbs : BITFIELD_BIT(1);
        UINT32 CodecSleepStateMachinestatus : BITFIELD_RANGE(2, 4);
        UINT32 UNIQUENAME(Reserved) : BITFIELD_BIT(5);
        UINT32 DisableSyncCounterrorgeneration : BITFIELD_BIT(6);
        UINT32 Disablecodecwakeevent : BITFIELD_BIT(7);
        UINT32 DACFPcdclockdelay : BITFIELD_RANGE(8, 9);
        UINT32 UNIQUENAME(Reserved) : BITFIELD_RANGE(10, 15);
        UINT32 PipeAStickybitVRRdebug : BITFIELD_BIT(16);
        UINT32 PipeBStickybitVRRdebug : BITFIELD_BIT(17);
        UINT32 PipeCStickybitVRRdebug : BITFIELD_BIT(18);
        UINT32 PipeDStickybitVRRdebug : BITFIELD_BIT(19);
        UINT32 TimestampProgrammableDPSpecVersionFix : BITFIELD_BIT(20);
        UINT32 UNIQUENAME(Reserved) : BITFIELD_BIT(21);
        UINT32 TimestampDPECCFix : BITFIELD_BIT(22);
        UINT32 SilentStreamDPModeChangeFix : BITFIELD_BIT(23);
        UINT32 Disable8Tmodefix : BITFIELD_BIT(24);
        UINT32 UNIQUENAME(Reserved) : BITFIELD_RANGE(25, 27);
        UINT32 LowerCDClockSupport : BITFIELD_BIT(27);
        UINT32 PortSelect : BITFIELD_RANGE(28, 31);
    };
    UINT32 ulValue;

} AUD_CHICKENBIT_REG2, *PAUD_CHICKENBIT_REG_2;

typedef union _TRANS_DDI_FUNC_CTL {
    struct
    {
        SIZE32BITS HDMI_Scrambling_Enabled : BITFIELD_BIT(0);
        SIZE32BITS Port_Width_Selection : BITFIELD_RANGE(1, 3);
        SIZE32BITS High_TMDS_Char_Rate : BITFIELD_BIT(4);
        SIZE32BITS Multistream_HDCP_Select : BITFIELD_BIT(5);
        SIZE32BITS HDMI_Scrambler_Reset_frequency : BITFIELD_BIT(6);
        SIZE32BITS HDMI_Scrambler_CTS_Enable : BITFIELD_BIT(7);
        SIZE32BITS DP_VC_Payload_Allocate : BITFIELD_BIT(8);
        SIZE32BITS HDMI_DVI_HDCP_Signaling : BITFIELD_BIT(9); // This bit enables HDCP signaling for HDMI and DVI modes. This bit must be used in conjunction with the HDCP
                                                              // registers. This bit is ignored when not in HDMI or DVI modes.
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(10, 11);
        SIZE32BITS EDP_DSI_Input_Select
            : BITFIELD_RANGE(12, 14); // These bits determine the input to transcoder EDP or transcoder DSI. These bits are ignored by the other transcoders.
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(15);
        SIZE32BITS Sync_Polarity : BITFIELD_RANGE(16, 17); // This field indicates the polarity of Hsync and Vsync.
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(18, 19);
        SIZE32BITS Bits_Per_Color : BITFIELD_RANGE(20, 22); // This field selects the number of bits per color output on the DDI connected to this transcoder. Dithering should be
                                                            // enabled when selecting a pixel color depth higher or lower than the pixel color depth of the frame buffer.
        SIZE32BITS DSS_branch_Select_for_EDP : BITFIELD_BIT(23);
        SIZE32BITS TRANS_DDI_Mode_Select : BITFIELD_RANGE(24, 26);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(27);
        SIZE32BITS DDI_Select
            : BITFIELD_RANGE(28, 30); // These bits determine which DDI port this transcoder will connect to. It is not valid to enable and direct more than one transcoder to one
                                      // DDI, except when using DisplayPort multistreaming. These bits are ignored by transcoder EDP since it can only connect to DDI A (EDP DDI)
        SIZE32BITS TRANS_DDI_Function_Enable : BITFIELD_BIT(31); // This bit enables the transcoder DDI function.
    };
    SIZE32BITS ulValue;
} AUD_TRANS_DDI_FUNC_CTL;

typedef union _PWR_WELL_CTL2 {
    struct
    {
        SIZE32BITS MiscIOPowerState : BITFIELD_BIT(0);         //
        SIZE32BITS MiscIOPowerRequest : BITFIELD_BIT(1);       //
        SIZE32BITS DDIAIOPowerState : BITFIELD_BIT(2);         //
        SIZE32BITS DDIAIOPowerRequest : BITFIELD_BIT(3);       //
        SIZE32BITS DDIBIOPowerState : BITFIELD_BIT(4);         //
        SIZE32BITS DDIBIOPowerRequest : BITFIELD_BIT(5);       //
        SIZE32BITS DDICIOPowerState : BITFIELD_BIT(6);         //
        SIZE32BITS DDICIOPowerRequest : BITFIELD_BIT(7);       //
        SIZE32BITS DDIDIOPowerState : BITFIELD_BIT(8);         //
        SIZE32BITS DDIDIOPowerRequest : BITFIELD_BIT(9);       //
        SIZE32BITS Reserved : BITFIELD_RANGE(10, 27);          //
        SIZE32BITS PowerWell1State : BITFIELD_BIT(28);         //
        SIZE32BITS DriverPowerWell1Request : BITFIELD_BIT(29); //
        SIZE32BITS PowerWell2State : BITFIELD_BIT(30);         //
        SIZE32BITS DriverPowerWell2Request : BITFIELD_BIT(31); //
    };
    SIZE32BITS ulValue;

} AUD_PWR_WELL_CTL2;

typedef union _PWR_WELL_CTL {
    struct
    {
        SIZE32BITS PowerWell1State : BITFIELD_BIT(0);   //
        SIZE32BITS PowerWell1Request : BITFIELD_BIT(1); //
        SIZE32BITS PowerWell2State : BITFIELD_BIT(2);   //
        SIZE32BITS PowerWell2Request : BITFIELD_BIT(3); //
        SIZE32BITS PowerWell3State : BITFIELD_BIT(4);   //
        SIZE32BITS PowerWell3Request : BITFIELD_BIT(5); //
        SIZE32BITS PowerWell4State : BITFIELD_BIT(6);   //
        SIZE32BITS PowerWell4Request : BITFIELD_BIT(7); //
        SIZE32BITS Reserved : BITFIELD_RANGE(8, 31);
    };
    SIZE32BITS ulValue;

} AUD_PWR_WELL_CTL;

typedef union _AUD_PWRST_RO // 0x6504c
{
    struct
    {
        SIZE32BITS PinBWidgetPwrStSet : BITFIELD_RANGE(0, 1);
        SIZE32BITS PinBWidgetPwrStCurr : BITFIELD_RANGE(2, 3);
        SIZE32BITS PinCWidgetPwrStSet : BITFIELD_RANGE(4, 5);
        SIZE32BITS PinCWidgetPwrStCurr : BITFIELD_RANGE(6, 7);
        SIZE32BITS PinDWidgetPwrStSet : BITFIELD_RANGE(8, 9);
        SIZE32BITS PinDWidgetPwrStCurr : BITFIELD_RANGE(10, 11);
        SIZE32BITS Convertor1WidgetPwrStReq : BITFIELD_RANGE(12, 13);
        SIZE32BITS Convertor1WidgetPwrStCurr : BITFIELD_RANGE(14, 15);
        SIZE32BITS Convertor2WidgetPwrStReq : BITFIELD_RANGE(16, 17);
        SIZE32BITS Convertor2WidgetPwrStCurr : BITFIELD_RANGE(18, 19);
        SIZE32BITS Converter3WidgetPwrStReq : BITFIELD_RANGE(20, 21);
        SIZE32BITS Converter3WidgetPwrStCurr : BITFIELD_RANGE(22, 23);
        SIZE32BITS FuncGrpDevPwrStSet : BITFIELD_RANGE(24, 25);
        SIZE32BITS FuncGrpDevPwrStCurr : BITFIELD_RANGE(26, 27);
        SIZE32BITS Converter4WidgetPwrStReq : BITFIELD_RANGE(28, 29);
        SIZE32BITS Converter4WidgetPwrStCurr : BITFIELD_RANGE(30, 31);
    };
    SIZE32BITS ulValue;

} AUD_PWRST_RO, *PAUD_PWRST_RO;

typedef union _AUDIO_PIN_BUF_CTL_SKL {
    struct
    {
        SIZE32BITS PullupSlew : BITFIELD_RANGE(0, 3);
        SIZE32BITS PullupStrength : BITFIELD_RANGE(4, 8);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(9, 11);
        SIZE32BITS PulldownSlew : BITFIELD_RANGE(12, 15);
        SIZE32BITS PulldownStrength : BITFIELD_RANGE(16, 20);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(21, 23);
        SIZE32BITS Spare : BITFIELD_RANGE(24, 26);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(27);
        SIZE32BITS Hysteresis : BITFIELD_RANGE(28, 29);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(30);
        SIZE32BITS Enable : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;

} AUDIO_PIN_BUF_CTL_SKL, *PAUDIO_PIN_BUF_CTL_SKL;

typedef union _AUD_PIPEANDCONVERTER {
    struct
    {
        SIZE32BITS ConvertorAdigen : BITFIELD_BIT(0);           //
        SIZE32BITS ConvertorBdigen : BITFIELD_BIT(1);           //
        SIZE32BITS ConvertorCdigen : BITFIELD_BIT(2);           //
        SIZE32BITS ConvertorDdigen : BITFIELD_BIT(3);           //
        SIZE32BITS Convertor1StreamID : BITFIELD_RANGE(4, 7);   //
        SIZE32BITS Convertor2StreamID : BITFIELD_RANGE(8, 11);  //
        SIZE32BITS Convertor3StreamID : BITFIELD_RANGE(12, 15); //
        SIZE32BITS PortBoutEnable : BITFIELD_BIT(16);           //
        SIZE32BITS PortCoutEnable : BITFIELD_BIT(17);           //
        SIZE32BITS PortDoutEnable : BITFIELD_BIT(18);           //
        SIZE32BITS PortFoutEnable : BITFIELD_BIT(19);           //
        SIZE32BITS PortBampMuteStatus : BITFIELD_BIT(20);       //
        SIZE32BITS PortCampMuteStatus : BITFIELD_BIT(21);       //
        SIZE32BITS PortDampMuteStatus : BITFIELD_BIT(22);       //
        SIZE32BITS PortFampMuteStatus : BITFIELD_BIT(23);       //
        SIZE32BITS AudReservedBit : BITFIELD_RANGE(24, 27);     //
        SIZE32BITS Convertor4StreamID : BITFIELD_RANGE(28, 31); //
    };
    SIZE32BITS ulValue;

} AUD_PIPEANDCONVERTER;

typedef union _CDCLK_CTL {
    struct
    {
        SIZE32BITS CDFrequencyDecimal
            : BITFIELD_RANGE(0, 10); // This field selects the decimal value of the frequency for CD clock, which is used to generate divided down clocks for some display engine
                                     // timers. This value is represented in a 10.1 format with 10 integer bits and 1 fractional bit.
        SIZE32BITS Reserved : BITFIELD_RANGE(11, 14); //
        SIZE32BITS SSAPrecharge : BITFIELD_BIT(15);
        SIZE32BITS SSAPrechargeEnable : BITFIELD_BIT(16); //
        SIZE32BITS OverrideCrystal
            : BITFIELD_BIT(17); // Debug: This field selects which DPLL is the source for CD2X clock. It disables and resets the CD2X dividers on the DPLL that is not selected.
        SIZE32BITS OverrideSlowClock : BITFIELD_BIT(18);    //
        SIZE32BITS CD2XPipeSelect : BITFIELD_RANGE(19, 21); //
        SIZE32BITS CD2XDivider : BITFIELD_RANGE(22, 23);    //
        SIZE32BITS ReservedMBZ : BITFIELD_RANGE(24, 31);    //
    };
    SIZE32BITS ulValue;
} AUD_CDCLK_CTL;

typedef union _CDCLK_PLL_ENABLE {
    struct
    {
        SIZE32BITS PLLRatio : BITFIELD_RANGE(0, 7);
        SIZE32BITS Reserved : BITFIELD_RANGE(8, 21);
        SIZE32BITS FreqChangeAck : BITFIELD_BIT(22);
        SIZE32BITS FreqChangeReq : BITFIELD_BIT(23);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 25);
        SIZE32BITS SlowClockLock : BITFIELD_BIT(26);
        SIZE32BITS SlowClockEnable : BITFIELD_BIT(27);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(28, 29);
        SIZE32BITS PLLLock : BITFIELD_BIT(30);
        SIZE32BITS PLLEnable : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;
} AUD_CDCLK_PLL_ENABLE;

typedef union _GEN9_ICS_MAILBOX {
    ULONG ulValue;
    struct
    {
        unsigned int bImmediateCommandBusy : 1; // bit[0]
        unsigned int bImmediateResultValid : 1; // bit[1]
        unsigned int Reserved : 30;
    };
} GEN9_ICS_MAILBOX, *PGEN9_ICS_MAILBOX;

typedef union _AUD_FREQ_CNTRL {
    struct
    {
        /******************************************************************************************************************/
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 2); //

        /******************************************************************************************************************
        Indicates that iDISPLAY Audio Link will run at 48MHz. This bit is defaulted to 0.
        BIOS or System Software must pre-program B96 before the iDISPLAY Audio Link is brought out from reset.
        \******************************************************************************************************************/
        SIZE32BITS _48MhzBclk : BITFIELD_BIT(3); //

        /******************************************************************************************************************
        Indicates that iDISPLAY Audio Link will run at 96MHz. This bit is defaulted to 1.
        BIOS or System Software must pre-program B96 before the iDISPLAY Audio Link is brought out from reset.
        \******************************************************************************************************************/
        SIZE32BITS _96MhzBclk : BITFIELD_BIT(4); //

        /******************************************************************************************************************/
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(5, 10); //

        /******************************************************************************************************************
        These bits are used to pullin the frame sync detection logic earlier to compensate for PV issues if any.
        Audio codec starts driving the SDI pin earlier by the number of clocks programmed by this register.
        \******************************************************************************************************************/
        SIZE32BITS DetectFrameSyncEarly : BITFIELD_RANGE(11, 12); // DETECT_FRAME_SYNC_EARLY

        /******************************************************************************************************************
        Setting this bit will bypass the flop in the IO in the Audout path.
        \******************************************************************************************************************/
        SIZE32BITS BypassFlop : BITFIELD_BIT(13); // BYPASS_FLOP

        /******************************************************************************************************************
        Indicates the T mode SDI is operating in. BIOS or System Software must pre-program the T-mode register.
        a. before the iDISPLAY Audio Link is brought out from Link Reset,
        b. to a value which is consistent with the value of the its counterpart T-mode bit in the Audio Controller.
        c. to a value which is within the electrical capabilities of the platform.
        Note that even T modes are prohibited from being used with any BCLK frequency which has an odd number of bit cells.
        Example, 2T mode is incompatible with BCLK=6MHz (125 bit cells).
        \******************************************************************************************************************/
        SIZE32BITS TMode : BITFIELD_RANGE(14, 15); // TMODE

        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 31); //
    };

    SIZE32BITS Value;

} REG_AUD_FREQ_CNTRL;

typedef union _AUD_PIN_ELD_CP_VLD {
    struct
    {
        /******************************************************************************************************************
        See ELD_validC descripion.
        \******************************************************************************************************************/
        SIZE32BITS EldValida : BITFIELD_BIT(0); // ELD_VALIDA

        /******************************************************************************************************************
        See CP_ReadyC description.
        \******************************************************************************************************************/
        SIZE32BITS CpReadya : BITFIELD_BIT(1); // CP_READYA

        /******************************************************************************************************************
        This bit directs audio to the device connected to this transcoder. When enabled along with Inactive set to 0 and audio data is available, the audio data will be combined
        with the video data and sent over this transcoder. The audio unit uses the status of this bit to indicate presence of the HDMI/DP output to the audio driver. This is
        transcoder based.
        \******************************************************************************************************************/
        SIZE32BITS AudioOutputEnablea : BITFIELD_BIT(2); // AUDIO_OUTPUT_ENABLEA

        /******************************************************************************************************************
        Inactive: When this bit is set, a digital display sink device has been attached but not active for streaming audio.
        \******************************************************************************************************************/
        SIZE32BITS AudioInactivea : BITFIELD_BIT(3); // AUDIO_INACTIVEA

        /******************************************************************************************************************
        See ELD_validC descripion.
        \******************************************************************************************************************/
        SIZE32BITS EldValidb : BITFIELD_BIT(4); // ELD_VALIDB

        /******************************************************************************************************************
        See CP_ReadyC description.
        \******************************************************************************************************************/
        SIZE32BITS CpReadyb : BITFIELD_BIT(5); // CP_READYB

        /******************************************************************************************************************
        This bit directs audio to the device connected to this transcoder. When enabled along with Inactive set to 0 and audio data is available, the audio data will be combined
        with the video data and sent over this transcoder. The audio unit uses the status of this bit to indicate presence of the HDMI/DP output to the audio driver. This is
        transcoder based.
        \******************************************************************************************************************/
        SIZE32BITS AudioOutputEnableb : BITFIELD_BIT(6); // AUDIO_OUTPUT_ENABLEB

        /******************************************************************************************************************
        Inactive: When this bit is set, a digital display sink device has been attached but not active for streaming audio.
        \******************************************************************************************************************/
        SIZE32BITS AudioInactiveb : BITFIELD_BIT(7); // AUDIO_INACTIVEB

        /******************************************************************************************************************
        This R/W bit reflects the state of the ELD data written to the ELD RAM. After writing the ELD data, the video software must set this bit to 1 to indicate that the ELD data
        is valid. At audio codec initialization, or on a hotplug event, this bit is set to 0 by the video software. This bit is reflected in the audio pin complex widget as the ELD
        valid status bit. This is transcoder based.
        \******************************************************************************************************************/
        SIZE32BITS EldValidc : BITFIELD_BIT(8); // ELD_VALIDC

        /******************************************************************************************************************
        This R/W bit reflects the state of CP request from the audio unit. When an audio CP request has been serviced, it must be reset to 1 by the video software to indicate that
        the CP request has been serviced. This is transcoder based. Software should add a delay of 1ms before updating the CP ready bit. This is needed to make sure that all the
        pending unsolicited responses are cleared (transmitted to HD audio) before CP ready unsolicited responses is generated. This is needed in case of DP MST is enabled and when
        many changes to PD, ELDV and CP ready bits are done during mode set.
        \******************************************************************************************************************/
        SIZE32BITS CpReadyc : BITFIELD_BIT(9); // CP_READYC

        /******************************************************************************************************************
        This bit directs audio to the device connected to this transcoder. When enabled along with Inactive set to 0 and audio data is available, the audio data will be combined
        with the video data and sent over this transcoder. The audio unit uses the status of this bit to indicate presence of the HDMI/DP output to the audio driver.
        \******************************************************************************************************************/
        SIZE32BITS AudioOutputEnablec : BITFIELD_BIT(10); // AUDIO_OUTPUT_ENABLEC

        /******************************************************************************************************************
        Inactive: When this bit is set, a digital display sink device has been attached but not active for streaming audio.
        \******************************************************************************************************************/
        SIZE32BITS AudioInactivec : BITFIELD_BIT(11); // AUDIO_INACTIVEC

        /******************************************************************************************************************
        This R/W bit reflects the state of the ELD data written to the ELD RAM. After writing the ELD data, the video software must set this bit to 1 to indicate that the ELD data
        is valid. At audio codec initialization, or on a hotplug event, this bit is set to 0 by the video software. This bit is reflected in the audio pin complex widget as the ELD
        valid status bit. This is transcoder based.
        \******************************************************************************************************************/
        SIZE32BITS EldValidd : BITFIELD_BIT(12); // ELD_VALIDD

        /******************************************************************************************************************
         This R/W bit reflects the state of CP request from the audio unit. When an audio CP request has been serviced, it must be reset to 1 by the video software to indicate that
        the CP request has been serviced. This is transcoder based. Software should add a delay of 1ms before updating the CP ready bit. This is needed to make sure that all the
        pending unsolicited responses are cleared (transmitted to HD audio) before CP ready unsolicited responses is generated. This is needed in case of DP MST is enabled and when
        many changes to PD, ELDV and CP ready bits are done during mode set.
        \******************************************************************************************************************/
        SIZE32BITS CpReadyd : BITFIELD_BIT(13); // CP_READYD

        /******************************************************************************************************************
        This bit directs audio to the device connected to this transcoder. When enabled along with Inactive set to 0 and audio data is available, the audio data will be combined
        with the video data and sent over this transcoder. The audio unit uses the status of this bit to indicate presence of the HDMI/DP output to the audio driver.
        \******************************************************************************************************************/
        SIZE32BITS AudioOutputEnabled : BITFIELD_BIT(14); // AUDIO_OUTPUT_ENABLED

        /******************************************************************************************************************
        Inactive: When this bit is set, a digital display sink device has been attached but not active for streaming audio.
        \******************************************************************************************************************/
        SIZE32BITS AudioInactived : BITFIELD_BIT(15); // AUDIO_INACTIVED

        /******************************************************************************************************************/
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(16, 31); //
    };

    SIZE32BITS Value;

} AUD_PIN_ELD_CP_VLD;

typedef union _AUD_DIG_CNVT {
    struct
    {
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(0);
        SIZE32BITS V : BITFIELD_BIT(1);
        SIZE32BITS VCFG : BITFIELD_BIT(2);
        SIZE32BITS PRE : BITFIELD_BIT(3);
        SIZE32BITS COPY : BITFIELD_BIT(4);
        SIZE32BITS NonPCM : BITFIELD_BIT(5);
        SIZE32BITS PRO : BITFIELD_BIT(6);
        SIZE32BITS Level : BITFIELD_BIT(7);
        SIZE32BITS CC : BITFIELD_RANGE(8, 14);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(15);
        SIZE32BITS ChannelIndex : BITFIELD_RANGE(16, 19);
        SIZE32BITS StreamId : BITFIELD_RANGE(20, 23);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31);
    };
    SIZE32BITS ulValue;
} AUD_DIG_CNVT;

typedef enum
{
    BITS_PER_SAMPLE_16 = 1,
    BITS_PER_SAMPLE_20 = 2,
    BITS_PER_SAMPLE_24 = 3,
    BITS_PER_SAMPLE_32 = 4,
} BITS_PER_SAMPLE;

typedef union _AUD_STR_DESC {
    struct
    {
        SIZE32BITS NumChannels : BITFIELD_RANGE(0, 3);
        SIZE32BITS BitsPerSample : BITFIELD_RANGE(4, 6);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(7);
        SIZE32BITS SamplingRateDivisor : BITFIELD_RANGE(8, 10);
        SIZE32BITS SamplingRateMultiplier : BITFIELD_RANGE(11, 13);
        SIZE32BITS BaseSamplingRate : BITFIELD_BIT(14);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(15);
        SIZE32BITS ChannelCount : BITFIELD_RANGE(16, 20);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(21, 31);
    };
    SIZE32BITS ulValue;
} AUD_STR_DESC;

// ravi......
// mmio: 650D4

typedef union _AUD_HDMI_FIFO_STATUS {
    struct
    {
        SIZE32BITS Conv4Overrun : BITFIELD_BIT(0);          //
        SIZE32BITS Conv4Underrun : BITFIELD_BIT(1);         //
        SIZE32BITS Reserved : BITFIELD_RANGE(2, 23);        //
        SIZE32BITS FunctionReset : BITFIELD_BIT(24);        //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(25); //
        SIZE32BITS Conv1Overrun : BITFIELD_BIT(26);         //
        SIZE32BITS Conv1Underrun : BITFIELD_BIT(27);        //
        SIZE32BITS Conv2Overrun : BITFIELD_BIT(28);         //
        SIZE32BITS Conv2Underrun : BITFIELD_BIT(29);        //
        SIZE32BITS Conv3Overrun : BITFIELD_BIT(30);         //
        SIZE32BITS Conv3Underrun : BITFIELD_BIT(31);        //
    };
    SIZE32BITS ulValue;
} AUD_HDMI_FIFO_STATUS;

// mmio: 65F20
typedef union _AUD_DP_FIFO_STATUS {
    struct
    {
        SIZE32BITS AudfaDpFifoFull : BITFIELD_BIT(0);     //
        SIZE32BITS AudfaDpFifoEmpty : BITFIELD_BIT(1);    //
        SIZE32BITS AudfaDpFifoOverrun : BITFIELD_BIT(2);  //
        SIZE32BITS AudfaDipFifofull : BITFIELD_BIT(3);    //
        SIZE32BITS AudfaDpFifoEmptycd : BITFIELD_BIT(4);  //
        SIZE32BITS PipeaAudioOverflow : BITFIELD_BIT(5);  //
        SIZE32BITS AudfbDpFifoFull : BITFIELD_BIT(6);     //
        SIZE32BITS AudfbDpFifoEmpty : BITFIELD_BIT(7);    //
        SIZE32BITS AudfbDpFifoOverrun : BITFIELD_BIT(8);  //
        SIZE32BITS AudfbDipFifoFull : BITFIELD_BIT(9);    //
        SIZE32BITS AudfbDpFifoEmptycd : BITFIELD_BIT(10); //
        SIZE32BITS PipebAudioOverFlow : BITFIELD_BIT(11); //
        SIZE32BITS AdfcDpFifoFull : BITFIELD_BIT(12);     //
        SIZE32BITS AudfcDpFifoEmpty : BITFIELD_BIT(13);   //
        SIZE32BITS AudfcDpFifoOverrun : BITFIELD_BIT(14); //
        SIZE32BITS AudfcDipFifoFull : BITFIELD_BIT(15);   //
        SIZE32BITS AudfcDpFifoEmptycd : BITFIELD_BIT(16); //
        SIZE32BITS PipecAudioOverFlow : BITFIELD_BIT(17); //
        SIZE32BITS AudfdDpFifoFull : BITFIELD_BIT(18);    //
        SIZE32BITS AudfdDpFifoEmpty : BITFIELD_BIT(19);   //
        SIZE32BITS AudfdDpFifoOverrun : BITFIELD_BIT(20); //
        SIZE32BITS AudfdDipFifoFull : BITFIELD_BIT(21);   //
        SIZE32BITS AudfdDpFifoEmptycd : BITFIELD_BIT(22); //
        SIZE32BITS PipedAudioOverFlow : BITFIELD_BIT(23);  //
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31);
    };
    SIZE32BITS ulValue;
} AUD_DP_DIP_STATUS;

typedef union _AUD_OUT_CHAN_MAP {
    struct
    {
        SIZE32BITS DigDispAudIndexPipeA : BITFIELD_RANGE(0, 3);
        SIZE32BITS ConverterChannelMAPPipeA : BITFIELD_RANGE(4, 7);
        SIZE32BITS DigDispAudIndexPipeB : BITFIELD_RANGE(8, 11);
        SIZE32BITS ConverterChannelMAPPipeB : BITFIELD_RANGE(12, 15);
        SIZE32BITS DigDispAudIndexPipeC : BITFIELD_RANGE(16, 19);
        SIZE32BITS ConverterChannelMAPPipeC : BITFIELD_RANGE(20, 23);
        SIZE32BITS DigDispAudIndexPipeD : BITFIELD_RANGE(24, 27);
        SIZE32BITS ConverterChannelMAPPipeD : BITFIELD_RANGE(28, 31);
    };
    SIZE32BITS ulValue;
} AUD_OUT_CHAN_MAP;

// AUD_C1_MISC_CTRL
// 65010h to 65310h

typedef union _AUD_MISC_CTRL {
    struct
    {
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_BIT(0);
        SIZE32BITS ProAllowed : BITFIELD_BIT(1);
        SIZE32BITS SampleFabricationEN : BITFIELD_BIT(2);
        SIZE32BITS OutputDelay : BITFIELD_RANGE(4, 7);
        SIZE32BITS SamplePresentDisable : BITFIELD_BIT(8);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(9, 31);
    };
    SIZE32BITS ulValue;
} AUD_MISC_CTRL;

//_AUD_PIPE_CONV_CFG - 6507C

typedef union _AUD_PIPE_CONV_CFG {
    struct
    {
        SIZE32BITS ConverterADigen : BITFIELD_BIT(0);
        SIZE32BITS ConverterBDigen : BITFIELD_BIT(1);
        SIZE32BITS ConverterCDigen : BITFIELD_BIT(2);
        SIZE32BITS ConverterDDigen : BITFIELD_BIT(3);
        SIZE32BITS Convertor1StreamID : BITFIELD_RANGE(4, 7);
        SIZE32BITS Convertor2StreamID : BITFIELD_RANGE(8, 11);
        SIZE32BITS Convertor3StreamID : BITFIELD_RANGE(12, 15);
        SIZE32BITS OutEnablePortB : BITFIELD_BIT(16);
        SIZE32BITS OutEnablePortC : BITFIELD_BIT(17);
        SIZE32BITS OutEnablePortD : BITFIELD_BIT(18);
        SIZE32BITS OutEnablePortF : BITFIELD_BIT(19);
        SIZE32BITS AmpMuteStatusPortB : BITFIELD_BIT(20);
        SIZE32BITS AmpMuteStatusPortC : BITFIELD_BIT(21);
        SIZE32BITS AmpMuteStatusPortD : BITFIELD_BIT(22);
        SIZE32BITS AmpMuteStatusPortF : BITFIELD_BIT(23);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 27);
        SIZE32BITS Convertor4StreamID : BITFIELD_RANGE(28, 31);
    };
    SIZE32BITS ulValue;
} AUD_PIPE_CONV_CFG;

// AUD_TCA_CONFIG

typedef union _AUD_TCA_CONFIG {
    struct
    {
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(0, 2);
        SIZE32BITS DisableNCTS : BITFIELD_BIT(3);
        SIZE32BITS LowerNValue : BITFIELD_RANGE(4, 15);
        SIZE32BITS PixelClockHDMI : BITFIELD_RANGE(16, 19);
        SIZE32BITS UpperNValue : BITFIELD_RANGE(20, 27);
        SIZE32BITS NProgrammingEnable : BITFIELD_BIT(28);
        SIZE32BITS NValueIndex : BITFIELD_BIT(29);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(30, 31);
    };
    SIZE32BITS ulValue;
} AUD_CONFIG;

// AUD_TCA_CONFIG 2

typedef union _AUD_TCA_CONFIG2 {
    struct
    {
        SIZE32BITS UpperBitsMCTSValue : BITFIELD_RANGE(0, 3);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(4, 7);
        SIZE32BITS UpperBitsNValue : BITFIELD_RANGE(8, 11);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(12, 15);
        SIZE32BITS DPSpecVersion : BITFIELD_RANGE(16, 20);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(21, 30);
        SIZE32BITS DisableHBlankOverFlowFix : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;
} AUD_CONFIG2;

// 65F44h/65F54h/65F64h/65F74h

typedef union _AUD_M_CTS {
    struct
    {
        SIZE32BITS AudioCTSValues : BITFIELD_RANGE(0, 23);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(24, 31);
    };
    SIZE32BITS ulValue;
} AUD_M_CTS;

typedef union _AUD_M_CTS_ENABLE {
    struct
    {
        SIZE32BITS CTSProgramming : BITFIELD_RANGE(0, 19);
        SIZE32BITS EnableCTSORM : BITFIELD_BIT(20);
        SIZE32BITS CTSMValueIndex : BITFIELD_BIT(21);
        SIZE32BITS UNIQUENAME(Reserved) : BITFIELD_RANGE(22, 31);
    };
    SIZE32BITS ulValue;
} AUD_M_CTS_ENABLE;

typedef union _AUD_CONFIG_BE {
    struct
    {
        SIZE32BITS NumberofSamplesPerLinePipeA : BITFIELD_RANGE(0, 1);
        SIZE32BITS DPMixerMainStreamPpriorityEnablePipeA : BITFIELD_BIT(2);
        SIZE32BITS HBlankStartCountPipeA : BITFIELD_RANGE(3, 5);
        SIZE32BITS NumberofSamplesPerLinePipeB : BITFIELD_RANGE(6, 7);
        SIZE32BITS DPMixerMainstreamPriorityEnablePipeB : BITFIELD_BIT(8);
        SIZE32BITS HBlankStartCountPipeB : BITFIELD_RANGE(9, 11);
        SIZE32BITS NumberofSamplesPerLinePipeC : BITFIELD_RANGE(12, 13);
        SIZE32BITS DPMixerMainstreamPriorityEnablePipeC : BITFIELD_BIT(14);
        SIZE32BITS HBlankStartCountPipeC : BITFIELD_RANGE(15, 17);
        SIZE32BITS NumberofSamplesPerLinePipeD : BITFIELD_RANGE(18, 19);
        SIZE32BITS DPMixerMainstreamPriorityEnablePipeD : BITFIELD_BIT(20);
        SIZE32BITS HBlankStartCountPipeD : BITFIELD_RANGE(21, 23);
        SIZE32BITS HBlankEarlyEnablePipeA : BITFIELD_BIT(24);
        SIZE32BITS HBlankEarlyEnablePipeB : BITFIELD_BIT(25);
        SIZE32BITS HBlankEarlyEnablePipeC : BITFIELD_BIT(26);
        SIZE32BITS HBlankEnablePipeD : BITFIELD_BIT(27);
        SIZE32BITS DelaySampleCountLatchPipeA : BITFIELD_BIT(28);
        SIZE32BITS DelaySampleCountLatchPipeB : BITFIELD_BIT(29);
        SIZE32BITS DelaySampleCountLatchPipeC : BITFIELD_BIT(30);
        SIZE32BITS DelaysampleCountLatchPipeD : BITFIELD_BIT(31);
    };
    SIZE32BITS ulValue;
} AUD_CONFIG_BE;