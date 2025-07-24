// EDIDToolDlg.cpp : implementation file


#include "stdafx.h"
#include "EDIDToolDlg.h"
#include "EDIDHeader.h"



#ifdef _VISTA_

#define NTSTATUS long

#define SIZE8BITS UCHAR
#define SIZE32BITS ULONG

#include "..\\..\\..\\..\\SourceCUI3\\igfx\\inc\\d3dkmthk.h"
#include "..\\..\\..\\inc\\common\\gfxEscape.h"
			
HMODULE hGdi32 = NULL;
PFND3DKMT_OPENADAPTERFROMHDC OpenAdapter = NULL;
PFND3DKMT_ESCAPE D3DKmtEscape = NULL;
PFND3DKMT_CLOSEADAPTER CloseAdapter = NULL;
PFND3DKMT_INVALIDATEACTIVEVIDPN InvalidateActiveVidPnThunk = NULL;

#endif

INT iRet ;
BOOL bWinXP,bWinVista;


#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static CHAR THIS_FILE[] = __FILE__;
#endif
extern CString Text;


//Buffer to Store the 128 Byte EDID Structure
extern BYTE *edidbuffer;
extern BYTE *BlockMapExt;
extern BYTE *ceaext;
extern BYTE *vtbext;
BYTE *Extension = (BYTE *) 0;

extern BOOLEAN cextflag;
extern BOOLEAN vtbextflag;
extern BOOLEAN BlockMapFlag;

extern INT L1;//Length of Video Block
extern INT L2;//Length of Audio Block
extern INT L3;//Length of Speaker Allocation
extern INT L4;//Length of Vendor Specific Data Block

extern INT listcount;
extern BYTE byteTemp;
extern INT byteCount;

extern INT CurrentExtNo; // Modified in DisplayInfo ...Strictly used form storing No. of Current Extension Block

//Offset for Data Block
extern INT d;
//No. of DTDs
extern INT n;

INT NumExt = 0;			// Total No. of Extensions in the EDID.


/*typedef enum
{
    // DONOT change the order of type definitions
    // Add new types just before MAX_DISPLAY_TYPES & increment value of MAX_DISPLAY_TYPES
    NULL_DISPLAY_TYPE = 0,
    CRT_TYPE,
    TV_TYPE,
    DFP_TYPE,
    LFP_TYPE,
    MAX_DISPLAY_TYPES = LFP_TYPE
} DISPLAY_TYPE; */

//
// ENCODER_TYPE
//
typedef enum _ENCODER_TYPE
{
    CRT_ENCODER_TYPE = CRT_TYPE,
    TV_ENCODER_TYPE = TV_TYPE,
    DFP_ENCODER_TYPE = DFP_TYPE,
    LFP_ENCODER_TYPE = LFP_TYPE,

    MAX_ENCODER_TYPES = LFP_ENCODER_TYPE
}ENCODER_TYPE;


typedef enum _CONNECTOR_TYPE
{
    eUnknownConnector   = 0,        // (Unknown connector - init state)
    e15PinVGA           = 1,        // (Multi frequency CRT)
    e5PinBNC            = 2,        // (Fixed frequency CRT)
    
    eDVI_D              = 3,        // (Digital for DFPs)
    eDVI_A              = 4,        // (Analog for CRTs)
    eDVI_I              = 5,        // (Analog & Digital)
    eHDMI               = 6,        // (DVI + Audio)
    
    eLVDS               = 7,        // (LVDS - for LFPs)
    eDualChannelLVDS    = 8,        // (LVDS - Dual channel)
    
    eComposite          = 9,        // (CVBS - TV)
    eSVideo             = 10,       // (SVideo - TV)
    eComponent          = 11,       // (YCrCb - HDTV)
    eDConnector         = 12,       // (D-Connector)
    eSCART              = 13,       // (SCART)

    eExternalDP         = 14,
    eEmbeddedDP         = 15,
    eTPVConnector       = 16,       //NIVO Connector
    eMaxConnectorTypes              // Maximum possible connector types (Note: Includes unknown connector type as well)
}CONNECTOR_TYPE;

typedef union _ENCODER_UID
{
    SIZE8BITS ucEncoderUID; 

    struct 
    {
        SIZE8BITS ucEncoderType     : 3;    // bits 2:0 (See ENCODER_TYPE)
        SIZE8BITS ucEncoderIndex    : 4;    // bits 6:3 (In case of multiple encoders of the same type)
        SIZE8BITS ucEUIDReserved    : 1;    // bits 7
    };

}ENCODER_UID, *PENCODER_UID;

//
// Connector UID: Uniquely identifies a connector
// Note: This is independent of encoder UID. ie., with
// just connector UID one will be able to identify the encoder &
// display.
//
typedef union _CONNECTOR_UID
{
    SIZE8BITS ucConnectorUID;

    struct
    {
        SIZE8BITS ucConnectorType   : 5;    // See CONNECTOR_TYPE definition
        SIZE8BITS ucConnectorIndex  : 3;    // In case of multiple connectors of same type      
    };

}CONNECTOR_UID, *PCONNECTOR_UID;




typedef union _DISPLAY_ID
{
    SIZE32BITS   ulDisplayID;

    struct 
    {
        //
        // Note new format which is ok with old format (DISPLAY_UID)    
        // Old format:-
        //  Byte 0: EDID hash
        //  Byte 1: Not used
        //  Byte 2: Port type
        //  Byte 3: Display type

        // Byte 0: Not used
        // Note: During clone/twin mode table creation, this byte will be
        // used to store the connector UID of secondary display ID
        BYTE ucReservedDID1;

        // Byte 1: Encoder UID
        ENCODER_UID stEncoderId;

        // Byte 2: Connector UID (old port info)
        CONNECTOR_UID stConnectorID;

        // Byte3: Display specific information (old 
        struct
        {
            SIZE8BITS ucDisplayType     : 4;    // Bits 3:0 = Display Type possible with this connector
            SIZE8BITS ucReserverdDID    : 4;    // Unused
        };
    };
} DISPLAY_ID, *PDISPLAY_ID;



//----------------------------------------------------------------------------
//  Function    :   hex_to_decimal
//	Note		:	Author Defined Function
//-----------------------------------------------------------------------------
INT hex_to_decimal(BYTE ch)
{
	if(ch >= '0' && ch <= '9')
		 return ch - '0';
    else
	{
		switch(ch)
		{
		
		case 'a' :
        case 'A' :return 10; break;
		
		case 'b' :
		case 'B' :return 11; break;
		
		case 'c' :
		case 'C' :return 12; break;	
		
		case 'd' :
		case 'D' :return 13; break;
		
		case 'e' :
		case 'E' :return 14; break;
		
		case 'f' :
		case 'F' :return 15; break;
		
		default: return -1; 

		}
	}
}

