#include<Windows.h>
#include<math.h>
#include<stdio.h>
#include<string.h>
#include <inttypes.h>

/* Macro to Unmask windows target id if OS is Win 10 or above we are masking windows target id
*  since win 10 onwords though driver reports 24 bit target id, OS enumerate as 28 bit target id. */
#define TARGET_ID_MASK				  0x00FFFFFF
#define UNMASK_TARGET_ID(a) (a & TARGET_ID_MASK)

//Local Method..
void printOutputTechnogy(int target , DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY   outputTechnologytoPrint);
void printRotationAngle(int target, DISPLAYCONFIG_ROTATION RotationAngle);
void printScaling(int target, DISPLAYCONFIG_SCALING DispScaling);
void printScanlineOrdering(int target, DISPLAYCONFIG_SCANLINE_ORDERING DispScanline);
void printtargetFlag(int target, UINT32 TargetFlag);
void printTopology(DISPLAYCONFIG_TOPOLOGY_ID DispTopology);
void printDispConfigTargetDeviceDetails(int target, UINT32 TargetId, LUID TargetadapterId);
void printDispConfigSourceDeviceDetails(int source, UINT32 SourceId, LUID SourceadapterId);
void printDispAdapterName(int source, UINT32 SourceId, LUID SourceadapterId);
void printTargetPreferredMode(int target, bool printpreferredtiming, UINT32 TargetId, LUID TargetadapterId);
void printPixelFormat(UINT32 num_path, DISPLAYCONFIG_PIXELFORMAT pixelFormat);
INT RefreshRateRoundOff(FLOAT float_rr);

