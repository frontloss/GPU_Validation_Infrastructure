#pragma once

class ACPIControlMethodManager
{
public:
    ACPIControlMethodManager(void);
public:
    ~ACPIControlMethodManager(void);

    bool ACPIControlMethodManager::EvaluateControlMethod(
    ULONG ulCommand,
    ULONG ulInputBufSize,
    ULONG ulOutputBufSize,
    PVOID pInputBuffer,
    PVOID pOutputBuffer);


    OPREG_Escape esc ;
};
