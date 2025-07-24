//Author: Ganesh Ram S.T 
//Author: Sudhir Tiruke	(VTB & Block Map Ext support)

#include "stdAfx.h"
#include "EDIDHeader.h"
#include "EDIDToolDlg.h"

/*==============================================================================
Parser for EDID Structure 1.3 
Supports CEA, VTB & Block Map Extensions, Thus it supports EDID with more than 1 extensions.
================================================================================*/

CString Text;//Text Data to be Displayed
BYTE *edidbuffer;//128 byte structure for the base block
BYTE *ceaext;//128 byte structure for the CEA 861B extension
BYTE *vtbext;//128 byte for VTB extension.
BYTE *BlockMapExt; // 128 byte Block in EDID which has Tags for all extensions present.
BOOLEAN cextflag=FALSE;//Indicates whether block has Extension or not
BOOLEAN vtbextflag = FALSE; //Check for presence of VTB ext 
BOOLEAN BlockMapFlag = FALSE; // Flag for presence of Block Map.
BOOLEAN Headervalid = TRUE; // Flag to avoid reading extension if base block header is Invalid.
//INT NumExt = 0;	// Number of Extensions present in the EDID.
CListCtrl *ListBox;//Handle of the ListItem

//CEA Data Block Tag Codes
enum CEA_Data_Block_Tag_Codes{
	//Reseved_0 
	Audio_Data_Block				= 1,
	Video_Data_Block				= 2,
	Vendor_Specific_Data_Block		= 3,
	Speaker_Allocation_Data_Block	= 4,
	VESA_DTC_Data_Block				= 5,
	//Reserved_6
	Extended_Tag					= 7 };

CEA_Data_Block_Tag_Codes tag_code; //- CEA Data Block Tag Codes

	

INT L=0;//Length of Extension Block
INT k=0;


INT listcount=0;  //Variable used for the no. of items in listItem
BYTE byteTemp;    //
INT byteCount=0;  //

//Offset for Data Block
INT d=0;
//No. of DTDs
INT n;
INT n1=0;
INT CurrentExtNo = 0;		// Current Extension number.
INT CurrentByteNo = 0;		// Contains the no. of the last byte parsed in the current extension .

#define BIT(x) (1<<x)

//Parsing Starts Here

void EDID_BaseBlockParser::parseHeader(_HEADER HEADER)
{
	//Process the Header
	Text="\r\n**************************************\r\n";
	Text+="Block No.: 0     Base Block\r\n";
	Text+="**************************************\r\n";	
	
	Text+="[0-7],Header";

	
	if(HEADER.START_HEADER!= 0x00 || HEADER.byte2!= 0xFF || HEADER.byte3!= 0xFF || HEADER.byte4!=0xFF || HEADER.byte5!= 0xFF || HEADER.byte6!= 0xFF || HEADER.byte7!= 0xFF || HEADER.END_HEADER!=0x00)
	{
		Text+=" Not OK!\r\n";
	}
	else
	{
		Text+=" OK!\r\n";
	}

}


void EDID_BaseBlockParser::parseManufacturerID(_MANUFACTURER_ID MANUFACTURER_ID)
{
			
	//Parse Manufacturer ID, 
	//Byte 1,Bit 7 = 0
	//Byte 1,Bit 6-2 = 1st Char
	//Byte 1,Bit 1,0 and Byte 2,Bit 7-5 = 2nd Char
	//Byte 2,BIt 4-0=3rd Char
	
	CHAR First_Char;
	CHAR Second_Char;
	CHAR Third_Char;
	CHAR temp;
	CHAR *string=(CHAR *)malloc(256);
	
	
	First_Char=MANUFACTURER_ID.First_Second;
	First_Char=(First_Char>>2);
	First_Char&=0x1F;
	First_Char+=64;
	
	Second_Char=MANUFACTURER_ID.First_Second;
	Second_Char=(Second_Char<<3);
	Second_Char=(Second_Char&0x18);
	temp=MANUFACTURER_ID.Second_Third;
	temp=temp>>5;
	temp=temp&0x07;
	Second_Char=(Second_Char|temp);
	Second_Char+=64;
	
	Third_Char=MANUFACTURER_ID.Second_Third;
	Third_Char=Third_Char&0x01F;
	Third_Char+=64;
	sprintf_s(string,256,"[8-9],Manufacturer ID: %c%c%c\r\n",First_Char,Second_Char,Third_Char);	
	Text+=string;
	free(string);
}


void EDID_BaseBlockParser::parseProductID(_PRODUCT_ID PRODUCT_ID)
{
	//Parse Product ID
	//Info is in Hex Value
	
	CHAR *string=(CHAR *)calloc(256,1);
	sprintf_s(string,256,"[10-11],Product ID: %2x%2x \r\n",PRODUCT_ID.SecondNumber,PRODUCT_ID.FirstNumber);
	
	Text+=string;
	free(string);
}


void EDID_BaseBlockParser::parseSerialID(_SERIAL_ID SERIAL_ID)
{
	//Parse Serial ID
	//Info is in Hex Value
	
	CHAR *string=(CHAR *)malloc(256);
	sprintf_s(string,256,"[12-15],Serial ID: %2x%2x%2x%2x\r\n",SERIAL_ID.byte4,SERIAL_ID.byte3,SERIAL_ID.byte2,SERIAL_ID.byte1);
	
	Text+=string;
	free(string);
}

void EDID_BaseBlockParser::parseYear_And_Week(_YEAR_AND_WEEK_OF_MANUFACTURE YEAR_AND_WEEK_OF_MANUFACTURE)
{
	//Parse Year and Week
	//Week in decimal value
	//Add 1990 + year to get the actual value
	
	CHAR *string=(CHAR *)malloc(256);
	
	sprintf_s(string,256,"[16],Week of Manufacture: %d\r\n",YEAR_AND_WEEK_OF_MANUFACTURE.Week_Of_Manufacture);
	Text+=string;
	
	sprintf_s(string,256,"[17],Year of Manufacture: %d\r\n",(YEAR_AND_WEEK_OF_MANUFACTURE.Year_Of_Manufacture+1990));
	Text+=string;
	free(string);
}

void EDID_BaseBlockParser::parseEDID_Version_And_Revision(_EDID_VERSION_AND_REVISION EDID_VERSION_AND_REVISION)
{
	//EDID Version and Revision
	
	CHAR *string=(CHAR *)malloc(256);
	
	sprintf_s(string,256,"[18],EDID Version: %d\r\n",EDID_VERSION_AND_REVISION.Edid_Version);
	Text+=string;
	
	sprintf_s(string,256,"[19],EDID Revision: %d\r\n",EDID_VERSION_AND_REVISION.Edid_Revision);
	Text+=string;
	free(string);
}

void EDID_BaseBlockParser::parseBasicDisplayParameters(_BASIC_DISPLAY_PARAMETERS BASIC_DISPLAY_PARAMETERS)
{
	//Basic Display Parameters
	
	Text+="[20-24],Display Parameters\r\n";
	
	CHAR *string=(CHAR *)malloc(256);
	
	//First Byte, Video Input Definition
	parseVideoInputDefinition(BASIC_DISPLAY_PARAMETERS.VIDEO_INPUT_DEFN);
	
	//Horizontal Image Size
	sprintf_s(string,256,"\tMaximum Horizontal Image Size: %d\r\n",BASIC_DISPLAY_PARAMETERS.MAX_HORIZONTAL_SIZE);
	Text+=string;
	
	//Vertical Image Size
	sprintf_s(string,256,"\tMaximum Vertical Image Size: %d\r\n",BASIC_DISPLAY_PARAMETERS.MAX_VERTICAL_SIZE);
	Text+=string;
	
	//Display Gamma
	FLOAT gamma=BASIC_DISPLAY_PARAMETERS.DISPLAY_GAMMA;
	gamma+=100;
	gamma/=100;
	
	sprintf_s(string,256,"\tDisplay Gamma Value: %f\r\n",gamma);
	Text+=string;
	
	//Power Management Features
	parsePowerMgmtFeatures(BASIC_DISPLAY_PARAMETERS.DISPLAY_FEATURES_SUPPORT);
	free(string);
}

void EDID_BaseBlockParser::parseVideoInputDefinition(_VIDEO_INPUT_DEFN VIDEO_INPUT_DEFINITION)
{
	
	//Check if Display is Analog or Digital
	if(VIDEO_INPUT_DEFINITION.Analog_Digital==0)
	{
		Text+="\tAnalog\r\n";
		
		//Check Signal Level Standard
		if(VIDEO_INPUT_DEFINITION.signal_level_standard==0)
		{
			Text+="\t0.7,0.3\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION.signal_level_standard==1)
		{
			Text+="\t0.714,0.286\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION.signal_level_standard==2)
		{
			Text+="\t1.0,0.4\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION.signal_level_standard==3)
		{
			Text+="\t0.7,0.0\r\n";
		}
		
		//Check if it expects blank-black setup
		if(VIDEO_INPUT_DEFINITION.setup==1)
		{
			Text+="\tDisplay expects Blank-Black Setup\r\n";
		}
		
		//Check if it supports Separate syncs
		if(VIDEO_INPUT_DEFINITION.sync_input_supported_3==1)
		{
			Text+="\tSeparate Syncs Supported\r\n";
		}
		
		//Check if it supports composite syncs
		if(VIDEO_INPUT_DEFINITION.sync_input_supported_2==1)
		{
			Text+="\tComposite Syncs Supported \r\n";
		}
		
		//Check if it supports Green Video Sync
		if(VIDEO_INPUT_DEFINITION.sync_input_supported_1==1)
		{
			Text+="\tGreen Video Syncs \r\n";
		}
		
		//Check if Serration is required
		if(VIDEO_INPUT_DEFINITION.sync_input_supported_0_DFP==1)
		{
			Text+="\tSerration of Vsync Pulse is required \r\n";
		}
		
	}
	//Check if its Digital
	else if(VIDEO_INPUT_DEFINITION.Analog_Digital==1)
	{
		Text+="\tDigital \r\n";
		
		//Check for Interface Compatibility
		if(VIDEO_INPUT_DEFINITION.sync_input_supported_0_DFP==1)
		{
			Text+="\tInterface is Signal Compatible with VESA DFP 1.x \r\n";
		}
	}
}


void EDID_BaseBlockParser::parsePowerMgmtFeatures(_DISPLAY_FEATURES_SUPPORT DISPLAY_FEATURES_SUPPORT)
{
	Text+="\tPower Management Inforamtion:\r\n";
	
	//Check for Standby support
	if(DISPLAY_FEATURES_SUPPORT.StandBy==1)
	{
		Text+="\t\tStand By Supported\r\n";
	}
	//Check for Suspend support
	if(DISPLAY_FEATURES_SUPPORT.Suspend==1)
	{
		Text+="\t\tSuspend Supported\r\n";
	}
	//Check for Active-Off support
	if(DISPLAY_FEATURES_SUPPORT.ActiveOff_VeryLowPower==1)
	{
		Text+="\t\tActive Off Or Very Low Power Supported\r\n";
	}
	//Get Display Type
	switch(DISPLAY_FEATURES_SUPPORT.display_type)
	{
	case 0:Text+="\t\tMonochrome Or Gray Scale Display\r\n";break;
	case 1:Text+="\t\tRGB Color Display\r\n";break;
	case 2:Text+="\t\tNon-RGB Color Display\r\n";break;
	case 3:Text+="\t\tUndefined\r\n";break;
	} 
	//Check for Default Color Space
	if(DISPLAY_FEATURES_SUPPORT.default_color_space==1)
	{
		Text+="\t\tDisplay Uses standard default Color Space\r\n";
	}
	//Check if Preferred Timing Mode is listed in the first Descriptor Block
	if(DISPLAY_FEATURES_SUPPORT.pref_timing_mode==1)
	{
		Text+="\t\tPreferred Timing Mode is Indicated in I Descriptor Block \r\n";
	}
	//Check if GTF is supported
	if(DISPLAY_FEATURES_SUPPORT.GTF_Supported)
	{
		Text+="\t\tDisplay Supports Default GTF \r\n";
	}
	else
	{
		Text+="\t\tDisplay Does Not Support GTF \r\n";
	}
}

void EDID_BaseBlockParser::parsechromaInfo(_CHROMA_INFO CHROMA_INFO)
{
	//Parsing of Chroma Info
	//10 bit information
	//Low Bits Contain Bits 1,0
	//High Bits Contain Bits 9-2
	//Actual value is less than 1
	
	INT redx=0;
	INT redy=0;
	INT greenx=0;
	INT greeny=0;
	INT bluex=0;
	INT bluey=0;
	INT whitex=0;
	INT whitey=0;
	
	CHAR temp;
	CHAR *string=(CHAR *)malloc(256);
	
	Text+="[25-34],Chroma Info\r\n";
	
	//Red X
	temp=CHROMA_INFO.low_redx;
	temp=temp&0x03;
	redx=CHROMA_INFO.high_redx;
	redx=redx<<2;
	redx=redx|temp;
	
	sprintf_s(string,256,"\tRed X: 0.%d\t",redx);
	Text+=string;
	
	//Red Y
	temp=CHROMA_INFO.low_redy;
	redy=CHROMA_INFO.high_redy;
	redy=redy<<2;
	redy=redy|temp;
	
	sprintf_s(string,256,"Red Y: 0.%d\r\n",redy);
	Text+=string;
	
	//Green X
	temp=CHROMA_INFO.low_greenx;
	greenx=CHROMA_INFO.high_greenx;
	greenx=greenx<<2;
	greenx=greenx|temp;
	
	sprintf_s(string,256,"\tGreen X: 0.%d\t",greenx);
	Text+=string;
	
	//Green Y
	temp=CHROMA_INFO.low_greeny;
	greeny=CHROMA_INFO.high_greeny;
	greeny=greeny<<2;
	greeny=greeny|temp;
	
	sprintf_s(string,256,"Green Y: 0.%d\r\n",greeny);
	Text+=string;
	
	//Blue X
	temp=CHROMA_INFO.low_bluex;
	bluex=CHROMA_INFO.high_bluex;
	bluex=bluex<<2;
	bluex=bluex|temp;
	
	sprintf_s(string,256,"\tBlue X: 0.%d\t",bluex);
	Text+=string;
	
	//Blue Y
	temp=CHROMA_INFO.low_bluey;
	bluey=CHROMA_INFO.high_bluey;
	bluey=bluey<<2;
	bluey=bluey|temp;
	
	sprintf_s(string,256,"Blue Y: 0.%d\r\n",bluey);
	Text+=string;
	
	//White X
	temp=CHROMA_INFO.low_whitex;
	whitex=CHROMA_INFO.high_whitex;
	whitex=whitex<<2;
	whitex=whitex|temp;
	
	sprintf_s(string,256,"\tWhite X: 0.%d\t",whitex);
	Text+=string;
	
	//White Y
	temp=CHROMA_INFO.low_whitey;
	whitey=CHROMA_INFO.high_whitey;
	whitey=whitey<<2;
	whitey=whitey|temp;
	
	sprintf_s(string,256,"White Y: 0.%d\r\n",whitey);
	Text+=string;
	free(string);
}

void EDID_BaseBlockParser::parseEstablishedTiming_i(_ESTABLISHED_TIMING_SECTION_I ESTABLISHED_TIMING_SECTION_I)
{
	//Check the Established Timing Modes I
	Text+="[35],Established Timing I\r\n\t";
	
	BYTE temp;
	memcpy(&temp,&ESTABLISHED_TIMING_SECTION_I,1);
	if(temp==0x00)Text+="None\r\n\t";


	if(ESTABLISHED_TIMING_SECTION_I.bit7==1)Text+="720x400@70 Hz, IBM VGA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit6==1)Text+="720x400@88 Hz, IBM XGA 2\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit5==1)Text+="640x480@60 Hz, IBM VGA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit4==1)Text+="640x480@67 Hz, Apple Mac II\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit3==1)Text+="640x480@72 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit2==1)Text+="640x480@75 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit1==1)Text+="800x600@56 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_I.bit0==1)Text+="800x600@60 Hz, VESA\r\n\t";
	
	Text+="\r\n";
}

void EDID_BaseBlockParser::parseEstablishedTiming_ii(_ESTABLISHED_TIMING_SECTION_II ESTABLISHED_TIMING_SECTION_II)
{
	//Check the Established Timing Modes II
	Text+="[36],Established Timing II\r\n\t";

	BYTE temp;
	memcpy(&temp,&ESTABLISHED_TIMING_SECTION_II,1);
	if(temp==0x00)Text+="None\r\n\t";

	if(ESTABLISHED_TIMING_SECTION_II.bit7==1)Text+="800x600@72 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit6==1)Text+="800x600@75 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit5==1)Text+="832x624@75 Hz, Apple Mac II\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit4==1)Text+="1024x768@87 Hz, IBM \r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit3==1)Text+="1024x768@60 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit2==1)Text+="1024x768@70 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit1==1)Text+="1024x768@75 Hz, VESA\r\n\t";
	if(ESTABLISHED_TIMING_SECTION_II.bit0==1)Text+="1280x1024@75 Hz, VESA\r\n";
	
	Text+="\r\n";
}

void EDID_BaseBlockParser::parseManufacturers_Reserved_timing(_MANUFACTURERS_RESERVED_TIMING_SECTION MANUFACTURERS_RESERVED_TIMING_SECTION)
{
	//Check if any Mfr. Reserved timing supported
	Text+="[37],Manufacturers Reserved Timing Section\r\n";
	
	if(MANUFACTURERS_RESERVED_TIMING_SECTION.bit7==1)
	{
		Text+="\t1152x870 @ 75 Hz, Apple Mac II\r\n";
	}
	else
	{
		Text+="\t Not Used!\r\n";
	}
}	

