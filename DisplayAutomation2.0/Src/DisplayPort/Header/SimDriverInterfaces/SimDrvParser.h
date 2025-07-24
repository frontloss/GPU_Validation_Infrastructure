#pragma once
#include <iostream>
#include <fstream>

/* User defined header(s) */
#include "..\Exports\rapidxml.hpp"
#include "..\Exports\rapidxml_print.hpp"
#include "..\Exports\rapidxml_utils.hpp"
#include "log.h"

#define MAX_NUM_FILES 50 // Lets keep it 50 for now, increase if you are testing with more than 50 files
#define LT_MODEL_DATA_PATH "\\TestStore\\PanelInputData\\LINK_TRAINING_DATA\\"
#define MAX_SET_COUNT 2
#define MAX_VALUE_COUNT 8
#define MAX_TRANSACTION_COUNT 15

/* Structure contains MST topology information */
struct DPMSTTopology
{
    CHAR chNode[8];  /* Array to hold name of the node where node can be Branch or Display */
    UINT uiParentId; /* Parent id of the node */
    BOOL bVisited;   /* Flag indicates whether node processed/compared or not */
};

/* Helper Funcions */
BOOL SIMDRVPARSER_RecursiveParseTopologyDataFromXML(rapidxml::xml_node<> *pchFirstBranchNode, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiParentIndex);
BOOL SIMDRVPARSER_ParseDisplayDataFromXML(rapidxml::xml_node<> *pchBranchOrDisplay, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiParentIndex);
BOOL SIMDRVPARSER_ParseTopologyXMLData(CHAR *pchXmlFile, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiPortNumber, rapidxml::xml_node<> *pchRootNode);
BOOL SIMDRVHELPERFUNCS_ParseNSendMSTInfoToSimDrv(CHAR *pchXmlFile, UINT uiPortNumber, PBRANCHDISP_DATA_ARRAY pBranchDispArray, BOOL bIsLowPower);

BOOL SIMDRVHELPERFUNCS_ParseNSendSSTInfoToSimDrv(CHAR *pchXmlFile, UINT uiPortNumber, BOOL bIsLowPower);
BOOL SIMDRVPARSER_ParseFileDataAndSendInfo(UINT uiPortnumber, rapidxml::xml_node<> *pchNode, ULONG ulIOCTLNum);
BOOL SIMDRVPARSER_ValidateModelData(UINT tCount, std::vector<std::vector<UINT>> inputOffset, std::vector<std::vector<std::vector<UINT>>> inputValues,
                                                             std::vector<std::vector<UINT>> responseOffset, std::vector<std::vector<std::vector<UINT>>> responseValues);
BOOL SIMDRVPARSER_ValidateInputCount(UINT maxValue, UINT actualValue, size_t tCount, std::string str);
BOOL SIMDRVPARSER_ParseFileDataAndSendDPCDModelInfo(UINT uiPortnumber, rapidxml::xml_node<> *pchNode, ULONG ulIOCTLNum);
std::vector<std::vector<UINT>> SIMDRVPARSER_ParseLTValues(std::string LTValues);
std::vector<UINT>              SIMDRVPARSER_ParseLTOffset(std::string LTOffset);

