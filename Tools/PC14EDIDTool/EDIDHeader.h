//Author: Ganesh Ram S.T
//Author: Sudhir Tiruke	(VTB & Block Map Ext support)

#include "Resource.h"

// #defines for the Extension Tags of supported Exts in EDID.
#define	BLOCK_MAP_TAG	0xF0
#define CE_EXT_TAG		0x02
#define	VTB_EXT_TAG		0x10


//EDID Structure Definition Starts Here	
		
	//0-7
	struct _HEADER
	{
		BYTE START_HEADER;//00h
		BYTE byte2;//FFh
		BYTE byte3;//FFh
		BYTE byte4;//FFh
		BYTE byte5;//FFh
		BYTE byte6;//FFh
		BYTE byte7;//FFh
		BYTE END_HEADER;//00h
	};
	
	//8-9
	struct _MANUFACTURER_ID
	{
		BYTE  First_Second;//Bit 7-0,Bit 6-2, First Character,Bit 1,0 Second Character
		BYTE  Second_Third;//Bit 7-5,Second Character,Bit 4-0,Third Character
	};
	
	
	//10-11
	struct _PRODUCT_ID
	{
		BYTE FirstNumber;//Stored in Little Endian Format
		BYTE SecondNumber;
	};
	
	
	//12-15
	struct _SERIAL_ID
	{
		BYTE byte1;//Stored in Little Endian Format
		BYTE byte2;
		BYTE byte3;
		BYTE byte4;
	};
	
	//16-17
	struct _YEAR_AND_WEEK_OF_MANUFACTURE	
	{
		BYTE Week_Of_Manufacture;//Gives Week of Manufacture
		BYTE Year_Of_Manufacture;//Gives Year of Manufacture
	};
	
	//18-19
	struct _EDID_VERSION_AND_REVISION
	{
		BYTE Edid_Version;//Gives EDID Version Number
		BYTE Edid_Revision;//Gives EDID Revision Number
	};
	
	
	struct _VIDEO_INPUT_DEFN
	{
		BYTE sync_input_supported_0_DFP: 1;//if set,serration of Vsync Pulse is required
		//if Digital, Interface is Signal Compatible with
		//VESA DFP TMDS Standard	
		BYTE sync_input_supported_1: 1;//if set,sync on green video supported
		BYTE sync_input_supported_2: 1;//if set,composite syncs supported
		BYTE sync_input_supported_3: 1;//if set,separate syncs supported
		BYTE setup : 1;// Bit 4 If 1 Display expects blank-blank signal
		BYTE signal_level_standard: 2;//Bit 6&5
		//0 0.700 0.300 1.0 Vpp			
		//1 0.714 0.286 1.0 Vpp
		//2 1.000 0.400 1.4 Vpp
		//3 0.700 0.000 0.7 Vpp
		BYTE Analog_Digital : 1; // 0- Analog ,1 - Digital
	};
	
	
	struct _DISPLAY_FEATURES_SUPPORT
	{
		BYTE GTF_Supported:1;// if set , indicates GTF is supported
		BYTE pref_timing_mode: 1;//if set, the timing mode is described in the first
		//detailed timing block
		BYTE default_color_space: 1;// If set,display uses default RGB Space
		BYTE display_type:2;// Bit 4 & 3
		// 0 Monochrome
		// 1 RGB Color	
		// 2 Non RGB Multicolor
		// 3 Undefined
		BYTE ActiveOff_VeryLowPower: 1;
		BYTE Suspend: 1;//Suspend
		BYTE StandBy : 1;// StandBy supported
	};			
	
	//20-24
	struct _BASIC_DISPLAY_PARAMETERS
	{
		
		_VIDEO_INPUT_DEFN VIDEO_INPUT_DEFN;
		BYTE MAX_HORIZONTAL_SIZE; //Indicates Max Horizontal Size in mm
		BYTE MAX_VERTICAL_SIZE;// Indicates Max Vertical Size in mm
		BYTE DISPLAY_GAMMA;//Value * 100 - 100 gives display gamma value
		_DISPLAY_FEATURES_SUPPORT DISPLAY_FEATURES_SUPPORT;
	};
	
	//25-34
	struct _CHROMA_INFO
	{
		BYTE low_redx:2;//Lower 2 bits of Red X
		BYTE low_redy:2;//Lower 2 bits of Red Y
		BYTE low_greenx:2;//Lower 2 bits of Green X
		BYTE low_greeny:2;//Lower 2 bits of Green Y
		
		
		BYTE low_bluex:2;//Lower 2 bits of Blue X
		BYTE low_bluey:2;//Lower 2 bits of Blue Y
		BYTE low_whitex:2;//Lower 2 bits of White X
		BYTE low_whitey:2;//Lower 2 bits of White Y
		
		BYTE high_redx:8;//Upper 8 bits of Red X
		BYTE high_redy:8;//Upper 8 bits of Red Y
		BYTE high_greenx:8;//Upper 8 bits of Green X
		BYTE high_greeny:8;//Upper 8 bits of Green Y
		BYTE high_bluex:8;//Upper 8 bits of Blue X
		BYTE high_bluey:8;//Upper 8 bits of Blue X
		BYTE high_whitex:8;//Upper 8 bits of White X
		BYTE high_whitey:8;//Upper 8 bits of White X
	};
	
	//35
	struct _ESTABLISHED_TIMING_SECTION_I
	{
		BYTE bit0:1;//800x600@60 Hz, VESA
		BYTE bit1:1;//800x600@56 Hz, VESA
		BYTE bit2:1;//640x480@75 Hz, VESA
		BYTE bit3:1;//640x480@72 Hz, VESA
		BYTE bit4:1;//640x480@67 Hz, Apple Mac II
		BYTE bit5:1;//640x480@60 Hz, IBM VGA
		BYTE bit6:1;//720x400@88 Hz, IBM XGA 2
		BYTE bit7:1;//720x400@70 Hz, IBM VGA
		
	};
	
	//36
	struct _ESTABLISHED_TIMING_SECTION_II	
	{
		
		BYTE bit0:1;//1280x1024@75 Hz, VESA
		BYTE bit1:1;//1024x768@75 Hz, VESA
		BYTE bit2:1;//1024x768@70 Hz, VESA
		BYTE bit3:1;//1024x768@60 Hz, VESA
		BYTE bit4:1;//1024x768@87 Hz, IBM 
		BYTE bit5:1;//832x624@75 Hz, Apple Mac II
		BYTE bit6:1;//800x600@75 Hz, VESA
		BYTE bit7:1;//800x600@72 Hz, VESA
	};
	
	//37
	struct _MANUFACTURERS_RESERVED_TIMING_SECTION	
	{
		BYTE bits0_6:7;// Reserved
		BYTE bit7:1;//1152x870@75 Hz, Apple Mac II
	};
	
	
	struct _STANDARD_TIMING_IDENTIFICATION_RESOLUTION
	{
		BYTE hor_res:8;//Multiply by 8 and add 248
		BYTE ver_freq:6;//Multiply by 60
		BYTE aspect_ratio:2;//0 16:10
		//1 4:3
		//2 5:4
		//3 16:9
		
	};
	
	//38-53
	struct _STANDARD_TIMING_IDENTIFICATION
	{
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION1;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION2;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION3;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION4;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION5;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION6;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION7;
		_STANDARD_TIMING_IDENTIFICATION_RESOLUTION RESOLUTION8;
	};
	
	//54-71
	struct _DETAILED_TIMING_DESCRIPTOR_BLOCK
	{
		BYTE pixel_clock_LSB;//LSB Of Pixel Clock Value
		BYTE pixel_clock_MSB;//MSB Of Pixel Clock Value, Actual Value=Value/10000 MHz
		
		BYTE low_hor_active:8;//LSB of Horizontal Active
		BYTE low_hor_blank:8;//LSB of Horizontal Blanking
		BYTE high_hor_blank:4;//MSB of Hozrizontal Blanking
		BYTE high_hor_active:4;//MSB of Horizontal Active
		
		BYTE low_vert_active:8;//LSB of Vertical Active
		BYTE low_vert_blank:8;//LSB of Vertical Blanking
		BYTE high_vert_blank:4;//MSB of Vertical Blanking
		BYTE high_vert_active:4;//MSB of Vertical Active
		
		BYTE low_hor_sync_offset:8;//LSB of Horizontal Sync Offset
		BYTE low_hor_sync_pulse_width:8;//LSB of Horizontal Sync Pulse Width
		
		BYTE low_vert_pulse_width:4;//LSB of Vertical Sync Pulse Width
		BYTE low_vert_sync_offset:4;//LSB of Vertical Sync Offset
		
		BYTE high_vert_pulse_width:2;//MSB of Vertical Sync Pulse Width
		BYTE high_vert_sync_offset:2;//MSB of Vertical Sync Offset
		BYTE high_hor_sync_pulse_width:2;//MSB of Horizontal Sync Pulse Width
		BYTE high_hor_sync_offset:2;//MSB of Horizontal Sync Offset 
		
		
		BYTE low_horz_image_size:8;//LSB of Horizontal Image Size
		BYTE low_vert_image_size:8;//LSB of Vertical Image Size
		BYTE high_vert_image_size:4;//MSB of Vertical Image Size
		BYTE high_horz_image_size:4;//MSB of Horizontal Image Size
		
		BYTE horz_border:8;//Horizontal Border
		BYTE vert_border:8;//Vertical Border
		
		BYTE stereo_mode_bit:1;//See stereo_mode
		BYTE polarity:1;//See Above
		BYTE serration_bit:1;// See Above  		
		
		BYTE sync_signal_desc:2;//Bits 4,3
		//00 - Analog Composite, 
								//bit 2 - set controller	shall supply serration
								//bit 1 - set sync pulses should appear on all 3 video lines
		//01 - Bipolar Analog Composite
								//bit 2 - set controller	shall supply serration
								//bit 1 - set sync pulses should appear on all 3 video lines
		//10 - Digital Composite
								//bit 2 - set controller	shall supply serration
								//bit 1 - set Polarity of Hsync Pulses, if 1,polarity is +ve
		//11 - Digital Separate
								//bit 2 - set VSync Polarity is +ve
								//bit 1 - set HSync Polarity is +ve
		
		BYTE stereo_mode:2;// Bits 6,5,0
					   //0,1 - Normal Display, No Stereo
					   //2 - Field Sequential Stereo, right image when stereo sync=1
					   //3 - Field Sequential Stereo, left image when stereo sync=1
					   //4 - 2 way Interleaved Stereo, right image on even lines
					   //5 - 2 way Interleaved Stereo, left image on even lines
					   //6 - 4 way Interleaved Stereo
					   //7 - Side-by-Side Interleaved Stereo	
		
		BYTE interlaced:1;//0 Non Interlaced
						  //1 Interlaced
		
	};
	
	//72-89,90-107,108-125
	struct _DESCRIPTOR_BLOCK
	{
		BYTE FLAGS[2];//0000 Indicates Block Used as Descritptor
		BYTE START_FLAG:8;//00 Indicates Block Contains Data
		BYTE DATA_TYPE_TAG:8;//FF Monitor Serial Number is Stored
							 //FE ASCII Data String is Stored
							 //FD Monitor Range Limits are specified, 
								//see MONITOR_RANGE_LIMITS Structure
							 //FC Monitor Name is Stored
							 //FB Color Point Data is Stored
								//see COLOR_POINT Struct
							 //FA Standard Timing Identifiers are stored
							 //0F-00h Manufacturer Specified
		BYTE END_FLAG:8;
		CHAR MON_DESC_DATA[13];
	};
	
	
	struct _MONITOR_RANGE_LIMITS
	{
		
		BYTE min_vert_rate;//Min Vertical Rate,in Hz
		BYTE max_vert_rate;//Max Vertical Rate, in Hz
		BYTE min_horz_rate;//Min Horizontal Rate, in Hz
		BYTE max_horz_rate;//Max Horizontal Rate, in Hz
		BYTE max_pixel_clock;//Max Pixel Clock,Value/10 Mhz
		BYTE timing_formula_support;//00 - No Secondary Timing Formula Supported
								//02 - Secondary GTF Curve Supported
		//If timing_formula_support is 02
		BYTE reserved;//00h
		BYTE start_freq;//Horizontal Freq, Value/2, KHz
		BYTE byte_C;//C*2
		BYTE LSB_M;//LSB of M Value
		BYTE MSB_M;//MSB of M Value
		BYTE byte_K;//K Value
		BYTE byte_J;//J*2
	};
	
	struct _COLOR_POINT
	{
		BYTE white_point_index_number_1;
		BYTE white_low_bits_1;
		BYTE white_x_1;
		BYTE white_y_1;
		BYTE white_gamma_1;
		BYTE white_point_index_number_2;
		BYTE white_low_bits_2;
		BYTE white_x_2;
		BYTE white_y_2;
		BYTE white_gamma_2;
		BYTE byte_15;
		BYTE byte_16_17[2];
	};                        
	
	//This is the 128-Byte EDID Structure
	struct EDID_STRUCTURE
	{
		_HEADER HEADER;//0-7,8 Bytes
		_MANUFACTURER_ID MANUFACTURER_ID;//8-9,2 Bytes 
		_PRODUCT_ID PRODUCT_ID;//10-11,2 Bytes
		_SERIAL_ID SERIAL_ID;//12-15,4 Bytes
		_YEAR_AND_WEEK_OF_MANUFACTURE YEAR_AND_WEEK_OF_MANUFACTURE;//16-17,2 Bytes
		_EDID_VERSION_AND_REVISION EDID_VERSION_AND_REVISION;//18-19,2 Bytes
		_BASIC_DISPLAY_PARAMETERS BASIC_DISPLAY_PARAMETERS;//20-24,5 Bytes
		_CHROMA_INFO CHROMA_INFO;//25-34,10 Bytes
		_ESTABLISHED_TIMING_SECTION_I ESTABLISHED_TIMING_SECTION_I;//35,1 Byte
		_ESTABLISHED_TIMING_SECTION_II ESTABLISHED_TIMING_SECTION_II;//36,1 Byte
		_MANUFACTURERS_RESERVED_TIMING_SECTION MANUFACTURERS_RESERVED_TIMING_SECTION;//37,1 Byte
		_STANDARD_TIMING_IDENTIFICATION STANDARD_TIMING_IDENTIFICATION;//38-53,16 Bytes
		//_DETAILED_TIMING_DESCRIPTOR_BLOCK DETAILED_TIMING_DESCRIPTOR_BLOCK;//54-71,18 Bytes
		_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK_I;//54-71,18 Bytes
		_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK_II;//72-89,18 Bytes
		_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK_III;//90-107,18 Bytes
		_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK_IV;//108-125,18 Bytes
		BYTE EXTENSION_FLAG;//126,1 Byte
		BYTE CHECK_SUM;//127,1 Byte
	};


		//CEA Extension Block Structure
	//Version 861B


	struct _NATIVE_FORMATS
	{
		BYTE NO_DTD:4;//No. of DTDs Prescribed
		BYTE YCbCr2:1;//Monitor Supports YCbCr 4:2:2 in addition to RGB
		BYTE YCbCr4:1;//Monitor Supports YCbCr 4:4:4 in addtion to RGB
		BYTE AUDIO:1;//Monitor Supports Basic Audio
		BYTE UNDERSCAN:1;//Monitor Supports underscan
		
	};


	struct _GENERAL_TAG_FORMAT
	{	
		BYTE LENGTH_OF_BLOCK:5;//Length of following data block
		BYTE TAG_CODE:3;//Tag Code
						//0 Reserved
						//1 Audio Data Block
						//2 Video Data Block
						//3 Vendor Specific Data Block
						//4 Speaker Allocation Data Block
						//5 VESA DTC Data Block
						//6 RSVD
						//7 Extended Tag
		
	};

	typedef enum _EXTD_TAG
	{
		VIDEO_CAP_DATA_BLK =0,
		VS_VIDEO_DATA_BLK  =1,
		COLORIMETRY_BLK = 5
	}EXTD_TAG;



	struct _CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_UNCOMPRESSED
	{
		BYTE MAX_NO_OF_CHANNELS:3;
		BYTE AUDIO_FORMAT_CODE:4;
		BYTE RESERVED_1:1;

		BYTE BIT_2_0:1;
		BYTE BIT_2_1:1;
		BYTE BIT_2_2:1;
		BYTE BIT_2_3:1;
		BYTE BIT_2_4:1;
		BYTE BIT_2_5:1;
		BYTE BIT_2_6:1;
		BYTE RESERVED_2:1;
		
		BYTE BIT_3_0:1;
		BYTE BIT_3_1:1;
		BYTE BIT_3_2:1;
		BYTE RESERVED_3:5;
	};


	struct _CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_COMPRESSED
	{
		BYTE MAX_NO_OF_CHANNELS:3;
		BYTE AUDIO_FORMAT_CODE:4;
		BYTE RESERVED_1:1;
		
		BYTE BIT_2_0:1;
		BYTE BIT_2_1:1;
		BYTE BIT_2_2:1;
		BYTE BIT_2_3:1;
		BYTE BIT_2_4:1;
		BYTE BIT_2_5:1;
		BYTE BIT_2_6:1;
		BYTE RESERVED_2:1;
		
		BYTE BIT_RATE;
	};


	struct _CEA_SPEAKER_ALLOCATION_DATA_BLOCK
	{
		BYTE BIT1_0:1;
		BYTE BIT1_1:1;
		BYTE BIT1_2:1;
		BYTE BIT1_3:1;
		BYTE BIT1_4:1;
		BYTE BIT1_5:1;
		BYTE BIT1_6:1;
		BYTE RESERVED_1:1;//Reserved
		BYTE RESERVED_2;
		BYTE RESERVED_3;
	};

	struct _CEA_SHORT_VIDEO_DESCRIPTOR_BLOCK
	{
		BYTE VIDEO_ID_CODE:7;
		BYTE NATIVE:1;
	};

	struct _CEA_VIDEO_CAPABILITY_BLOCK
	{
		BYTE S_CE:2;
		BYTE S_IT:2;
		BYTE S_PT:2;
		BYTE QS:1;
		BYTE F37:1;
		BYTE* Future;
	};


	struct _CEA_COLORIMETRY_DATA_BLOCK
	{
		BYTE xvYCC_601:1;
		BYTE xvYCC_709:1;
		BYTE F:6;
		BYTE MD0:1;
		BYTE MD1:1;
		BYTE MD2:1;
		BYTE F_1:5;
		BYTE* Future_1;
	};


	struct _CEA_VENDOR_SPECIFIC_DATA_BLOCK
	{
		BYTE IEEE_REGNO[3];
		BYTE Phys_Add_1;
		BYTE Phys_Add_2;
		BYTE DVI:1;
		BYTE Reserved:2;
		BYTE DC_Y444:1;
		BYTE DC_30:1;
		BYTE DC_36:1;
		BYTE DC_48:1;
		BYTE Al:1;
		BYTE Max_TMDS_Clock;
		BYTE Reserved_1:6;
		BYTE I_Latency:1;
		BYTE Latency:1;
		BYTE Video_Latency;
		BYTE Audio_Latency;
		BYTE Interlaced_Video_Latency;
		BYTE Interlaced_Audio_Latency;
		BYTE PAYLOAD_Reserved[20]; // just an arbitrary value for time being
	};

    // HDMI 1.4 VSDB
	struct _CEA_VENDOR_SPECIFIC_DATA_BLOCK_14
	{
		BYTE IEEE_REGNO[3];
		BYTE Phys_Add_1;
		BYTE Phys_Add_2;
		BYTE DVI:1;
		BYTE Reserved:2;
		BYTE DC_Y444:1;
		BYTE DC_30:1;
		BYTE DC_36:1;
		BYTE DC_48:1;
		BYTE Al:1;
		BYTE Max_TMDS_Clock;
		BYTE Reserved_1:5;
        BYTE HDMI_Video_Present:1;
		BYTE I_Latency:1;
		BYTE Latency:1;
		//BYTE Video_Latency;
		//BYTE Audio_Latency;
		//BYTE Interlaced_Video_Latency;
		//BYTE Interlaced_Audio_Latency;
        BYTE PAYLOAD[50]; // just an arbitrary value for time being
	};

	struct CEA_EXTENSION
	{
		BYTE TAG;//Specifies the tag 02h
		BYTE REVISION;//Specifies revision no 03h
		BYTE DTD_OFFSET;//Specifies byte no. where DTD begins
						//if d=0, No DTDs are provided
						//if no data is proivided then d=4
		_NATIVE_FORMATS NATIVE_FORMATS;
		
		BYTE DATA_BLOCK[123];//Data Blocks
		BYTE CHECK_SUM;//Check sum Value
	};

