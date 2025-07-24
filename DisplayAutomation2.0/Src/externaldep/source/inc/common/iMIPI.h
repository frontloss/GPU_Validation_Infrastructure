/*+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**
** Copyright (c) Intel Corporation (2013).
**
** INTEL MAKES NO WARRANTY OF ANY KIND REGARDING THE CODE.  THIS CODE IS LICENSED
** ON AN "AS IS" BASIS AND INTEL WILL NOT PROVIDE ANY SUPPORT, ASSISTANCE,
** INSTALLATION, TRAINING OR OTHER SERVICES.  INTEL DOES NOT PROVIDE ANY UPDATES,
** ENHANCEMENTS OR EXTENSIONS.  INTEL SPECIFICALLY DISCLAIMS ANY WARRANTY OF
** MERCHANTABILITY, NONINFRINGEMENT, FITNESS FOR ANY PARTICULAR PURPOSE, OR ANY
** OTHER WARRANTY.  Intel disclaims all liability, including liability for
** infringement of any proprietary rights, relating to use of the code. No license,
** express or implied, by estoppel or otherwise, to any intellectual property
** rights is granted herein.
**
**
** File Name: iMIPI.h
**
** Abstract:  MIPI defines
**
** Notes:
**
** Items In File:
**
**+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

#ifndef __IMIPI_H__
#define __IMIPI_H__

/////////////////////////////////////////////////////////
//
// MIPI Parameters
//

typedef union _MIPI_SENDPACKET_FLAGS {
    UCHAR ucValue;
    struct
    {
        UCHAR bPowerMode : 1;       // HS/LP Mode
        UCHAR ucVirtualChannel : 2; // VirtualChannel 0-3
        UCHAR ucPortType : 2;       // Port-A/Port-C
        UCHAR ucReserved1 : 3;      // Reserved
    };
} MIPI_SENDPACKET_FLAGS;

typedef enum _SB_MIPI_SEQUENCE_TYPE
{
    eMipiSequenceUndefined = 0,
    eMipiAssertResetPin,
    eMipiSequenceInitialDcsCmds,
    eMipiSequenceDisplayOn,
    eMipiSequenceDisplayOff,
    eMipiDeassertResetPin,
    eLfpBkltOn,
    eLfpBkltOff,
    eMipiTearOn,
    eMipiTearOff,
    eLfpPanelPowerOn,
    eLfpPanelPowerOff,
    eMipiSequenceTypeMax
} SB_MIPI_SEQUENCE_TYPE,
*PSB_MIPI_SEQUENCE_TYPE;

typedef enum _SB_MIPI_SEQ_ELEMENT
{
    eMipiSeqElementUndefined = 0,
    eMipiSeqElementSendPacket,
    eMipiSeqElementDelay,
    eMipiSeqElementGPIOProg,
    eMipiSeqElementI2CProg,
    eMipiSeqElementSPIProg,
    eMipiSeqElementPMICProg,
    eMipiSeqElementMax
} SB_MIPI_SEQ_ELEMENTS,
*PSB_MIPI_SEQ_ELEMENTS;

typedef enum _SB_GPIO_NUMBER_MAPPING
{
    eDSI_RESET = 0,
    eDSI_VIO_EN,
    eDSI_BKLT_EN,
    eDSI_AVEE_EN,
    eDSI_AVDD_EN,
    eDSI_GPIO_NUMBER_MAX
} SB_GPIO_NUMBER_MAPPING;

#endif