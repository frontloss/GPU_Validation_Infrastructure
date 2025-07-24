namespace Intel.VPG.Display.Automation
{
    using System;
    using System.Text;
    using System.Collections.Generic;

    public enum INFOFRAME_TYPE
    {
        Unsupported = -1,
        Vendor_INFO_FRAME = 0X81,
        AVI_INFO_FRAME = 0x82,
        SPD_INFO_FRAME = 3,
        AUDIO_INFO_FRAME = 0x84,
        MPEG_SOURCE_INFO_FRAME = 5,
    }
    public class Resolutions
    {
        private int _x, _y, _colorDepth;
        private double _refreshRate;
        private bool _isInterlaced;

        private double _pixelFrequency;
        private int _Hactive, _Hblank, _Hfront, _Hsync, _Hback;

        private double _vFreq, _Vfront, _Vback;
        private int _Vactive, _Vblank, _Vsync;

        public int X
        {
            get
            {
                return _x;
            }
            set
            {
                _x = value;
            }
        }
        public int Y
        {
            get
            {
                return _y;
            }
            set
            {
                _y = value;
            }
        }
        public double RefreshRate
        {
            get { return _refreshRate; }
            set { _refreshRate = value; }
        }
        public int ColorDepth
        {
            get { return _colorDepth; }
            set { _colorDepth = value; }
        }
        public bool IsInterlaced
        {
            get { return _isInterlaced; }
            set { _isInterlaced = value; }
        }
        public double PixelFrequency
        {
            get { return _pixelFrequency; }
            set { _pixelFrequency = value; }
        }
        public int Hactive
        {
            get { return _Hactive; }
            set { _Hactive = value; }
        }
        public int Hblank
        {
            get { return _Hblank; }
            set { _Hblank = value; }
        }
        public int Hfront
        {
            get { return _Hfront; }
            set { _Hfront = value; }
        }
        public int Hsync
        {
            get { return _Hsync; }
            set { _Hsync = value; }
        }
        public int Hback
        {
            get { return _Hback; }
            set { _Hback = value; }
        }
        public double VFreq
        {
            get { return _vFreq; }
            set { _vFreq = value; }
        }

        public int Vactive
        {
            get { return _Vactive; }
            set { _Vactive = value; }
        }
        public int Vblank
        {
            get { return _Vblank; }
            set { _Vblank = value; }
        }
        public double Vfront
        {
            get { return _Vfront; }
            set { _Vfront = value; }
        }
        public int Vsync
        {
            get { return _Vsync; }
            set { _Vsync = value; }
        }

        public double Vback
        {
            get { return _Vback; }
            set { _Vback = value; }
        }
        public Resolutions(int x, int y, int refreshRate, bool isInterlaced)
        {
            _x = x;
            _y = y;
            _refreshRate = refreshRate;
            _isInterlaced = isInterlaced;
        }
        public Resolutions(int x, int y, double refreshRate, bool isInterlaced, double pixelFrequency, int Hactive, int Hblank, int Hfront, int Hsync, int Hback, double vFreq, int Vactive, int Vblank, double Vfront, int Vsync, double Vback)
        {
            _x = x;
            _y = y;
            _refreshRate = refreshRate;
            _isInterlaced = isInterlaced;
            _pixelFrequency = pixelFrequency;
            _Hactive = Hactive;
            _Hblank = Hblank;
            _Hfront = Hfront;
            _Hsync = Hsync;
            _Hback = Hback;
            _vFreq = vFreq;
            _Vactive = Vactive;
            _Vblank = Vblank;
            _Vfront = Vfront;
            _Vsync = Vsync;
            _Vback = Vback;
        }
    }
    
    public class InfoFrameParsing : FunctionalBase, IParse, IGetMethod
    {
        private enum HDMI_COLOR_FORMAT
        {
            Unsupported = -1,
            RGB,
            YCBCR_4_2_2,
            YCBCR_4_4_4,
            RESERVED
        }
        private enum ACTIVE_FORMAT_INFO
        {
            Unsupported = -1,
            NO_DATA,
            VALID_DATA
        }
        private enum BAR_INFO
        {
            Unsupported = -1,
            BAR_INFO_NOT_VALID,
            VERTICAL_BAR_INFO_VALID,
            HORIZONTAL_BAR_INFO_VALID,
            VERTICAL_HORIZONTAL_BAR_INFO_VALID
        }
        private enum SCAN_INFO
        {
            Unsupported = -1,
            NO_DATA,
            OVERSCANNED,
            UNDERSCANNED,
            RESERVED
        }
        private enum COLORIMETRY
        {
            Unsupported = -1,
            NO_DATA,
            SMPTE_170M_ITU601,
            ITU709,
            EXT_Colorimetry_Valid
        }
        private enum PICTURE_ASPECT_RATIO
        {
            Unsupported = -1,
            NO_DATA,
            ASPECT_RATIO_4_3,
            ASPECT_RATIO_16_9,
            RESERVED
        }
        private enum ACTIVE_FORMAT_ASPECT_RATIO
        {
            Unsupported = -1,
            PICTURE_ASPECT_RATIO = 8,
            CENTER_4_3,
            CENTER_16_9,
            CENTER_14_9,
            RESERVED
        }
        private enum NON_UNIFORM_PICTURE_SCALING
        {
            Unsupported = -1,
            NO_KNOWN_NON_UNIFORM_SCALING,
            PICTURE_SCALED_HORIZONTALLY,
            PICTURE_SCALED_VERTICALLY,
            PICTURE_SCALED_HORIZONTAL_VERTICAL,
        }
        private enum PIXEL_REPITION
        {
            No_Repetition,
            pixel_sent_2_times,
            pixel_sent_3_times,
            pixel_sent_4_times,
            pixel_sent_5_times,
            pixel_sent_6_times,
            pixel_sent_7_times,
            pixel_sent_8_times,
            pixel_sent_9_times,
            pixel_sent_10_times,
            RESERVED
        }
        private enum EXTENDED_COLORIMETRY
        {
            Unsupported = -1,
            xvYCC_601,
            xvYCC_709,
            sYCC_601,
            AdobeYCC_601,
            Adobe_RGB,
            RESERVED
        }
     
        private enum IT_CONTENT
        {
            Unsupported = -1,
            NO_DATA,
            IT_Content,
        }
        private enum YCC_QUANTIZATION_RANGE
        {
            Unsupported = -1,
            Limited_Range,
            Full_Range,
            RESERVED
        }
        private enum IT_CONTENT_TYPE
        {
            Unsupported = -1,
            NO_DATA,
            PHOTO,
            CINEMA,
            GAME,
            GRAPHICS,
            PHOTO_IT_CONTENT,
            CINEMA_IT_CONTENT,
            GAME_IT_CONTENT
        }
        private enum AUDIO_CODING_TYPE
        {
            Unsupported = -1,
            Refer_To_Stream_Header,
            IEC60958_PCM_30_31,
            AC_3,
            MPEG1_Layer_1_2,
            MP3_MPEG1_Layer_3,
            MPEG2_Multichannel,
            AAC,
            DTS_ATRAC,
            One_Bit_Audio,
            Dolby_Digital_Plus,
            DTS_HD,
            MAT_MLP,
            DST,
            WMA_Pro,
            Reserved
        }
        private enum AUDIO_CHANNEL_COUNT
        {
            Unsupported = -1,
            Refer_To_Stream_Header,
            Two_Channel,
            Three_Channel,
            Four_Channel,
            Five_Channel,
            Six_Channel,
            Seven_Channel,
            Eight_Channel
        }
        private enum SAMPLING_FREQUENCY
        {
            Unsupported = -1,
            Refer_To_Stream_Header,
            SF_32kHz,
            SF_44_1kHz_CD,
            SF_48kHz,
            SF_82_2kHz,
            SF_96kHz,
            SF_176_4kHz,
            SF_192kHz
        }
        private enum SAMPLE_SIZE
        {
            Unsupported = -1,
            Refer_To_Stream_Header,
            SS_16Bit,
            SS_20Bit,
            SS_24Bit
        }
        private enum DOWN_MIX_INHIBIT
        {
            Unsupported = -1,
            Permitted_or_no_information_about_any_assertion_of_this,
            Prohibited
        }
        private enum LEVEL_SHIFT_VALUE
        {
            LSV_0dB,
            LSV_1dB,
            LSV_2dB,
            LSV_3dB,
            LSV_4dB,
            LSV_5dB,
            LSV_6dB,
            LSV_7dB,
            LSV_8dB,
            LSV_9dB,
            LSV_10dB,
            LSV_11dB,
            LSV_12dB,
            LSV_13dB,
            LSV_14dB,
            LSV_15dB
        }
        private enum LFE_PLAYBACK_LEVEL_INFO
        {
            No_Information,
            LFE_0dB_Playback,
            LFE_Plus_10dB_Playback,
            Reserved
        }
        public enum SPEAKER_PLACEMENT
        {
            Unsupported,
            Front_Left,
            Front_Center,
            Front_Right,
            Front_Left_Center,
            Front_Right_Center,
            Rear_Left,
            Rear_Center,
            Rear_Right,
            Rear_Left_Center,
            Rear_Right_Center,
            Low_Frequency_Effect,
            Reserved
        }
        private enum HDMI_VIDEO_FORMAT
        {
            Unsupported = -1,
            No_Additional_HDMI_Format_Present,
            Extended_Resolution_Format,
            Three_3D_Format,
            RESERVED
        }
        private enum THREE_3D_STRUCTURE
        {
            Unsupported = -1,
            Frame_Packing = 0,
            Top_And_Bottom = 6,
            Side_By_Side = 8,
            RESERVED_Upto_0111,
            RESERVED_From_1001
        }
        private enum THREE_3D_EXTENDED_DATA
        {
            Unsupported = -1,
            No_Data = 0,
            Vendor_Specific_Infoframe,
            Additional_3D_Data,
            RESERVED
        }
        private enum SOURCE_DEVICE_INFORMATION
        {
            Unsupported = -1,
            Unknown,
            Digital_STB,
            DVD_player,
            D_VHS,
            HDD_Videorecorder,
            DVC,
            DSC,
            Video_CD,
            Game,
            PC_general,
            Blu_Ray_Disc_BD,
            Super_Audio_CD,
            Reserved
        }
        private enum GBD_PROFILE
        {
            UnSupported = -1,
            P0,
            P1,
            P2,
            P3,
            Reserved
        }
        private enum PACKET_SEQUENCE
        {
            UnSupported = -1,
            Intermediate_Packet_In_Sequence,
            First_Packet_In_Sequence,
            Last_Packet_In_Sequence,
            Only_Packet_In_Sequence_P0
        }
        private enum FORMAT_FLAG
        {
            Vertices_or_Facets,
            Range
        }
        private enum FACET_MODE
        {
            Facets_Included,
            Reserved
        }
        private enum GBD_COLOR_PRECISION
        {
            GBD_Color_8bit,
            GBD_Color_10bit,
            GBD_Color_12bit,
            Reserved
        }
        private enum GBD_COLOR_SPACE
        {
            RGB,
            xvYCC601,
            xvYCC709,
            XYZ,
            RESERVED,
            RGB_Expression_Of_xvYCC601,
            RGB_Expression_Of_xvYCC709
        }
        private enum COLOR_DEPTH
        {
            UnSupported = -1,
            ColorDepth_Not_Indicated,
            ColorDepth_24Bits_Per_Pixel = 4,
            ColorDepth_30Bits_Per_Pixel = 5,
            ColorDepth_36Bits_Per_Pixel = 6,
            ColorDepth_48Bits_Per_Pixel = 7,
            Reserved
        }
        private enum PIXEL_PACKING_PHASE
        {
            UnSupported = -1,
            Phase4_10P4,
            Phase1_10P1_12P1_16P1,
            Phase2_10P2_12P2,
            Phase3_10P3,
            Reserved
        }
        private enum DEEPCOLORBPC
        {
            UnSupported = -1,
            DeepColor_8_BPC,
            DeepColor_10_BPC,
            DeepColor_12_BPC,
            DeepColor_16_BPC
        }

        private const byte HDMI_MAP = 0x68;
        private byte[] aviInfoData;
        private INFOFRAME_TYPE infoFrameType = INFOFRAME_TYPE.Unsupported;
        private int version, length, checkSum;
        private HDMI_COLOR_FORMAT hdmiColorFormat;
        private ACTIVE_FORMAT_INFO activeFormatInfo;
        private BAR_INFO barInfo;
        private SCAN_INFO scanInfo;
        private COLORIMETRY colorimetry;
        private PICTURE_ASPECT_RATIO pictureAspectRatio;
        private ACTIVE_FORMAT_ASPECT_RATIO activeFormatAspectRatio;
        private NON_UNIFORM_PICTURE_SCALING nonUniformPictureScaling;
        private PIXEL_REPITION pixelRepetition;
        private EXTENDED_COLORIMETRY extendedColorimetry;
        private RGB_QUANTIZATION_RANGE rgbQuantizationRange;
        private IT_CONTENT itContent;
        private YCC_QUANTIZATION_RANGE yccQuantizationRange;
        private IT_CONTENT_TYPE itContentType;
        private uint lineNumberOfEndOfTopBar, lineNumberOfStartOfBottomBar, pixelNumberOfEndOfLeftBar, pixelNumberOfStartOfRightBar;

        private byte[] audioInfoData;
        private AUDIO_CODING_TYPE audioCodingType;
        private AUDIO_CHANNEL_COUNT audioChannelCount;
        private SAMPLING_FREQUENCY samplingFrequency;
        private SAMPLE_SIZE sampleSize;
        private DOWN_MIX_INHIBIT downMixInhibit;
        private LEVEL_SHIFT_VALUE levelShiftValue;
        private LFE_PLAYBACK_LEVEL_INFO lfePlaybackLevelInfo;
        private SPEAKER_PLACEMENT[] speakerPlacement;

        private byte[] vendorInfoData;
        private uint registrationIdentifier;
        private HDMI_VIDEO_FORMAT hdmiVideoFormat;
        public List<Resolutions> hdmiVicResolutionList;
        public List<Resolutions> three3DTransmissionVideoFormatsResolList;
        private THREE_3D_STRUCTURE threeDStructure;
        private THREE_3D_EXTENDED_DATA three3DExtendedData;

        private byte[] spdInfoData;
        public string vendorName;
        public string productDescription;
        private SOURCE_DEVICE_INFORMATION sourceDeviceInformation;


        private byte[] gmPacketData;
        private int packetTypeCode, nextField, noCurrentGBD, affectedGamutSeqNum, currentGamutSeqNum, gbdLength, gbdChecksum, numberVertices, numberFacets, vSize, minRedData, maxRedData, minGreenData, maxGreenData, minBlueData, maxBlueData;
        private GBD_PROFILE gbdprofile;
        private PACKET_SEQUENCE packetSequence;
        private byte[] gbdData;
        private FORMAT_FLAG formatFlag;
        private FACET_MODE facetMode;
        private GBD_COLOR_PRECISION gbdColorPrecision;
        private GBD_COLOR_SPACE gbdColorSpace;


        private byte[] gcpPacketData;

        private void helpText()
        {
            StringBuilder sb = new StringBuilder();
            sb.Append("..\\>Execute InfoFrameParsing GET frameType functionInrame port]").Append(Environment.NewLine);
            sb.Append("frameType AVI|AUDIO|VENDOR|SPD|GMP|GCP").Append(Environment.NewLine);
            sb.Append("AVI =>  FillHeaderData_Avi|ComputePixelRepetition|ComputeHDMIColorFormat|ComputeExtendedColorimetry|ComputeActiveFormat_Info|ComputeLinePixelBarData|All_Avi|ComputeITContentType|ComputeYCCQuantizationRange|ComputeITContent|ComputeRGBQuantizationRange|ComputeBarInfo|ComputeScanInfo|ComputeColorimetry|ComputePictureAspectRatio|ComputeActiveFormatAspectRatio|ComputeNonUniformPictureScaling").Append(Environment.NewLine);
            sb.Append("AUDIO =>  FillHeaderData_Audio|ComputeAudioCodingType|ComputeAudioChannelCount|ComputeSamplingFrequency|ComputeSampleSize|ComputeDownMixInhibit|ComputeLevelShiftValue|ComputeLFE_PlaybackLevelInfo|All_Audio").Append(Environment.NewLine);
            sb.Append("VENDOR =>  FillHeaderData_Vendor|ComputeRegistrationIdentifier|ComputeHdmiVideoFormat|Compute3DStructure|Compute3DExtendedData|All_Vendor|Compute3DTransmissionVideoFormatsResolList|ComputeHdmiVicResolutionList").Append(Environment.NewLine);
            sb.Append("SPD =>  FillHeaderData_Spd|ComputeVendorName|ComputeProductDescription|ComputeSourceDeviceInformation|All_Spd").Append(Environment.NewLine);
            sb.Append("GMP =>  FillHeaderData_GMP|ComputeGMPBodyPacket|ComputeGBDBodyPacket|AllGMP").Append(Environment.NewLine);
            sb.Append("GCP =>  GetDeepColor|GetAVMUTE|AllGCP").Append(Environment.NewLine);
            Log.Message(sb.ToString());
        }
        public void Parse(string[] args)
        {
            InfoFrame objInfoframe = new InfoFrame();
            string setOrGet = args[0].ToUpper();
            int checkFrameType = 0, checkFunctionName = 0, checkPort = 0;

            if (args.Length.Equals(4) && setOrGet.Equals("GET"))
            {
                Log.Message("Get Call");
                string frameType = args[1].ToUpper();
                string functionCalled = args[2].ToUpper();
                string port = args[3].ToUpper();
                foreach (var value in Enum.GetValues(typeof(InfoFrameType)))
                {
                    if (String.Equals(value.ToString(), frameType, StringComparison.OrdinalIgnoreCase))
                    {
                        checkFrameType = 1;
                        objInfoframe.infoFrameType = (InfoFrameType)value;
                    }
                }
                if (checkFrameType == 0)
                    throw new Exception("Entered frameType is wrong....enter avi/audio/vendor/gcp/gmp/spd");

                foreach (var value in Enum.GetValues(typeof(FunctionInfoFrame)))
                {
                    if (String.Equals(value.ToString(), functionCalled, StringComparison.OrdinalIgnoreCase))
                    {
                        checkFunctionName = 1;
                        objInfoframe.functionInfoFrame = (FunctionInfoFrame)value;
                    }
                }
                if (checkFunctionName == 0)
                    throw new Exception("Enterned functionName is wrong....refer to help");

                foreach (var value in Enum.GetValues(typeof(PORT)))
                {
                    if (String.Equals(value.ToString(), port, StringComparison.OrdinalIgnoreCase))
                    {
                        checkPort = 1;
                        objInfoframe.port = (DVMU_PORT)value;
                    }
                }
                if (checkPort == 0)
                    throw new Exception("Enterned port is wrong....enter porta or portb");

                InfoFrame abc = (InfoFrame)this.GetMethod(objInfoframe);
            }
            else if ((args.Length > 0 && (args[0].Contains("?") || args[0].ToLower().Contains("help"))))
                this.helpText();
        }
        public object GetMethod(object argMessage)
        {
            Log.Message("Inside GetMethod function");
            List<string> abc = new List<string>();
            InfoFrame infoframeObject = argMessage as InfoFrame;
            List<string> returnInfoframeData = new List<string>();

            Log.Message("Creating dictionary for the infoframe type and functions in infoframe");
            Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> dictionary = new Dictionary<FunctionInfoFrame, Func<byte[], List<string>>>();
            dictionary.Add(FunctionInfoFrame.FillHeaderDataAvi, (byte[] x) => FillHeaderDataAvi(x));
            dictionary.Add(FunctionInfoFrame.ComputeHDMIColorFormat, (byte[] x) => ComputeHDMIColorFormat(x));
            dictionary.Add(FunctionInfoFrame.ComputeActiveFormatInfo, (byte[] x) => ComputeActiveFormatInfo(x));
            dictionary.Add(FunctionInfoFrame.ComputeBarInfo, (byte[] x) => ComputeBarInfo(x));
            dictionary.Add(FunctionInfoFrame.ComputeScanInfo, (byte[] x) => ComputeScanInfo(x));
            dictionary.Add(FunctionInfoFrame.ComputeColorimetry, (byte[] x) => ComputeColorimetry(x));
            dictionary.Add(FunctionInfoFrame.ComputePictureAspectRatio, (byte[] x) => ComputePictureAspectRatio(x));
            dictionary.Add(FunctionInfoFrame.ComputeActiveFormatAspectRatio, (byte[] x) => ComputeActiveFormatAspectRatio(x));
            dictionary.Add(FunctionInfoFrame.ComputeNonUniformPictureScaling, (byte[] x) => ComputeNonUniformPictureScaling(x));
            dictionary.Add(FunctionInfoFrame.ComputePixelRepetition, (byte[] x) => ComputePixelRepition(x));
            dictionary.Add(FunctionInfoFrame.ComputeExtendedColorimetry, (byte[] x) => ComputeExtendedColorimetry(x));
            dictionary.Add(FunctionInfoFrame.ComputeLinePixelBarData, (byte[] x) => ComputeLinePixelBarData(x));
            dictionary.Add(FunctionInfoFrame.ComputeRGBQuantizationRange, (byte[] x) => ComputeRGBQuantizationRange(x));
            dictionary.Add(FunctionInfoFrame.ComputeITContent, (byte[] x) => ComputeITContent(x));
            dictionary.Add(FunctionInfoFrame.ComputeYCCQuantizationRange, (byte[] x) => ComputeYCCQuantizationRange(x));
            dictionary.Add(FunctionInfoFrame.ComputeITContentType, (byte[] x) => ComputeITContentType(x));
            dictionary.Add(FunctionInfoFrame.AllAvi, (byte[] x) => AllAvi(x));
            dictionary.Add(FunctionInfoFrame.FillHeaderDataAudio, (byte[] x) => FillHeaderDataAudio(x));
            dictionary.Add(FunctionInfoFrame.ComputeAudioCodingType, (byte[] x) => ComputeAudioCodingType(x));
            dictionary.Add(FunctionInfoFrame.ComputeAudioChannelCount, (byte[] x) => ComputeAudioChannelCount(x));
            dictionary.Add(FunctionInfoFrame.ComputeSamplingFrequency, (byte[] x) => ComputeSamplingFrequency(x));
            dictionary.Add(FunctionInfoFrame.ComputeSampleSize, (byte[] x) => ComputeSampleSize(x));
            dictionary.Add(FunctionInfoFrame.ComputeDownMixInhibit, (byte[] x) => ComputeDownMixInhibit(x));
            dictionary.Add(FunctionInfoFrame.ComputeLevelShiftValue, (byte[] x) => ComputeLevelShiftValue(x));
            dictionary.Add(FunctionInfoFrame.ComputeLFEPlaybackLevelInfo, (byte[] x) => ComputeLFEPlaybackLevelInfo(x));
            dictionary.Add(FunctionInfoFrame.SpeakerPlacement, (byte[] x) => SpeakerPlacement(x));
            dictionary.Add(FunctionInfoFrame.AllAudio, (byte[] x) => AllAudio(x));
            dictionary.Add(FunctionInfoFrame.FillHeaderDataVendor, (byte[] x) => FillHeaderDataVendor(x));
            dictionary.Add(FunctionInfoFrame.ComputeRegistrationIdentifier, (byte[] x) => ComputeRegistrationIdentifier(x));
            dictionary.Add(FunctionInfoFrame.ComputeHdmiVideoFormat, (byte[] x) => ComputeHdmiVideoFormat(x));
            dictionary.Add(FunctionInfoFrame.Compute3DStructure, (byte[] x) => Compute3DStructure(x));
            dictionary.Add(FunctionInfoFrame.Compute3DExtendedData, (byte[] x) => Compute3DExtendedData(x));
            dictionary.Add(FunctionInfoFrame.Compute3DTransmissionVideoFormatsResolList, (byte[] x) => Compute3DTransmissionVideoFormatsResolList(x));
            dictionary.Add(FunctionInfoFrame.ComputeHdmiVicResolutionList, (byte[] x) => ComputeHdmiVicResolutionList(x));
            dictionary.Add(FunctionInfoFrame.AllVendor, (byte[] x) => AllVendor(x));
            dictionary.Add(FunctionInfoFrame.FillHeaderDataSpd, (byte[] x) => FillHeaderDataSpd(x));
            dictionary.Add(FunctionInfoFrame.ComputeVendorName, (byte[] x) => ComputeVendorName(x));
            dictionary.Add(FunctionInfoFrame.ComputeProductDescription, (byte[] x) => ComputeProductDescription(x));
            dictionary.Add(FunctionInfoFrame.ComputeSourceDeviceInformation, (byte[] x) => ComputeSourceDeviceInformation(x));
            dictionary.Add(FunctionInfoFrame.AllSpd, (byte[] x) => AllSpd(x));
            dictionary.Add(FunctionInfoFrame.FillHeaderDataGMP, (byte[] x) => FillHeaderDataGMP(x));
            dictionary.Add(FunctionInfoFrame.ComputeGMPBodyPacket, (byte[] x) => ComputeGMPBodyPacket(x));
            dictionary.Add(FunctionInfoFrame.ComputeGBDBodyPacket, (byte[] x) => ComputeGBDBodyPacket(x));
            dictionary.Add(FunctionInfoFrame.AllGMP, (byte[] x) => AllGMP(x));
            dictionary.Add(FunctionInfoFrame.GetDeepColor, (byte[] x) => GetDeepColor(x));
            dictionary.Add(FunctionInfoFrame.GetAVMUTE, (byte[] x) => GetAVMUTE(x));
            dictionary.Add(FunctionInfoFrame.AllGCP, (byte[] x) => AllGCP(x));

            if (infoframeObject.infoFrameType == InfoFrameType.AVI)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetAviInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            else if (infoframeObject.infoFrameType == InfoFrameType.AUDIO)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetAudioInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            else if (infoframeObject.infoFrameType == InfoFrameType.VENDOR)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetVendorInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            else if (infoframeObject.infoFrameType == InfoFrameType.SPD)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetSPDInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            else if (infoframeObject.infoFrameType == InfoFrameType.GMP)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetGMPInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            else if (infoframeObject.infoFrameType == InfoFrameType.GCP)
            {
                Log.Message("InfoFrame Type = {0}", infoframeObject.infoFrameType);
                infoframeObject.infoFrameData = GetGCPInfoData(infoframeObject.functionInfoFrame, infoframeObject.port, dictionary);
            }
            return infoframeObject;
        }

        private List<string> GetAviInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> avibytes = GetAviDataBytes(port);
            aviInfoData = avibytes.ToArray();
            List<string> aviData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    aviData = myDictionary[key](aviInfoData);
                }
            }
            aviData.ForEach(Console.WriteLine);
            return aviData;
        }

        private List<string> GetAudioInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> audiobytes = GetAudioDataBytes(port);
            audioInfoData = audiobytes.ToArray();
            List<string> audioData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    audioData = myDictionary[key](audioInfoData);
                }
            }
            audioData.ForEach(Console.WriteLine);
            return audioData;
        }

        private List<string> GetVendorInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> vendorbytes = GetVendorDataBytes(port);
            vendorInfoData = vendorbytes.ToArray();
            List<string> vendorData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    vendorData = myDictionary[key](vendorInfoData);
                }
            }
            vendorData.ForEach(Console.WriteLine);
            return vendorData;
        }

        private List<string> GetSPDInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> spdbytes = GetSourceProductDescriptionDataBytes(port);
            spdInfoData = spdbytes.ToArray();
            List<string> spdData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    spdData = myDictionary[key](spdInfoData);
                }
            }
            spdData.ForEach(Console.WriteLine);
            return spdData;
        }

        private List<string> GetGMPInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> gmpbytes = GetGMPMetadataPacketBytes(port);
            gmPacketData = gmpbytes.ToArray();
            List<string> gmpData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    gmpData = myDictionary[key](gmPacketData);
                }
            }
            gmpData.ForEach(Console.WriteLine);
            return gmpData;
        }

        private List<string> GetGCPInfoData(FunctionInfoFrame function, DVMU_PORT ports, Dictionary<FunctionInfoFrame, Func<byte[], List<string>>> myDictionary)
        {
            DVMU_PORT port = (DVMU_PORT)Enum.Parse(typeof(DVMU_PORT), ports.ToString());
            List<byte> gcpbytes = new List<byte>();
            switch (port)
            {
                case DVMU_PORT.PORTA: gcpbytes.Add(0x00);
                    break;
                case DVMU_PORT.PORTB: gcpbytes.Add(0x01);
                    break;
                default: break;
            }
            gcpPacketData = gcpbytes.ToArray();
            List<string> gcpData = new List<string>();
            foreach (FunctionInfoFrame key in myDictionary.Keys)
            {
                if (String.Compare(function.ToString(), key.ToString()) == 0)
                {
                    gcpData = myDictionary[key](gcpPacketData);
                }
            }
            gcpData.ForEach(Console.WriteLine);
            return gcpData;
        }

        private static DVMU4_STATUS ReadHDMIReg(byte address, byte offset, out byte value)
        {
            return Interop.ReadHdmiRegistry(address, offset, out value);
        }

        private List<byte> GetAviDataBytes(DVMU_PORT port)
        {
            Log.Message("Get AVI Data Bytes");
            byte value = 0;
            List<byte> aviData = new List<byte>();
            byte[] aviAddresses = new byte[31] { 0xE0, 0xE1, 0xE2, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C,
                                                 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B};
            if (Interop.SelectActivePort(port) == DVMU4_STATUS.SUCCESS)
                Log.Message("Interop Select Active Port Sucess");

            for (int i = 0; i < aviAddresses.Length; i++)
            {
                ReadHDMIReg(0x7c, aviAddresses[i], out value);
                aviData.Add(value);
            }
            return aviData;
        }

        private List<byte> GetAudioDataBytes(DVMU_PORT port)
        {
            Log.Message("Get Audio Data Bytes");
            byte value = 0;
            List<byte> audioData = new List<byte>();

            byte[] audioAddresses = new byte[17] { 0xE3, 0xE4, 0xE5, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29 };

            if (Interop.SelectActivePort(port) == DVMU4_STATUS.SUCCESS)
                Log.Message("Interop Select Active Port Sucess");

            for (int i = 0; i < audioAddresses.Length; i++)
            {
                ReadHDMIReg(0x7c, audioAddresses[i], out value);
                audioData.Add(value);
            }
            return audioData;
        }

        private static List<byte> GetVendorDataBytes(DVMU_PORT port)
        {
            Log.Message("Get Vendor Data Bytes");
            byte value = 0;
            List<byte> vendorData = new List<byte>();
            byte[] vendorSpecificAddr = new byte[31] { 0xEC, 0xED, 0xEE, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5E, 0x5F, 0x60,
                                                 0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F};
            if (Interop.SelectActivePort(port) == DVMU4_STATUS.SUCCESS)
                Log.Message("Interop Select Active Port Sucess");
            for (int i = 0; i < vendorSpecificAddr.Length; i++)
            {
                ReadHDMIReg(0x7c, vendorSpecificAddr[i], out value);
                vendorData.Add(value);
            }
            return vendorData;
        }

        private static List<byte> GetSourceProductDescriptionDataBytes(DVMU_PORT port)
        {
            Log.Message("Get SPD Data Bytes");
            byte value = 0;
            List<byte> spdData = new List<byte>();
            byte[] spdAddresses = new byte[31] { 0xE6, 0xE7, 0xE8, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45 };
            if (Interop.SelectActivePort(port) == DVMU4_STATUS.SUCCESS)
                Log.Message("Interop Select Active Port Sucess");
            for (int i = 0; i < spdAddresses.Length; i++)
            {
                ReadHDMIReg(0x7c, spdAddresses[i], out value);
                spdData.Add(value);
            }
            return spdData;
        }

        private static List<byte> GetGMPMetadataPacketBytes(DVMU_PORT port)
        {
            Log.Message("Get GMP Data Bytes");
            byte value = 0;
            List<byte> GMPData = new List<byte>();
            byte[] gmpMedadataAddr = new byte[31] { 0xF8, 0xF9, 0xFA, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xCB, 0xCC, 0xCD, 0xCE, 0xCF, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xDB, 0xDC, 0xDD, 0xDE, 0xDF };
            if (Interop.SelectActivePort(port) == DVMU4_STATUS.SUCCESS)
                Console.WriteLine("Interop Select Active Port Sucess");
            for (int i = 0; i < gmpMedadataAddr.Length; i++)
            {
                ReadHDMIReg(0x7c, gmpMedadataAddr[i], out value);
                GMPData.Add(value);
            }
            return GMPData;
        }

        private List<string> AllAvi(byte[] aviInfoData)
        {
            Log.Message("Getting All AVI InfoFrame Data");
            List<string> returnAVIInfoframeData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnAVIInfoframeData = ComputeYCCQuantizationRange(aviInfoData);
            returnFunction = ComputeITContentType(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeActiveFormatInfo(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeBarInfo(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeScanInfo(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeColorimetry(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeActiveFormatAspectRatio(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeNonUniformPictureScaling(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputePixelRepition(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeLinePixelBarData(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeRGBQuantizationRange(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeITContent(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = FillHeaderDataAvi(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeHDMIColorFormat(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputeExtendedColorimetry(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            returnFunction = ComputePictureAspectRatio(aviInfoData);
            returnAVIInfoframeData.AddRange(returnFunction);
            return returnAVIInfoframeData;
        }

        private List<string> ComputeYCCQuantizationRange(byte[] aviInfoData)
        {
            Log.Message("Compute YCC Quantization Range");
            List<string> retString = new List<string>();
            yccQuantizationRange = (YCC_QUANTIZATION_RANGE)((aviInfoData[8] & 0xc0) >> 6);
            string complete = " YCCQuantizationRange = " + yccQuantizationRange.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeITContentType(byte[] aviInfoData)
        {
            Log.Message("Compute IT Content Type");
            List<string> retString = new List<string>();
            itContentType = (IT_CONTENT_TYPE)(((aviInfoData[6] & 0x0c) >> 6) | ((aviInfoData[8] & 0x30) >> 4));
            string complete = " ITContentType = " + itContentType.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeActiveFormatInfo(byte[] aviInfoData)
        {
            Log.Message("Compute Active Format Info");
            List<string> retString = new List<string>();
            activeFormatInfo = (ACTIVE_FORMAT_INFO)((aviInfoData[4] & 0x10) >> 4);
            string complete = "ActiveFormatInfo = " + activeFormatInfo.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeBarInfo(byte[] aviInfoData)
        {
            Log.Message("Compute Bar Info");
            List<string> retString = new List<string>();
            barInfo = (BAR_INFO)((aviInfoData[4] & 0x0c) >> 2);
            string complete = " BarInfo = " + barInfo.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeScanInfo(byte[] aviInfoData)
        {
            Log.Message("Compute Scan Info");
            List<string> retString = new List<string>();
            scanInfo = (SCAN_INFO)(aviInfoData[4] & 0x03);
            string complete = " ScanInfo = " + scanInfo.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeColorimetry(byte[] aviInfoData)
        {
            Log.Message("Compute Colorimetry");
            List<string> retString = new List<string>();
            colorimetry = (COLORIMETRY)((aviInfoData[5] & 0xc0) >> 6);
            string complete = " Colorimetry = " + colorimetry.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputePictureAspectRatio(byte[] aviInfoData)
        {
            Log.Message("Compute Picture Aspect Ratio");
            List<string> retString = new List<string>();
            pictureAspectRatio = (PICTURE_ASPECT_RATIO)((aviInfoData[5] & 0xa0) >> 6);
            string complete = " PictureAspectRatio = " + pictureAspectRatio.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeActiveFormatAspectRatio(byte[] aviInfoData)
        {
            Log.Message("Compute Active Format Aspect Ratio");
            List<string> retString = new List<string>();
            activeFormatAspectRatio = (ACTIVE_FORMAT_ASPECT_RATIO)(aviInfoData[5] & 0x0f);
            string complete = " ActiveFormatAspectRatio = " + activeFormatAspectRatio.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeNonUniformPictureScaling(byte[] aviInfoData)
        {
            Log.Message("Compute Non Uniform Picture Scaling");
            List<string> retString = new List<string>();
            nonUniformPictureScaling = (NON_UNIFORM_PICTURE_SCALING)(aviInfoData[6] & 0x03);
            string complete = " NonUniformPictureScaling = " + nonUniformPictureScaling.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputePixelRepition(byte[] aviInfoData)
        {
            Log.Message("Compute Pixel Repition");
            List<string> retString = new List<string>();
            pixelRepetition = (PIXEL_REPITION)(aviInfoData[8] & 0x0f);
            string complete = " PixelRepetition = " + pixelRepetition.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeExtendedColorimetry(byte[] aviInfoData)
        {
            Log.Message("\nCompute Extended Colorimetry");
            List<string> retString = new List<string>();
            extendedColorimetry = (EXTENDED_COLORIMETRY)((aviInfoData[6] & 0x70) >> 4);
            string complete = "ExtendedColorimetry = " + extendedColorimetry.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeLinePixelBarData(byte[] aviInfoData)
        {
            Log.Message("Compute Line Pixel Bar Data");
            lineNumberOfEndOfTopBar = Convert.ToUInt32((aviInfoData[10] << 8) | aviInfoData[9]);
            lineNumberOfStartOfBottomBar = Convert.ToUInt32((aviInfoData[12] << 8) | aviInfoData[11]);
            pixelNumberOfEndOfLeftBar = Convert.ToUInt32((aviInfoData[14] << 8) | aviInfoData[13]);
            pixelNumberOfStartOfRightBar = Convert.ToUInt32((aviInfoData[16] << 8) | aviInfoData[15]);
            string complete = "Line_Number_of_End_of_Top_Bar = " + lineNumberOfEndOfTopBar.ToString() + " Line_Number_of_Start_of_Bottom_Bar = " + lineNumberOfStartOfBottomBar.ToString() + " Pixel_Number_of_End_of_Left_Bar = " + pixelNumberOfEndOfLeftBar.ToString() + "Pixel_Number_of_Start_of_Right_Bar = " + pixelNumberOfStartOfRightBar.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeRGBQuantizationRange(byte[] aviInfoData)
        {
            Log.Message("Compute RGB Quantization Range");
            rgbQuantizationRange = (RGB_QUANTIZATION_RANGE)((aviInfoData[6] & 0x0c) >> 2);
            string complete = "RGBQuantizationRange = " + rgbQuantizationRange.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeITContent(byte[] _aviInfoData)
        {
            Log.Message("Compute IT Content");
            itContent = (IT_CONTENT)((_aviInfoData[6] & 0x0c) >> 7);
            string complete = " ITContent = " + itContent.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }
        private List<string> FillHeaderDataAvi(byte[] aviInfoData)
        {
            Log.Message("Fill Header Data");
            List<string> retString = new List<string>();
            infoFrameType = (INFOFRAME_TYPE)aviInfoData[0];
            version = aviInfoData[1];
            length = aviInfoData[2];
            checkSum = aviInfoData[3];
            string complete = "InfoFrame Type = " + infoFrameType + " Version = " + version.ToString() + " Length = " + length.ToString() + " Checksum = " + checkSum.ToString(); ;
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeHDMIColorFormat(byte[] aviInfoData)
        {
            Log.Message("Compute HDMI Color Format");
            hdmiColorFormat = (HDMI_COLOR_FORMAT)((aviInfoData[4] & 0x60) >> 5);
            string complete = " HdmiColorFormat = " + hdmiColorFormat.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }

        private List<string> AllAudio(byte[] audioInfoData)
        {
            Log.Message("Getting All AUDIO InfoFrame Data");
            List<string> returnAudioInfoFrameData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnAudioInfoFrameData = FillHeaderDataAudio(audioInfoData);
            returnFunction = ComputeAudioCodingType(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeAudioChannelCount(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeSamplingFrequency(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeSampleSize(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeDownMixInhibit(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeLevelShiftValue(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeLFEPlaybackLevelInfo(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            returnFunction = SpeakerPlacement(audioInfoData);
            returnAudioInfoFrameData.AddRange(returnFunction);
            return returnAudioInfoFrameData;
        }

        private List<string> FillHeaderDataAudio(byte[] audioInfoData)
        {
            Log.Message("Fill Header Data");
            infoFrameType = (INFOFRAME_TYPE)audioInfoData[0];
            version = audioInfoData[1];
            length = audioInfoData[2] & 0x1F;
            checkSum = audioInfoData[3];
            List<string> retString = new List<string>();
            string complete = "InfoFrame_Type = " + infoFrameType.ToString() + " Version = " + version.ToString() + " Length = " + length.ToString() + " CheckSum = " + checkSum.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeAudioCodingType(byte[] audioInfoData)
        {
            Log.Message("Compute Audio Coding Type");
            List<string> retString = new List<string>();
            audioCodingType = (AUDIO_CODING_TYPE)(audioInfoData[4] & 0xF0);
            string complete = "AudioCodingType = " + audioCodingType.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeAudioChannelCount(byte[] audioInfoData)
        {
            Log.Message("Compute Audio Channel Count");
            List<string> retString = new List<string>();
            audioChannelCount = (AUDIO_CHANNEL_COUNT)(audioInfoData[4] & 0x07);
            string complete = " AudioChannelCount = " + audioChannelCount.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeSamplingFrequency(byte[] audioInfoData)
        {
            Log.Message("Compute Sampling Frequency");
            samplingFrequency = (SAMPLING_FREQUENCY)((audioInfoData[5] & 0x1c) >> 2);
            List<string> retString = new List<string>();
            string complete = " SamplingFrequency = " + samplingFrequency.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeSampleSize(byte[] audioInfoData)
        {
            Log.Message("Compute Sample Size");
            sampleSize = (SAMPLE_SIZE)(audioInfoData[5] & 0x03);
            List<string> retString = new List<string>();
            string complete = " SampleSize = " + sampleSize.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeDownMixInhibit(byte[] audioInfoData)
        {
            Log.Message("Compute Down Mix Inhibit");
            downMixInhibit = (DOWN_MIX_INHIBIT)(audioInfoData[8] >> 7);
            List<string> retString = new List<string>();
            string complete = " DownMixInhibit = " + downMixInhibit.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeLevelShiftValue(byte[] audioInfoData)
        {
            Log.Message("Compute Shift Value");
            levelShiftValue = (LEVEL_SHIFT_VALUE)((audioInfoData[8] & 0x78) >> 3);
            string complete = "LevelShiftValue = " + levelShiftValue.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeLFEPlaybackLevelInfo(byte[] audioInfoData)
        {
            Log.Message("Compute Lfe Playback Level Info");
            lfePlaybackLevelInfo = (LFE_PLAYBACK_LEVEL_INFO)(audioInfoData[8] & 0x03);
            string complete = " LFE_PlaybackLevelInfo = " + lfePlaybackLevelInfo.ToString();
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }
        private List<string> SpeakerPlacement(byte[] audioInfoData)
        {
            int val = audioInfoData[7];
            speakerPlacement = new SPEAKER_PLACEMENT[8];
            speakerPlacement[0] = SPEAKER_PLACEMENT.Front_Left;
            speakerPlacement[1] = SPEAKER_PLACEMENT.Front_Right;

            switch (val)
            {
                case 0:
                    break;
                case 1:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    break;
                case 2:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    break;
                case 3:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    break;
                case 4:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 5:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 6:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 7:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 8:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    break;
                case 9:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    break;
                case 10:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    break;
                case 11:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    break;
                case 12:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 13:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 14:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Center;
                    break;

                case 15:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Center;
                    break;
                case 16:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Rear_Right_Center;
                    break;
                case 17:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Rear_Right_Center;
                    break;
                case 18:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Rear_Right_Center;
                    break;
                case 19:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Rear_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Rear_Right_Center;
                    break;
                case 20:
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 21:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 22:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 23:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 24:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;

                case 25:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 26:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 27:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Center;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 28:
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 29:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 30:
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                case 31:
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Low_Frequency_Effect;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Front_Center;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Rear_Left;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Rear_Right;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Front_Left_Center;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Front_Right_Center;
                    break;
                default:
                    speakerPlacement[0] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[1] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[2] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[3] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[4] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[5] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[6] = SPEAKER_PLACEMENT.Reserved;
                    speakerPlacement[7] = SPEAKER_PLACEMENT.Reserved;
                    break;
            }
            string complete = "Speaker Placement =";
            for (int i = 0; i < speakerPlacement.Length; i++)
            {
                if (speakerPlacement[i] != SPEAKER_PLACEMENT.Unsupported)
                {
                    complete += speakerPlacement[i] + "   ";
                }
            }
            List<string> retString = new List<string>();
            retString.Add(complete);
            return retString;
        }

        private List<string> AllVendor(byte[] vendorInfoData)
        {
            Log.Verbose("Getting All Vendor InfoFrame Data");
            List<string> returnVendorInfoFrameData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnVendorInfoFrameData = FillHeaderDataVendor(vendorInfoData);
            returnFunction = ComputeRegistrationIdentifier(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeHdmiVideoFormat(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);
            returnFunction = Compute3DStructure(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);
            returnFunction = Compute3DExtendedData(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeHdmiVicResolutionList(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeHdmiVicResolutionList(vendorInfoData);
            returnVendorInfoFrameData.AddRange(returnFunction);

            return returnVendorInfoFrameData;
        }

        private List<string> FillHeaderDataVendor(byte[] vendorInfoData)
        {
            Log.Message("Fill Header Data");
            infoFrameType = (INFOFRAME_TYPE)vendorInfoData[0];
            version = vendorInfoData[1];
            length = vendorInfoData[2] & 0X1F;
            checkSum = vendorInfoData[3];
            List<string> retString = new List<string>();
            string complete = " InfoFrame_Type = " + infoFrameType.ToString() + " Version = " + version.ToString() + " Length = " + length.ToString() + " CheckSum = " + checkSum.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeRegistrationIdentifier(byte[] vendorInfoData)
        {
            Log.Message("Compute Registration Identifier");
            registrationIdentifier = Convert.ToUInt32((vendorInfoData[4] << 16) | (vendorInfoData[5] << 8) | vendorInfoData[6]);
            List<string> retString = new List<string>();
            string complete = " RegistrationIdentifier = " + registrationIdentifier.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeHdmiVideoFormat(byte[] vendorInfoData)
        {
            Log.Message("Compute Hdmi Video Format");
            hdmiVideoFormat = (HDMI_VIDEO_FORMAT)(vendorInfoData[7] & 0xE0);
            List<string> retString = new List<string>();
            string complete = " HdmiVideoFormat = " + hdmiVideoFormat.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> ComputeHdmiVicResolutionList(byte[] vendorInfoData)
        {
            hdmiVicResolutionList = new List<Resolutions>();
            List<string> retString = new List<string>();
            if (hdmiVideoFormat == HDMI_VIDEO_FORMAT.Extended_Resolution_Format)
            {
                int format = vendorInfoData[8];
                Resolutions res1, res2;
                switch (format)
                {
                    case 1:
                        res1 = new Resolutions(4096, 2048, 29.97, false, 296.703, 3840, 560, 176, 88, 296, 29.97, 2160, 90, 8, 10, 72);
                        res2 = new Resolutions(4096, 2048, 30, false, 297, 3840, 560, 176, 88, 296, 30, 2160, 90, 8, 10, 72);
                        hdmiVicResolutionList.Add(res1);
                        hdmiVicResolutionList.Add(res2);
                        break;
                    case 2:
                        res1 = new Resolutions(4096, 2048, 25, false, 297, 3840, 1440, 1056, 88, 296, 25, 2160, 90, 8, 10, 72);
                        hdmiVicResolutionList.Add(res1);
                        break;
                    case 3:
                        res1 = new Resolutions(4096, 2048, 23.98, false, 296.703, 3840, 1660, 1276, 88, 296, 23.976, 2160, 90, 8, 10, 72);
                        res2 = new Resolutions(4096, 2048, 24, false, 297, 3840, 1660, 1276, 88, 296, 24, 2160, 90, 8, 10, 72);
                        hdmiVicResolutionList.Add(res1);
                        hdmiVicResolutionList.Add(res2);
                        break;
                    case 4:
                        res2 = new Resolutions(4096, 2048, 24, false, 297, 4096, 1404, 1020, 88, 296, 24, 2160, 90, 8, 10, 72);
                        hdmiVicResolutionList.Add(res2);
                        break;
                    default:
                        throw new Exception(string.Format("Invalid value ={0} got in ComputeHdmiVicResolutionList()", format));
                }//end of switch
            }//end of if loop
            string complete = "Resolution = " + hdmiVicResolutionList.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> Compute3DStructure(byte[] vendorInfoData)
        {
            Log.Message("Compute 3D Structure");
            threeDStructure = THREE_3D_STRUCTURE.Unsupported;
            List<string> retString = new List<string>();
            if (hdmiVideoFormat == HDMI_VIDEO_FORMAT.Three_3D_Format)
            {
                int format = vendorInfoData[8] & 0xF0;
                switch (format)
                {
                    case 0:
                        threeDStructure = THREE_3D_STRUCTURE.Frame_Packing;
                        break;
                    case 6:
                        threeDStructure = THREE_3D_STRUCTURE.Top_And_Bottom;
                        break;
                    case 8:
                        threeDStructure = THREE_3D_STRUCTURE.Side_By_Side;
                        break;
                    default:
                        if (format > 8)
                        {
                            threeDStructure = THREE_3D_STRUCTURE.RESERVED_From_1001;
                        }
                        else
                        {
                            threeDStructure = THREE_3D_STRUCTURE.RESERVED_Upto_0111;
                        }
                        break;
                }//end of switch
            }
            string complete = " ThreeDStructure = " + threeDStructure.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> Compute3DExtendedData(byte[] vendorInfoData)
        {
            Log.Message("Compute 3D Extended Data");
            if (threeDStructure == THREE_3D_STRUCTURE.Side_By_Side)
            {
                three3DExtendedData = THREE_3D_EXTENDED_DATA.Vendor_Specific_Infoframe;
            }
            else if (threeDStructure == THREE_3D_STRUCTURE.RESERVED_From_1001)
            {
                three3DExtendedData = THREE_3D_EXTENDED_DATA.Additional_3D_Data;
            }
            else
            {
                three3DExtendedData = THREE_3D_EXTENDED_DATA.No_Data;
            }
            List<string> retString = new List<string>();
            string complete = " Three3DExtendedData = " + three3DExtendedData.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> Compute3DTransmissionVideoFormatsResolList(byte[] vendorInfoData)
        {
            Resolutions res1, res2;
            three3DTransmissionVideoFormatsResolList = new List<Resolutions>();
            List<string> retString = new List<string>();
            if (threeDStructure == THREE_3D_STRUCTURE.Frame_Packing)
            {
                res1 = new Resolutions(1920, 1080, 23.98, false, 148.35, 1920, 830, 638, 44, 148, 23.976, 1080, 45, 4, 5, 36);
                res2 = new Resolutions(1920, 1080, 24, false, 148.50, 1920, 830, 638, 44, 148, 24, 1080, 45, 4, 5, 36);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
                res1 = new Resolutions(1280, 720, 59.94, false, 148.35, 1280, 370, 110, 40, 220, 59.94, 720, 30, 5, 5, 20);
                res2 = new Resolutions(1280, 720, 60, false, 148.50, 1280, 370, 110, 40, 220, 60, 720, 30, 5, 5, 20);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
                res1 = new Resolutions(1280, 720, 50, false, 148.50, 1280, 700, 440, 40, 220, 50, 720, 30, 5, 5, 20);
                three3DTransmissionVideoFormatsResolList.Add(res1);
            }
            else if (threeDStructure == THREE_3D_STRUCTURE.Side_By_Side)
            {
                res1 = new Resolutions(1920, 1080, 59.94, true, 74.176, 1920, 280, 88, 44, 148, 59.94, 540, 22, 2, 5, 15);
                res2 = new Resolutions(1920, 1080, 60, true, 74.25, 1920, 280, 88, 44, 148, 60, 540, 23, 2.5, 5, 15.5);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
                res1 = new Resolutions(1920, 1080, 50, true, 74.176, 1920, 720, 528, 44, 148, 50, 540, 22, 2, 5, 15);
                res2 = new Resolutions(1920, 1080, 50, true, 74.176, 1920, 720, 528, 44, 148, 50, 540, 23, 2.5, 5, 15.5);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
            }
            else if (threeDStructure == THREE_3D_STRUCTURE.Top_And_Bottom)
            {
                res1 = new Resolutions(1920, 1080, 23.98, false, 74.176, 1920, 830, 638, 44, 148, 23.976, 1080, 45, 4, 5, 36);
                res2 = new Resolutions(1920, 1080, 24, false, 74.25, 1920, 830, 638, 44, 148, 24, 1080, 45, 4, 5, 36);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
                res1 = new Resolutions(1280, 720, 59.94, false, 74.176, 1280, 370, 110, 40, 220, 59.94, 720, 30, 5, 5, 20);
                res2 = new Resolutions(1280, 720, 60, false, 74.25, 1280, 370, 110, 40, 220, 60, 720, 30, 5, 5, 20);
                three3DTransmissionVideoFormatsResolList.Add(res1);
                three3DTransmissionVideoFormatsResolList.Add(res2);
                res1 = new Resolutions(1280, 720, 50, false, 74.25, 1280, 700, 440, 40, 220, 50, 720, 30, 5, 5, 20);
                three3DTransmissionVideoFormatsResolList.Add(res1);
            }
            string complete = "3D Transmission Video Resolution List = " + three3DTransmissionVideoFormatsResolList.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> AllSpd(byte[] spdInfoData)
        {
            Log.Message("Getting All SPD InfoFrame Data");
            List<string> returnSpdInfoFrameData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnSpdInfoFrameData = FillHeaderDataSpd(spdInfoData);
            returnFunction = ComputeVendorName(spdInfoData);
            returnSpdInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeProductDescription(spdInfoData);
            returnSpdInfoFrameData.AddRange(returnFunction);
            returnFunction = ComputeSourceDeviceInformation(spdInfoData);
            returnSpdInfoFrameData.AddRange(returnFunction);
            return returnSpdInfoFrameData;
        }

        private List<string> FillHeaderDataSpd(byte[] spdInfoData)
        {
            Log.Message("Fill Header Data");
            infoFrameType = (INFOFRAME_TYPE)spdInfoData[0];
            version = spdInfoData[1];
            length = spdInfoData[2];
            List<string> retString = new List<string>();
            string complete = " InfoFrame_Type = " + infoFrameType.ToString() + " Version = " + version.ToString() + " Length = " + length.ToString();
            retString.Add(complete);
            return retString;
        }
        private List<string> ComputeVendorName(byte[] spdInfoData)
        {
            Log.Message("Compute Vendor Name");
            int sourceVendorLength = 8;
            for (int i = 0; i < sourceVendorLength; i++)
            {
                if (spdInfoData[3 + i] != 0)
                {
                    vendorName += (char)spdInfoData[3 + i];
                }
                else
                    vendorName = "default";
            }
            List<string> retString = new List<string>();
            string complete = " VendorName = " + vendorName.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> ComputeProductDescription(byte[] spdInfoData)
        {
            Log.Message("Compute Product Description");
            int productDescriptionLength = 16;
            for (int i = 0; i < productDescriptionLength; i++)
            {
                if (spdInfoData[11 + i] != 0)
                {
                    productDescription += (char)spdInfoData[11 + i];
                }
                else
                    productDescription = "default";
            }
            List<string> retString = new List<string>();
            string complete = " ProductDescription = " + productDescription.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> ComputeSourceDeviceInformation(byte[] spdInfoData)
        {
            Log.Message("Compute Source Device Information");
            sourceDeviceInformation = SOURCE_DEVICE_INFORMATION.Reserved;
            sourceDeviceInformation = (SOURCE_DEVICE_INFORMATION)spdInfoData[27];
            List<string> retString = new List<string>();
            string complete = "SourceDeviceInformation = " + sourceDeviceInformation.ToString();
            retString.Add(complete);
            return retString;

        }
        private List<string> AllGMP(byte[] gmPacketData)
        {
            Log.Message("Getting All GMP Data");
            List<string> returnGMPData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnGMPData = FillHeaderDataGMP(gmPacketData);
            returnFunction = ComputeGMPBodyPacket(gmPacketData);
            returnGMPData.AddRange(returnFunction);
            returnFunction = ComputeGBDBodyPacket(gmPacketData);
            returnGMPData.AddRange(returnFunction);
            return returnGMPData;
        }

        private List<string> FillHeaderDataGMP(byte[] gmPacketData)
        {
            Log.Message("Fill Header Data");
            packetTypeCode = gmPacketData[0] & 0x0f;
            nextField = gmPacketData[1] >> 7;
            affectedGamutSeqNum = gmPacketData[1] & 0x0f;
            currentGamutSeqNum = gmPacketData[2] & 0x0f;
            noCurrentGBD = gmPacketData[2] >> 7;
            gbdprofile = (GBD_PROFILE)((gmPacketData[1] & 0x70) >> 4);
            packetSequence = (PACKET_SEQUENCE)((gmPacketData[2] & 0x30) >> 4);
            List<string> retString = new List<string>();
            string complete = " _Packet_Type_Code = " + packetTypeCode.ToString() + " _Next_Field = " + nextField.ToString() + " _Affected_Gamut_Seq_Num = " + affectedGamutSeqNum.ToString() + " _Current_Gamut_Seq_Num = " + currentGamutSeqNum.ToString() + " _No_Current_GBD = " + noCurrentGBD.ToString() + " GBDprofile = " + gbdprofile.ToString() + " PacketSequence = " + packetSequence.ToString();
            retString.Add(complete);
            return retString;
        }

        private List<string> ComputeGMPBodyPacket(byte[] gmPacketData)
        {
            int gbdStartIndex = 0;
            if (gbdprofile == GBD_PROFILE.P0)
            {
                gbdLength = 28;
                gbdStartIndex = 3;
            }
            else
            {
                gbdLength = ((gmPacketData[3] << 8) | gmPacketData[4]);
                gbdChecksum = gmPacketData[5];
                gbdStartIndex = 6;
            }
            gbdData = new byte[gbdLength];
            for (int i = 0; i < gbdLength; i++)
            {
                gbdData[i] = gmPacketData[i + gbdStartIndex];
            }
            List<string> retString = new List<string>();
            retString.Add(gbdData.ToString());
            return retString;
        }

        private List<string> ComputeGBDBodyPacket(byte[] gmPacketData)
        {
            formatFlag = (FORMAT_FLAG)((gbdData[0] & 0x80) >> 7);
            gbdColorPrecision = (GBD_COLOR_PRECISION)((gbdData[0] & 0x18) >> 3);
            gbdColorSpace = ComputeGBDColorSpace(formatFlag);
            int bpp = GetbppFromGBDColorPrecision(gbdColorPrecision);
            if (formatFlag == FORMAT_FLAG.Vertices_or_Facets)
            {
                numberVertices = (gbdData[1] << 8) | (gbdData[2]);
                facetMode = (FACET_MODE)((gbdData[0] & 0x40) >> 6);
                vSize = Convert.ToInt32(3 * numberVertices * bpp / 8 + 0.99999);
                numberFacets = (gbdData[vSize + 3] << 8) | (gbdData[vSize + 4]);
            }
            else
            {
                facetMode = FACET_MODE.Reserved;
                minRedData = ComputeMinMaxColorData(0, bpp);
                maxRedData = ComputeMinMaxColorData(1, bpp);
                minGreenData = ComputeMinMaxColorData(2, bpp);
                maxGreenData = ComputeMinMaxColorData(3, bpp);
                minBlueData = ComputeMinMaxColorData(4, bpp);
                maxBlueData = ComputeMinMaxColorData(5, bpp);
            }
            List<string> retString = new List<string>();
            string complete = " Max_Blue_Data =" + maxBlueData.ToString() + "Min_Blue_Data = " + minBlueData.ToString() + " Max_Green_Data =" + maxGreenData.ToString() + "Min_Green_Data = " + minGreenData.ToString() + " Max_Red_Data =" + maxRedData.ToString() + "Min_Red_Data = " + minRedData.ToString() + " Number_Facets= " + numberFacets.ToString() + "VSize = " + vSize.ToString() + "FacetMode = " + facetMode.ToString() + "Number_Vertices = " + numberVertices.ToString() + " FormatFlag = " + formatFlag.ToString() + " GBDColorPrecision = " + gbdColorPrecision.ToString() + " GBDColorSpace =" + gbdColorSpace.ToString() + " bpp = " + bpp.ToString();
            retString.Add(complete);
            return retString;
        }

        private int ComputeMinMaxColorData(int field, int precision)
        {
            int byte1 = (field + 1) * precision / 8;
            int start = (int)decimal.Remainder((field + 1) * precision, 8);
            int byte2 = (field + 2) * precision / 8;
            int end = (int)decimal.Remainder((field + 2) * precision, 8) - 1;
            int[] arr = new int[precision];
            int x = 0;
            int[] byte1Array = ConvertIntToBinaryarray(gbdData[byte1]);
            for (int i = start; i < byte1Array.Length; i++)
            {
                arr[x] = byte1Array[i];
                x++;
            }
            int[] byte2Array = ConvertIntToBinaryarray(gbdData[byte2]);
            if (end >= 0)
            {
                for (int i = 0; i < end; i++)
                {
                    arr[x] = byte2Array[i];
                    x++;
                }
            }
            return ConvertBinaryarrayToInt(arr);
        }

        private int ConvertBinaryarrayToInt(int[] DataArray)
        {
            int x = 0;
            for (int i = 0; i < DataArray.Length; i++)
            {
                x += DataArray[i] * (int)Math.Pow(2, DataArray.Length - 1 - i);
            }
            return x;
        }

        private int[] ConvertIntToBinaryarray(int data)
        {
            int[] bitArray = new int[8];
            for (int i = 0; i < bitArray.Length; i++)
            {
                bitArray[bitArray.Length - 1 - i] = data % 2;
                data /= 2;
            }
            return bitArray;
        }

        private GBD_COLOR_SPACE ComputeGBDColorSpace(FORMAT_FLAG formatFlag)
        {
            GBD_COLOR_SPACE colorSpace = GBD_COLOR_SPACE.RESERVED;
            if (formatFlag == FORMAT_FLAG.Vertices_or_Facets)
            {
                gbdColorSpace = (GBD_COLOR_SPACE)(gbdData[0] & 0x07);
            }
            else
            {
                switch ((gbdData[0] & 0x07))
                {
                    case 1:
                        colorSpace = GBD_COLOR_SPACE.RGB_Expression_Of_xvYCC601;
                        break;
                    case 2:
                        colorSpace = GBD_COLOR_SPACE.RGB_Expression_Of_xvYCC709;
                        break;

                    default:
                        colorSpace = GBD_COLOR_SPACE.RESERVED;

                        break;
                }
            }
            return colorSpace;
        }
        private int GetbppFromGBDColorPrecision(GBD_COLOR_PRECISION gBDColorPrecision)
        {
            int bpp = -1;
            switch (gBDColorPrecision)
            {
                case GBD_COLOR_PRECISION.GBD_Color_8bit:
                    bpp = 8;
                    break;
                case GBD_COLOR_PRECISION.GBD_Color_10bit:
                    bpp = 10;
                    break;
                case GBD_COLOR_PRECISION.GBD_Color_12bit:
                    bpp = 12;
                    break;

                default:
                    throw new Exception(gBDColorPrecision + " value selected in GetbppFromGBDColorPrecision()");
            }
            return bpp;
        }

        private List<string> AllGCP(byte[] gcpPacketData)
        {
            Log.Message("Getting All GCP Data");
            List<string> returnGCPData = new List<string>();
            List<string> returnFunction = new List<string>();
            returnGCPData = GetAVMUTE(gcpPacketData);
            returnFunction = GetDeepColor(gcpPacketData);
            returnGCPData.AddRange(returnFunction);
            return returnGCPData;
        }

        private List<string> GetAVMUTE(byte[] gcpPacketData)
        {
            bool status = false;
            byte value = 0;
            List<string> retString = new List<string>();
            DVMU_PORT ports;
            byte port_byte = gcpPacketData[0];
            if (port_byte == 0x00)
                ports = DVMU_PORT.PORTA;
            else
                ports = DVMU_PORT.PORTB;

            Interop.SelectActivePort(ports);
            if ((ports == DVMU_PORT.PORTA) || (ports == DVMU_PORT.PORTB))
                ReadHDMIReg(HDMI_MAP, 0x04, out value);
            else
                ReadHDMIReg(HDMI_MAP + 2, 0x04, out value);

            status = (value & 0x40) == 0x40 ? true : false;
            string complete = "AVMute status= " + status;
            retString.Add(complete);
            return retString;
        }
        private List<string> GetDeepColor(byte[] gcpPacketData)
        {
            DEEPCOLORBPC colorFormat = DEEPCOLORBPC.UnSupported;
            byte value = 0;
            int outputColor = 0;
            byte port_byte = gcpPacketData[0];
            DVMU_PORT ports;
            if (port_byte == 0x00)
                ports = DVMU_PORT.PORTA;
            else
                ports = DVMU_PORT.PORTB;
            Interop.SelectActivePort(ports);
            if ((ports == DVMU_PORT.PORTA) || (ports == DVMU_PORT.PORTB))
                ReadHDMIReg(HDMI_MAP, 0x0B, out value);
            else
                ReadHDMIReg(HDMI_MAP + 2, 0x0B, out value);
            outputColor = (value & 0xC0) >> 6;
            colorFormat = (DEEPCOLORBPC)outputColor;

            String str = "Deep color value is:  " + colorFormat.ToString();
            if (colorFormat == DEEPCOLORBPC.UnSupported)
                Console.WriteLine("Failed to fetch deepcolor bpc.. Received " + colorFormat);
            else
                Console.WriteLine(str);
            List<string> retString = new List<string>();
            retString.Add(str);
            return retString;
        }
    }

}