//**********************************************************
	struct _CVT_DESCRIPTOR
	{
		BYTE VERTICAL_LOWER;

		BYTE RESERVED00 : 2;      // These r reserved & set to 00.
		BYTE ASPECT_RATIO : 2;	  // 00 : 4:3
								  // 01 : 16:9
								  // 10 : 16:10
								  // 11 : Undefined or Reserved.
		BYTE VERTICAL_HIGHER : 4;

		union
		{
			BYTE REFRESH_RATE_Bits;	
			struct
			{
				BYTE RR_60Hz_RB : 1;
				BYTE RR_85Hz	: 1;
				BYTE RR_75Hz	: 1;
				BYTE RR_60Hz	: 1;
				BYTE RR_50Hz	: 1;
				BYTE PREFERED_RR_CONTROL : 2; // 00: 50Hz
											  // 01: 60Hz This means if 60HZ_RB is supported then it wud be preferred or otherwise.
											  // 10: 75Hz
											  // 11: 85Hz
				BYTE RESERVED0  : 1;   // This is reserved & set to 0.
			};
		};
	};


	struct VTB_EXTENSION
	{
		BYTE TAG;            // Should be 0x10
		BYTE VERSION;		 //	Version of VTB Ext 
		BYTE NumDTD;
		BYTE NumCVT;
		BYTE NumST;
		BYTE DATA[122];
		BYTE CHECKSUM;
	};
