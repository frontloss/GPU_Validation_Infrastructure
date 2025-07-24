#include <sys/stat.h>
#include <direct.h>
#include "DisplayPort.h"
#include "SimDrvParser.h"

struct DPMSTTopology    BranchDetails[MAX_PATH], DisplayDetails[MAX_PATH], CurTopology[MAX_PATH];
extern GFX_ADAPTER_INFO GFX_0_ADAPTER_INFO; // Multiadapter WA

/**
 * @brief		Routine that recursively parse XML file for Branch Node details
 * @params[In]   The MST XML file
 * @params[In]   Topology data structure consisting of branch and display details needed for filling up data
 * @params[In]   Port number
 * @params[In]   First node detail in the XML file
 * @return		BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL SIMDRVPARSER_ParseTopologyXMLData(CHAR *pchXmlFile, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiPortNumber, rapidxml::xml_node<> *pchRootNode)
{
    rapidxml::xml_node<> *pchFirstBranchNode;
    UINT                  uiParentIndex = PARENT_INDEX_BRANCH_CONNECTED_TO_SRC;
    BOOL                  bRet          = TRUE;

    do
    {
        /* Initialize DP AUX Stub driver */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        /* Checking the node name is topology or not in the given xml */
        if ((pchRootNode == NULL) || (strcmp(pchRootNode->name(), "Topology") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Topology Node NOT found in DPMSTTopology XML file!!!... Exiting.... ");
            bRet = FALSE;
            break;
        }

        /* Populate the portNumber to the Branch Structure given from the user */
        pBranchDispArray->uiPortNum = uiPortNumber;

        /* Parse the MST Topology from XML file to get Branch and Display Node details*/
        pchFirstBranchNode = pchRootNode->first_node();
        if (pchFirstBranchNode == NULL || (strcmp(pchFirstBranchNode->name(), "Branch") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: First Node Element in Topology Node NOT found!!!... Exiting....");
            bRet = FALSE;
            break;
        }

        /* Function call to parse Branch and Display data, fail if data is not present*/
        if (SIMDRVPARSER_RecursiveParseTopologyDataFromXML(pchFirstBranchNode, pBranchDispArray, uiParentIndex) == FALSE)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: The Branch/Display Data in the XML is not proper!!!... Exiting....");
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    return bRet;
}

/**
 * @brief       Routine that converts Link Training values in string format to 2D vector of integers.
 * @params[In]  LTValues in the form of string(e.g. [[0x11,0x11,0x00],[0x77,0x77,0x80]])
 * @return      2D Vector of integers
 */
std::vector<std::vector<UINT>> SIMDRVPARSER_ParseLTValues(std::string LTValues)
{
    std::vector<std::vector<UINT>> vecValues;
    UINT8                          startPos = 0, endPos = 0;
    std::string                    startDelimiter        = "0x";
    std::string                    commaDelimiter        = ",";
    std::string                    openBracketDelimiter  = "[";
    std::string                    closeBracketDelimiter = "]";

    /* Terminating condition for LTValues string*/
    while (LTValues.size() > 2)
    {
        /* startPos and endPos gets the position of first occurance of '[' and ']' in LTValues string*/
        startPos = (UINT8)LTValues.find(openBracketDelimiter);
        endPos   = (UINT8)LTValues.find(closeBracketDelimiter);
        /* if (endPos -startPos <=2) then LTValues is empty(e.g. [])*/
        if ((endPos - startPos) > 2)
        {
            /* Get Values offset wise, e.g.( first it get [0x11,0x11,0x00] and so on  */
            /* Length of subStrValues is (endPos-startPos + 1) */
            std::string subStrValues = LTValues.substr(startPos, (endPos - startPos + 1));
            LTValues.erase(startPos, endPos + 2);
            std::vector<UINT> vec;
            /* Extract each value which starts with 0x and ends with either ',' or ']' */
            while (((startPos = (UINT8)subStrValues.find(startDelimiter)) != (UINT8)std::string::npos) &&
                   (((endPos = (UINT8)subStrValues.find(commaDelimiter)) != (UINT8)std::string::npos) ||
                    ((endPos = (UINT8)subStrValues.find(closeBracketDelimiter)) != (UINT8)std::string::npos)))
            {
                vec.push_back(std::stol(subStrValues.substr(startPos, (endPos - startPos + 1)), NULL, 0));
                /* Erase the sub string which is processed*/
                subStrValues.erase(startPos, (endPos - startPos + 1));
            }
            /* Building nested vector*/
            vecValues.push_back(vec);
        }
    }
    return vecValues;
}

/**
 * @brief       Routine that converts Link Training offsets in string format to vector of integers.
 * @params[In]  LTOffset in the form of string(e.g. [0x202, 0x100])
 * @return      integer vector
 */
std::vector<UINT> SIMDRVPARSER_ParseLTOffset(std::string LTOffset)
{
    std::vector<UINT> vecOffset;
    UINT8             startPos = 0, endPos = 0;
    std::string       startDelimiter        = "0x";
    std::string       commaDelimiter        = ",";
    std::string       closeBracketDelimiter = "]";
    /* Extract each value which starts with 0x and ends with either ',' or ']' */
    while (((startPos = (UINT8)LTOffset.find(startDelimiter)) != (UINT8)std::string::npos) &&
           (((endPos = (UINT8)LTOffset.find(commaDelimiter)) != (UINT8)std::string::npos) || ((endPos = (UINT8)LTOffset.find(closeBracketDelimiter)) != (UINT8)std::string::npos)))
    {
        vecOffset.push_back(std::stol(LTOffset.substr(startPos, (endPos - startPos)), NULL, 0));
        /* Erase the sub string which is processed*/
        LTOffset.erase(startPos, (endPos - startPos + 1));
    }
    return vecOffset;
}

/**
 * @brief		Routine that recursively parse XML file for Branch Node details
 * @params[In]   First node detail in the XML file
 * @params[In]   Topology data structure consisting of branch and display details needed for filling up data
 * @params[In]   ParentIndex ID of the BranchOrDisplay Node
 * @return		BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL SIMDRVPARSER_RecursiveParseTopologyDataFromXML(rapidxml::xml_node<> *pchFirstBranchNode, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiParentIndex)
{
    /* Details of Branch Data*/
    rapidxml::xml_node<> *pchBranchOrDisplay;
    rapidxml::xml_node<> *pchUpStrmBranchOutPort;
    rapidxml::xml_node<> *pchThisBranchInputPort;
    rapidxml::xml_node<> *pchTotalInputPorts;
    rapidxml::xml_node<> *pchTotalPhysicalPorts;
    rapidxml::xml_node<> *pchTotalVirtualPorts;
    rapidxml::xml_node<> *pchTotalAvailablePBN;
    rapidxml::xml_node<> *pchMaxLinkRate;
    rapidxml::xml_node<> *pchMaxLaneCount;
    rapidxml::xml_node<> *pchBranchReplyDelay;
    rapidxml::xml_node<> *pchLinkAddressDelay;
    rapidxml::xml_node<> *pchRemoteI2ReadDelay;
    rapidxml::xml_node<> *pchRemoteI2WriteDelay;
    rapidxml::xml_node<> *pchRemoteDPCDReadDelay;
    rapidxml::xml_node<> *pchRemoteDPCDWriteDelay;
    rapidxml::xml_node<> *pchEPRDelay;
    rapidxml::xml_node<> *pchAllocatePayloadDelay;
    rapidxml::xml_node<> *pchClearPayLoadDelay;
    rapidxml::xml_node<> *pchDisplayNode;

    BOOL bRet = TRUE;

    do
    {
        INFO_LOG("SIMDRVPARSER_RecursiveParseTopologyDataFromXML Entered");

        /* Check for First Child Node of Branch in the MST Topology XML*/
        if (pchFirstBranchNode != NULL)
        {
            if (strcmp(pchFirstBranchNode->name(), "Display") == 0)
            {
                /* Function call if is Display Node*/
                if (SIMDRVPARSER_ParseDisplayDataFromXML(pchFirstBranchNode, pBranchDispArray, uiParentIndex) == FALSE)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: Display Data Parsing Failed!!! Exiting...");
                    bRet = FALSE;
                    break;
                }
            }
            else if (strcmp(pchFirstBranchNode->name(), "Branch") == 0)
            {
                pchUpStrmBranchOutPort = pchFirstBranchNode->first_node();
                if (pchUpStrmBranchOutPort == NULL || (strcmp(pchUpStrmBranchOutPort->name(), "UpStrmBranchOutPort") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: UpStrmBranchOutPort node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If UpStrmBranchOutPort present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.ucUpStrmBranchOutPort = atoi(pchUpStrmBranchOutPort->value());

                pchThisBranchInputPort = pchUpStrmBranchOutPort->next_sibling();
                if (pchThisBranchInputPort == NULL || (strcmp(pchThisBranchInputPort->name(), "ThisBranchInputPort") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: ThisBranchInputPort node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If ThisBranchInputPort present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.ucThisBranchInputPort = atoi(pchThisBranchInputPort->value());

                pchTotalInputPorts = pchThisBranchInputPort->next_sibling();
                if (pchTotalInputPorts == NULL || (strcmp(pchTotalInputPorts->name(), "TotalInputPorts") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: TotalInputPorts node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If TotalInputPorts present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.ucTotalInputPorts = atoi(pchTotalInputPorts->value());

                pchTotalPhysicalPorts = pchTotalInputPorts->next_sibling();
                if (pchTotalPhysicalPorts == NULL || (strcmp(pchTotalPhysicalPorts->name(), "TotalPhysicalPorts") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: TotalPhysicalPorts node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If TotalPhysicalPorts present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.ucTotalPhysicalPorts = atoi(pchTotalPhysicalPorts->value());

                pchTotalVirtualPorts = pchTotalPhysicalPorts->next_sibling();
                if (pchTotalVirtualPorts == NULL || (strcmp(pchTotalVirtualPorts->name(), "TotalVirtualPorts") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: TotalVirtualPorts node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If TotalVirtualPorts present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.ucTotalVirtualPorts = atoi(pchTotalVirtualPorts->value());

                pchTotalAvailablePBN = pchTotalVirtualPorts->next_sibling();
                if (pchTotalAvailablePBN == NULL || (strcmp(pchTotalAvailablePBN->name(), "TotalAvailablePBN") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: TotalAvailablePBN node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If TotalAvailablePBN node present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.usTotalAvailablePBN = atoi(pchTotalAvailablePBN->value());

                pchMaxLinkRate = pchTotalAvailablePBN->next_sibling();
                if (pchMaxLinkRate == NULL || (strcmp(pchMaxLinkRate->name(), "MaxLinkRate") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: MaxLinkRate node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If MaxLinkRate present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiMaxLinkRate = atoi(pchMaxLinkRate->value());

                pchMaxLaneCount = pchMaxLinkRate->next_sibling();
                if (pchMaxLaneCount == NULL || (strcmp(pchMaxLaneCount->name(), "MaxLaneCount") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: MaxLaneCount node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If MaxLaneCount present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiMaxLaneCount = atoi(pchMaxLaneCount->value());

                pchBranchReplyDelay = pchMaxLaneCount->next_sibling();
                if (pchBranchReplyDelay == NULL || (strcmp(pchBranchReplyDelay->name(), "BranchReplyDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: BranchReplyDelay node is present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If BranchReplyDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiBranchReplyDelay = atoi(pchBranchReplyDelay->value());

                pchLinkAddressDelay = pchBranchReplyDelay->next_sibling();
                if (pchLinkAddressDelay == NULL || (strcmp(pchLinkAddressDelay->name(), "LinkAddressDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: LinkAddressDelay node is present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If LinkAddressDelay present fill the detils in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiLinkAddressDelay = atoi(pchLinkAddressDelay->value());

                pchRemoteI2ReadDelay = pchLinkAddressDelay->next_sibling();
                if (pchRemoteI2ReadDelay == NULL || (strcmp(pchRemoteI2ReadDelay->name(), "RemoteI2ReadDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: RemoteI2ReadDelay node NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If remoteI2ReadDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiRemoteI2ReadDelay = atoi(pchRemoteI2ReadDelay->value());

                pchRemoteI2WriteDelay = pchRemoteI2ReadDelay->next_sibling();
                if (pchRemoteI2WriteDelay == NULL || (strcmp(pchRemoteI2WriteDelay->name(), "RemoteI2WriteDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: RemoteI2WriteDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If remoteI2WriteDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiRemoteI2WriteDelay = atoi(pchRemoteI2WriteDelay->value());

                pchRemoteDPCDReadDelay = pchRemoteI2WriteDelay->next_sibling();
                if (pchRemoteDPCDReadDelay == NULL || (strcmp(pchRemoteDPCDReadDelay->name(), "RemoteDPCDReadDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: RemoteDPCDReadDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If RemoteDPCDReadDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiRemoteDPCDReadDelay = atoi(pchRemoteDPCDReadDelay->value());

                pchRemoteDPCDWriteDelay = pchRemoteDPCDReadDelay->next_sibling();
                if (pchRemoteDPCDWriteDelay == NULL || (strcmp(pchRemoteDPCDWriteDelay->name(), "RemoteDPCDWriteDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: RemoteDPCDWriteDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If RemoteDPCDWriteDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiRemoteDPCDWriteDelay = atoi(pchRemoteDPCDWriteDelay->value());

                pchEPRDelay = pchRemoteDPCDWriteDelay->next_sibling();
                if (pchEPRDelay == NULL || (strcmp(pchEPRDelay->name(), "EPRDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: EPRDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If EPRDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiEPRDelay = atoi(pchEPRDelay->value());

                pchAllocatePayloadDelay = pchEPRDelay->next_sibling();
                if (pchAllocatePayloadDelay == NULL || (strcmp(pchAllocatePayloadDelay->name(), "AllocatePayloadDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: AllocatePayloadDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If AllocatePayloadDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiAllocatePayloadDelay = atoi(pchAllocatePayloadDelay->value());

                pchClearPayLoadDelay = pchAllocatePayloadDelay->next_sibling();
                if (pchClearPayLoadDelay == NULL || (strcmp(pchClearPayLoadDelay->name(), "ClearPayLoadDelay") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: ClearPayLoadDelay node is NOT present in Branch data. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If ClearPayLoadDelay present fill the details in Branch Data*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].stBranchNodeDesc.uiClearPayLoadDelay = atoi(pchClearPayLoadDelay->value());

                pchDisplayNode = pchClearPayLoadDelay->next_sibling();
                if (pchDisplayNode == NULL || (strcmp(pchDisplayNode->name(), "BranchDPCD") != 0))
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: DisplayNode is NOT present. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }
                /* If pchDisplayNode present fill the details in Branch Data*/
                strcpy((char *)pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].ucDPCDName, pchDisplayNode->value());

                /* Fill NoOfBranches, ParentIndex details before proceeding to next node*/
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].uiThisIndex         = pBranchDispArray->uiNumBranches;
                pBranchDispArray->stBranchData[pBranchDispArray->uiNumBranches].uiParentBranchIndex = uiParentIndex;
                pBranchDispArray->uiNumBranches++;
                uiParentIndex++;

                if (pBranchDispArray->uiNumBranches > MAX_NUM_BRANCHES)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: Branchs in XML has exceeded given limit. XML data in Invald!!!... Exiting...");
                    bRet = FALSE;
                    break;
                }

                /* To Check for Next node whether it is Branch or Display Node*/
                pchBranchOrDisplay = pchDisplayNode->next_sibling();

                for (pchBranchOrDisplay; pchBranchOrDisplay; pchBranchOrDisplay = pchBranchOrDisplay->next_sibling())
                {
                    if (strcmp(pchBranchOrDisplay->name(), "Display") == 0)
                    {
                        /* Function call if is Display Node*/
                        if (SIMDRVPARSER_ParseDisplayDataFromXML(pchBranchOrDisplay, pBranchDispArray, ((pBranchDispArray->uiNumBranches) - 1)) == FALSE)
                        {
                            INFO_LOG("[DisplayPort.DLL]: Error: Display Data Parsing Failed!!! Exiting...");
                            bRet = FALSE;
                            break;
                        }
                    }
                    else if (strcmp(pchBranchOrDisplay->name(), "Branch") == 0)
                    {
                        /* Recursive Function call if is Branch Or Display Node*/
                        if (SIMDRVPARSER_RecursiveParseTopologyDataFromXML(pchBranchOrDisplay, pBranchDispArray, ((pBranchDispArray->uiNumBranches) - 1)) == FALSE)
                        {
                            INFO_LOG("[DisplayPort.DLL]: Error: Topology Data Parsing Failed!!! Exiting...");
                            bRet = FALSE;
                            break;
                        }
                    }
                }
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Error: Branch/Display node is NOT present. XML is Invalid!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }

    } while (FALSE);

    return bRet;
}

/**
 * @brief		Routine that recursively parse XML file for Display Node details
 * @params[In]   First node detail in the XML file
 * @params[In]   Display data structure needed for filling up data
 * @params[In]   ParentIndex ID of the Display Node
 * @return		BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL SIMDRVPARSER_ParseDisplayDataFromXML(rapidxml::xml_node<> *pchBranchOrDisplay, PBRANCHDISP_DATA_ARRAY pBranchDispArray, UINT uiParentIndex)
{
    /* Details of Display Data*/
    rapidxml::xml_node<> *pchDispUpStrmBranchOutPort;
    rapidxml::xml_node<> *pchDispThisDisplayInputPort;
    rapidxml::xml_node<> *pchDispTotalInputPorts;
    rapidxml::xml_node<> *pchDispTotalAvailablePBN;
    rapidxml::xml_node<> *pchDispMaxLinkRate;
    rapidxml::xml_node<> *pchDispMaxLaneCount;
    rapidxml::xml_node<> *pchDispRemoteDPCDReadDelay;
    rapidxml::xml_node<> *pchDispRemoteDPCDWriteDelay;
    rapidxml::xml_node<> *pchDispRemoteI2ReadDelay;
    rapidxml::xml_node<> *pchDispRemoteI2WriteDelay;
    rapidxml::xml_node<> *pchDispDPCDNode;
    rapidxml::xml_node<> *pchDispEDIDNode;

    BOOL bRet = TRUE;

    do
    {
        /* Check for First Child Node of Display in the MST Topology XML*/
        pchDispUpStrmBranchOutPort = pchBranchOrDisplay->first_node();
        if (pchDispUpStrmBranchOutPort == NULL || (strcmp(pchDispUpStrmBranchOutPort->name(), "UpStrmBranchOutPort") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain UpStrmBranchOutPort details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If UpStrmBranchOutPort present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.ucUpStrmBranchOutPort = atoi(pchDispUpStrmBranchOutPort->value());

        pchDispThisDisplayInputPort = pchDispUpStrmBranchOutPort->next_sibling();
        if (pchDispThisDisplayInputPort == NULL || (strcmp(pchDispThisDisplayInputPort->name(), "ThisDisplayInputPort") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain ThisDisplayInputPort details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If ThisDisplayInputPort present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.ucThisDisplayInputPort = atoi(pchDispThisDisplayInputPort->value());

        pchDispTotalInputPorts = pchDispThisDisplayInputPort->next_sibling();
        if (pchDispTotalInputPorts == NULL || (strcmp(pchDispTotalInputPorts->name(), "TotalInputPorts") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain dispTotalInputPorts details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If dispTotalInputPorts present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.ucTotalInputPorts = atoi(pchDispTotalInputPorts->value());

        pchDispTotalAvailablePBN = pchDispTotalInputPorts->next_sibling();
        if (pchDispTotalAvailablePBN == NULL || (strcmp(pchDispTotalAvailablePBN->name(), "TotalAvailablePBN") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain dispTotalAvailablePBN details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If dispTotalAvailablePBN present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.usTotalAvailablePBN = atoi(pchDispTotalAvailablePBN->value());

        pchDispMaxLinkRate = pchDispTotalAvailablePBN->next_sibling();
        if (pchDispMaxLinkRate == NULL || (strcmp(pchDispMaxLinkRate->name(), "MaxLinkRate") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain MaxLinkRate details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If MaxLinkRate present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiMaxLinkRate = atoi(pchDispMaxLinkRate->value());

        pchDispMaxLaneCount = pchDispMaxLinkRate->next_sibling();
        if (pchDispMaxLaneCount == NULL || (strcmp(pchDispMaxLaneCount->name(), "MaxLaneCount") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain MaxLaneCount details... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If MaxLaneCount present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiMaxLaneCount = atoi(pchDispMaxLaneCount->value());

        pchDispRemoteI2ReadDelay = pchDispMaxLaneCount->next_sibling();
        if (pchDispRemoteI2ReadDelay == NULL || (strcmp(pchDispRemoteI2ReadDelay->name(), "RemoteI2ReadDelay") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain RemoteI2ReadDelay data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If RemoteI2ReadDelay present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteI2ReadDelay = atoi(pchDispRemoteI2ReadDelay->value());

        pchDispRemoteI2WriteDelay = pchDispRemoteI2ReadDelay->next_sibling();
        if (pchDispRemoteI2WriteDelay == NULL || (strcmp(pchDispRemoteI2WriteDelay->name(), "RemoteI2WriteDelay") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain RemoteI2WriteDelay data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If RemoteI2WriteDelay present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteI2WriteDelay = atoi(pchDispRemoteI2WriteDelay->value());

        pchDispRemoteDPCDReadDelay = pchDispRemoteI2WriteDelay->next_sibling();
        if (pchDispRemoteDPCDReadDelay == NULL || (strcmp(pchDispRemoteDPCDReadDelay->name(), "RemoteDPCDReadDelay") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain RemoteDPCDReadDelay data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If RemoteDPCDReadDelay present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteDPCDReadDelay = atoi(pchDispRemoteDPCDReadDelay->value());

        pchDispRemoteDPCDWriteDelay = pchDispRemoteDPCDReadDelay->next_sibling();
        if (pchDispRemoteDPCDWriteDelay == NULL || (strcmp(pchDispRemoteDPCDWriteDelay->name(), "RemoteDPCDWriteDelay") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain RemoteDPCDWriteDelay data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If RemoteDPCDWriteDelay present fill the details in Display Data*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].stDisplayNodeDesc.uiRemoteDPCDWriteDelay = atoi(pchDispRemoteDPCDWriteDelay->value());

        pchDispDPCDNode = pchDispRemoteDPCDWriteDelay->next_sibling();
        if (pchDispDPCDNode == NULL || (strcmp(pchDispDPCDNode->name(), "DisplayDPCD") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain Display DPCD name data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If pchDispDPCDNode present fill the details in Display Data*/
        strcpy((char *)pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].ucDPCDName, pchDispDPCDNode->value());

        pchDispEDIDNode = pchDispDPCDNode->next_sibling();
        if (pchDispEDIDNode == NULL || (strcmp(pchDispEDIDNode->name(), "DisplayEDID") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Display data don't contain Display EDID name data... XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }
        /* If pchDispEDIDNode present fill the details in Display Data*/
        strcpy((char *)pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].ucDisplayName, pchDispEDIDNode->value());

        /* Fill NoofBranches, ParentIndex details before proceeding to next Display node*/
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].uiThisIndex         = pBranchDispArray->uiNumDisplays;
        pBranchDispArray->stDisplayData[pBranchDispArray->uiNumDisplays].uiParentBranchIndex = uiParentIndex;
        pBranchDispArray->uiNumDisplays++;

        if (pBranchDispArray->uiNumDisplays > MAX_NUM_DISPLAYS)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Displays in XML has exceeded given limit. XML data in Invald!!!... Exiting...");
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    return bRet;
}

/**
 * @brief			Routine that parses DP SST/MST XML file for EDID/DPCD details
 * @params[In]   	Port number detail in the DP SST/MST XML file
 * @params[In]   	Root node detail in the DP SST/MST XML file
 * @params[In]   	IoCTL name required for passing data to sim driver
 * @return			BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL SIMDRVPARSER_ParseFileDataAndSendInfo(UINT uiPortnumber, rapidxml::xml_node<> *pchNode, ULONG ulIOCTLNum)
{
    BOOL  bRet          = TRUE;
    DWORD dwStatus      = 0;
    DWORD BytesReturned = 0;
    INT   iFileSize;
    CHAR  chFilePath[256];

    struct stat st;
    size_t      bytes_read = 0;
    errno_t     err        = 0;

    FILE *                   fptrBuff;
    BYTE *                   pFileDataBuffer    = NULL;
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };
    pchNode                                     = pchNode->first_node();

    if (stDPDevContext.hGfxValSimHandle != NULL)
    {
        /* Recursively parse all EDID/DPCD data from DPMST/SST XML's files and send it to DP MST simulation driver */
        for (pchNode; pchNode; pchNode = pchNode->next_sibling())
        {
            /* This is needed to get the path of EDID and DPCD bin files */
            _getcwd(chFilePath, 255);
            strcat(chFilePath, "\\TestStore\\PanelInputData\\DP_MST_TILE\\");
            strcat(chFilePath, pchNode->value());

            /* Fill the size of the EDID in the 4 bytes of edidBuffer*/
            INT stat_result = stat(chFilePath, &st);

            /* If DP_MST_TILE path fails retry with eDP_DPSST Path*/
            if (stat_result != 0)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: %s File not found in DP_MST_TILE Folder!!!... Retrying with eDP_DPSST Folder....", pchNode->value());
                memset(chFilePath, 0, (256 * sizeof(chFilePath[0])));
                _getcwd(chFilePath, 255);
                strcat(chFilePath, "\\TestStore\\PanelInputData\\eDP_DPSST\\");
                strcat(chFilePath, pchNode->value());

                stat_result = stat(chFilePath, &st);

                /* If retry result also fails then exit */
                if (stat_result != 0)
                {
                    INFO_LOG("[DisplayPort.DLL]: Error: %s File not found in DP_MST_TILE and eDP_DPSST Folder!!!... Exiting....", pchNode->value());
                    bRet = FALSE;
                    break;
                }
            }

            iFileSize = st.st_size;

            pFileDataBuffer = (BYTE *)malloc(sizeof(FILE_DATA) + iFileSize);
            if (pFileDataBuffer == NULL)
            {
                bRet = FALSE;
                break;
            }
            ZeroMemory(pFileDataBuffer, sizeof(FILE_DATA) + iFileSize);

            /* Populate the port number to file structure*/
            ((PFILE_DATA)pFileDataBuffer)->uiPortNum = uiPortnumber;

            /* Populate the file size to file structure*/
            ((PFILE_DATA)pFileDataBuffer)->uiDataSize = iFileSize;

            strcpy((char *)(((PFILE_DATA)pFileDataBuffer)->ucNodeName), pchNode->name());

            err = fopen_s(&fptrBuff, chFilePath, "rb");
            if (err == 0)
            {
                if (fptrBuff != NULL)
                {
                    bytes_read = fread((pFileDataBuffer + sizeof(FILE_DATA)), sizeof(unsigned char), iFileSize, fptrBuff);

                    /* Close the file handle*/
                    fclose(fptrBuff);
                }
            }
            else
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD file read failed!!!... Exiting with error code : 0x%u", GetLastError());
                bRet = FALSE;
                break;
            }

            devIoControlBuffer.pInBuffer    = pFileDataBuffer;
            devIoControlBuffer.inBufferSize = (sizeof(FILE_DATA) + iFileSize);
            devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO; /* Get adapter info from cached data */

            /* IoCTL call for sending EDID/DPCD data to Simulation driver */
            dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)ulIOCTLNum, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

            if (OPERATION_FAILED == dwStatus)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: Failed to send IOCTLs during DPCD data to Gfx Sim driver with error code: 0x%u", GetLastError());
                bRet = FALSE;
                break;
            }
        }

        /* free file data buffer created */
        if (pFileDataBuffer != NULL)
        {
            free(pFileDataBuffer);
        }
    }

    return bRet;
}

/**
 *   @brief         Utility Function to Validate the count limit on a type of data
 *   @params[In]    maxValue: MAX Count of the data
 *   @params[In]    actualValue : Actual count of the data
 *   @params[In]    Transaction Count
 *   @params[In]    Type of DPCD Model data
 *   @return        BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL SIMDRVPARSER_ValidateInputCount(size_t maxValue, size_t actualValue, UCHAR tCount, std::string str)
{
    if (actualValue > maxValue)
    {
        INFO_LOG("[DisplayPort.DLL]: Error: For TransactionNum: %d and %s model data, Input Count: %d exceeds max_count: %d ... DPCD Model data Invalid!!!... Exiting...", tCount,
                 str, actualValue, maxValue);
        return false;
    }
    return true;
}

/**
 *   @brief         Verify DPCD model data for each transaction,
 *                  Each transaction can have maximum two values in input/response starting offset
 *                  Based on no of values in input/response offsets corresponding input/response values will have those many list
 *                  Lenght of list for input/response values for each offsets should not be more than 8
 *   @params[In]    Transaction Count ( <= 15)
 *   @params[In]    Input/Response DPCD offsets and its values.
 *   @return        BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL SIMDRVPARSER_ValidateModelData(UCHAR tCount, std::vector<std::vector<UINT>> inputOffset, std::vector<std::vector<std::vector<UINT>>> inputValues,
                                    std::vector<std::vector<UINT>> responseOffset, std::vector<std::vector<std::vector<UINT>>> responseValues)
{
    BOOL status = true;

    if (tCount > MAX_TRANSACTION_COUNT)
    {
        INFO_LOG("[DisplayPort.DLL]: Error: TransactionCount: %d exceeds MAX_TRANSACTION_COUNT: % ... DPCD Model data Invalid!!!... Exiting...", tCount, MAX_TRANSACTION_COUNT);
        return false;
    }

    for (int tranCount = 0; tranCount < tCount; ++tranCount)
    {
        status = SIMDRVPARSER_ValidateInputCount(MAX_SET_COUNT, inputOffset[tranCount].size(), tranCount, "input_starting_offsets");

        /* Input DPCD Values should be present for each input DPCD Offset*/
        if (inputOffset[tranCount].size() == inputValues[tranCount].size())
        {
            for (int inputSetCount = 0; inputSetCount < inputOffset[tranCount].size(); ++inputSetCount)
            {
                status = SIMDRVPARSER_ValidateInputCount(MAX_VALUE_COUNT, inputValues[tranCount][inputSetCount].size(), tranCount, "input_values");
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error: inputOffset Count and Num of inputValues Count mismatch. DPCD Model data Invald!!!... Exiting...");
            status = false;
        }
        status = SIMDRVPARSER_ValidateInputCount(MAX_SET_COUNT, responseOffset[tranCount].size(), tranCount, "response_starting_offsets");

        /* Response DPCD Values should be present for each Response DPCD Offset*/
        if (responseOffset[tranCount].size() == responseValues[tranCount].size())
        {
            for (int responseSetCount = 0; responseSetCount < responseOffset[tranCount].size(); ++responseSetCount)
            {
                status = SIMDRVPARSER_ValidateInputCount(MAX_VALUE_COUNT, responseValues[tranCount][responseSetCount].size(), tranCount, "response_values");
            }
        }
        else
        {
            INFO_LOG("[DisplayPort.DLL]: Error: ResponseOffset Count and Num of ResponseValues Count mismatch. DPCD Model data Invald!!!... Exiting...");
            status = false;
        }
    }
    return status;
}
/**
 * @brief           Routine that parses DPCD Model Data from XML and Builds DPCD model data struct
 * @params[In]      Port number required for DPCD Model Data XML file
 * @params[In]      IoCTL name required for passing data to sim driver
 * @return          BOOL. TRUE if PASS, FALSE if FAIL
 */
BOOL SIMDRVPARSER_ParseFileDataAndSendDPCDModelInfo(UINT uiPortnumber, rapidxml::xml_node<> *pchNode, ULONG ulIOCTLNum)
{
    PDP_DPCD_MODEL_DATA pDPDPCDModelData = nullptr;

    BOOL                     bRet          = TRUE;
    DWORD                    dwStatus      = 0;
    DWORD                    BytesReturned = 0;
    CHAR                     chFilePath[256];
    DEVICE_IO_CONTROL_BUFFER devIoControlBuffer = { 0 };

    pchNode = pchNode->first_node();
    if (stDPDevContext.hGfxValSimHandle != NULL)
    {
        /* Recursively parse all DPCD Model data from DPMST/SST model data XML's files and send it to DP MST simulation driver */
        for (pchNode; pchNode; pchNode = pchNode->next_sibling())
        {
            /* This is needed to get the path of DPCD Model Data file */
            _getcwd(chFilePath, 255);
            strcat(chFilePath, LT_MODEL_DATA_PATH);
            strcat(chFilePath, pchNode->value());

            rapidxml::file<>         xmlFile(chFilePath);
            rapidxml::xml_document<> doc;
            doc.parse<0>(xmlFile.data());

            rapidxml::xml_node<> *                      DPCDModel     = doc.first_node("DPCDModel");
            rapidxml::xml_node<> *                      DPCDModelData = DPCDModel->first_node("DPCDModelData");
            std::vector<std::vector<UINT>>              inputOffset;
            std::vector<std::vector<std::vector<UINT>>> inputValues;
            std::vector<std::vector<UINT>>              responseOffset;
            std::vector<std::vector<std::vector<UINT>>> responseValues;
            UCHAR                                       transactionCount = 0;
            pDPDPCDModelData                                             = (PDP_DPCD_MODEL_DATA)malloc(sizeof(DP_DPCD_MODEL_DATA));
            pDPDPCDModelData->uiPortNum                                  = uiPortnumber;
            pDPDPCDModelData->eTopologyType                              = eDPMST;

            rapidxml::xml_node<> *ulTriggerOffset = DPCDModelData->first_node();
            rapidxml::xml_node<> *transactionNode;

            if (ulTriggerOffset == NULL || (strcmp(ulTriggerOffset->name(), "ulTriggerOffsetForTrans") != 0))
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Model data doesn't contain ulTriggerOffsetForTrans... DPCD Model data Invald!!!... Exiting...");
                return FALSE;
            }
            pDPDPCDModelData->stDPCDModelData.ulTriggerOffset = std::stol(ulTriggerOffset->value(), NULL, 0);

            transactionNode = ulTriggerOffset->next_sibling();
            if (transactionNode == NULL || (strcmp(transactionNode->name(), "transaction") != 0))
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Model data doesn't contain transaction... DPCD Model data Invald!!!... Exiting...");
                return FALSE;
            }

            for (; transactionNode != NULL; transactionNode = transactionNode->next_sibling())
            {
                transactionCount++;
                for (rapidxml::xml_node<> *currNode = transactionNode->first_node(); currNode != NULL; currNode = currNode->next_sibling())
                {
                    // Null Check on currNode already happened
                    if (strcmp(currNode->name(), "inputStartingOffsets") == 0)
                    {
                        inputOffset.push_back(SIMDRVPARSER_ParseLTOffset(currNode->value()));
                        continue;
                    }

                    if (strcmp(currNode->name(), "inputValues") == 0)
                    {
                        inputValues.push_back(SIMDRVPARSER_ParseLTValues(currNode->value()));
                        continue;
                    }

                    if (strcmp(currNode->name(), "responseStartingOffsets") == 0)
                    {
                        responseOffset.push_back(SIMDRVPARSER_ParseLTOffset(currNode->value()));
                        continue;
                    }

                    if (strcmp(currNode->name(), "responseValues") == 0)
                    {
                        responseValues.push_back(SIMDRVPARSER_ParseLTValues(currNode->value()));
                        continue;
                    }
                    INFO_LOG("Error: Invalid DPCD Model Data XML format");
                    bRet = FALSE;
                }
            }

            if (SIMDRVPARSER_ValidateModelData(transactionCount, inputOffset, inputValues, responseOffset, responseValues) == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: Validate DPCD Model Data Failed... Exiting...");
                return FALSE;
            }

            pDPDPCDModelData->stDPCDModelData.ucTransactionCount = transactionCount;

            /* Fill DPCDModelData */
            for (UINT tcCount = 0; tcCount < transactionCount; ++tcCount)
            {
                pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].ucNumInputDpcdSets = (UCHAR)inputOffset[tcCount].size();
                for (UINT inputOff = 0; inputOff < inputOffset[tcCount].size(); ++inputOff)
                {
                    pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stInputDpcdSets[inputOff].ulStartingOffset = inputOffset[tcCount][inputOff];
                    pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stInputDpcdSets[inputOff].ucLength         = (UCHAR)inputValues[tcCount][inputOff].size();
                    for (UINT inputVal = 0; inputVal < inputValues[tcCount][inputOff].size(); ++inputVal)
                    {
                        pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stInputDpcdSets[inputOff].ucValues[inputVal] = inputValues[tcCount][inputOff][inputVal];
                    }
                }
                pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].ucNumResponseDpcdSets = (UCHAR)responseOffset[tcCount].size();
                for (UINT responseOff = 0; responseOff < responseOffset[tcCount].size(); ++responseOff)
                {
                    pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stResponseDpcdSets[responseOff].ulStartingOffset = responseOffset[tcCount][responseOff];
                    pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stResponseDpcdSets[responseOff].ucLength = (UCHAR)responseValues[tcCount][responseOff].size();
                    for (UINT responseVal = 0; responseVal < responseValues[tcCount][responseOff].size(); ++responseVal)
                    {
                        pDPDPCDModelData->stDPCDModelData.stDPCDTransactions[tcCount].stResponseDpcdSets[responseOff].ucValues[responseVal] =
                        responseValues[tcCount][responseOff][responseVal];
                        TRACE_LOG(CRITICAL_LOGS, "\n[DisplayPort.DLL]: DPCD Response Data: %d \n", responseValues[tcCount][responseOff][responseVal]);
                    }
                }
            }

            devIoControlBuffer.pInBuffer    = pDPDPCDModelData;
            devIoControlBuffer.inBufferSize = sizeof(DP_DPCD_MODEL_DATA);
            devIoControlBuffer.pAdapterInfo = &GFX_0_ADAPTER_INFO;

            /* IoCTL call for sending DPCD model data to Simulation driver */
            dwStatus = DeviceIoControl(stDPDevContext.hGfxValSimHandle, (DWORD)ulIOCTLNum, &devIoControlBuffer, sizeof(DEVICE_IO_CONTROL_BUFFER), NULL, 0, &BytesReturned, NULL);

            if (OPERATION_FAILED == dwStatus)
            {
                INFO_LOG("Error: Failed to send IOCTLs during send DPCD model data to Gfx Sim driver with error code: 0x%u", GetLastError());
                bRet = FALSE;
                if (pDPDPCDModelData != nullptr)
                    free(pDPDPCDModelData);
                break;
            }
            if (pDPDPCDModelData != nullptr)
                free(pDPDPCDModelData);
        }
    }
    return bRet;
}
