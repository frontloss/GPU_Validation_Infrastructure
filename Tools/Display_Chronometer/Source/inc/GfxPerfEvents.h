/*******************************************************************************
**
** Copyright (c) Intel Corporation (2012).
**
** DISCLAIMER OF WARRANTY
** NEITHER INTEL NOR ITS SUPPLIERS MAKE ANY REPRESENTATION OR WARRANTY OR
** CONDITION OF ANY KIND WHETHER EXPRESS OR IMPLIED (EITHER IN FACT OR BY
** OPERATION OF LAW) WITH RESPECT TO THE SOURCE CODE.  INTEL AND ITS SUPPLIERS
** EXPRESSLY DISCLAIM ALL WARRANTIES OR CONDITIONS OF MERCHANTABILITY OR
** FITNESS FOR A PARTICULAR PURPOSE.  INTEL AND ITS SUPPLIERS DO NOT WARRANT
** THAT THE SOURCE CODE IS ERROR-FREE OR THAT OPERATION OF THE SOURCE CODE WILL
** BE SECURE OR UNINTERRUPTED AND HEREBY DISCLAIM ANY AND ALL LIABILITY ON
** ACCOUNT THEREOF.  THERE IS ALSO NO IMPLIED WARRANTY OF NON-INFRINGEMENT.
** SOURCE CODE IS LICENSED TO LICENSEE ON AN 'AS IS' BASIS AND NEITHER INTEL
** NOR ITS SUPPLIERS WILL PROVIDE ANY SUPPORT, ASSISTANCE, INSTALLATION,
** TRAINING OR OTHER SERVICES.  INTEL AND ITS SUPPLIERS WILL NOT PROVIDE ANY
** UPDATES, ENHANCEMENTS OR EXTENSIONS.
**
** File Name: GfxPerfEvents.h
**
** Author(s): Nikhil nikhil
**
** Description: Contains the Intel Responsiveness Tool Data
**
*******************************************************************************/

#ifndef _GFX_PROFILE_

#define _GFX_PROFILE_

// enum values of the EVENTS
typedef enum _EVENT_NAME_PROFILING
{
    EVENT_UNINITIALIZED = 0,
    EVENT_ENTER_SLEEP = 1,
    EVENT_RESUME_FROM_SLEEP = 2,
    EVENT_ENTER_HIBERNATION = 3,
    EVENT_RESUME_FROM_HIBERNATION = 4,
    EVENT_MONITOR_TURN_OFF = 5,
    EVENT_MONITOR_TURN_ON = 6,
    EVENT_MODE_CHANGE = 7,
    EVENT_BOOT = 8,
	CUSTOM_EVENT = 9,
	EVENT_RESERVE1,
	EVENT_RESERVE2,
	EVENT_RESERVE3,
	EVENT_RESERVE4,
	EVENT_RESERVE5,
    MAX_PROFILING_EVENTS

}EVENT_NAME_PROFILING, *PEVENT_NAME_PROFILING;


//Structure holding the dependency of minimum number of calls each DDI comes during the course of an event. 
//Only when all the values store per DDI becomes 0, we can consider that the event is complete.
//As we know the start and end DDI, so this dependency will ensure that we got to the correct Start and End
//For Ex ,suppose Committ is the end DDI for any event, and we get 3 calls for it, 
//so in this case, intermediate dependency will ensure that we captured the last DDI not its second call.
typedef struct _DEPENDENCY_DDI_PROFILING
{
    union
    {
        struct
        {
            LONG32   lCommitNum               :   6;
            LONG32   lUpdateActiveVidpnNum    :   8;
            LONG32   lVisibilityNum           :   8;
            LONG32   lSetDispPowerNum         :   6;
            LONG32   lAdapterPowerNum         :   4;
        };
        ULONG32 ulValue;
    };

}DEPENDENCY_DDI_PROFILING, *PDEPENDENCY_DDI_PROFILING;



#endif _GFX_PROFILE_