/******************************************************************************************
*******************************************************************************************

STRUCTURES FOR EDID 1.4

*******************************************************************************************
*******************************************************************************************/

//16-17
	struct _YEAR_AND_WEEK_OF_MANUFACTURE1_4	
	{
		BYTE Week_Of_Manufacture;//Gives Week of Manufacture
		BYTE Year_Of_Manufacture;//Gives Year of Manufacture
	};

	struct _VIDEO_INPUT_DEFN1_4
	{
		BYTE sync_input_supported_0_DFP: 1;//if set,serration of Vsync Pulse is required
		//if Digital, Interface is Signal Compatible with
		//VESA DFP TMDS Standard	
		BYTE sync_input_supported_1: 1;//if set,sync on green video supported
		BYTE sync_input_supported_2: 1;//if set,composite syncs supported
		BYTE sync_input_supported_3: 1;//if set,separate syncs supported
		BYTE setup : 1;// Bit 4 If 1 Display expects blank-blank signal
		BYTE signal_level_standard: 2;//Bit 6&5
		//0 0.700 0.300 1.0 Vpp			
		//1 0.714 0.286 1.0 Vpp
		//2 1.000 0.400 1.4 Vpp
		//3 0.700 0.000 0.7 Vpp
		BYTE Analog_Digital : 1; // bit 7 0- Analog ,1 - Digital
	};

	struct _DISPLAY_FEATURES_SUPPORT1_4
	{
		
		BYTE continuos_frequency:1; // if set, indicates display is continuos frequency
		
		BYTE pref_timing_mode: 1;//if set, the timing mode is described in the first
		//detailed timing block
		BYTE default_color_space: 1;// If set,display uses default RGB Space
		BYTE display_type:2;// Bit 4 & 3
		// 0 Monochrome
		// 1 RGB Color	
		// 2 Non RGB Multicolor
		// 3 Undefined
		BYTE ActiveOff_VeryLowPower: 1;
		BYTE Suspend: 1;//Suspend
		BYTE StandBy : 1;// StandBy supported
	};	

	struct _BASIC_DISPLAY_PARAMETERS1_4
	{
		
		_VIDEO_INPUT_DEFN1_4 VIDEO_INPUT_DEFN1_4;
		union 
		{
			BYTE MAX_HORIZONTAL_SIZE; //Indicates Max Horizontal Size in mm
			BYTE ASPECT_RATIO_L; // Indicates Aspect Ratio (Landscape Orientation)
		};
		union
		{
			BYTE MAX_VERTICAL_SIZE;// Indicates Max Vertical Size in mm
			BYTE ASPECT_RATIO_P; // Indicates Aspect Ratio (Portrait Orientation)
		};
		BYTE DISPLAY_GAMMA;//Value * 100 - 100 gives display gamma value
		_DISPLAY_FEATURES_SUPPORT1_4 DISPLAY_FEATURES_SUPPORT1_4;
	};

	struct _DISPLAY_RANGE_LIMITS1_4
	{
		
		BYTE min_vert_rate;//Min Vertical Rate,in Hz
		BYTE max_vert_rate;//Max Vertical Rate, in Hz
		BYTE min_horz_rate;//Min Horizontal Rate, in Hz
		BYTE max_horz_rate;//Max Horizontal Rate, in Hz
		BYTE max_pixel_clock;//Max Pixel Clock,Value/10 Mhz
		BYTE timing_formula_support;//00 - No Secondary Timing Formula Supported
								//02 - Secondary GTF Curve Supported
		//If timing_formula_support is 02
		BYTE reserved;//00h
		BYTE start_freq;//Horizontal Freq, Value/2, KHz
		BYTE byte_C;//C*2
		BYTE LSB_M;//LSB of M Value
		BYTE MSB_M;//MSB of M Value
		BYTE byte_K;//K Value
		BYTE byte_J;//J*2
	};
	struct _DISPLAY_RANGE_LIMIT_OFFSETS1_4
	{
		BYTE bit_0:1;
		BYTE bit_1:1;
		BYTE bit_2:1;
		BYTE bit_3:1;
		BYTE bit_4:1;
		BYTE bit_5:1;
		BYTE bit_6:1;
		BYTE bit_7:1;
	};

	//72-89,90-107,108-125
	struct _DESCRIPTOR_BLOCK1_4
	{
		BYTE FLAGS[2];//0000 Indicates Block Used as Descritptor
		BYTE START_FLAG:8;//00 Indicates Block Contains Data
		BYTE DATA_TYPE_TAG:8;//FF Monitor Serial Number is Stored
							 //FE ASCII Data String is Stored
							 //FD Monitor Range Limits are specified, 
								//see MONITOR_RANGE_LIMITS Structure
							 //FC Monitor Name is Stored
							 //FB Color Point Data is Stored
								//see COLOR_POINT Struct
							 //FA Standard Timing Identifiers are stored
							 //0F-00h Manufacturer Specified
		_DISPLAY_RANGE_LIMIT_OFFSETS1_4 DISPLAY_RANGE_LIMIT_OFFSETS1_4;
		CHAR MON_DESC_DATA[13];
	   
	};

	struct _COLOR_MANAGEMENT_DATA1_4
	{
		BYTE DCM_VERSION_NUMBER;
		BYTE RED_A3_LSB;
		BYTE RED_A3_MSB;
		BYTE RED_A2_LSB;
		BYTE RED_A2_MSB;
		BYTE GREEN_A3_LSB;
		BYTE GREEN_A3_MSB;
		BYTE GREEN_A2_LSB;
		BYTE GREEN_A2_MSB;
		BYTE BLUE_A3_LSB;
		BYTE BLUE_A3_MSB;
		BYTE BLUE_A2_LSB;
		BYTE BLUE_A2_MSB;
	};

	struct _CVT3_BYTE_CODE_DESCRIPTOR1_4
	{
		BYTE VERSION_NUMBER;
		BYTE PRIORITY_1[3];
		BYTE PRIORITY_2[3];
		BYTE PRIORITY_3[3];
		BYTE PRIORITY_4[3];
	};

	struct _ESTABLISHED_TIMING_SECTION_III1_4
	{
		BYTE REVISION_NUMBER;
		BYTE BYTE_6;
		BYTE BYTE_7;
		BYTE BYTE_8;
		BYTE BYTE_9;
		BYTE BYTE_10;
		BYTE BYTE_11;
		BYTE RESERVED_BYTES;
	};

	

	struct EDID_STRUCTURE1_4
	{
		_HEADER HEADER;//0-7,8 Bytes
		_MANUFACTURER_ID MANUFACTURER_ID;//8-9,2 Bytes 
		_PRODUCT_ID PRODUCT_ID;//10-11,2 Bytes
		_SERIAL_ID SERIAL_ID;//12-15,4 Bytes
		_YEAR_AND_WEEK_OF_MANUFACTURE1_4 YEAR_AND_WEEK_OF_MANUFACTURE1_4;//16-17,2 Bytes
		_EDID_VERSION_AND_REVISION EDID_VERSION_AND_REVISION;//18-19,2 Bytes
		_BASIC_DISPLAY_PARAMETERS1_4 BASIC_DISPLAY_PARAMETERS1_4;//20-24,5 Bytes
		_CHROMA_INFO CHROMA_INFO;//25-34,10 Bytes
		_ESTABLISHED_TIMING_SECTION_I ESTABLISHED_TIMING_SECTION_I;//35,1 Byte
		_ESTABLISHED_TIMING_SECTION_II ESTABLISHED_TIMING_SECTION_II;//36,1 Byte
		_MANUFACTURERS_RESERVED_TIMING_SECTION MANUFACTURERS_RESERVED_TIMING_SECTION;//37,1 Byte
		_STANDARD_TIMING_IDENTIFICATION STANDARD_TIMING_IDENTIFICATION;//38-53,16 Bytes
		_DESCRIPTOR_BLOCK  DESCRIPTOR_BLOCK_I;//54-71,18 Bytes  //Preferred Timing Mode
		_DESCRIPTOR_BLOCK1_4 DESCRIPTOR_BLOCK_II;//72-89,18 Bytes
		_DESCRIPTOR_BLOCK1_4 DESCRIPTOR_BLOCK_III;//90-107,18 Bytes// changes reqd
		_DESCRIPTOR_BLOCK1_4 DESCRIPTOR_BLOCK_IV;//108-125,18 Bytes
		BYTE EXTENSION_FLAG;//126,1 Byte
		BYTE CHECK_SUM;//127,1 Byte
	};

