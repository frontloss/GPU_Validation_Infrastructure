/*===========================================================================
; SideBandMessaging.c
;----------------------------------------------------------------------------
;    Copyright (c) 2015  Intel Corporation.
;    All Rights Reserved.  Copyright notice does not imply publication.
;    This software is protected as an unpublished work.  This software
;    contains the valuable trade secrets of Intel Corporation, and must
;    and must be maintained in confidence.
;
; File Description:
;    SideBandMessageParserDlg.cpp : implementation file
;
;--------------------------------------------------------------------------*/
// Author: smukhe5

#include "stdafx.h"
#include "SidebandMsgParser.h"
#include "SidebandMsgParserDlg.h"
#include "afxdialogex.h"
//#include <SbArgs.h>
#include "SideBandMessageDef.h"

#include <string>

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

BYTE g_EDID[128] = { 0 };
// copied from driver


// Buffer size for Sideband message 
#define SB_MAX_MSG_BUFF_SIZE 512 

// size of message list
#define SB_MAX_MSG_NUM 30
//Based on DP1.2 Spec. Total Number of Links is 15
#define MAX_LINK_COUNT 15 

//As every Address for a link requires 4 Bits, therefore total 14 links (MAX_LINK_COUNT - 1, since for 1st link RAD is not required) would require 56 bits.
//Hence total 7 Bytes
#define MAX_BYTES_RAD  ((MAX_LINK_COUNT )/2)

#pragma pack(1)
typedef struct _RELATIVEADDRESS
{
    UCHAR ucTotalLinkCount;

    //If ucTotalLinkCount is 1 then Relative ucAddress should have zero value at all the indexes..

    //If the ucTotalLinkCount is Even then index from 0 till (ucTotalLinkCount/2 - 1) (apart from the Upper Nibble of last index) is a Valid Address, .

    //If the ucTotalLinkCount is Odd then index from 0 till (ucTotalLinkCount)/2 - 1) will be a Valid Address

    //Hence for both odd/even ucTotalLinkCount, we can use Index from 0 till (ucTotalLinkCount/2 - 1)

    UCHAR ucAddress[MAX_BYTES_RAD];

}RELATIVEADDRESS, *PRELATIVEADDRESS;


typedef enum _SB_REQ_ID_TYPE
{
    SB_GET_MESSAGE_TRANSACTION_VERSION = 0x00,
    SB_LINK_ADDRESS = 0x01,        // PATH_MSG , BROADCAST_MSG = 0
    SB_CONNECTION_STATUS_NOTIFY = 0x02,        // UPSTREAM_MSG
    SB_ENUM_PATH_RESOURCES = 0x10,        // PATH_MSG = 1, BROADCAST_MSG = 0
    SB_ALLOCATE_PAYLOAD = 0x11,        // PATH_MSG = 1, BROADCAST_MSG = 0
    SB_QUERY_PAYLOAD = 0x12,        // PATH_MSG = 1, BROADCAST_MSG = 0
    SB_RESOURCE_STATUS_NOTIFY = 0x13,        // UPSTREAM_MSG
    SB_CLEAR_PAYLOAD_ID_TABLE = 0x14,        // PATH_MSG = 1, BROADCAST_MSG = 1
    SB_REMOTE_DPCD_READ = 0x20,        // PATH_MSG = 0, BROADCAST_MSG = 0 
    SB_REMOTE_DPCD_WRITE = 0x21,        // PATH_MSG = 0, BROADCAST_MSG = 0  
    SB_REMOTE_I2C_READ = 0x22,        // PATH_MSG = 0, BROADCAST_MSG  =0  
    SB_REMOTE_I2C_WRITE = 0x23,        // PATH_MSG = 0, BROADCAST_MSG = 0 
    SB_POWER_UP_PHY = 0x24,        // PATH_MSG = 1, BROADCAST_MSG = 0 
    SB_POWER_DOWN_PHY = 0x25,        // PATH_MSG = 1, BROADCAST_MSG = 0 
    SB_SINK_EVENT_NOTIFY = 0x30,        // UPSTREAM_MSG,(Functionality Undefined)
    SB_QUERY_STREAM_ENCRYPTION_STATUS = 0x38,        // Undefined.
    SB_UNDEFINED = 0XFF
}SB_REQ_ID_TYPE;


typedef enum _PEER_DEVICE_TYPE
{
    eInValidType = 0,
    eSSTBranchDevice = 1,
    eMSTBranchDevice = 2,
    eSSTSinkorStreamSink = 3,
    eDP2LegacyConverter = 4,
    eDP2WirelessConverter = 5
}PEER_DEVICE_TYPE;


typedef struct _SB_MESSAGEINFO
{
    RELATIVEADDRESS stRelativeAddress;
    SB_REQ_ID_TYPE eReqIDType;
    ULONG ulTimeDelayforReply;
    ULONG ulBufferLength;
    BYTE  byMsgBuffer[SB_MAX_MSG_BUFF_SIZE];
}SB_MESSAGEINFO, *PSB_MESSAGEINFO;

typedef struct _SIDEBAND_HEADER_TOP
{
    BYTE Link_Count_Remaining : 4;
    BYTE Link_Count_Total : 4;
} SIDEBAND_HEADER_TOP, *PSIDEBAND_HEADER_TOP;

typedef struct _SIDEBAND_HEADER_BOTTOM
{
    BYTE SideBand_MSG_Body_Length : 6;
    BYTE Path_Message : 1;
    BYTE Broadcast_Message : 1;

    BYTE Sideband_MSG_Header_CRC : 4;
    BYTE Message_Sequence_No : 1;
    BYTE ucZero : 1;
    BYTE EMT : 1;
    BYTE SMT : 1;
} SIDEBAND_HEADER_BOTTOM, *PSIDEBAND_HEADER_BOTTOM;

typedef struct _SIDEBAND_MSG_HEADER
{
    SIDEBAND_HEADER_TOP SBMSG_HEADER_TOP;
    UCHAR ucRelativeAddress[MAX_BYTES_RAD];
    SIDEBAND_HEADER_BOTTOM SBMSG_HEADER_BOTTOM;
}SIDEBAND_MSG_HEADER, *PSIDEBAND_MSG_HEADER;

typedef struct _SBM_UP_REQ_EVENT
{
    UCHAR ucConnectionStatusNotify : 1;
    UCHAR ucResourceStatusNotify : 1;
    UCHAR ucSinkEventNotify : 1;
    UCHAR ecReserve : 5;
}SBM_UP_REQ_EVENT, *PSBM_UP_REQ_EVENT;

#pragma pack()

// globals 
CString g_sMsgBuff;
CString g_sDisplayText;


// CAboutDlg dialog used for App About

class CAboutDlg : public CDialogEx
{
public:
    CAboutDlg();

    // Dialog Data
    enum { IDD = IDD_ABOUTBOX };

protected:
    virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support

    // Implementation
protected:
    DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(CAboutDlg::IDD)
{}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
    CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)
END_MESSAGE_MAP()


// CSidebandMsgParserDlg dialog



CSidebandMsgParserDlg::CSidebandMsgParserDlg(CWnd* pParent /*=NULL*/)
    : CDialogEx(CSidebandMsgParserDlg::IDD, pParent)
{
    m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CSidebandMsgParserDlg::DoDataExchange(CDataExchange* pDX)
{
    CDialogEx::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_EDIT2, m_editDisplay);
    DDX_Control(pDX, IDC_EDIT1, m_EditInput);
    DDX_Control(pDX, IDC_BUTTON6, m_btnTest);
}