void EDID_BaseBlockParser::parseStandard_timing_identification(_STANDARD_TIMING_IDENTIFICATION STANDARD_TIMING_IDENTIFICATION,BOOLEAN standard)
{
	//Parsing the Standard Timing Identification
	if(standard){
		Text+="[38-53],Standard Timing Identification\r\n";
	}
	else
	{
		Text+="Standard Timing Identification\r\n";
	}
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION1);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION2);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION3);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION4);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION5);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION6);
	if(standard)
	{
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION7);
	parseStandard_timing_identification_resolution(STANDARD_TIMING_IDENTIFICATION.RESOLUTION8);
	}
}

void EDID_BaseBlockParser::parseStandard_timing_identification_resolution(_STANDARD_TIMING_IDENTIFICATION_RESOLUTION STANDARD_TIMING_IDENTIFICATION_RESOLUTION)
{
	
	//This Functions contains the actual formula for translation
	//Horizontal Resoultion is given, actual value * 8 + 248
	//Aspect Ratio is given, it could be any of the 4 values.
	//Vertical Resolution is calculated from Horizontal Resolution and Aspect Ratio
	//Vertical Frequency is given, actual value + 60.
	
	
	INT hor_res=0;
	INT ver_res=0;
	INT ver_freq=0;
	CHAR *string=(CHAR *)malloc(256);

	BYTE TEMP[2];

	memcpy(TEMP,&STANDARD_TIMING_IDENTIFICATION_RESOLUTION,2);

	if(!(TEMP[0]==0x01 && TEMP[1]==0x01))
	{
	//Find the Horizotal and Vertical Resolution using the Aspect Ratio
	
		hor_res=(STANDARD_TIMING_IDENTIFICATION_RESOLUTION.hor_res*8)+248;
		switch(STANDARD_TIMING_IDENTIFICATION_RESOLUTION.aspect_ratio)
		{
		case 0:ver_res=(hor_res * 10)/16;break;
		case 1:ver_res=(hor_res * 3)/4;break;
		case 2:ver_res=(hor_res * 4)/5;break;
		case 3:ver_res=(hor_res * 9)/16;break;				
		}
		
		//Vertical Freq. = Actual Value + 60
		ver_freq=(STANDARD_TIMING_IDENTIFICATION_RESOLUTION.ver_freq+60);	
		sprintf_s(string,256,"\t%dx%d @ %d\r\n\r\n",hor_res,ver_res,ver_freq);
		Text+=string;
	}
	free(string);
}	


void EDID_BaseBlockParser::checkDescriptorBlock(_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK)
{
	if(DESCRIPTOR_BLOCK.FLAGS[0]==0 && DESCRIPTOR_BLOCK.FLAGS[1]==0)
	{
		parsedescriptor_block(DESCRIPTOR_BLOCK);
	}
	else
	{
		//Copy the DTD block on to a DB and call the appropriate. function
		_DETAILED_TIMING_DESCRIPTOR_BLOCK DETAILED_TIMING_DESCRIPTOR_BLOCK;
		memcpy(&DETAILED_TIMING_DESCRIPTOR_BLOCK,&DESCRIPTOR_BLOCK,18);
		if(DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_LSB>0x00 && DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_MSB>0x00)
			parsedetailed_timing_descriptor(DETAILED_TIMING_DESCRIPTOR_BLOCK);
	}
}

void EDID_BaseBlockParser::parsedetailed_timing_descriptor(_DETAILED_TIMING_DESCRIPTOR_BLOCK DETAILED_TIMING_DESCRIPTOR_BLOCK)
{
	CHAR *string=(CHAR *)malloc(256);
	Text+="Detailed Timing Descriptor\r\n";
	
	//Pixel Clok Calculation
	//Actual Value /100 MHz
	
	INT clock=DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_MSB;
	clock=clock<<8;
	clock=clock|DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_LSB;
	sprintf_s(string,256,"\tPixel Clock:%f\r\n",((FLOAT)clock/100));
	Text+=string;
	
	//Horizontal Active
	INT hor_act=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_hor_active;
	hor_act=hor_act<<8;
	hor_act=hor_act|DETAILED_TIMING_DESCRIPTOR_BLOCK.low_hor_active;
	sprintf_s(string,256,"\tHorizontal Active:%d\r\n",hor_act);
	Text+=string;
	
	//Horizontal Blanking
	INT hor_blank=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_hor_blank;
	hor_blank=hor_blank<<8;
	hor_blank=hor_blank|DETAILED_TIMING_DESCRIPTOR_BLOCK.low_hor_blank;
	sprintf_s(string,256,"\tHorizontal Blanking:%d\r\n",hor_blank);
	Text+=string;
	
	//Vertical Active
	INT ver_act=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_vert_active;
	ver_act=ver_act<<8;
	ver_act=ver_act|DETAILED_TIMING_DESCRIPTOR_BLOCK.low_vert_active;
	sprintf_s(string,256,"\tVertical Active:%d\r\n",ver_act);
	Text+=string;
	
	//Vertical Blanking
	INT ver_blank=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_vert_blank;
	ver_blank=ver_blank<<8;
	ver_blank=ver_blank|DETAILED_TIMING_DESCRIPTOR_BLOCK.low_vert_blank;
	sprintf_s(string,256,"\tVertical Blanking:%d\r\n",ver_blank);
	Text+=string;
	
	//Horizontal Sync. Offset
	INT hor_sync_offset=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_hor_sync_offset;
	hor_sync_offset=hor_sync_offset<<8;
	hor_sync_offset|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_hor_sync_offset;
	sprintf_s(string,256,"\tHorizontal Sync Offset:%d\r\n",hor_sync_offset);
	Text+=string;
	
	//Horizontal Sync Pulse Width
	INT hor_sync_width=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_hor_sync_pulse_width;
	hor_sync_width=hor_sync_width<<8;
	hor_sync_width|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_hor_sync_pulse_width;
	sprintf_s(string,256,"\tHorizontal Sync Pulse Width:%d\r\n",hor_sync_width);
	Text+=string;
	
	//Vertical Sync. Offset
	INT ver_sync_offset=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_vert_sync_offset;
	ver_sync_offset=ver_sync_offset<<4;
	ver_sync_offset|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_vert_sync_offset;
	sprintf_s(string,256,"\tVertical Sync Offset:%d\r\n",ver_sync_offset);
	Text+=string;
	
	//Vertical Sync. Pulse Width
	INT ver_sync_width=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_vert_pulse_width;
	ver_sync_width=ver_sync_width<<4;
	ver_sync_width|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_vert_pulse_width;
	sprintf_s(string,256,"\tVertical Sync Pulse Width:%d\r\n",ver_sync_width);
	Text+=string;
	
	//Horizontal Image Size
	INT hor_image_size=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_horz_image_size;
	hor_image_size=hor_image_size<<8;
	hor_image_size|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_horz_image_size;
	sprintf_s(string,256,"\tHorizontal Image Size:%d\r\n",hor_image_size);
	Text+=string;
	
	//Vertical Image Size
	INT ver_image_size=DETAILED_TIMING_DESCRIPTOR_BLOCK.high_vert_image_size;
	ver_image_size=ver_image_size<<8;
	ver_image_size|=DETAILED_TIMING_DESCRIPTOR_BLOCK.low_vert_image_size;
	sprintf_s(string,256,"\tVertical Image Size:%d\r\n",ver_image_size);
	Text+=string;
	
	//Horizontal and Vertical Border
	sprintf_s(string,256,"\tHorizontal Border: %d\r\n",DETAILED_TIMING_DESCRIPTOR_BLOCK.horz_border);
	Text+=string;
	sprintf_s(string,256,"\tVertical Border: %d\r\n",DETAILED_TIMING_DESCRIPTOR_BLOCK.vert_border);
	Text+=string;
	
	//Interlaced
	if(DETAILED_TIMING_DESCRIPTOR_BLOCK.interlaced==1)
	{
		Text+="\tInterlaced \r\n";
	}
	else
	{
		Text+="\tNon-Interlaced \r\n";
	}
	
	
	//Check the Stereo Modes
	INT stereo_mode=DETAILED_TIMING_DESCRIPTOR_BLOCK.stereo_mode;
	stereo_mode=stereo_mode<<1;
	stereo_mode|=DETAILED_TIMING_DESCRIPTOR_BLOCK.stereo_mode_bit;
	
	switch(stereo_mode)
	{
	case 0:Text+="\tNormal Display,No Stereo\r\n";break;
	case 1:Text+="\tNormal Display,No Stereo\r\n";break;
	case 2:Text+="\tField Sequential Stereo,right image when stereo sync=1\r\n";
	case 3:Text+="\t2-way Interleaved Stereo,right image on even lines\r\n";
	case 4:Text+="\tField Sequential Stereo,left image when stereo sync=1\r\n";
	case 5:Text+="\t2-way Interleaved Stereo,left image on even lines\r\n";
	case 6:Text+="\t4-Way Interleaved Stereo\r\n";
	case 7:Text+="\tSide-by-Side Interleaved Stereo\r\n";
	}
	//-------------------
	//Analog Composite
	//-------------------
	//0000 - bit4-0 bit3-0 bit2-0 bit1-0 (sync_signal_desc - 00 serration_bit - 0 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tAnalog Composite\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tSync On Green Signal only \r\n";
	}
	
	//0001 - bit4-0 bit3-0 bit2-0 bit1-1 (sync_signal_desc - 00 serration_bit - 0 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tAnalog Composite\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tSync On all three (RGB) video signals \r\n";
	}
	

	//0010 - bit4-0 bit3-0 bit2-1 bit1-0 (sync_signal_desc - 00 serration_bit - 1 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tAnalog Composite\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tSync On Green Signal only\r\n";
	}

	//0011 -  bit4-0 bit3-0 bit2-1 bit1-1 (sync_signal_desc - 00 serration_bit - 1 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tAnalog Composite\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tSync On all three (RGB) video signals\r\n";
	}
	//--------------------------------
	//Bipolar Analog Composite Sync
	//---------------------------------
	//0100 - bit4-0 bit3-1 bit2-0 bit1-0 (sync_signal_desc - 01 serration_bit - 0 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tBipolar Analog Composite Sync\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tSync On Green Signal only\r\n";
	}

	//0101 - bit4-0 bit3-1 bit2-0 bit1-1 (sync_signal_desc - 01 serration_bit - 0 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tBipolar Analog Composite Sync\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tSync On all three (RGB) video signals\r\n";
	}


	//0110 - bit4-0 bit3-1 bit2-1 bit1-0 (sync_signal_desc - 01 serration_bit - 1 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tBipolar Analog Composite Sync\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tSync On Green Signal only\r\n";
	}

	//0111 - bit4-0 bit3-1 bit2-1 bit1-1 (sync_signal_desc - 01 serration_bit - 1 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tBipolar Analog Composite Sync\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tSync On all three (RGB) video signals\r\n";
	}
	//--------------------------------
	//Digital Composite Sync
	//--------------------------------
	//1000 - bit4-1 bit3-0 bit2-0 bit1-0 (sync_signal_desc - 10 serration_bit - 0 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==2) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tDigital Composite Sync\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tHorizontal Sync is Negative -ve (outside of V-sync)\r\n";
	}

	//1001 - bit4-1 bit3-0 bit2-0 bit1-1 (sync_signal_desc - 10 serration_bit - 0 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==2) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tDigital Composite Sync\r\n";
		Text+="\tWithout Serrations\r\n";
		Text+="\tHorizontal Sync is Positive +ve (outside of V-sync)\r\n";
	}

	//1010 - bit4-1 bit3-0 bit2-1 bit1-0 (sync_signal_desc - 10 serration_bit - 1 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==2) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tDigital Composite Sync\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tHorizontal Sync is Negative -ve (outside of V-sync)\r\n";
	}

	//1011 - bit4-1 bit3-0 bit2-1 bit1-1 (sync_signal_desc - 10 serration_bit - 1 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==2) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tDigital Composite Sync\r\n";
		Text+="\tWith Serrations (H-sync during V-sync)\r\n";
		Text+="\tHorizontal Sync is Positive +ve(outside of V-sync)\r\n";
	}
	//----------------------
	//Digital Separate 
	//----------------------
	//1100 - bit4-1 bit3-1 bit2-0 bit1-0 (sync_signal_desc - 11 serration_bit - 0 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==3) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tDigital Separate Sync\r\n";
		Text+="\tVertical Sync is Negative - ve\r\n";
		Text+="\tHorizontal Sync is Negative - ve\r\n";
	}

	//1101 - bit4-1 bit3-1 bit2-0 bit1-1 (sync_signal_desc - 11 serration_bit - 0 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==3) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==0) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tDigital Separate Sync\r\n";
		Text+="\tVertical Sync is Negative - ve\r\n";
		Text+="\tHorizontal Sync is Positive + ve\r\n";
	}

	//1110 - bit4-1 bit3-1 bit2-1 bit1-0 (sync_signal_desc - 11 serration_bit - 1 polarity -  0)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==3) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==0))
	{
		Text+="\tDigital Separate Sync\r\n";
		Text+="\tVertical Sync is Positive +ve\r\n";
		Text+="\tHorizontal Sync is Negative -ve\r\n";
	}
	//1111 - bit4-1 bit3-1 bit2-1 bit1-1 (sync_signal_desc - 11 serration_bit - 1 polarity -  1)
	if((DETAILED_TIMING_DESCRIPTOR_BLOCK.sync_signal_desc==3) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.serration_bit==1) && (DETAILED_TIMING_DESCRIPTOR_BLOCK.polarity==1))
	{
		Text+="\tDigital Separate Sync\r\n";
		Text+="\tVertical Sync is Positive +ve\r\n";
		Text+="\tHorizontal Sync is Positive +ve\r\n";
	}

	//Below block of code is added to show DTD in terms of X x Y @ RR format (- Mainly for easy understanding of DTD for end users) 
	//***********************************************
	if(DETAILED_TIMING_DESCRIPTOR_BLOCK.interlaced==1)
	{
		if(clock !=0)

		{
			Text+="\t-----------------------------\r\n";
			sprintf_s(string,256,"\tResolution:%d x %di @ %dHz \r\n",hor_act,(ver_act *2),((clock*10000) / ((hor_act + hor_blank)* (ver_act + ver_blank))));
			Text+=string;
			Text+="\t------------------------------\r\n";
			Text+="\r\n";
		}
		
	}
	else
	{
		if(clock !=0)
		{
			Text+="\t------------------------------\r\n";
			sprintf_s(string,256,"\tResolution:%d x %dp @ %dHz \r\n",hor_act,ver_act,((clock*10000) / ((hor_act + hor_blank)* (ver_act + ver_blank))));
			Text+=string;
			Text+="\t------------------------------\n";
			Text+="\r\n";
		}
	}
	//***********************************************
	free(string);
}


void EDID_BaseBlockParser::parsedescriptor_block(_DESCRIPTOR_BLOCK DESCRIPTOR_BLOCK)
{
	if(DESCRIPTOR_BLOCK.FLAGS[0]==0x00 && DESCRIPTOR_BLOCK.FLAGS[1]==0x00)
	{
		//Text+="Descriptor Block Contains Data\r\n";
	}
	if(DESCRIPTOR_BLOCK.START_FLAG==0)
	{
		//Text+="Descriptor Block Starts here\r\n";
	}
	
	//Check the Data Type Tag and call the appropriate function
	
	switch(DESCRIPTOR_BLOCK.DATA_TYPE_TAG)
	{
	case 0xFF:parseSerialNumber(DESCRIPTOR_BLOCK.MON_DESC_DATA);break;
	case 0xFE:parseASCIIString(DESCRIPTOR_BLOCK.MON_DESC_DATA);break;
	case 0xFD:parseMonitor_range_limits(DESCRIPTOR_BLOCK.MON_DESC_DATA);break;
	case 0xFC:parseMonitorName(DESCRIPTOR_BLOCK.MON_DESC_DATA);break;
	case 0xFB:parseColor_Point_info(DESCRIPTOR_BLOCK.MON_DESC_DATA);break;
	case 0xFA:_STANDARD_TIMING_IDENTIFICATION STANDARD_TIMING_IDENTIFICATION;
		memcpy(&STANDARD_TIMING_IDENTIFICATION,DESCRIPTOR_BLOCK.MON_DESC_DATA,13);
		parseStandard_timing_identification(STANDARD_TIMING_IDENTIFICATION,FALSE);
		break;
	}
	
	if(DESCRIPTOR_BLOCK.END_FLAG==0)
	{
		//Text+="Descriptor Block Ends here\r\n";
	}
	Text+="\r\n";
}

void EDID_BaseBlockParser::parseSerialNumber(CHAR *data)
{
	//Parse Serial No, ends with 0A, if not 13 bytes in length
	Text+="\tMonitor Serial No:";
	CHAR *value=(CHAR *)malloc(256);
	INT i=0;
	
	for(i=0;i<13;i++)
	{
		if(data[i]!=0x0A)
		{
			value[i]=data[i];
		}
		else
		{
			break;
		}
	}
	
	value[i]='\0';
	Text+=value;
	Text+="\r\n";
	free(value);
}

void EDID_BaseBlockParser::parseASCIIString(CHAR *data)
{
	//Parse ASCII string,100, ends with 0A, if not 13 bytes in length
	
	Text+="\tMonitor ASCII String:";
	CHAR *value=(CHAR *)malloc(256);
	INT i=0;
	
	for(i=0;i<13;i++)
	{
		if(data[i]!=0x0A)
		{
			value[i]=data[i];
		}
		else
		{
			break;
		}
	}
	
	value[i]='\0';
	Text+=value;
	Text+="\r\n";
	free(value);
}

