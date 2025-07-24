// Dlg_CEVT.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CEVT.h"
#include "stdlib.h"


// CDlg_CEVT dialog

IMPLEMENT_DYNAMIC(CDlg_CEVT, CDialog)

CDlg_CEVT::CDlg_CEVT(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CEVT::IDD, pParent)
{

}

CDlg_CEVT::~CDlg_CEVT()
{
}


void CDlg_CEVT::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCurrentEvent = 0;
    ulCurrentEvent = m_ACPIMailboxManager.stACPIMbx.ulCurrentEvent;
    
    m_CEVTCombo.ResetContent();

    m_CEVTCombo.AddString(L"No Event(0)");
    m_CEVTCombo.SetItemData(0,0);

    m_CEVTCombo.AddString(L"Display Switch Hot-Key Event(1)");
    m_CEVTCombo.SetItemData(1,1);

    m_CEVTCombo.AddString(L"Lid open/close Event(2)");
    m_CEVTCombo.SetItemData(2,2);

    m_CEVTCombo.AddString(L"Dock/Undock Event(4)");
    m_CEVTCombo.SetItemData(3,4);

    if((ulCurrentEvent >=0 && ulCurrentEvent <= 4))
    {
        m_CEVTCombo.SetCurSel(ulCurrentEvent);
    }
    else
    {
        m_CEVTCombo.AddString(L"Invalid Data");
        m_CEVTCombo.SetItemData(4,5);
        m_CEVTCombo.SetCurSel(4);
    }

    UpdateData(FALSE);

}


void CDlg_CEVT::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_CEVT, m_CEVTCombo);
}


BEGIN_MESSAGE_MAP(CDlg_CEVT, CDialog)
END_MESSAGE_MAP()


// CDlg_CEVT message handlers