BEGIN_MESSAGE_MAP(CSidebandMsgParserDlg, CDialogEx)
    ON_WM_SYSCOMMAND()
    ON_WM_PAINT()
    ON_WM_QUERYDRAGICON()
    ON_BN_CLICKED(IDC_BUTTON1, &CSidebandMsgParserDlg::OnBnClickedButton1)
    ON_BN_CLICKED(IDOK, &CSidebandMsgParserDlg::OnBnClickedOk)
    ON_BN_CLICKED(IDCANCEL, &CSidebandMsgParserDlg::OnBnClickedCancel)
    ON_BN_CLICKED(IDC_BTN_LINK_ADD, &CSidebandMsgParserDlg::OnBnClickedBtnLinkAdd)
    ON_BN_CLICKED(IDC_BTN_REMOTE_EDID, &CSidebandMsgParserDlg::OnBnClickedBtnRemoteEdid)
    ON_BN_CLICKED(IDC_BTN_EPR, &CSidebandMsgParserDlg::OnBnClickedBtnEpr)
    ON_EN_SETFOCUS(IDC_EDIT1, &CSidebandMsgParserDlg::OnEnSetfocusEdit1)
    ON_BN_CLICKED(IDC_ALLOC_PAY_LOAD, &CSidebandMsgParserDlg::OnBnClickedAllocPayLoad)
    ON_BN_CLICKED(IDC_BUTTON6, &CSidebandMsgParserDlg::OnBnClickedButton6)
    ON_BN_CLICKED(IDC_BUTTON_COPY, &CSidebandMsgParserDlg::OnBnClickedButtonCopy)
    ON_BN_CLICKED(IDC_BUTTON_PASTE, &CSidebandMsgParserDlg::OnBnClickedButtonPaste)
END_MESSAGE_MAP()


// CSidebandMsgParserDlg message handlers

BOOL CSidebandMsgParserDlg::OnInitDialog()
{
    CDialogEx::OnInitDialog();

    // Add "About..." menu item to system menu.

    // IDM_ABOUTBOX must be in the system command range.
    ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
    ASSERT(IDM_ABOUTBOX < 0xF000);

    CMenu* pSysMenu = GetSystemMenu(FALSE);
    if (pSysMenu != NULL)
    {
        BOOL bNameValid;
        CString strAboutMenu;
        bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
        ASSERT(bNameValid);
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
#if _DEBUG
    m_btnTest.ShowWindow(SW_SHOW);
#endif
    // TODO: Add extra initialization here
    SetInstructionText();
    return TRUE;  // return TRUE  unless you set the focus to a control
}

void CSidebandMsgParserDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
    if ((nID & 0xFFF0) == IDM_ABOUTBOX)
    {
        CAboutDlg dlgAbout;
        dlgAbout.DoModal();
    }
    else
    {
        CDialogEx::OnSysCommand(nID, lParam);
    }
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CSidebandMsgParserDlg::OnPaint()
{
    if (IsIconic())
    {
        CPaintDC dc(this); // device context for painting

        SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

        // Center icon in client rectangle
        int cxIcon = GetSystemMetrics(SM_CXICON);
        int cyIcon = GetSystemMetrics(SM_CYICON);
        CRect rect;
        GetClientRect(&rect);
        int x = (rect.Width() - cxIcon + 1) / 2;
        int y = (rect.Height() - cyIcon + 1) / 2;

        // Draw the icon
        dc.DrawIcon(x, y, m_hIcon);
    }
    else
    {
        CDialogEx::OnPaint();
    }
}

// The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CSidebandMsgParserDlg::OnQueryDragIcon()
{
    return static_cast<HCURSOR>(m_hIcon);
}

BYTE CalculateHeaderCRC(const PBYTE data, int iNoOfNibbles)
{
    BYTE BitMask = 0x80;
    BYTE BitShift = 7;
    BYTE ArrayIndex = 0;
    int NumberOfBits = iNoOfNibbles * 4;
    BYTE Remainder = 0;

    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;
        Remainder |= (data[ArrayIndex] & BitMask) >> BitShift;
        BitMask >>= 1;
        BitShift--;

        if (BitMask == 0)
        {
            BitMask = 0x80;
            BitShift = 7;
            ArrayIndex++;
        }

        if ((Remainder & 0x10) == 0x10)
        {
            Remainder ^= 0x13;
        }
    }

    NumberOfBits = 4;

    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;

        if ((Remainder & 0x10) != 0)
        {
            Remainder ^= 0x13;
        }
    }

    return Remainder;
}

BYTE CalculateDataCRC(const PBYTE data, int iNoOfNibbles)
{
    BYTE BitMask = 0x80;
    BYTE BitShift = 7;
    BYTE ArrayIndex = 0;
    USHORT NumberOfBits = iNoOfNibbles * 8;
    USHORT Remainder = 0;

    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;
        Remainder |= (data[ArrayIndex] & BitMask) >> BitShift;
        BitMask >>= 1;
        BitShift--;
        if (BitMask == 0)
        {
            BitMask = 0x80;
            BitShift = 7;
            ArrayIndex++;
        }

        if ((Remainder & 0x100) == 0x100)
        {
            Remainder ^= 0xD5;
        }
    }

    NumberOfBits = 8;
    while (NumberOfBits != 0)
    {
        NumberOfBits--;
        Remainder <<= 1;
        if ((Remainder & 0x100) != 0)
        {
            Remainder ^= 0xD5;
        }
    }

    return Remainder & 0xFF;
}

bool ConvertStringToHex(CAtlString input, BYTE pOutput[], DWORD *pLength)
{
    int iCurPos = 0;
    CAtlString Token;
    Token = input.Tokenize(_T(" ,"), iCurPos);

    int index = 0;
    while (_T("") != Token)
    {
        if (Token.Find(_T("0x"), 0) == -1)
        {
            swscanf_s(Token, _T("%x"), &pOutput[index]);
        }
        else
        {
            swscanf_s(Token, _T("0x%x"), &pOutput[index]);
        }
        ++index;
        Token = input.Tokenize(_T(" ,"), iCurPos);
    }
    *pLength = index;

    return true;
}

// Read reply header
bool ReadMsgHeader(BYTE pbBuff[], DWORD ulBufferSize, PSIDEBAND_MSG_HEADER pMsgHeader)
{
    // parse header 
    bool bRet = false;
    UCHAR ucHDRSize = SIDEBAND_MSG_STATIC_HEADER_SIZE, ucRADSize = 0;

    do
    {
        if (pbBuff == NULL || pMsgHeader == NULL || ulBufferSize < SIDEBAND_MSG_STATIC_HEADER_SIZE)
        {
            // invalid args !!
            break;
        }

        // read header top
        memcpy(&pMsgHeader->SBMSG_HEADER_TOP, pbBuff, sizeof(SIDEBAND_HEADER_TOP));
        if (pMsgHeader->SBMSG_HEADER_TOP.Link_Count_Total > 1)
        {
            ucRADSize = (pMsgHeader->SBMSG_HEADER_TOP.Link_Count_Total) / 2;
            if (ucRADSize > MAX_BYTES_RAD)
            {
                break;
            }
            ucHDRSize += ucRADSize;
            if (ucHDRSize > ulBufferSize) // validate the boundary 
            {
                // not enough length
                break;
            }
            // copy the RAD 
            memcpy(pMsgHeader->ucRelativeAddress, pbBuff + sizeof(SIDEBAND_HEADER_TOP), ucRADSize);
        }
        // read header bottom
        memcpy(&pMsgHeader->SBMSG_HEADER_BOTTOM, pbBuff + sizeof(SIDEBAND_HEADER_TOP) + ucRADSize, sizeof(SIDEBAND_HEADER_BOTTOM));


        bRet = true;

    } while (FALSE);

    return bRet;
}

