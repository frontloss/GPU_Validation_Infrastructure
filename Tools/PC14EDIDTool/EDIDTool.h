// EDIDTool.h : main header file for the EDIDTOOL application
//


#if !defined(AFX_EDIDTOOL_H__4B119CE7_4480_458A_957A_97BB1E9745AA__INCLUDED_)
#define AFX_EDIDTOOL_H__4B119CE7_4480_458A_957A_97BB1E9745AA__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols
#include "..\\..\\..\\inc\\common\\SB_ESC.H"
#include "..\\..\\..\\inc\\common\\sbArgs.h"
#include "..\\..\\..\\inc\\common\\itvout.h"
#include "..\\..\\..\\inc\\common\\iLFP.h"
#include "..\\..\\..\\inc\\common\\tvout.h"


/////////////////////////////////////////////////////////////////////////////
// CEDIDToolApp:
// See EDIDTool.cpp for the implementation of this class
//

class CEDIDToolApp : public CWinApp
{
public:
	CEDIDToolApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CEDIDToolApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CEDIDToolApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_EDIDTOOL_H__4B119CE7_4480_458A_957A_97BB1E9745AA__INCLUDED_)
