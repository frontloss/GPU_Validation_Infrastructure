/**
 * @file		PcEscapes.h
 * @brief	This contains declarations of the functions and structures for PcEscapes.c
 *
 * @author	Ashish Tripathi
 */

/* Avoid multi inclusion of header file */
#pragma once

#include "PowerConsEscapes.h"
#include <d3dkmthk.h>

#define MINORESCAPEVERSION 1
#define DDRWESCAPEVERSION 1

typedef ULONGLONG ESC_PTR; // "Pointer" used in escape structs

/**
 * @brief         Generic macro for null pointer check
 * @param[in]     expr - Expression to check for null
 * @param[in]     msg  - runtime error message
 *
 * @return        void
 */
#define NULLPTRCHECK(expr, errorCode) \
    {                                 \
        if ((NULL == expr))           \
        {                             \
            errorCode = E_POINTER;    \
            return;                   \
        }                             \
    }

/**
 * @brief		Escape Code: Identifies the escape call. Based on escape code the DxgkDdiEscape(...)
 *		    will decide which escape code function to use to handle
 *			EscapeCb(...) or OsThunkDDIEscape(...) call.
 */
typedef enum _GFX_ESCAPE_CODE
{
    // DO NOT ADD NEGATIVE ENUMERATORS
    GFX_ESCAPE_CODE_DEBUG_CONTROL = 0L, // DO NOT CHANGE
    GFX_ESCAPE_DISPLAY_CONTROL,         // For all display escapes
    GFX_ESCAPE_CUICOM_CONTROL = GFX_ESCAPE_DISPLAY_CONTROL,
    GFX_ESCAPE_GMM_CONTROL,
    GFX_ESCAPE_CAMARILLO_CONTROL,
    GFX_ESCAPE_ROTATION_CONTROL,
    GFX_ESCAPE_PAVP_CONTROL,
    GFX_ESCAPE_UMD_GENERAL_CONTROL,
    GFX_ESCAPE_RESOURCE_CONTROL,
    GFX_ESCAPE_SOFTBIOS_CONTROL,
    GFX_ESCAPE_ACPI_CONTROL,
    GFX_ESCAPE_CODE_KM_DAF,
    GFX_ESCAPE_CODE_PERF_CONTROL,
    GFX_ESCAPE_IGPA_INSTRUMENTATION_CONTROL,
    GFX_ESCAPE_CODE_OCA_TEST_CONTROL,
    GFX_ESCAPE_AUTHCHANNEL,
    GFX_ESCAPE_SHARED_RESOURCE,
    GFX_ESCAPE_PWRCONS_CONTROL,
    GFX_ESCAPE_KMD,
    GFX_ESCAPE_DDE,
    GFX_ESCAPE_IFFS,
    GFX_ESCAPE_TOOLS_CONTROL, // Escape for Tools
    GFX_ESCAPE_ULT_FW,
    GFX_ESCAPE_HDCP_SRVC,
    GFX_ESCAPE_KM_GUC,
    GFX_ESCAPE_EVENT_PROFILING,
    GFX_ESCAPE_WAFTR,
    GFX_ESCAPE_KM_GUC_INTERNAL,
    GFX_ESCAPE_PSMI,
    GFX_ESCAPE_PERF_STATS = 100,
    GFX_ESCAPE_SW_DECRYPTION,
    GFX_ESCAPE_CHECK_PRESENT_DURATION_SUPPORT = 102,
    GFX_ESCAPE_GET_DISPLAYINFO_ESCAPE,
    GFX_ESCAPE_VIRTUAL_DISPLAYS,
    GFX_ESCAPE_SECURESPRITE_BANDWIDTH,

    GFX_MAX_ESCAPE_CODES // MUST BE LAST
} GFX_ESCAPE_CODE;

/**
@brief		Enum for PC Escape Operations
*/
typedef enum _PC_ESCAPE_OPERATION
{
    PC_ESCAPE_UNKNOWN = 0,
    PC_ESCAPE_CHANGE_FREQUENCY,
    PC_ESCAPE_GET_PLATFORM_FREQ_RANGE,
    PC_ESCAPE_SET_DRIVER_FREQ_RANGE,
    PC_ESCAPE_GET_NUM_OF_SUPPORTED_FREQUENCIES,
    PC_ESCAPE_GET_SUPPORTED_FREQUENCIES,
    PC_ESCAPE_SLICE_SHUTDOWN,       // Function obsolete or no longer supported
    PC_ESCAPE_ACCESS_IOSF_REGISTER, // Function obsolete or no longer supported
    PC_ESCAPE_GET_DFPS_INFO,
    PC_ESCAPE_GET_IPS_PCODE_SUPPORT, // Function obsolete or no longer supported
    PC_ESCAPE_OVERRIDE_POWER_GATING,
    PC_ESCAPE_GET_POWER_GATING_METRICS,
    PC_ESCAPE_GET_BURST_TURBO_INFO, // Function obsolete or no longer supported
    PC_ESCAPE_GET_POWER_GATING_CAPABILITY,
    PC_ESCAPE_SLPM_SET_PARAMETER,
    PC_ESCAPE_SLPM_UNSET_PARAMETER,
    PC_ESCAPE_SLPM_GET_PARAMETER,
    PC_ESCAPE_SLPM_DUMP_STATE_UNUSED,
    PC_ESCAPE_SLPM_SEND_EVENT,
    PC_ESCAPE_SLPM_RESET_PROFILING_UNUSED,
    PC_ESCAPE_ACCESS_GTMMIO_REGISTER,
    PC_ESCAPE_ACCESS_PCU_MAILBOX,
    PC_ESCAPE_ACCESS_MSR,
    PC_ESCAPE_GET_FREQ_AND_BACKLIGHT_INFO,
    PC_ESCAPE_GET_FEATURE_STATE,
    PC_ESCAPE_SET_FEATURE_STATE,
    PC_ESCAPE_DUMP_POWER_DATA,
    PC_ESCAPE_WRITE_PCU_MBX,
    PC_ESCAPE_READ_PCU_MBX,
    PC_ESCAPE_OVERRIDE_ALS_INFO,
    PC_ESCAPE_RUN_POWER_MAX_ULT,
    PC_ESCAPE_SLPM_PERF_MODE_CHANGE,

    PC_ESCAPE_MAX_OPERATIONS
} PC_ESCAPE_OPERATION;