// Create header for SBM reply data 
PBYTE CreateHeader(PRELATIVEADDRESS pRAD, SB_REQ_ID_TYPE RequestID, UCHAR ucSBMLength, BOOLEAN bSMT, BOOLEAN bEMT, BOOLEAN bMSN, PUCHAR pucHeaderSize)
{
    PBYTE pHeader = NULL;
    BYTE byHeader[MAX_BYTES_RAD + 3] = { 0 };
    UCHAR ucIndex = 0;
    UCHAR ucRADsize = 0;
    SIDEBAND_MSG_HEADER SBM_Header = { 0 };
    RAD_BYTE_ST stRADByte = { 0 };

    if (pRAD)
    {
        SBM_Header.SBMSG_HEADER_TOP.Link_Count_Total = pRAD->ucTotalLinkCount;
        //sjm link cnt remaining 0 for reply: SBM_Header.SBMSG_HEADER_TOP.Link_Count_Remaining = pRAD->ucTotalLinkCount - 1;

        // If LinkCount is more than one, then we need to fill up the  RAD appropriately.
        // RAD should be byte aligned. This is assumed to be taken care by caller.

        ucRADsize = SIZE_OF_RAD(SBM_Header);

        if (ucRADsize > 0)
        {
            memcpy(SBM_Header.ucRelativeAddress, pRAD->ucAddress, ucRADsize);
            if (pRAD->ucTotalLinkCount % 2 == 0)
            {
                stRADByte.ucData = pRAD->ucAddress[ucRADsize - 1];
                stRADByte.LowerRAD = 0;
                SBM_Header.ucRelativeAddress[ucRADsize - 1] = stRADByte.ucData;
            }
        }
    }

    // Fill up the rest of the SideBandMessage Parameters.
    SBM_Header.SBMSG_HEADER_BOTTOM.Broadcast_Message = IS_BROADCAST_MSG(RequestID);
    SBM_Header.SBMSG_HEADER_BOTTOM.Path_Message = IS_PATH_MSG(RequestID);
    SBM_Header.SBMSG_HEADER_BOTTOM.SideBand_MSG_Body_Length = ucSBMLength;

    SBM_Header.SBMSG_HEADER_BOTTOM.SMT = bSMT;
    SBM_Header.SBMSG_HEADER_BOTTOM.EMT = bEMT;
    SBM_Header.SBMSG_HEADER_BOTTOM.ucZero = 0;
    SBM_Header.SBMSG_HEADER_BOTTOM.Message_Sequence_No = bMSN;

    // Copy the Header structure to a byte array for CRC Calculation.
    if (byHeader)
    {
        memcpy(&byHeader[0], &SBM_Header.SBMSG_HEADER_TOP, 1);
        ucIndex++;

        if (SBM_Header.SBMSG_HEADER_TOP.Link_Count_Total > 1)
        {
            memcpy(&byHeader[ucIndex], SBM_Header.ucRelativeAddress, ucRADsize);
            ucIndex += ucRADsize;
        }

        memcpy(&byHeader[ucIndex], &SBM_Header.SBMSG_HEADER_BOTTOM, sizeof(SIDEBAND_HEADER_BOTTOM));
    }


    // Calculate Header CRC
    SBM_Header.SBMSG_HEADER_BOTTOM.Sideband_MSG_Header_CRC = CalculateHeaderCRC((PBYTE)byHeader, SIDEBAND_MSG_HEADER_CRC_NIBBLES(SBM_Header));
    // Copy CRC also back into the array.
    memcpy(&byHeader[ucIndex], &SBM_Header.SBMSG_HEADER_BOTTOM, sizeof(SIDEBAND_HEADER_BOTTOM));


    // Fill up Size
    *pucHeaderSize = ucRADsize + SIDEBAND_MSG_STATIC_HEADER_SIZE;
    /*if (SB_ENUM_PATH_RESOURCES == RequestID || SB_ALLOCATE_PAYLOAD == RequestID)
    {
    pHeader = pThis->m_pbyStaticHeaderBuffer;
    }
    else*/
    {
        // Fill up Header Buffer. This should be freed up by the caller.
        pHeader = (PBYTE)malloc(*pucHeaderSize);
        memset(pHeader, 0, *pucHeaderSize);
    }

    if (pHeader)
    {
        memcpy(pHeader, byHeader, *pucHeaderSize);
    }


    return pHeader;
}


PBYTE CreateMessagePackets(PRELATIVEADDRESS pRelativeAddress, PBYTE pbyBody, ULONG ulDataSz, PULONG pulFinalBufSize)
{
    ULONG ucBodyLenRem = ulDataSz;
    UCHAR ucMaxDataLen = 32;
    UCHAR curDataSz = 0;
    PBYTE pMsgBuffer = NULL;
    ULONG uDstOffset = 0;
    UCHAR ucHeaderLength;
    PBYTE pHeaderBuffer = NULL;
    BOOLEAN bSMT = 1, bEMT = 0;
    REPLY_DATA stReplyData = { 0 };
    UCHAR ucDataCRC = 0;

    memcpy(&stReplyData, pbyBody, 1);
    pMsgBuffer = (PBYTE)malloc(512);
    *pulFinalBufSize = 0;
    while (ucBodyLenRem > 0)
    {
        if (pHeaderBuffer)
        {
            free(pHeaderBuffer);
            pHeaderBuffer = NULL;
        }
        if (ucBodyLenRem > ucMaxDataLen)
        {
            curDataSz = ucMaxDataLen;
        }
        else
        {
            curDataSz = (UCHAR)ucBodyLenRem;
            bEMT = TRUE;
        }
        ucDataCRC = CalculateDataCRC((PBYTE)(pbyBody + uDstOffset), curDataSz);
        pHeaderBuffer = CreateHeader(pRelativeAddress, (SB_REQ_ID_TYPE)stReplyData.ucRequestID, curDataSz + 1, bSMT, bEMT, 0, &ucHeaderLength);

        memcpy(pMsgBuffer + *pulFinalBufSize, pHeaderBuffer, ucHeaderLength);
        *pulFinalBufSize += ucHeaderLength;
        memcpy(pMsgBuffer + *pulFinalBufSize, pbyBody + uDstOffset, curDataSz);
        *pulFinalBufSize += curDataSz;
        memcpy(pMsgBuffer + *pulFinalBufSize, &ucDataCRC, 1);
        *pulFinalBufSize += 1;

        uDstOffset += curDataSz;
        ucBodyLenRem -= curDataSz;
        bSMT = FALSE;
    }

    if (pHeaderBuffer)
    {
        free(pHeaderBuffer);
        pHeaderBuffer = NULL;
    }
    return pMsgBuffer;

}
void CSidebandMsgParserDlg::SetInstructionText()
{
    // set info test
    m_EditInput.SetWindowText(_T("\t-- Input Data field --\r\nParse or Create Side Band Down Reply Msg packet.\r\n\r\nEnter full Sideband reply buffer from SMT to EMT for parsing, \r\nor \r\nEnter reply details in below form to create Reply data buffer."));

    //m_editDisplay.SetWindowText(_T(""));
    g_sDisplayText = _T("input Param syntax to create Side Band Reply Msg packet:\r\n\r\n");
    g_sDisplayText += _T("Link Address:\r\n\t{Branch RAD}{leaf,branch,....}{portNumbers}\r\n\t e.g.{0.2.3.1}{L,B,L,...}{1,8,2,3,...}\r\n\r\n");
    g_sDisplayText += _T("Enum Path Resource:\r\n\t{Leaf RAD}{FullPBN,AvlPBN}\r\n\t e.g.{0.2.3.1.2}{2560,1280}\r\n\r\n");
    g_sDisplayText += _T("Read Remote EDID:\r\n\t{Leaf RAD}{EDID buffer}\r\n\t e.g.{0.2.3.1.2}{0x00 0x11 0xff ....}\r\n\r\n");
    g_sDisplayText += _T("Allocate Payload:\r\n\t{Leaf RAD}{PBN}{vcID}\r\n\t e.g.{0.2.3.1.2}{2560}{1}");
    m_editDisplay.SetWindowText(g_sDisplayText);
    //g_sDisplayText.ReleaseBuffer();//
    m_bInit = true;
}

