#pragma once

#pragma pack(push, ACPI_MBX)
#pragma pack(1) 

/*typedef union _ACPI30_DOD_ID {
    ULONG ulId;
    struct {
        unsigned int Idx:4; // Display index
        unsigned int Port:4;// Port index
        unsigned int Type:4;// Display type
        unsigned int Rsvd1512:4;// Reserved bits 15:12
        
        unsigned int BiosDetectable:1; // BIOS can detect the device
        unsigned int NonVgaOut:1; // Non-VGA output device like TV tuner
        unsigned int Pipe:3;// For Multi-head devices, specifies pipe ID
        unsigned int Rsvd3021:10; // Reserved bits 30:21
        unsigned int Acpi30Defn:1; // 1 - indicates this style defn, 0 - custom
    };
} ACPI30_DOD_ID, *PACPI30_DOD_ID;*/

typedef struct _ACPI_MBX
{
    ULONG ulDriverReadiness;
    ULONG ulNotificationStatus;
    ULONG ulCurrentEvent;
    ULONG ulRsvd[5];
    ACPI30_DOD_ID stSupportedDisplayList[8];
    ACPI30_DOD_ID stAttachedDisplayList[8];
    ACPI30_DOD_ID stActiveDisplayList[8];
    ACPI30_DOD_ID stNextActiveDisplayList[8];
    ULONG ulASLSleepTimeOut;
    ULONG ulToggleTableIndex;
    ULONG ulCurrentHotPlugIndicator;
    ULONG ulCurrentLidStatus;
    ULONG ulCurrentDockStatus;
    ULONG ulSxSW;
    ULONG ulEVTS;
    ULONG ulCNOT;
    ULONG ulDriverStatus;
    ULONG RSVD[15];

}ACPI_MBX, *PACPI_MBX;

typedef union __ASLE_INT_CMD
{
    struct{
    unsigned int ALSEvent      :1;  // Indicate ALS Event  BIT0
    unsigned int BLCEvent      :1;  // Indicate BLC Event  BIT1
    unsigned int PFITEvent     :1;  // Indicate PFIT Event BIT2
    unsigned int Reserved      :7;  // Reserved BIT3-BIT9
    unsigned int ALSReturn     :2;  // Driver Response for ALS  BIT10-BIT11
    unsigned int BLCReturn     :2;  // Driver Response for BLC  BIT12-BIT13
    unsigned int PFITReturn    :2;  // Driver Response for PFIT BIT14-BIT15 
    unsigned int Reserved2     :16; // Reserved BIT16-BIT31
    };
    ULONG ulValue;
}ASLE_INT_CMD, *PASLE_INT_CMD;


typedef union __TCHE_FLD
{
    struct{
    unsigned int ALSEvent      :1;  // Indicate ALS Event  BIT0
    unsigned int BLCEvent      :1;  // Indicate BLC Event  BIT1
    unsigned int PFITEvent     :1;  // Indicate PFIT Event BIT2
    unsigned int Reserved      :29;  // Reserved BIT3-BIT31
    };
    ULONG ulValue;
}TCHE_FLD, *PTCHE_FLD;


typedef union __ARDY_DRIVER_READINESS
{
    struct{
    unsigned int ARDY          :1;  // Indicate Driver readiness
    unsigned int Reserved      :15;  // reserved fields
    unsigned int NotReadyReason     :16;  // Reason why driver is not ready
    };
    ULONG ulValue;
}ARDY_DRIVER_READINESS, *PARDY_DRIVER_READINESS;


typedef union __PFIT_FIELD
{
    struct{
    unsigned int Centering          :1;  // Indicate Centering Request
    unsigned int TextModeStretch    :1;  // Indicate Text Mode streaching request
    unsigned int GfxModeStretch     :1;  // Indicate Graphics Mode Streaching Request
    unsigned int Reserved           :28; // Reserved
    unsigned int FieldValidBit      :1;  // Tells Whether Other Bits are valid
    };
    ULONG ulValue;
}PFIT_FIELD, *PPFIT_FIELD;


typedef union __BLC_FIELD
{
    struct{
    unsigned int BackLightBrightness          :31;  // Indicate Brightness level
    unsigned int FieldValidBit                :1;   // Tells Whether Other Bits are valid
    };
    ULONG ulValue;
}BLC_FIELD, *PBLC_FIELD;

typedef union __ALS_FIELD
{
    struct{
    unsigned int ALSData          :32;  // ALS data
    };
    ULONG ulValue;
}ALS_FIELD, *PALS_FIELD;


typedef struct _BIOSDRIV_MBX
{
    ARDY_DRIVER_READINESS ulDriverReadiness;
    ASLE_INT_CMD ulASLEIntCommand;
    TCHE_FLD ulTCHE;
    ALS_FIELD ulALSReading;
    BLC_FIELD ulBacklightBrightness;
    PFIT_FIELD ulPFIT;
    BLC_FIELD ulCurrentBrightness;
    ULONG ulRsvd[57];
}BIOSDRIV_MBX, *PBIOSDRIV_MBX;


#pragma pack()
#pragma pack(pop, ACPI_MBX)

class ACPIMbxManager
{
public:
    //Variables
    bool bMailboxValid;
    unsigned long ulMbxSize;
    ACPI_MBX stACPIMbx;
    BIOSDRIV_MBX stBiosDriverMailbox;
    ACPIMbxManager(void);
    bool ACPIMbxManager::GetMailboxData(void);
    OPREG_Escape esc ;
public:
    ~ACPIMbxManager(void);
};
