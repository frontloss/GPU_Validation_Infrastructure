#ifndef __HDMIINTERFACE_H__
#define __HDMIINTERFACE_H__

#include "..\\CommonCore\\PortingLayer.h"
#include "..\\CommonInclude\\ValSimCommonInclude.h"
#include "..\\CommonInclude\\DisplayDefs.h"
#include "GMBusInterface.h"

typedef struct _HDMI_INTERFACE
{
    PGMBUS_INTERFACE pstGMBusInterface;
} HDMI_INTERFACE, *PHDMI_INTERFACE;

#endif