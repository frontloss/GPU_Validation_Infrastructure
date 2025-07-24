#include "PlaybackVerifierApp.h"
#include "..\DisplayAudioCodec\Header\DisplayAudioCodec.h"
#pragma warning(disable : 4996)

int main(int argc, CHAR *argv[])
{
    try
    {
        PlaybackVerifierApp::GetInstance()->Init(argc, argv);
    }
    catch (std::bad_alloc &exc)
    {
        std::cerr << exc.what() << std::endl;
    }
    return 0;
}

PlaybackVerifierApp::PlaybackVerifierApp()
{
}

PlaybackVerifierApp::~PlaybackVerifierApp()
{
}

PlaybackVerifierApp *PlaybackVerifierApp::GetInstance()
{
    static PlaybackVerifierApp *Shared;
    Shared = new PlaybackVerifierApp;
    return Shared;
}

bool PlaybackVerifierApp::Init(int argc, CHAR *argv[])
{
    BOOL bVerify = FALSE;
    if (argc < 3)
    {
        printf("Invalid usage. Refer Readme.txt\n\n");
        return false;
    }
    // Initialize(NULL); kept it for future purpose

    if (dllversion() == DLLEXEVERSION)
    {
        printf("\nDLL is loaded\n");
    }

    CHAR *waveFileToPlay = NULL;
    CHAR *EndPointName   = NULL;
    CHAR *portType       = NULL;
    BOOL  BVerify        = FALSE;
    DWORD i              = 1;
    while (i < argc)
    {
        if (0 == strcmp(argv[i], "-endpoint"))
        {
            i++;
            EndPointName = (char *)malloc(sizeof(char) * strlen(argv[i]));
            memcpy((char *)EndPointName, argv[i], strlen(argv[i]));
        }
        else if (0 == strcmp(argv[i], "-play"))
        {
            i++;
            waveFileToPlay = (char *)malloc(sizeof(char) * strlen(argv[i]));
            memcpy((char *)waveFileToPlay, argv[i], strlen(argv[i]));
        }
        else if (0 == strcmp(argv[i], "-port"))
        {
            i++;
            portType = (char *)malloc(sizeof(char) * strlen(argv[i]));
            memcpy((char *)portType, argv[i], strlen(argv[i]));
        }
        else if (0 == strcmp(argv[i], "-verify"))
        {
            BVerify = TRUE;
        }
        i++;
    }

    if (BVerify)
    {
        PlayAudioAndVerify(waveFileToPlay, EndPointName, portType);
    }
    else
    {
        PlayAudio(waveFileToPlay, EndPointName, portType);
    }
    free((char *)waveFileToPlay);
    free((char *)EndPointName);

    DeInitialize();

    return true;
}