void CSidebandMsgParserDlg::OnBnClickedButton1()
{
    ParseMsg();
}
bool CSidebandMsgParserDlg::ValidateAndExtractData()
{
    bool bRet = true;
    BYTE ucOffset = 0;
    PBYTE pDownReplyData = NULL;
    UCHAR ucDataBufferSize = 0;
    ULONG ucHeaderCRC = 0, ucBodyCRC = 0;
    SIDEBAND_MSG_HEADER SBM_HEADER = { 0 };
    REPLY_DATA stReplyData = { 0 };

    pDownReplyData = (PBYTE)malloc(512);
    memset(pDownReplyData, 0, 512);

    while (ucOffset < m_dwBuffLen && true == bRet)
    {
        memset(&SBM_HEADER, 0, sizeof(SBM_HEADER));
        bRet = ReadMsgHeader(m_byBuffer + ucOffset, m_dwBuffLen - ucOffset, &SBM_HEADER);
        if (bRet == false)
            break;

        ucHeaderCRC = CalculateHeaderCRC(m_byBuffer + ucOffset, 2 * SIZE_OF_MSG_HDR(SBM_HEADER) - 1);
        ucOffset += SIZE_OF_MSG_HDR(SBM_HEADER);
        if (ucHeaderCRC != SBM_HEADER.SBMSG_HEADER_BOTTOM.Sideband_MSG_Header_CRC)
        {
            bRet = false;
            break;
        }


        if (SBM_HEADER.SBMSG_HEADER_BOTTOM.SMT == 1) // Start of Message.
        {
            ReadMessage(m_byBuffer, (PBYTE)&stReplyData, ucOffset, sizeof(stReplyData));
            //ucOffset += sizeof(stReplyData);
            if (stReplyData.bReplyType == 0) // ACK
            {
                //pDownReplyData = SIDEBANDMESSAGING_ReAllocateMemory(pThis, pDownReplyData, ucDataBufferSize, 0, ucDataBufferSize + GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER) ,FALSE,NULL);
                if (pDownReplyData)
                {
                    memcpy(&pDownReplyData[ucDataBufferSize], &m_byBuffer[ucOffset], GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER));
                    ucDataBufferSize += GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER); // No CRC.
                    ucOffset += SBM_HEADER.SBMSG_HEADER_BOTTOM.SideBand_MSG_Body_Length;
                }
                else
                {
                    bRet = FALSE;
                }
            }
        }
        else
        {
            //pDownReplyData = SIDEBANDMESSAGING_ReAllocateMemory(pThis, pDownReplyData, ucDataBufferSize, 0, ucDataBufferSize + GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER) ,FALSE,NULL);
            if (pDownReplyData)
            {
                memcpy(&pDownReplyData[ucDataBufferSize], &m_byBuffer[ucOffset], GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER));
                ucDataBufferSize += GET_SIDEBAND_MSG_PAYLOAD_SIZE(SBM_HEADER); // No CRC.
                ucOffset += SBM_HEADER.SBMSG_HEADER_BOTTOM.SideBand_MSG_Body_Length;
            }
        }
    }

    if (bRet)
    {
        memcpy(&m_byBuffer[0], pDownReplyData, ucDataBufferSize);
        m_dwBuffLen = ucDataBufferSize;
    }

    if (pDownReplyData)
    {
        free(pDownReplyData);
        pDownReplyData = NULL;
    }

    return bRet;

}

bool CSidebandMsgParserDlg::ReadMessage(BYTE pbBuff[], PBYTE pout, BYTE byOffset, DWORD dwSize)
{
    bool bRet = FALSE;

    // Note:- For Up Request we are not parsing detailed information as of now, will change this to read from 
    //        Up Request buffer once that is required.
    if (pbBuff && pout && (byOffset + dwSize <= m_dwBuffLen))
    {
        memcpy(pout, (PBYTE)(m_byBuffer)+byOffset, dwSize);
        bRet = true;
    }

    return bRet;
}