/*******************************************************************************************
********************************************************************************************

END OF STRUCTURES EDID 1.4

********************************************************************************************
********************************************************************************************/

//***********************************************************
//======================================================================
//							Block Map Extension
//======================================================================
	struct BLOCK_MAP_EXTENSION
	{
		BYTE TAG;            // Should be 0xF0
		BYTE DATA[126];		 // Has Extension Tags for next 126 Extensions
		BYTE CHECKSUM;
	};
//=======================================================================

class EDID_BaseBlockParser
{

public:
	EDID_STRUCTURE BASE_BLOCK;
	
	//Parsing EDID Info
	void parseHeader(_HEADER);
	
	void parseManufacturerID(_MANUFACTURER_ID);
	
	void parseProductID(_PRODUCT_ID);
	
	void parseSerialID(_SERIAL_ID);
	
	void parseYear_And_Week(_YEAR_AND_WEEK_OF_MANUFACTURE);
	
	void parseEDID_Version_And_Revision(_EDID_VERSION_AND_REVISION);
	
	void parseBasicDisplayParameters(_BASIC_DISPLAY_PARAMETERS);
	void parseVideoInputDefinition(_VIDEO_INPUT_DEFN);
	void parsePowerMgmtFeatures(_DISPLAY_FEATURES_SUPPORT);
	