void Encrypt(PVOID pvStruct,ULONG Size)
{
	CHAR *tempArr;
	ULONG count =0;
	tempArr = (CHAR *)malloc(Size*sizeof(CHAR));
	memcpy(tempArr,pvStruct,Size);
	for(count = 0;count<Size;count++)
	{
		tempArr[count]=  tempArr[count] ^ MAGIC_NUMBER; }
	
	memcpy(pvStruct,tempArr,Size);
	free(tempArr);
}

ULONG GetIntFromHex(CHAR *hldStr)
{
	ULONG tempvar = 0;
	ULONG ulDisId = 0;

	//hex to int conversion
	while(hldStr[tempvar]!='\0')
	{
		if(hldStr[tempvar]>='0' && hldStr[tempvar]<='9')
			ulDisId=16*ulDisId+hldStr[tempvar]-48;
		else if(hldStr[tempvar]>=65 && hldStr[tempvar] <= 70)
			ulDisId=16*ulDisId+hldStr[tempvar]-55;
		else if(hldStr[tempvar] >=97 && hldStr[tempvar] <= 102)
			ulDisId=16*ulDisId+hldStr[tempvar]-87;
		tempvar++;
	}

	return ulDisId;
}

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();
	

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CEDIDToolDlg dialog

CEDIDToolDlg::CEDIDToolDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CEDIDToolDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CEDIDToolDlg)
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CEDIDToolDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CEDIDToolDlg)
	DDX_Control(pDX, IDC_COMBO1, m_DeviceId);
	DDX_Control(pDX, IDC_COMBO2, m_DeviceId2);
	DDX_Control(pDX, IDC_EDIT4, m_DeviceName);
	DDX_Control(pDX, IDC_BUTTON1, m_Open);
	DDX_Control(pDX, IDC_BUTTON2, m_Save);
	DDX_Control(pDX, IDC_BUTTON3, m_Read);
	DDX_Control(pDX, IDC_EDIT1, m_HexValues);
	DDX_Control(pDX, IDC_EDIT2, m_TextData);
	DDX_Control(pDX, IDC_EDIT3, m_ByteValues);
	DDX_Control(pDX, IDC_LIST1, m_ByteDetails);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CEDIDToolDlg, CDialog)
	//{{AFX_MSG_MAP(CEDIDToolDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_BUTTON1, OnOpen)
	ON_BN_CLICKED(IDC_BUTTON2, OnSave)
	ON_BN_CLICKED(IDC_BUTTON3, OnRead)
	ON_BN_CLICKED(IDC_BUTTON4, OnSaveToRegistry)
	ON_NOTIFY(NM_CLICK, IDC_LIST1, OnByteDetails)
	ON_CBN_SELCHANGE(IDC_COMBO1, OnChangeDeviceId)
	ON_BN_CLICKED(IDC_CLONE_EDID_BUTTON, OnCloneEdidButton)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CEDIDToolDlg message handlers

BOOL CEDIDToolDlg::OnInitDialog()
{
		OSVERSIONINFO OSVersionInfo;
		ZeroMemory (&OSVersionInfo, sizeof(OSVERSIONINFO));
		OSVersionInfo.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);
		GetVersionEx(&OSVersionInfo);

		if ((OSVersionInfo.dwMajorVersion >= 6) && (OSVersionInfo.dwPlatformId == VER_PLATFORM_WIN32_NT))
		{
			bWinVista = TRUE;
					
		}
			else 
			{		
				bWinXP = TRUE;
		
			}

		

 	if (bWinVista)
	{
            hGdi32 = LoadLibrary("gdi32.dll");
            OpenAdapter = (PFND3DKMT_OPENADAPTERFROMHDC)GetProcAddress(hGdi32,"D3DKMTOpenAdapterFromHdc");
            D3DKmtEscape = (PFND3DKMT_ESCAPE)GetProcAddress(hGdi32,"D3DKMTEscape");
	        CloseAdapter = (PFND3DKMT_CLOSEADAPTER)GetProcAddress(hGdi32,"D3DKMTCloseAdapter");
	}

			
    CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here

	//Adding Columns to the List View
	
	m_ByteDetails.InsertColumn(0,"Byte No");
	m_ByteDetails.InsertColumn(1,"Byte Values");
	m_ByteDetails.InsertColumn(2,"Byte Details");
	
	m_ByteDetails.SetColumnWidth(0,70);
	m_ByteDetails.SetColumnWidth(1,220);	
	m_ByteDetails.SetColumnWidth(2,450);

	m_Read.EnableWindow(FALSE);
	
	//Detect the Display Devices 
	SbDisDetect();
	
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CEDIDToolDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CEDIDToolDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		INT cxIcon = GetSystemMetrics(SM_CXICON);
		INT cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		INT x = (rect.Width() - cxIcon + 1) / 2;
		INT y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CEDIDToolDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CEDIDToolDlg::OnOpen() 
{
	//Get the File to be Opened
	CString Filename=GetFileName(TRUE);
	edidbuffer=(BYTE *)calloc(128,1);
	
	FILE *fp;
	fopen_s(&fp,Filename, "r");
	
	if(!(Filename.IsEmpty()))
	{
		
		// Do check for txt files with Hex values or BIN files.
		// This assumes that txt files will be having data in Hex format only.
		if( !(Filename.Find(".txt") < 0 )  )
		{
			CHAR previous_char, current_char, temp_char;
			INT valuebyte,Tempvalue;	// Valuebyte has value of valid byte of EDID.
			INT bytecount=0;			// Counts parsed number of bytes of EDID.
			BOOLEAN bytecountOver = FALSE; 
		
			// Following loop will run 2 times. First time for calculating bytes present.
			// & second time for storing the bytes in buffers.
			while(1)
			{			
				current_char = getc(fp );					
					
				if(current_char < 0)
				{
					if(bytecountOver == TRUE)
						break;
					else
					{
						if(bytecount > 128)
						{
							Extension = (BYTE *) 0;
							Extension = (BYTE *) calloc(bytecount-128,sizeof(BYTE));
						}

						bytecount = 0;
						bytecountOver = TRUE;
						rewind(fp);		
						continue;
					}
				}
			
				// If last two letters are '0' & 'x' then read a hex number.
				if(current_char == 'x')
				{
					if(previous_char == '0')
					{
						bytecount++;
					
						temp_char=0;
						valuebyte=0;
					
						temp_char = getc(fp);
						Tempvalue =  hex_to_decimal(temp_char);
						if(0 <= Tempvalue )
							valuebyte = Tempvalue;
						else
						{
							previous_char =  temp_char;
							bytecount--;
							MessageBox("Warning: There might be a wrong Hex Number in the file!!",NULL,MB_OK);
							continue;
						}					
					
						temp_char = getc(fp);
						Tempvalue =  hex_to_decimal(temp_char);
					
						if(0 <= Tempvalue )							
							valuebyte = ((valuebyte * 16) +  Tempvalue);
						else	
							previous_char =  temp_char;

						if(bytecountOver == TRUE)
						{							
							if(bytecount < 129)
								*(edidbuffer + bytecount - 1 ) =  valuebyte;
							else					
								*(Extension + bytecount - 129 ) =  valuebyte;
						}
					}
				}
				else
				{
					previous_char = current_char;
					continue;
				}
			}					
		
			ClearAll();
			getByteValues();
			DisplayInfo();			
			getHexValues();						

		}
		else
		{		
			//Read the File Contents on to the buffer			
			fopen_s(&fp,Filename,"rb");
		
			fseek(fp,0L,SEEK_END);
			LONG size=ftell(fp);
			rewind(fp);		
		
			CString Temp;
			Temp.Format("%d",size);
			
			if( size >= 128)
			{
				fread(edidbuffer,128,1,fp);
				if(size >= 256)
				{
					Extension = (BYTE *) 0;
					Extension = (BYTE *) calloc(size,sizeof(BYTE));
//					fseek(fp,0,127);
					if(Extension)
					{
						fread(Extension, size-128, 1, fp);
					}
					else
					{
						MessageBox("Error in allocating memory for extensions!!",NULL,MB_OK);
					}
				}
				
				ClearAll();
				getByteValues();
				DisplayInfo();
				getHexValues();								
			}
		}
			fclose(fp);
						
			//m_Read.EnableWindow(FALSE);
	}
}