//Main Program
void main()
{
	LONG returnValue = 0;

	UINT32 PathArraySize;
	UINT32 ModeArraySize;
	
	UINT32 sourcemodeindextoread = 0;
	UINT32 targetmodeindextoread = 0;
    UINT32 deskmodeinfoidxtoread = 0;

	DISPLAYCONFIG_PATH_INFO* PathArray = NULL;
	DISPLAYCONFIG_MODE_INFO* ModeArray = NULL;
	DISPLAYCONFIG_TOPOLOGY_ID CurrentTopology;
	DISPLAYCONFIG_RATIONAL vSyncFreq = { 0 };

	FLOAT ver_syncFreq = 0;
	INT roundedRR = 0;

	UINT32 qdc_flag = (QDC_DATABASE_CURRENT | QDC_VIRTUAL_MODE_AWARE);

	GetDisplayConfigBufferSizes(qdc_flag, &PathArraySize, &ModeArraySize);
    
    PathArray = (DISPLAYCONFIG_PATH_INFO*)calloc(PathArraySize, sizeof(DISPLAYCONFIG_PATH_INFO));
    ModeArray = (DISPLAYCONFIG_MODE_INFO*)calloc(ModeArraySize, sizeof(DISPLAYCONFIG_MODE_INFO));
    
    LONG ret = QueryDisplayConfig(qdc_flag, &PathArraySize, PathArray, &ModeArraySize, ModeArray, &CurrentTopology);

	if (ret == ERROR_SUCCESS) // The function succeeded.
	{
		printf("***************************************************************************\n ");
		printf("                     Query Display Configuration\n");
		printf("***************************************************************************\n ");
		printf("Total No of Path         : %d\n ", PathArraySize);
		printf("Total No of Mode Array   : %d\n ", ModeArraySize);
		printTopology(CurrentTopology);		//Print Topology Details..
		printf("\n");
		for (UINT32 numpath = 0; numpath < PathArraySize; numpath++)
		{
			printf("******************************Display Path : %d******************************\n ", numpath + 1);

			targetmodeindextoread = PathArray[numpath].targetInfo.targetModeInfoIdx;
			sourcemodeindextoread = PathArray[numpath].sourceInfo.sourceModeInfoIdx;
			deskmodeinfoidxtoread = PathArray[numpath].targetInfo.desktopModeInfoIdx;

			printf("PathSource Details:\n ");
			printf("\tSource - %d - Source ID               : %d\n ", numpath, PathArray[numpath].sourceInfo.id);
			printf("\tSource - %d - Target ID               : %d\n ", numpath, UNMASK_TARGET_ID(PathArray[numpath].targetInfo.id));
			printf("\tSource - %d - Adapter ID              : LowPart: %d HighPart: %d\n ", numpath, PathArray[numpath].sourceInfo.adapterId.LowPart, PathArray[numpath].sourceInfo.adapterId.HighPart);
			// Print Display Adaptar Name
			printDispAdapterName(numpath, PathArray[numpath].sourceInfo.id, PathArray[numpath].sourceInfo.adapterId);
			printf("\tSource - %d - Source CloneGroupID     : %d\n ", numpath, PathArray[numpath].sourceInfo.cloneGroupId);
			printPixelFormat(numpath, ModeArray[sourcemodeindextoread].sourceMode.pixelFormat);

			printf("PathTarget Details:\n ");
			printDispConfigTargetDeviceDetails(numpath, PathArray[numpath].targetInfo.id, PathArray[numpath].targetInfo.adapterId);
			
			// Other Target path info details.
			printRotationAngle(numpath, PathArray[numpath].targetInfo.rotation);
			printScaling(numpath, PathArray[numpath].targetInfo.scaling);
			printScanlineOrdering(numpath, PathArray[numpath].targetInfo.scanLineOrdering);
			printtargetFlag(numpath, PathArray[numpath].targetInfo.statusFlags);

			printf("Preferred Mode Details:\n ");
			printTargetPreferredMode(numpath, TRUE, PathArray[numpath].targetInfo.id, PathArray[numpath].targetInfo.adapterId);  // When detailed preferred timing will be printed when we set True.

			printf("SourceMode Details (Mode Index: %d):\n ", sourcemodeindextoread);
			printf("\tSource - %d - Source Mode             : %4d x %-4d \n ", numpath,
				ModeArray[sourcemodeindextoread].sourceMode.width, ModeArray[sourcemodeindextoread].sourceMode.height);
			printf("\tSource - %d - Source Position         : X = %-4d Y = %-4d \n ", numpath,
				ModeArray[sourcemodeindextoread].sourceMode.position.x, ModeArray[sourcemodeindextoread].sourceMode.position.y);

			printf("TargetMode Details (Mode Index: %d):\n ", targetmodeindextoread);
			
			vSyncFreq = ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.vSyncFreq;
			ver_syncFreq = (FLOAT)vSyncFreq.Numerator / vSyncFreq.Denominator;
			roundedRR = RefreshRateRoundOff(ver_syncFreq);

			printf("\tTarget - %d - Target Mode [Active]    : %4d x %-4d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.activeSize.cx,
																					   ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.activeSize.cy);
			printf("\tTarget - %d - Target Mode [Total]     : %4d x %-4d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.totalSize.cx,
																					   ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.totalSize.cy);
			printf("\tTarget - %d - VSync Numerator         : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.vSyncFreq.Numerator);
			printf("\tTarget - %d - VSync Denominator       : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.vSyncFreq.Denominator);
			printf("\tTarget - %d - Refresh Rate            : %.4f Hz (Rounded RR: %d)\n ", numpath, ver_syncFreq, roundedRR);
			printf("\tTarget - %d - HSync Numerator         : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.hSyncFreq.Numerator);
			printf("\tTarget - %d - HSync Denominator       : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.hSyncFreq.Denominator);
			printf("\tTarget - %d - Pixel Rate              : %I64d Hz\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.pixelRate);
			printf("\tTarget - %d - Video Standard          : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.videoStandard);
			printf("\tTarget - %d - Add. Video Standard     : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.AdditionalSignalInfo.videoStandard);
			printf("\tTarget - %d - Add. VSync Divider      : %d\n ", numpath, ModeArray[targetmodeindextoread].targetMode.targetVideoSignalInfo.AdditionalSignalInfo.vSyncFreqDivider);
			
			printf("DeskImageInfo Details (Mode Index: %d):\n ", deskmodeinfoidxtoread);

			printf("\tDskImg - %d - Path Source Size        : %4d x %-4d\n ", numpath, ModeArray[deskmodeinfoidxtoread].desktopImageInfo.PathSourceSize.x,
																					   ModeArray[deskmodeinfoidxtoread].desktopImageInfo.PathSourceSize.y);

			printf("\tDskImg - %d - Desktop Image Region    : T:%-4d L:%-4d R:%-4d B:%-4d\n ", numpath, ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageRegion.top,
																										ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageRegion.left,
																										ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageRegion.right,
																										ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageRegion.bottom);

			printf("\tDskImg - %d - Desktop image Clip      : %4d x %-4d\n ", numpath, ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageClip.right,
																					   ModeArray[deskmodeinfoidxtoread].desktopImageInfo.DesktopImageClip.bottom);

			if (PathArray[numpath].targetInfo.targetAvailable == TRUE)
			{
				printf("\nTarget - %d : Available (Connected)\n", numpath); 			//Target Available
			}
			else
			{
				printf("\nTarget - %d : Not Available (Disconnected)\n", numpath); 		//Target Not Availale
			}
			printf("----------------------------------------------------------------------------\n");
			printf("\n");
		}// PathArray For Loop
	} // if 
	else
	{
		printf("ONE OF THIS ERROR : ERROR_INVALID_PARAMETER /ERROR_NOT_SUPPORTED /ERROR_ACCESS_DENIED /	ERROR_GEN_FAILURE /	ERROR_INSUFFICIENT_BUFFER\n ");
	}
	printf("\n");
	printf("Error Value %d\n ", returnValue);

	free(PathArray);
	free(ModeArray);

} //Main end



//*************************************************************************
//     Local Function start 
//************************************************************************

INT RefreshRateRoundOff(FLOAT d_RefreshRate)
{
	/*	59.0  -59.5  ==>59, 
		59.5  -60.5  ==>60,
		59.94 -59.97 ==>59 */

	INT intPart = (INT)d_RefreshRate;
	if (intPart == 23 || intPart == 29 || intPart == 59 || intPart == 119)
	{
		FLOAT decPart = d_RefreshRate - intPart;
		if ((decPart >= 0.9345555 && decPart <= 0.9785500) || (decPart >= 0.00000000 && decPart <= 0.5000000))
			return intPart;
		else
			return (INT)ceilf(d_RefreshRate);
	}
	else
	{
		FLOAT roundRR;
		FLOAT temp = d_RefreshRate;
		temp = (FLOAT)(d_RefreshRate + 0.0555555);
		temp = roundf(temp * 100);
		roundRR = temp / 100;
		return (int)(roundRR);
	}
}

void printPixelFormat(UINT32 num_path, DISPLAYCONFIG_PIXELFORMAT pixelFormat)
{
	char pixel_format[200];

	switch (pixelFormat)
	{
	case DISPLAYCONFIG_PIXELFORMAT_8BPP:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_8BPP");
		break;
	case DISPLAYCONFIG_PIXELFORMAT_16BPP:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_16BPP");
		break;
	case DISPLAYCONFIG_PIXELFORMAT_24BPP:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_24BPP");
		break;
	case DISPLAYCONFIG_PIXELFORMAT_32BPP:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_32BPP");
		break;
	case DISPLAYCONFIG_PIXELFORMAT_NONGDI:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_NONGDI");
		break;
	default:
		strcpy_s(pixel_format, "DISPLAYCONFIG_PIXELFORMAT_UNKNOWN");
		break;
	}

	printf("\tSource - %d - Source Pixel Format     : %s\n ", num_path, pixel_format);
}

void printOutputTechnogy(int target ,DISPLAYCONFIG_VIDEO_OUTPUT_TECHNOLOGY outputTechnologytoPrint)
{
	char outputTech[200];
		
	if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_OTHER)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_OTHER");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HD15");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SVIDEO)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SVIDEO");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPOSITE_VIDEO)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPOSITE_VIDEO");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPONENT_VIDEO)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_COMPONENT_VIDEO");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DVI");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_HDMI");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_LVDS)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_LVDS");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_D_JPN)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_D_JPN");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDI)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDI");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EXTERNAL");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EMBEDDED)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_DISPLAYPORT_EMBEDDED");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EXTERNAL)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EXTERNAL");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EMBEDDED)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_UDI_EMBEDDED");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDTVDONGLE)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_SDTVDONGLE");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_MIRACAST)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_MIRACAST");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL");
	}
	else if (outputTechnologytoPrint == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32)
	{
		strcpy_s(outputTech, "DISPLAYCONFIG_OUTPUT_TECHNOLOGY_FORCE_UINT32");
	}
		
	//Print the Output Technology 
	printf("\tTarget - %d - Output Technology       : %s\n ",target, outputTech);
}

