#ifndef __MMIOREGS_H__
#define __MMIOREGS_H__

#include "ValSimCommonInclude.h"

#define DDI_AUX_CTL_A_SKL 0x64010
#define DDI_AUX_CTL_B_SKL 0x64110
#define DDI_AUX_CTL_C_SKL 0x64210
#define DDI_AUX_CTL_D_SKL 0x64310

#define DDI_AUX_DATA_A_START_SKL 0x64014 // 64014h - 64027h
#define DDI_AUX_DATA_A_END_SKL 0x64024

#define DDI_AUX_DATA_B_START_SKL 0x64114 // 64114h - 64127h
#define DDI_AUX_DATA_B_END_SKL 0x64124

#define DDI_AUX_DATA_C_START_SKL 0x64214 // 64214h - 64227h
#define DDI_AUX_DATA_C_END_SKL 0x64224

#define DDI_AUX_DATA_D_START_SKL 0x64314 // 64314h - 64327h
#define DDI_AUX_DATA_D_END_SKL 0x64324

#define IS_AUX_DATA_REG(RegOffset)                                                                                                                                        \
    (((DDI_AUX_DATA_A_START_SKL >= RegOffset && DDI_AUX_DATA_A_END_SKL <= RegOffset) || (DDI_AUX_DATA_B_START_SKL >= RegOffset && DDI_AUX_DATA_B_END_SKL <= RegOffset) || \
      (DDI_AUX_DATA_C_START_SKL >= RegOffset && DDI_AUX_DATA_C_END_SKL <= RegOffset) || (DDI_AUX_DATA_D_START_SKL >= RegOffset && DDI_AUX_DATA_D_END_SKL <= RegOffset)) ? \
     TRUE :                                                                                                                                                               \
     FALSE)

#define IS_AUX_CONTROL_REG(RegOffset) \
    ((DDI_AUX_CTL_A_SKL == RegOffset || DDI_AUX_CTL_B_SKL == RegOffset || DDI_AUX_CTL_C_SKL == RegOffset || DDI_AUX_CTL_D_SKL == RegOffset) ? TRUE : FALSE)

#define GET_AUXREG_PORTTYPE(RegOffset) (DP_PORT_A + ((RegOffset & 0xF00u) >> 8))

#endif