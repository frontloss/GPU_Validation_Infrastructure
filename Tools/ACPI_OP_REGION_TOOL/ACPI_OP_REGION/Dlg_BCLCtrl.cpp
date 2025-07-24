// Dlg_BCLCtrl.cpp : implementation file
//


#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_BCLCtrl.h"
#include "stdlib.h"


// CDlg_BCLCtrl dialog

IMPLEMENT_DYNAMIC(CDlg_BCLCtrl, CDialog)

CDlg_BCLCtrl::CDlg_BCLCtrl(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_BCLCtrl::IDD, pParent)
{

}

CDlg_BCLCtrl::~CDlg_BCLCtrl()
{
}

void CDlg_BCLCtrl::Update(ACPIControlMethodManager m_ACPICMManager)
{
    LVCOLUMN lvColumn;
    ULONG ulACPIId = 0;
    char ucBuffer[100];
    char ucTempBuffer[20];

    //Delete all items
    m_BCLListCtrl.DeleteAllItems();

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


    bool bRet = false;

    PACPI_BCL_OUTPUT pBCLOutput = NULL;
    ULONG ulBlcVal = 0;

    pBCLOutput = (PACPI_BCL_OUTPUT) malloc (sizeof(ACPI_BCL_OUTPUT) + 0x100);


    bRet = m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICE_BRIGHTNESS_LEVELS,
        0, sizeof(ACPI_BCL_OUTPUT) + 0x100, 
        NULL, (PVOID) pBCLOutput);    
 

    if((bRet) && ((pBCLOutput->ulNumBclLevels >= 2)))
    {
        
        m_BCLListCtrl.InsertItem(0, L"Brightness(AC)");
        _ultoa((ULONG) pBCLOutput->ulBclLevelAC, ucBuffer, 10);
        m_BCLListCtrl.SetItemText(0, 1, (LPCTSTR)(CString)ucBuffer);
        strcpy(ucBuffer, "");

        m_BCLListCtrl.InsertItem(1, L"Brightness(DC)");
        _ultoa((ULONG) pBCLOutput->ulBclLevelDC, ucBuffer, 10);
        m_BCLListCtrl.SetItemText(1, 1, (LPCTSTR)(CString)ucBuffer);
        strcpy(ucBuffer, "");



        for(int i = 2  ; i < (pBCLOutput->ulNumBclLevels - 2) ; i++)
        {
            strcpy(ucTempBuffer, "" );
            _ultoa((ULONG) pBCLOutput->ulBclLevelOther[i-2], ucTempBuffer, 10);
            strcat(ucBuffer, " ");
            strcat(ucBuffer, ucTempBuffer);
        }

        m_BCLListCtrl.InsertItem(2, L"Other levels");
        m_BCLListCtrl.SetItemText(2, 1, (LPCTSTR)(CString)ucBuffer);
    }

    UpdateData(FALSE);


}



void CDlg_BCLCtrl::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_BCL_LIST, m_BCLListCtrl);
}


BEGIN_MESSAGE_MAP(CDlg_BCLCtrl, CDialog)
END_MESSAGE_MAP()


// CDlg_BCLCtrl message handlers