void EDID_BaseBlockParser::parseMonitor_range_limits(CHAR *data)
{
	//Parse Monitor Range Limits
	
	_MONITOR_RANGE_LIMITS *MONITOR_RANGE_LIMITS;
	MONITOR_RANGE_LIMITS=(_MONITOR_RANGE_LIMITS *)malloc(sizeof(_MONITOR_RANGE_LIMITS));
	memcpy(MONITOR_RANGE_LIMITS,data,sizeof(_MONITOR_RANGE_LIMITS));
	
	Text+="Monitor Range Limits\r\n";
	
	CHAR *string=(CHAR *)malloc(256);
	
	//Minimum Vertical Rate
	sprintf_s(string,256,"\tMin. Vertical Rate:%d\r\n",MONITOR_RANGE_LIMITS->min_vert_rate);
	Text+=string;
	//Maximum Vertical Rate
	sprintf_s(string,256,"\tMax. Vertical Rate:%d\r\n",MONITOR_RANGE_LIMITS->max_vert_rate);
	Text+=string;
	//Minimum Horizontal Rate
	sprintf_s(string,256,"\tMin. Horizontal Rate:%d\r\n",MONITOR_RANGE_LIMITS->min_horz_rate);
	Text+=string;
	//Maximum Horizontal Rate
	sprintf_s(string,256,"\tMax. Horizontal Rate:%d\r\n",MONITOR_RANGE_LIMITS->max_horz_rate);
	Text+=string;
	//Maximum Pixel Clock
	sprintf_s(string,256,"\tMax. Pixel Clock:%d MHz\r\n",(MONITOR_RANGE_LIMITS->max_pixel_clock*10));
	Text+=string;
	
	//Check if Timing Formula is Supported
	if(MONITOR_RANGE_LIMITS->timing_formula_support==0x00)
	{
		Text+="\tNo Secondary Timing Formula Support\r\n";
	}
	else if(MONITOR_RANGE_LIMITS->timing_formula_support==0x02)
	{
		sprintf_s(string,256,"\tStart Frequency, %d Hz\r\n",(MONITOR_RANGE_LIMITS->start_freq/2));
		Text+=string;
		
		sprintf_s(string,256,"\tC, %d \r\n",(MONITOR_RANGE_LIMITS->byte_C*2));
		Text+=string;
		
		INT m=MONITOR_RANGE_LIMITS->MSB_M;
		m=m<<8;
		m=m|MONITOR_RANGE_LIMITS->LSB_M;
		sprintf_s(string,256,"\tM, %d \r\n",m);
		Text+=string;
		
		sprintf_s(string,256,"\tK, %d \r\n",MONITOR_RANGE_LIMITS->byte_K);
		Text+=string;
		
		sprintf_s(string,256,"\tJ, %d \r\n",(MONITOR_RANGE_LIMITS->byte_J*2));
		Text+=string;
	}	
	
	free(MONITOR_RANGE_LIMITS);
	free(string);
}

void EDID_BaseBlockParser::parseMonitorName(CHAR *data)
{	
	//Parse Monitor Name, ends with 0A, if not 13 bytes in length
	
	Text+="\tMonitor Name:";
	CHAR *value=(CHAR *)malloc(256);
	INT i=0;
	
	for(i=0;i<13;i++)
	{
		if(data[i]!=0x0A)
		{
			value[i]=data[i];
		}
		else
		{
			break;
		}
	}
	
	value[i]='\0';
	Text+=value;
	Text+="\r\n";
	free(value);
}

void EDID_BaseBlockParser::parseColor_Point_info(CHAR *data)
{
	//Parse Color Point Info
	
	_COLOR_POINT *COLOR_POINT;
	COLOR_POINT=(_COLOR_POINT *)malloc(sizeof(_COLOR_POINT));
	memcpy(COLOR_POINT,data,sizeof(_COLOR_POINT));
	
	
	Text+="Color Point Info\r\n";
	CHAR *string=(CHAR *)malloc(256);
	
	sprintf_s(string,256,"White Point Index Number:%d\r\n",COLOR_POINT->white_point_index_number_1);
	Text+=string;
	
	sprintf_s(string,256,"White_X:%d",COLOR_POINT->white_x_1);
	Text+=string;
	
	sprintf_s(string,256,"White_Y:%d",COLOR_POINT->white_y_1);
	Text+=string;
	
	sprintf_s(string,256,"White_Gamma:%d",((COLOR_POINT->white_gamma_1*100)-100));
	Text+=string;
	
	sprintf_s(string,256,"White Point Index Number:%d\r\n",COLOR_POINT->white_point_index_number_2);
	Text+=string;
	
	sprintf_s(string,256,"White_X:%d",COLOR_POINT->white_x_2);
	Text+=string;
	
	sprintf_s(string,256,"White_Y:%d",COLOR_POINT->white_y_2);
	Text+=string;
	
	sprintf_s(string,256,"White_Gamma:%d",((COLOR_POINT->white_gamma_2*100)-100));
	Text+=string;
	
	free(COLOR_POINT);
	free(string);
}

void EDID_BaseBlockParser::checkExtension(BYTE flag)
{
	//Check Extension Flag
	Text+="[126],Extension Flag:";
	CString temp;
	temp.Format("%d\r\n",(flag));
	Text+=temp;

	temp.Format("\tEDID has %d Extension(s)\r\n",(flag));
	Text+=temp;
//	NumExt = flag;
}

void EDID_BaseBlockParser::checkSum()
{
	
	//Do the Checksum
	//The sum of the 128 bytes should be 0.
	
	BYTE sum=0;
	
	CString test;
	
	for(INT i=0;i<128;i++)
	{
		sum+=edidbuffer[i];
	}
	
	test.Format("%d",sum);
	
	Text+="[127],CheckSum\r\n";
	
	if(sum==0)
	{
		Text+="\tCheckSum OK!\r\n";
	}
	else
	{
		Text+="\tCheckSum Failed!\r\n";
	}	
}


//==========================================Methods specific to CEA Extension=============================
//====================================================================================================

void CEAExtensionParser::parseCEAExtension(CEA_EXTENSION CEA_EXT,CListCtrl *Ptr)
{

	CString Temp;
	INT index=0;
	CurrentByteNo = 0;	// Contains the no. of last Byte parsed.

	INT i = 0;
	
	ListBox=Ptr;
	
	/*if(CEA_EXT.REVISION!=0x03)
	{
		return;
	}*/

	index=ListBox->InsertItem(++listcount,"");
	ListBox->SetItemText(index,1,"");
	ListBox->SetItemText(index,2,"");
	
	index=ListBox->InsertItem(++listcount,"****");
	Temp.Format("Block No.: %d", CurrentExtNo);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CEA EXTENSION BLOCK");
	
	Text+="\r\n\r\n**************************************\r\n";
	Temp.Format("Block No.: %d     CEA Extension Block\r\n", CurrentExtNo);
	Text+=Temp;
	Text+="**************************************\r\n";		
	
	
	//**************************************************
	//Definintion of Various Blocks inside CEA Extension
	//**************************************************
	
	_CEA_SHORT_VIDEO_DESCRIPTOR_BLOCK SHORT_VIDEO_DESC_BLOCK;
	_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_UNCOMPRESSED AUDIO_DESC_BLOCK;
	_CEA_SPEAKER_ALLOCATION_DATA_BLOCK SPEAKER_ALLOC_BLOCK;
	_CEA_VENDOR_SPECIFIC_DATA_BLOCK_14 VENDOR_BLOCK;
	_DETAILED_TIMING_DESCRIPTOR_BLOCK DTD;
	_CEA_VIDEO_CAPABILITY_BLOCK VIDEO_CAP_BLOCK;
	_CEA_COLORIMETRY_DATA_BLOCK COLORI_DATA_BLOCK;
	
	
	//Parsing the Tag and EDID Revision Number
	parseTagRevision(CEA_EXT);
		
	//Gettting the Byte Offset Number for them First DTD
	d=CEA_EXT.DTD_OFFSET;
	
	
	//Populating Byte Details for DTD offset
	Temp.Format("[%d]Byte Offset for DTD: %d",++CurrentByteNo, d);
	Text+=Temp;
	Text+="\r\n";

	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",d);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Byte Offset for DTD");
	
	if(d==0)
	{
		return;
	}
	
	
	//Parsing the Native Format Structure
	parseNativeFormat(CEA_EXT);
	

	//Getting the No. of DTDs provided in the CEA Extension Block
	n1=CEA_EXT.NATIVE_FORMATS.NO_DTD;
	
	//Populating Byte Details for Byte 3 
	memcpy(&byteTemp,&CEA_EXT.NATIVE_FORMATS,1);
	
	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",byteTemp);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"No. of DTDs in CEA Block");
	
	
	//Parsing the Data Block	
	//******************************************
	//VIDEO DESCRIPTOR BLOCKS
	//******************************************
	
	//Get the Length of Video Block
	byteCount=0;
	
	_GENERAL_TAG_FORMAT BLOCK_TAG;

	k=CurrentByteNo;

	while (k<(d-1))
	{
	
	k++;
	byteTemp=CEA_EXT.DATA_BLOCK[byteCount++];
	memcpy(&BLOCK_TAG,&byteTemp,1);
	tag_code=CEA_Data_Block_Tag_Codes(BLOCK_TAG.TAG_CODE);//Typecast - CEA Data Block Tag Codes
	L=BLOCK_TAG.LENGTH_OF_BLOCK;
	
	if (tag_code==Video_Data_Block)
	{
	//Populating Byte Details for Video Descriptor Block
	Temp.Format("%d",++CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",byteTemp);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Video Descriptor Block Tag");
	
	Text+="\r\n";
	Temp.Format("[%d]Video Descriptor Block Tag 0x%02X",CurrentByteNo, byteTemp);
	Text+=Temp;
	Text+="\r\n";


	Text+="\n\tVideo Descriptor Blocks\r\n";
	
	Text+="\n\t     Video code\tHorizontal\tVertical\ti/p\tVertical Freq\tAspect Ratio\tWhere Defined\tRemark\r\n";
	
	//parse the Video Descriptor Blocks
	
	for(i=byteCount;i<(byteCount+L);i++)
	{
		++k;
		CString Temp;
		byteTemp=CEA_EXT.DATA_BLOCK[i];
		memcpy(&SHORT_VIDEO_DESC_BLOCK,(&byteTemp),1);
		parseVideoDescBlock(SHORT_VIDEO_DESC_BLOCK);

        // save the VIC in array for later info pickup
        ucSupportedVIC[i-byteCount] = SHORT_VIDEO_DESC_BLOCK.VIDEO_ID_CODE;
	}
	
	byteCount=i;	
	}
	//*********************************************
	//AUDIO DESCRIPTOR BLOCKS 
	//*********************************************
	
	//Get the Audio Block Tag
	
	if(tag_code==Audio_Data_Block)
	{
	//Populating Byte Details for Audio Descriptor Block

	//Adding the Byte Offset in Text Box
	Temp.Format("\r\n[%d]",++CurrentByteNo);
	Text+=Temp;

	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	byteTemp=0;
	memcpy(&byteTemp,&BLOCK_TAG,1);
	Temp.Format("0x%02X",byteTemp);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Audio Descriptor Block Tag");
	

	//Adding the Tag in Text Box
	Text+="Audio Descriptor Block Tag ";
	Temp.Format("0x%02X",byteTemp);
	Text+=Temp;
	Text+="\r\n";


	
	//parse the Audio Descriptor Blocks
	
	for(i=byteCount;i<(byteCount+L);i+=3)
	{
		BYTE bArray[3];
 		for(INT j=0;j<3;j++)
		{
			++k;
			bArray[j]=CEA_EXT.DATA_BLOCK[i+j];
		}
		
		memcpy(&AUDIO_DESC_BLOCK,bArray,3);
		if(AUDIO_DESC_BLOCK.AUDIO_FORMAT_CODE==1)
		{
			_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_UNCOMPRESSED AUDIO_BLOCK;
			memcpy(&AUDIO_BLOCK,&AUDIO_DESC_BLOCK,3);
			parseAudioDescBlockUncompressed(AUDIO_BLOCK);
		}
		else
		{
			_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_COMPRESSED AUDIO_BLOCK;
			memcpy(&AUDIO_BLOCK,&AUDIO_DESC_BLOCK,3);
			parseAudioDescBlockCompressed(AUDIO_BLOCK);
		}
	}
	
	byteCount=i;
	}
	
	//*********************************************
	//SPEAKER ALLOCATION BLOCK
	//*********************************************
	
	//Adding the Byte Offset in Text Box
	if(tag_code==Speaker_Allocation_Data_Block)
	{
	Temp.Format("\r\n[%d]",++CurrentByteNo);
	Text+=Temp;


	//Populating Byte Details for Speaker Allocation Block
	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	memcpy(&byteTemp,&BLOCK_TAG,1);
	Temp.Format("0x%02X",byteTemp);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Speaker Allocation Block Tag");
	
	//Adding the Data in Text Box	
	Text+="Speaker Descriptor Block Tag ";
	Temp.Format("0x%02X",byteTemp);
	Text+=Temp;
	Text+="\r\n";
		
	for(i=byteCount;i<(byteCount+L);i+=3)
	{
		BYTE bArray[3];
		for(INT j=0;j<3;j++)
		{
			++k;
			bArray[j]=CEA_EXT.DATA_BLOCK[i+j];
		}
		
		memcpy(&SPEAKER_ALLOC_BLOCK,bArray,3);
		
		parseSpeakerAllocBlock(SPEAKER_ALLOC_BLOCK);
	}
	
	byteCount=i;
	}
		//*********************************************
	//VENDOR BLOCK
	//*********************************************

	//Adding the Byte Offset in Text Box
	if(tag_code==Vendor_Specific_Data_Block)
	{
	Temp.Format("\r\n[%d]",++CurrentByteNo);
	Text+=Temp;

	//Populating Byte Details for Vendor Specific Data Block
	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	memcpy(&byteTemp,&BLOCK_TAG,1);
	Temp.Format("0x%02X",byteTemp);
	
	//Adding the Data in Text Box	
	Text+="Vendor Specific Descriptor Block Tag ";
	Temp.Format("0x%02X",byteTemp);
	Text+=Temp;
	Text+="\r\n";


	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Vendor Block Tag");
	
	//Copy Vendor Block and Parse it
	
	Temp.Format("L=%d",L);
	//MessageBox(Temp);
	
	BYTE *bArray=new BYTE[L];
	for(INT j=0;j<L;j++)
	{
		++k;
		bArray[j]=CEA_EXT.DATA_BLOCK[j+byteCount];
	}
	memcpy(&VENDOR_BLOCK,bArray,L);
	parseVendorSpecificBlock(VENDOR_BLOCK);
	byteCount=byteCount+L;
	}

	//********************************************
	//EXTENDED TAG FORMAT
	//********************************************
	if (tag_code==Extended_Tag)
	{
		Temp.Format("\r\n[%d]",++CurrentByteNo);
		Text+=Temp;

		//Populating Byte Details for Extended Block Tag
		Temp.Format("%d",CurrentByteNo);
		index=ListBox->InsertItem(++listcount,Temp);
		memcpy(&byteTemp,&BLOCK_TAG,1);
		Temp.Format("0x%02X",byteTemp);
			
		//Adding the Data in Text Box	
		Text+="Extended Tag Code";
		Temp.Format("0x%02X",byteTemp);
		Text+=Temp;
		Text+="\r\n";
	
		ListBox->SetItemText(index,1,Temp);
		ListBox->SetItemText(index,2,"Extended Block Tag");


		
	    //**********************************  
		//Video Capability Block
		//**********************************
		if(CEA_EXT.DATA_BLOCK[byteCount]==0)
		{
			
			// L is reduced by 1, Since L accounts for Video Capability Block tag + pay load 
			L-=1;			
			
			k++;
			Temp.Format("\r\n[%d]",++CurrentByteNo);
			Text+=Temp;
	
			//Populating Byte Details for type of Extended Block
			Temp.Format("%d",CurrentByteNo);
			index=ListBox->InsertItem(++listcount,Temp);
			memcpy(&byteTemp,&(CEA_EXT.DATA_BLOCK[byteCount]),1);
			Temp.Format("0x%02X",byteTemp);
	
			//Adding the Data in Text Box	
			Text+="Video Capability Block Tag";
			Temp.Format("0x%02X",byteTemp);
			Text+=Temp;
			Text+="\r\n";

			ListBox->SetItemText(index,1,Temp);
			ListBox->SetItemText(index,2,"Video Capability Block Tag");
			i=byteCount++;
			BYTE *bArray1=new BYTE[L];
			
			for (i=0;i<L;i++)
			{
				++k;
				bArray1[i]=CEA_EXT.DATA_BLOCK[i+byteCount];
			}
			
			memcpy(&VIDEO_CAP_BLOCK,bArray1,L);
			parseVideoCapabilityBlock(VIDEO_CAP_BLOCK);
			byteCount=byteCount+L;
			CurrentByteNo =k;
		}

	
		//**********************************  
		//Video Capability Block
		//**********************************
		if(CEA_EXT.DATA_BLOCK[byteCount]==5)
		{
			// L is reduced by 1, Since L accounts for Colorimetry data block tag + pay load 
			L-=1;			
			
			k++;
			Temp.Format("\r\n[%d]",++CurrentByteNo);
			Text+=Temp;

			//Populating Byte Details for type of Extended Block
			Temp.Format("%d",CurrentByteNo);
			index=ListBox->InsertItem(++listcount,Temp);
			memcpy(&byteTemp,&(CEA_EXT.DATA_BLOCK[byteCount]),1);
			Temp.Format("0x%02X",byteTemp);
	
			//Adding the Data in Text Box	
			Text+="Colorimetry Data Block Tag";
			Temp.Format("0x%02X",byteTemp);
			Text+=Temp;
			Text+="\r\n";
	
			ListBox->SetItemText(index,1,Temp);
			ListBox->SetItemText(index,2,"Colorimetry Data Block Tag");

			i=byteCount++;
			BYTE *bArray1=new BYTE[L];
			
			for (i=0;i<L;i++)
			{
				++k;
				bArray1[i]=CEA_EXT.DATA_BLOCK[i+byteCount];
			}
			
			memcpy(&COLORI_DATA_BLOCK,bArray1,L);
			parseColorimetryBlock(COLORI_DATA_BLOCK);
			byteCount=byteCount+L;
			CurrentByteNo =k;
			
		}

	}
}


	
	//********************************************
	//DETAILED TIMING DESCRIPTOR BLOCK
	//********************************************
	
	//parse the DTDs
	n=(128 - d) / sizeof(_DETAILED_TIMING_DESCRIPTOR_BLOCK);
	
	if(((n * sizeof(_DETAILED_TIMING_DESCRIPTOR_BLOCK)) + d) > 128)
	return;

	if(n1>n)
	{
		Text+="***********************************************\r\n\t";
		Text+="EDID CEA Extension Version 3 Format violated\r\n";
		Text+="***********************************************\r\n\t";
		Text+="\r\n\t";
	}
	INT n2=0;
	
	for(i=byteCount;i<(byteCount+(18*n));i+=18)
	{
		n2++;
		BYTE *bArray=new BYTE[18];
		for(INT j=0;j<18;j++)
		{
			bArray[j]=CEA_EXT.DATA_BLOCK[i+j];
		}
		INT cnt=0;
		BOOLEAN flag=FALSE;
		
		for(cnt=0;cnt<17;cnt++)
		{
			if(bArray[cnt]!=0x00)
			{
				flag=TRUE;
			}
		}
		
		if(flag==FALSE)
		{
			break;
		}
		
		
		memcpy(&DTD,bArray,18);
	
		CString DTD_Values;
		Temp.Format("%d-%d",++CurrentByteNo,CurrentByteNo+17);
		index=ListBox->InsertItem(++listcount,Temp);

		//Adding Byte offset to Text Data
		Temp.Format("[%d-%d]",CurrentByteNo,CurrentByteNo+17);
		Text+=Temp;

		CurrentByteNo+=17;
		
		for(INT c=0;c<17;c++)
		{
			Temp.Format("0x%02X,",bArray[c]);
			DTD_Values+=Temp;
		}
		ListBox->SetItemText(index,1,DTD_Values);
		
		ListBox->SetItemText(index,2,"Detailed Timing Descriptor Block");
		
		parsedetailed_timing_descriptor(DTD);
	}
	
	
	Temp.Format("%d-126",++CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp="";
	
	
	byteCount=i;
	if(n2>n1 && CEA_EXT.REVISION !=1)
	{
		Text+="***************************************************************************\r\n\t";
		Text+="Padding not done properly,parsing more DTD's than supplied by the EDID\r\n";
		Text+="***************************************************************************\r\n\t";
		Text+="\r\n\t";
	}
	if(n2<n1 && n1<=n)
	{
		Text+="********************************************************************\r\n\t";
		Text+="Parsing less DTD's than supplied by the EDID\r\n";
		Text+="********************************************************************\r\n\t";
		Text+="\r\n\t";
	}

	
	
	//******************************************
	//PADDING
	//******************************************
	
	for(INT c=byteCount;c<122;c++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",CEA_EXT.DATA_BLOCK[c]);
		Temp+=strTemp;
		Temp+=",";
	}
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Padding");
	
	//***************************
	//CHECK SUM
	//**************************
	
	Text+="[127]CheckSum\r\n\t";
	
	CEAcheckSum();
}


