#ifndef _COMMON
#define _COMMON
#include<Windows.h>
#include<iostream>
using namespace std;
#include<sstream>
#include<fstream>


typedef enum
{
    HW_SIM_ERR_NONE = 0,
    HW_SIM_ERR_INVALID_INPUT_DATARANGE = 1,
    HW_SIM_ERR_INVALID_INPUT_DATA = 2,
    HW_SIM_ERR_INVALID_POINTER = 3,

}HW_SIM_ERR;

#endif