###################################################################################################################
# @file         ui.py
# @addtogroup   NorthGate
# @brief        Contains APIs to draw basic shapes
# @description  Below APIs are exposed in this file:
#               1. draw_box()
#               2. draw_label()
#               3. draw_select_box()
#               4. draw_check_button()
#               5. draw_button()
#               6. draw_entry()
#               7. draw_radio()
#
# @author       Rohit Kumar
###################################################################################################################

import tkinter


##
# @brief        Exposed class object for color palette
class Color(object):
    primary = "#7266ba"
    success = "#27c24c"
    info = "#0071c5"
    warning = "#fad733"
    danger = "#f05050"
    dark = "#3a3f51"
    light = "#dee5e7"
    white = "#fff"
    black = "#000"


##
# @brief        Exposed API to draw box on given canvas with given parameters
# @param[in]    canvas, target canvas
# @param[in]    x, starting x position of box
# @param[in]    y, starting y position of box
# @param[in]    width, width of box
# @param[in]    height, height of box
def draw_box(canvas, x, y, width, height, **kwargs):
    canvas.create_rectangle(x, y, width, height, kwargs)
    canvas.pack(fill=tkinter.BOTH)


##
# @brief        Exposed API to draw Label on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    label_text
# @param[in]    x, starting x position of label
# @param[in]    y, starting y position of label
# @return       [label, x, y], Label object, starting x and y position
def draw_label(_frame, label_text, x, y, **kwargs):
    label = tkinter.Label(_frame, kwargs, text=label_text, justify=tkinter.LEFT)
    label.place(x=x, y=y)
    return [label, x, y]


##
# @brief        Exposed API to draw select box on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    x, starting x position of select box
# @param[in]    y, starting y position of select box
# @param[in]    options, options for OptionMenu object
# @param[in]    command, command function to be called on any selection change
# @return       [select_box_ctrl, select_box_variable, x, y]
#               OptionMenu object, select box variable, starting x and y positions
def draw_select_box(_frame, x, y, options, command, **kwargs):
    select_box_variable = tkinter.StringVar(_frame)
    select_box_variable.set(options[0])
    select_box_ctrl = tkinter.OptionMenu(_frame, select_box_variable, *options, command=command, **kwargs)
    select_box_ctrl.place(x=x, y=y)
    return [select_box_ctrl, select_box_variable, x, y]


##
# @brief        Exposed API to draw check button on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    label_text, label text for check button
# @param[in]    text_color
# @param[in]    x, starting x position of check button
# @param[in]    y, starting y position of check button
# @param[in]    command, command function to be called on check button selection
# @return       [check_button, check_button_variable, x, y]
#               Checkbutton object, check button variable, starting x and y positions
def draw_check_button(_frame, label_text, text_color, x, y, command):
    check_button_variable = tkinter.IntVar()
    check_button = tkinter.Checkbutton(_frame, text=label_text, variable=check_button_variable, foreground=text_color,
                                       bg="white", command=command)
    check_button.place(x=x, y=y)
    return [check_button, check_button_variable, x, y]


##
# @brief        Exposed API to draw button on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    text, label text for button
# @param[in]    width, width of button
# @param[in]    x, starting x position of button
# @param[in]    y, starting y position of button
# @param[in]    command, command function to be called on button click
# @return       [button, x, y]
#               Button object, starting x and y positions
def draw_button(_frame, text, width, x, y, command, **kwargs):
    button = tkinter.Button(_frame, kwargs, text=text, width=width, command=command)
    button.place(x=x, y=y)
    return [button, x, y]


##
# @brief        Exposed API to draw text input box on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    x, starting x position of input box
# @param[in]    y, starting y position of input box
# @param[in]    value, default text value
# @return       [entry_ctrl, entry_variable, x, y]
#               Entry object, entry variable, starting x and y positions
def draw_entry(_frame, x, y, default_value=None, **kwargs):
    entry_variable = tkinter.StringVar(_frame)
    if default_value is not None:
        entry_variable.set(default_value)
    entry_ctrl = tkinter.Entry(_frame, kwargs, textvariable=entry_variable)
    entry_ctrl.place(x=x, y=y)
    return [entry_ctrl, entry_variable, x, y]


##
# @brief        Exposed API to draw radio button on given frame with given parameters
# @param[in]    _frame, target frame
# @param[in]    radio_variable, target variable for Radiobutton object
# @param[in]    x, starting x position of radio button
# @param[in]    y, starting y position of radio button
# @param[in]    text, label text for radio button
# @param[in]    value, value for Radiobutton object
# @return       [radio_ctrl, radio_variable, x, y]
#               Radiobutton object, radio button variable, starting x and y positions
def draw_radio(_frame, radio_variable, x, y, text, value, **kwargs):
    radio_ctrl = tkinter.Radiobutton(_frame, kwargs, text=text, variable=radio_variable, value=value)
    radio_ctrl.place(x=x, y=y)
    return [radio_ctrl, radio_variable, x, y]
