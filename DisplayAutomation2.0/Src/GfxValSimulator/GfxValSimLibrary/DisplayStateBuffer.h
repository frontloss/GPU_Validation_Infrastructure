#include <Windows.h>
#define MAX_SUPPORTED_PIPE 4

#pragma pack(push, SIMDRV_DSB_TRIGGER)
#pragma pack(1)

/* DSB trigger selection type */
typedef enum _SIMDRV_DSB_SELECTOR
{
    SIMDRV_DSB_SELECTOR_NONE = -1,
    SIMDRV_DSB_SELECTOR_PIPE,
    SIMDRV_DSB_SELECTOR_LACE,
    SIMDRV_DSB_SELECTOR_HDR,
    SIMDRV_DSB_SELECTOR_MAX
} SIMDRV_DSB_SELECTOR;

/* DSB trigger mode */
typedef enum _SIMDRV_DSB_TRIGGER_MODE
{
    SIMDRV_DSB_TRIGGER_MODE_NONE = 0,
    SIMDRV_DSB_TRIGGER_MODE_SYNC,
    SIMDRV_DSB_TRIGGER_MODE_ASYNC,
    SIMDRV_DSB_TRIGGER_MODE_OVERRIDE,
    SIMDRV_DSB_TRIGGER_MODE_APEND,
    SIMDRV_DSB_TRIGGER_MODE_MAX
} GVSTUB_DSB_TRIGGER_MODE;

/* DSB synchronization type */
typedef enum _SIMDRV_DSB_SYNC_TYPE
{
    SIMDRV_DSB_WAIT_FOR_NONE = 0,
    SIMDRV_DSB_WAIT_FOR_VBLANK,
    SIMDRV_DSB_WAIT_FOR_U_SEC,
    SIMDRV_DSB_WAIT_FOR_SCANLINES,
    SIMDRV_DSB_WAIT_FOR_SCANLINE_IN_RANGE,
    SIMDRV_DSB_WAIT_FOR_SCANLINE_OUT_OF_RANGE,
    SIMDRV_DSB_WAIT_FOR_POLL_REG,
} SIMDRV_DSB_SYNC_TYPE;

/* DSB Error Code */
typedef enum _SIMDRV_DSB_ERROR_CODE
{
    SIMDRV_DSB_SUCCESS                  = 0,
    SIMDRV_DSB_FAILED                   = 1,
    SIMDRV_DSB_MEMORY_ALLOCATION_FAILED = 2,
    SIMDRV_DSB_INVALID_MEMORY_ACCESS    = 3,
    SIMDRV_DSB_INVALID_PIPE             = 4,
    SIMDRV_DSB_TRIGGER_FAILED           = 5,
    SIMDRV_DSB_VERIFICATION_FAIEDL      = 6,
    SIMDRV_DSB_VALSIM_INIT_FAILED       = 7,
    SIMDRV_DSB_VALSIM_IOCTL_FAILED      = 8,
    SIMDRV_DSB_ERROR_UNDEFINED          = 9,
    /* All Error code must be before this */
    SIMDRV_DSB_ERROR_CODE_MAX = 10,
} SIMDRV_DSB_ERROR_CODE;

/* Structure defination for DSB offset value pair */
typedef struct _SIMDRV_OFFSET_DATA_PAIR
{
    ULONG Offset;
    ULONG Data;
} SIMDRV_OFFSET_DATA_PAIR;

/* Structure for DSB write with contiguous polling */
typedef struct _SIMDRV_DSB_POLL_ARGS
{
    ULONG PollOffset;
    ULONG PollValue;
    ULONG PollMask;
} SIMDRV_DSB_POLL_ARGS;

/* Structure defination for DSB pipe parameter */
typedef struct _SIMDRV_PIPE_ARGS
{
    ULONG                    PipeIndex;           // Pipe index will specify which DSB need to trigger
    ULONG                    IndexRegister;       // 3D Lut/Gamma index register
    ULONG                    IndexRegStartOffset; // Index register start offset
    SIMDRV_OFFSET_DATA_PAIR *pOffsetDataPair;     // Offset data pair
    ULONG                    DataCount;           // Offset data pair count
    ULONG                    ScanlineCountOffset; // Scanline count offset.
    ULONG                    FrameCountOffset;    // Frame count offset.
    ULONG                    DeltaFrameCount;     // Specify verification apply after how many frame.
} SIMDRV_PIPE_ARGS;

/* DSB buffer to trigger DSB per pipe */
typedef struct _SIMDRV_DSB_BUFFER_PIPE_ARGS
{
    SIMDRV_PIPE_ARGS        PipeArgs;              // DSB pipe args
    SIMDRV_DSB_SELECTOR     DsbSelection;          // DSB select type
    GVSTUB_DSB_TRIGGER_MODE DsbTriggerMode;        // DSB trigger mode
    SIMDRV_DSB_SYNC_TYPE    DsbSyncType;           // DSB synchronization type
    ULONG                   DsbSyncData;           // waiting time if Sync Type is DSB_WAIT_FOR_U_SEC (max time 6 sec) or Scanline Count
    SIMDRV_DSB_POLL_ARGS    DsbPollArgs;           // DSB polling args
    BOOLEAN                 IsAutoIncrement;       // Specify dsb write with auto mode or not
    BOOLEAN                 InterruptOnCompletion; // Specify whether HW will generate interrupt on completion or not.
    ULONG                   Delay;                 // Specify delay for DSB Verification
    SIMDRV_DSB_ERROR_CODE   Status;                // DSB trigger status
} SIMDRV_DSB_BUFFER_PIPE_ARGS;

typedef struct _SIMDRV_DSB_BUFFER_ARGS
{
    SIMDRV_DSB_BUFFER_PIPE_ARGS DsbBufferPipeArgs[MAX_SUPPORTED_PIPE]; // DSB Pipe Args
    ULONG                       NumDisplayPipe;                        // No of display pipe
} SIMDRV_DSB_BUFFER_ARGS;

#pragma pack(pop, SIMDRV_DSB_TRIGGER)
