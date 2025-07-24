// Dlg_CADL.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CADL.h"
#include "stdlib.h"

#define MAX_DEVICES 8


// CDlg_CADL dialog

IMPLEMENT_DYNAMIC(CDlg_CADL, CDialog)

CDlg_CADL::CDlg_CADL(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CADL::IDD, pParent)
{

}

CDlg_CADL::~CDlg_CADL()
{
}

void CDlg_CADL::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char str[100];
    char *temp = NULL;

    m_CADLList.ResetContent();
    mCADLDesc.SetWindowTextW((LPCTSTR)(CString)"");

    //m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[0].ulId = 0x400;
    //m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[1].ulId = 0x100;
    //m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[2].ulId = 0;

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        if(0 == m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[i].ulId)
        {
            break;
        }

        str[0] = '0';
        str[1] = 'x';
        temp = &str[2];

        _ultoa(m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[i].ulId, temp, 16);

        m_CADLList.AddString((LPCTSTR)(CString)str);        
        m_CADLList.SetItemData(i, m_ACPIMailboxManager.stACPIMbx.stActiveDisplayList[i].ulId);
    }
    
    UpdateData(FALSE);
}

void CDlg_CADL::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_LIST_ASLP, m_CADLList);
    DDX_Control(pDX, IDC_EDIT_ASLP, mCADLDesc);
}


BEGIN_MESSAGE_MAP(CDlg_CADL, CDialog)
    ON_STN_CLICKED(IDC_STATIC_ASLP, &CDlg_CADL::OnStnClickedStaticAslp)
    ON_LBN_SELCHANGE(IDC_LIST_ASLP, &CDlg_CADL::OnLbnSelchangeListAslp)
END_MESSAGE_MAP()


// CDlg_CADL message handlers

void CDlg_CADL::OnStnClickedStaticAslp()
{
    // TODO: Add your control notification handler code here
}

void CDlg_CADL::OnLbnSelchangeListAslp()
{
    char Data[200];
    char temp[10];
    ULONG ulIndex;
    ACPI30_DOD_ID ulACPIId = {0};
    ulIndex = m_CADLList.GetCurSel();
    ulACPIId.ulId = m_CADLList.GetItemData(ulIndex);

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
    
    mCADLDesc.SetWindowTextW((LPCTSTR)(CString)Data);

}
