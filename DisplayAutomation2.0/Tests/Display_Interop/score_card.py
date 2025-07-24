########################################################################################################################
# @file         score_card.py
# @brief        It contains setUp and tearDown methods of unittest framework.
# @details      For all Display Interop tests which is derived from this,
#               will make use of setup/teardown of this base class.
#               This script contains helper functions that will be used by test scripts.
# @author       chandrakanth pabolu
########################################################################################################################
import json
import csv
import logging
import os
import shutil

from enum import Enum
from Libs.Core.test_env import test_context
from Libs.manual.modules import alert

MASTER_SCORE_CARD = os.path.join(test_context.ROOT_FOLDER, "SCORE_CARD_DB", "master_score_card.json")
SCORE_CARD = os.path.join(test_context.LOG_FOLDER, "score_card.json")


##
# @brief        AffinityOption Enum
class Features(Enum):
    ColdBoot = 0
    Unplug_Plug = 1
    Restart = 2
    PowerEvents = 3
    NativeResolutionCheck = 4
    HDREnable_Default = 5
    VRR = 6
    AudioPlayback = 7
    HDCP = 8
    QuantizationRange = 9
    ColorDepthOverride = 10
    AllResolutions = 11
    HDR_Color_Override = 12
    SDR_Color_Override = 13
    LinkConfig_DP = 14
    LinkConfig_FRL = 15
    LinkConfig_TMDS = 16


score_card_entries = {
    Features.ColdBoot.name: {"score": "NA", "observations": "", "comments": ""},
    Features.Unplug_Plug.name: {"score": "NA", "observations": "", "comments": ""},
    Features.Restart.name: {"score": "NA", "observations": "", "comments": ""},
    Features.PowerEvents.name: {"score": "NA", "observations": "", "comments": ""},
    Features.NativeResolutionCheck.name: {"score": "NA", "observations": "", "comments": ""},
    Features.HDREnable_Default.name: {"score": "NA", "observations": "", "comments": ""},
    Features.VRR.name: {"score": "NA", "observations":  "", "comments": ""},
    Features.AudioPlayback.name: {"score": "NA", "observations": "", "comments": ""},
    Features.HDCP.name: {"score": "NA", "observations":  "", "comments": ""},
    Features.QuantizationRange.name: {"score": "NA", "observations":  "", "comments": ""},
    Features.ColorDepthOverride.name: {"score": "NA", "observations": "", "comments": ""},
    Features.AllResolutions.name: {"score": "NA", "observations": "", "comments": ""},
    Features.HDR_Color_Override.name: {"score": "NA", "observations": "", "comments": ""},
    Features.SDR_Color_Override.name: {"score": "NA", "observations": "", "comments": ""},
    Features.LinkConfig_DP.name: {"score": "NA", "observations": "", "comments": ""},
    Features.LinkConfig_FRL.name: {"score": "NA", "observations": "", "comments": ""},
    Features.LinkConfig_TMDS.name: {"score": "NA", "observations": "", "comments": ""},
}

FailureType = {Features.ColdBoot: {"NoIssue": 1, "Booted with Non Native": 0.75, "Minor corruption": 0.75,
                                   "Blankout Observed": 0, "Static Corruption": 0},
               Features.Restart: {"NoIssue": 1, "Booted with Non Native": 0.75, "Minor corruption": 0.75,
                                  "Blankout Observed": 0, "Static Corruption": 0},
               Features.PowerEvents: {"NoIssue": 1, "Booted with Non Native": 0.75, "Minor corruption": 0.75,
                                      "Blankout Observed": 0, "Static Corruption": 0},
               Features.NativeResolutionCheck: {"NoIssue": 1, "Display comes in Non Native": 0.75,
                                                "Minor corruption": 0.75, "Blankout Observed": 0, "Static Corruption": 0},
               Features.Unplug_Plug: {"NoIssue": 1, "Display comes in Non Native": 0.75, "Minor corruption": 0.75,
                                      "Blankout Observed": 0, "Static Corruption": 0},
               Features.HDREnable_Default: {"Display Comes up, No Issue": 1, "HDR Capability Not shown": 0,
                                            "Blankout Observed": 0, "Static Corruption": 0,
                                            "HDR option seen for Non-HDR panel": 0},
               Features.VRR: {"Display Comes up, No Issue": 1, "Display Comes but reverts to previous RR": 0.5,
                              "VRR not working": 0.5, "Blankout Observed": 0, "Static Corruption": 0,
                              "Capability Not shown": 0},
               Features.AudioPlayback: {"Playback heard, No Issue": 1, "Playback not heard": 0,
                                        "Audio Capability Not shown": 0},
               Features.HDCP: {"Display Comes up & Playback works fine": 1, "Video playback lag": 0.5,
                                "Capability Not shown": 0, "Display Blankout Observed": 0, "Static Corruption": 0},
               Features.QuantizationRange: {"Variations seen when applying quantization range without issues.": 1,
                                            "Capability Not shown": 0, "Display Blankout Observed": 0,
                                            "Static Corruption": 0},
               Features.AllResolutions: {"Display Comes up, No Issue.": 1, "Resolution revert to previous config.": 0.5,
                                         "Display Blankout Observed": 0, "Static Corruption": 0,
                                         "Resolution list not shown": 0},
               Features.HDR_Color_Override: {"Display Comes up, No Issue": 1, "Blankout Observed": 0,
                                            "Static Corruption": 0, "Other issue": 0},
               Features.SDR_Color_Override: {"Display Comes up, No Issue": 1, "Blankout Observed": 0,
                                             "Static Corruption": 0, "Other issue": 0},
               Features.LinkConfig_DP: {"Display Comes up, No Issue": 1, "Blankout Observed": 0,
                                             "Static Corruption": 0, "Other issue": 0},
               Features.LinkConfig_FRL: {"Display Comes up, No Issue": 1, "Blankout Observed": 0,
                                             "Static Corruption": 0, "Other issue": 0},
               Features.LinkConfig_TMDS: {"Display Comes up, No Issue": 1, "Blankout Observed": 0,
                                         "Static Corruption": 0, "Other issue": 0},
               }

