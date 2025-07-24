########################################################################################################################
# @file         alert.py
# @brief        Python library containing manual alert boxes related APIs.
# @ref alert.py exposes below APIs:
# <ul>
# <li>
#   info(message)
#   Info Alerts are typically used to notify the user about
#       * new information
#       * an urgent situation that requires acknowledgement
#       * an action was successful or not
#   Example:
#       from Libs import manual as m
#       m.alert.info("Starting the test")
# </li>
# <li>
#   error(message)
#   Error Alerts are used to notify the user about an error. Alert box will be in red color with "Error" as title.
#   Example:
#       from Libs import manual as m
#       m.alert.error("Expected and actual audio endpoints are not matching")
# </li>
# <li>
#   warning(message)
#   Warning Alerts are used to notify the user about any warning. Alert box will be in yellow color with "Warning" as
#   title.
#   Example:
#       from Libs import manual as m
#       m.alert.warning("Newly plugged panel is not detected.
#                      Do you want to try again?")
# </li>
# <li>
#   fail(message)
#   Fail Alerts are used to notify the user about a failed test. Alert box will be in red color with "Test Failed" as
#   title.
#   Example:
#       from Libs import manual as m
#       m.alert.fail("Audio endpoint verification failed")
# </li>
# <li>
#   confirm(message)
#   Confirmation Alerts are used when it is required that the user confirms a choice before continuing the test. For
#   example: "Did audio playback happened successfully?" question can be asked with "yes" and "no" options.
#   Alert box box will have two buttons "yes" and "no". If "yes" is selected True will be returned, otherwise False
#   will be returned.
#   Example:
#       from Libs import manual as m
#       result = m.alert.confirm("Did audio playback happened successfully?")
#       if result is False:
#           print "Playback failed"
# </li>
# <li>
#   prompt(message, inputs)
#   Prompt Alerts offer a way to input data or information. Prompt can be used to ask the user for a short input before
#   continuing the test. 'inputs' is a list of text fields. Alert will have two buttons "Cancel" and "Ok". None will be
#   returned if Cancel is selected, otherwise a dictionary of values entered by user will be returned.
#   Example:
#       from Libs import manual as m
#       user_input = m.alert.prompt("Enter your details", ["username", "introduction"])
#       if user_input is None:
#           print "User pressed Cancel"
#       else:
#           print user_input["username"]
#           print user_input["introduction"]
# </li>
# <li>
#   radio(message, options)
#   Radio Alerts offer several choices. A list of options is provided to the user, but only one option can be selected.
#   Alert has two buttons "Cancel" and "Ok". None will be returned if Cancel is selected, otherwise option selected by
#   user will be returned.
#   Example:
#       from Libs import manual as m
#       user_input = m.alert.radio("Select one of the below options", ["Option 1", "Option 2", "Option 3"])
#       if user_input is None:
#           print "User pressed Cancel"
#       else:
#           print user_input
# </li>
# </ul>
# @remark       To see the demo of all the alert boxes, run below command
#               python Libs\manual\modules\alert.py
# @todo         Add timeout for each alert box
# @todo         Add Entry and Exit logs for each alert
# @author       Rohit Kumar
########################################################################################################################

import tkinter
from functools import partial

from Libs.manual.modules import ui

DEFAULT_ALERT_WIDTH = 400
DEFAULT_ALERT_HEIGHT = 200
SMALL_CHAR_PIXEL = 7
CAPITAL_CHAR_PIXEL = 10
LINE_HEIGHT = 25
INPUT_FIELD_HEIGHT = 50
RADIO_HEIGHT = 30
PADDING_LEFT = 20
PADDING_TOP = 20
FOOTER_HEIGHT = 50
BUTTON_WIDTH = 20
HEADING_X = int((DEFAULT_ALERT_WIDTH - 200) / 2)
FOOTER_BUTTON_X = int((DEFAULT_ALERT_WIDTH - (2 * PADDING_LEFT) - 140) / 2)
FOOTER_BUTTON_Y = DEFAULT_ALERT_HEIGHT - FOOTER_HEIGHT


