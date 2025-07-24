#pragma once
#include "Windows.h"
#include <iostream>
#define DLLEXEVERSION 100
class PlaybackVerifierApp
{
  public:
    PlaybackVerifierApp();
    ~PlaybackVerifierApp();
    static PlaybackVerifierApp *GetInstance();
    bool                        Init(int argc, CHAR *argv[]);
};