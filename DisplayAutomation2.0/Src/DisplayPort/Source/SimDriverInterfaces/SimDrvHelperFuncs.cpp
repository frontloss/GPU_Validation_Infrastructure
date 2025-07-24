#include "DisplayPort.h"
#include "SimDrvParser.h"

extern "C"
{
#include "..\GfxValSimulator\GfxValSimLibrary\GfxValSim.h"
}

extern struct DPMSTTopology BranchDetails[MAX_PATH], DisplayDetails[MAX_PATH];

/*
 * @brief        Helper function to initialize DP SST and parse EDID, DPCD details from the XML
 * @param[In]    SSTXMLFile needed for parsing the EDID and DPCD data
 * @param[In]    Port number
 * @param[In]    Low power state to enable plug/unplug during S3/S4 event
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL SIMDRVHELPERFUNCS_ParseNSendSSTInfoToSimDrv(CHAR *pchXmlFile, UINT uiPortNumber, BOOL bIsLowPower)
{
    BOOL  bRet           = TRUE;
    BOOL  bEdidRetStatus = FALSE;
    BOOL  bDpcdRetStatus = FALSE;
    ULONG ulCount        = 0;

    rapidxml::xml_node<> *    pchRootNode;
    rapidxml::file<>          SSTXMLFile(pchXmlFile);
    rapidxml::xml_document<> *doc = new rapidxml::xml_document<>();

    /* Parse EDID from DP SST XML and get details */
    doc->parse<0>(SSTXMLFile.data());

    do
    {
        /* To check for the node that is pointing is EDID node or not */

        pchRootNode = doc->first_node();

        if (pchRootNode == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: EDID node not present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        if ((strcmp(pchRootNode->name(), "EDID")) != 0)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: EDID name is present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        /* To check for low power mode */
        if (bIsLowPower == TRUE)
        {
            /* Function call for parsing EDID Information from XML file and sending all the EDID data to GFX Simulation driver in low power mode */
            bEdidRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_GFXS3S4_EDID_DATA);
            if (bEdidRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: EDID Parsing Failed in low power mode!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }
        else
        {
            /* Function call for parsing EDID Information from XML file and sending all the EDID data to GFX Simulation driver */
            bEdidRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_EDID_DATA);
            if (bEdidRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: EDID Parsing Failed!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }

        /* To proceed to next node in the xml file and get DPCD details */
        pchRootNode = pchRootNode->next_sibling();

        if (pchRootNode == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: DPCD node not present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        /* To check for the node that is pointing is DPCD node or not */
        if ((strcmp(pchRootNode->name(), "DPCD")) != 0)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: DPCD name NOT present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        /* To check for low power mode */
        if (bIsLowPower == TRUE)
        {
            /* Function call for parsing DPCD Information from XML file and sending all the EDID data to GFX Simulation driver in low power mode */
            bDpcdRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_GFXS3S4_DPCD_DATA);
            if (bDpcdRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Parsing Failed in low power mode!!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }
        else
        {
            /* Function call for parsing DPCD Information from XML file and sending all the EDID data to GFX Simulation driver */
            bDpcdRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_DPCD_DATA);
            if (bDpcdRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Parsing Failed!!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }

    } while (FALSE);

    doc->clear();
    delete doc;

    return bRet;
}

/*
 * @brief        Helper function to Get DP MST Topology details of Branch/Display Nodes from the XML
 * @param[In]    TopologyFile needed for parsing the Branch and Display data
 * @param[In]    Port number
 * @param[In]    Low power state to enable plug/unplug during S3/S4 event
 * @return       BOOL. 'TRUE' indicates SUCCESS and 'FALSE' indicates FAILURE
 */
BOOL SIMDRVHELPERFUNCS_ParseNSendMSTInfoToSimDrv(CHAR *pchXmlFile, UINT uiPortNumber, PBRANCHDISP_DATA_ARRAY pBranchDispArray, BOOL bIsLowPower)
{
    BOOL bEdidRetStatus = FALSE;
    BOOL bDpcdRetStatus = FALSE;
    BOOL bRet           = TRUE;

    rapidxml::xml_node<> *    pchRootNode;
    rapidxml::file<>          TopologyXMLFile(pchXmlFile);
    rapidxml::xml_document<> *doc = new rapidxml::xml_document<>();

    /* Parse Branch/Display Data from DPMST XML and get details*/
    doc->parse<0>(TopologyXMLFile.data());
    pchRootNode = doc->first_node();

    do
    {
        stDPDevContext.hGfxValSimHandle = GetGfxValSimHandle();
        /* Initialize DP AUX Stub driver */
        if (stDPDevContext.hGfxValSimHandle == NULL)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Gfx Val Simulation driver not initialized!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        /* To check for the node that is pointing is EDID node or not */
        pchRootNode = doc->first_node();
        if ((pchRootNode == NULL) || (strcmp(pchRootNode->name(), "EDID") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: EDID node not present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        if (bIsLowPower == TRUE)
        {
            /* Function call for parsing EDID Information from XML file and sending all the EDID data to GFX Simulation driver in low power mode */
            bEdidRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_GFXS3S4_EDID_DATA);
            if (bEdidRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: EDID Parsing Failed in low power mode!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }
        else
        {
            /* Function call for parsing EDID Information from XML file and sending all the EDID data to GFX Simulation driver */
            bEdidRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_EDID_DATA);
            if (bEdidRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: EDID Parsing Failed!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }

        /* To proceed to next node in the xml file and get DPCD Model details */
        pchRootNode = pchRootNode->next_sibling();

        /* To check for the node that is pointing is DPCDModel node or not */
        if ((pchRootNode == NULL) || (strcmp(pchRootNode->name(), "DPCDModel") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: DPCDModel node not present in the given xml, Load default DPCD Model Data!!!");
        }
        else
        {
            ULONG IOCTL_code = (bIsLowPower == TRUE) ? IOCTL_SET_GFXS3S4_DPCD_MODEL_DATA : IOCTL_SET_DPCD_MODEL_DATA;

            /* Function call for parsing DPCD Model Information from XML file and sending it to GFX Simulation driver */
            bDpcdRetStatus = SIMDRVPARSER_ParseFileDataAndSendDPCDModelInfo(uiPortNumber, pchRootNode, IOCTL_code);
            if (bDpcdRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Model Parsing Failed, bIsLowPower:%c !!!... Exiting...", (bIsLowPower == TRUE) ? 'T' : 'F');
                bRet = FALSE;
                break;
            }
            /* To proceed to next node in the xml file and get DPCD details, only if previous one was DPCDModel */
            pchRootNode = pchRootNode->next_sibling();
        }

        /* To check for the node that is pointing is DPCD node or not */
        if ((pchRootNode == NULL) || (strcmp(pchRootNode->name(), "DPCD") != 0))
        {
            INFO_LOG("[DisplayPort.DLL]: Error: DPCD node not present in the given xml!!!... Exiting...");
            bRet = FALSE;
            break;
        }

        if (bIsLowPower == TRUE)
        {
            /* Function call for parsing DPCD Information from XML file and sending all the EDID data to GFX Simulation driver in low power mode */
            bDpcdRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_GFXS3S4_DPCD_DATA);
            if (bDpcdRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Parsing Failed in low power mode!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }
        else
        {
            /* Function call for parsing DPCD Information from XML file and sending all the EDID data to GFX Simulation driver */
            bDpcdRetStatus = SIMDRVPARSER_ParseFileDataAndSendInfo(uiPortNumber, pchRootNode, IOCTL_SET_DPCD_DATA);
            if (bDpcdRetStatus == FALSE)
            {
                INFO_LOG("[DisplayPort.DLL]: Error: DPCD Parsing Failed!!!... Exiting...");
                bRet = FALSE;
                break;
            }
        }

        pchRootNode = pchRootNode->next_sibling();
        /* Function call to parse Branch, Display, EDID, DPCD Data from DPMST XML file*/
        if (SIMDRVPARSER_ParseTopologyXMLData(pchXmlFile, pBranchDispArray, uiPortNumber, pchRootNode) == FALSE)
        {
            INFO_LOG("[DisplayPort.DLL]: Error: Parsing Topology Failed!!!... Exiting...");
            bRet = FALSE;
            break;
        }

    } while (FALSE);

    doc->clear();
    delete doc;

    return bRet;
}