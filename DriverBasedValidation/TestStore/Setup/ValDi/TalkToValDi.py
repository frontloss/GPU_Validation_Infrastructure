import ctypes
import sys
import os
from igdkmd64_stubs import  *


C_GVSTUB_FEATURE_INFO_VERSION = 1

class ValDi:
    
    MAX_PIPES = 3
    MESSAGE_SLOTS = 16
    MESSAGE_SIZE = 128
    
    ################################################################################################
    def __init__(self):
        self.is_64bits = sys.maxsize > 2**32
        
        mpath = os.path.abspath(os.path.dirname(__file__))
        
        if self.is_64bits:
            self._ValDiLib_handler = ctypes.cdll.LoadLibrary(os.path.join(mpath, ".", "ValDiLib64.dll"))
        else:
            self._ValDiLib_handler = ctypes.cdll.LoadLibrary(os.path.join(mpath, ".", "ValDiLib.dll"))
        
        self._ValDiLib_handler.ValDi_GetLastErrorStr.argtypes = []
        self._ValDiLib_handler.ValDi_GetLastErrorStr.restype = ctypes.c_char_p
        
        self._ValDiLib_handler.ValDi_GetState.argtypes = []
        self._ValDiLib_handler.ValDi_GetState.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_ReadMMIO.argtypes = [ctypes.c_ulong,  ctypes.c_ulong]
        self._ValDiLib_handler.ValDi_ReadMMIO.restype =  ctypes.c_ulong        
        
        self._ValDiLib_handler.ValDi_WriteMMIO.argtypes = [ctypes.c_ulong,  ctypes.c_ulong,  ctypes.c_void_p]
        self._ValDiLib_handler.ValDi_WriteMMIO.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_GetPipeToPortMapping.argtypes = [ctypes.c_void_p]
        self._ValDiLib_handler.ValDi_GetPipeToPortMapping.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_ResumeTracing.argtypes = []
        self._ValDiLib_handler.ValDi_ResumeTracing.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_SuspendTracing.argtypes = []
        self._ValDiLib_handler.ValDi_SuspendTracing.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_FinalizeTracing.argtypes = []
        self._ValDiLib_handler.ValDi_FinalizeTracing.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_RestartTracing.argtypes = []
        self._ValDiLib_handler.ValDi_RestartTracing.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_GetHookStats.argtypes = [ctypes.c_void_p]
        self._ValDiLib_handler.ValDi_GetHookStats.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_InsertTxtMarker.argtypes = [ctypes.c_char_p]
        self._ValDiLib_handler.ValDi_InsertTxtMarker.restype = ctypes.c_ulong
        
        self._ValDiLib_handler.ValDi_GetMessages.argtypes = [ctypes.c_char_p,  ctypes.c_ushort]
        self._ValDiLib_handler.ValDi_GetMessages.restype = ctypes.c_ulong

        self._ValDiLib_handler.ValDi_GfxValStub.argtypes = [ctypes.POINTER(C_GVSTUB_FEATURE_INFO_ARGS), ctypes.c_ushort]
        self._ValDiLib_handler.ValDi_GfxValStub.restype = ctypes.c_int
        
        self._ValDiLib_handler.ValDi_AUXAccess.argtypes = [ctypes.POINTER(C_GMCH_AUX_ARGUMENTS),  ctypes.c_ushort]
        self._ValDiLib_handler.ValDi_AUXAccess.restype = ctypes.c_int

    ################################################################################################
    def GetLastError(self):
        return self._ValDiLib_handler.ValDi_GetLastErrorStr()
        
    ################################################################################################
    def getState(self):
        return self._ValDiLib_handler.ValDi_GetState()
        
    ################################################################################################
    def readMMIO(self,  address,  size):    
        dataBuffer = (ctypes.c_ubyte*size)()
        res = self._ValDiLib_handler.ValDi_ReadMMIO(address,  size,  ctypes.byref(dataBuffer))
        blist = [dataBuffer[i] for i in range(size)]
        return [res,  blist]
        
    ################################################################################################
    def writeMMIO(self,  address,  size,  data):
        dataBuffer = (ctypes.c_byte*size)(*data)
        return self._ValDiLib_handler.ValDi_WriteMMIO(address,  size,  ctypes.byref(dataBuffer))
        
    ################################################################################################
    def getPipeToPortMapping(self):
        ppMappings = (ctypes.c_ulong*self.MAX_PIPES)()
        ret = self._ValDiLib_handler.ValDi_GetPipeToPortMapping(ctypes.byref(ppMappings))
        mlist = [ppMappings[i] for i in range(self.MAX_PIPES)]
        return [ret,  mlist]
        
    ################################################################################################
    def resumeTracing(self):
        return self._ValDiLib_handler.ValDi_ResumeTracing()
    
    ################################################################################################
    def suspendTracing(self):
        return self._ValDiLib_handler.ValDi_SuspendTracing()

    ################################################################################################
    def finalizeTracing(self):
        return self._ValDiLib_handler.ValDi_FinalizeTracing()
        
    ################################################################################################
    def restartTracing(self):
        return self._ValDiLib_handler.ValDi_RestartTracing()
        
    ################################################################################################
    def getHookStats(self):
        ppStats = (ctypes.c_ulonglong*(self.MAX_PIPES*2))()
        ret = self._ValDiLib_handler.ValDi_GetHookStats(ctypes.byref(ppStats))
        syncCount =  [ppStats[i] for i in range(self.MAX_PIPES)]
        underrunsCount = [ppStats[i] for i in range(self.MAX_PIPES,  2*self.MAX_PIPES)]
        return [ret,  syncCount,  underrunsCount]
        
    ################################################################################################
    def insertTxtMarker(self, text):
        sBuff = ctypes.c_char_p(text)
        return self._ValDiLib_handler.ValDi_InsertTxtMarker(sBuff)
        
    ################################################################################################
    def getMessages(self):
        sBuff = ctypes.create_string_buffer(self.MESSAGE_SLOTS*self.MESSAGE_SIZE)
        ret = self._ValDiLib_handler.ValDi_GetMessages(sBuff,  sBuff._length_)
        rstr = ''
        rstr += sBuff.raw[:(self.MESSAGE_SLOTS*self.MESSAGE_SIZE)]
        return [ret,  rstr]
        
    ################################################################################################
    def gfxValStub(self, argBuf):
        fArg = C_GVSTUB_FEATURE_INFO_ARGS()
        fArg.stFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + argBuf.stDisplayFeatureMetaData.ulSize
        fArg.stFeatureMetaData.ulVersion = C_GVSTUB_FEATURE_INFO_VERSION
        fArg.stFeatureMetaData.ulServiceType = C_GVSTUB_FEATURE_DISPLAY
        fArg.u0.stDisplayFeatureArgs = argBuf
        size = ctypes.sizeof(fArg)
        retV = self._ValDiLib_handler.ValDi_GfxValStub(fArg, size)
        if fArg.stFeatureMetaData.ulStatus != 0:
            retV |= -1
        if fArg.u0.stDisplayFeatureArgs.stDisplayFeatureMetaData.ulStatus != 0:
            retV |= -1
        return [retV,  fArg.u0.stDisplayFeatureArgs]
        
    ################################################################################################
    def AUXAccess(self,  argBuf):
        size = ctypes.sizeof(argBuf)
        retV = self._ValDiLib_handler.ValDi_AUXAccess(ctypes.byref(argBuf),  size)
        return [retV,  argBuf]
        