void CSidebandMsgParserDlg::ParseMsg()
{
    CString sTemp = _T("");
    SIDEBAND_MSG_HEADER HDR = { 0 };
    CString sRADBytes = _T("RAD Bytes: ");
    CString sRAD = _T("RAD: ");
    // UCHAR ucRequestID;

    // init window text
    m_editDisplay.SetWindowText(_T(""));
    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;

    m_EditInput.GetWindowText(g_sMsgBuff.GetBuffer((MAX_MSG_BYTES+1) * 5), MAX_MSG_BYTES * 5);
    g_sMsgBuff.ReleaseBuffer();

    g_sMsgBuff.Trim(_T(" \r\n:{}"));

    ConvertStringToHex(g_sMsgBuff.GetBuffer(), m_byBuffer, &m_dwBuffLen);
    g_sMsgBuff.ReleaseBuffer();

    ReadMsgHeader(m_byBuffer, m_dwBuffLen, &HDR);
    // display header
    g_sDisplayText = _T("Message Header\r\n");

    sTemp.Format(_T("Header top:\r\n\tLink count total: %d, Link Count Remaining: %d\r\n"), HDR.SBMSG_HEADER_TOP.Link_Count_Total, HDR.SBMSG_HEADER_TOP.Link_Count_Remaining);
    g_sDisplayText += sTemp;

    sTemp.Format(_T("Header Bottom:\r\n\tSideBand_MSG_Body_Length: %d, Path_Message: %d, Broadcast_Message: %d,\r\n\tSideband_MSG_Header_CRC: %d, Message_Sequence_No: %d, EMT: %d, SMT: %d\r\n"),
                 HDR.SBMSG_HEADER_BOTTOM.SideBand_MSG_Body_Length, HDR.SBMSG_HEADER_BOTTOM.Path_Message, HDR.SBMSG_HEADER_BOTTOM.Broadcast_Message,
                 HDR.SBMSG_HEADER_BOTTOM.Sideband_MSG_Header_CRC, HDR.SBMSG_HEADER_BOTTOM.Message_Sequence_No, HDR.SBMSG_HEADER_BOTTOM.EMT, HDR.SBMSG_HEADER_BOTTOM.SMT);

    g_sDisplayText += sTemp;
    // RAD
    if (HDR.SBMSG_HEADER_TOP.Link_Count_Total > 0)
    {
        sRAD += _T("0.");
        if (HDR.SBMSG_HEADER_TOP.Link_Count_Total > 1)
        {
            for (int i = 0; i < HDR.SBMSG_HEADER_TOP.Link_Count_Total - 1; i++)
            {
                RAD_BYTE_ST addByte;
                addByte.ucData = HDR.ucRelativeAddress[i / 2];
                char Port = (i % 2) != 0 ? (addByte.ucData & 0xF) : (addByte.ucData & 0xF0) >> 4; // big endian
                sTemp.Format(_T("%d."), Port);
                sRAD += sTemp;
                if (i % 2 == 0)
                    sRADBytes.AppendFormat(_T("[%#x] "), addByte.ucData);
            }
        }
        else
        {
            sRADBytes += _T("NONE");
        }

        g_sDisplayText += sRADBytes + _T("\r\n") + sRAD + _T("\r\n");
    }
    // print header bytes
    g_sDisplayText += _T("Header Bytes: ");
    for (int i = 0; i < SIZE_OF_MSG_HDR(HDR); i++)
    {
        sTemp.Format(_T("0x%02x "), m_byBuffer[i]);
        g_sDisplayText += sTemp;
    }
    g_sDisplayText += _T("\r\n");

    try
    {
        UCHAR ucOffset = 0;
        REPLY_DATA stReplyData = { 0 };
        ValidateAndExtractData();
        ReadMessage(m_byBuffer, (PBYTE)&stReplyData, ucOffset, sizeof(stReplyData));
        ucOffset += sizeof(stReplyData);

        if (stReplyData.ucRequestID == SB_LINK_ADDRESS)
        {
            UCHAR ucCount = 0;
            SB_LINK_ADDRESS_REPLY_DATA stLinkAddressReplyData = { 0 };
            SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0 stLinkAddressPortDetails_0 = { 0 };
            SB_LINK_ADDRESS_REPLY_PORT_DETAILS stLinkAddressPortDetails = { 0 };

            g_sDisplayText += _T("\r\nMessage Body:\r\nRequest Type: Link Address\r\n");

            {


                ReadMessage(m_byBuffer, (PBYTE)&stLinkAddressReplyData, ucOffset, sizeof(stLinkAddressReplyData));
                ucOffset += sizeof(stLinkAddressReplyData);

                if (stLinkAddressReplyData.guid.Data1 != 0)
                {
                    // print GUID
                    OLECHAR* bstrGuid;
                    StringFromCLSID(stLinkAddressReplyData.guid, &bstrGuid);

                    g_sDisplayText += "Branch Guid: ";
                    g_sDisplayText += bstrGuid;
                    g_sDisplayText += "\r\n";

                    // ensure memory is freed
                    ::CoTaskMemFree(bstrGuid);

                }
                else
                {
                    // pExtInterface->GenerateGUID(pExtInterface, &stLinkAddressReplyData.guid);
                    // Caller has to write a GUID back in this case using REMOTE_DPCD_WRITE
                    g_sDisplayText += _T("Branch GUID = NULL\r\n");
                }
                g_sDisplayText += _T("Number of Ports: ");
                g_sDisplayText.AppendFormat(_T("%d\r\n"), stLinkAddressReplyData.ucPortNo);

                for (ucCount = 0; ucCount < stLinkAddressReplyData.ucPortNo; ucCount++)
                {
                    g_sDisplayText += _T("---------------------------------------------------------------------\r\n");
                    if (ucCount == 0)
                    {
                        // For First device info
                        // LINK_ADDRESS_REPLY_PORT_DETAILS_0 stLinkAddressPortDetails = {0};
                        ReadMessage(m_byBuffer, (PBYTE)&stLinkAddressPortDetails_0, ucOffset, sizeof(SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0));
                        ucOffset += sizeof(SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0);

                        if (stLinkAddressPortDetails_0.ucMsgCapStatus)
                        {
                            g_sDisplayText.AppendFormat(_T("Port: %d, "), stLinkAddressPortDetails_0.ucPortNumber);
                            if (stLinkAddressPortDetails_0.ucInputPort)
                                g_sDisplayText.AppendFormat(_T(" Input Port. "));
                            g_sDisplayText.AppendFormat(_T("Branch: bMSTCapStatus: %d,"), stLinkAddressPortDetails_0.ucMsgCapStatus);
                            g_sDisplayText.AppendFormat(_T(" PeerDeviceType: %d\r\n"), stLinkAddressPortDetails_0.ucPeerDeviceType);

                        }
                    }
                    else
                    {
                        //LINK_ADDRESS_REPLY_PORT_DETAILS stLinkAddressPortDetails = {0};
                        ReadMessage(m_byBuffer, (PBYTE)&stLinkAddressPortDetails, ucOffset, sizeof(SB_LINK_ADDRESS_REPLY_PORT_DETAILS));
                        ucOffset += sizeof(SB_LINK_ADDRESS_REPLY_PORT_DETAILS);
                        g_sDisplayText.AppendFormat(_T("port number: %d, "),
                                                    stLinkAddressPortDetails.ucPortNumber);
                        if (stLinkAddressPortDetails.ucMsgCapStatus)
                        {
                            g_sDisplayText.AppendFormat(_T("Branch: device type: %d, "), stLinkAddressPortDetails.ucPeerDeviceType);

                        }
                        else //if (stLinkAddressPortDetails.ucDPDevicePlugStatus)
                        {
                            g_sDisplayText.AppendFormat(_T("Leaf: device type: %d, "), stLinkAddressPortDetails.ucPeerDeviceType);
                        }
                        g_sDisplayText.AppendFormat(_T("DP dev plug %d, DPCDRev %#x, Legacy plug %d, Num SDP Str %d, Num SDP Str sink %d, "),
                                                    stLinkAddressPortDetails.ucDPDevicePlugStatus, stLinkAddressPortDetails.DPCDRev, stLinkAddressPortDetails.ucLegacyDevicePlugStatus,
                                                    stLinkAddressPortDetails.ucNumSDPStreams, stLinkAddressPortDetails.ucNumSDPStreamSinks);
                        if (stLinkAddressPortDetails.Peerguid.Data1 != 0)
                        {
                            // print GUID
                            OLECHAR* bstrGuid;
                            StringFromCLSID(stLinkAddressPortDetails.Peerguid, &bstrGuid);

                            g_sDisplayText += _T("Guid: ");
                            g_sDisplayText += bstrGuid;
                            g_sDisplayText += _T("\r\n");

                            // ensure memory is freed
                            ::CoTaskMemFree(bstrGuid);

                        }
                        else
                        {
                            // pExtInterface->GenerateGUID(pExtInterface, &stLinkAddressReplyData.guid);
                            // Caller has to write a GUID back in this case using REMOTE_DPCD_WRITE
                            g_sDisplayText += _T("GUID: {NULL}\r\n");
                        }
                    }
                }
            }

        }
        else if (stReplyData.ucRequestID == SB_REMOTE_I2C_READ)
        {
            // parse edid 
            BYTE byTempOut[256] = { 0 };
            ULONG size = 0;
            SB_REMOTE_I2C_READ_REPLY_ST stRemoteI2CReadReply = { 0 };
            BYTE m_byEdidBuf[128] = { 0 };

            ReadMessage(m_byBuffer, (PBYTE)&stRemoteI2CReadReply, ucOffset, sizeof(stRemoteI2CReadReply));
            ucOffset += sizeof(stRemoteI2CReadReply);

            if (stRemoteI2CReadReply.Number_Of_Bytes_Read) // non-zero bytes read.
            {
                // Copy the buffer into the input buffer.
                ReadMessage(m_byBuffer, m_byEdidBuf, ucOffset, stRemoteI2CReadReply.Number_Of_Bytes_Read);
            }

            g_sDisplayText += _T("\r\nRemote I2C data: \r\n");
            g_sDisplayText.AppendFormat(_T("Port number: %d \r\nEDID Buffer:\r\n"), stRemoteI2CReadReply.Port_Number);
            for (int i = 0; i < 128; i++)
            {
                g_sDisplayText.AppendFormat(_T("0x%02x "), m_byEdidBuf[i]);
            }
            g_sDisplayText += "\r\n";

        }
        else if (stReplyData.ucRequestID == SB_ENUM_PATH_RESOURCES)
        {
            SB_ENUM_PATH_RESOURCES_REPLY stEPRReplyData = { 0 };
            ReadMessage(m_byBuffer, (PBYTE)&stEPRReplyData, ucOffset, sizeof(stEPRReplyData));
            ucOffset += sizeof(stEPRReplyData);
            ULONG ulPBN;
            g_sDisplayText += _T("\r\nEnum Path Resorces\r\n");
            ulPBN = stEPRReplyData.Payload_Bandwidth_Full_Number7_0 | (stEPRReplyData.Payload_Bandwidth_Full_Number15_8 << 8);


            g_sDisplayText.AppendFormat(_T("Port number: %d \r\n"), stEPRReplyData.Port_Number);
            g_sDisplayText.AppendFormat(_T("Full PBN: %d\r\n"), ulPBN);

            ulPBN = stEPRReplyData.Payload_Bandwidth_Available_Number7_0 | (stEPRReplyData.Payload_Bandwidth_Available_Number15_8 << 8);
            g_sDisplayText.AppendFormat(_T("Available PBN: %d\r\n"), ulPBN);

        }
        else if (SB_ALLOCATE_PAYLOAD == stReplyData.ucRequestID)
        {
            ALLOC_PAYLOAD_REPLY stAllPLReply = { 0 };
            ReadMessage(m_byBuffer, (PBYTE)&stAllPLReply, ucOffset, sizeof(stAllPLReply));
            ucOffset += sizeof(stAllPLReply);
            ULONG ulPBN;
            g_sDisplayText += _T("\r\nAllocate Payload\r\n");
            g_sDisplayText.AppendFormat(_T("Port number: %d \r\n"), stAllPLReply.Port_Number);
            ulPBN = stAllPLReply.Payload_Bandwidth_Number7_0 | (stAllPLReply.Payload_Bandwidth_Number15_8 << 8);
            g_sDisplayText.AppendFormat(_T("Allocated PBN: %d\r\n"), ulPBN);
            g_sDisplayText.AppendFormat(_T("VC id: %d\r\n"), stAllPLReply.Virtual_Channel_Payload_Identifier);

        }
    }
    catch (...) {};

    m_editDisplay.SetWindowText(g_sDisplayText);
}



