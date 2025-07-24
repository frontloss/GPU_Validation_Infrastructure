// DGS_List.cpp : implementation file
//


#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "DGS_List.h"
#include "stdlib.h"


#define MAX_DEVICES 8

// CDGS_List dialog

IMPLEMENT_DYNAMIC(CDGS_List, CDialog)

CDGS_List::CDGS_List(CWnd* pParent /*=NULL*/)
	: CDialog(CDGS_List::IDD, pParent)
{

}

CDGS_List::~CDGS_List()
{
    
}


void CDGS_List::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_DGS_LIST, m_DGSListCtrl);
}

void CDGS_List::Update(ACPIMbxManager m_ACPIMailboxManager,
                       ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    char ucACPIID[100];
    char ucACPIIDDesc[500];
    char Data[200];
    char ucStatus[10];
    char temp[10];
    ACPI30_DOD_ID ulACPIId = {0};
    static boolean uiDone = false;

    m_DGSListCtrl.DeleteAllItems();

	
    if(false == uiDone)
    {
        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 120;
	    lvColumn.pszText = L"ACPI ID";
        m_DGSListCtrl.InsertColumn(0, &lvColumn);

	    lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 175;
	    lvColumn.pszText = L"Description";
	    m_DGSListCtrl.InsertColumn(1, &lvColumn);

	    lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 80;
	    lvColumn.pszText = L"Output";
	    m_DGSListCtrl.InsertColumn(2, &lvColumn);

        uiDone = true;
    }

	LVITEM lvItem;
	int nItem;

    ACPI_DGS_ARGS stDGSInput = {0};
    ULONG stDGSOutput = ACPI_CHILD_DESIRED_INACTIVE;

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        ulACPIId.ulId = m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId;
        bool bRet = false;

        if(0 == ulACPIId.ulId)
        {
            break;
        }

        //Clear the list control
        //m_DGSListCtrl.DeleteAllItems();

        //Fill Data in the List Control
        _ultoa(ulACPIId.ulId, ucACPIID, 16);

        m_DGSListCtrl.InsertItem(i, (LPCTSTR)(CString)ucACPIID);

        /////Conversion code
        switch(ulACPIId.Type)
        {
        case 0:
            strcpy(Data,"Display Type:\r\nOther");
            break;
        case 1:
            strcpy(Data,"Display Type:\r\nVGA CRT / Analog Monitor");
            break;
        case 2:
            strcpy(Data,"Display Type:\r\nTV/HDTV");
            break;
        case 3:
            strcpy(Data,"Display Type:\r\nExternal Digital Monitor");
            break;
        case 4:
            strcpy(Data,"Display Type:\r\nInternal or Integrated Digital Flat Panel");
            break;
        default:
            strcpy(Data,"Display Type:\r\nOther");
            break;
        }

        _ultoa(ulACPIId.Idx, temp, 10);
        strcat(Data," Index: ");
        strcat(Data,temp);

        //End of conversion code...
        
        m_DGSListCtrl.SetItemText(i, 1, (LPCTSTR)(CString)Data);



        //m_DGSListCtrl.SetItemText(i, 1, (LPCTSTR)(CString)ucACPIID);

        //Fill Input Buffer
        stDGSInput.ulAcpiID = ulACPIId.ulId;
        stDGSInput.eDesiredState = ACPI_CHILD_DESIRED_INACTIVE;

        stDGSOutput = ACPI_CHILD_DESIRED_INACTIVE;

        

        //Evaluate _DGS for each Child Device
        bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICE_NEXT_DESIRED_STATE,
            sizeof(ACPI_DGS_ARGS), sizeof(ACPI_DGS_OUTPUT), 
            (PVOID) &stDGSInput, (PVOID) &stDGSOutput);

        if(bRet == true)
        {
            stDGSOutput = stDGSOutput & 0xFF;
                                                  
            if(stDGSOutput)
            {
	            m_DGSListCtrl.SetItemText(i, 2, L"ON");
            }
            else
            {
                m_DGSListCtrl.SetItemText(i, 2, L"OFF");
            }
        }
        else
        {
            m_DGSListCtrl.SetItemText(0, 2, L"FAILED");

        }

    }
}



