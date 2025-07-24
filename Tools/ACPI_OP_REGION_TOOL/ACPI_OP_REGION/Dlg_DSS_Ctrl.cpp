// Dlg_DSS_Ctrl.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_DSS_Ctrl.h"
#include "stdlib.h"


// CDlg_DSS_Ctrl dialog

IMPLEMENT_DYNAMIC(CDlg_DSS_Ctrl, CDialog)

CDlg_DSS_Ctrl::CDlg_DSS_Ctrl(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_DSS_Ctrl::IDD, pParent)
{

}

CDlg_DSS_Ctrl::~CDlg_DSS_Ctrl()
{
}

void CDlg_DSS_Ctrl::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_DSS_CTRL1, m_DSSACPIID);
    DDX_Control(pDX, IDC_COMBO_DSS_CRTL2, m_DSSVal);
}

void CDlg_DSS_Ctrl::Update(ACPIControlMethodManager m_ACPICMManager)
{

    ACPI_DOD_LIST * pDODOutput = NULL;

    char str[100];
    char *temp = NULL;

    m_DSSACPIID.ResetContent();
    m_DSSVal.ResetContent();

    pDODOutput = (PACPI_DOD_LIST) malloc (sizeof(ACPI_DOD_LIST) * 8);

    m_ACPICMManager.EvaluateControlMethod(ESC_ACPI_GET_DEVICES, 0, sizeof(ACPI_DOD_LIST) * 8, NULL, (PVOID) pDODOutput);

    for(int i = 0 ; i < pDODOutput->ulNumAcpiIds ; i++)
    {
        str[0] = '0';
        str[1] = 'x';
        temp = &str[2];

        if(0 == pDODOutput->ulAcpiId[i].ulId)
        {
            break;
        }

        _ultoa(pDODOutput->ulAcpiId[i].ulId, temp, 16);

        m_DSSACPIID.AddString((LPCTSTR)(CString)temp);
        m_DSSACPIID.SetItemData(i,pDODOutput->ulAcpiId[i].ulId);

        strcpy(str, "");
        temp = NULL;
    }

    m_DSSVal.AddString(L"OFF");
    m_DSSVal.SetItemData(0,0);

    m_DSSVal.AddString(L"ON");
    m_DSSVal.SetItemData(1,1);




    UpdateData(FALSE);
}


BEGIN_MESSAGE_MAP(CDlg_DSS_Ctrl, CDialog)
END_MESSAGE_MAP()


// CDlg_DSS_Ctrl message handlers