	void parsechromaInfo(_CHROMA_INFO);
	
	void parseEstablishedTiming_i(_ESTABLISHED_TIMING_SECTION_I);
	void parseEstablishedTiming_ii(_ESTABLISHED_TIMING_SECTION_II);
	void parseManufacturers_Reserved_timing(_MANUFACTURERS_RESERVED_TIMING_SECTION);
	
	void parseStandard_timing_identification(_STANDARD_TIMING_IDENTIFICATION ,BOOLEAN);
	
	
	
	
	void parseStandard_timing_identification_resolution(_STANDARD_TIMING_IDENTIFICATION_RESOLUTION );
	
	void parsedetailed_timing_descriptor(_DETAILED_TIMING_DESCRIPTOR_BLOCK);
	
	void parsedescriptor_block(_DESCRIPTOR_BLOCK);
	
	void checkDescriptorBlock(_DESCRIPTOR_BLOCK);
	
	void parseMonitor_range_limits(CHAR *);
	void parseColor_Point_info(CHAR *);
	void parseSerialNumber(CHAR *);
	void parseASCIIString(CHAR *);
	void parseMonitorName(CHAR *);
	
	void checkExtension(BYTE);
	void checkSum();

/******************************************************************************************
*******************************************************************************************
FUNCTIONS FOR EDID 1.4
*******************************************************************************************
*******************************************************************************************/