BEGIN_MESSAGE_MAP(CDGS_List, CDialog)

END_MESSAGE_MAP()


// CDGS_List message handlers



void CDGS_List::Eval(ACPIMbxManager m_ACPIMailboxManager,
                ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    char ucACPIID[100];
    char Data[200];
    char temp[10];
    ACPI30_DOD_ID ulACPIId = {0};
    static boolean uiDone = false;

    m_DGSListCtrl.DeleteAllItems();

	
    if(false == uiDone)
    {
        lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 120;
	    lvColumn.pszText = L"ACPI ID";
        m_DGSListCtrl.InsertColumn(0, &lvColumn);

	    lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 175;
	    lvColumn.pszText = L"Description";
	    m_DGSListCtrl.InsertColumn(1, &lvColumn);

	    lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	    lvColumn.fmt = LVCFMT_LEFT;
	    lvColumn.cx = 80;
	    lvColumn.pszText = L"Output";
	    m_DGSListCtrl.InsertColumn(2, &lvColumn);

        uiDone = true;
    }

    ACPI_DGS_ARGS stDGSInput = {0};
    ULONG stDGSOutput = ACPI_CHILD_DESIRED_INACTIVE;

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        ulACPIId.ulId = m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId;
        bool bRet = false;

        if(0 == ulACPIId.ulId)
        {
            break;
        }

        //Clear the list control
        //m_DGSListCtrl.DeleteAllItems();

        //Fill Data in the List Control
        _ultoa(ulACPIId.ulId, ucACPIID, 16);

        m_DGSListCtrl.InsertItem(i, (LPCTSTR)(CString)ucACPIID);

        /////Conversion code
        switch(ulACPIId.Type)
        {
        case 0:
            strcpy(Data,"Display Type:\r\nOther");
            break;
        case 1:
            strcpy(Data,"Display Type:\r\nVGA CRT / Analog Monitor");
            break;
        case 2:
            strcpy(Data,"Display Type:\r\nTV/HDTV");
            break;
        case 3:
            strcpy(Data,"Display Type:\r\nExternal Digital Monitor");
            break;
        case 4:
            strcpy(Data,"Display Type:\r\nInternal or Integrated Digital Flat Panel");
            break;
        default:
            strcpy(Data,"Display Type:\r\nOther");
            break;
        }

        _ultoa(ulACPIId.Idx, temp, 10);
        strcat(Data," Index: ");
        strcat(Data,temp);

        //End of conversion code...
        
        m_DGSListCtrl.SetItemText(i, 1, (LPCTSTR)(CString)Data);



        //m_DGSListCtrl.SetItemText(i, 1, (LPCTSTR)(CString)ucACPIID);

        //Fill Input Buffer
        stDGSInput.ulAcpiID = ulACPIId.ulId;
        stDGSInput.eDesiredState = ACPI_CHILD_DESIRED_INACTIVE;

        stDGSOutput = ACPI_CHILD_DESIRED_INACTIVE;

        

        //Evaluate _DGS for each Child Device
        bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICE_NEXT_DESIRED_STATE,
            sizeof(ACPI_DGS_ARGS), sizeof(ACPI_DGS_OUTPUT), 
            (PVOID) &stDGSInput, (PVOID) &stDGSOutput);

        if(bRet == true)
        {
            stDGSOutput = stDGSOutput & 0xFF;
                                                  
            if(stDGSOutput)
            {
	            m_DGSListCtrl.SetItemText(i, 2, L"ON");
            }
            else
            {
                m_DGSListCtrl.SetItemText(i, 2, L"OFF");
            }
        }
        else
        {
            m_DGSListCtrl.SetItemText(0, 2, L"FAILED");

        }

    }
}