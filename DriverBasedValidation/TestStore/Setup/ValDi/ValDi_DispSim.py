from ValDi_Base import *
from igdkmd64_stubs import  *

class GfxStubSimClass(ValDi_BaseClass):
    
    ################################################################################################
    def __init__(self):
        if not self.enabledFramework:
            self.enableGfxValStubFramework()
            
        if not C_GVSTUB_FEATURE_DEV_SIM in self.enabledFeatures:
            if self.enableGfxValStubFeature(C_GVSTUB_FEATURE_DEV_SIM):
                raise Exception('GfxStubSim failed')
    
    ################################################################################################
    def getFreeUIDForPort(self,  ePortType):
        
        portIsFree = 1
        lastUID = 0
        
        listOfDisplays = super.enumDisplays()
        for i in listOfDisplays:
            if i[1] == ePortType:
                lastUID = i[0]
                if i[2] == 1:
                    portIsFree = 0
                    break
        
        if portIsFree:
            return lastUID
        
        return 0

    ################################################################################################
    def cacheDPCDData(self, displayUID, address, data):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_DEV_SIM_CACHE_DPCD_DATA
        args.u0.stDPCDInfo.ulDisplayUID = displayUID
        args.u0.stDPCDInfo.ulDPCDAddress = address
        args.u0.stDPCDInfo.ulSize = min(len(data),  C_GVSTUB_MAX_DPCD_DATA)
        
        DPCD_Data = (ctypes.c_ubyte*len(data))(*data)
        ctypes.memmove(ctypes.addressof(args.u0.stDPCDInfo.ucDPCDData),  ctypes.addressof(DPCD_Data),  args.u0.stDPCDInfo.ulSize)
        args.u0.stDPCDInfo.ulIndex = self.getNextTransactionIndex()
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('DPCD cache failed!\n')
            return -1
        
    ###############################################################################################    
    def patchDPCD(self,  displayUID):
        data = [0xFF, 0xFF, 0xFF]
        self.cacheDPCDData(displayUID, 0x202, data)

        data = [0x0]
        self.cacheDPCDData(displayUID, 0x101, data)
        self.cacheDPCDData(displayUID, 0x200, data)
        self.cacheDPCDData(displayUID, 0x206, data)
    
        data = [0xA4, 0x1F, 0xBC, 0x34, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.cacheDPCDData(displayUID, 0x10, data)

        data = [0x1]
        self.cacheDPCDData(displayUID, 0x600, data)
        self.cacheDPCDData(displayUID, 0x205, data)
    
    ###############################################################################################
    def plugToPort(self,  ePortType, lowPowConnect,  EDID_file,  DPCD_file):
        #check if port is free
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        portCheck = self.checkIfPortIsFree(ePortType)
        if portCheck <= 0:
            print 'Could not attach sim device - port is busy.\n'
            return -1
        
        [errCode,  EDID_Data] = self.loadBinFile(EDID_file)
        if errCode != 0:
            return -1
        
        [errCode,  DPCD_Data] = self.loadBinFile(DPCD_file)
        if errCode != 0:
            return -1
        
        #cache DPCD
        if len(DPCD_file) > 0 and ePortType >= C_GVSTUB_INTDPA_PORT and ePortType <=C_GVSTUB_INTDPD_PORT :
            args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
            args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_DEV_SIM_CACHE_DPCD_DATA_ARGS)
            args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_DEV_SIM_CACHE_DPCD_DATA
            args.u0.stDPCDInfo.ulDisplayUID = portCheck
            args.u0.stDPCDInfo.ulDPCDAddress = 0x0
            args.u0.stDPCDInfo.ulSize = min(ctypes.sizeof(DPCD_Data),  C_GVSTUB_MAX_DPCD_DATA)
            ctypes.memmove(ctypes.addressof(args.u0.stDPCDInfo.ucDPCDData),  ctypes.addressof(DPCD_Data),  args.u0.stDPCDInfo.ulSize)
            args.u0.stDPCDInfo.ulIndex = self.getNextTransactionIndex()
            [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
            if errFlag != 0:
                print('DPCD cache failed!\n')
                return -1

            self.patchDPCD(portCheck)

        #attach display
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_GET_SET_SIMULATE_DEVICE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_GET_SET_SIMULATE_DEVICE
        args.u0.stGetSetSimulateDevice.ulNumDevices = 1
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].OpType = C_GVSTUB_OP_SET
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].bAttach = 1
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].ulDisplayUID = portCheck
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].ulPortType = ePortType
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].bSimConnnectionInLowPower = lowPowConnect
        ctypes.memmove(args.u0.stGetSetSimulateDevice.stDeviceInfo[0].ucDisplayEdid,  EDID_Data,  ctypes.sizeof(EDID_Data))
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Set sim device failed!\n')
            return -1
            
        return 0
        
    ################################################################################################
    def unplugPort(self,  ePortType):
        args = C_GVSTUB_DISPLAY_FEATURE_ARGS()
        args.stDisplayFeatureMetaData.ulVersion = C_GVSTUB_DISPLAY_FEATURE_ACCESS_VERSION
        args.stDisplayFeatureMetaData.ulSize = ctypes.sizeof(C_GVSTUB_META_DATA) + ctypes.sizeof(C_GVSTUB_GET_SET_SIMULATE_DEVICE_ARGS)
        args.stDisplayFeatureMetaData.ulServiceType = C_GVSTUB_GET_SET_SIMULATE_DEVICE
        args.u0.stGetSetSimulateDevice.ulNumDevices = 1
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].OpType = GVSTUB_OP_SET
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].bAttach = 0
        
        portCheck = self.checkIfPortIsFree(ePortType)
        if portCheck > 0:
            print 'Port is not attached.\n'
            return -1
        
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].ulDisplayUID = portCheck
        args.u0.stGetSetSimulateDevice.stDeviceInfo[0].ulPortType = ePortType
        
        [errFlag,  args] = self.ValDiAPI.gfxValStub(args)
        if errFlag != 0:
            print('Set sim device failed!\n')
            return -1
        
        return 0
        

####################################################################################################
##EXAMPLE###########################################################################################
####################################################################################################

#clear all previous config
b = ValDi_BaseClass()
b.disableGfxValStubFeature(C_GVSTUB_FEATURE_DEV_SIM)


GfxStubSim = GfxStubSimClass()
testPorts = [C_GVSTUB_INTDPA_PORT, C_GVSTUB_INTDPB_PORT, C_GVSTUB_INTDPC_PORT, C_GVSTUB_INTDPD_PORT, C_GVSTUB_DVOA_PORT, C_GVSTUB_DVOB_PORT, C_GVSTUB_DVOC_PORT, C_GVSTUB_DVOD_PORT]

freePortUID = 0
for p in testPorts:
    if GfxStubSim.checkIfPortIsFree(p) > 0:
        freePortUID = p
        break

if freePortUID > 0:
    GfxStubSim.plugToPort(freePortUID, 0,  '.\\BIN\\DP_HP_ZR2240W.EDID',  '.\\BIN\\DP_HP_ZR2240W_DPCD.bin')
