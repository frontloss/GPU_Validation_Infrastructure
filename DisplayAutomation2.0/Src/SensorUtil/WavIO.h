#pragma once

#include <windows.h>

typedef struct
{
#pragma pack(1)
    UCHAR                chunkID[4];
    DWORD                chunkSize;
    UCHAR                format[4];
    UCHAR                subChunk1Id[4];
    DWORD                subChunk1Size;
    WAVEFORMATEXTENSIBLE waveFormatEx;
    UCHAR                subChunk2Id[4];
    DWORD                subChunk2Size;
#pragma pack()
} WAVE_HDR_EX2;