void CEDIDToolDlg::OnSave() 
{
	//Get the File name
	CString Filename=GetFileName(FALSE);
	
	if(Text=="")
	{
		MessageBox("No data to be written");
	}
	
	if(!(Filename.IsEmpty()) && Text!="")
	{
		FILE *fp;
		fopen_s(&fp,Filename,"wb");
		
		//Write the Buffer Contents on to a file
		fwrite(edidbuffer,1,128,fp);
		fwrite(Extension, 1, 128*NumExt, fp);
		fclose(fp);
	}
	
	
}

void CEDIDToolDlg::OnSaveToRegistry() 
{
	HKEY hk = NULL; 
	TCHAR szBuf[200]; 
	INT i = 0;
	ULONG ePort = 0;
	DWORD dwDisp = 0;
	CHAR hldStr[25];
	ULONG ulDisId = 0;
	BOOLEAN bSuccess = FALSE;
	CString szKeyName = "SYSTEM\\CurrentControlSet\\Services\\ialm\\Device0"; // for XP


	memset(&hldStr,0,sizeof(hldStr));

	if (bWinVista)
	{
		// Change key name
		szKeyName = "SYSTEM\\CurrentControlSet\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000";
	}

	if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, szKeyName, 0, NULL, &hk) != ERROR_SUCCESS)
	{
		RegCreateKeyEx(HKEY_LOCAL_MACHINE, szKeyName,0, NULL, REG_OPTION_NON_VOLATILE,KEY_WRITE, NULL, &hk, &dwDisp);
	}

	if (hk != NULL)
	{
		// Save EDID data to registry in the following format
		// FakeEDID_<port value>_<block number>

		//Get the Selected Device Name and ID	
		m_DeviceId.GetLBText(m_DeviceId.GetCurSel(),hldStr);
		ulDisId = GetIntFromHex(hldStr);

		if (ulDisId != 0)
		{
			ePort = GetDisplayPortUsed(ulDisId);

			if (ePort != NULL_PORT_TYPE)
			{
				sprintf_s(szBuf,256,"FakeEDID_%d_%d", ePort, 0);
				if (RegSetValueEx(hk,szBuf,0,REG_BINARY,edidbuffer,128) == ERROR_SUCCESS)
				{
					MessageBox(szBuf, "Created entry");
					bSuccess = TRUE;
				}

				for (i = 1; i <= NumExt; i++)
				{
					sprintf_s(szBuf,256,"FakeEDID_%d_%d", ePort, i);

					if (RegSetValueEx(hk,szBuf,0,REG_BINARY,Extension+((i-1)*128),128) == ERROR_SUCCESS)
					{
						MessageBox(szBuf, "Created entry");
					}
				}
			}
			else
			{
				MessageBox("Port type is NULL_PORT_TYPE");
			}
		}
		else
		{
			MessageBox("Display ID is 0!");
		}

		RegCloseKey(hk);
	}
	else
	{
		MessageBox(szKeyName, "Not able to open driver key");
	}

	if (bSuccess == FALSE)
	{
		MessageBox("Could not create the registry value - some error!"); 
	}
	else
	{
		MessageBox("Fake EDID entry made in registry","Save",MB_OK);
	}
	
	return;
}

CString CEDIDToolDlg::GetFileName(BOOL Open_Save)
{
	CString FileName="";
	CHAR path[200];
	memset(&path,0,sizeof(path));
	OPENFILENAME ofn;
	ofn.lStructSize = sizeof(OPENFILENAME);
	ofn.hwndOwner = AfxGetApp()->m_pMainWnd->m_hWnd;
	ofn.hInstance = NULL;
	ofn.lpstrFilter ="Binary(*.bin)\0*.bin\0Text(*.txt)\0*.txt\0" ;
	ofn.lpstrCustomFilter = NULL;
	ofn.nMaxCustFilter = 0;
	ofn.nFilterIndex = 0;
	ofn.lpstrFile = &path[0];
	ofn.nMaxFile = MAX_PATH;
	ofn.lpstrFileTitle = NULL;
	ofn.nMaxFileTitle = 0;
	ofn.lpstrInitialDir = NULL;
	ofn.Flags = OFN_OVERWRITEPROMPT| OFN_FILEMUSTEXIST | OFN_HIDEREADONLY | OFN_PATHMUSTEXIST | OFN_EXPLORER;
	ofn.nFileOffset = 0;
	ofn.nFileExtension = 0;
	ofn.lpstrDefExt ="BIN";
	ofn.lCustData = 0;
	ofn.lpfnHook = NULL;
	ofn.lpTemplateName = NULL;
	if(Open_Save)
	{
		ofn.lpstrTitle = "Open";
		if(GetOpenFileName(&ofn)==TRUE)
		{
			FileName=ofn.lpstrFile; 		
		}
	}
	else
	{
		ofn.lpstrTitle = "Save As"; 				
		if(GetSaveFileName(&ofn)==TRUE)
		{
			FileName=ofn.lpstrFile; 		
		}
	}
	return FileName;
}

void CEDIDToolDlg::OnRead() 
{
	GetEdidInfo();
}
ULONG checksum(ULONG iSize,PVOID pData)
{
	ULONG sum=0,i=0,*element = (ULONG*)pData;

	ULONG BMUL = iSize & ((ULONG)(-1) - (sizeof(ULONG)-1));

	ULONG NUM = BMUL/sizeof(ULONG);

	for(i=0;i<NUM;i++)
	{
		sum += *(element++);
	}

	return sum;
}

