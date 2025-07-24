import ctypes
 
'''
Register instance and offset 
'''
AUD_PIN_ELD_CP_VLD = 0x650C0 

 
'''
Register field expected values 
'''
audio_inactivea_DISABLE = 0b0 
audio_inactivea_ENABLE = 0b1 
audio_inactiveb_DISABLE = 0b0 
audio_inactiveb_ENABLE = 0b1 
audio_inactivec_DISABLE = 0b0 
audio_inactivec_ENABLE = 0b1 
audio_inactived_DISABLE = 0b0 
audio_inactived_ENABLE = 0b1 
audio_output_enablea_DISABLE = 0b0 
audio_output_enablea_ENABLE = 0b1 
audio_output_enableb_DISABLE = 0b0 
audio_output_enableb_ENABLE = 0b1 
audio_output_enablec_DISABLE = 0b0 
audio_output_enablec_VALID = 0b1 
audio_output_enabled_DISABLE = 0b0 
audio_output_enabled_VALID = 0b1 
cp_readya_NOT_READY = 0b0 
cp_readya_READY = 0b1 
cp_readyb_NOT_READY = 0b0 
cp_readyb_READY = 0b1 
cp_readyc_PENDING_OR_NOT_READY = 0b0 
cp_readyc_READY = 0b1 
cp_readyd_PENDING_OR_NOT_READY = 0b0 
cp_readyd_READY = 0b1 
eld_valida_INVALID = 0b0 
eld_valida_VALID = 0b1 
eld_validb_INVALID = 0b0 
eld_validb_VALID = 0b1 
eld_validc_INVALID = 0b0 
eld_validc_VALID = 0b1 
eld_validd_INVALID = 0b0 
eld_validd_VALID = 0b1 

 
'''
Register bitfield defnition structure 
'''
class AUD_PIN_ELD_CP_VLD_REG( ctypes.LittleEndianStructure ):
    _fields_ = [
        ("eld_valida"          , ctypes.c_uint32, 1), # 0 to 0 
        ("cp_readya"           , ctypes.c_uint32, 1), # 1 to 1 
        ("audio_output_enablea" , ctypes.c_uint32, 1), # 2 to 2 
        ("audio_inactivea"     , ctypes.c_uint32, 1), # 3 to 3 
        ("eld_validb"          , ctypes.c_uint32, 1), # 4 to 4 
        ("cp_readyb"           , ctypes.c_uint32, 1), # 5 to 5 
        ("audio_output_enableb" , ctypes.c_uint32, 1), # 6 to 6 
        ("audio_inactiveb"     , ctypes.c_uint32, 1), # 7 to 7 
        ("eld_validc"          , ctypes.c_uint32, 1), # 8 to 8 
        ("cp_readyc"           , ctypes.c_uint32, 1), # 9 to 9 
        ("audio_output_enablec" , ctypes.c_uint32, 1), # 10 to 10 
        ("audio_inactivec"     , ctypes.c_uint32, 1), # 11 to 11
        ("eld_validd", ctypes.c_uint32, 1),  # 12 to 12
        ("cp_readyd", ctypes.c_uint32, 1),  # 13 to 13
        ("audio_output_enabled", ctypes.c_uint32, 1),  # 14 to 14
        ("audio_inactived", ctypes.c_uint32, 1),  # 15 to 15
        ("reserved_16"         , ctypes.c_uint32, 16), # 16 to 31
    ]

 
class AUD_PIN_ELD_CP_VLD_REGISTER( ctypes.Union ):
    _anonymous_ = ("u",)
    _fields_ = [
        ("u",      AUD_PIN_ELD_CP_VLD_REG ),
        ("asUint", ctypes.c_uint32 ) ]