void CEAExtensionParser::parseNativeFormat(CEA_EXTENSION CEA_EXT)
{
	//INT n;
	CString Temp;
	if (CEA_EXT.REVISION ==3)

	{	Temp.Format("[%d]Monitor Support\r\n\t", ++CurrentByteNo);
		Text+=Temp;

		if(CEA_EXT.NATIVE_FORMATS.UNDERSCAN==1)
		{
			Text+="Monitor Supports Underscan\r\n\t";
		}
		if(CEA_EXT.NATIVE_FORMATS.AUDIO==1)
		{
			Text+="Monitor Supports Basic Audio\r\n\t";
		}
		if(CEA_EXT.NATIVE_FORMATS.YCbCr4==1)
		{
			Text+="Monitor Supports YCbCr 4:4:4 in addition to RGB\r\n\t";
		}
		if(CEA_EXT.NATIVE_FORMATS.YCbCr2==1)
		{
		Text+="Monitor Supports YCbCr 4:2:2 in addition to RGB\r\n\t";
		}

		n=CEA_EXT.NATIVE_FORMATS.NO_DTD;

		Temp.Format(" %d",n);
		Text+="No.of DTDs in CEA Extensions";
		Text+=Temp;
		Text+="\r\n";
	}

	if (CEA_EXT.REVISION ==1)

	{	Temp.Format("[%d] Reserved\r\n", ++CurrentByteNo);
		Text+=Temp;
	}

	
}

void CEAExtensionParser::parseTagRevision(CEA_EXTENSION CEA_EXT)
{
	CString Temp;
	INT index=0;
		
	if(CEA_EXT.TAG==CE_EXT_TAG)
	{
		//Temp.Format("[%d]Tag OK!\r\n", (CurrentExtNo-1)*128 + 127 + 1 );  // This way We can have contiguous numbering of Bytes.
		Text+="[0]Tag OK!\r\n";
	}
	else
	{
		MessageBox(NULL,"Extension Not Supported","Error",MB_OK);
		return;
	}
	
	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",CEA_EXT.TAG);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CEA Extension Tag");
	
	Temp.Format("%d",++CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",CEA_EXT.REVISION);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CEA Extension Revision");

	Temp.Format("[%d]CEA Extension Revision:%x",CurrentByteNo, CEA_EXT.REVISION);
	Text+=Temp+"\r\n";	
}


void CEAExtensionParser::parseVideoDescBlock(_CEA_SHORT_VIDEO_DESCRIPTOR_BLOCK VIDEO_BLOCK)
{
	INT index=0;
	CString Temp;
	
	//Video Descriptor Block 

	Temp.Format("[%d]",++CurrentByteNo);
	Text+=Temp;

	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	memcpy(&byteTemp,&VIDEO_BLOCK,1);
	Temp.Format("0x%02X,",byteTemp);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Video Descriptor Block");
	
	if(VIDEO_BLOCK.NATIVE==1)
	{
		Text+="\tNative\t";
	}
	else
	{
		Text+="\t\t";
	}
	BYTE CODE=VIDEO_BLOCK.VIDEO_ID_CODE;
	
	switch(CODE)
	{
	case 0:Text+="No Video Code Available\r\n";break;
	case 1:Text+="01\t640\t\t480\tp\t59.94/60Hz\t4:3\t\t861\t\tDefault Format\t";break;
	case 2:Text+="02\t720\t\t480\tp\t59.94/60Hz\t4:3\t\t861\t\tEDTV\t";break;
	case 3:Text+="03\t720\t\t480\tp\t59.94/60Hz\t16:9\t\t861\t\tEDTV\t";break;
	case 4:Text+="04\t1280\t\t720\tp\t59.94/60Hz\t16:9\t\t861\t\tHDTV\t";break;
	case 5:Text+="05\t1920\t\t1080\ti\t59.94/60Hz\t16:9\t\t861\t\tHDTV\t";break;
	case 6:Text+="06\t720(1440)\t480\ti\t59.94/60Hz\t4:3\t\t861 Optional\tDouble Clock for 720x480i\t";break;
	case 7:Text+="07\t720(1440)\t480\ti\t59.94/60Hz\t16:9\t\t861 Optional\tDouble Clock for 720x480i\t";break;
	case 8:Text+="08\t720(1440)\t240\tp\t59.94/60Hz\t4:3\t\tNew\t\tDouble Clock for 720x240p\t";break;
	case 9:Text+="09\t720(1440)\t240\tp\t59.94/60Hz\t16:9\t\tNew\t\tDouble Clock for 720x240p\t";break;
	case 10:Text+="10\t(2880)\t\t480\ti\t59.94/60Hz\t4:3\t\tNew\t\tGame Console\t";break;
	case 11:Text+="11\t(2880)\t\t480\ti\t59.94/60Hz\t16:9\t\tNew\t\tGame Console\t";break;
	case 12:Text+="12\t(2880)\t\t480\tp\t59.94/60Hz\t4:3\t\tNew\t\tGame Console\t";break;
	case 13:Text+="13\t(2880)\t\t480\tp\t59.94/60Hz\t16:9\t\tNew\t\tGame Console\t";break;
	case 14:Text+="14\t1440\t\t480\tp\t59.94/60Hz\t4:3\t\tNew\t\tHigh End DVD\t";break;
	case 15:Text+="15\t1440\t\t480\tp\t59.94/60Hz\t16:9\t\tNew\t\tHigh End DVD\t";break;
	case 16:Text+="16\t1920\t\t1080\tp\t59.94/60Hz\t16:9\t\tNew\t\tOptional HDTV\t";break;
	case 17:Text+="17\t720\t\t576\tp\t50Hz\t\t4:3\t\t861A\t\tEDTV\t";break;
	case 18:Text+="18\t720\t\t576\tp\t50Hz\t\t16:9\t\t861A\t\tEDTV\t";break;
	case 19:Text+="19\t1280\t\t720\tp\t50Hz\t\t16:9\t\t861A\t\tHDTV\t";break;		
	case 20:Text+="20\t1920\t\t1080\ti\t50Hz\t\t16:9\t\t861A\t\tHDTV\t";break;
	case 21:Text+="21\t720(1440)\t576\ti\t50Hz\t4:3\t\t861A Optional\tDouble Clock for 720x576i\t";break;
	case 22:Text+="22\t720(1440)\t576\ti\t50Hz\t16:9\t\t861A Optional\tDouble Clock for 720x576i\t";break;
	case 23:Text+="23\t720(1440)\t288\tp\t50Hz\t4:3\t\tNew\t\tDouble Clock for 720x288p\t";break;
	case 24:Text+="24\t720(1440)\t288\tp\t50Hz\t16:9\t\tNew\t\tDouble Clock for 720x288p\t";break;
	case 25:Text+="25\t(2880)\t\t576\ti\t50Hz\t4:3\t\tNew\t\tGame Console\t";break;
	case 26:Text+="26\t(2880)\t\t576\ti\t50Hz\t16:9\t\tNew\t\tGame Console\t";break;
	case 27:Text+="27\t(2880)\t\t288\tp\t50Hz\t4:3\t\tNew\t\tGame Console\t";break;
	case 28:Text+="28\t(2880)\t\t288\tp\t50Hz\t16:9\t\tNew\t\tGame Console\t";break;
	case 29:Text+="29\t1440\t\t576\tp\t50Hz\t\t4:3\t\tNew\t\tHigh End DVD\t";break;
	case 30:Text+="30\t1440\t\t576\tp\t50Hz\t\t16:9\t\tNew\t\tHigh End DVD\t";break;
	case 31:Text+="31\t1920\t\t1080\tp\t50Hz\t\t16:9\t\tNew\t\tOptional HDTV\t";break;
	case 32:Text+="32\t1920\t\t1080\tp\t23.97/24Hz\t16:9\t\tNew\t\tOptional HDTV\t";break;
	case 33:Text+="33\t1920\t\t1080\tp\t50Hz\t\t16:9\t\tNew\t\tOptional HDTV\t";break;
	case 34:Text+="34\t1920\t\t1080\tp\t29.97/30Hz\t16:9\t\tNew\t\tOptional HDTV\t";break;

	case 35:Text+="35\t2880\t\t480\tp\t59.94/60Hz\t4:3\t\tNew\t\tOptional\t";break;
	case 36:Text+="36\t2880\t\t480\tp\t59.94/60Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 37:Text+="37\t2880\t\t576\tp\t50Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 38:Text+="38\t2880\t\t576\tp\t50Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 39:Text+="39\t1920\t\t1080\ti\t50Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 40:Text+="40\t1920\t\t1080\ti\t100Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 41:Text+="41\t1280\t\t720\tp\t100Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 42:Text+="42\t720\t\t576\tp\t100Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 43:Text+="43\t720\t\t576\tp\t100Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 44:Text+="44\t720(1440)\t\t576\ti\t100Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 45:Text+="45\t720(1440)\t\t576\ti\t100Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 46:Text+="46\t1920\t\t1080\ti\t119.88/120Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 47:Text+="47\t1280\t\t720\tp\t119.88/120Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 48:Text+="48\t720\t\t480\tp\t119.88/120Hz\t4:3\t\tNew\t\tOptional\t";break;
	case 49:Text+="49\t720\t\t480\tp\t119.88/120Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 50:Text+="50\t720(1440)\t\t480\ti\t119.88/120Hz\t4:3\t\tNew\t\tOptional\t";break;
	case 51:Text+="51\t720(1440)\t\t480\ti\t119.88/120Hz\t16:9\t\tNew\t\tOptional\t";break;
	case 52:Text+="52\t720\t\t576\tp\t200Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 53:Text+="53\t720\t\t576\tp\t200Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 54:Text+="54\t720(1440)\t\t576\ti\t200Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 55:Text+="55\t720(1440)\t\t576\ti\t200Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 56:Text+="56\t720\t\t480\tp\t240Hz\t\t4:3\t\tNew\t\tOptional\t";break;
	case 57:Text+="57\t720\t\t480\tp\t240Hz\t\t16:9\t\tNew\t\tOptional\t";break;
	case 58:Text+="58\t720(1440)\t\t480\ti\t239.76/240Hz\t4:3\t\tNew\t\tOptional\t";break;
	case 59:Text+="59\t720(1440)\t\t480\ti\t239.76/240Hz\t16:9\t\tNew\t\tOptional\t";break;
	default:Text+="Reserved\r\n";break;		
	}
	Text+="\r\n";
	
}