// ******************************************************************************************************

void printRotationAngle(int target, DISPLAYCONFIG_ROTATION RotationAngle)
{
	char outputrotangle[200];

	if (RotationAngle == DISPLAYCONFIG_ROTATION_IDENTITY)
	{
		strcpy_s(outputrotangle, "DISPLAYCONFIG_ROTATION_IDENTITY");
	}
	else if (RotationAngle == DISPLAYCONFIG_ROTATION_ROTATE90)
	{
		strcpy_s(outputrotangle, "DISPLAYCONFIG_ROTATION_ROTATE90");
	}
	else if (RotationAngle == DISPLAYCONFIG_ROTATION_ROTATE180)
	{
		strcpy_s(outputrotangle, "DISPLAYCONFIG_ROTATION_ROTATE180");
	}
	else if (RotationAngle == DISPLAYCONFIG_ROTATION_ROTATE270)
	{
		strcpy_s(outputrotangle, "DISPLAYCONFIG_ROTATION_ROTATE270");
	}
	else if (RotationAngle == DISPLAYCONFIG_ROTATION_FORCE_UINT32)
	{
		strcpy_s(outputrotangle, "DISPLAYCONFIG_ROTATION_FORCE_UINT32");
	}
	//Print the Rotation Angle 
	printf("\tTarget - %d - Rotation Angle          : %s\n ", target, outputrotangle);
}