void CEDIDToolDlg::VistaEsc(INT iEsc, INT cbIn, void * pIn, BOOLEAN bDetect)
{

             	void * pLocal = NULL;
				HANDLE hLocal = NULL;
  		    		
			
				hLocal = GlobalAlloc(GHND, cbIn);
				
				pLocal = GlobalLock(hLocal);
				
			    memcpy(pLocal,pIn,cbIn);


				CHAR *DeviceContext = "\\\\.\\DISPLAY1";
				HDC hdc = CreateDC(NULL,TEXT(DeviceContext), NULL, NULL);

				GFX_ESCAPE_HEADER_T *pHeader = NULL;

                D3DKMT_OPENADAPTERFROMHDC* poa = (D3DKMT_OPENADAPTERFROMHDC *)malloc(sizeof(D3DKMT_OPENADAPTERFROMHDC));
                ZeroMemory(poa,sizeof(poa));
                poa->hDc = hdc;
                OpenAdapter(poa);

                D3DKMT_ESCAPE esc;
                ZeroMemory(&esc,sizeof(esc));
                esc.hAdapter = poa->hAdapter;
                esc.Type = D3DKMT_ESCAPE_DRIVERPRIVATE;
                esc.pPrivateDriverData = (void*)malloc(cbIn+sizeof(GFX_ESCAPE_HEADER_T));
                esc.PrivateDriverDataSize = cbIn+sizeof(GFX_ESCAPE_HEADER_T);

                pHeader = (GFX_ESCAPE_HEADER_T *)malloc(sizeof(GFX_ESCAPE_HEADER_T));
                ZeroMemory(pHeader,sizeof(GFX_ESCAPE_HEADER_T));
                pHeader->EscapeCode = GFX_ESCAPE_SOFTBIOS_CONTROL; 
                pHeader->Size = cbIn;
                pHeader->CheckSum = checksum(cbIn,(PVOID)pLocal);
				

                memcpy(esc.pPrivateDriverData,pHeader,sizeof(GFX_ESCAPE_HEADER_T));
                CHAR *pPointer = (CHAR*)esc.pPrivateDriverData;
                void *pret = pPointer+sizeof(GFX_ESCAPE_HEADER_T);
                memcpy(pret,pLocal,cbIn);
				
				// Before making the escape call, encrypt the whole data
				// The driver will be decrypting it before using this. 
				//Encrypt((void *)esc.pPrivateDriverData, esc.PrivateDriverDataSize);
             
			    ULONG ntret = D3DKmtEscape(&esc);

				if(ntret == 0)
				{
                    iRet = 1;
				}

				if(bDetect)
				{ 
					memcpy(pIn,pret,cbIn);
				}
				else
				{
					memcpy(pLocal,pret,cbIn);
				}
			
			    //close adapter.
                D3DKMT_CLOSEADAPTER ca;
                ca.hAdapter	 = poa->hAdapter;
                CloseAdapter(&ca);

                //free all the mallocs
                if(pHeader)
                {
                    free(pHeader);
                    pHeader = NULL;
                }
                if(poa)
                {
                    free(poa);
                    poa = NULL;
                }
                if(esc.pPrivateDriverData)
                {
                    free(esc.pPrivateDriverData);
                    esc.pPrivateDriverData =NULL;
                }

				
				
}

void CEDIDToolDlg::SbDisDetect()
{
	
	
	//Structure for Device Info
	SBULT_CUST_DETECT_STRUCT dispdet;
	memset(&dispdet, 0, sizeof(dispdet));
	dispdet.Cmd=SB_GET_DISPLAY_DETECT;
	dispdet.SbInfo.ulSize=sizeof(SB_GETDISPLAYDETECT_ARGS);
	
  	
	//Get the Devices and their IDs
	
    CDC* Cdc =  GetDC();			// Get the device context object for current window
    HDC hdc = Cdc ->m_hDC;       // Get the device context handle for current window
	
    dispdet.SbInfo.stDisplayDeviceStatus[0].ulDisplayUID = DISPLAY_ALL;

	Encrypt(&dispdet,sizeof(SBULT_CUST_DETECT_STRUCT));

	if (bWinVista)
	{	 
			   VistaEsc(SB_GET_DISPLAY_DETECT,sizeof(dispdet),&dispdet, TRUE);
	}

	
	else
	{
			 iRet=ExtEscape(hdc,SB_ESCAPE,sizeof(SBULT_CUST_DETECT_STRUCT),(LPCSTR)&dispdet,sizeof(SBULT_CUST_DETECT_STRUCT),(LPSTR)&dispdet);
	}	
	
	//Populate the List Box with Device IDs
	for(UINT i=0;i<dispdet.SbInfo.ulNumDisplays;i++)
	{
		if(dispdet.SbInfo.stDisplayDeviceStatus[i].ulDisplayUID!=0)
		{
			CHAR buf[25];
			_itoa_s(dispdet.SbInfo.stDisplayDeviceStatus[i].ulDisplayUID,buf,16);

			INT Res=m_DeviceId.AddString(buf);

			if (dispdet.SbInfo.ulNumDisplays > 1)
			{
				m_DeviceId2.AddString(buf);
			}

			m_DeviceId.SetCurSel(i);
		}
		m_Read.EnableWindow(TRUE);
	}

	m_DeviceId.SetCurSel(0);
	m_DeviceId2.SetCurSel(1);

	ReleaseDC(Cdc);
	//DeleteDC(hdc);
	
}

