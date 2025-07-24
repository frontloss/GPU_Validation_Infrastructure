// Dlg_CPDL.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CPDL.h"
#include "stdlib.h"

#define MAX_DEVICES 8


// CDlg_CPDL dialog

IMPLEMENT_DYNAMIC(CDlg_CPDL, CDialog)

CDlg_CPDL::CDlg_CPDL(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CPDL::IDD, pParent)
{

}

CDlg_CPDL::~CDlg_CPDL()
{
}

void CDlg_CPDL::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    
    char str[100];
    char *temp = NULL;


    m_CPDLList.ResetContent();
    m_CPDLEditDesc.SetWindowTextW((LPCTSTR)(CString)"");

    for(int i = 0 ; i < MAX_DEVICES ; i++)
    {
        //m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId = 0x100;
        if(0 == m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId)
        {
            break;
        }

        str[0] = '0';
        str[1] = 'x';
        temp = &str[2];

        _ultoa(m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId, temp, 16);

        m_CPDLList.AddString((LPCTSTR)(CString)str);        
        m_CPDLList.SetItemData(i, m_ACPIMailboxManager.stACPIMbx.stAttachedDisplayList[i].ulId);
    }
    
    UpdateData(FALSE);
}


void CDlg_CPDL::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_LIST_CPDL, m_CPDLList);
    DDX_Control(pDX, IDC_EDIT_CPDL, m_CPDLEditDesc);
}


BEGIN_MESSAGE_MAP(CDlg_CPDL, CDialog)
    ON_LBN_SELCHANGE(IDC_LIST_CPDL, &CDlg_CPDL::OnLbnSelchangeListCpdl)
END_MESSAGE_MAP()


// CDlg_CPDL message handlers

void CDlg_CPDL::OnLbnSelchangeListCpdl()
{
    char Data[200];
    char temp[10];
    ULONG ulIndex;
    ACPI30_DOD_ID ulACPIId = {0};
    ulIndex = m_CPDLList.GetCurSel();
    ulACPIId.ulId = m_CPDLList.GetItemData(ulIndex);

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
    
    m_CPDLEditDesc.SetWindowTextW((LPCTSTR)(CString)Data);
   
    

}
