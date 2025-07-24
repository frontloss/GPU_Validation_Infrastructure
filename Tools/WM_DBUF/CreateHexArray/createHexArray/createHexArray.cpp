// createHexArray.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>

int _tmain(int argc, _TCHAR* argv[])
{
	HANDLE hFile,hNewFile;
	char ucBuf[8],*pSrcBufr = NULL;
	ULONG bytesRead=0,bytesWritten=0, i=0, srcFileSize = 0;

	do
	{
		hFile = CreateFile(L"Vbt2.bin",
							GENERIC_READ|GENERIC_WRITE,
							FILE_SHARE_READ | FILE_SHARE_WRITE,
							NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);

		if(hFile == INVALID_HANDLE_VALUE)
		{
			printf(" create file failed \n");
			break;
		}

		hNewFile = CreateFile(L"Vbt_Test_Array.txt",
							GENERIC_READ|GENERIC_WRITE,
							FILE_SHARE_READ | FILE_SHARE_WRITE,
							NULL,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,NULL);

		if(hNewFile == INVALID_HANDLE_VALUE)
		{
			printf(" create new file failed \n");
			break;
		}

		srcFileSize = GetFileSize(hFile,&srcFileSize);

		printf(" write data start ..Total bytes to Write %x\n",srcFileSize);

		pSrcBufr = (char *)malloc(srcFileSize);

		if(pSrcBufr==NULL)
		{
			printf(" malloc failed \n");
			break;
		}

		if(ReadFile(hFile,pSrcBufr,srcFileSize,&bytesRead,NULL)==FALSE)
		{
			printf("File read failed \n");
			free(pSrcBufr);
			break;
		}

		if(bytesRead!=srcFileSize)
		{
			printf("total bytes read %x not matched \n",bytesRead);
			free(pSrcBufr);
			break;
		}

		i=0;
		while(i<srcFileSize)
		{
			memset(&ucBuf[0],0,8);
			sprintf(&ucBuf[0],"%x,",pSrcBufr[i] & 0xff);
			i++;
			if(WriteFile(hNewFile,ucBuf,strlen(ucBuf),&bytesWritten,NULL)==FALSE)
			{
				printf(" write data failed in new file \n");
				free(pSrcBufr);
				break;
			} 

			/*if(i%8==0)
			{
				memset(&ucBuf[0],0,8);
				sprintf(&ucBuf[0],"\r\n",pSrcBufr[i]);
				//printf(" i = %d %d\n", i,strlen(ucBuf));
				if(WriteFile(hNewFile,ucBuf,2,&bytesWritten,NULL)==FALSE)
				{
					printf(" write data failed in new file \n");
					free(pSrcBufr);
					break;
				} 
			}*/
		}

		/*if(WriteFile(hNewFile,pSrcBufr,srcFileSize,&bytesWritten,NULL)==FALSE)
		{
			printf(" write data failed in new file \n");
			free(pSrcBufr);
			break;
		}

		if(bytesWritten!=srcFileSize)
		{
			printf("total bytes written %x not matched \n",bytesWritten);
			free(pSrcBufr);
			break;
		}*/

		printf(" Total bytes written : %x %d \n",srcFileSize,srcFileSize);

		CloseHandle(hNewFile);
	}while(FALSE);

exit_label:
	CloseHandle(hFile);

	getchar();

	return 0;
}

