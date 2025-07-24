// Dlg_DOD_Ctrl.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPIControlMethodManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_DOD_Ctrl.h"
#include "stdlib.h"


// CDlg_DOD_Ctrl dialog

IMPLEMENT_DYNAMIC(CDlg_DOD_Ctrl, CDialog)

CDlg_DOD_Ctrl::CDlg_DOD_Ctrl(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_DOD_Ctrl::IDD, pParent)
{

}

CDlg_DOD_Ctrl::~CDlg_DOD_Ctrl()
{
}

void CDlg_DOD_Ctrl::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_LIST_DOD, m_DODList);
    DDX_Control(pDX, IDC_EDIT_DOD_CRTL, m_DODComment);
}

void CDlg_DOD_Ctrl::Update(ACPIControlMethodManager m_ACPICMManager)
{
    ACPI_DOD_LIST * pDODOutput = NULL;

    char str[100];
    char *temp = NULL;

    m_DODList.ResetContent();
    m_DODComment.SetWindowTextW((LPCTSTR)(CString)"");

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

        m_DODList.AddString((LPCTSTR)(CString)str);        
        m_DODList.SetItemData(i, pDODOutput->ulAcpiId[i].ulId);

        strcpy(str, "");
        temp = NULL;
    }

    UpdateData(FALSE);
}



BEGIN_MESSAGE_MAP(CDlg_DOD_Ctrl, CDialog)
    ON_LBN_SELCHANGE(IDC_LIST_DOD, &CDlg_DOD_Ctrl::OnLbnSelchangeListDod)
END_MESSAGE_MAP()


// CDlg_DOD_Ctrl message handlers

void CDlg_DOD_Ctrl::OnLbnSelchangeListDod()
{
    char Data[200];
    char temp[10];
    ULONG ulIndex;
    ACPI30_DOD_ID ulACPIId = {0};
    ulIndex = m_DODList.GetCurSel();
    
    ulACPIId.ulId = m_DODList.GetItemData(ulIndex);



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
    strcat(Data,"\r\n\r\nIndex: ");
    strcat(Data,temp);
    
    m_DODComment.SetWindowTextW((LPCTSTR)(CString)Data);

}

void CDlg_DOD_Ctrl::Eval(ACPIControlMethodManager m_ACPICMManager)
{
    //Do nothing
}