##
# @brief        Alert Types
class AlertTypes(object):
    fail = 0
    info = 1
    warning = 2
    error = 3
    confirm = 4
    prompt = 5
    radio = 6


alert_master_frame = None
controls = {}
alert_output = None


##
# @brief        Internal function to break a message into multiple lines to show withing frame boundaries
# @param[in]    message
# @return       new_message, message with '\n' character inserted
#               line_count, number of new lines in message
def __break_message(message):
    line_count = 0
    line_width = 0
    new_message = ""
    for ch in message:
        if ch.isupper():
            line_width += CAPITAL_CHAR_PIXEL
        else:
            line_width += SMALL_CHAR_PIXEL
        if ch != '\n':
            new_message += str(ch)
        if line_width >= DEFAULT_ALERT_WIDTH - (2 * PADDING_LEFT) or ch == '\n':
            new_message += "-\n"
            line_count += 1
            line_width = 0

    line_count += 1
    return new_message, line_count


##
# @brief        Internal function to destroy alert frame and set the alert output
# @param[in]    alert_type
# @param[in]    option_selected
# @return       None
def __destroy_frame(alert_type, option_selected):
    global alert_output
    global alert_master_frame

    ##
    # Handle prompt alert output
    alert_output = None
    if alert_type == 'PROMPT':
        if option_selected == 'Cancel':
            ##
            # None if Cancel button is pressed
            alert_output = None
        else:
            ##
            # Input text if pressed Ok
            output = {}
            for control in controls.keys():
                if 'input_' in control:
                    output[controls[control][4]] = controls[control][1].get()
            alert_output = output

    ##
    # Handle radio alert output
    if alert_type == 'RADIO':
        if option_selected == 'Cancel':
            ##
            # None if Cancel button is pressed
            alert_output = None
        else:
            ##
            # Selected option if pressed Ok
            for control in controls.keys():
                if 'radio_' in control:
                    alert_output = controls[control][1].get()
                    break

    ##
    # Handle confirm alert output
    if alert_type == 'CONFIRM':
        alert_output = option_selected

    ##
    # Destroy the alert master frame
    alert_master_frame.destroy()


##
# @brief        Initialize alert master frame
# @param[in]    width[optional], width of alert box
# @param[in]    height[optional], height of alert box
# @param[in]    bg[optional], background color for alert box
def __init_alert_frame(width=DEFAULT_ALERT_WIDTH, height=DEFAULT_ALERT_HEIGHT, bg=ui.Color.white):
    global alert_master_frame

    alert_master_frame = tkinter.Tk()
    alert_master_frame.lift()
    alert_master_frame.overrideredirect(1)
    alert_master_frame.resizable(0, 0)
    alert_master_frame.configure(bg=bg)
    alert_master_frame.attributes('-topmost', True)
    screen_width = alert_master_frame.winfo_screenwidth()
    screen_height = alert_master_frame.winfo_screenheight()

    ##
    # @todo calculate x and y position by considering scaling value
    # calculate position x and y coordinates
    # x = (screen_width / 2) - (width / 2)
    # y = (screen_height / 2) - (height / 2)
    x = 300
    y = 200

    alert_master_frame.geometry('%dx%d+%d+%d' % (width, height, x, y))


def info(message):
    global alert_master_frame

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + (PADDING_TOP + FOOTER_HEIGHT)

    __init_alert_frame(height=height)

    ui.draw_label(alert_master_frame, message, PADDING_LEFT, PADDING_TOP, bg=ui.Color.white, font='Helvetica 12')
    f = partial(__destroy_frame, 'INFO', 'Ok')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Ok', BUTTON_WIDTH, FOOTER_BUTTON_X, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.light, fg=ui.Color.dark)
    alert_master_frame.mainloop()


