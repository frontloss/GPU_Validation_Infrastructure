###############################################################################
#Test Name           : MPO_Media_Youtube_SnapMode
#Test Author         : IMAHENDR
#Test Owner          : IMAHENDR
#Test Revision       : 2
#Revision History    :
#[1:IMAHENDR] - Script created
#[2:IMAHENDR] - Added verification, flow changes 4/4/16
#Description         : Test to check for flicker/corruption during resize of 
#2 YUY2 planes in Snapmode 
#HSD Bugs:           :
#Test Effectiveness  :
#TAGS                : RESIZE;WM;DBUF;2PLANES;SNAP
#Platform            : SKL; KBL 
###############################################################################

import sys
import clr
import time
sys.path.append(r"c:\Program Files (x86)\ironPython 2.7\lib")
import os
from System.Collections.Generic import *

parentPath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
refPath = os.path.join(parentPath, "PythonHelper")
sys.path.append(parentPath)
sys.path.append(refPath)
clr.AddReference(r"Intel.VPG.Display.Automation.Logger.dll")
from Intel.VPG.Display.Automation import *
from PyTestBase import *
Log.Init("MPO_Media_Youtube_SnapMode", 5, True, True,  True, True)
Obj = PyTestBase()
clr.AddReference(r"DivaUtilityCLR.dll")  # path of dll
clr.AddReference(r"PythonExecute.dll")
clr.AddReference(r"FlipsInterface.dll")  # path of dll
import DIVA_M_RECT_CLR, DIVA_SURFACE_TILEFORMAT_CLR, DIVA_PIXELFORMAT_CLR,DIVA_SETVIDPNSRCADDR_FLAGS_CLR
from Intel.VPG.Display.FlipsInterface import *
from Intel.VPG.Display.FlipsInterface.MPO import *
from Intel.VPG.Display.FlipsInterface.Iterators import *

expectedValue= clr.Reference[int]();

PixelFormatOffset = clr.Reference[int]();
PixelFormatBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PIXEL_FORMAT_PLANE1", "EDP",  PixelFormatOffset, PixelFormatBitmap, expectedValue); 

TiledSurfaceOffset = clr.Reference[int]();
TiledSurfaceBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("TILED_SURFACE_PLANE1", "EDP",  TiledSurfaceOffset, TiledSurfaceBitmap, expectedValue); 

ScalerOffset = clr.Reference[int]();
ScalerBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("ENABLE_SCALER_SCALER1", "EDP",  ScalerOffset, ScalerBitmap, expectedValue); 

ScalerWinXPosOffset = clr.Reference[int]();
ScalerWinXPosBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PS_WIN_XPOS_SCALER1", "EDP",  ScalerWinXPosOffset, ScalerWinXPosBitmap, expectedValue); 

ScalerWinYPosOffset = clr.Reference[int]();
ScalerWinYPosBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PS_WIN_YPOS_SCALER1", "EDP",  ScalerWinYPosOffset, ScalerWinYPosBitmap, expectedValue); 

ScalerWinXSZOffset = clr.Reference[int]();
ScalerWinXSZBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PS_WIN_XSZ_SCALER1", "EDP",  ScalerWinXSZOffset, ScalerWinXSZBitmap, expectedValue); 

ScalerWinYSZOffset = clr.Reference[int]();
ScalerWinYSZBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PS_WIN_YSZ_SCALER1", "EDP",  ScalerWinYSZOffset, ScalerWinYSZBitmap, expectedValue); 

PlaneXPOSOffset = clr.Reference[int]();
PlaneXPOSBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PLANE_XPOS_PLANE1", "EDP",  PlaneXPOSOffset, PlaneXPOSBitmap, expectedValue); 

PlaneYPOSOffset = clr.Reference[int]();
PlaneYPOSBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PLANE_YPOS_PLANE1", "EDP",  PlaneYPOSOffset, PlaneYPOSBitmap, expectedValue); 

PlaneXSizeOffset = clr.Reference[int]();
PlaneXSizeBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PLANE_SIZE_WIDTH_PLANE1", "EDP",  PlaneXSizeOffset, PlaneXSizeBitmap, expectedValue); 

