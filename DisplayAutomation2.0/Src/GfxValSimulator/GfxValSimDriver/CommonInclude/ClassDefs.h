/*===========================================================================
; ClassDefs.h
;----------------------------------------------------------------------------
INTEL CONFIDENTIAL
Copyright 2000-2014
Intel Corporation All Rights Reserved.

The source code contained or described herein and all documents related to the
source code ("Material") are owned by Intel Corporation or its suppliers or
licensors. Title to the Material remains with Intel Corporation or its suppliers
and licensors. The Material contains trade secrets and proprietary and confidential
information of Intel or its suppliers and licensors. The Material is protected by
worldwide copyright and trade secret laws and treaty provisions. No part of the
Material may be used, copied, reproduced, modified, published, uploaded, posted,
transmitted, distributed, or disclosed in any way without Intel’s prior express
written permission.

No license under any patent, copyright, trade secret or other intellectual
property right is granted to or conferred upon you by disclosure or delivery
of the Materials, either expressly, by implication, inducement, estoppel or
otherwise. Any license under such intellectual property rights must be express
and approved by Intel in writing.
;--------------------------------------------------------------------------*/
/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Class specific macros
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Base class declaration
//
#define BEGIN_CLASS_DECLARE(ClassName) \
    typedef struct _##ClassName        \
    {
#define END_CLASS_DECLARE(ClassName) \
    void (*Destroy)(void *pThis);    \
    }                                \
    ClassName, *P##ClassName;
//
// Derived class declaration
//
#define BEGIN_DERIVEDCLASS_DECLARE(ClassName, BaseClassName) \
    typedef struct _##ClassName                              \
    {                                                        \
        BaseClassName;
#define END_DERIVEDCLASS_DECLARE(ClassName) \
    }                                       \
    ClassName, *P##ClassName;
//
// For abstraction
//
#define RESERVED2(x, y) x##y
#define RESERVED1(x, y) RESERVED2(x, y)
#define RANDOMNUMBER __LINE__ // __COUNTER__
#define UNIQUENAME(ValueName) RESERVED1(ValueName, RANDOMNUMBER)
//#ifdef _DEBUG
#define HIDE(TYPE, ValueName) const TYPE UNIQUENAME(ValueName)
//#else	// Too much of data hiding, not required, preserve type info
//	#define HIDE(TYPE, ValueName) const unsigned char UNIQUENAME(ValueName)[sizeof(TYPE)]
//#endif
//
// Destructor
//
#define DESTROYOBJECT(pObject) pObject->Destroy(pObject)
//
// Virtual method
// Format: RETTYPE VIRTUAL(FuncName) (Param1, Param2 etc.);
//
#define VIRTUAL(FuncName) (*##FuncName)
//
// Special pragmas
//
// Convert warning C4013 to error so that undeclared functions could be caught
#pragma warning(error : 4013)
// Convert warning C4700 to error in order to catch uninitialized local variables
//#pragma warning(error: 4700)
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// Macros very specific to CSL, GAL & IAIM abstraction
//
/////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef _CSL
#define CSL_VIRTUAL(FuncName) VIRTUAL(FuncName)
#define CSL_PRIVATE(TYPE, ValueName) TYPE ValueName
#define CSL_PRIVATE_VALUE(ValueName) ValueName
#else
#define CSL_VIRTUAL(FuncName) VIRTUAL(UNIQUENAME(FuncName))
#define CSL_PRIVATE(TYPE, ValueName) HIDE(TYPE, ValueName)
#define CSL_PRIVATE_VALUE(ValueName) UNIQUENAME(ValueName)
#endif

#ifdef _GAL
#define GAL_VIRTUAL(FuncName) VIRTUAL(FuncName)
#define GAL_PRIVATE(TYPE, ValueName) TYPE ValueName
#define GAL_PRIVATE_VALUE(ValueName) ValueName
#else
#define GAL_VIRTUAL(FuncName) VIRTUAL(UNIQUENAME(FuncName))
#define GAL_PRIVATE(TYPE, ValueName) HIDE(TYPE, ValueName)
#define GAL_PRIVATE_VALUE(ValueName) UNIQUENAME(ValueName)
#endif

#ifdef _IAIM
#define GAL_IAIM_PRIVATE(TYPE, ValueName) TYPE ValueName
#else
#define GAL_IAIM_PRIVATE(TYPE, ValueName) GAL_PRIVATE(TYPE, ValueName)
#endif

#ifdef _IAIM
#define IAIM_VIRTUAL(FuncName) VIRTUAL(FuncName)
#else
#define IAIM_VIRTUAL(FuncName) VIRTUAL(UNIQUENAME(FuncName))
#endif
/////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////