// ******************************************************************************************************

void printScaling(int target, DISPLAYCONFIG_SCALING DispScaling)
{
	char outputscaling[200];

	if (DispScaling == DISPLAYCONFIG_SCALING_IDENTITY)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_IDENTITY");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_CENTERED)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_CENTERED");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_STRETCHED)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_STRETCHED");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_ASPECTRATIOCENTEREDMAX");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_CUSTOM)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_CUSTOM");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_PREFERRED)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_PREFERRED");
	}
	else if (DispScaling == DISPLAYCONFIG_SCALING_FORCE_UINT32)
	{
		strcpy_s(outputscaling, "DISPLAYCONFIG_SCALING_FORCE_UINT32");
	}
	//Print the Display Scaling 
	printf("\tTarget - %d - Display Scaling         : %s\n ", target, outputscaling);
}

// ******************************************************************************************************

void printScanlineOrdering(int target, DISPLAYCONFIG_SCANLINE_ORDERING DispScanline)
{
	char outputscanline[200];

	if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED");
	}
	else if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE");
	}
	else if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED");
	}
	// hence = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST = DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED,
	else if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED");
	}
	else if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST");
	}
	else if (DispScanline == DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32)
	{
		strcpy_s(outputscanline, "DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32");
	}
	
	//Print the Display Scan Line
	printf("\tTarget - %d - Display Scan Line       : %s\n ", target, outputscanline);
}

// ******************************************************************************************************

