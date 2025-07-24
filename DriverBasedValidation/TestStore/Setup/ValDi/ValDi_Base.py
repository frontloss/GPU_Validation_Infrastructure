import os
import TalkToValDi
from igdkmd64_stubs import  *


C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION = 1
C_GVSTUB_DISPLAY_FEATURE_STATUS_SUCCESS = 0
C_GVSTUB_MAX_DPCD_DATA = 512
dpAuxChannels = [4,  1,  2,  3]

class ValDi_BaseClass():
    

    DPCDTransactionIndex = 0
    ValDiAPI = TalkToValDi.ValDi()
    enabledFramework = 0
    enabledFeatures = []
    
    ################################################################################################
    def isFrameworkEnabled(self):
        return enabledFramework
        
    ################################################################################################
    def isFeatureEnabled(self,  eFeature):
        
        if eFeature in self.enabledFeatures :
            return 1
            
        return 0
    
    ################################################################################################
    def enableGfxValStubFramework(self):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS)
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENABLE_DISABLE_FRAMEWORK
        args.u0.stEnableDisableFramework.bEnableFramework = 1
        [errFlag,  args]  = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Enable framework failed!\n')
            return -1
        
        self.enabledFramework = 1
        return 0
            
    ################################################################################################   
    def enableGfxValStubFeature(self,  eFeature):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENABLE_DISABLE_FEATURE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENABLE_DISABLE_FEATURE
        args.u0.stEnableDisableFeature.bEnableFeature = 1
        args.u0.stEnableDisableFeature.eFeatureEnable = eFeature
        [errFlag,  args]  = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Enable feature failed!\n')
            return -1
        
        if not (eFeature in self.enabledFeatures):
            self.enabledFeatures.append(eFeature)
            
        return 0
    
    ################################################################################################
    def disableGfxValStubFramework(self):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENABLE_DISABLE_DISPLAY_FRAMEWORK_ARGS)
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENABLE_DISABLE_FRAMEWORK
        args.u0.stEnableDisableFramework.bEnableFramework = 0
        [errFlag,  args]  = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Disable framework failed!\n')
            return -1
        
        self.enabledFramework = 0
        return 0
    
    ################################################################################################
    def disableGfxValStubFeature(self,  eFeature):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENABLE_DISABLE_FEATURE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENABLE_DISABLE_FEATURE
        args.u0.stEnableDisableFeature.bEnableFeature = 0
        args.u0.stEnableDisableFeature.eFeatureEnable = eFeature
        [errFlag,  args]  = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Disable feature failed!\n')
            return -1
            
        if eFeature in self.enabledFeatures:
            self.enabledFeatures.remove(eFeature)
        
        return 0
        
    ################################################################################################
    def getNextTransactionIndex(self):
        ret = self.DPCDTransactionIndex
        self.DPCDTransactionIndex +=1
        return ret
        
    ################################################################################################
    def checkDisplayConnectivity(self, displayUID):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_GET_DEVICE_CONNECTIVITY_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_GET_DEVICE_CONNECTIVITY
        args.u0.stDeviceConnectivity.ulDisplayUID = displayUID
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Get display connectivity failed!\n')
            return -1
        
        if args.u0.stDeviceConnectivity.bAttached:
            return 1
            
        return 0
        
    ################################################################################################
    def checkIfPortIsFree(self,  ePortType):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENUM_DEVICE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENUM_DEVICE
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Enum displays failed!\n')
            return -1
        lastUID = 0
        for i in range(args.u0.stEnumDevice.ulNumDisplays):
            if args.u0.stEnumDevice.stDisplayDetailsArgs[i].ePortType == ePortType:
                if self.checkDisplayConnectivity(args.u0.stEnumDevice.stDisplayDetailsArgs[i].ulDisplayUID) == 1:
                    return 0
                else:
                    lastUID = args.u0.stEnumDevice.stDisplayDetailsArgs[i].ulDisplayUID
                
        return lastUID
    
    ################################################################################################
    def enumDisplays(self):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_ENUM_DEVICE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_ENUM_DEVICE
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print 'Enum displays failed!\n'

        listOfDisplays = [] 
        for i in range(args.u0.stEnumDevice.ulNumDisplays):
            listOfDisplays.append([args.u0.stEnumDevice.stDisplayDetailsArgs[i].ulDisplayUID,  args.u0.stEnumDevice.stDisplayDetailsArgs[i].ePortType,  self.checkDisplayConnectivity(args.u0.stEnumDevice.stDisplayDetailsArgs[i].ulDisplayUID)])
        
        return listOfDisplays
            
    ################################################################################################
    def loadBinFile(self,  path):
        if not os.path.isfile(path):
            print 'Could not open [%s]'%path
            return [-1,  []]
            
        f = open(path,  "rb")
        data = f.read()
        bdata = (ctypes.c_ubyte*len(data)).from_buffer_copy(data)
        return [0,  bdata]
    
    ################################################################################################
    def setDPCDData(self,  ePortType,  address,  data):
        auxAccessArgs = C_GMCH_AUX_ARGUMENTS()
    
        DPCDBuffer = (ctypes.c_ubyte*len(data))(*data)
        auxAccessArgs.eDisplayPort = ePortType
        auxAccessArgs.eOperation = C_GMCH_AUX_READ
        auxAccessArgs.ucAuxChannelType = dpAuxChannels[ ePortType - C_GVSTUB_INTDPA_PORT]
        auxAccessArgs.pucBuffer = ctypes.addressof(DPCDBuffer)
        auxAccessArgs.ucBufferSize = len(data)
        auxAccessArgs.ulDPCDAddress = address
        [errFlag,  auxAccessArgs]  = self.ValDiAPI.AUXAccess(auxAccessArgs)
        if errFlag != 0:
            print 'setDPCDData failed!\n'
    
        return [errFlag, auxAccessArgs]
