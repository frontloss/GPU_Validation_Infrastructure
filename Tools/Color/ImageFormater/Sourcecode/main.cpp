#include"ImageFormater.h"
#include<cstdlib>


void term_func() {
    std::cout << "Unhandled Exception Triggered" << endl;
    exit(-1);
}


int wmain(int argc, wchar_t* argv[])
{
    wchar_t* pInFileName = NULL;
    wchar_t* pOutFileName = NULL;
    int pitch, width, height, tile;
    SB_PIXELFORMAT format;
    IMAGEPROPERTIES image = { 0, 0, 0, SB_B8G8R8A8, GVSTUB_SURFACE_MEMORY_LINEAR,(10000 / 80) };
    int RetVal = 0;

    printf(" Image Formatter Version 0_3 \n"); // To Identify Version from the Exe

    if (argc < 2)
    {
        printf("Not enough Arguments Received .Usage:  -i <in image file>  -o <out image file> -w <output width> -h <output height> -f <format> -t <Surface Memory Type> -HDR <1-enable HDR>  -b <brightness unit [optional]> \n\n");
        return -1;
    }

    for (int i = 0; i < argc; i++)   //parse the command line arguments
    {
        if (wcscmp(argv[i], L"-i") == 0)
        {
            i++;
            pInFileName = argv[i];
        }
        else if (wcscmp(argv[i], L"-w") == 0)
        {
            i++;
            image.width = stoi(argv[i]);
        }
        else if (wcscmp(argv[i], L"-h") == 0)
        {
            i++;
            image.height = stoi(argv[i]);
        }
        else if (wcscmp(argv[i], L"-f") == 0)
        {
            i++;
            image.pixelFormat = (SB_PIXELFORMAT)stoi(argv[i]);  //numerical input for format enum
            //image.pixelFormat = string2pixelformat(argv[i]);  //string input for format enum
        }
        else if (wcscmp(argv[i], L"-t") == 0)
        {
            -
                i++;
            image.tile = (GVSTUB_SURFACE_MEMORY_TYPE)stoi(argv[i]);

            if ((image.tile != GVSTUB_SURFACE_MEMORY_LINEAR) && (image.tile != GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED))   //only linear & Y legacy supported
            {
                printf("\nSurface Memory Type Not Supported : Only Linear & Legacy Y tileed Supported \n");
                return -2;
            }
        }
        else if (wcscmp(argv[i], L"-HDR") == 0)
        {
            i++;
            image.HDR = stoi(argv[i]);
        }
        else if (wcscmp(argv[i], L"-o") == 0)
        {
            i++;
            pOutFileName = argv[i];
        }
        else if (wcscmp(argv[i], L"-b") == 0)
        {
            i++;
            image.brightness_unit = 10000.0 / (double)stoi(argv[i]);
        }
    }

    DWORD dataSize;
    int n64Rows;
    int nTIles;
    int nBytesPerRow;

    try
    {
        set_terminate(term_func); // Ensure no Abrubt Crash

        if (image.tile == GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED)
        {
            switch (image.pixelFormat)
            {
            case SB_B8G8R8X8:
            case SB_B8G8R8A8:
            case SB_R8G8B8X8:
            case SB_R8G8B8A8:
            case SB_R10G10B10X2:
            case SB_R10G10B10A2:
            case SB_B10G10R10X2:
            case SB_B10G10R10A2:
            case SB_YUV444_8:
            case SB_YUV444_10:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 4;           //4 Bytes for each pixel
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128);
                break;
            }
            case SB_R16G16B16X16F:
            case SB_R16G16B16A16F:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 8;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128);
                break;
            }
            case SB_YUV444_16:
            case SB_YUV444_12:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 8;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128);
                break;
            }
            case SB_NV12YUV420:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = n64Rows * 64 * nTIles * 128 + round(n64Rows * 64 * nTIles * 128 / 2.0);   //planar format Y plane + UV plane
                break;
            }
            case SB_P016YUV420:
            case SB_P010YUV420:
            case SB_P012YUV420:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 2;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128 + round(n64Rows * 64 * nTIles * 128 / 2.0));   //planar format Y plane + UV plane
                break;
            }
            case SB_YUV422:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 2;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128);
            }
            case SB_YUV422_10:
            case SB_YUV422_12:
            case SB_YUV422_16:
            {
                n64Rows = ceil(image.height / 64.0);
                nBytesPerRow = image.width * 4;
                nTIles = ceil(nBytesPerRow / 128.0);
                dataSize = (n64Rows * 64 * nTIles * 128);
                break;
            }

            default:
            {
                printf("Entered Format is NOT Supported \n");
                return -8;
                break;
            }

            }

            if (n64Rows * 64 != image.height || nTIles * 128 != nBytesPerRow)
            {
                printf("\nERROR:: Buffer Dimentsion do not match condition:\n Height must be multiple of 64 and width must be multiple of Tile width \n");
                return -7;
            }
        }

        else
        {
            switch (image.pixelFormat)
            {
            case SB_B8G8R8X8:
            case SB_B8G8R8A8:
            case SB_R8G8B8X8:
            case SB_R8G8B8A8:
            case SB_R10G10B10X2:
            case SB_R10G10B10A2:
            case SB_B10G10R10X2:
            case SB_B10G10R10A2:
            case SB_YUV444_8:
            {
                dataSize = image.width * image.height * 4;
                break;
            }

            case SB_R16G16B16X16F:
            case SB_R16G16B16A16F:
            case SB_YUV444_16:
            case SB_YUV444_12:
            {
                dataSize = image.width * image.height * 8;
                break;
            }
            case SB_NV12YUV420:
            {
                // height should be even number,
                image.height = (image.height + 1) & (0xFFFE); //height should be always an even number
                dataSize = ((image.height * ceil(image.width / 4096.0) * 4096) + round((image.height / 2.0) * ceil(image.width / 4096.0) * 4096)); //  planar format has a Y surface and A UV surface;UV is half height of Y
                break;
            }
            case SB_P016YUV420:
            case SB_P010YUV420:
            case SB_P012YUV420:
            {
                // height should be even number,
                image.height = (image.height + 1) & (0xFFFE); //height should be always an even number
                dataSize = ((image.height * ceil((image.width * 2) / 4096.0) * 4096) + round((image.height / 2.0) * ceil((image.width * 2) / 4096.0) * 4096));  //  planar format has a Y surface and A UV surface;UV is half height of Y
                break;
            }
            case SB_YUV422:
            {
                dataSize = image.width * image.height * 2;
                break;
            }
            case SB_YUV422_10:
            case SB_YUV422_12:
            case SB_YUV422_16:
            case SB_YUV444_10:
            {
                dataSize = image.width * image.height * 4;
                break;
            }
            default:
            {
                printf("Entered Format is NOT Supported \n");
                return -3;
                break;
            }
            }

        }



        ImageFormater Buffer;

        IPIXEL* pixel = (IPIXEL*)malloc(dataSize);  //alocate memory for the output dump;
        if (pixel == NULL)
        {
            printf("MEMORY ALLOCATION FAILED\n");
            return -4;
        }

        Buffer.SetBufferParameters(image);

        if (image.tile == GVSTUB_SURFACE_MEMORY_Y_LEGACY_TILED)
        {
            Buffer.ProcessYTilled(pInFileName, pixel);
        }
        else
        {
            Buffer.ProcessLinear(pInFileName, pixel);
        }

        //write to raw data to file
        FILE* pF = _wfopen(pOutFileName, L"wb");
        if (!pF)
        {
            printf("Failed to Open Write File");
            RetVal = -5;
            goto exit;
        }
        fwrite(pixel, 1, dataSize, pF);
        fclose(pF);

    exit:
        free(pixel);
    }
    catch (std::exception & e)
    {
        std::cout << "Exception Occurred! : " << e.what();
        RetVal = -6;
    }
    return RetVal;
}