void CSidebandMsgParserDlg::OnBnClickedOk()
{
    SetInstructionText();
}


void CSidebandMsgParserDlg::OnBnClickedCancel()
{
    CDialogEx::OnCancel();
}

void CreateBranchRad(PRELATIVEADDRESS pRAD, CAtlString szRAD)
{
    int iNibbleCnt = 0, iStart = 0;
    CAtlString Token = _T("");
    Token = szRAD.Tokenize(_T("."), iStart);
    if (_T("0") == Token)
        Token = szRAD.Tokenize(_T("."), iStart);

    while (_T("") != Token)
    {
        iNibbleCnt++;
        if (iNibbleCnt % 2 == 0) //even
            pRAD->ucAddress[(iNibbleCnt - 1) / 2] |= _wtoi(Token.GetBuffer());
        else
            pRAD->ucAddress[(iNibbleCnt - 1) / 2] |= _wtoi(Token.GetBuffer()) << 4;

        Token.ReleaseBuffer();
        Token = szRAD.Tokenize(_T("."), iStart);
    }
    pRAD->ucTotalLinkCount = iNibbleCnt + 1;
}

void CSidebandMsgParserDlg::OnBnClickedBtnLinkAdd()
{
    CString sTemp;
    SIDEBAND_MSG_HEADER HDR = { 0 };
    PBYTE pSrc = NULL, pDst = NULL;
    UINT uSz = 0;
    UINT uSrcOffset = 0, uDstOffset = 0;
    UCHAR ucDataCRC = 0;
    UCHAR ucBodySz = 0;
    UCHAR ucMsgLength = 0, ucBodyLength = 0, ucHeaderLength = 0;
    RELATIVEADDRESS RelativeAddress = { 0 };
    PBYTE pHeaderBuffer = NULL;
    SB_REQ_ID_TYPE RequestID = SB_LINK_ADDRESS;
    UCHAR ucCount = 0;
    SB_LINK_ADDRESS_REPLY_DATA stLinkAddressReplyData = { 0 };
    SB_LINK_ADDRESS_REPLY_PORT_DETAILS_0 stLinkAddressPortDetails_0 = { 0 };
    SB_LINK_ADDRESS_REPLY_PORT_DETAILS stLinkAddressPortDetails = { 0 };

    CString sLADIn;
    m_EditInput.GetWindowText(sLADIn.GetBuffer(MAX_MSG_BYTES * 5), MAX_MSG_BYTES * 5);
    CAtlString sRad, sPorts, sLeafBranch, Token;
    int iStart = 0;
    UCHAR ucPortNos[16] = { 0 };
    BOOL bBranch[16] = { 0 };
    REPLY_DATA stReplyData = { 0 };
    g_sDisplayText = _T("");

    sLADIn.ReleaseBuffer();

    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;
    try
    {
        //CAtlString sIn = sLADIn.GetBuffer();
        //sLADIn.ReleaseBuffer();//

        sRad = sLADIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong RAD";
            throw("");
        }

        sLeafBranch = sLADIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong Leaf/Branch info";
            throw("");
        }
        sPorts = sLADIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong ports";
            throw("");
        }

        // Create branch RAD
        CreateBranchRad(&RelativeAddress, sRad);
        iStart = 0;
        ucCount = 0;
        Token = _T("");
        Token = sPorts.Tokenize(_T(","), iStart);
        while (_T("") != Token)
        {
            ucPortNos[ucCount++] = _wtoi(Token.GetBuffer());
            Token.ReleaseBuffer();
            Token = sPorts.Tokenize(_T(","), iStart);
        }

        iStart = 0;
        ucCount = 0;
        Token = _T("");
        Token = sLeafBranch.Tokenize(_T(","), iStart);
        while (_T("") != Token)
        {
            bBranch[ucCount++] = (_T("B") == Token);
            Token = sLeafBranch.Tokenize(_T(","), iStart);
        }


        stReplyData.ucRequestID = RequestID;
        pDst = m_byBuffer;
        memcpy((PBYTE)(pDst + uDstOffset), (PBYTE)&stReplyData, sizeof(stReplyData));
        uDstOffset += sizeof(stReplyData);

        CoCreateGuid(&stLinkAddressReplyData.guid);
        stLinkAddressReplyData.ucPortNo = ucCount + 1;

        memcpy((PBYTE)(pDst + uDstOffset), (PBYTE)&stLinkAddressReplyData, sizeof(stLinkAddressReplyData));
        uDstOffset += sizeof(stLinkAddressReplyData);

        stLinkAddressPortDetails_0.ucPeerDeviceType = 1;
        stLinkAddressPortDetails_0.ucInputPort = 1;
        stLinkAddressPortDetails_0.ucMsgCapStatus = 1;
        stLinkAddressPortDetails_0.ucDPDevicePlugStatus = 1;
        stLinkAddressPortDetails_0.ucPortNumber = 0;

        memcpy((PBYTE)(pDst + uDstOffset), (PBYTE)&stLinkAddressPortDetails_0, sizeof(stLinkAddressPortDetails_0));
        uDstOffset += sizeof(stLinkAddressPortDetails_0);
        int i;
        BOOL bHasBranch = FALSE;
        for (i = 0; i < ucCount; i++)
        {
            bHasBranch = bBranch[i];
            CoCreateGuid(&stLinkAddressPortDetails.Peerguid);
            stLinkAddressPortDetails.ucPortNumber = ucPortNos[i];

            if (bHasBranch)// && (i == sizeof(ucPortNos) - 1))
            {
                stLinkAddressPortDetails.ucPeerDeviceType = eMSTBranchDevice;
                stLinkAddressPortDetails.ucInputPort = 0;
                stLinkAddressPortDetails.ucMsgCapStatus = 1;
                stLinkAddressPortDetails.DPCDRev = 18;
                stLinkAddressPortDetails.ucNumSDPStreamSinks = 0;
                stLinkAddressPortDetails.ucNumSDPStreams = 0;
            }
            else
            {
                stLinkAddressPortDetails.ucPeerDeviceType = eSSTSinkorStreamSink;
                stLinkAddressPortDetails.ucInputPort = 0;
                stLinkAddressPortDetails.ucLegacyDevicePlugStatus = 0;
                stLinkAddressPortDetails.ucDPDevicePlugStatus = 1;
                stLinkAddressPortDetails.ucMsgCapStatus = 0;
                stLinkAddressPortDetails.DPCDRev = 18;
                stLinkAddressPortDetails.ucNumSDPStreamSinks = 2;
                stLinkAddressPortDetails.ucNumSDPStreams = 1;
            }
            memcpy((PBYTE)(pDst + uDstOffset), (PBYTE)&stLinkAddressPortDetails, sizeof(stLinkAddressPortDetails));
            uDstOffset += sizeof(stLinkAddressPortDetails);
        }
        // create packets
        PBYTE pMsgBuffer = NULL;
        ULONG ulFinalBufSize = 0;
        pMsgBuffer = CreateMessagePackets(&RelativeAddress, m_byBuffer, uDstOffset, &ulFinalBufSize);

        //g_sDisplayText += _T("Link Address Sideband Down Reply Msg Bytes: \r\n\r\n");
        for (UINT i = 0; i < ulFinalBufSize; i++)
        {
            sTemp.Format(_T("0x%02x "), pMsgBuffer[i]);
            g_sDisplayText += sTemp;
        }
        g_sDisplayText += "\r\n";

        if (pMsgBuffer)
        {
            free(pMsgBuffer);
            pMsgBuffer = NULL;
        }
    }
    catch (...) {}
    m_editDisplay.SetWindowText(_T("Link Address Sideband Down Reply Msg Bytes: \r\n\r\n") + g_sDisplayText);


}