void CEDIDToolDlg::GetEdidInfo()
{
	cextflag=FALSE;
	vtbextflag=FALSE;
	
	
	//Structure for Storing EDID Info

	SBULT_CUST_EDID_STRUCT edidbuf;
	memset(&edidbuf, 0, sizeof(edidbuf));
	CHAR hldStr[25];
	memset(&hldStr,0,sizeof(hldStr));
	ULONG ulDisId=0;
	edidbuf.Cmd=SB_GET_EDID;
	edidbuf.SbInfo.ulEdidSize=128;
	INT iPort;
	//Get the Selected Device Name and ID	
	m_DeviceId.GetLBText(m_DeviceId.GetCurSel(),hldStr);

	ulDisId = GetIntFromHex(hldStr);
	
	//set the display device here
	edidbuf.SbInfo.ulDisplayUID=ulDisId;
	edidbuf.SbInfo.ulAddress=0xa0;
	edidbuf.SbInfo.bForceRead=1;
	edidbuf.SbInfo.ulEdidBlockNum = 0;
	edidbuf.SbInfo.ulEdidSize = 128;
	edidbuf.Cmd=SB_GET_EDID;
    edidbuf.SbInfo.pEdid = edidbuf.pEdid;
	CDC* Cdc = GetDC(); 			// Get the device context object for current window
	HDC hdc = Cdc ->m_hDC;			// Get the device context handle for current window
	
	//Get the EDID for the Selected Device
    Encrypt(&edidbuf,sizeof(SBULT_CUST_EDID_STRUCT));

	if (bWinVista)
	{			 
				 VistaEsc(SB_GET_EDID,sizeof(edidbuf),&edidbuf, FALSE);
	}

	else  
	{
				
				iRet=ExtEscape(hdc,SB_ESCAPE,sizeof(SBULT_CUST_EDID_STRUCT),(LPCSTR)&edidbuf,sizeof(SBULT_CUST_EDID_STRUCT),(LPSTR)&edidbuf);
	}
	

	if(iRet==1)
	{
		edidbuffer=(BYTE *)calloc(128,1);
		memmove(edidbuffer,edidbuf.pEdid,128);
		NumExt = edidbuf.pEdid[126];
		//Check if EDID has Any Extensions
		if(NumExt>0)
		{
			Extension = (BYTE *) calloc( (NumExt * 128),sizeof(BYTE) );
							
			for(INT i=1; i <= NumExt; i++)
			{
				edidbuf.SbInfo.ulDisplayUID=ulDisId;
				edidbuf.SbInfo.ulAddress=0xa0;
				edidbuf.SbInfo.bForceRead=1;
				edidbuf.SbInfo.ulEdidSize = 128;

				edidbuf.SbInfo.ulEdidBlockNum = i;
				
				CDC* Cdc = GetDC(); 			// Get the device context object for current window
				HDC hdc = Cdc ->m_hDC;			// Get the device context handle for current window
				
				edidbuf.Cmd=SB_GET_EDID;
				edidbuf.SbInfo.pEdid = edidbuf.pEdid;
				Encrypt(&edidbuf,sizeof(SBULT_CUST_EDID_STRUCT));	
                //Get the EDID for the Selected Device


				if (bWinVista)
				{

					VistaEsc(SB_GET_EDID,sizeof(edidbuf),&edidbuf, FALSE);
				}
	
				else
				{
					iRet=ExtEscape(hdc,SB_ESCAPE,sizeof(SBULT_CUST_EDID_STRUCT),(LPCSTR)&edidbuf,sizeof(SBULT_CUST_EDID_STRUCT),(LPSTR)&edidbuf);
				}

				if(iRet==1)
				{
					memmove( (Extension + (i-1)*128) ,&edidbuf.pEdid,128);
				}
				else
				{
					MessageBox("Error. while reading Extensions in EDID from the device!!",NULL,MB_OK);
				}
			}
		}
	}
	

	if(iRet<0)
	{
		MessageBox("Error. EDID Info Call Failure/Or Doesnt Contain EDID Info!!",NULL,MB_OK);
	}
	
	//code to display the different details to go here.
	
	if(iRet==1)
	{
		m_Save.EnableWindow(TRUE);
		ClearAll();
		iPort = GetDisplayPortUsed(ulDisId);
		setDisplayName(ulDisId,(PORT_TYPES)iPort);
		getByteValues();
		DisplayInfo();
		getHexValues();
	}
	ReleaseDC(Cdc);
	
	
}

void CEDIDToolDlg::DisplayInfo()
{
	//Display the Information on the Text Box
	
	Text="";
	EDID_STRUCTURE EDID;
	EDID_STRUCTURE1_4 EDID1_4;
	
	
	memmove(&EDID,edidbuffer,128);
	memmove(&EDID1_4,edidbuffer,128);
	
	EDID_BaseBlockParser EDIDParser;
	
	EDIDParser.parseHeader(EDID.HEADER);
	
	EDIDParser.parseManufacturerID(EDID.MANUFACTURER_ID);
	
	EDIDParser.parseProductID(EDID.PRODUCT_ID);
	
	EDIDParser.parseSerialID(EDID.SERIAL_ID);
	
	
	
	
	if (EDID.EDID_VERSION_AND_REVISION.Edid_Version == 1 && EDID.EDID_VERSION_AND_REVISION.Edid_Revision == 4)
	{
		EDIDParser.parseYear_And_Week1_4(EDID1_4.YEAR_AND_WEEK_OF_MANUFACTURE1_4);
		EDIDParser.parseEDID_Version_And_Revision(EDID.EDID_VERSION_AND_REVISION);
		EDIDParser.parseBasicDisplayParameters1_4(EDID1_4.YEAR_AND_WEEK_OF_MANUFACTURE1_4,EDID1_4.BASIC_DISPLAY_PARAMETERS1_4);
		EDIDParser.parsechromaInfo(EDID1_4.CHROMA_INFO);
		EDIDParser.parseEstablishedTiming_i(EDID1_4.ESTABLISHED_TIMING_SECTION_I);	
		EDIDParser.parseEstablishedTiming_ii(EDID1_4.ESTABLISHED_TIMING_SECTION_II);
		EDIDParser.parseManufacturers_Reserved_timing(EDID1_4.MANUFACTURERS_RESERVED_TIMING_SECTION);
	
		EDIDParser.parseStandard_timing_identification(EDID1_4.STANDARD_TIMING_IDENTIFICATION,TRUE);
	
		Text+="[54-71]Descriptor Block I\r\n";
		EDIDParser.checkDescriptorBlock(EDID1_4.DESCRIPTOR_BLOCK_I);
		Text+="[72-89]Descriptor Block II\r\n";
		EDIDParser.checkDescriptorBlock1_4(EDID1_4.DESCRIPTOR_BLOCK_II);
		Text+="[90-107]Descriptor Block III\r\n";
		EDIDParser.checkDescriptorBlock1_4(EDID1_4.DESCRIPTOR_BLOCK_III);
		Text+="[108-125]Descritor Block IV\r\n";
		EDIDParser.checkDescriptorBlock1_4(EDID1_4.DESCRIPTOR_BLOCK_IV);
	
		EDIDParser.checkExtension(EDID1_4.EXTENSION_FLAG);
		EDIDParser.checkSum();
		
	}
	else
	{
		EDIDParser.parseYear_And_Week(EDID.YEAR_AND_WEEK_OF_MANUFACTURE);
		EDIDParser.parseEDID_Version_And_Revision(EDID.EDID_VERSION_AND_REVISION);
		EDIDParser.parseBasicDisplayParameters(EDID.BASIC_DISPLAY_PARAMETERS);
		EDIDParser.parsechromaInfo(EDID.CHROMA_INFO);
		EDIDParser.parseEstablishedTiming_i(EDID.ESTABLISHED_TIMING_SECTION_I);	
		EDIDParser.parseEstablishedTiming_ii(EDID.ESTABLISHED_TIMING_SECTION_II);
		EDIDParser.parseManufacturers_Reserved_timing(EDID.MANUFACTURERS_RESERVED_TIMING_SECTION);
	
		EDIDParser.parseStandard_timing_identification(EDID.STANDARD_TIMING_IDENTIFICATION,TRUE);
	
		Text+="[54-71]Descriptor Block I\r\n";
		EDIDParser.checkDescriptorBlock(EDID.DESCRIPTOR_BLOCK_I);
		Text+="[72-89]Descriptor Block II\r\n";
		EDIDParser.checkDescriptorBlock(EDID.DESCRIPTOR_BLOCK_II);
		Text+="[90-107]Descriptor Block III\r\n";
		EDIDParser.checkDescriptorBlock(EDID.DESCRIPTOR_BLOCK_III);
		Text+="[108-125]Descritor Block IV\r\n";
		EDIDParser.checkDescriptorBlock(EDID.DESCRIPTOR_BLOCK_IV);
	
		EDIDParser.checkExtension(EDID.EXTENSION_FLAG);
		EDIDParser.checkSum();
	}
	

	NumExt = EDID.EXTENSION_FLAG;
	
	for(INT Count = 1; Count <= NumExt && (Extension); Count++)
	{
		CurrentExtNo = Count;
		BYTE * TempExt = (Extension + (Count-1)*128);

		if(*TempExt == BLOCK_MAP_TAG)
		{
			BlockMapExt = TempExt;
			BlockMapFlag = TRUE;			
		}
		else if(*TempExt == CE_EXT_TAG)	
		{		
			ceaext = TempExt;
			cextflag=TRUE;	
		}
		else if( *TempExt == VTB_EXT_TAG)
		{
			vtbext = TempExt;
			vtbextflag=TRUE;				
		}
		else
		{
			MessageBox("Error. EDID has Ext. which is not supported!!",NULL,MB_OK);
			break;
		}

		
		if(BlockMapFlag)
		{
			BLOCK_MAP_EXTENSION BLOCK_MAP_EXT;
			BlockMapExtensionParser BlockMapParser;
			memmove(&BLOCK_MAP_EXT,BlockMapExt,128);
			BlockMapParser.parseBlockMapExtension(BLOCK_MAP_EXT,&m_ByteDetails);
			BlockMapFlag = FALSE;
			BlockMapExt = (BYTE *) 0;
		}
		else if(cextflag)
		{				
			CEA_EXTENSION CEA_EXT;
			CEAExtensionParser CEAParser;
			memmove(&CEA_EXT,ceaext,128);
			CEAParser.parseCEAExtension(CEA_EXT,&m_ByteDetails);
			cextflag = FALSE;
			ceaext = (BYTE *) 0;
		}
		else if(vtbextflag)
		{
			VTB_EXTENSION VTB_EXT;
			VTBExtensionParser VTBParser;
			memmove(&VTB_EXT,vtbext,128);
			VTBParser.parseVTBExtension(VTB_EXT,&m_ByteDetails);
			vtbextflag = FALSE;
			vtbext = (BYTE *) 0;
		}
				
	}	
		
	m_TextData.SetWindowText(Text);		
}