/**
@brief		Enum for Error types encountered during escape execution
*/
typedef enum _PC_ESCAPE_ERROR_TYPE
{
    PC_ESCAPE_NO_ERROR = 0,
    PC_ESCAPE_INVALID_PARAMETER,
    PC_ESCAPE_OUT_OF_BOUNDS,
    PC_ESCAPE_OPERATION_NOT_IMPLEMENTED,
    PC_ESCAPE_PLATFORM_NOT_SUPPORTED,
    PC_ESCAPE_FEATURE_NOT_SUPPORTED,

    PC_ESCAPE_UNKNOWN_ERROR

} PC_ESCAPE_ERROR_TYPE;

/**
@brief		Structure definition for escape opcode details
*/
typedef struct _ESCAPE_OPCODES
{
    _In_ INT MajorEscapeCode;
    _In_ INT MinorEscapeCode;
    _In_ SHORT MinorInterfaceVersion;
    _In_ SHORT MajorInterfaceVersion;
} ESCAPE_OPCODES;

/**
@brief		Escape Structure Header
*/
typedef struct _GFX_ESCAPE_HEADER
{
    union {
        struct
        {
            UINT            Size;       // Size of operation specific data arguments
            UINT            CheckSum;   // ulong based sum of data arguments
            GFX_ESCAPE_CODE EscapeCode; // code defined for each independent component
            UINT            ulReserved;
        };
        // The new HEADER definition below is being added for the escape codes
        // in GFX_ESCAPE_CUICOM_CONTROL & GFX_ESCAPE_TOOLS_CONTROL
        struct
        {
            UINT            ulReserved1;
            WORD            usEscapeVersion;
            WORD            usFileVersion;
            GFX_ESCAPE_CODE ulMajorEscapeCode; // code defined for each independent component
            UINT            uiMinorEscapeCode; // Code defined for each sub component contained in the component
        };
    }; // ensure sizeof struct divisible by 8 to prevent padding on 64-bit builds
} GFX_ESCAPE_HEADER;

/**
@brief		structure for AlsOverride info
*/
typedef struct _PC_ESCAPE_ALS_OVERRIDE_DATA_IN
{
    _In_ BOOLEAN Override;
    _In_ ULONG Lux;
} PC_ESCAPE_ALS_OVERRIDE_DATA_IN;

/**
@brief		structure for data required in PC Escape
*/
typedef struct _PC_ESCAPE_INFO
{
    _In_ GFX_ESCAPE_HEADER Header;              // First member has to be Header
    _In_ PC_ESCAPE_OPERATION EscapeOperation;   // Escape Operation requested
    _Out_ PC_ESCAPE_ERROR_TYPE EscapeErrorType; // Error type encountered during escape processing

    _In_ ULONG DataInSize; // Size of DataIn
    _In_ ESC_PTR pDataIn;  // Pointer of escape-call related struct

    _In_ ULONG DataOutSize; // Size of DataOut
    _In_ ESC_PTR pDataOut;  // Pointer to escape-call related struct
} PC_ESCAPE_INFO;

/**
 * @brief						          Treat pBuffer as an array of unsigned long and
 *                                         calculate the sum of all values in the array.
 *									      Used to calculate simple check sum to make sure
 *										  that data passed to EscapeCall is data send by user mode or OGL driver.
 * @param[in]	pBuffer                   Pointer to the buffer
 * @param[in]	BufferSize                Buffer size in bytes
 * @return		ULONG                     Checksum
 */
ULONG SumOfBufferData(VOID *pBuffer, ULONG BufferSize);

/**
 * @brief									Driver Escapes for PowerCons.
 *											Set up data structure and send to driver
 * @param[in]	cbIn						Size of the PC_ESCAPE_INFO structure
 * @param[in]	pIn							required escape info struct for PC Escape operation
 * @param[out]	pErrorCode					contains error if any
 */
VOID PcDriverEscape(INT cbIn, VOID *pIn, HRESULT *pErrorCode);