def error(message):
    global alert_master_frame

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + (FOOTER_HEIGHT * 2)

    __init_alert_frame(height=height, bg=ui.Color.danger)

    ui.draw_label(
        alert_master_frame, "Error", HEADING_X + 2 * PADDING_LEFT, 0, bg=ui.Color.danger, fg=ui.Color.white,
        font='Helvetica 28 bold')
    ui.draw_label(
        alert_master_frame, message, PADDING_LEFT, FOOTER_HEIGHT, bg=ui.Color.danger, fg=ui.Color.white,
        font='Helvetica 12')
    f = partial(__destroy_frame, 'ERROR', 'Ok')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Ok', BUTTON_WIDTH, FOOTER_BUTTON_X, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.light, fg=ui.Color.dark)
    alert_master_frame.mainloop()


def fail(message):
    global alert_master_frame

    if message != "":
        message, lines = __break_message(message)
        height = lines * LINE_HEIGHT + 120
    else:
        height = 2 * FOOTER_HEIGHT + PADDING_TOP

    __init_alert_frame(height=height, bg=ui.Color.danger)

    ui.draw_label(
        alert_master_frame, "Test Failed", HEADING_X, 0, bg=ui.Color.danger, fg=ui.Color.white,
        font="Helvetica 28")
    if message != "":
        ui.draw_label(
            alert_master_frame, message, PADDING_LEFT, FOOTER_HEIGHT, bg=ui.Color.danger, fg=ui.Color.white,
            font="Helvetica 12")
    f = partial(__destroy_frame, 'ERROR', 'Ok')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Ok', BUTTON_WIDTH, FOOTER_BUTTON_X, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.light, fg=ui.Color.dark)
    alert_master_frame.mainloop()


def warning(message, alert_type=None):
    global alert_master_frame

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + (2 * FOOTER_HEIGHT)

    __init_alert_frame(height=height, bg=ui.Color.warning)

    ui.draw_label(
        alert_master_frame, "Warning", HEADING_X + PADDING_LEFT, 0, bg=ui.Color.warning, fg=ui.Color.dark,
        font='Helvetica 24')
    ui.draw_label(
        alert_master_frame, message, PADDING_LEFT, FOOTER_HEIGHT, bg=ui.Color.warning, fg=ui.Color.dark,
        font='Helvetica 12')
    if alert_type == AlertTypes.confirm:
        f = partial(__destroy_frame, 'CONFIRM', True)
        f.__name__ = "__destroy_frame"
        ui.draw_button(
            alert_master_frame, 'Yes', BUTTON_WIDTH, PADDING_LEFT, height - FOOTER_HEIGHT,
            f,
            bg=ui.Color.success, fg=ui.Color.white)
        f = partial(__destroy_frame, 'CONFIRM', False)
        f.__name__ = "__destroy_frame"
        ui.draw_button(
            alert_master_frame, 'No', BUTTON_WIDTH, 11 * PADDING_LEFT, height - FOOTER_HEIGHT,
            f,
            bg=ui.Color.danger, fg=ui.Color.white)
    else:
        f = partial(__destroy_frame, 'WARNING', 'Ok')
        f.__name__ = "__destroy_frame"
        ui.draw_button(
            alert_master_frame, 'Ok', BUTTON_WIDTH, FOOTER_BUTTON_X, height - FOOTER_HEIGHT,
            f,
            bg=ui.Color.dark, fg=ui.Color.light)
    alert_master_frame.mainloop()
    return alert_output


def confirm(message):
    global alert_output
    global alert_master_frame

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + (PADDING_TOP + FOOTER_HEIGHT)

    __init_alert_frame(height=height)

    ui.draw_label(
        alert_master_frame, message, PADDING_LEFT, PADDING_TOP, bg=ui.Color.white,
        font="Helvetica 12")
    f = partial(__destroy_frame, 'CONFIRM', True)
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Yes', BUTTON_WIDTH, PADDING_LEFT, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.success, fg=ui.Color.white)
    f = partial(__destroy_frame, 'CONFIRM', False)
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'No', BUTTON_WIDTH, 11 * PADDING_LEFT, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.danger, fg=ui.Color.white)
    alert_master_frame.mainloop()
    return alert_output