void CEAExtensionParser::parseAudioDescBlockUncompressed(_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_UNCOMPRESSED AUDIO_BLOCK_UNCOMP)
{
	CString Temp;
	INT format_code=AUDIO_BLOCK_UNCOMP.AUDIO_FORMAT_CODE;
	

	Temp.Format("\r\n[%d-%d]",++CurrentByteNo,CurrentByteNo+2);
	Text+=Temp;
	
	Text+="Audio Descriptor Block Uncompressed\r\n\t";
		

	//Audio Descriptor Block 
	Temp.Format("%d-%d",CurrentByteNo,CurrentByteNo+2);
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	BYTE TEMP[3];
	memcpy(TEMP,&AUDIO_BLOCK_UNCOMP,3);
	
	Temp="";
	for(INT i=0;i<3;i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"\r\n\tAudio Descriptor Block\t");
	
	CurrentByteNo+=2;
	
	if(format_code==1)
	{
		Text+="Linear PCM\r\n\t";
	}
	
	Temp.Format("Max. no of Channels : %d",(AUDIO_BLOCK_UNCOMP.MAX_NO_OF_CHANNELS+1));
	Text+=Temp;
	Text+="\r\n\t";
	
	
	if(AUDIO_BLOCK_UNCOMP.BIT_2_6==1)
	{
		Text+="192 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_5==1)
	{
		Text+="176.4 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_4==1)
	{
		Text+="96 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_3==1)
	{
		Text+="88.2 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_2==1)
	{
		Text+="48 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_1==1)
	{
		Text+="44.1 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_2_0==1)
	{
		Text+="32 KHz\r\n\t";
	}
	
	
	if(AUDIO_BLOCK_UNCOMP.BIT_3_0==1)
	{
		Text+="Bit Rate";
		Text+="16 bit\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_3_1==1)
	{
		Text+="Bit Rate";
		Text+="20 bit\r\n\t";
	}
	if(AUDIO_BLOCK_UNCOMP.BIT_3_2==1)
	{
		Text+="Bit Rate";
		Text+="24 bit\r\n\t";
	}
	
	Text+="\r\n";
}


void CEAExtensionParser::parseAudioDescBlockCompressed(_CEA_SHORT_AUDIO_DESCRIPTOR_BLOCK_COMPRESSED AUDIO_BLOCK_COMPRESSED)
{
	CString Temp;

	Temp.Format("\r\n[%d-%d]",++CurrentByteNo,CurrentByteNo+2);
	Text+=Temp;
	
	Temp.Format("%d-%d",CurrentByteNo,CurrentByteNo+2);
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	Text+="Audio Descriptor Block Compressed\r\n\t";
	
	BYTE TEMP[3];
	memcpy(TEMP,&AUDIO_BLOCK_COMPRESSED,3);
	
	Temp="";
	for(INT i=0;i<3;i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"\r\n\tAudio Descriptor Block\r\n\r\n\t");
	
	CurrentByteNo+=2;
	
	INT format_code=AUDIO_BLOCK_COMPRESSED.AUDIO_FORMAT_CODE;
	
	switch(format_code)
	{
	case 0:Text+="Reserved\r\n\t";break;
	case 1:Text+="1 - Linear PCM\r\n\t";break;
	case 2:Text+="2 - AC-3\r\n\t";break;
	case 3:Text+="3 - MPEG1(Layers 1 & 2)\r\n\t";break;
	case 4:Text+="4 - MP3(MPEG1 Layer 3)\r\n\t";break;
	case 5:Text+="5 - MPEG-2(MultiChannel)\r\n\t";break;
	case 6:Text+="6 - AAC\r\n\t";break;
	case 7:Text+="7 - DTS\r\n\t";break;
	case 8:Text+="8 - ATRAC\r\n\t";break;
	case 9:Text+="9 - ONE BIT AUDIO\r\n\t";break;
	case 10:Text+="10 - DIGITAL DOLBY + \r\n\t";break;
	case 11:Text+="11 - DTS-HD\r\n\t";break;
	case 12:Text+="12 - MAT (MLP)\r\n\t";break;
	case 13:Text+="13 - DST\r\n\t";break;
	case 14:Text+="14 - WMA Pro\r\n\t";break;
	case 15:Text+="Reserved\r\n\t";break;
	default:Temp.Format("%d",format_code);
		Text+="Reserved For Audio Format\r\n\t";
		Text+=Temp;
		break;				
	}
	
	Temp.Format("Max. no of Channels : %d",(AUDIO_BLOCK_COMPRESSED.MAX_NO_OF_CHANNELS+1));
	Text+=Temp;
	Text+="\r\n\t";


//	Text+="\r\n\t";
	
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_6==1)
	{
		Text+="192 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_5==1)
	{
		Text+="176.4 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_4==1)
	{
		Text+="96 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_3==1)
	{
		Text+="88.2 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_2==1)
	{
		Text+="48 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_1==1)
	{
		Text+="44.1 KHz\r\n\t";
	}
	if(AUDIO_BLOCK_COMPRESSED.BIT_2_0==1)
	{
		Text+="32 KHz\r\n\t";
	}
	
//	Text+="\r\n\t";
	if(format_code ==2 || format_code ==3 ||format_code ==4 ||format_code ==5 ||format_code ==6 || format_code ==7 || format_code ==8)
	{	 
		Temp.Format("Max. bit rate: %d",((AUDIO_BLOCK_COMPRESSED.BIT_RATE)/8));
		Text+=Temp;
		Text+="\r\n\t";
	}

	if(format_code ==9 || format_code ==10 ||format_code ==11 ||format_code ==12 ||format_code ==13 || format_code ==14 || format_code ==15)
	{	 
		Temp.Format("Value Defined by Audio Codec Vendor:%d",AUDIO_BLOCK_COMPRESSED.BIT_RATE);
		Text+=Temp;
		Text+="\r\n\t";
	}
}



void CEAExtensionParser::parseSpeakerAllocBlock(_CEA_SPEAKER_ALLOCATION_DATA_BLOCK SPEAKER_ALLOC_BLOCK)
{
	CString Temp;
	Temp.Format("\r\n[%d-%d]",++CurrentByteNo,CurrentByteNo+2);
	Text+=Temp;

	Text+="Speaker Allocation Block\r\n\t";

	
		
	Temp.Format("%d-%d",CurrentByteNo,CurrentByteNo+2);
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	BYTE TEMP[3];
	memcpy(TEMP,&SPEAKER_ALLOC_BLOCK,3);
	
	Temp="";
	for(INT i=0;i<3;i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Speaker Allocation Block");
	
	CurrentByteNo+=2;
	
	if(SPEAKER_ALLOC_BLOCK.BIT1_6==1)
	{
		Text+="(RLC/RRC) Rear Left Center,Rear Right Center\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_5==1)
	{
		Text+="(FLC/FRC) Front Left Center,Front Right Center\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_4==1)
	{
		Text+="(RC) Rear Center\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_3==1)
	{
		Text+="(RL/RR) Rear Left, Rear Right\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_2==1)
	{
		Text+="(FC) Front Center\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_1==1)
	{
		Text+="(LFE) Low-Frequency Effects\r\n\t";
	}
	if(SPEAKER_ALLOC_BLOCK.BIT1_0==1)
	{
		Text+="(FL/FR) Front Left,Front Right\r\n\t";
	}

	Text+="\r\n";

}

void CEAExtensionParser::parseVendorSpecificBlock(_CEA_VENDOR_SPECIFIC_DATA_BLOCK_14 VENDOR_BLOCK)
{
    INT payload_start = 0;
	CString Temp;
	Temp.Format("\r\n[%d-%d]",++CurrentByteNo,(CurrentByteNo+L));
	Text+=Temp;

	Text+="Vendor Specific Data Block\r\n\t";

	Temp.Format("%d-%d",CurrentByteNo,(CurrentByteNo+L-1));
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	BYTE *TEMP=new BYTE[L];
	memcpy(TEMP,&VENDOR_BLOCK,L);
	
	Temp="";
	for(INT i=0;i<L;i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Vendor Block");
	
	Text+="IEEE Registration Number:";
	if (TEMP[0]==3 && TEMP[1]==12 && TEMP[2]==0)
	{
	//Temp.Format("%d",VENDOR_BLOCK.IEEE_REGNO);
	//Temp=("0x%02X",VENDOR_BLOCK.IEEE_REGNO);
	//Text+=Temp;
	//CHAR ID[]="1239112";

	//if (strcmp(Temp,ID)==0)
	
		Text+="HDMI display";
	}
	else
	{
		Text+="Some other Display(not HDMI)";
	}
	INT length=3;
	Text+="\r\n";

	while (length<=L)
	{
		switch(length)
		{
			case 0:break; 
			case 1:break;
			case 2:break;
			case 3:length++;break;
			case 4:
				{
				Temp.Format("[%d] Components of source physical address('A' and 'B' 4 bits each)",(CurrentByteNo+3));
				Text+="\t";
				Text+=Temp;
				Text+="\r\n";
				length++;
				break;
				}
			case 5:
				{
					Temp.Format("[%d] Components of source physical address('C' and 'D' 4 bits each)",(CurrentByteNo+4));
					Text+="\t";
					Text+=Temp;
					Text+="\r\n";
					length++;
					break;
				}
			case 6:
				{
				if ((VENDOR_BLOCK.Al)==1)
				{ 
					Text+="\t The Sink shall Accept and Process any ACP,ISRC1 or ISRC2 packet \r\n";
				}
				else
				{ 
					Text+="\t The Sink Doesn't Accept and Process any ACP,ISRC1 or ISRC2 packet \r\n";
				}
				if ((VENDOR_BLOCK.DC_30)==1)
				{ 
					Text+="\t Sink supports 30 bits/pixel (10 bits/color). \r\n";
				}
				if ((VENDOR_BLOCK.DC_36)==1)
				{ 
					Text+="\t Sink supports 36 bits/pixel (12 bits/color). \r\n";
				}
				if ((VENDOR_BLOCK.DC_48)==1)
				{ 
					Text+="\t Sink supports 48 bits/pixel (16 bits/color). \r\n";
					
				}
				if ((VENDOR_BLOCK.DC_Y444)==1)
				{ 
					Text+="\t Sink supports YCBCR 4:4:4 in Deep Color modes.. \r\n";
					
				}
				if ((VENDOR_BLOCK.DVI)==1)
				{ 
					Text+="\t Sink supports DVI dual-link operation \r\n";
					
				}
				length++;
				break;
				}
			case 7:
				{
					Temp.Format(" Maximum TMDS clock rate supported=%d MHz",((VENDOR_BLOCK.Max_TMDS_Clock)*5));
					Text+="\t";
					Text+=Temp;
					Text+="\r\n";
					length++;
					break;
				}
			case 8:
				{
					if ((VENDOR_BLOCK.Latency)==1)
					{
						Text+="\t Video_Latency and Audio_Latency fields are present\r\n";
						
					}
					if ((VENDOR_BLOCK.I_Latency)==1)
					{
						Text+="\t Interlaced Video Latency and Audio Latency fields are present\r\n";
						
					}
                    if ((VENDOR_BLOCK.HDMI_Video_Present)==1)
					{
						Text+="\t HDMI Video bit is set (value for HDMI1.4) only\r\n";
						
					}
					length++;

                    payload_start = length; // init
					break;
				}
			case 9:
				{
					
					if ( (VENDOR_BLOCK.Latency ==1) && (VENDOR_BLOCK.I_Latency ==1))
					{
						Temp.Format(" Video_Latency While receiving Progressive Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++;
					
						
						Temp.Format(" Audio_Latency While receiving Progressive Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++;

						Temp.Format(" Interlaced_Video_Latency While receiving an Interlaced Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++;
						
						Temp.Format(" Interlaced_Audio_Latency While receiving an Interlaced Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++; // In this if loop length is increased by 4 bytes for Video latency + Audio latency + Interlaced video latency + Interlaced audio Latency
					}

					if ( (VENDOR_BLOCK.Latency ==1) && (VENDOR_BLOCK.I_Latency!=1))
					{
						Temp.Format(" Video_Latency While receiving Any Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++;
						
						Temp.Format(" Audio_Latency While receiving Any Video format=%d msec",((VENDOR_BLOCK.PAYLOAD[(length-payload_start)]-1)*2));
						Text+="\t";
						Text+=Temp;
					    Text+="\r\n";
						length++;; // In this if loop length is increased by 2 bytes for Video latency + Audio latency. 
											}
					}

					// HDMI 1.4 VSDB
                    if (VENDOR_BLOCK.HDMI_Video_Present)
                    {
                        int Image_Size = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0x18) >> 3;
                        Temp.Format("\t [%d] Image size = %d\r\n", CurrentByteNo+length-1, Image_Size);
                        Text+=Temp;

                        int _3D_Multi_Present = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0x60)>>5;
                        Temp.Format("\t [%d] 3D Multi present = %d\r\n", CurrentByteNo+length-1, _3D_Multi_Present);
                        Text+=Temp;

                        if (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0x80)
				        { 
                            Text+="\t Sink supports mandatory 3D HDMI 1.4 modes!! \r\n";    					
				        }
                        else
                        {
                            Text+="\t Sink doesn't indicate support for mandatory 3D HDMI 1.4 modes\r\n";
                        }
				        
						length++;

                        int HDMI_3D_LEN = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0x1F);
                        Temp.Format("\t [%d] HDMI 3D format field size = %d\r\n", CurrentByteNo+length-1, HDMI_3D_LEN);
                        Text+=Temp;                        

                        int HDMI_VIC_LEN = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0xE0)>>5;
                        Temp.Format("\t [%d] HDMI VIC format field size = %d\r\n", CurrentByteNo+length-1, HDMI_VIC_LEN);
                        Text+=Temp;
                        length++;

                        if (HDMI_VIC_LEN > 0)
                        {
                            // check size aspects
                            if (length+HDMI_VIC_LEN-1 > L)
                            {
                                Text += "\t HDMI_VIC_LEN size goes beyond the total size of VSDB! Bad data\r\n";
									#if 0 // skip bad data
					                    length += HDMI_VIC_LEN;
							            break;
									#endif
                            }

                            // Print all VIC's for now
                            Temp.Format("\t [%d-%d] HDMI VIC: ", CurrentByteNo+length-1, CurrentByteNo-1+length+HDMI_VIC_LEN);
                            Text += Temp;
                            int i = 0; // current pos
                            while (i < HDMI_VIC_LEN)
                            {
                                Temp.Format(" \t %d, ", VENDOR_BLOCK.PAYLOAD[length-payload_start]);
                                Text += Temp;
                                length++;
                                i++;
                            }
                            Text += "\r\n";
                        }
                        
                        int order_structure_detail_length = HDMI_3D_LEN; // init

                        // check size aspects
                        if (length+HDMI_3D_LEN-1 > L)
                        {
                            Text += "\t HDMI_3D_LEN size goes beyond the total size of VSDB! Bad data\r\n";
							#if 0 // skip bad data
								length += HDMI_3D_LEN;
								break;
							#endif
                        }

                        ULONG ul3DVics = 0;
                        ULONG ul3DStructure = 0;

                        if (_3D_Multi_Present == 1 || _3D_Multi_Present == 2)
                        {
                            ul3DStructure = VENDOR_BLOCK.PAYLOAD[length-payload_start]<<8; // byte 1
                            ul3DStructure |= (VENDOR_BLOCK.PAYLOAD[length-payload_start+1]); // byte 0

                            Temp.Format("\t [%d-%d] Supporting 3D formats: 0x%X\r\n", CurrentByteNo-1+length, CurrentByteNo-1+length+1, ul3DStructure);

                            ul3DVics = 0xFFFF; // all VIC's in EDID supports the 3D formats in ul3DStructure

                            length += 2;
                            order_structure_detail_length -= 2; // reduce 2 from original length
                            Text += Temp;
                        }

                        if (_3D_Multi_Present == 2) // mask present
                        {
                            int i = (VENDOR_BLOCK.PAYLOAD[length-payload_start] << 8); // byte 1
                            i |= (VENDOR_BLOCK.PAYLOAD[length-payload_start+1]); // byte 0

                            Temp.Format("\t [%d-%d] VIC's supporting 3D formats is masked by 0x%X\r\n", CurrentByteNo-1+length, CurrentByteNo-1+length+1, i);
                            ul3DVics &= i; // apply masking if any
                            length += 2;
                            order_structure_detail_length -= 2; // reduce 2 from current length
                            Text += Temp;
                        }

                        if (ul3DVics != 0)
                        {
                            Text += Print3DVICDetails(ul3DVics);
                            Text += "\t\t Sink Supports " + Print3DStructureAll(ul3DStructure) + "\r\n";

						}

                        int i = 0;
                        int j = 0;
                        while (i < order_structure_detail_length)
                        {
                            BYTE structure = VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0xF;
                            BYTE order = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0xF0) >> 4;

                            j++;
                            Temp.Format("\t [%d] 2D_VIC_Order_%d = %d (%s), 3D_Structure_%d = %d (%s)", CurrentByteNo-1+length, j, order, GetVICModeText(ucSupportedVIC[order]), j, structure, Print3DFormats(structure));
                            Text += Temp;

                            length++;
                            i++;

                            BYTE detail = 0;
                            if (structure >= 0x8)
                            {
                                // next byte has 3d detail info in bits 7:4
                                detail = (VENDOR_BLOCK.PAYLOAD[length-payload_start] & 0xF0) >> 4;

                                Temp.Format(" [%d] 3D_Detail_%d = %d (%s)", CurrentByteNo-1+length, j, detail, Print3DDetail(detail));
                                Text += Temp;

                                // just a check
                                if (structure == 8 && detail != 1)
                                {
                                    Text += " - ERROR: 3D_Details should be 1 (horizontal sub-sampling)";
                                }

                                length++;
                                i++;
                            }

                            Text += "\r\n";
                        }                   

                        length++;
                        break;
                    }
	
				


           default:
				{
					//Temp.Format("[%d-%d] Reserved",(CurrentByteNo+11),(CurrentByteNo+L));
					Text+="\t";
					Text+=Temp;
					Text+="\r\n";
					Text+="\r\n";
					length=L+1;
					break;
				}
		}
	}
				
	Text+="\r\n";
	Text+="\r\n";
	CurrentByteNo += L-1;


}

CString CEAExtensionParser::Print3DVICDetails(ULONG ul3DVics)
{
    CString stTemp, st3DVics = "";
    int i = 1;
    
    for (i= 0; i < 16; i++)
    {
        if ((1<<i) & ul3DVics)
        {
            // Get this vic data from EDID, print it
            stTemp.Format("\t\tVIC index = %d (%s) in EDID supports 3D\r\n", i+1, GetVICModeText(ucSupportedVIC[i]));
            st3DVics += stTemp;
        }
    }

    return st3DVics;
}

CString CEAExtensionParser::Print3DFormats(ULONG ul3DStructure)
{
    CString stTemp = "";

    switch (ul3DStructure)
    {
    case 0:
        stTemp += "Frame packing";
        break;
    case 1:
        stTemp += "Field alternative";
        break;
    case 2:
        stTemp += "Line alternative";
        break;
    case 3:
        stTemp += "Side-by-side (Full)";
        break;
    case 4:
        stTemp += "L+depth";
        break;
    case 5:
        stTemp += "L+depth+graphics+graphics-depth";
        break;
    case 6:
        stTemp += "Top-and-bottom";
        break;
    case 8:
        stTemp += "Side-by-side (Half) horizontal sub-sampling";
        break;
    case 0xF:
        stTemp += "Side-by-side (Half) quincunx sub-sampling";
        break;
    default:
        stTemp += "Reserved";
        break;
    }

    return stTemp;
}

CString CEAExtensionParser::Print3DDetail(ULONG ul3DDetail)
{
    CString stTemp = "";

    switch (ul3DDetail)
    {
    case 0:
        stTemp += "Supports all of the horizontal sub-sampling & four quincunx matrix";
        break;
    case 1:
        stTemp += "Horizontal sub-sampling";
        break;
    case 6:
        stTemp += "Quincunx matrix - Support All four combination of sub-sampling position";
        break;
    case 7:
        stTemp += "Quincunx matrix - Odd/Left Picture, Odd/Right Picture";
        break;
    case 8:
        stTemp += "Quincunx matrix - Odd/Left Picture , Even/Right Picture";
        break;
    case 9:
        stTemp += "Quincunx matrix - Even/Left Picture, Odd/Right Picture";
        break;
    case 10:
        stTemp += "Quincunx matrix - Even/Left Picture, Even/Right Picture";
        break;
    default:
        stTemp += "Reserved";
        break;
    }

    return stTemp;
}

CString CEAExtensionParser::Print3DStructureAll(ULONG ul3DStructure)
{
    CString stTemp = "";
    
    for (int i= 0; i < 16; i++)
    {
        if ((1<<i) & ul3DStructure)
        {
            stTemp += Print3DFormats(i);
            stTemp += ", ";
        }
    }

    return stTemp;
}

CString CEAExtensionParser::GetVICModeText(BYTE CODE)
{
    CString Temp = "";

	switch(CODE)
	{
	    case 0:Temp+="No Video Code Available";break;
	    case 1:Temp+="640 480p 59.94/60Hz 4:3 861 Default Format ";break;
	    case 2:Temp+="720 480p 59.94/60Hz 4:3 861 EDTV ";break;
	    case 3:Temp+="720 480p 59.94/60Hz 16:9 861 EDTV ";break;
	    case 4:Temp+="1280 720p 59.94/60Hz 16:9 861 HDTV ";break;
	    case 5:Temp+="1920 1080 i 59.94/60Hz 16:9 861 HDTV ";break;
	    case 6:Temp+="720(1440) 480 i 59.94/60Hz 4:3 ";break;
	    case 7:Temp+="720(1440) 480 i 59.94/60Hz 16:9 ";break;
	    case 8:Temp+="720(1440) 240p 59.94/60Hz 4:3 ";break;
	    case 9:Temp+="720(1440) 240p 59.94/60Hz 16:9 ";break;
	    case 10:Temp+="(2880) 480 i 59.94/60Hz 4:3 ";break;
	    case 11:Temp+="(2880) 480 i 59.94/60Hz 16:9 ";break;
	    case 12:Temp+="(2880) 480p 59.94/60Hz 4:3 ";break;
	    case 13:Temp+="(2880) 480p 59.94/60Hz 16:9 ";break;
	    case 14:Temp+="1440 480p 59.94/60Hz 4:3 ";break;
	    case 15:Temp+="1440 480p 59.94/60Hz 16:9 ";break;
	    case 16:Temp+="1920 1080p 59.94/60Hz 16:9 ";break;
	    case 17:Temp+="720 576p 50Hz 4:3 861A EDTV ";break;
	    case 18:Temp+="720 576p 50Hz 16:9 861A EDTV ";break;
	    case 19:Temp+="1280 720p 50Hz 16:9 861A HDTV ";break;		
	    case 20:Temp+="1920 1080 i 50Hz 16:9 861A HDTV ";break;
	    case 21:Temp+="720(1440) 576 i 50Hz 4:3 ";break;
	    case 22:Temp+="720(1440) 576 i 50Hz 16:9 ";break;
	    case 23:Temp+="720(1440) 288p 50Hz 4:3 ";break;
	    case 24:Temp+="720(1440) 288p 50Hz 16:9 ";break;
	    case 25:Temp+="(2880) 576 i 50Hz 4:3 ";break;
	    case 26:Temp+="(2880) 576 i 50Hz 16:9 ";break;
	    case 27:Temp+="(2880) 288p 50Hz 4:3 ";break;
	    case 28:Temp+="(2880) 288p 50Hz 16:9 ";break;
	    case 29:Temp+="1440 576p 50Hz 4:3 ";break;
	    case 30:Temp+="1440 576p 50Hz 16:9 ";break;
	    case 31:Temp+="1920 1080p 50Hz 16:9 ";break;
	    case 32:Temp+="1920 1080p 23.97/24Hz ";break;
	    case 33:Temp+="1920 1080p 50Hz 16:9 ";break;
	    case 34:Temp+="1920 1080p 29.97/30Hz 16:9 ";break;
	    default:Temp+="Reserved";break;		
	}

    return Temp;
}

void CEAExtensionParser::parseColorimetryBlock(_CEA_COLORIMETRY_DATA_BLOCK COLORI_DATA_BLOCK)
{
	CString Temp;
	Temp.Format("\r\n[%d-%d]",++CurrentByteNo,(CurrentByteNo+L));
	Text+=Temp;

	Text+="Colorimetry Data Block\r\n";

	Temp.Format("%d-%d",CurrentByteNo,(CurrentByteNo+L-1));
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	BYTE *TEMP=new BYTE[L];
	memcpy(TEMP,&COLORI_DATA_BLOCK,L);
	
	Temp="";
	for(INT i=0;i<(L);i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Colorimetry Data Block");
	
	if (COLORI_DATA_BLOCK.xvYCC_601==1)
	{
		Text+="\t Support  Standard Definition Colorimetry based on IEC 61966-2-4 (xvYcc601)";
		Text+="\r\n";
	}
	if (COLORI_DATA_BLOCK.xvYCC_709==1)
	{
		Text+="\t Support  High Definition Colorimetry based on IEC 61966-2-4 (xvYcc709)";
		Text+="\r\n";
	}
	
	if (COLORI_DATA_BLOCK.MD0==1)
	{
		Text+="\t Metadata Profile :MD0.";
		Text+="\r\n";
	}
	if (COLORI_DATA_BLOCK.MD1==1)
	{
		Text+="\t Metadata Profile :MD1.";
		Text+="\r\n";
	}
	if (COLORI_DATA_BLOCK.MD2==1)
	{
		Text+="\t Metadata Profile :MD2.";
		Text+="\r\n";
	}

	Text+="\r\n";
	Text+="\r\n";
	CurrentByteNo += L-2;

	//future gamult related metadata to be added.
}




void CEAExtensionParser::parseVideoCapabilityBlock(_CEA_VIDEO_CAPABILITY_BLOCK VIDEO_CAP_BLOCK)
{
	CString Temp;
	//Temp.Format("\r\n[%d-%d]",++CurrentByteNo,(CurrentByteNo+L-2));
	Temp.Format("\r\n[%d]",++CurrentByteNo);
	Text+=Temp;

	Text+="Video Capability Data Block\r\n\t";

	//Temp.Format("%d-%d",CurrentByteNo,(CurrentByteNo+L-2));
	Temp.Format("%d",CurrentByteNo);
	INT index=ListBox->InsertItem(++listcount,Temp);
	
	BYTE *TEMP=new BYTE[L];
	memcpy(TEMP,&VIDEO_CAP_BLOCK,L);
	
	Temp="";
	for(INT i=0;i<L;i++)
	{
		CString strTemp;
		strTemp.Format("0x%02X",TEMP[i]);
		Temp+=strTemp;
		Temp+=",";
	}
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Video Capablility Block");
	
	if (VIDEO_CAP_BLOCK.QS==1)
	{
		Text+=" Quantization Range(Applies to RGB only)-Selectable(Via AVI Q) ";
		Text+="\r\n";
	}
	switch (VIDEO_CAP_BLOCK.S_PT)
	{
	case 0:
		{
			Text+="\t No Data in PT Overscan/Underscan beahvior.";
			Text+="\r\n";
			break;
		}
	case 1:
		{
			Text+="\t PT Overscan/Underscan Behavior = Always Overscanned.";
			Text+="\r\n";
			break;
		}
	case 2:
		{
			Text+="\t PT Overscan/Underscan Behavior = Always Underscanned.";
			Text+="\r\n";
			break;
		}
	case 3:
		{
			Text+="\t PT Overscan/Underscan Behavior = Supports both Underscan and Overscan.";
			Text+="\r\n";
			break;
		}
	default:break;
	}
	switch (VIDEO_CAP_BLOCK.S_IT)
	{
	case 0:
		{
			Text+="\t IT Video Formats NOT supported.";
			Text+="\r\n";
			break;
		}
	case 1:
		{
			Text+="\t IT Overscan/underscan behavior = Always Overscanned.";
			Text+="\r\n";
			break;
		}
	case 2:
		{
			Text+="\t IT Overscan/underscan behavior = Always Underscanned.";
			Text+="\r\n";
			break;
		}
	case 3:
		{
			Text+="\t IT Overscan/underscan behavior = Supports both Underscan and Overscan.";
			Text+="\r\n";
			break;
		}
	default:break;
	}

	switch (VIDEO_CAP_BLOCK.S_CE)
	{
	case 0:
		{
			Text+="\t CE Video Formats NOT supported.";
			Text+="\r\n";
			break;
		}
	case 1:
		{
			Text+="\t CE Overscan/underscan behavior = Always Overscanned.";
			Text+="\r\n";
			break;
		}
	case 2:
		{
			Text+="\t CE Overscan/underscan behavior = Always Underscanned.";
			Text+="\r\n";
			break;
		}
	case 3:
		{
			Text+="\t CE Overscan/underscan behavior = Supports both Underscan and Overscan.";
			Text+="\r\n";
			break;
		}
	default:break;
	}

	Text+="\r\n";
	Text+="\r\n";
	CurrentByteNo += L-2;

	//future gamult related metadata to be added.
}


void CEAExtensionParser::getByteValuesCEA()
{
	
}

void CEAExtensionParser::CEAcheckSum()
{
	
	BYTE sum=0;
	CString Temp;
	
	for(INT i=0;i<128;i++)
	{
		sum+=ceaext[i];
	}
	
	if(sum==0)
	{
		Text+="CEA Check Sum OK!\r\n";
	}
	else
	{
		Text+="CEA Check Sum Failed!\r\n";
	}
	
	INT index=ListBox->InsertItem(++listcount,"127");
	Temp.Format("0x%02X",*(ceaext+127));
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CheckSum");
	
}


//************************************ Methods specific to VTB****************************************************
//====================================================================================================

void VTBExtensionParser::parseVTBExtension(VTB_EXTENSION VTB_EXT, CListCtrl *Ptr)
{
	CString Temp;
	INT index=0;
	CurrentByteNo = 0; // Contains the no. of last Byte parsed.
	
	ListBox=Ptr;

	index=ListBox->InsertItem(++listcount,"");
	ListBox->SetItemText(index,1,"");
	ListBox->SetItemText(index,2,"");

	index=ListBox->InsertItem(++listcount,"****");
	Temp.Format("Block No.: %d", CurrentExtNo);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"VTB EXTENSION BLOCK");
	
	Text+="\r\n\r\n**************************************\r\n";
	Temp.Format("Block No.: %d     VTB Release-A Extension Block\r\n", CurrentExtNo);
	Text+=Temp;
	Text+="**************************************\r\n";		
	
	
	//**************************************************
	//Definintion of Various Descriptor Blocks inside VTB Extension
	//**************************************************

	_DETAILED_TIMING_DESCRIPTOR_BLOCK DTD;
	_CVT_DESCRIPTOR CVT;
	_STANDARD_TIMING_IDENTIFICATION_RESOLUTION STD;

	//Parse Tag and Version of the VTB Ext.
	parseTagVersion(VTB_EXT);
	CurrentByteNo++;

	//Adding type & number of descriptors.
	// DTDs
	Temp.Format("[%d]No. of DTDs in VTB Block %d",++CurrentByteNo,VTB_EXT.NumDTD);
	Text+=Temp;
	Text+="\r\n";

	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",VTB_EXT.NumDTD);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"No. of DTDs in VTB Block");

	// CVTs
	Temp.Format("[%d]No. of CVTs in VTB Block %d",++CurrentByteNo, VTB_EXT.NumCVT);
	Text+=Temp;
	Text+="\r\n";

	Temp.Format("%d",CurrentByteNo);	
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",VTB_EXT.NumCVT);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"No. of CVTs in VTB Block");

	// Standard Timing Descriptors
	Temp.Format("[%d]No. of STDs in VTB Block %d",++CurrentByteNo, VTB_EXT.NumST);
	Text+=Temp;
	Text+="\r\n";

	Temp.Format("%d",CurrentByteNo);
	index=ListBox->InsertItem(++listcount,Temp);
	Temp.Format("0x%02X",VTB_EXT.NumST);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"No. of STDs in VTB Block");

	
	//***********************Parsing DTDs*********************
	//Now, parse DTDs

	if(VTB_EXT.NumDTD)
	{
		for(byteCount=0; byteCount < VTB_EXT.NumDTD; byteCount++)
		{
			memcpy(&DTD,&VTB_EXT.DATA[18 * byteCount], 18);
	
			CString DTD_Values;
			Temp.Format("%d-%d",++CurrentByteNo,CurrentByteNo+17);
			index=ListBox->InsertItem(++listcount ,Temp);

			//Adding Text Data
			Temp.Format("[%d-%d]",CurrentByteNo,CurrentByteNo+17);
			Text+=Temp;

			CurrentByteNo+=17;
		
			for(INT c=0;c<18;c++)
			{
				Temp.Format("0x%02X, ",VTB_EXT.DATA[18 * byteCount + c]);
				DTD_Values+=Temp;
			}
			ListBox->SetItemText(index,1,DTD_Values);
		
			ListBox->SetItemText(index,2,"Detailed Timing Descriptor Block");
		
			parsedetailed_timing_descriptor(DTD);

		}
	}		

	
	//****************************Parsing CVTs***********************
	//Parsing the CVT Descriptors 
	if(VTB_EXT.NumCVT)
	{
		for(byteCount=0; byteCount < VTB_EXT.NumCVT; byteCount++)
		{
			memcpy(&CVT,&VTB_EXT.DATA[++CurrentByteNo-5],3);
	
			CString CVT_Values;
			Temp.Format("%d-%d",CurrentByteNo,CurrentByteNo+2);
			index=ListBox->InsertItem(++listcount ,Temp);

			//Adding Text Data
			Temp.Format("[%d-%d] CVT Descriptor Block\r\n",CurrentByteNo,CurrentByteNo+2);
			Text+=Temp;

			for(INT c=0;c<3;c++)
			{
				Temp.Format("0x%02X, ",VTB_EXT.DATA[CurrentByteNo - 5 + c]);
				CVT_Values+=Temp;
			}
			ListBox->SetItemText(index,1,CVT_Values);
		
			ListBox->SetItemText(index,2,"CVT Descriptor Block");
		
			parseCVTDescriptor(CVT);

			CurrentByteNo+=2;
		}
	}		

	//**********************************Parsing Standard Timings******************
	//Parsing the Standard Timing Descriptors
	if(VTB_EXT.NumST)
	{
		for(byteCount=0; byteCount < VTB_EXT.NumST; byteCount++)
		{
			memcpy(&STD,&VTB_EXT.DATA[++CurrentByteNo - 5],2);
	
			CString ST_Values;
			Temp.Format("%d-%d",CurrentByteNo,CurrentByteNo+1);
			index=ListBox->InsertItem(++listcount ,Temp);

			//Adding Text Data
			Temp.Format("[%d-%d] Standard Timing Block",CurrentByteNo,CurrentByteNo+1);
			Text+=Temp + "\r\n";

			for(INT c=0;c<2;c++)
			{
				Temp.Format("0x%02X, ",VTB_EXT.DATA[CurrentByteNo - 5 + c]);
				ST_Values+=Temp;
			}
			ListBox->SetItemText(index,1,ST_Values);
		
			ListBox->SetItemText(index,2,"Standard Timing Block");
		
			parseStandard_timing_identification_resolution(STD);

			CurrentByteNo+=1;
		}
	}		
	
	//*******************************Padding***************************************
	if(CurrentByteNo < 126 )
	{
		Temp.Format("%d-126", ++CurrentByteNo);
		index=ListBox->InsertItem(++listcount,Temp);
		Temp="";
		
		for(INT c=CurrentByteNo - 5;c<122;c++)
		{
			CString strTemp;
			strTemp.Format("0x%02X, ",VTB_EXT.DATA[c]);
			Temp+=strTemp;
		}
		ListBox->SetItemText(index,1,Temp);
		ListBox->SetItemText(index,2,"Padding");
	}
	
	//***************************CHECK SUM**************************
		Text+="[127]CheckSum\r\n\t";
	
		VTBChecksum();
}
		
	

	
	
void VTBExtensionParser::parseTagVersion(VTB_EXTENSION VTB_EXT)
{
	CString Temp;
	INT index=0;
	
	if(VTB_EXT.TAG==VTB_EXT_TAG)
	{
		Text+="[0]Tag OK!\r\n";
	}
	else
	{
		MessageBox(NULL,"Extension Not Supported","Error",MB_OK);
		return;
	}

	Temp.Format("0x%02X",VTB_EXT.TAG);
	index=ListBox->InsertItem(++listcount,"0");
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"VTB Extension Tag");
	
	Temp.Format("0x%02X",VTB_EXT.VERSION);
	index=ListBox->InsertItem(++listcount,"1");
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"VTB Extension Version");

	Temp.Format("[1] VTB Extension Version:%x",VTB_EXT.VERSION);
	Text+=Temp;
	Text+="\r\n";
	
	
}

void VTBExtensionParser::parseCVTDescriptor(_CVT_DESCRIPTOR CVT_DESCRIPTOR)
{
	_CVT_DESCRIPTOR *pCVT;
	CString Temp;
	INT YRes=0, XRes=0;
	BYTE SupportBits =0;
	BYTE ExtractByte = 0, RequiredBit=0;
	INT MaxSupported_RR = 0;
		
	pCVT = &CVT_DESCRIPTOR;

	YRes = ((pCVT->VERTICAL_HIGHER << 8) + pCVT->VERTICAL_LOWER + 1) * 2;
	Temp.Format("\tVertical Resolution : %d ", YRes);
	Text+=Temp + "\r\n";
	
	switch (pCVT->ASPECT_RATIO)
	{
		case 0x00 :
			XRes = (YRes * 4/3);
			Text+="\tAspect Ratio : 4:3  \r\n";
			break;
	
		case 0x01 :
			XRes = (YRes * 16/9);
			Text+="\tAspect Ratio : 16:9 \r\n";
			break;
	
		case 0x02 :
			XRes = (YRes * 16/10);
			Text+="\tAspect Ratio : 16:10 \r\n";
			break;
	
		case 0x03 :			// Undefined/reserved case...
			Text+="\tAspect Ratio : Undefined/ Reserved Case\r\n";
			break;						
	}

	Temp.Format("\tHorizontal Resolution : %d (Calculated)", XRes);
	Text+=Temp + "\r\n";
	
    SupportBits = (0x1F & pCVT->REFRESH_RATE_Bits);  // 0x1F = 00011111.
	ExtractByte = 1;

	Text += "\tSupported Refresh Rates : \r\n";
	for (INT Count = 0; Count < 5; Count++)
	{
		RequiredBit = SupportBits & ExtractByte;  // RequiredBit stores bit used for current RR

		if(RequiredBit)
		{
			switch (ExtractByte)
			{
				case 1:												// 60 Hz RB				
					Text += "\t\t60 Hz (with Reduced Blanking) \r\n";
					break;
					
				case 2 :											// 85 Hz
					Text += "\t\t85 Hz \r\n";
					break;

				case 4:												// 75 Hz
					Text += "\t\t75 Hz \r\n";
					break;

				case 8:												// 60 Hz Normal Blanking
					Text += "\t\t60 Hz (Without Reduced Blanking) \r\n";
					break;
					
				case 16:											// 50 Hz
					Text += "\t\t50 Hz \r\n";
					break;
			}
		}

		ExtractByte <<= 1;		
	}


	switch(pCVT->PREFERED_RR_CONTROL)
	{
		case 0:
			Temp.Format("\tPreferred Refresh Rate : 50 Hz");
			break;
		case 1:
			Temp.Format("\tPreferred Refresh Rate : 60 Hz (Reduced Blanking if Supported OR Normal Blanking) ");	
			break;
		case 2:
			Temp.Format("\tPreferred Refresh Rate : 75 Hz");
			break;
		case 3:
			Temp.Format("\tPreferred Refresh Rate : 85 Hz ");
	}
		Text+=Temp + "\r\n\r\n";
}	

void VTBExtensionParser::VTBChecksum()
{
	
	BYTE sum=0;
	CString Temp;
	
	for(INT i=0;i<128;i++)
	{
		sum+=vtbext[i];
	}
	
	if(sum==0)
	{
		Text+="VTB Check Sum OK!\r\n";
	}
	else
	{
		Text+="VTB Check Sum Failed!\r\n";
	}
	
	INT index=ListBox->InsertItem(++listcount,"127");
	Temp.Format("0x%02X",*(vtbext+127));
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CheckSum");
	
}

//==========================================Methods specific to Block Map=============================
//====================================================================================================

void BlockMapExtensionParser::parseTag(BLOCK_MAP_EXTENSION BLOCK_MAP_EXT)
{
	CString Temp;
	INT index=0;
	
	if(BLOCK_MAP_EXT.TAG==BLOCK_MAP_TAG)
	{
		Text+="[0]Tag OK!\r\n";
	}
	else
	{
		MessageBox(NULL,"Extension Not Supported","Error",MB_OK);
		return;
	}

	index=ListBox->InsertItem(++listcount,"0");
	Temp.Format("0x%02X",BLOCK_MAP_EXT.TAG);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Block Map Extension Tag");	
}

void BlockMapExtensionParser::parseBlockMapExtension(BLOCK_MAP_EXTENSION BLOCK_MAP_EXT, CListCtrl *Ptr)
{
	CString Temp;
	INT index=0;
	INT i = 0;
	CurrentByteNo = 0; // Contains the no. of last Byte parsed.
	
	ListBox=Ptr;

	index=ListBox->InsertItem(++listcount,"");
	ListBox->SetItemText(index,1,"");
	ListBox->SetItemText(index,2,"");

	index=ListBox->InsertItem(++listcount,"****");
	Temp.Format("Block No.: %d", CurrentExtNo);
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"Block Map EXTENSION BLOCK");
	
	Text+="\r\n\r\n**************************************\r\n";
	Temp.Format("Block No.: %d     Block Map Extension Block\r\n", CurrentExtNo);
	Text+=Temp;
	Text+="**************************************\r\n";		
	
	//Parse Tag of the Block Map Ext.
	parseTag(BLOCK_MAP_EXT);
	
	for(i=0; i<126 && BLOCK_MAP_EXT.DATA[i]; i++)
	{
		Temp.Format("[%d] Extension Tag of Block No. %d in E-EDID: 0x%02X",(++CurrentByteNo), (2+i), BLOCK_MAP_EXT.DATA[i]);
		Text+=Temp;
		Text+="\r\n";

		Temp.Format("%d",CurrentByteNo);
		index=ListBox->InsertItem(++listcount,Temp);
		Temp.Format("0x%02X",BLOCK_MAP_EXT.DATA[i]);
		ListBox->SetItemText(index,1,Temp);
		Temp.Format("Extension Tag of Block No. %d in E-EDID",(2+i));
		ListBox->SetItemText(index,2,Temp);
	}
	 
	//*******************************Padding***************************************
	if(CurrentByteNo < 126 )	
	{
		if(CurrentByteNo < 125)		
			Temp.Format("%d-126", ++CurrentByteNo);
		else
			Temp.Format("%d", ++CurrentByteNo);

		index=ListBox->InsertItem(++listcount,Temp);
		Temp="";
				
		for(;i<126;i++)
		{
			CString strTemp;
			strTemp.Format("0x%02X, ",BLOCK_MAP_EXT.DATA[i]);
			Temp+=strTemp;
		}
		ListBox->SetItemText(index,1,Temp);
		ListBox->SetItemText(index,2,"Padding");
	}
	
	//***************************CHECK SUM**************************
		//Temp.Format("[%d]CheckSum\r\n\t", CurrentExtNo*128 + 127 );
		Text+="[127]CheckSum\r\n\t";
	
		BlockMapChecksum();
}
	

void BlockMapExtensionParser::BlockMapChecksum()
{	
	BYTE sum=0;
	CString Temp;
	
	for(INT i=0;i<128;i++)
	{
		sum+=*(BlockMapExt+i);
	}
	
	if(sum==0)
	{
		Text+="Block Map Check Sum OK!\r\n";
	}
	else
	{
		Text+="Block Map Check Sum Failed!\r\n";
	}

	INT index=ListBox->InsertItem(++listcount,"127");
	Temp.Format("0x%02X",*(BlockMapExt + 127) );
	ListBox->SetItemText(index,1,Temp);
	ListBox->SetItemText(index,2,"CheckSum");
	
}
//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////

/*****************************FUNCTIONS FOR EDID 1.4************************************/

//////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////

void EDID_BaseBlockParser::parsePowerMgmtFeatures1_4(_DISPLAY_FEATURES_SUPPORT1_4 DISPLAY_FEATURES_SUPPORT1_4,_VIDEO_INPUT_DEFN1_4 VIDEO_INPUT_DEFINITION1_4)
{
	
	Text+="\tPower Management Inforamtion:\r\n";
	
	//Check for Standby support

	
	if(DISPLAY_FEATURES_SUPPORT1_4.StandBy==0)
	{
		Text+="\t\tStand By Mode Is Not Supported\r\n";
	}
	

	if(DISPLAY_FEATURES_SUPPORT1_4.StandBy==1)
	{
		Text+="\t\tStand By Mode Is Supported\r\n";
	}

	//Check for Suspend support

	
	if(DISPLAY_FEATURES_SUPPORT1_4.Suspend==0)
	{
		Text+="\t\tSuspend Mode Is Not Supported\r\n";
	}
	

	if(DISPLAY_FEATURES_SUPPORT1_4.Suspend==1)
	{
		Text+="\t\tSuspend Mode Is Supported\r\n";
	}

	//Check for Active-Off support
	
	
	if(DISPLAY_FEATURES_SUPPORT1_4.ActiveOff_VeryLowPower==0)
	{
		Text+="\t\tActive Off Or Very Low Power Is Not Supported\r\n";
	}
	

	if(DISPLAY_FEATURES_SUPPORT1_4.ActiveOff_VeryLowPower==1)
	{
		Text+="\t\tActive Off Or Very Low Power Supported\r\n";
	}

	//Get Display Type
	if (VIDEO_INPUT_DEFINITION1_4.Analog_Digital == 0)
	{
		switch(DISPLAY_FEATURES_SUPPORT1_4.display_type)
		{
		case 0:Text+="\t\tMonochrome Or Gray Scale Display\r\n";break;
		case 1:Text+="\t\tRGB Color Display\r\n";break;
		case 2:Text+="\t\tNon-RGB Color Display\r\n";break;
		case 3:Text+="\t\tUndefined\r\n";break;
		} 
	}
	if(VIDEO_INPUT_DEFINITION1_4.Analog_Digital == 1)
	{
		switch(DISPLAY_FEATURES_SUPPORT1_4.display_type)
		{
		case 0:Text+="\t\tRGB 4.4.4\r\n";break;
		case 1:Text+="\t\tRGB 4.4.4 YCrCb 4.4.4\r\n";break;
		case 2:Text+="\t\tRGB 4.4.4 YCrCb 4.2.2\r\n";break;
		case 3:Text+="\t\tRGB 4.4.4 YCrCb 4.4.4 YCrCb 4.2.2\r\n";break;
		} 
	}
	//Check for Default Color Space

	
	if(DISPLAY_FEATURES_SUPPORT1_4.default_color_space==0)
	{
		Text+="\t\tsRGB Standard Is Not The Default Color Space\r\n";
	}
	


	if(DISPLAY_FEATURES_SUPPORT1_4.default_color_space==1)
	{
		Text+="\t\tsRGB Standard Is The Default Color Space\r\n";
	}

	//Check if Preferred Timing Mode is listed in the first Descriptor Block
	
	if(DISPLAY_FEATURES_SUPPORT1_4.pref_timing_mode==0)
	{
		Text+="\t\tPreferred Timing Mode Does Not Include The Native Pixel Format And Preffered Refresh Rate Of The Display Device\r\n";
	}
	

	if(DISPLAY_FEATURES_SUPPORT1_4.pref_timing_mode==1)
	{
		Text+="\t\tPreferred Timing Mode includes Native Pixel Format\r\n";
	}

	
	if(DISPLAY_FEATURES_SUPPORT1_4.continuos_frequency==1)
	{
		Text+="\t\tDisplay Is Continous Frequency\r\n";
	}
	else if(DISPLAY_FEATURES_SUPPORT1_4.continuos_frequency==0)
	{
		Text+="\t\tDisplay Is Non Continuos Frequency\r\n";
	}
	
}
void EDID_BaseBlockParser::parseYear_And_Week1_4(_YEAR_AND_WEEK_OF_MANUFACTURE1_4 YEAR_AND_WEEK_OF_MANUFACTURE1_4)
{
	//Parse Year and Week
	//Week in decimal value
	//Add 1990 + year to get the actual value
	
	CHAR *string=(CHAR *)malloc(256);

	if (YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture >= 1 && YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture <= 54)
	{
	
	sprintf_s(string,256,"[16],Week Of Manufacture: %d\r\n",YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture);
	Text+=string;

	}

	else if (YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture = 255)
	{
		Text+="[16],*****Model Year*****\r\n";
	}
	
	if (YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture != 255)
	{
		sprintf_s(string,256,"[17],Year of Manufacture: %d\r\n",(YEAR_AND_WEEK_OF_MANUFACTURE1_4.Year_Of_Manufacture+1990));
		Text+=string;
	}

	else if(YEAR_AND_WEEK_OF_MANUFACTURE1_4.Week_Of_Manufacture = 255)
	{
		sprintf_s(string,256,"[17],Model Year: %d\r\n",(YEAR_AND_WEEK_OF_MANUFACTURE1_4.Year_Of_Manufacture+1990));
		Text+=string;
	}
	free(string);
}
void EDID_BaseBlockParser::parseBasicDisplayParameters1_4(_YEAR_AND_WEEK_OF_MANUFACTURE1_4 YEAR_AND_WEEK_OF_MANUFACTURE1_4, _BASIC_DISPLAY_PARAMETERS1_4 BASIC_DISPLAY_PARAMETERS1_4)
{
	//Basic Display Parameters
	
	Text+="[20-24],Display Parameters\r\n";
	
	CHAR *string=(CHAR *)malloc(256);

	//First Byte, Video Input Definition
	parseVideoInputDefinition1_4(BASIC_DISPLAY_PARAMETERS1_4.VIDEO_INPUT_DEFN1_4);
	
	
		if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L > 1 && BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L < 255)
		{
			if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P == 0 )
			{
				if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 79)
				{
					Text+="\t16 : 9 AR in Landscape\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 61)
				{
					Text+="\t16 : 10 AR in Landscape\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 34)
				{
					Text+="\t\4 : 3 AR in Landscape\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 26)
				{
					Text+="\t5 : 4 AR in Landscape\r\n";
				}
				 
				
			}
		
			else if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P != 0 )
			{
					sprintf_s(string,256,"\tMaximum Horizontal Image Sizes: %d\r\n",BASIC_DISPLAY_PARAMETERS1_4.MAX_HORIZONTAL_SIZE);
					Text+=string;
			}
		}

		else if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 0 )
		{
			Text+="\tAspect Ratio(Portrait Orientation)\r\n";
		}
		
		if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P > 1 && BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P < 255)
		{
			if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L != 0)
			{
				sprintf_s(string,256,"\tMaximum Vertical Image Sizes: %d\r\n",BASIC_DISPLAY_PARAMETERS1_4.MAX_VERTICAL_SIZE);
				Text+=string;
			}
		

			else if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 0)
			{
					
				if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 79)
				{
					Text+="\t9 : 16 AR in Portrait\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 61)
				{
					Text+="\t10 : 16 AR in Portrait\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 34)
				{
					Text+="\t3 : 4 AR in Portrait\r\n";
				}
				else if(BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 26)
				{
					Text+="\t4 : 5 AR in Portrait\r\n";
				}
			}

		}
		else if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P == 0)
		{
				Text+="\tAspect Ratio(Landscape Orientation)\r\n";
		}

		
		if ( BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_L == 0 && BASIC_DISPLAY_PARAMETERS1_4.ASPECT_RATIO_P == 0 )
		{
			sprintf_s(string,256,"\tScreen Size Or Aspect Ratio Are Unknown Or Undefined\r\n");
			Text+=string;
		}
	
	
	//Display Gamma
	FLOAT gamma=BASIC_DISPLAY_PARAMETERS1_4.DISPLAY_GAMMA;
	gamma+=100;
	gamma/=100;
	
	sprintf_s(string,256,"\tDisplay Gamma Value: %f\r\n",gamma);
	Text+=string;
	
	//Power Management Features
	parsePowerMgmtFeatures1_4(BASIC_DISPLAY_PARAMETERS1_4.DISPLAY_FEATURES_SUPPORT1_4,BASIC_DISPLAY_PARAMETERS1_4.VIDEO_INPUT_DEFN1_4);
	free(string);
}
void EDID_BaseBlockParser::parseVideoInputDefinition1_4(_VIDEO_INPUT_DEFN1_4 VIDEO_INPUT_DEFINITION1_4)
{
	
	//Check if Display is Analog or Digital
	if(VIDEO_INPUT_DEFINITION1_4.Analog_Digital==0)
	{
		Text+="\tAnalog\r\n";
		
		//Check Signal Level Standard
		if(VIDEO_INPUT_DEFINITION1_4.signal_level_standard==0)
		{
			Text+="\t0.7,0.3\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION1_4.signal_level_standard==1)
		{
			Text+="\t0.714,0.286\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION1_4.signal_level_standard==2)
		{
			Text+="\t1.0,0.4\r\n";
		}
		else if(VIDEO_INPUT_DEFINITION1_4.signal_level_standard==3)
		{
			Text+="\t0.7,0.0\r\n";
		}

		
		if(VIDEO_INPUT_DEFINITION1_4.setup==0)
		{
			Text+="\t Blank Level = Black Level Setup\r\n";
		}
		

		//Check if it expects blank-black setup
		else if(VIDEO_INPUT_DEFINITION1_4.setup==1)
		{
			Text+="\tDisplay expects Blank-Black Setup\r\n";
		}
		
		//Check if it supports Separate syncs

		
		if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_3==0)
		{
			Text+="\tSeparate Syncs H & V Signals Are Not Supported\r\n";
		}
		

		else if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_3==1)
		{
			Text+="\tSeparate Syncs H & V Signals Are Supported\r\n";
		}
		
		//Check if it supports composite syncs

		
		if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2==0)
		{
			Text+="\tComposite Sync Signal On Horizontal Is Not Supported \r\n";
		}
		

		else if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2==1)
		{
			Text+="\tComposite Sync Signal On Horizontal Is Supported \r\n";
		}
		
		//Check if it supports Green Video Sync

		
		if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1==0)
		{
			Text+="\tComposite Sync Signal On Green Video Is Not Supported \r\n";
		}
		

		else if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1==1)
		{
			Text+="\tComposite Sync Signal On Green Video Is Supported \r\n";
		}
		
		//Check if Serration is supported
	
		if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP==0)
		{
			Text+="\tSerration On The Vertical Sync Is Not Supported \r\n";
		}

		else if(VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP==1)
		{
			Text+="\tSerration On The Vertical Sync Is Supported \r\n";
		}
		
	}
	//Check if its Digital
	else if(VIDEO_INPUT_DEFINITION1_4.Analog_Digital==1)
	{
		 
		Text+="\tDigital \r\n";
		
		//Check for Interface Compatibility
		
				BYTE temp = ((VIDEO_INPUT_DEFINITION1_4.signal_level_standard * 2) + VIDEO_INPUT_DEFINITION1_4.setup );
				if ( temp == 0)
				{
					Text+="\tColor Bit Depth is undefined\r\n";
				}
				else if ( temp == 1)
				{
					Text+="\t6 Bits per Primary Color\r\n";
				}
				else if ( temp == 2)
				{
					Text+="\t8 Bits per Primary Color\r\n";
				}
				else if ( temp == 3)
				{
					Text+="\t10 Bits per Primary Color\r\n";
				}
				else if ( temp == 4)
				{
					Text+="\t12 Bits per Primary Color\r\n";
				}
				else if ( temp == 5)
				{
					Text+="\t14 Bits per Primary Color\r\n";
				}
				else if ( temp == 6)
				{
					Text+="\t16 Bits per Primary Color\r\n";
				}
				else if ( temp == 7)
				{
					Text+="\tReserved\r\n";
				}
			
				
				if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_3 == 0)
				{

					if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 0)
					{
						Text+="\tDigital Interface Is Not Defined\r\n";
					}
					
					else if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 1)
					{
						Text+="\tDVI Is Supported\r\n";
					}

					else if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 1 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 0)
					{
						Text+="\tHDMI-a Is Supported\r\n";
					}

					else if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 1 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 1)
					{
						Text+="\tHDMI-b Is Supported\r\n";
					}

					else if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 1 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 0)
					{
						Text+="\tMDDI Is Supported\r\n";
					}

					else if ( VIDEO_INPUT_DEFINITION1_4.sync_input_supported_2 == 1 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_1 == 0 &&  VIDEO_INPUT_DEFINITION1_4.sync_input_supported_0_DFP == 1)
					{
						Text+="\tDisplay Port Is Supported\r\n";
					}
				}
	}
	  
}