	void parseYear_And_Week1_4(_YEAR_AND_WEEK_OF_MANUFACTURE1_4);
	void parseBasicDisplayParameters1_4(_YEAR_AND_WEEK_OF_MANUFACTURE1_4,_BASIC_DISPLAY_PARAMETERS1_4);
	void parseVideoInputDefinition1_4(_VIDEO_INPUT_DEFN1_4);
	void parsePowerMgmtFeatures1_4(_DISPLAY_FEATURES_SUPPORT1_4,_VIDEO_INPUT_DEFN1_4);
	void parsedescriptor_block1_4(_DESCRIPTOR_BLOCK1_4);
	void checkDescriptorBlock1_4(_DESCRIPTOR_BLOCK1_4);
	void parseDisplay_color_management_data1_4(CHAR *);
	void parseCVT3_byte_timing_codes1_4(CHAR *);
	void parseEstablished_timings_III1_4(CHAR *);
	void parseDisplay_range_limits1_4(_DISPLAY_RANGE_LIMIT_OFFSETS1_4,CHAR *);
	
};


class CEAExtensionParser:public EDID_BaseBlockParser
{
	public:
	EDID_STRUCTURE BASE_BLOCK;
	CEA_EXTENSION CEA_EXT;
	
	void parseCEAExtension(CEA_EXTENSION,CListCtrl *);
	void parseTagRevision(CEA_EXTENSION);
	void parseNativeFormat(CEA_EXTENSION);