def prompt(message, inputs):
    global alert_master_frame
    global alert_output

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + len(inputs) * INPUT_FIELD_HEIGHT + 90

    __init_alert_frame(height=height)

    ui.draw_label(alert_master_frame, message, PADDING_LEFT, PADDING_TOP, bg=ui.Color.white, font="Helvetica 12")
    y_increment = 20
    for _input in inputs:
        if 'value' not in _input.keys():
            _input['value'] = None
        ui.draw_label(
            alert_master_frame, _input['name'], PADDING_LEFT, lines * LINE_HEIGHT + y_increment, bg=ui.Color.white)
        y_increment += 25
        controls['input_' + _input['name']] = ui.draw_entry(
            alert_master_frame, PADDING_LEFT, lines * LINE_HEIGHT + y_increment, default_value=_input['value'],
            bg="white", fg="#58666e", width=40) + [_input['name']]
        y_increment += 25
    f = partial(__destroy_frame, 'PROMPT', 'Cancel')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Cancel', BUTTON_WIDTH, PADDING_LEFT, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.danger, fg=ui.Color.white)
    f = partial(__destroy_frame, 'PROMPT', 'Ok')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Ok', BUTTON_WIDTH, 11 * PADDING_LEFT, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.success, fg=ui.Color.white)
    alert_master_frame.mainloop()
    return alert_output


def radio(message, options):
    global alert_output
    global alert_master_frame

    message, lines = __break_message(message)
    height = lines * LINE_HEIGHT + len(options) * RADIO_HEIGHT + 90

    __init_alert_frame(height=height)

    ui.draw_label(alert_master_frame, message, PADDING_LEFT, 20, bg=ui.Color.white, font="Helvetica 12")
    y = lines * LINE_HEIGHT + 30
    index = 0
    radio_variable = tkinter.IntVar()
    for option in options:
        controls['radio_'] = ui.draw_radio(
            alert_master_frame, radio_variable, PADDING_LEFT, y, option, index, bg=ui.Color.white)
        index += 1
        y += 30
    f = partial(__destroy_frame, 'RADIO', 'Cancel')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Cancel', BUTTON_WIDTH, PADDING_LEFT, height - FOOTER_HEIGHT,
        f, bg=ui.Color.danger, fg=ui.Color.white)
    f = partial(__destroy_frame, 'RADIO', 'Ok')
    f.__name__ = "__destroy_frame"
    ui.draw_button(
        alert_master_frame, 'Ok', BUTTON_WIDTH, 11 * PADDING_LEFT, height - FOOTER_HEIGHT,
        f,
        bg=ui.Color.success, fg=ui.Color.white)
    alert_master_frame.mainloop()
    if alert_output is not None:
        alert_output = options[alert_output]
    return alert_output


if __name__ == '__main__':
    info("This is an INFORMATION alert. Info alert can be used to show general instructions during test. "
         "This is an INFORMATION alert. Info alert can be used to show general instructions during test. "
         "This is an INFORMATION alert. Info alert can be used to show general instructions during test. ")
    error("This is an error alert. Error alert can be used to show any failure during test.")
    warning("This is a warning alert. Warning alert can be used to show warnings during test.")
    print(confirm("This is a confirm alert. Confirm alert has two buttons, yes and no. It can be used to ask simple"
                  "questions from the user. \n\n\nResult will be True in case of yes and False in case of no."))
    print(warning("Try Again?", alert_type=AlertTypes.confirm))
    print(prompt('Please enter your name and message',
                 [{'name': 'Full Name'}, {'name': 'Message', 'value': 'Message placeholder'}]))
    print(radio("Please select an option", ["Option 1", "Option 2", "Option 3"]))
    fail("")
    fail("Failed with message")