void EDID_BaseBlockParser::parsedescriptor_block1_4(_DESCRIPTOR_BLOCK1_4 DESCRIPTOR_BLOCK1_4)
{
	if(DESCRIPTOR_BLOCK1_4.FLAGS[0]==0x00 && DESCRIPTOR_BLOCK1_4.FLAGS[1]==0x00)
	{
		//Text+="Descriptor Block Contains Data\r\n";
	}
	if(DESCRIPTOR_BLOCK1_4.START_FLAG==0)
	{
		//Text+="Descriptor Block Starts here\r\n";
	}
	
	//Check the Data Type Tag and call the appropriate function
	
	switch(DESCRIPTOR_BLOCK1_4.DATA_TYPE_TAG)
	{
	case 0xFF:parseSerialNumber(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xFE:parseASCIIString(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xFD:parseDisplay_range_limits1_4(DESCRIPTOR_BLOCK1_4.DISPLAY_RANGE_LIMIT_OFFSETS1_4,DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xFC:parseMonitorName(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xFB:parseColor_Point_info(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xFA:_STANDARD_TIMING_IDENTIFICATION STANDARD_TIMING_IDENTIFICATION;
		memcpy(&STANDARD_TIMING_IDENTIFICATION,DESCRIPTOR_BLOCK1_4.MON_DESC_DATA,13);
		parseStandard_timing_identification(STANDARD_TIMING_IDENTIFICATION,FALSE);
		break;
	case 0xF9:parseDisplay_color_management_data1_4(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xF8:parseCVT3_byte_timing_codes1_4(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	case 0xF7:parseEstablished_timings_III1_4(DESCRIPTOR_BLOCK1_4.MON_DESC_DATA);break;
	}

}

void EDID_BaseBlockParser::checkDescriptorBlock1_4(_DESCRIPTOR_BLOCK1_4 DESCRIPTOR_BLOCK)
{
	if(DESCRIPTOR_BLOCK.FLAGS[0]==0 && DESCRIPTOR_BLOCK.FLAGS[1]==0)
	{
		parsedescriptor_block1_4(DESCRIPTOR_BLOCK);
	}
	else
	{
		//Copy the DTD block on to a DB and call the appropriate. function
		_DETAILED_TIMING_DESCRIPTOR_BLOCK DETAILED_TIMING_DESCRIPTOR_BLOCK;
		memcpy(&DETAILED_TIMING_DESCRIPTOR_BLOCK,&DESCRIPTOR_BLOCK,18);
		if(DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_LSB>0x00 && DETAILED_TIMING_DESCRIPTOR_BLOCK.pixel_clock_MSB>0x00)
			parsedetailed_timing_descriptor(DETAILED_TIMING_DESCRIPTOR_BLOCK);
	}
}

void EDID_BaseBlockParser::parseDisplay_color_management_data1_4(CHAR *data)
{
	_COLOR_MANAGEMENT_DATA1_4 *COLOR_MANAGEMENT_DATA1_4;
	COLOR_MANAGEMENT_DATA1_4=(_COLOR_MANAGEMENT_DATA1_4 *)malloc(sizeof(_COLOR_MANAGEMENT_DATA1_4));
	memcpy(COLOR_MANAGEMENT_DATA1_4,data,sizeof(_COLOR_MANAGEMENT_DATA1_4));
	
	
	Text+="COLOR MANAGEMENT DATA\r\n";
	CHAR *string=(CHAR *)malloc(256);

	INT temp = ((((COLOR_MANAGEMENT_DATA1_4->RED_A3_MSB) << 8)) + (COLOR_MANAGEMENT_DATA1_4->RED_A3_LSB));

	sprintf_s(string,256,"RED A3 VALUE IS :%d\r\n",temp);
	Text+=string;
	
	temp = (((COLOR_MANAGEMENT_DATA1_4->RED_A2_MSB) << 8) + (COLOR_MANAGEMENT_DATA1_4->RED_A2_LSB));

	sprintf_s(string,256,"RED A2 VALUE IS :%d\r\n",temp);
	Text+=string;

	temp = (((COLOR_MANAGEMENT_DATA1_4->GREEN_A3_MSB) << 8) + (COLOR_MANAGEMENT_DATA1_4->GREEN_A3_LSB));

	sprintf_s(string,256,"GREEN A3 VALUE IS :%d\r\n",temp);
	Text+=string;

	temp = (((COLOR_MANAGEMENT_DATA1_4->GREEN_A2_MSB) << 8) + (COLOR_MANAGEMENT_DATA1_4->GREEN_A2_LSB));

	sprintf_s(string,256,"GREEN A2 VALUE IS :%d\r\n",temp);
	Text+=string;

	temp = (((COLOR_MANAGEMENT_DATA1_4->BLUE_A3_MSB) << 8) + (COLOR_MANAGEMENT_DATA1_4->BLUE_A3_LSB));

	sprintf_s(string,256,"BLUE A3 VALUE IS :%d\r\n",temp);
	Text+=string;

	temp = (((COLOR_MANAGEMENT_DATA1_4->BLUE_A2_MSB) << 8) + (COLOR_MANAGEMENT_DATA1_4->BLUE_A2_LSB));

	sprintf_s(string,256,"BLUE A2 VALUE IS :%d\r\n",temp);
	Text+=string;
	free(COLOR_MANAGEMENT_DATA1_4);
	free(string);
}

void EDID_BaseBlockParser::parseEstablished_timings_III1_4(CHAR *data)
{
	_ESTABLISHED_TIMING_SECTION_III1_4 *ESTABLISHED_TIMING_SECTION_III1_4;
	ESTABLISHED_TIMING_SECTION_III1_4=(_ESTABLISHED_TIMING_SECTION_III1_4 *)malloc(sizeof(_ESTABLISHED_TIMING_SECTION_III1_4));
	memcpy(ESTABLISHED_TIMING_SECTION_III1_4,data,sizeof(_ESTABLISHED_TIMING_SECTION_III1_4));
	
	
	Text+="ESTABLISHED TIMING SECTION III\r\n";
	CHAR *string=(CHAR *)malloc(256);

	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 1) == 1)
		Text+="1152 x 864 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 2) == 1)
		Text+="1024x768@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 4) == 1)
		Text+="800x600@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 8) == 1)
		Text+="848x480@60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 16) == 1)
		Text+="640x480@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 32) == 1)
		Text+="720x400@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 64) == 1)
		Text+="640x400@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_6 & 128) == 1)
		Text+="640x350@85 Hz\r\n";



	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 1) == 1)
		Text+="1280x1024@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 2) == 1)
		Text+="1280x1024@60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 4) == 1)
		Text+="1280x960@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 8) == 1)
		Text+="1280x960@60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 16) == 1)
		Text+="1280x768@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 32) == 1)
		Text+="1280x768@75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 64) == 1)
		Text+="1280x768@60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_7 & 128) == 1)
		Text+="1280x768@60 Hz\r\n";



	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 1) == 1)
		Text+="1400 x 1050 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 2) == 1)
		Text+="1400 x 1050 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 4) == 1)
		Text+="1400 x 1050 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 8) == 1)
		Text+="1440 x 900 @ 85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 16) == 1)
		Text+="1440 x 900 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 32) == 1)
		Text+="1440 x 900 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 64) == 1)
		Text+="1440 x 900 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_8 & 128) == 1)
		Text+="1360 x 768 @ 60 Hz\r\n";



	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 1) == 1)
		Text+="1600 x 1200 @ 70  Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 2) == 1)
		Text+="1600 x 1200 @ 65 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 4) == 1)
		Text+="1600 x 1200 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 8) == 1)
		Text+="1680 x 1050 @ 85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 16) == 1)
		Text+="1680 x 1050 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 32) == 1)
		Text+="1680 x 1050 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 64) == 1)
		Text+="1680 x 1050 @ 60 Hz (RB)\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_9 & 128) == 1)
		Text+="1400 x 1050 @ 85 Hz\r\n";



	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 1) == 1)
		Text+="1920 x 1200 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 2) == 1)
		Text+="1920 x 1200 @ 60 Hz (RB)\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 4) == 1)
		Text+="1856 x 1392 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 8) == 1)
		Text+="1856 x 1392 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 16) == 1)
		Text+="1792 x 1344 @ 75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 32) == 1)
		Text+="1792 x 1344 @ 60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 64) == 1)
		Text+="1600 x 1200 @ 85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_10 & 128) == 1)
		Text+="1600 x 1200 @ 75 Hz\r\n";




	if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_11 & 16) == 1)
		Text+="1920x1440@75 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_11 & 32) == 1)
		Text+="1920x1440@60 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_11 & 64) == 1)
		Text+="1920x1200@85 Hz\r\n";

	else if ((ESTABLISHED_TIMING_SECTION_III1_4 -> BYTE_11 & 128) == 1)
		Text+="1920x1200@85 Hz\r\n";

	free(ESTABLISHED_TIMING_SECTION_III1_4);
	free(string);
}