void printtargetFlag(int target, UINT32 TargetFlag)
{
	if ((DISPLAYCONFIG_TARGET_IN_USE & TargetFlag) == DISPLAYCONFIG_TARGET_IN_USE)
	{
		printf("\tTarget - %d - Target Flag             : DISPLAYCONFIG_TARGET_IN_USE\n ", target);
	}
	else if ((DISPLAYCONFIG_TARGET_FORCIBLE & TargetFlag) == DISPLAYCONFIG_TARGET_FORCIBLE)
	{
		printf("\tTarget - %d - Target Flag             : DISPLAYCONFIG_TARGET_FORCIBLE\n ", target);
	}
	else if ((DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_BOOT & TargetFlag) == DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_BOOT)
	{
		printf("\tTarget - %d - Target Flag             : DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_BOOT\n ", target);
	}
	else if ((DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_PATH & TargetFlag) == DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_PATH)
	{
		printf("\tTarget - %d - Target Flag             : DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_PATH\n ", target);
	}
	else if ((DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_SYSTEM & TargetFlag) == DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_SYSTEM)
	{
		printf("\tTarget - %d - Target Flag             : DISPLAYCONFIG_TARGET_FORCED_AVAILABILITY_SYSTEM\n ", target);
	}
}


// ******************************************************************************************************

void printTopology(DISPLAYCONFIG_TOPOLOGY_ID DispTopology)
{
	char outputtopology[200];

	if (DispTopology == DISPLAYCONFIG_TOPOLOGY_INTERNAL)
	{
		strcpy_s(outputtopology, "DISPLAYCONFIG_TOPOLOGY_INTERNAL");
	}
	else if (DispTopology == DISPLAYCONFIG_TOPOLOGY_CLONE)
	{
		strcpy_s(outputtopology, "DISPLAYCONFIG_TOPOLOGY_CLONE");
	}
	else if (DispTopology == DISPLAYCONFIG_TOPOLOGY_EXTEND)
	{
		strcpy_s(outputtopology, "DISPLAYCONFIG_TOPOLOGY_EXTEND");
	}
	
	else if (DispTopology == DISPLAYCONFIG_TOPOLOGY_EXTERNAL)
	{
		strcpy_s(outputtopology, "DISPLAYCONFIG_TOPOLOGY_EXTERNAL");
	}
	else if (DispTopology == DISPLAYCONFIG_TOPOLOGY_FORCE_UINT32)
	{
		strcpy_s(outputtopology, "DISPLAYCONFIG_TOPOLOGY_FORCE_UINT32");
	}
	
	//Print the Display Topology
	printf("Current Display Topology : %s\n", outputtopology);
}

// ******************************************************************************************************

void printDispConfigTargetDeviceDetails(int target ,UINT32 TargetId, LUID TargetadapterId)
{
	ULONG result;
	DISPLAYCONFIG_TARGET_DEVICE_NAME targetinfo;

	ZeroMemory(&targetinfo, sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME));
	targetinfo.header.size = sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME);

	targetinfo.header.adapterId = TargetadapterId;
	targetinfo.header.id = TargetId;
	targetinfo.header.type = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME;

	result = DisplayConfigGetDeviceInfo(&targetinfo.header);

	if (result == ERROR_SUCCESS)
	{
		printf("\tTarget - %d - Monitor Device Path     : %ls\n ", target, targetinfo.monitorDevicePath);
		if (targetinfo.outputTechnology == DISPLAYCONFIG_OUTPUT_TECHNOLOGY_INTERNAL)
			printf("\tTarget - %d - Friendly Device Name    : Built-in Display (eDP or MIPI)\n ", target);
		else
			printf("\tTarget - %d - Friendly Device Name    : %ls\n ", target, targetinfo.monitorFriendlyDeviceName);
		printOutputTechnogy(target, targetinfo.outputTechnology);
		printf("\tTarget - %d - Flag Value              : %d\n ", target,targetinfo.flags.value); //TBD - Need to parse.
		printf("\tTarget - %d - Connector Instance      : %d\n ", target, targetinfo.connectorInstance);
		printf("\tTarget - %d - EDID Manufacture ID     : %d\n ", target, targetinfo.edidManufactureId);
		printf("\tTarget - %d - EDID Product Code ID    : %d\n ", target, targetinfo.edidProductCodeId);
	}
}

// ******************************************************************************************************

