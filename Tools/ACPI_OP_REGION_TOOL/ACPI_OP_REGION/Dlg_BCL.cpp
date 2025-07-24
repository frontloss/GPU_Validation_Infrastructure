// Dlg_BCL.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_BCL.h"
#include "stdlib.h"


// CDlg_BCL dialog

IMPLEMENT_DYNAMIC(CDlg_BCL, CDialog)

CDlg_BCL::CDlg_BCL(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_BCL::IDD, pParent)
    , m_BCLCtrl(0)
{

}

CDlg_BCL::~CDlg_BCL()
{
}

void CDlg_BCL::Update(ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    char ucACPIID[100];
    char ucACPIIDDesc[500];
    char ucStatus[10];
    ULONG ulACPIId = 0;
    char ucBuffer[200];
    char ucTempBuffer[20];

    lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	lvColumn.fmt = LVCFMT_LEFT;
	lvColumn.cx = 120;
	lvColumn.pszText = L"Title";
    m_BCLListCtrl.InsertColumn(0, &lvColumn);

	lvColumn.mask = LVCF_FMT | LVCF_TEXT | LVCF_WIDTH;
	lvColumn.fmt = LVCFMT_LEFT;
	lvColumn.cx = 175;
	lvColumn.pszText = L"Brightness levels (%)";
	m_BCLListCtrl.InsertColumn(1, &lvColumn);


	LVITEM lvItem;
	int nItem;

    bool bRet = false;

    ACPI_BCL_OUTPUT stBCLOutput = {0};
    ULONG ulBlcVal = 0;


    //Evaluate _DGS for each Child Device
    bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICE_BRIGHTNESS_LEVELS,
        0, sizeof(ACPI_BCL_OUTPUT), 
        NULL, (PVOID) &stBCLOutput);    

    if((bRet) && ((stBCLOutput.ulNumBclLevels >= 2)))
    {
        
        m_BCLListCtrl.InsertItem(0, L"Brightness(AC)");
        _ultoa((ULONG) stBCLOutput.ulBclLevelAC, ucBuffer, 10);
        m_BCLListCtrl.SetItemText(0, 1, (LPCTSTR)(CString)ucBuffer);
        strcpy(ucBuffer, "");

        m_BCLListCtrl.InsertItem(1, L"Brightness(DC)");
        _ultoa((ULONG) stBCLOutput.ulBclLevelDC, ucBuffer, 10);
        m_BCLListCtrl.SetItemText(1, 1, (LPCTSTR)(CString)ucBuffer);
        strcpy(ucBuffer, "");



        for(int i = 2  ; i < (stBCLOutput.ulNumBclLevels - 2) ; i++)
        {
            _ultoa((ULONG) stBCLOutput.ulBclLevelOther[i-2], ucTempBuffer, 10);
            strcat(ucBuffer, " ");
            strcat(ucBuffer, ucTempBuffer);
        }

        m_BCLListCtrl.InsertItem(2, L"Other levels");
        m_BCLListCtrl.SetItemText(2, 1, (LPCTSTR)(CString)ucBuffer);


    }


/*    ULONG   ulBclLevelAC;   // BCL Level when on AC power
    ULONG   ulBclLevelDC;   // BCL Level when on DC power
    ULONG   ulBclLevelOther[ANYSIZE_ARRAY]; // Other intermediate BCL levels */
    

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        ulACPIId = m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId;
        bool bRet = false;

        if(0 == ulACPIId)
        {
            break;
        }

        //Clear the list control
        m_DGSListCtrl.DeleteAllItems();

        //Fill Data in the List Control
        _ultoa(ulACPIId, ucACPIID, 16);

        m_DGSListCtrl.InsertItem(i, (LPCTSTR)(CString)ucACPIID);
        m_DGSListCtrl.SetItemText(i, 1, (LPCTSTR)(CString)ucACPIID);

        //Fill Input Buffer
        stDGSInput.ulAcpiID = ulACPIId;
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


void CDlg_BCL::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}


BEGIN_MESSAGE_MAP(CDlg_BCL, CDialog)
END_MESSAGE_MAP()


// CDlg_BCL message handlers
