// Dlg_NADL.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_NADL.h"
#include "stdlib.h"

#define MAX_DEVICES 8
\
// CDlg_NADL dialog

IMPLEMENT_DYNAMIC(CDlg_NADL, CDialog)

CDlg_NADL::CDlg_NADL(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_NADL::IDD, pParent)
{

}

CDlg_NADL::~CDlg_NADL()
{
}

void CDlg_NADL::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    
    char str[100];
    char *temp = NULL;


    m_NADLList.ResetContent();
    m_NADLEditDesc.SetWindowTextW((LPCTSTR)(CString)"");

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        if(0 == m_ACPIMailboxManager.stACPIMbx.stNextActiveDisplayList[i].ulId)
        {
            break;
        }

        str[0] = '0';
        str[1] = 'x';
        temp = &str[2];

        _ultoa(m_ACPIMailboxManager.stACPIMbx.stNextActiveDisplayList[i].ulId, temp, 16);

        m_NADLList.AddString((LPCTSTR)(CString)str);      
        m_NADLList.SetItemData(i, m_ACPIMailboxManager.stACPIMbx.stNextActiveDisplayList[i].ulId);
    }
    
    UpdateData(FALSE);
}

void CDlg_NADL::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_LIST_NADL, m_NADLList);
    DDX_Control(pDX, IDC_EDIT_NADL, m_NADLEditDesc);
}


BEGIN_MESSAGE_MAP(CDlg_NADL, CDialog)
    ON_LBN_SELCHANGE(IDC_LIST_NADL, &CDlg_NADL::OnLbnSelchangeListNadl)
END_MESSAGE_MAP()


// CDlg_NADL message handlers

void CDlg_NADL::OnLbnSelchangeListNadl()
{
    char Data[200];
    char temp[10];
    ULONG ulIndex;
    ACPI30_DOD_ID ulACPIId = {0};
    
    ulIndex = m_NADLList.GetCurSel();
    ulACPIId.ulId = m_NADLList.GetItemData(ulIndex);

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
    
    m_NADLEditDesc.SetWindowTextW((LPCTSTR)(CString)Data);
   
}