void printDispConfigSourceDeviceDetails(int source, UINT32 SourceId, LUID SourceadapterId)
{
	ULONG result;
	DISPLAYCONFIG_SOURCE_DEVICE_NAME sourceInfo;

	ZeroMemory(&sourceInfo, sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME));
	sourceInfo.header.size = sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME);

	sourceInfo.header.adapterId = SourceadapterId;
	sourceInfo.header.id = SourceId;
	sourceInfo.header.type = DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME;

	result = DisplayConfigGetDeviceInfo(&sourceInfo.header);

	if (result == ERROR_SUCCESS)
	{
		printf("Source -%d - View GDI Device Path : %ls\n ", source, sourceInfo.viewGdiDeviceName);
	}
}

// ******************************************************************************************************

void printDispAdapterName(int source, UINT32 SourceId, LUID SourceadapterId)
{
	ULONG result;
	DISPLAYCONFIG_ADAPTER_NAME adapterInfo;

	ZeroMemory(&adapterInfo, sizeof(DISPLAYCONFIG_ADAPTER_NAME));
	adapterInfo.header.size = sizeof(DISPLAYCONFIG_ADAPTER_NAME);

	adapterInfo.header.adapterId = SourceadapterId;
	adapterInfo.header.id = SourceId;
	adapterInfo.header.type = DISPLAYCONFIG_DEVICE_INFO_GET_ADAPTER_NAME;

	result = DisplayConfigGetDeviceInfo(&adapterInfo.header);

	if (result == ERROR_SUCCESS)
	{
		printf("\tSource - %d - Adapter Name            : %ls\n ", source, adapterInfo.adapterDevicePath);
	}
}

// ******************************************************************************************************

void printTargetPreferredMode(int target, bool printpreferredtiming, UINT32 TargetId, LUID TargetadapterId)
{
	INT roundedRR = 0;
	FLOAT ver_syncFreq = 0;
	DISPLAYCONFIG_TARGET_PREFERRED_MODE preferredmodeInfo;
	
	ZeroMemory(&preferredmodeInfo, sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE));
	preferredmodeInfo.header.size = sizeof(DISPLAYCONFIG_TARGET_PREFERRED_MODE);

	preferredmodeInfo.header.adapterId = TargetadapterId;
	preferredmodeInfo.header.id = TargetId;
	preferredmodeInfo.header.type = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_PREFERRED_MODE;
	
	ULONG rc = DisplayConfigGetDeviceInfo(&preferredmodeInfo.header);

	if (rc == ERROR_SUCCESS)
	{
		printf("\tTarget - %d - Preferred Mode [Active] : %d x %d \n ", target, preferredmodeInfo.width, preferredmodeInfo.height);
		if (printpreferredtiming == TRUE)
		{
			ver_syncFreq = (FLOAT)preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator / preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator;
			roundedRR = RefreshRateRoundOff(ver_syncFreq);

			printf("\tTarget - %d - Preferred Mode [Total]  : %d x %d \n ", target,
				preferredmodeInfo.targetMode.targetVideoSignalInfo.totalSize.cx, preferredmodeInfo.targetMode.targetVideoSignalInfo.totalSize.cy);
			printf("\tTarget - %d - VSync Numerator         : %d \n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Numerator);
			printf("\tTarget - %d - VSync Denominator       : %d \n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.vSyncFreq.Denominator);
			printf("\tTarget - %d - Refresh Rate            : %.4f Hz (Rounded RR: %d)\n ", target, ver_syncFreq, roundedRR);
			printf("\tTarget - %d - HSync Numerator         : %d \n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Numerator);
			printf("\tTarget - %d - HSync Denominator       : %d \n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.hSyncFreq.Denominator);
			printf("\tTarget - %d - Pixel Rate              : %I64d Hz\n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.pixelRate);
			printf("\tTarget - %d - Video Standard          : %d\n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.videoStandard);
			printf("\tTarget - %d - Add. Video Standard     : %d\n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.videoStandard);
			printf("\tTarget - %d - Add. VSync Divider      : %d\n ", target, preferredmodeInfo.targetMode.targetVideoSignalInfo.AdditionalSignalInfo.vSyncFreqDivider);
		}
	}
}

// ------------------------------------------------------------
// Local Function - End
//-------------------------------------------------------------