	void parseVideoDescBlock(_CEA_SHORT_VIDEO_DESCRIPTOR_BLOCK);
	void parseAudioDescBlockUncompressed(_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_UNCOMPRESSED);
	void parseAudioDescBlockCompressed(_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_COMPRESSED);
	void parseSpeakerAllocBlock(_CEA_SPEAKER_ALLOCATION_DATA_BLOCK);
	void parseVendorSpecificBlock(_CEA_VENDOR_SPECIFIC_DATA_BLOCK_14);
	void parseColorimetryBlock(_CEA_COLORIMETRY_DATA_BLOCK);
	void parseVideoCapabilityBlock(_CEA_VIDEO_CAPABILITY_BLOCK);
    CString Print3DVICDetails(ULONG ul3DVics);
    CString Print3DFormats(ULONG ul3DStructure);
    CString Print3DDetail(ULONG ul3DDetail);
    CString Print3DStructureAll(ULONG ul3DStructure);
    CString GetVICModeText(BYTE CODE);

	void getByteValues();
	void getByteValuesCEA();
	void CEAcheckSum();

protected:
    BYTE ucSupportedVIC[30];
};

class VTBExtensionParser : public EDID_BaseBlockParser
{
	public:
	EDID_STRUCTURE BASE_BLOCK;
	VTB_EXTENSION VTB_EXT;

	void parseTagVersion(VTB_EXTENSION);
	void parseVTBExtension(VTB_EXTENSION, CListCtrl *);
	void parseCVTDescriptor(_CVT_DESCRIPTOR);
	void VTBChecksum();
};

class BlockMapExtensionParser : public EDID_BaseBlockParser
{
	public:
	EDID_STRUCTURE BASE_BLOCK;
	BLOCK_MAP_EXTENSION BLOCK_MAP_EXT;

	void parseTag(BLOCK_MAP_EXTENSION);
	void parseBlockMapExtension(BLOCK_MAP_EXTENSION, CListCtrl *);
	void BlockMapChecksum();
};