void EDID_BaseBlockParser::parseCVT3_byte_timing_codes1_4(CHAR *data)
{
	_CVT3_BYTE_CODE_DESCRIPTOR1_4 *CVT3_BYTE_CODE_DESCRIPTOR1_4;
	CVT3_BYTE_CODE_DESCRIPTOR1_4=(_CVT3_BYTE_CODE_DESCRIPTOR1_4 *)malloc(sizeof(_CVT3_BYTE_CODE_DESCRIPTOR1_4));
	memcpy(CVT3_BYTE_CODE_DESCRIPTOR1_4,data,sizeof(_CVT3_BYTE_CODE_DESCRIPTOR1_4));
	
	
	Text+="CVT3 BYTE CODE DESCRIPTOR\r\n";
	CHAR *string=(CHAR *)malloc(256);

	INT Addr_lines = (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[1] & 0xF0) << 4) + CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[0]);

	INT Value_stored = ((Addr_lines/2) - 1);

	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4 -> PRIORITY_1[1] & 0xc ) >> 2 ) == 0)

		Text+="4 : 3 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[1] & 0xc ) >> 2 ) == 1)

		Text+="16 : 9 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[1] & 0xc ) >> 2 ) == 2)

		Text+="16 : 10 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[1] & 0xc ) >> 2 ) == 3)

		Text+="15 : 9 AR \r\n";

	if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 0x60 ) >> 5 ) == 0) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))

		Text+="50 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))

		Text+="60 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 0x60 ) >> 5 ) == 2) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))

		Text+="75 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))

		Text+="85 Hz \r\n";


	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 1) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))
		Text+="60 Hz with reduced blanking (as per CVT Standard) is supported \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 2) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))
		Text+="85 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 4) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))
		Text+="75 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 8) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))
		Text+="60 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 16) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_1[2] & 128) == 0))
		Text+="50 Hz with standard blanking (CRT style) is supported\r\n";





	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4 -> PRIORITY_2[1] & 0xc ) >> 2 ) == 0)

		Text+="4 : 3 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[1] & 0xc ) >> 2 ) == 1)

		Text+="16 : 9 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[1] & 0xc ) >> 2 ) == 2)

		Text+="16 : 10 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[1] & 0xc ) >> 2 ) == 3)

		Text+="15 : 9 AR \r\n";

	if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 0x60 ) >> 5 ) == 0) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))

		Text+="50 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))

		Text+="60 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 0x60 ) >> 5 ) == 2) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))

		Text+="75 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))

		Text+="85 Hz \r\n";


	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 1) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))
		Text+="60 Hz with reduced blanking (as per CVT Standard) is supported \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 2) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))
		Text+="85 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 4) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))
		Text+="75 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 8) == 1)&& ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))
		Text+="60 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 16) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_2[2] & 128) == 0))
		Text+="50 Hz with standard blanking (CRT style) is supported\r\n";




	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4 -> PRIORITY_3[1] & 0xc ) >> 2 ) == 0)

		Text+="4 : 3 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[1] & 0xc ) >> 2 ) == 1)

		Text+="16 : 9 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[1] & 0xc ) >> 2 ) == 2)

		Text+="16 : 10 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[1] & 0xc ) >> 2 ) == 3)

		Text+="15 : 9 AR \r\n";

	if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 0x60 ) >> 5 ) == 0) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))

		Text+="50 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))

		Text+="60 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 0x60 ) >> 5 ) == 2) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))

		Text+="75 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))

		Text+="85 Hz \r\n";


	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 1) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))
		Text+="60 Hz with reduced blanking (as per CVT Standard) is supported \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 2) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))
		Text+="85 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 4) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0))
		Text+="75 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 8) == 1) && (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0)))
		Text+="60 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 16) == 1) && (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_3[2] & 128) == 0)))
		Text+="50 Hz with standard blanking (CRT style) is supported\r\n";



	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4 -> PRIORITY_4[1] & 0xc ) >> 2 ) == 0)

		Text+="4 : 3 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[1] & 0xc ) >> 2 ) == 1)

		Text+="16 : 9 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[1] & 0xc ) >> 2 ) == 2)

		Text+="16 : 10 AR \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[1] & 0xc ) >> 2 ) == 3)

		Text+="15 : 9 AR \r\n";

	if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 0x60 ) >> 5 ) == 0) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))

		Text+="50 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))

		Text+="60 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 0x60 ) >> 5 ) == 2) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))

		Text+="75 Hz \r\n";

	else if ((((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 0x60 ) >> 5 ) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))

		Text+="85 Hz \r\n";


	if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 1) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))
		Text+="60 Hz with reduced blanking (as per CVT Standard) is supported \r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 2) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))
		Text+="85 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 4) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))
		Text+="75 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 8) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))
		Text+="60 Hz with standard blanking (CRT style) is supported\r\n";

	else if (((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 16) == 1) && ((CVT3_BYTE_CODE_DESCRIPTOR1_4->PRIORITY_4[2] & 128) == 0))
		Text+="50 Hz with standard blanking (CRT style) is supported\r\n";
	free(CVT3_BYTE_CODE_DESCRIPTOR1_4);
	free(string);
}

