#ifndef __LNL_MMIO_H__
#define __LNL_MMIO_H__

#include "Gen15CommonMMIO.h"

/* LNL specific MMIO handlers*/
BOOLEAN LNL_MMIOHANDLERS_GenSpecificMMIOInitialization(PMMIO_INTERFACE pstMMIOInterface);
BOOLEAN LNL_MMIOHANDLERS_RegisterGeneralMMIOHandlers(PMMIO_INTERFACE pstMMIOInterface);
#endif
