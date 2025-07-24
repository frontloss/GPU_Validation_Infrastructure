from ValDi_Base import *
from igdkmd64_stubs import  *
import os

dpAuxChannels = [4,  1,  2,  3]

class DispGetData_Class(ValDi_BaseClass):
    
    binPath = '.'
    
    ################################################################################################
    def __init__(self):
        if not self.enabledFramework:
            self.enableGfxValStubFramework()
    
    ################################################################################################
    def setStorePath(self,  path):
        self.binPath = path

    ################################################################################################
    def storeEDIDForUID(self,  displayUID):

        edidFileName = 'edid_'
        edidFileName += str(displayUID)
        edidFileName += '.bin'
        
        edidFileName = os.path.join(self.binPath,  edidFileName)
        edidFile = open(edidFileName,  'wb')
    
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
    
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof( C_GVSTUB_GET_EDID_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_GET_EDID
    
        args.u0.stEDID.ulDisplayUID = displayUID
    
        args.stDisplayFeatureMetaData.ulStatus = 0
        bN = 0
        while args.stDisplayFeatureMetaData.ulStatus == C_GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS:
            args.u0.stEDID.ulEdidBlockNum = bN
            bN +=1
            [errFlag,  args]  = self.ValDiAPI.gfxValStub(args)
            if args.stDisplayFeatureMetaData.ulStatus == C_GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS:
                edidFile.write(args.u0.stEDID.ucEdidData)
        
        for t in args.u0.stEDID._fields_: print(t,  getattr(args.u0.stEDID, t[0]))
        print ('\n')
    
        edidFile.close()
    
    ################################################################################################
    def storeDPCDForPortType(self,  ePortType):
        
        if ePortType < C_GVSTUB_INTDPA_PORT:
            return
            
        dpcdFileName = 'dpcd_portE'
        dpcdFileName += str(ePortType)
        dpcdFileName += '.bin'
        
        dpcdFileName = os.path.join(self.binPath,  dpcdFileName)
        dpcdFile = open(dpcdFileName,  'wb')

        #get 16x32 bytes starting from address 0x0
        readChunkSize = 16
        DPCDBuffer = (ctypes.c_ubyte*readChunkSize)(0)
        readChunks = 32
        auxAccessArgs = C_GMCH_AUX_ARGUMENTS()
        auxAccessArgs.eDisplayPort = ePortType
        auxAccessArgs.eOperation = C_GMCH_AUX_READ
        auxAccessArgs.ucAuxChannelType = dpAuxChannels[ ePortType- C_GVSTUB_INTDPA_PORT]
        auxAccessArgs.pucBuffer = ctypes.addressof(DPCDBuffer)
        auxAccessArgs.ucBufferSize = readChunkSize
        auxAccessArgs.ulDPCDAddress = 0
        while readChunks > 0:
            [errFlag,  auxAccessArgs]  = self.ValDiAPI.AUXAccess(auxAccessArgs)
            dpcdFile.write(DPCDBuffer)
            auxAccessArgs.ulDPCDAddress += readChunkSize
            readChunks -=1

        dpcdFile.close()
    
    ################################################################################################
    def storeDataForCurrentConfig(self):
        
        listOfDisplays = self.enumDisplays()
        if not listOfDisplays is None:
            for d in listOfDisplays:
                if d[2] == 1:
                    self.storeEDIDForUID(d[0])
                    self.storeDPCDForPortType(d[1])
                
                
                
####################################################################################################
##EXAMPLE
####################################################################################################
dispGetData = DispGetData_Class()
dispGetData.setStorePath('c:\\ValDi\\BIN')
dispGetData.storeDataForCurrentConfig()
