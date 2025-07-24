#include "ColorModelInterface.h"
#include "ImageIO.h"

int DumpWbBufferToPngFile(void *pFilename, unsigned int width, unsigned int height, void *pBitArray, unsigned int imageBpc)
{
    ImageIO * pImg      = new ImageIO();
    IPIXEL16 *pPixArray = (IPIXEL16 *)malloc(width * height * sizeof(IPIXEL16));
    if (NULL == pPixArray)
    {
        return E_POINTER;
    }

    switch (imageBpc)
    {
    case 8:
        pImg->Conver8bitArrayto16BitArray((IPIXEL8 *)pBitArray, width, height, pPixArray);
        break;
    case 10:
        pImg->Conver10bitArrayto16BitArray((IPIXEL10 *)pBitArray, width, height, pPixArray);
        break;
    default:
        pImg->Conver8bitArrayto16BitArray((IPIXEL8 *)pBitArray, width, height, pPixArray);
        break;
    }

    int ret_val = pImg->WriteFile((WCHAR *)pFilename, width, height, pPixArray);
    delete pImg;
    free(pPixArray);
    return ret_val;
}
