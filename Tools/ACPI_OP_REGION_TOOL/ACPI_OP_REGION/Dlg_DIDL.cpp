// Dlg_DIDL.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_DIDL.h"
#include "stdlib.h"

#define MAX_DEVICES 8

// CDlg_DIDL dialog

IMPLEMENT_DYNAMIC(CDlg_DIDL, CDialog)

CDlg_DIDL::CDlg_DIDL(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_DIDL::IDD, pParent)
{

}

CDlg_DIDL::~CDlg_DIDL()
{
}

void CDlg_DIDL::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    
    char str[100];
    char *temp = NULL;


    m_DIDL.ResetContent();
    m_DIDLEditDesc.SetWindowTextW((LPCTSTR)(CString)"");

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        //m_ACPIMailboxManager.stACPIMbx.stSupportedDisplayList[i].ulId = 0x100;
        if(0 == m_ACPIMailboxManager.stACPIMbx.stSupportedDisplayList[i].ulId)
        {
            break;
        }

        str[0] = '0';
        str[1] = 'x';
        temp = &str[2];

        _ultoa(m_ACPIMailboxManager.stACPIMbx.stSupportedDisplayList[i].ulId, temp, 16);

        m_DIDL.AddString((LPCTSTR)(CString)str);        
        m_DIDL.SetItemData(i, m_ACPIMailboxManager.stACPIMbx.stSupportedDisplayList[i].ulId);
    }
    
    UpdateData(FALSE);
}

void CDlg_DIDL::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_STATIC_DIDL, m_DIDL);
    DDX_Control(pDX, IDC_EDIT_DIDL, m_DIDLEditDesc);
}


BEGIN_MESSAGE_MAP(CDlg_DIDL, CDialog)
    ON_LBN_SELCHANGE(IDC_STATIC_DIDL, &CDlg_DIDL::OnLbnSelchangeStaticDidl)
END_MESSAGE_MAP()


// CDlg_DIDL message handlers

void CDlg_DIDL::OnLbnSelchangeStaticDidl()
{
    char Data[200];
    char temp[10];
    ULONG ulIndex;
    ACPI30_DOD_ID ulACPIId = {0};
    ulIndex = m_DIDL.GetCurSel();
    
    ulACPIId.ulId = m_DIDL.GetItemData(ulIndex);

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
    
    m_DIDLEditDesc.SetWindowTextW((LPCTSTR)(CString)Data);
    

}