void CEDIDToolDlg::OnByteDetails(NMHDR* pNMHDR, LRESULT* pResult) 
{
	// TODO: Add your control notification handler code here
	
	//Get the Selected Index Value and Populate the Selected Value Text Box
	INT selected=m_ByteDetails.GetSelectionMark();
	m_ByteValues.SetWindowText(m_ByteDetails.GetItemText(selected,1));
	
	*pResult = 0;
}	

void CEDIDToolDlg::OnChangeDeviceId() 
{
	// TODO: Add your control notification handler code here
	//On Change of Device Id
	//Get the Device ID and get the EDID for that Device
	INT iPort = 0;
	CHAR *deviceid=new CHAR[100];
	INT ctr=0;
	ULONG displayid=0;
	m_Read.EnableWindow(TRUE);
	
	m_DeviceId.GetLBText(m_DeviceId.GetCurSel(),deviceid);
	m_Read.EnableWindow(TRUE);
	
	while(deviceid[ctr]!='\0')
	{
		if(deviceid[ctr]>='0' && deviceid[ctr]<='9')
			displayid=16*displayid+deviceid[ctr]-48;
		else if(deviceid[ctr]>64 && deviceid[ctr]<71)
			displayid=16*displayid+deviceid[ctr]-55;
		else if(deviceid[ctr]>96 && deviceid[ctr]<103)
			displayid=16*displayid+deviceid[ctr]-87;
		ctr++;
	}
	
	iPort = GetDisplayPortUsed(displayid);
	setDisplayName(displayid,(PORT_TYPES)iPort);
	


}


void CEDIDToolDlg::setDisplayName(ULONG Id, PORT_TYPES ePort)
{
	ULONG ulDisplayID = Id;
	DISPLAY_ID stDisplayID = {0};
	ENCODER_UID stEncoderUID= {0};
	CString Name="Device : ";
	if(SB_IsCRT(Id))
	{
		Name+="CRT   ";
	}
	if(SB_IsTV(Id))
	{
		Name+="TV   ";
	}
	if(SB_IsLFP(Id))
	{
		Name+="LFP   ";
	}
	if(SB_IsDFP(Id))
	{
		Name+="DFP   ";
	}
	
	stDisplayID.ulDisplayID = ulDisplayID;
	stEncoderUID=stDisplayID.stEncoderId;

	ENCODER_TYPE eType = MAX_ENCODER_TYPES;
	eType = (ENCODER_TYPE)stEncoderUID.ucEncoderType;

	switch(eType)
	{
	case CRT_TYPE:
		Name+="Encoder Type:CRT Type   ";
		break;
	case TV_TYPE:
		Name+="Encoder Type:TV Type   ";
		break;
	case DFP_TYPE:
		Name+="Encoder Type:DFP Type   ";
		break;
	case LFP_TYPE:
		Name+="Encoder Type:LFP Type   ";
		break;
	}

//	printf("Encoder Index:%d\r\n",stEncoderUID.ucEncoderIndex);
	
	CONNECTOR_UID stConnectorUID= {0};
	stConnectorUID=(stDisplayID.stConnectorID);
	CONNECTOR_TYPE eType1 = eMaxConnectorTypes;
		
	eType1 = (CONNECTOR_TYPE)stConnectorUID.ucConnectorType;
	switch(eType1)
	{
	case eUnknownConnector:
		Name+="ConnectorType:Unknown";
		break;
    case e15PinVGA:
		Name+="ConnectorType:15PinVGA";
		break;
    case e5PinBNC:
		Name+="ConnectorType:5PinBNC";
		break;
    case eDVI_D:
		Name+="ConnectorType:DVI/HDMI";
		break;
    case eDVI_A:
		Name+="ConnectorType:DVI_A";
		break;
    case eDVI_I:
		Name+="ConnectorType:DVI_I";
		break;
    case eHDMI:
		Name+="ConnectorType:HDMI";
		break;
    case eLVDS:
		Name+="ConnectorType:LVDS";
		break;
    case eDualChannelLVDS:
		Name+="ConnectorType:DualChannelLVDS";
		break;
    case eComposite:
		Name+="ConnectorType:Composite";
		break;
    case eSVideo:
		Name+="ConnectorType:SVideo";
		break;
    case eComponent:
		Name+="ConnectorType:Component";
		break;
    case eDConnector:
		Name+="ConnectorType:DConnector";
		break;
    case eSCART:
		Name+="ConnectorType:SCART";
		break;
    case eExternalDP:
		Name+="ConnectorType:ExternalDP";
		break;
    case eEmbeddedDP:
		Name+="ConnectorType:EmbeddedDP";
		break;
    case eTPVConnector:
		Name+="ConnectorType:TPV";
		break;
    case eMaxConnectorTypes:
	default:
		Name+="ConnectorType:Unknown";
		break;
	}
	

	switch(ePort)
	{
		
	case NULL_PORT_TYPE:
		Name+="PortType:Unknown";
		break;

    case ANALOG_PORT:
		Name+="   PortType:Analog";
		break;

    case DVOA_PORT:
		Name+="   PortType:SDVO-A";
		break;

    case DVOB_PORT:
		Name+="   PortType:Port-B(Int/SDVO)";
		break;

    case DVOC_PORT:
		Name+="   PortType:Port-C(Int/SDVO)";
		break;
    case DVOD_PORT:
		Name+="   PortType:Port-D(Int/SDVO)";
		break;
    case LVDS_PORT:
		Name+="   PortType:LVDS";
		break;
    case INT_TVOUT_PORT:
		Name+="   PortType:INT TV OUT";
		break;
    case INTHDMIB_PORT:
		Name+="   PortType:HDMI-B";
		break;
    case INTHDMIC_PORT:
		Name+="   PortType:HDMI-C";
		break;
    case INTHDMID_PORT:
		Name+="   PortType:HDMI-D";
		break;
    case INT_DVI_PORT:						//NA
		Name+="   PortType:INT DVI";
		break;
    case INTDPA_PORT:						//Embedded DP For ILK
		Name+="   PortType:DP-A(eDP) ";
		break;
    case INTDPB_PORT:    
		Name+="   PortType:DP-B";
		break;
    case INTDPC_PORT:
		Name+="   PortType:DP-C";
		break;
    case INTDPD_PORT:    
		Name+="   PortType:DP-D";
		break;
    case TPV_PORT:							 //This is for all the TPV Ports..
		Name+="   PortType:TPV";
		break;
    case MAX_PORTS:
		Name+="   PortType:TPV";
		break;
	}

	m_DeviceName.SetWindowText(Name);

//	printf("Connector Index:%d\r\n",stConnectorUID.ucConnectorIndex);

}

