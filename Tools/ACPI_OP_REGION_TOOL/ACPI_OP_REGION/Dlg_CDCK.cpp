// Dlg_CDCK.cpp : implementation file
//

#include "stdafx.h"
#include "OPREG_Escape.h"

#include "ACPIMbxManager.h"
#include "ACPI_OP_REGION.h"
#include "Dlg_CDCK.h"
#include "stdlib.h"


// CDlg_CDCK dialog

IMPLEMENT_DYNAMIC(CDlg_CDCK, CDialog)

CDlg_CDCK::CDlg_CDCK(CWnd* pParent /*=NULL*/)
	: CDialog(CDlg_CDCK::IDD, pParent)
{

}

CDlg_CDCK::~CDlg_CDCK()
{
}

void CDlg_CDCK::Update(ACPIMbxManager m_ACPIMailboxManager)
{
    char *temp = NULL;
    ULONG ulCurrentDockStatus = 0;
    ulCurrentDockStatus = m_ACPIMailboxManager.stACPIMbx.ulCurrentDockStatus;

    mCDCKCombo.ResetContent();

    mCDCKCombo.AddString(L"Undocked(0)");
    mCDCKCombo.SetItemData(0,0);

    mCDCKCombo.AddString(L"Docked(1)");
    mCDCKCombo.SetItemData(1,1);

    if((ulCurrentDockStatus >=0 && ulCurrentDockStatus <= 1))
    {
        mCDCKCombo.SetCurSel(ulCurrentDockStatus);
    }
    else
    {
        mCDCKCombo.AddString(L"Invalid Data");
        mCDCKCombo.SetItemData(2,2);
        mCDCKCombo.SetCurSel(2);
    }

    UpdateData(FALSE);

}


void CDlg_CDCK::DoDataExchange(CDataExchange* pDX)
{
    CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_COMBO_CDCK, mCDCKCombo);
}


BEGIN_MESSAGE_MAP(CDlg_CDCK, CDialog)
END_MESSAGE_MAP()


// CDlg_CDCK message handlers