void CSidebandMsgParserDlg::OnBnClickedBtnRemoteEdid()
{

    // create edid reply:
    SIDEBAND_MSG_HEADER HDR = { 0 };
    ULONG size = 0;
    SB_REMOTE_I2C_READ_REPLY_ST stRemoteI2CReadReply = { 0 };
    DWORD edidSize = 128;
    SB_REQ_ID_TYPE RequestID = SB_REMOTE_I2C_READ;
    REPLY_DATA stReplyData = { 0 };
    UCHAR ucDataCRC = 0;
    RELATIVEADDRESS RelativeAddress = { 0 };
    CString sInput;
    m_EditInput.GetWindowText(sInput.GetBuffer(MAX_MSG_BYTES * 5), MAX_MSG_BYTES * 5);
    CAtlString sRad, sEDID;
    int iStart = 0;

    sInput.ReleaseBuffer();
    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;

    g_sDisplayText = _T("");

    try
    {
        sRad = sInput.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong RAD";
            throw("");
        }
        sEDID = sInput.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong EDID";
            throw("");
        }

        // Create branch RAD
        CreateBranchRad(&RelativeAddress, sRad);

       // parse edid
        ConvertStringToHex(sEDID.GetBuffer(), g_EDID, &edidSize);//m_byEdidBuf
        sEDID.ReleaseBuffer();



        stReplyData.ucRequestID = RequestID;
        memcpy(m_byBuffer, &stReplyData, 1);
        size += 1;

        stRemoteI2CReadReply.Port_Number = GET_PORT_NUMBER(RelativeAddress);
        RelativeAddress.ucTotalLinkCount > 0 ? RelativeAddress.ucTotalLinkCount-- : RelativeAddress.ucTotalLinkCount;

        stRemoteI2CReadReply.Number_Of_Bytes_Read = 128;
        memcpy(m_byBuffer + size, (PBYTE)&stRemoteI2CReadReply, sizeof(stRemoteI2CReadReply));
        size += sizeof(stRemoteI2CReadReply);
        memcpy(m_byBuffer + size, g_EDID, 128);
        size += 128;

        // create packets
        PBYTE pMsgBuffer = NULL;
        ULONG ulFinalBufSize = 0;
        pMsgBuffer = CreateMessagePackets(&RelativeAddress, m_byBuffer, size, &ulFinalBufSize);

        for (UINT i = 0; i < ulFinalBufSize; i++)
        {
            g_sDisplayText.AppendFormat(_T("0x%02x "), pMsgBuffer[i]);
        }
        g_sDisplayText += "\r\n";

        if (pMsgBuffer)
        {
            free(pMsgBuffer);
            pMsgBuffer = NULL;
        }

       // OnBnClickedButtonCopy();// temp code as app crashes
    }
    catch (...) {}
    m_editDisplay.SetWindowText(_T("Remote I2C read Sideband Down Reply Msg Bytes: \r\n\r\n") + g_sDisplayText);
}

// EPR reply buffer
void CSidebandMsgParserDlg::OnBnClickedBtnEpr()
{
    REPLY_DATA stReplyData = { 0 };
    SB_ENUM_PATH_RESOURCES_REPLY stEPRReplyData = { 0 };
    RELATIVEADDRESS RelativeAddress = { 0 };
    CString sLADIn;
    m_EditInput.GetWindowText(sLADIn.GetBuffer(MAX_MSG_BYTES * 5), MAX_MSG_BYTES * 5);
    CAtlString sRad, PBN, Token;
    int iStart = 0;
    USHORT usPBNFull = 0, usPBNavl = 0;
    sLADIn.ReleaseBuffer();

    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;
    g_sDisplayText = _T("");
    try
    {
        // Create EPR reply:
        ULONG size = 0;
        //UCHAR ucPort = 0;
        CAtlString sIn = sLADIn.GetBuffer();
        sLADIn.ReleaseBuffer();//
        sRad = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong RAD";
            throw("");
        }

        PBN = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong PBN";
            throw("");
        }
        iStart = 0;
        Token = PBN.Tokenize(_T(","), iStart);
        if (Token != _T(""))
        {
            usPBNFull = _wtoi(Token.GetBuffer());
            Token.ReleaseBuffer();//
            Token = PBN.Tokenize(_T(","), iStart);
            if (Token != _T(""))
            {
                usPBNavl = _wtoi(Token.GetBuffer());
                Token.ReleaseBuffer();//
            }
        }

        // Create branch RAD
        CreateBranchRad(&RelativeAddress, sRad);

        stReplyData.ucRequestID = SB_ENUM_PATH_RESOURCES;
        memcpy(m_byBuffer, &stReplyData, 1);
        size += 1;

        stEPRReplyData.Port_Number = GET_PORT_NUMBER(RelativeAddress);
        RelativeAddress.ucTotalLinkCount > 0 ? RelativeAddress.ucTotalLinkCount-- : RelativeAddress.ucTotalLinkCount;
        stEPRReplyData.Payload_Bandwidth_Full_Number7_0 = usPBNFull & 0xFF;
        stEPRReplyData.Payload_Bandwidth_Full_Number15_8 = (usPBNFull & 0xFF00) >> 8;
        stEPRReplyData.Payload_Bandwidth_Available_Number7_0 = usPBNavl & 0xFF;
        stEPRReplyData.Payload_Bandwidth_Available_Number15_8 = (usPBNavl & 0xFF00) >> 8;

        memcpy(m_byBuffer + size, (PBYTE)&stEPRReplyData, sizeof(stEPRReplyData));
        size += sizeof(stEPRReplyData);


        // create packets
        PBYTE pMsgBuffer = NULL;
        ULONG ulFinalBufSize = 0;
        pMsgBuffer = CreateMessagePackets(&RelativeAddress, m_byBuffer, size, &ulFinalBufSize);

        //g_sDisplayText = _T("");
        for (UINT i = 0; i < ulFinalBufSize; i++)
        {
            g_sDisplayText.AppendFormat(_T("0x%02x "), pMsgBuffer[i]);
        }
        g_sDisplayText += "\r\n";

        if (pMsgBuffer)
        {
            free(pMsgBuffer);
            pMsgBuffer = NULL;
        }
    }
    catch (...) {}

    m_editDisplay.SetWindowText(_T("Enum Path Resource Sideband Down Reply Msg Bytes: \r\n\r\n") + g_sDisplayText);
}


