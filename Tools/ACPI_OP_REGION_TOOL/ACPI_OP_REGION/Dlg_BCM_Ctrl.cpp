// Dlg_BCM_Ctrl.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_BCM_Ctrl.h"
#include "stdlib.h"


// CDlg_BCM_Ctrl dialog

IMPLEMENT_DYNAMIC(CDlg_BCM_Ctrl, CDialog)

CDlg_BCM_Ctrl::CDlg_BCM_Ctrl(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_BCM_Ctrl::IDD, pParent)
{

}

CDlg_BCM_Ctrl::~CDlg_BCM_Ctrl()
{
}

void CDlg_BCM_Ctrl::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_BCM_CTRL, m_BCM_Ctrl);
}

void CDlg_BCM_Ctrl::Update(ACPIControlMethodManager m_ACPICMManager)
{
    ULONG ulACPIId = 0;
    char usStr[10];
    bool bRet = false;

    PACPI_BCL_OUTPUT pBCLOutput = NULL;
    ULONG ulBlcVal = 0;

    pBCLOutput = (PACPI_BCL_OUTPUT) malloc (sizeof(ACPI_BCL_OUTPUT) + 0x100);

    //Reset Content
    m_BCM_Ctrl.ResetContent();

    bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICE_BRIGHTNESS_LEVELS,
        0, sizeof(ACPI_BCL_OUTPUT) + 0x100, 
        NULL, (PVOID) pBCLOutput);    
    

    if((bRet) && ((pBCLOutput->ulNumBclLevels >= 2)))
    {
        for(int i = 2  ; i < (pBCLOutput->ulNumBclLevels - 2) ; i++)
        {
            _ultoa(pBCLOutput->ulBclLevelOther[i-2], usStr, 10);
            m_BCM_Ctrl.AddString((LPCTSTR)(CString)usStr);
            m_BCM_Ctrl.SetItemData(i-2,pBCLOutput->ulBclLevelOther[i-2]);
        }
    }

    UpdateData(FALSE);
}

void CDlg_BCM_Ctrl::Eval(ACPIControlMethodManager m_ACPICMManager)
{
    ACPI_BCM_INPUT stBCMIn = {0};

    ZeroMemory(&stBCMIn, sizeof(ACPI_DOS_INPUT));
    
    ULONG ulBCMIndex = m_BCM_Ctrl.GetCurSel();;
    stBCMIn.ulBclLevel = m_BCM_Ctrl.GetItemData(ulBCMIndex);

  
    m_ACPICMManager.EvaluateControlMethod(
        ESC_ACPI_SET_DEVICE_BRIGHTNESS_LEVELS,
        sizeof(ACPI_BCM_INPUT),
        0,
        (PVOID) &stBCMIn,
        NULL);

    UpdateData(FALSE);
}




BEGIN_MESSAGE_MAP(CDlg_BCM_Ctrl, CDialog)
END_MESSAGE_MAP()


// CDlg_BCM_Ctrl message handlers
