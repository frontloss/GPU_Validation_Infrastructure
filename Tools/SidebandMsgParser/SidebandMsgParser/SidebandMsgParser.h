
// SidebandMsgParser.h : main header file for the PROJECT_NAME application
//

#pragma once

#ifndef __AFXWIN_H__
	#error "include 'stdafx.h' before including this file for PCH"
#endif

#include "resource.h"		// main symbols


// CSidebandMsgParserApp:
// See SidebandMsgParser.cpp for the implementation of this class
//

class CSidebandMsgParserApp : public CWinApp
{
public:
	CSidebandMsgParserApp();

// Overrides
public:
	virtual BOOL InitInstance();

// Implementation

	DECLARE_MESSAGE_MAP()
};

extern CSidebandMsgParserApp theApp;