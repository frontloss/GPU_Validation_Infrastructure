#pragma once
#include "Windows.h"
#ifdef __cplusplus
extern "C"
{
#endif
    int DumpWbBufferToPngFile(void *pFilename, unsigned int width, unsigned int height, void *pBitArray, unsigned int imageBpc);
#ifdef __cplusplus
}
#endif
