// ACPI_OP_REGION.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'stdafx.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols


// CACPI_OP_REGIONApp:
// See ACPI_OP_REGION.cpp for the implementation of this class
//

class CACPI_OP_REGIONApp : public CWinApp
{
public:
	CACPI_OP_REGIONApp();

// Overrides
	public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
};

extern CACPI_OP_REGIONApp theApp;