panel_template = {
    "panel_name": "dummy",
    "idsid": "dummy",
    "feature_score": score_card_entries,
    "hsd": []
}

master_score_card = {
    "panel_name": "dummy",
    "feature_score": score_card_entries,
    "hsd": []
}


##
# @brief        Exposed API to verify observation from user and assign corresponding score.
# @param[in]    feature - Feature for which user observation is retrieved.
# @return       bool - Returns True if score is 1 else False
def verify_observation_assign_score(feature: Features) -> bool:
    comments = ""
    observation = alert.radio(
        f"{feature.name} : Please enter your observation", list(FailureType[feature].keys()))
    if observation is None:
        logging.info("User selected Cancel.")
        # alert.info("Retry: Please choose the right option.")
        # verify_observation_assign_score(feature)
        return False
    else:
        logging.info(f"Observation from user: {observation}.")
        score = FailureType[feature][observation]
        if score < 1:
            msg = alert.prompt('Please enter your comments', [{'name': 'Message'}])
            comments = msg['Message']
            logging.error(f"User observations: {comments}")
        __assign_score(feature, score, observation, comments)

        return True if score == 1 else False


##
# @brief        Internal API to verify if panel exists.
# @param[in]    panel_name - Checks if current json belongs to the passed panel.
# @return       bool - Returns True if panel exists else False
def __check_panel_exists(panel_name: str) -> bool:
    if os.path.exists(SCORE_CARD):
        with open(SCORE_CARD, 'r') as openfile:
            # Reading from json file
            score_card = json.load(openfile)
            if score_card["panel_name"] != panel_name:
                os.remove(SCORE_CARD)
            else:
                return True  # File exists and matches to monitor
    return False


##
# @brief        Exposed API for initialization of scorecard json with panel name.
# @param[in]    panel_name - Panel name for initialization.
# @param[in]    idsid      - idsid of tester.
# @return       None
def init(panel_name: str, idsid: str):
    if __check_panel_exists(panel_name):
        return

    # Serializing json
    panel_template["panel_name"] = panel_name
    panel_template["idsid"] = idsid
    json_object = json.dumps(panel_template, indent=4)

    # Writing to sample.json
    with open(SCORE_CARD, "w") as outfile:
        outfile.write(json_object)


##
# @brief        Exposed API for returning panel/monitor name.
# @return       panel_name - Panel name.
def get_panel_name():
    if not os.path.exists(SCORE_CARD):
        logging.error(f"{SCORE_CARD} doesn't exist.")
    with open(SCORE_CARD, 'r') as openfile:
        # Reading from json file
        score_card = json.load(openfile)
        panel_name = score_card["panel_name"]

    return panel_name


##
# @brief        Internal API to assign score, user observations and comments.
# @param[in]    feature - Feature for which user observation is retrieved.
# @param[in]    score - Score as per the user observation.
# @param[in]    observations - Predefined observations.
# @param[in]    comments - User comments.
# @return       bool - Returns True if score is 1 else False
def __assign_score(feature: Features, score: int, observations: str, comments: str):
    # Opening JSON file
    if not os.path.exists(SCORE_CARD):
        logging.error(f"{SCORE_CARD} doesn't exist.")

    with open(SCORE_CARD, 'r') as openfile:
        # Reading from json file
        score_card = json.load(openfile)

        # updating json with score
        score_card['feature_score'][feature.name]["score"] = score
        score_card['feature_score'][feature.name]["observations"] = observations
        score_card['feature_score'][feature.name]["comments"] = comments

    os.remove(SCORE_CARD)
    with open(SCORE_CARD, 'w') as f:
        json.dump(score_card, f, indent=4)

    print(score_card)
    print(type(score_card))


##
# @brief        Internal API to update current json to master json.
# @param[in]    feature - Feature for which user observation is retrieved.
# @return       bool - Returns True if score is 1 else False
def __update_panel_score_details():
    # To be done
    if os.path.exists(MASTER_SCORE_CARD):
        logging.info(f"{MASTER_SCORE_CARD}  exists.")
        with open(MASTER_SCORE_CARD, 'r') as openfile:
            # Reading from json file
            master_score_card = json.load(openfile)

    with open(SCORE_CARD, 'r') as openfile:
        # Reading from json file
        score_card = json.load(openfile)
        master_score_card[score_card["panel_name"]] = score_card


def __convert_to_csv():
    # iterating through enum
    # import inspect
    #
    # def iter_enum(e):
    #     for member in e:
    #         if inspect.isclass(member.value) and issubclass(member.value, enum.Enum):
    #             iter_enum(member.value)
    #         else:
    #             print(member)
    #
    # iter_enum(Properties)
    #
    with open(SCORE_CARD, 'r') as openfile:
        # Reading from json file
        score_card = json.load(openfile)
        with open('score_card.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # writer.writeheader()
            writer.writerow(["S.No", "Scenario", "Score"])
            counter = 1
            for key, value in score_card.items():
                writer.writerow([counter, key, value])
                counter = counter+1


if __name__ == '__main__':
    init("dummy")
    verify_observation_assign_score(Features.ColdBoot)
    verify_observation_assign_score(Features.Restart)
    verify_observation_assign_score(Features.AllResolutions)
    # convert_to_csv()