void CEDIDToolDlg::getHexValues()
{
	//Display the Binary Values in the Text Box
	CString hexvalue="Binary Data\r\n";
	CString temp="";
	INT mod=0;
	
	hexvalue+="\r\nBase Block\r\n";
	hexvalue+="\r\n";

	for(INT i=0;i<128;i++)
	{			
		temp.Format("0x%02X,",edidbuffer[i]);
		hexvalue+=temp;
		mod++;
		if(mod==10){hexvalue+="\r\n";mod=0;}
	}
	
	for (INT Count = 1; Count <= NumExt && (Extension); Count++)
	{
		BYTE * TempExt = (Extension + (Count-1)*128);
		if(*TempExt == BLOCK_MAP_TAG)
		{
 			BlockMapExt = TempExt;
			BlockMapFlag = TRUE;
		}
		else if(*TempExt == CE_EXT_TAG)	
		{
			ceaext = TempExt;
			cextflag=TRUE;
	
		}
		else if( *TempExt == VTB_EXT_TAG)
		{
			vtbext = TempExt;
			vtbextflag=TRUE;				
		}
		
		
		if(BlockMapFlag)
		{
			hexvalue+="\r\n";
			hexvalue+="\r\nBlock Map Extension Block\r\n";
			hexvalue+="\r\n";
				
			mod=0;
			for(INT i=0;i<128;i++)
			{
				temp.Format("0x%02X,",*(BlockMapExt+i));
				hexvalue+=temp;
				mod++;
				if(mod==10){hexvalue+="\r\n";mod=0;}
			}
			BlockMapFlag = FALSE;
			BlockMapExt = (BYTE *) 0;
		}
		else if(cextflag)
		{
			hexvalue+="\r\n";
			hexvalue+="\r\nCEA Extension Block\r\n";
			hexvalue+="\r\n";
				
			mod=0;
			for(INT i=0;i<128;i++)
			{
				temp.Format("0x%02X,",*(ceaext+i));
				hexvalue+=temp;
				mod++;
				if(mod==10){hexvalue+="\r\n";mod=0;}
			}

			cextflag = FALSE;
			ceaext = (BYTE *) 0;
		}
		else if(vtbextflag)
		{
			hexvalue+="\r\n";
			hexvalue+="\r\nVTB Extension Block\r\n";
			hexvalue+="\r\n";
				
			mod=0;
			for(INT i=0;i<128;i++)
			{
				temp.Format("0x%02X,",*(vtbext+i));
				hexvalue+=temp;
				mod++;
				if(mod==10){hexvalue+="\r\n";mod=0;}
			}
			vtbextflag = FALSE;
			vtbext = (BYTE *) 0;
		}
				
	}
	
	m_HexValues.SetWindowText(hexvalue);
}


void CEDIDToolDlg::getByteValues()
{
	//Get the Actual Byte Values and Populate the List View
	
	CHAR *bytedata=(CHAR *)malloc(256);
	CHAR *temp=(CHAR *)malloc(256);
	INT i=0;

	INT index=m_ByteDetails.InsertItem(++listcount,"*****");
	m_ByteDetails.SetItemText(index,1,"Block No.: 0");
	m_ByteDetails.SetItemText(index,2,"Base Block");
	
	sprintf_s(bytedata,256,"");
	//0-7,Header
	for(i=0;i<8;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	
	index=m_ByteDetails.InsertItem(++listcount,"0-7");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Header");
	
	sprintf_s(bytedata,256,"");
	//8-9,Manufacturer ID
	for(i=8;i<10;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"8-9");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Manufacturer ID");
	
	sprintf_s(bytedata,256,"");
	//10-11,Product ID
	for(i=10;i<12;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"10-11");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Product ID");
	
	sprintf_s(bytedata,256,"");
	//12-15,Serial ID
	for(i=12;i<16;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"12-15");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Serial ID");
	
	sprintf_s(bytedata,256,"");
	//16,Week Of Manufacture
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[16]);
	index=m_ByteDetails.InsertItem(++listcount,"16");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Week Of Manufacture");
	
	sprintf_s(bytedata,256,"");
	//17,Year Of Manufacture
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[17]);
	index=m_ByteDetails.InsertItem(++listcount,"17");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Year of Manufacture");
	
	
	sprintf_s(bytedata,256,"");
	//18,EDID Version Number
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[18]);
	index=m_ByteDetails.InsertItem(++listcount,"18");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"EDID Version");
	
	sprintf_s(bytedata,256,"");
	//19,EDID Revision Number
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[19]);
	index=m_ByteDetails.InsertItem(++listcount,"19");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"EDID Revision");
	
	sprintf_s(bytedata,256,"");
	//20-24,Basic Display Parameters
	for(i=20;i<25;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"20-24");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Basic Display Parameters");
	
	sprintf_s(bytedata,256,"");
	//25-34,Chroma Info
	for(i=25;i<35;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"25-34");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Chroma Info");
	
	
	sprintf_s(bytedata,256,"");
	//35,Established Timing I
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[35]);
	index=m_ByteDetails.InsertItem(++listcount,"35");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Established Timing I");
	
	sprintf_s(bytedata,256,"");
	//36,Established Timing II
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[36]);
	index=m_ByteDetails.InsertItem(++listcount,"36");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Established Timing II");
	
	sprintf_s(bytedata,256,"");
	//37,Manufacturers Reserved Timing
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[37]);
	index=m_ByteDetails.InsertItem(++listcount,"37");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Manufacturers Reserved Timing");
	
	sprintf_s(bytedata,256,"");
	//38-53,Standard Timing Identification
	for(i=38;i<54;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"38-53");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Standard Timing Identification");
	
	
	sprintf_s(bytedata,256,"");
	//54-71,Descriptor Block I
	for(i=54;i<72;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"54-71");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Descriptor Block I");
	
	sprintf_s(bytedata,256,"");
	//72-89,Descriptor Block II
	for(i=72;i<90;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"72-89");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Descriptor Block II");
	
	sprintf_s(bytedata,256,"");
	//90-107,Descriptor Block III
	for(i=90;i<108;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"90-107");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Descriptor Block III");
	
	sprintf_s(bytedata,256,"");
	//108-125,Descriptor Block IV
	for(i=108;i<126;i++)
	{
		sprintf_s(temp,256,"0x%02X,",edidbuffer[i]);
		strcat_s(bytedata,256,temp);
	}
	index=m_ByteDetails.InsertItem(++listcount,"108-125");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Descriptor Block IV");
	
	//126,Extension Flag
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[126]);
	index=m_ByteDetails.InsertItem(++listcount,"126");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"Extension Flag");
	
	
	//127,Check Sum
	sprintf_s(bytedata,256,"0x%02X,",edidbuffer[127]);
	index=m_ByteDetails.InsertItem(++listcount,"127");
	m_ByteDetails.SetItemText(index,1,bytedata);
	m_ByteDetails.SetItemText(index,2,"CheckSum");
}