void CSidebandMsgParserDlg::OnEnSetfocusEdit1()
{
    if (m_bInit)
    {
        // clear input box
        m_EditInput.SetWindowText(_T(""));
        m_bInit = false;
    }
}

// Alloc payload reply buffer 
void CSidebandMsgParserDlg::OnBnClickedAllocPayLoad()
{
    REPLY_DATA stReplyData = { 0 };
    ALLOC_PAYLOAD_REPLY stAPLReplyData = { 0 };
    RELATIVEADDRESS RelativeAddress = { 0 };
    CString sInput;
    m_EditInput.GetWindowText(sInput.GetBuffer(MAX_MSG_BYTES * 5), MAX_MSG_BYTES * 5);
    CAtlString sRad, PBN, vcId;
    int iStart = 0;
    USHORT usPBNFull = 0;

    sInput.ReleaseBuffer();//
    // init window text
    //m_editDisplay.SetWindowText(_T(""));
    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;
    g_sDisplayText = _T("");
    try
    {
        // Create EPR reply:
        ULONG size = 0;

        CAtlString sIn = sInput.GetBuffer();
        sInput.ReleaseBuffer();//
        sRad = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong RAD";
            throw("");
        }

        PBN = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong PBN";
            throw("");
        }
        vcId = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "wrong VC ID";
            throw("");
        }

        // Create branch RAD
        CreateBranchRad(&RelativeAddress, sRad);

        stReplyData.ucRequestID = SB_ALLOCATE_PAYLOAD;
        memcpy(m_byBuffer, &stReplyData, 1);
        size += 1;

        usPBNFull = _wtoi(PBN.GetBuffer());
        PBN.ReleaseBuffer();//

        stAPLReplyData.Port_Number = GET_PORT_NUMBER(RelativeAddress);
        RelativeAddress.ucTotalLinkCount > 0 ? RelativeAddress.ucTotalLinkCount-- : RelativeAddress.ucTotalLinkCount;
        stAPLReplyData.Payload_Bandwidth_Number7_0 = usPBNFull & 0xFF;
        stAPLReplyData.Payload_Bandwidth_Number15_8 = (usPBNFull & 0xFF00) >> 8;
        stAPLReplyData.Virtual_Channel_Payload_Identifier = _wtoi(vcId.GetBuffer());
        vcId.ReleaseBuffer();//

        memcpy(m_byBuffer + size, (PBYTE)&stAPLReplyData, sizeof(stAPLReplyData));
        size += sizeof(stAPLReplyData);


        // create packets
        PBYTE pMsgBuffer = NULL;
        ULONG ulFinalBufSize = 0;
        pMsgBuffer = CreateMessagePackets(&RelativeAddress, m_byBuffer, size, &ulFinalBufSize);

        //g_sDisplayText = _T("");// _T("Allocate Payload Sideband Down Reply Msg Bytes: \r\n\r\n");
        for (UINT i = 0; i < ulFinalBufSize; i++)
        {
            g_sDisplayText.AppendFormat(_T("0x%02x "), pMsgBuffer[i]);
        }
        g_sDisplayText += "\r\n";

        if (pMsgBuffer)
        {
            free(pMsgBuffer);
            pMsgBuffer = NULL;
        }
    }
    catch (...) {}

    m_editDisplay.SetWindowText(_T("Allocate Payload Sideband Down Reply Msg Bytes: \r\n\r\n") + g_sDisplayText);
}

// test func
void CSidebandMsgParserDlg::OnBnClickedButton6()
{
    // Use for runtime packet data fillup test data
    REPLY_DATA stReplyData = { 0 };
    RELATIVEADDRESS RelativeAddress = { 0 };
    CString sInput;
    m_EditInput.GetWindowText(sInput.GetBuffer(MAX_MSG_BYTES * 5), MAX_MSG_BYTES * 5);
    CAtlString sRad, PBN, vcId;
    int iStart = 0;

    sInput.ReleaseBuffer();
    // init window text
    //m_editDisplay.SetWindowText(_T(""));
    memset(m_byBuffer, 0, sizeof(m_byBuffer));
    m_dwBuffLen = 0;
    g_sDisplayText = "";
    try
    {
        // Create EPR reply:
        ULONG size = 0;

        CAtlString sIn = sInput.GetBuffer();
        sInput.ReleaseBuffer();
        sRad = sIn.Tokenize(_T("{}"), iStart);
        if (iStart == -1)
        {
            g_sDisplayText += "Wrong RAD";
            throw("");
        }



        // Create branch RAD
        CreateBranchRad(&RelativeAddress, sRad);

        stReplyData.ucRequestID = SB_CLEAR_PAYLOAD_ID_TABLE;
        memcpy(m_byBuffer, &stReplyData, 1);
        size += 1;




        // create packets
        PBYTE pMsgBuffer = NULL;
        ULONG ulFinalBufSize = 0;
        pMsgBuffer = CreateMessagePackets(&RelativeAddress, m_byBuffer, size, &ulFinalBufSize);

        //g_sDisplayText = _T("");// _T("Custom Sideband Down Reply Msg Bytes: \r\n\r\n");
        for (UINT i = 0; i < ulFinalBufSize; i++)
        {
            g_sDisplayText.AppendFormat(_T("0x%02x "), pMsgBuffer[i]);
        }
        g_sDisplayText += "\r\n";

        if (pMsgBuffer)
        {
            free(pMsgBuffer);
            pMsgBuffer = NULL;
        }
    }
    catch (...) {}

    m_editDisplay.SetWindowText(_T("Custom Sideband Down Reply Msg Bytes: \r\n\r\n") + g_sDisplayText);
}



void CSidebandMsgParserDlg::OnBnClickedButtonCopy()
{
    HGLOBAL h;
    LPTSTR arr;

    h = GlobalAlloc(GMEM_MOVEABLE, sizeof(TCHAR)*(g_sDisplayText.GetLength() + 1));
    arr = (LPTSTR)GlobalLock(h);
    wcscpy_s((TCHAR*)arr, g_sDisplayText.GetLength() + 1, g_sDisplayText.GetBuffer());

    GlobalUnlock(h);

    ::OpenClipboard(NULL);
    EmptyClipboard();
    SetClipboardData(CF_UNICODETEXT, h);
    CloseClipboard();
    g_sDisplayText.ReleaseBuffer();
}

void CSidebandMsgParserDlg::GetClipBoardData()
{
    if (OpenClipboard())
    {
        HANDLE hClipboardData = GetClipboardData(CF_UNICODETEXT);

        TCHAR *pData = (TCHAR*)GlobalLock(hClipboardData);

        CString strFromClipboard = pData;
        m_EditInput.SetWindowText(strFromClipboard);

        // Unlock the global memory.
        GlobalUnlock(hClipboardData);

        CloseClipboard();
    }

}

void CSidebandMsgParserDlg::OnBnClickedButtonPaste()
{
    GetClipBoardData();
}