PlaneYSizeOffset = clr.Reference[int]();
PlaneYSizeBitmap = clr.Reference[int]();
Obj.GetEventRegisterInfo("PLANE_SIZE_HEIGHT_PLANE1", "EDP",  PlaneYSizeOffset, PlaneYSizeBitmap, expectedValue); 

#Diva Interface Initialization 
divaHandler = DivaInterface(0, ConfigItem.EdpMonitor_ID())
divaHandler.EnableDFT()

viewPort  = Dim()           #TODO Add GetCurrentMode Implementation from FW
viewPort.Width = ConfigItem.CurrentMode.Width
viewPort.Height = ConfigItem.CurrentMode.Height

Plane1_Rect = DIVA_M_RECT_CLR()
DIVA_M_RECT_CLR.Left.SetValue(Plane1_Rect, 0)
DIVA_M_RECT_CLR.Top.SetValue(Plane1_Rect, 0)
DIVA_M_RECT_CLR.Right.SetValue(Plane1_Rect, viewPort.Width/2 - 1)
DIVA_M_RECT_CLR.Bottom.SetValue(Plane1_Rect, viewPort.Height)

Plane2_Rect = DIVA_M_RECT_CLR()
DIVA_M_RECT_CLR.Left.SetValue(Plane2_Rect, viewPort.Width/2)
DIVA_M_RECT_CLR.Top.SetValue(Plane2_Rect, 0)
DIVA_M_RECT_CLR.Right.SetValue(Plane2_Rect, viewPort.Width)
DIVA_M_RECT_CLR.Bottom.SetValue(Plane2_Rect, viewPort.Height)

Plane3_Rect = DIVA_M_RECT_CLR()
DIVA_M_RECT_CLR.Left.SetValue(Plane3_Rect, 0)
DIVA_M_RECT_CLR.Top.SetValue(Plane3_Rect, viewPort.Height - 100)
DIVA_M_RECT_CLR.Right.SetValue(Plane3_Rect, viewPort.Width)
DIVA_M_RECT_CLR.Bottom.SetValue(Plane3_Rect, viewPort.Height)

PLANE1 = MPOPlane(Plane1_Rect.Right - Plane1_Rect.Left,Plane1_Rect.Bottom - Plane1_Rect.Top, DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_YUV422, DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y, 2)
PLANE2 = MPOPlane(Plane2_Rect.Right - Plane2_Rect.Left,Plane2_Rect.Bottom - Plane2_Rect.Top, DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_YUV422, DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y, 1)
PLANE3 = MPOPlane(Plane3_Rect.Right - Plane3_Rect.Left,Plane3_Rect.Bottom - Plane3_Rect.Top, DIVA_PIXELFORMAT_CLR.DIVA_PIXEL_FORMAT_B8G8R8A8, DIVA_SURFACE_TILEFORMAT_CLR.DIVA_SURFACE_TILEFORMAT_Y, 0)

PLANES = List[MPOPlane]()
PLANES.Add(PLANE1)
PLANES.Add(PLANE2)
PLANES.Add(PLANE3)
PLANE1.Allocate()
PLANE2.Allocate()
PLANE3.Allocate()