void EDID_BaseBlockParser::parseDisplay_range_limits1_4(_DISPLAY_RANGE_LIMIT_OFFSETS1_4 offsetdata, CHAR *data)
{
	//Parse Monitor Range Limits
	
	_DISPLAY_RANGE_LIMIT_OFFSETS1_4 DISPLAY_RANGE_LIMIT_OFFSETS1_4 = offsetdata;
	_DISPLAY_RANGE_LIMITS1_4 *DISPLAY_RANGE_LIMITS1_4;
	DISPLAY_RANGE_LIMITS1_4=(_DISPLAY_RANGE_LIMITS1_4 *)malloc(sizeof(_DISPLAY_RANGE_LIMITS1_4));
	
	memcpy(DISPLAY_RANGE_LIMITS1_4,data,sizeof(_DISPLAY_RANGE_LIMITS1_4));
	
	
	Text+="Display Range Limits\r\n";
	
	CHAR *string=(CHAR *)malloc(256);
	
	if(DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_7 != 0 ||DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_6 != 0 || DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_5 != 0 || DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_4 != 0 )
	{
		//Text+="RESERVED:Do Not Use1\r\n";
	}
	else
	{
		BYTE temp = (((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_3) << 3) + ((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_2) << 2) + ((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_1) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_0));

		if (temp == 1 || temp == 4 || temp == 7 || temp == 9 || temp == 0xd)
		{
			//Text+="RESERVED:Do Not Use2\r\n";
		}
		else
		{
			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_1) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_0)) == 00)
			{
				Text+="Vertical Rate Offsets are Zero\r\n";
			}

			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_1) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_0)) == 10)
			{
				Text+="Max. Vertical Rate + 255 Hz offset; Min. Vertical Rate is not offset\r\n";
			}

			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_1) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_0)) == 11)
			{
				Text+="Max. Vertical Rate + 255 Hz offset; Min. Vertical Rate + 255 Hz offset\r\n";
			}

			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_3) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_2)) == 00)
			{
				Text+="Horizontal Rate Offsets are Zero\r\n";
			}

			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_3) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_2)) == 10)
			{
				Text+="Max. Horizontal Rate + 255 Hz offset; Min. Horizontal Rate is not offset\r\n";
			}

			if((((DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_3) << 1) + (DISPLAY_RANGE_LIMIT_OFFSETS1_4.bit_2)) == 11)
			{
				Text+="Max. Horizontal Rate + 255 Hz offset; Min. Horizontal Rate + 255 kHz offset\r\n";
			}
		}
	}
	//Minimum Vertical Rate
	sprintf_s(string,256,"\tMin. Vertical Rate:%d\r\n",DISPLAY_RANGE_LIMITS1_4->min_vert_rate);
	Text+=string;
	//Maximum Vertical Rate
	sprintf_s(string,256,"\tMax. Vertical Rate:%d\r\n",DISPLAY_RANGE_LIMITS1_4->max_vert_rate);
	Text+=string;
	//Minimum Horizontal Rate
	sprintf_s(string,256,"\tMin. Horizontal Rate:%d\r\n",DISPLAY_RANGE_LIMITS1_4->min_horz_rate);
	Text+=string;
	//Maximum Horizontal Rate
	sprintf_s(string,256,"\tMax. Horizontal Rate:%d\r\n",DISPLAY_RANGE_LIMITS1_4->max_horz_rate);
	Text+=string;
	//Maximum Pixel Clock
	sprintf_s(string,256,"\tMax. Pixel Clock:%d MHz\r\n",(DISPLAY_RANGE_LIMITS1_4->max_pixel_clock*10));
	Text+=string;
	
	//Check if Timing Formula is Supported
	if(DISPLAY_RANGE_LIMITS1_4->timing_formula_support==0x00)
	{
		Text+="\tNo Secondary Timing Formula Support\r\n";
	}
	else if(DISPLAY_RANGE_LIMITS1_4->timing_formula_support==0x02)
	{
		sprintf_s(string,256,"\tStart Frequency, %d Hz\r\n",(DISPLAY_RANGE_LIMITS1_4->start_freq/2));
		Text+=string;
		
		sprintf_s(string,256,"\tC, %d \r\n",(DISPLAY_RANGE_LIMITS1_4->byte_C*2));
		Text+=string;
		
		INT m=DISPLAY_RANGE_LIMITS1_4->MSB_M;
		m=m<<8;
		m=m|DISPLAY_RANGE_LIMITS1_4->LSB_M;
		sprintf_s(string,256,"\tM, %d \r\n",m);
		Text+=string;
		
		sprintf_s(string,256,"\tK, %d \r\n",DISPLAY_RANGE_LIMITS1_4->byte_K);
		Text+=string;
		
		sprintf_s(string,256,"\tJ, %d \r\n",(DISPLAY_RANGE_LIMITS1_4->byte_J*2));
		Text+=string;
	}	
	
	free(DISPLAY_RANGE_LIMITS1_4);
	free(string);
}