void CEDIDToolDlg::ClearAll()
{
	//Reset the UI
	m_ByteDetails.DeleteAllItems();
	m_TextData.SetWindowText("");
	m_ByteValues.SetWindowText("");
	m_HexValues.SetWindowText("");
	m_DeviceName.SetWindowText("");
	Text="";
}


void CEDIDToolDlg::OnCloneEdidButton() 
{
	BOOLEAN cextflag=FALSE;
	SBULT_CUST_GETCLONECAPS_ARGS stCloneCaps;
	ULONG ulDisId = 0;
	ULONG ulDisId2 = 0;
	CHAR hldStr[25];
	
	
	memset(&stCloneCaps, 0, sizeof(stCloneCaps));
	stCloneCaps.Cmd = SB_GET_CLONE_MODE_LIST;

	// Get first device
	m_DeviceId.GetLBText(m_DeviceId.GetCurSel(),hldStr);
	//hex to int conversion
	ulDisId = GetIntFromHex(hldStr);

	// Get second device
	ulDisId2 = 0;
	m_DeviceId2.GetLBText(m_DeviceId2.GetCurSel(),hldStr);
	//hex to int conversion
	ulDisId2 = GetIntFromHex(hldStr);

	if (ulDisId != ulDisId2)
	{
		stCloneCaps.SbInfo.EdidSize = 256; 
		stCloneCaps.SbInfo.stDispEDIDPolicy.bActiveEDIDRead = 1;
		stCloneCaps.SbInfo.stDispEDIDPolicy.bRR_Intersection = 0;
		stCloneCaps.SbInfo.stDispEDIDPolicy.bX_Y_Bpp_Intersection = 1;
		stCloneCaps.SbInfo.ulDisplay1UID = ulDisId;
		stCloneCaps.SbInfo.ulDisplay2UID = ulDisId2;
		stCloneCaps.stGetCloneModeList.stDisplayList.nDisplays = 2;
		stCloneCaps.stGetCloneModeList.stDisplayList.ulDisplayUID[0] = ulDisId;
		stCloneCaps.stGetCloneModeList.stDisplayList.ulDisplayUID[1] = ulDisId2;
		stCloneCaps.stGetCloneModeList.ulNumMode = 0;
		stCloneCaps.stGetCloneModeList.pModeInfo = NULL;

		CDC* Cdc = GetDC(); 			// Get the device context object for current window
		HDC hdc = Cdc ->m_hDC;			// Get the device context handle for current window
		
		Encrypt(&stCloneCaps,sizeof(stCloneCaps));


	if (bWinVista)
	{

		VistaEsc(SB_GET_CLONE_MODE_LIST,sizeof(stCloneCaps),&stCloneCaps, TRUE);
	}
	else
	{
		iRet=ExtEscape(hdc,SB_ESCAPE,sizeof(stCloneCaps),(LPCSTR)&stCloneCaps,sizeof(stCloneCaps),(LPSTR)&stCloneCaps);
	}
		
		if(iRet==1)
		{
			edidbuffer=(BYTE *)calloc(128,1);
			memmove(edidbuffer,stCloneCaps.SbInfo.EdidData,128);
	
			//Check if EDID has Any Extensions
			if(stCloneCaps.SbInfo.EdidData[126]>0)
			{
				//Extension Found!! Copy on to the buffer.
				Extension=(BYTE *)calloc(128,1);					
				memmove(Extension,&(stCloneCaps.SbInfo.EdidData[128]),128);					
			} 

		}
		if(iRet<0)
		{
			MessageBox("Error. EDID Info Call Failure/Or Doesnt Contain EDID Info!!",NULL,MB_OK);
		}
		
		//code to display the different details to go here.
		
		if(iRet==1)
		{
			m_Save.EnableWindow(TRUE);
			ClearAll();
			INT iPort = GetDisplayPortUsed(ulDisId);
			setDisplayName(ulDisId,(PORT_TYPES)iPort);
			getByteValues();
			DisplayInfo();
			getHexValues();
		}
		ReleaseDC(Cdc);

	}
	else
	{
		MessageBox("Error. Select different displays!",NULL,MB_OK);
	}

	return;
}

// Function to issue escape call and get display ID details
INT CEDIDToolDlg::GetDisplayPortUsed(ULONG ulDisplayID)
{
	SBULT_QUERY_DISPLAY_DETAILS_ARGS stArgs = {0};
	// Issue escape
    CDC* Cdc =  GetDC();			// Get the device context object for current window
    HDC hdc = Cdc ->m_hDC;       // Get the device context handle for current window

	stArgs.Cmd = SB_QUERY_DISPLAYID_DETAILS;
	stArgs.SbInfo.eflag = QUERY_DISPLAYTYPE_INDEX;
	stArgs.SbInfo.ulDisplayUID = ulDisplayID;

	Encrypt(&stArgs,sizeof(SBULT_QUERY_DISPLAY_DETAILS_ARGS));

	if (bWinVista)
	{	 
		VistaEsc(SB_QUERY_DISPLAYID_DETAILS,sizeof(stArgs),&stArgs, TRUE);
	}
	else
	{
		iRet=ExtEscape(hdc,SB_ESCAPE,sizeof(stArgs),(LPCSTR)&stArgs,sizeof(stArgs),(LPSTR)&stArgs);
	}

	ReleaseDC(Cdc);

	if (iRet == 1)
		return (INT)stArgs.SbInfo.ePortType;
	else
		return (INT)NULL_PORT_TYPE;
}