try:
    Plane1_ResizeIterator = GenericRectResizeIterator(Plane1_Rect, viewPort)
    for index in range(0, 3):
        while(Plane1_ResizeIterator.Resize("RIGHT", 3)):
            PLANES[0].Attributes.MPODstRect = Plane1_ResizeIterator.CurrentRect
            PLANES[0].Attributes.MPOClipRect = Plane1_ResizeIterator.CurrentRect
            PLANES[1].Attributes.MPODstRect.Left = Plane1_ResizeIterator.CurrentRect.Right
            PLANES[1].Attributes.MPOClipRect.Left = Plane1_ResizeIterator.CurrentRect.Right

            Status = divaHandler.CheckMPO(PLANES)

            if(Status == True):
                divaHandler.SetSrcAddressMPO(PLANES,  DIVA_SETVIDPNSRCADDR_FLAGS_CLR.DIVA_SETVIDPNSRCADDR_FLAG_FLIPIMMEDIATE)
                #Verification      
                PixelFormat = divaHandler.ReadRegister(PixelFormatOffset.Value)
                if PixelFormat & PixelFormatBitmap.Value != 0x00000000: #YUY2
                    Log.Fail("Register Verification failed, PixelFormat:{0}", PixelFormat)
                    Obj.FailCount += 1
                TileFormat = divaHandler.ReadRegister(TiledSurfaceOffset.Value)
                if TileFormat & TiledSurfaceBitmap.Value != 0x00001000: #Y-Tile
                    Log.Fail("Register Verification failed, TileFormat:{0}", TileFormat)
                    Obj.FailCount += 1
                Scaler = divaHandler.ReadRegister(ScalerOffset.Value)
                if Scaler & ScalerBitmap.Value == 0x80000000:
                    #Plane scaler position
                    ScalerWindowXPos = divaHandler.ReadRegister(ScalerWinXPosOffset.Value)
                    if (ScalerWindowXPos & ScalerWinXPosBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Left:
                        Log.Fail("Register Verification failed, Scaler_WIN_XPOS.Expected:{0} Scaler_WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXPos)
                        Obj.FailCount += 1
                    ScalerWindowYPos = divaHandler.ReadRegister(ScalerWinYPosOffset.Value)
                    if ScalerWindowYPos & ScalerWinYPosBitmap.Value != PLANES[0].Attributes.MPODstRect.Top:
                        Log.Fail("Register Verification failed, Scaler_WIN_YPOS.Expected:{0} Scaler_WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYPos)
                        Obj.FailCount += 1
                    #Plane Scaler Size
                    ScalerWindowXSize = divaHandler.ReadRegister(ScalerWinXSZOffset.Value)
                    if (ScalerWindowXSize & ScalerWinXSZBitmap.Value) >> 16 != (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left):
                        Log.Fail("Register Verification failed, Scaler_WIN_XSIZE.Expected {0} Scaler_WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXSize)
                        Obj.FailCount += 1
                    ScalerWindowYSize = divaHandler.ReadRegister(ScalerWinYSZOffset.Value)
                    if ScalerWindowYSize & ScalerWinYSZBitmap.Value != (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top):
                        Log.Fail("Register Verification failed, Scaler_WIN_YSIZE.Expected {0} Scaler_WIN_YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYSize)
                        Obj.FailCount += 1
                #else:
                #    #Plane position
                #    #WindowXPos = divaHandler.ReadRegister(PlaneXPOSOffset.Value)
                #    #if WindowXPos & PlaneXPOSBitmap.Value != PLANES[0].Attributes.MPODstRect.Left:
                #    #    Log.Fail("Register Verification failed, WIN_XPOS.Expected:{0} WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, WindowXPos)
                #    #    Obj.FailCount += 1
                #    #WindowYPos = divaHandler.ReadRegister(PlaneYPOSOffset.Value)
                #    #if (WindowYPos & PlaneYPOSBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Top:
                #    #    Log.Fail("Register Verification failed, WIN_YPOS.Expected:{0} WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, WindowYPos)
                #    #    Obj.FailCount += 1
                #    #Plane Scaler Size
                #    WindowXSize = divaHandler.ReadRegister(PlaneXSizeOffset.Value)
                #    if WindowXSize& PlaneXSizeBitmap.Value <= (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1) and WindowXSize & PlaneXSizeBitmap.Value > (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1 - 3):
                #        Log.Fail("Register Verification failed, WIN_XSIZE.Expected {0} WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, WindowXSize)
                #        Obj.FailCount += 1
                #    WindowYSize = divaHandler.ReadRegister(PlaneYSizeOffset.Value)
                #    if (WindowYSize & PlaneYSizeBitmap.Value) >> 16 <= (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1) and (WindowYSize & PlaneYSizeBitmap.Value) >> 16 > (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1 - 3):
                #        Log.Fail("Register Verification failed, YSIZE.Expected {0} YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, WindowYSize)
                #        Obj.FailCount += 1
                if divaHandler.CheckUnderRun():
                    Log.Fail("Underrun Seen")
                    Obj.FailCount += 1
                ##Verfiy Watermark and DBUF implementation remaining.
            else:
                #TODO: Fallback mechanism to be implemented
                print "CheckMPO Failed"

        while(Plane1_ResizeIterator.Resize("LEFT", 3)):
            PLANES[0].Attributes.MPODstRect = Plane1_ResizeIterator.CurrentRect
            PLANES[0].Attributes.MPOClipRect = Plane1_ResizeIterator.CurrentRect
            PLANES[1].Attributes.MPODstRect.Left = Plane1_ResizeIterator.CurrentRect.Right
            PLANES[1].Attributes.MPOClipRect.Left = Plane1_ResizeIterator.CurrentRect.Right

            Status = divaHandler.CheckMPO(PLANES)

            if(Status == True):
                divaHandler.SetSrcAddressMPO(PLANES,  DIVA_SETVIDPNSRCADDR_FLAGS_CLR.DIVA_SETVIDPNSRCADDR_FLAG_FLIPIMMEDIATE)
                #Verification      
                PixelFormat = divaHandler.ReadRegister(PixelFormatOffset.Value)
                if PixelFormat & PixelFormatBitmap.Value != 0x00000000: #YUY2
                    Log.Fail("Register Verification failed, PixelFormat:{0}", PixelFormat)
                    Obj.FailCount += 1
                TileFormat = divaHandler.ReadRegister(TiledSurfaceOffset.Value)
                if TileFormat & TiledSurfaceBitmap.Value != 0x00001000: #Y-Tile
                    Log.Fail("Register Verification failed, TileFormat:{0}", TileFormat)
                    Obj.FailCount += 1
                Scaler = divaHandler.ReadRegister(ScalerOffset.Value)
                if Scaler & ScalerBitmap.Value == 0x80000000:
                    #Plane scaler position
                    ScalerWindowXPos = divaHandler.ReadRegister(ScalerWinXPosOffset.Value)
                    if (ScalerWindowXPos & ScalerWinXPosBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Left:
                        Log.Fail("Register Verification failed, Scaler_WIN_XPOS.Expected:{0} Scaler_WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXPos)
                        Obj.FailCount += 1
                    ScalerWindowYPos = divaHandler.ReadRegister(ScalerWinYPosOffset.Value)
                    if ScalerWindowYPos & ScalerWinYPosBitmap.Value != PLANES[0].Attributes.MPODstRect.Top:
                        Log.Fail("Register Verification failed, Scaler_WIN_YPOS.Expected:{0} Scaler_WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYPos)
                        Obj.FailCount += 1
                    #Plane Scaler Size
                    ScalerWindowXSize = divaHandler.ReadRegister(ScalerWinXSZOffset.Value)
                    if (ScalerWindowXSize & ScalerWinXSZBitmap.Value) >> 16 != (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left):
                        Log.Fail("Register Verification failed, Scaler_WIN_XSIZE.Expected {0} Scaler_WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXSize)
                        Obj.FailCount += 1
                    ScalerWindowYSize = divaHandler.ReadRegister(ScalerWinYSZOffset.Value)
                    if ScalerWindowYSize & ScalerWinYSZBitmap.Value != (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top):
                        Log.Fail("Register Verification failed, Scaler_WIN_YSIZE.Expected {0} Scaler_WIN_YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYSize)
                        Obj.FailCount += 1
                #else:
                #    #Plane position
                #    #WindowXPos = divaHandler.ReadRegister(PlaneXPOSOffset.Value)
                #    #if WindowXPos & PlaneXPOSBitmap.Value != PLANES[0].Attributes.MPODstRect.Left:
                #    #    Log.Fail("Register Verification failed, WIN_XPOS.Expected:{0} WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, WindowXPos)
                #    #    Obj.FailCount += 1
                #    #WindowYPos = divaHandler.ReadRegister(PlaneYPOSOffset.Value)
                #    #if (WindowYPos & PlaneYPOSBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Top:
                #    #    Log.Fail("Register Verification failed, WIN_YPOS.Expected:{0} WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, WindowYPos)
                #    #    Obj.FailCount += 1
                #    #Plane Scaler Size
                #    WindowXSize = divaHandler.ReadRegister(PlaneXSizeOffset.Value)
                #    if WindowXSize& PlaneXSizeBitmap.Value <= (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1) and WindowXSize & PlaneXSizeBitmap.Value > (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1 - 3):
                #        Log.Fail("Register Verification failed, WIN_XSIZE.Expected {0} WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, WindowXSize)
                #        Obj.FailCount += 1
                #    WindowYSize = divaHandler.ReadRegister(PlaneYSizeOffset.Value)
                #    if (WindowYSize & PlaneYSizeBitmap.Value) >> 16 <= (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1) and (WindowYSize & PlaneYSizeBitmap.Value) >> 16 > (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1 - 3):
                #        Log.Fail("Register Verification failed, YSIZE.Expected {0} YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, WindowYSize)
                #        Obj.FailCount += 1
                if divaHandler.CheckUnderRun():
                    Log.Fail("Underrun Seen")
                    Obj.FailCount += 1
                ##Verfiy Watermark and DBUF implementation remaining.
            else:
                #TODO: Fallback mechanism to be implemented
                print "CheckMPO Failed"

    for index in range(0, 3):
        while(Plane1_ResizeIterator.Resize("RIGHT", 3)):
            PLANES[0].Attributes.MPODstRect = Plane1_ResizeIterator.CurrentRect
            PLANES[0].Attributes.MPOClipRect = Plane1_ResizeIterator.CurrentRect
            PLANES[1].Attributes.MPODstRect.Left = Plane1_ResizeIterator.CurrentRect.Right
            PLANES[1].Attributes.MPOClipRect.Left = Plane1_ResizeIterator.CurrentRect.Right

            Status = divaHandler.CheckMPO(PLANES)

            if(Status == True):
                divaHandler.SetSrcAddressMPO(PLANES,  DIVA_SETVIDPNSRCADDR_FLAGS_CLR.DIVA_SETVIDPNSRCADDR_FLAG_FLIPIMMEDIATE)
                #Verification      
                PixelFormat = divaHandler.ReadRegister(PixelFormatOffset.Value)
                if PixelFormat & PixelFormatBitmap.Value != 0x00000000: #YUY2
                    Log.Fail("Register Verification failed, PixelFormat:{0}", PixelFormat)
                    Obj.FailCount += 1
                TileFormat = divaHandler.ReadRegister(TiledSurfaceOffset.Value)
                if TileFormat & TiledSurfaceBitmap.Value != 0x00001000: #Y-Tile
                    Log.Fail("Register Verification failed, TileFormat:{0}", TileFormat)
                    Obj.FailCount += 1
                Scaler = divaHandler.ReadRegister(ScalerOffset.Value)
                if Scaler & ScalerBitmap.Value == 0x80000000:
                    #Plane scaler position
                    ScalerWindowXPos = divaHandler.ReadRegister(ScalerWinXPosOffset.Value)
                    if (ScalerWindowXPos & ScalerWinXPosBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Left:
                        Log.Fail("Register Verification failed, Scaler_WIN_XPOS.Expected:{0} Scaler_WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXPos)
                        Obj.FailCount += 1
                    ScalerWindowYPos = divaHandler.ReadRegister(ScalerWinYPosOffset.Value)
                    if ScalerWindowYPos & ScalerWinYPosBitmap.Value != PLANES[0].Attributes.MPODstRect.Top:
                        Log.Fail("Register Verification failed, Scaler_WIN_YPOS.Expected:{0} Scaler_WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYPos)
                        Obj.FailCount += 1
                    #Plane Scaler Size
                    ScalerWindowXSize = divaHandler.ReadRegister(ScalerWinXSZOffset.Value)
                    if (ScalerWindowXSize & ScalerWinXSZBitmap.Value) >> 16 != (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left):
                        Log.Fail("Register Verification failed, Scaler_WIN_XSIZE.Expected {0} Scaler_WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXSize)
                        Obj.FailCount += 1
                    ScalerWindowYSize = divaHandler.ReadRegister(ScalerWinYSZOffset.Value)
                    if ScalerWindowYSize & ScalerWinYSZBitmap.Value != (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top):
                        Log.Fail("Register Verification failed, Scaler_WIN_YSIZE.Expected {0} Scaler_WIN_YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYSize)
                        Obj.FailCount += 1
                #else:
                #    #Plane position
                #    #WindowXPos = divaHandler.ReadRegister(PlaneXPOSOffset.Value)
                #    #if WindowXPos & PlaneXPOSBitmap.Value != PLANES[0].Attributes.MPODstRect.Left:
                #    #    Log.Fail("Register Verification failed, WIN_XPOS.Expected:{0} WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, WindowXPos)
                #    #    Obj.FailCount += 1
                #    #WindowYPos = divaHandler.ReadRegister(PlaneYPOSOffset.Value)
                #    #if (WindowYPos & PlaneYPOSBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Top:
                #    #    Log.Fail("Register Verification failed, WIN_YPOS.Expected:{0} WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, WindowYPos)
                #    #    Obj.FailCount += 1
                #    #Plane Scaler Size
                #    WindowXSize = divaHandler.ReadRegister(PlaneXSizeOffset.Value)
                #    if WindowXSize& PlaneXSizeBitmap.Value <= (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1) and WindowXSize & PlaneXSizeBitmap.Value > (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1 - 3):
                #        Log.Fail("Register Verification failed, WIN_XSIZE.Expected {0} WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, WindowXSize)
                #        Obj.FailCount += 1
                #    WindowYSize = divaHandler.ReadRegister(PlaneYSizeOffset.Value)
                #    if (WindowYSize & PlaneYSizeBitmap.Value) >> 16 <= (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1) and (WindowYSize & PlaneYSizeBitmap.Value) >> 16 > (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1 - 3):
                #        Log.Fail("Register Verification failed, YSIZE.Expected {0} YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, WindowYSize)
                #        Obj.FailCount += 1
                if divaHandler.CheckUnderRun():
                    Log.Fail("Underrun Seen")
                    Obj.FailCount += 1
                ##Verfiy Watermark and DBUF implementation remaining.
            else:
                #TODO: Fallback mechanism to be implemented
                print "CheckMPO Failed"

        while(Plane1_ResizeIterator.Resize("LEFT", 3)):
            PLANES[0].Attributes.MPODstRect = Plane1_ResizeIterator.CurrentRect
            PLANES[0].Attributes.MPOClipRect = Plane1_ResizeIterator.CurrentRect
            PLANES[1].Attributes.MPODstRect.Left = Plane1_ResizeIterator.CurrentRect.Right
            PLANES[1].Attributes.MPOClipRect.Left = Plane1_ResizeIterator.CurrentRect.Right

            Status = divaHandler.CheckMPO(PLANES)

            if(Status == True):
                divaHandler.SetSrcAddressMPO(PLANES,  DIVA_SETVIDPNSRCADDR_FLAGS_CLR.DIVA_SETVIDPNSRCADDR_FLAG_FLIPIMMEDIATE)
                #Verification      
                PixelFormat = divaHandler.ReadRegister(PixelFormatOffset.Value)
                if PixelFormat & PixelFormatBitmap.Value != 0x00000000: #YUY2
                    Log.Fail("Register Verification failed, PixelFormat:{0}", PixelFormat)
                    Obj.FailCount += 1
                TileFormat = divaHandler.ReadRegister(TiledSurfaceOffset.Value)
                if TileFormat & TiledSurfaceBitmap.Value != 0x00001000: #Y-Tile
                    Log.Fail("Register Verification failed, TileFormat:{0}", TileFormat)
                    Obj.FailCount += 1
                Scaler = divaHandler.ReadRegister(ScalerOffset.Value)
                if Scaler & ScalerBitmap.Value == 0x80000000:
                    #Plane scaler position
                    ScalerWindowXPos = divaHandler.ReadRegister(ScalerWinXPosOffset.Value)
                    if (ScalerWindowXPos & ScalerWinXPosBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Left:
                        Log.Fail("Register Verification failed, Scaler_WIN_XPOS.Expected:{0} Scaler_WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXPos)
                        Obj.FailCount += 1
                    ScalerWindowYPos = divaHandler.ReadRegister(ScalerWinYPosOffset.Value)
                    if ScalerWindowYPos & ScalerWinYPosBitmap.Value != PLANES[0].Attributes.MPODstRect.Top:
                        Log.Fail("Register Verification failed, Scaler_WIN_YPOS.Expected:{0} Scaler_WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYPos)
                        Obj.FailCount += 1
                    #Plane Scaler Size
                    ScalerWindowXSize = divaHandler.ReadRegister(ScalerWinXSZOffset.Value)
                    if (ScalerWindowXSize & ScalerWinXSZBitmap.Value) >> 16 != (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left):
                        Log.Fail("Register Verification failed, Scaler_WIN_XSIZE.Expected {0} Scaler_WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, ScalerWindowXSize)
                        Obj.FailCount += 1
                    ScalerWindowYSize = divaHandler.ReadRegister(ScalerWinYSZOffset.Value)
                    if ScalerWindowYSize & ScalerWinYSZBitmap.Value != (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top):
                        Log.Fail("Register Verification failed, Scaler_WIN_YSIZE.Expected {0} Scaler_WIN_YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, ScalerWindowYSize)
                        Obj.FailCount += 1
                #else:
                #    #Plane position
                #    #WindowXPos = divaHandler.ReadRegister(PlaneXPOSOffset.Value)
                #    #if WindowXPos & PlaneXPOSBitmap.Value != PLANES[0].Attributes.MPODstRect.Left:
                #    #    Log.Fail("Register Verification failed, WIN_XPOS.Expected:{0} WIN_XPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Left, WindowXPos)
                #    #    Obj.FailCount += 1
                #    #WindowYPos = divaHandler.ReadRegister(PlaneYPOSOffset.Value)
                #    #if (WindowYPos & PlaneYPOSBitmap.Value) >> 16 != PLANES[0].Attributes.MPODstRect.Top:
                #    #    Log.Fail("Register Verification failed, WIN_YPOS.Expected:{0} WIN_YPOS.Value:{1}", PLANES[0].Attributes.MPODstRect.Top, WindowYPos)
                #    #    Obj.FailCount += 1
                #    #Plane Scaler Size
                #    WindowXSize = divaHandler.ReadRegister(PlaneXSizeOffset.Value)
                #    if WindowXSize& PlaneXSizeBitmap.Value <= (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1) and WindowXSize & PlaneXSizeBitmap.Value > (PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left - 1 - 3):
                #        Log.Fail("Register Verification failed, WIN_XSIZE.Expected {0} WIN_XSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Right - PLANES[0].Attributes.MPODstRect.Left, WindowXSize)
                #        Obj.FailCount += 1
                #    WindowYSize = divaHandler.ReadRegister(PlaneYSizeOffset.Value)
                #    if (WindowYSize & PlaneYSizeBitmap.Value) >> 16 <= (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1) and (WindowYSize & PlaneYSizeBitmap.Value) >> 16 > (PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top - 1 - 3):
                #        Log.Fail("Register Verification failed, YSIZE.Expected {0} YSIZE.Value {1}", PLANES[0].Attributes.MPODstRect.Bottom - PLANES[0].Attributes.MPODstRect.Top, WindowYSize)
                #        Obj.FailCount += 1
                if divaHandler.CheckUnderRun():
                    Log.Fail("Underrun Seen")
                    Obj.FailCount += 1
                ##Verfiy Watermark and DBUF implementation remaining.
            else:
                #TODO: Fallback mechanism to be implemented
                print "CheckMPO Failed"

except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

finally:
    if(divaHandler != None):
        divaHandler.DisableDFT()

if Obj.FailCount == 0:
    Obj.PassCount += 1
    Log.Success("Test Passed", Obj.PassCount)
Log.GenerateHTMLReport()
#Obj.GeneratePaveXML(__file__)
#Obj.MoveLogFiles()