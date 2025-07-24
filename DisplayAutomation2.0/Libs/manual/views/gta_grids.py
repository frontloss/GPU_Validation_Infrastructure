###################################################################################################################
# @file         gta_grids.py
# @addtogroup   NorthGate
# @brief        View area implementation for GTA Grids view
# @description
#
# @author       Rohit Kumar
###################################################################################################################

import os
import threading
import time
import tkinter
from functools import partial
from tkinter import messagebox

from Libs.Core.test_env import test_context
from Libs.manual.modules import context
from Libs.manual.modules import parser
from Libs.manual.modules import ui

APPLICATION_NAME = "North Gate"
APPLICATION_VERSION = " "
APPLICATION_NAME_TAG_LINE = "Assisted Manual Testing Tool"
MAIN_ID = "#MAIN#"
NAME = "GTA Grids"  # View Name. Used in main.py master frame view list
ID = "#VIEW_GTA_GRIDS#"  # Used to uniquely identify view components
VIEW_HEADER_HEIGHT = 70  # Default height for view header
RIGHT_ASIDE_WIDTH = 190  # Default width for view right aside (System Information)
RIGHT_ASIDE_LABEL_WIDTH = 25  # Default width for label in right aside

test_list_canvas = None
__system_information = None
active_platform = None
active_os = None
active_grid = None
active_test = None
local_controls = None

tool_context = None


##
# @brief        Exposed API. Initializes all the controls of GTA grids view
#               Called by main.py init_view() function whenever selected
# @param[in]    master_frame, from main.py
# @param[in]    controls, main.py global controls dictionary
# @param[in]    view_start_x, starting x position of the view
# @param[in]    view_start_y, starting y position of the view
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
def init(master_frame, controls, view_start_x, view_start_y, frame_width, frame_height):
    global tool_context
    global local_controls
    global __system_information

    ##
    # Initialize view context
    tool_context = context.get()
    if ID not in tool_context.keys():
        tool_context[ID] = {}
        context.store(tool_context)

    ##
    # Header
    frame_view_header = tkinter.Frame(master_frame, height=VIEW_HEADER_HEIGHT, width=frame_width - view_start_x,
                                      bg=ui.Color.white)
    frame_view_header.place(x=view_start_x, y=view_start_y)
    controls[ID + 'frame_view_header'] = [frame_view_header, view_start_x, view_start_y]

    ##
    # Header Components
    controls[ID + 'label_application_name'] = ui.draw_label(
        frame_view_header, APPLICATION_NAME + APPLICATION_VERSION, 15, 5,
        font='Helvetica 24', bg=ui.Color.white, fg=ui.Color.dark)
    controls[ID + 'label_application_tag_line'] = ui.draw_label(
        frame_view_header, APPLICATION_NAME_TAG_LINE, 15, VIEW_HEADER_HEIGHT - 30,
        font='Helvetica 9', bg=ui.Color.white, fg=ui.Color.dark)
    # ui.draw_label(frame_view_header, "{0:2}".format(len(features)), FRAME_WIDTH-200, 55,
    #               font='Helvetica 24', bg=ui.Color.white)
    # ui.draw_label(frame_view_header, "Features", FRAME_WIDTH-200, 90, bg=ui.Color.white)
    # ui.draw_label(frame_view_header, "{0:3}".format(get_test_count()), FRAME_WIDTH-100, 55,
    #               font='Helvetica 24', bg=ui.Color.white)
    # ui.draw_label(frame_view_header, "Tests", FRAME_WIDTH-85, 90, bg=ui.Color.white)

    view_start_y += VIEW_HEADER_HEIGHT

    ##
    # Grid
    frame_view_grid = tkinter.Frame(master_frame,
                                    bg=ui.Color.white,
                                    height=frame_height - view_start_y - 20,
                                    width=frame_width - view_start_x - RIGHT_ASIDE_WIDTH - 20)
    frame_view_grid.place(x=view_start_x + 10, y=view_start_y + 10)
    controls[ID + 'frame_view_grid'] = [frame_view_grid, view_start_x + 10, view_start_y + 10]

    ##
    # Grid Components
    next_x = 20
    controls[ID + 'select_box_platform_label'] = ui.draw_label(
        frame_view_grid, "Platform", next_x, 20, bg=ui.Color.white)

    platform_list = ['None'] + parser.get_gta_platforms()
    if 'active_platform' in tool_context[ID].keys():
        temp = parser.get_gta_platforms()
        if tool_context[ID]['active_platform'] != 'None':
            temp.remove(tool_context[ID]['active_platform'])
        platform_list = [tool_context[ID]['active_platform'], 'None'] + temp
    f = partial(
        action_select_box_platform, next_x=next_x, frame_view_grid=frame_view_grid, master_frame=master_frame,
        frame_width=frame_width, frame_height=frame_height, view_start_x=view_start_x, view_start_y=view_start_y)
    f.__name__ = "action_select_box_platform"
    controls[ID + 'select_box_platform'] = ui.draw_select_box(
        frame_view_grid, next_x, 45, platform_list, f)
    controls[ID + 'select_box_platform'][0].config(
        bg=ui.Color.light, activebackground=ui.Color.dark, fg=ui.Color.dark, activeforeground=ui.Color.white,
        bd=0, highlightthickness=0, relief=tkinter.FLAT)

    local_controls = controls
    if 'active_platform' in tool_context[ID].keys():
        action_select_box_platform(
            0, next_x, frame_view_grid, master_frame, frame_width, frame_height, view_start_x, view_start_y)

    ##
    # System Information
    frame_view_system_information = tkinter.Frame(master_frame, bg=ui.Color.white,
                                                  height=frame_height - view_start_y - 20,
                                                  width=RIGHT_ASIDE_WIDTH - 10)
    frame_view_system_information.place(x=frame_width - RIGHT_ASIDE_WIDTH, y=view_start_y + 10)
    controls[ID + 'frame_view_system_information'] = [frame_view_system_information, frame_width - RIGHT_ASIDE_WIDTH,
                                                      view_start_y + 10]
    local_controls = controls

    ##
    # System Information Components
    next_y = 0
    ui.draw_label(
        frame_view_system_information, "System Information", 0, next_y, bg=ui.Color.dark, fg=ui.Color.white,
        width=RIGHT_ASIDE_LABEL_WIDTH)
    next_y += 24
    ui.draw_label(frame_view_system_information, "Loading...", 10, next_y, bg=ui.Color.white, fg=ui.Color.info)

    if 'system_information' in tool_context[ID].keys():
        __system_information = tool_context[ID]['system_information']
        get_system_information(frame_view_system_information)
    else:
        threading.Thread(target=get_system_information, args=(frame_view_system_information,)).start()


##
# @brief        Exposed API. Destroys all the controls of GTA grids view.
#               Called by main.py change_view() or reset() functions
# @param[in]    master_frame, from main.py
# @param[in]    controls, main.py global controls dictionary
def destroy(master_frame, controls):
    global tool_context
    global local_controls
    global active_platform
    global active_os
    global active_grid
    global active_test
    global __system_information

    try:
        filtered_controls = [control for control in controls.keys() if ID in control]
        for control_name in filtered_controls:
            controls[control_name][0].destroy()
    except Exception as e:
        print(e)

    local_controls = {}
    active_platform = None
    active_os = None
    active_grid = None
    __system_information = None
    # del tool_context[ID]
    # context.store(tool_context)
    active_test = None


##
# @brief        Internal helper function to break the text in lines.
#               Required to arrange text in given width.
# @param[in]    text
# @param[in]    n, breaking position in number of characters
def break_text(text, n):
    lines = [text[i:i + n] for i in range(0, len(text), n)]
    return ['\n'.join(lines), len(lines)]


##
# @brief        Internal helper function to get and add system information to GTA grids view.
#               Called in a separate thread by init()
# @param[in]    master_frame, from main.py
# @todo         Add WDTF and Connected Standby information in System Information
def get_system_information(master_frame):
    global tool_context
    global __system_information

    if __system_information is None:
        __system_information = {}
        print("Getting system information")
        from Libs.Core.machine_info.machine_info import SystemInfo, SystemDriverType
        # from Libs import display_power
        info = SystemInfo()
        info._get_system_info()
        __system_information['platform_name'] = info.get_gfx_display_hardwareinfo()[0].DisplayAdapterName
        __system_information['os'] = break_text(info.sys_info.OSInfo.OSName, 30)
        __system_information['bios'] = break_text(info.sys_info.BIOSVersion, 30)
        igfx_info = info.get_driver_info(SystemDriverType.GFX)
        if igfx_info is not None:
            __system_information['graphics_driver'] = break_text("{0} [{1}]".format(
                igfx_info.DriverInfo[0].DriverDescription,
                igfx_info.DriverInfo[0].DriverVersion), 30)
        else:
            __system_information['graphics_driver'] = ["Not Installed", 1]
        val_sim_info = info.get_driver_info(SystemDriverType.VALSIM)
        if val_sim_info is not None:
            __system_information['GfxValSimDriver'] = break_text("{0} [{1}]".format(
                val_sim_info.DriverInfo[0].DriverDescription, val_sim_info.DriverInfo[0].DriverVersion), 30)
        else:
            __system_information['GfxValSimDriver'] = ["Not Installed", 1]

        tool_context[ID]['system_information'] = __system_information
        context.store(tool_context)

    base_y = 0
    base_x = 0
    ui.draw_label(master_frame, "Platform", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white, width=24)
    base_y += 24
    ui.draw_label(master_frame, __system_information['platform_name'][0], base_x, base_y, bg=ui.Color.white)

    base_y += 24
    ui.draw_label(
        master_frame, "OS", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white, width=RIGHT_ASIDE_LABEL_WIDTH)
    base_y += 24
    ui.draw_label(master_frame, __system_information['os'][0], base_x, base_y, bg="white", justify=tkinter.LEFT)

    base_y += (__system_information['os'][1] * 24)
    ui.draw_label(
        master_frame, "BIOS", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white, width=RIGHT_ASIDE_LABEL_WIDTH)
    ui.draw_label(master_frame, __system_information['bios'][0], base_x, base_y + 24, bg="white", justify=tkinter.LEFT)

    base_y += (__system_information['bios'][1] * 30)
    ui.draw_label(
        master_frame, "Graphics Driver", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white,
        width=RIGHT_ASIDE_LABEL_WIDTH)
    ui.draw_label(
        master_frame, __system_information['graphics_driver'][0], base_x, base_y + 24, bg="white", justify=tkinter.LEFT)

    base_y += (__system_information['graphics_driver'][1] * 24) + 24
    ui.draw_label(
        master_frame, "GfxValSimDriver", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white,
        width=RIGHT_ASIDE_LABEL_WIDTH)
    ui.draw_label(
        master_frame, __system_information['GfxValSimDriver'][0], base_x, base_y + 24, bg="white", justify=tkinter.LEFT)

    # base_y += (__system_information['GfxValSimDriver'][1]*24)+24
    # ui.draw_label(
    #     master_frame, "WDTF", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white, width=RIGHT_ASIDE_LABEL_WIDTH)
    # ui.draw_label(
    #     master_frame, "Not Available", base_x, base_y+24, bg="white", justify=LEFT)
    #
    # base_y += (__system_information['GfxValSimDriver'][1]*24)+24
    # ui.draw_label(master_frame, "Connected Standby", base_x, base_y, bg=ui.Color.dark, fg=ui.Color.white,
    #                 width=RIGHT_ASIDE_LABEL_WIDTH)
    # ui.draw_label(master_frame, "Not Available", base_x, base_y+24, bg="white", justify=LEFT)


##
# @brief        Attached action method with platform select box.
#               Validate the selection and add the OS select box.
# @param[in]    selected_index, index of selected platform from select box options
# @param[in]    next_x, starting x position of the next component
# @param[in]    frame_view_grid, frame object for grid view
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
def action_select_box_platform(selected_index, next_x, frame_view_grid, master_frame, frame_width, frame_height,
                               view_start_x, view_start_y):
    global active_platform
    global active_os
    global active_grid
    global local_controls
    global tool_context

    tool_context = context.get()
    controls = local_controls

    select_box = controls[ID + 'select_box_platform'][0]
    select_box_variable = controls[ID + 'select_box_platform'][1]
    selected_platform = select_box_variable.get()
    if selected_platform == active_platform:
        return
    active_platform = selected_platform
    if ID + 'select_box_os' in controls.keys():
        controls[ID + 'select_box_os'][0].destroy()
        controls[ID + 'select_box_os_label'][0].destroy()
        controls.pop(ID + 'select_box_os', None)
        controls.pop(ID + 'select_box_os_label', None)
        active_os = None
        if 'active_os' in tool_context[ID].keys():
            del tool_context[ID]['active_os']
            context.store(tool_context)

    if ID + 'select_box_grid' in controls.keys():
        controls[ID + 'select_box_grid'][0].destroy()
        controls[ID + 'select_box_grid_label'][0].destroy()
        controls.pop(ID + 'select_box_grid', None)
        controls.pop(ID + 'select_box_grid_label', None)
        active_grid = None
        if 'active_grid' in tool_context[ID].keys():
            del tool_context[ID]['active_grid']
            context.store(tool_context)

    if ID + 'frame_test_list' in controls.keys():
        controls[ID + 'frame_test_list'][0].destroy()
        controls.pop(ID + 'frame_test_list', None)

    if selected_platform == 'None':
        return

    ##
    # Update Current Session Stats in Main Frame
    if MAIN_ID + 'session_title_label' in controls.keys():
        controls[MAIN_ID + 'session_title_label'][0].config(text='[{0}]'.format(selected_platform))
        controls[MAIN_ID + 'session_total_label'][0].config(text="")
        controls[MAIN_ID + 'session_passed_label'][0].config(text="")
        controls[MAIN_ID + 'session_failed_label'][0].config(text="")

    tool_context[ID]['active_platform'] = active_platform
    tool_context['title'] = "[{0}]".format(active_platform)
    tool_context['total'] = ''
    tool_context['passed'] = ''
    tool_context['failed'] = ''
    context.store(tool_context)

    target_os_list = ['None'] + parser.get_gta_os(selected_platform)
    if 'active_os' in tool_context[ID].keys():
        temp = parser.get_gta_os(selected_platform)
        temp.remove(tool_context[ID]['active_os'])
        target_os_list = [tool_context[ID]['active_os'], 'None'] + temp

    f = partial(
        action_select_box_os, next_x=next_x, frame_view_grid=frame_view_grid, master_frame=master_frame,
        frame_width=frame_width, frame_height=frame_height, view_start_x=view_start_x, view_start_y=view_start_y)
    f.__name__ = "action_select_box_os"
    next_x += 130
    controls[ID + 'select_box_os_label'] = ui.draw_label(frame_view_grid, "OS", next_x, 20, bg=ui.Color.white)
    controls[ID + 'select_box_os'] = ui.draw_select_box(
        frame_view_grid, next_x, 45, target_os_list, f)
    controls[ID + 'select_box_os'][0].config(
        bg=ui.Color.light, activebackground=ui.Color.dark, fg=ui.Color.dark, activeforeground=ui.Color.white,
        bd=0, highlightthickness=0, relief=tkinter.FLAT)

    if 'active_os' in tool_context[ID].keys():
        action_select_box_os(
            0, next_x, frame_view_grid, master_frame, frame_width, frame_height, view_start_x, view_start_y)


##
# @brief        Attached action method with OS select box.
#               Validate the selection and add the grids select box.
# @param[in]    selected_index, index of selected os from select box options
# @param[in]    next_x, starting x position of the next component
# @param[in]    frame_view_grid, frame object for grid view
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
def action_select_box_os(selected_index, next_x, frame_view_grid, master_frame, frame_width, frame_height, view_start_x,
                         view_start_y):
    global tool_context
    global active_platform
    global active_os
    global active_grid
    global local_controls

    tool_context = context.get()
    controls = local_controls

    select_box = controls[ID + 'select_box_os'][0]
    select_box_variable = controls[ID + 'select_box_os'][1]
    selected_os = select_box_variable.get()
    if selected_os == active_os:
        return
    active_os = selected_os
    if ID + 'select_box_grid' in controls.keys():
        controls[ID + 'select_box_grid'][0].destroy()
        controls[ID + 'select_box_grid_label'][0].destroy()
        controls.pop(ID + 'select_box_grid', None)
        controls.pop(ID + 'select_box_grid_label', None)
        active_grid = None
        if 'active_grid' in tool_context[ID].keys():
            del tool_context[ID]['active_grid']
            context.store(tool_context)

    if ID + 'frame_test_list' in controls.keys():
        controls[ID + 'frame_test_list'][0].destroy()
        controls.pop(ID + 'frame_test_list', None)

    if selected_os == 'None':
        return

    ##
    # Update Current Session Stats in Main Frame
    if MAIN_ID + 'session_title_label' in controls.keys():
        controls[MAIN_ID + 'session_title_label'][0].config(text='[{0}] [{1}]'.format(active_platform, active_os))
        controls[MAIN_ID + 'session_total_label'][0].config(text="")
        controls[MAIN_ID + 'session_passed_label'][0].config(text="")
        controls[MAIN_ID + 'session_failed_label'][0].config(text="")

    tool_context[ID]['active_os'] = active_os
    tool_context['title'] = "[{0}] [{1}]".format(active_platform, active_os)
    tool_context['total'] = ''
    tool_context['passed'] = ''
    tool_context['failed'] = ''
    context.store(tool_context)

    target_grid_list = ['None'] + parser.get_gta_grids(active_platform, selected_os)
    if 'active_grid' in tool_context[ID].keys():
        temp = parser.get_gta_grids(active_platform, active_os)
        temp.remove(tool_context[ID]['active_grid'])
        target_grid_list = [tool_context[ID]['active_grid'], 'None'] + temp

    f = partial(
        action_select_box_grid, master_frame=master_frame, frame_width=frame_width, frame_height=frame_height,
        view_start_x=view_start_x, view_start_y=view_start_y)
    f.__name__ = "action_select_box_grid"
    next_x += 130
    controls[ID + 'select_box_grid_label'] = ui.draw_label(frame_view_grid, "Grid", next_x, 20, bg=ui.Color.white)
    controls[ID + 'select_box_grid'] = ui.draw_select_box(
        frame_view_grid, next_x, 45, target_grid_list, f)
    controls[ID + 'select_box_grid'][0].config(
        bg=ui.Color.light, activebackground=ui.Color.dark, fg=ui.Color.dark, activeforeground=ui.Color.white,
        bd=0, highlightthickness=0, relief=tkinter.FLAT)

    if 'active_grid' in tool_context[ID].keys():
        action_select_box_grid(0, master_frame, frame_width, frame_height, view_start_x, view_start_y)


##
# @brief        Attached action method with grid select box.
#               Validate the selection and add the test list
# @param[in]    selected_index, index of selected grid from select box options
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
def action_select_box_grid(selected_index, master_frame, frame_width, frame_height, view_start_x, view_start_y):
    global tool_context
    global active_platform
    global active_os
    global active_grid
    global local_controls
    global test_list_canvas

    tool_context = context.get()
    controls = local_controls

    select_box = controls[ID + 'select_box_grid'][0]
    select_box_variable = controls[ID + 'select_box_grid'][1]
    selected_grid = select_box_variable.get()
    if selected_grid == active_grid:
        return
    active_grid = selected_grid

    if ID + 'frame_test_list' in controls.keys():
        controls[ID + 'frame_test_list'][0].destroy()
        controls.pop(ID + 'frame_test_list', None)

    test_list = parser.get_gta_tests(active_platform, active_os, active_grid)

    ##
    # Update Current Session Stats in Main Frame
    passed = 0
    failed = 0
    if 'test_results' in tool_context[ID].keys():
        test_ids = tool_context[ID]['test_results'].keys()
        for t_id in test_ids:
            if t_id in test_list.keys():
                if tool_context[ID]['test_results'][t_id]['text'] == 'PASSED':
                    passed += 1
                else:
                    failed += 1

    if MAIN_ID + 'session_title_label' in controls.keys():
        controls[MAIN_ID + 'session_title_label'][0].config(
            text='[{0}] [{1}] [{2}]'.format(active_platform, active_os, active_grid))
        controls[MAIN_ID + 'session_total_label'][0].config(text="Total: {0}".format(len(test_list.keys())))
        controls[MAIN_ID + 'session_passed_label'][0].config(text="Passed: {0}".format(passed))
        controls[MAIN_ID + 'session_failed_label'][0].config(text="Failed: {0}".format(failed))

    tool_context[ID]['active_grid'] = active_grid
    tool_context['title'] = "[{0}] [{1}] [{2}]".format(active_platform, active_os, active_grid)
    tool_context['total'] = 'Total: {0}'.format(len(test_list.keys()))
    tool_context['passed'] = 'Passed: {0}'.format(passed)
    tool_context['failed'] = 'Failed: {0}'.format(failed)
    context.store(tool_context)

    if 'active_test' in tool_context[ID].keys():
        action_check_button_test(
            master_frame, frame_width, frame_height, view_start_x, view_start_y, tool_context[ID]['active_test'],
            test_list[tool_context[ID]['active_test']])
    else:
        test_list_frame = tkinter.Frame(master_frame)
        controls[ID + 'frame_test_list'] = [test_list_frame, view_start_x + 20, view_start_y + 100]
        test_list_frame.place(x=view_start_x + 20, y=view_start_y + 100)
        test_list_canvas = tkinter.Canvas(test_list_frame,
                                          width=frame_width - view_start_x - RIGHT_ASIDE_WIDTH - 50,
                                          height=frame_height - view_start_y - 120,
                                          bg=ui.Color.white,
                                          highlightthickness=0)
        test_list_scroll_frame = tkinter.Frame(test_list_canvas, bg=ui.Color.white)
        test_list_scrollbar = tkinter.Scrollbar(test_list_frame, orient="vertical", command=test_list_canvas.yview)
        test_list_canvas.configure(yscrollcommand=test_list_scrollbar.set)
        test_list_scrollbar.pack(side="right", fill="y")
        test_list_canvas.pack(side="left")
        test_list_canvas.create_window((0, 0), window=test_list_scroll_frame, anchor='nw')
        test_list_scroll_frame.bind("<Configure>", test_list_canvas_scroll_configure)

        add_test_list(
            test_list_scroll_frame, test_list, master_frame, frame_width, frame_height, view_start_x, view_start_y)


##
# @brief        Attached action method with test list check button
#               Validate the selection and expand the test to show requirements and run button
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
# @param[in]    test_id, selected test id
# @param[in]    test, test object of the selected test. Contains test name, command line etc.
def action_check_button_test(master_frame, frame_width, frame_height, view_start_x, view_start_y, test_id, test):
    global tool_context
    global local_controls
    global active_platform
    global active_os
    global active_test
    global test_list_canvas

    controls = local_controls
    if ID + 'frame_test_list' in controls.keys():
        controls[ID + 'frame_test_list'][0].destroy()
        controls.pop(ID + 'frame_test_list', None)

    test_list_frame = tkinter.Frame(master_frame)
    controls[ID + 'frame_test_list'] = [test_list_frame, view_start_x + 20, view_start_y + 100]
    test_list_frame.place(x=view_start_x + 20, y=view_start_y + 100)
    test_list_canvas = tkinter.Canvas(test_list_frame,
                                      width=frame_width - view_start_x - RIGHT_ASIDE_WIDTH - 50,
                                      height=frame_height - view_start_y - 120,
                                      bg=ui.Color.white,
                                      highlightthickness=0)
    test_list_scroll_frame = tkinter.Frame(test_list_canvas, bg=ui.Color.white)
    test_list_scrollbar = tkinter.Scrollbar(test_list_frame, orient="vertical", command=test_list_canvas.yview)
    test_list_canvas.configure(yscrollcommand=test_list_scrollbar.set)
    test_list_scrollbar.pack(side="right", fill="y")
    test_list_canvas.pack(side="left")
    test_list_canvas.create_window((0, 0), window=test_list_scroll_frame, anchor='nw')
    test_list_scroll_frame.bind("<Configure>", test_list_canvas_scroll_configure)

    if active_test == test_id:
        del tool_context[ID]['active_test']
        context.store(tool_context)
        active_test = None

        test_list = parser.get_gta_tests(active_platform, active_os, active_grid)
        add_test_list(
            test_list_scroll_frame, test_list, master_frame, frame_width, frame_height, view_start_x, view_start_y)
    else:
        active_test = test_id
        tool_context[ID]['active_test'] = active_test
        context.store(tool_context)

        add_test(
            test_list_scroll_frame, test_id, test, master_frame, frame_width, frame_height, view_start_x, view_start_y)


##
# @brief        Attached action method with run button
#               Prepare and run the test command line based on test_id and test
# @param[in]    master_frame, from main.py
# @param[in]    test_id, selected test id
# @param[in]    test, selected test object
def action_button_run_test(master_frame, test_id, test):
    global tool_context
    global local_controls
    global active_platform
    global active_os
    global active_grid

    controls = local_controls

    command_line = test['CommandLine']
    print(command_line)
    master_frame.withdraw()
    os.system(command_line)

    is_logs_available = False
    log_file = None
    if os.path.exists(test_context.LOG_FOLDER):
        for path, sub_dirs, files in os.walk(test_context.LOG_FOLDER):
            for name in files:
                if ".log" in name:
                    is_logs_available = True
                    log_file = os.path.join(test_context.LOG_FOLDER, name)

    corruption_status = False
    result = messagebox.askquestion("Corruption Check", "Did you observe any visual corruption during test?",
                                    icon='warning')
    if result == 'yes':
        corruption_status = True
    if log_file is not None:
        if os.path.exists(log_file):
            with open(log_file, "a") as f:
                f.write("\n\n\nCorruption observed: {0}\n".format(corruption_status))
                if 'IDSID' in tool_context.keys():
                    f.write("User: {0}\n".format(tool_context['IDSID']))

    if 'test_results' not in tool_context[ID].keys():
        tool_context[ID]['test_results'] = {}
    if is_logs_available is False:
        controls[ID + 'label_active_test_result'].config(text="ERROR", fg=ui.Color.danger)
        tool_context[ID]['test_results'][test_id] = {'text': "ERROR", 'fg': ui.Color.danger}
    else:
        with open(log_file, 'r') as f:
            if 'TEST RESULT : PASS' in f.read() and not corruption_status:
                controls[ID + 'label_active_test_result'].config(text="PASSED", fg=ui.Color.success)
                tool_context[ID]['test_results'][test_id] = {'text': "PASSED", 'fg': ui.Color.success}
            else:
                controls[ID + 'label_active_test_result'].config(text="FAILED", fg=ui.Color.danger)
                tool_context[ID]['test_results'][test_id] = {'text': "FAILED", 'fg': ui.Color.danger}

    if os.path.exists(test_context.LOG_FOLDER):
        os.system(
            "rename Logs Logs_" + str(time.time()) + "_" + test_id + "_" +
            tool_context[ID]['test_results'][test_id]['text'])
    master_frame.deiconify()

    test_list = parser.get_gta_tests(active_platform, active_os, active_grid)

    ##
    # Update Current Session Stats in Main Frame
    passed = 0
    failed = 0
    test_ids = tool_context[ID]['test_results'].keys()
    for t_id in test_ids:
        if t_id in test_list.keys():
            if tool_context[ID]['test_results'][t_id]['text'] == 'PASSED':
                passed += 1
            else:
                failed += 1

    if MAIN_ID + 'session_title_label' in controls.keys():
        controls[MAIN_ID + 'session_title_label'][0].config(
            text='[{0}] [{1}] [{2}]'.format(active_platform, active_os, active_grid))
        controls[MAIN_ID + 'session_total_label'][0].config(text="Total: {0}".format(len(test_list.keys())))
        controls[MAIN_ID + 'session_passed_label'][0].config(text="Passed: {0}".format(passed))
        controls[MAIN_ID + 'session_failed_label'][0].config(text="Failed: {0}".format(failed))

    tool_context[ID]['active_grid'] = active_grid
    tool_context['title'] = "[{0}] [{1}] [{2}]".format(active_platform, active_os, active_grid)
    tool_context['total'] = 'Total: {0}'.format(len(test_list.keys()))
    tool_context['passed'] = 'Passed: {0}'.format(passed)
    tool_context['failed'] = 'Failed: {0}'.format(failed)
    context.store(tool_context)


##
# @brief        Helper function to add components for selected test and its requirements
# @param[in]    frame, parent frame
# @param[in]    test_id, selected test id
# @param[in]    test, test object of the selected test. Contains test name, command line etc.
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
def add_test(frame, test_id, test, master_frame, frame_width, frame_height, view_start_x, view_start_y):
    global local_controls
    global active_platform
    global active_os

    controls = local_controls
    row_index = 0
    tkinter.Label(frame, text="Test Name", bg=ui.Color.white, font='Helvetica 12 bold').grid(
        row=row_index, column=0, sticky=tkinter.W)
    tkinter.Label(frame, text="Owner", bg=ui.Color.white, font='Helvetica 12 bold').grid(
        row=row_index, column=1, padx=10)
    # Label(frame, text="Duration", bg=ui.Color.white, font='Helvetica 12 bold').grid(
    #     row=row_index, column=2, padx=10)
    tkinter.Label(frame, text="Result", bg=ui.Color.white, font='Helvetica 12 bold').grid(row=row_index, column=3)
    row_index += 1

    check_button_variable = tkinter.BooleanVar()
    check_button_variable.set(True)
    f = partial(
        action_check_button_test, master_frame=master_frame, frame_width=frame_width, frame_height=frame_height,
        view_start_x=view_start_x, view_start_y=view_start_y, test_id=test_id, test=test)
    f.__name__ = "action_check_button_test"
    tkinter.Checkbutton(
        frame, text=(test['Id'] + ' ' + test['Name']), var=check_button_variable,
        fg=ui.Color.info, bg=ui.Color.white, command=f).grid(
        row=row_index, column=0, sticky=tkinter.W)
    tkinter.Label(frame, text=test['Owner'], bg=ui.Color.white, fg=ui.Color.info).grid(row=row_index, column=1,
                                                                                       sticky=tkinter.W + tkinter.E)
    # Label(frame, text=test['ExecutionTime'], bg=ui.Color.white, fg=ui.Color.info).grid(
    #     row=row_index, column=2, sticky=W+E)

    if 'test_results' in tool_context[ID].keys():
        if test_id in tool_context[ID]['test_results'].keys():
            controls[ID + 'label_active_test_result'] = tkinter.Label(
                frame, text=tool_context[ID]['test_results'][test_id]['text'], bg=ui.Color.white,
                fg=tool_context[ID]['test_results'][test_id]['fg'])
            controls[ID + 'label_active_test_result'].grid(row=row_index, column=3)
            f = partial(
                action_button_run_test, master_frame=master_frame, test_id=test_id, test=test)
            f.__name__ = "action_button_run_test"
            tkinter.Button(frame, text="Re-Run", width=10, command=f, bg=ui.Color.warning,
                           fg=ui.Color.white).grid(row=row_index, column=4, padx=20)
        else:
            controls[ID + 'label_active_test_result'] = tkinter.Label(frame, text='--', bg=ui.Color.white)
            controls[ID + 'label_active_test_result'].grid(row=row_index, column=3)
            f = partial(
                action_button_run_test, master_frame=master_frame, test_id=test_id, test=test)
            f.__name__ = "action_button_run_test"
            tkinter.Button(frame, text="Run", width=10, command=f, bg=ui.Color.success,
                           fg=ui.Color.white).grid(row=row_index, column=4, padx=20)
    else:
        controls[ID + 'label_active_test_result'] = tkinter.Label(frame, text='--', bg=ui.Color.white)
        controls[ID + 'label_active_test_result'].grid(row=row_index, column=3)
        f = partial(
            action_button_run_test, master_frame=master_frame, test_id=test_id, test=test)
        f.__name__ = "action_button_run_test"
        tkinter.Button(frame, text="Run", width=10, command=f, bg=ui.Color.success,
                       fg=ui.Color.white).grid(row=row_index, column=4, padx=20)
    row_index += 1

    tkinter.Label(frame, text="Requirements", bg=ui.Color.white, fg=ui.Color.info, font='Helvetica 12 bold').grid(
        row=row_index, column=0, sticky=tkinter.W, pady=20)
    row_index += 1

    tkinter.Label(frame, text='Platform', bg=ui.Color.white).grid(row=row_index, column=0, sticky=tkinter.W)
    tkinter.Label(frame, text=active_platform, bg=ui.Color.white).grid(row=row_index, column=1)
    row_index += 1

    tkinter.Label(frame, text='OS', bg=ui.Color.white).grid(row=row_index, column=0, sticky=tkinter.W)
    tkinter.Label(frame, text=active_os, bg=ui.Color.white).grid(row=row_index, column=1)
    row_index += 1
    args = test['CommandLine'].strip().split(' ')[2:]
    index = 0
    while index < len(args):
        a = args[index]
        index += 1
        if a[0] == '-':
            tkinter.Label(frame, text=a, bg=ui.Color.white).grid(row=row_index, column=0, sticky=tkinter.W)
            a = args[index]
            if a[0] == '-':
                tkinter.Label(frame, text='', bg=ui.Color.white).grid(row=row_index, column=1)
                row_index += 1
                continue
            index += 1
            if a[0] == "\"":
                while a[-1] != "\"":
                    a += " " + args[index]
                    index += 1
            tkinter.Label(frame, text=a, bg=ui.Color.white).grid(row=row_index, column=1)
        else:
            tkinter.Label(frame, text='', bg=ui.Color.white).grid(row=row_index, column=0, sticky=tkinter.W)
            tkinter.Label(frame, text=a, bg=ui.Color.white).grid(row=row_index, column=1)
        row_index += 1


##
# @brief        Helper function to add components for all tests
# @param[in]    frame, parent frame
# @param[in]    test_id, selected test id
# @param[in]    test, test object of the selected test. Contains test name, command line etc.
# @param[in]    master_frame, from main.py
# @param[in]    frame_width, master frame width
# @param[in]    frame_height, master frame height
# @param[in]    view_start_x, starting x position of view
# @param[in]    view_start_y, starting y position of view
def add_test_list(frame, test_list, master_frame, frame_width, frame_height, view_start_x, view_start_y):
    global tool_context

    test_ids = test_list.keys()
    row_index = 0
    tkinter.Label(frame, text="Test Name", bg=ui.Color.white, font='Helvetica 12 bold').grid(
        row=row_index, column=0, sticky=tkinter.W)
    tkinter.Label(frame, text="Owner", bg=ui.Color.white, font='Helvetica 12 bold').grid(
        row=row_index, column=1, padx=10)
    # Label(frame, text="Duration", bg=ui.Color.white, font='Helvetica 12 bold').grid(
    #     row=row_index, column=2, padx=10)
    tkinter.Label(frame, text="Result", bg=ui.Color.white, font='Helvetica 12 bold').grid(row=row_index, column=3)
    row_index += 1
    for test_id in test_ids:
        check_button_variable = tkinter.IntVar()
        f = partial(
            action_check_button_test, master_frame=master_frame, frame_width=frame_width, frame_height=frame_height,
            view_start_x=view_start_x, view_start_y=view_start_y, test_id=test_id, test=test_list[test_id])
        f.__name__ = "action_check_button_test"
        tkinter.Checkbutton(
            frame, text=(test_list[test_id]['Id'] + ' ' + test_list[test_id]['Name']), variable=check_button_variable,
            fg=ui.Color.black, bg=ui.Color.white, command=f).grid(
            row=row_index, column=0, sticky=tkinter.W)
        tkinter.Label(frame, text=test_list[test_id]['Owner'], bg=ui.Color.white).grid(row=row_index, column=1)
        # Label(frame, text=test_list[test_id]['ExecutionTime'], bg=ui.Color.white).grid(row=row_index, column=2)
        if 'test_results' in tool_context[ID].keys():
            if test_id in tool_context[ID]['test_results'].keys():
                tkinter.Label(
                    frame, text=tool_context[ID]['test_results'][test_id]['text'], bg=ui.Color.white,
                    fg=tool_context[ID]['test_results'][test_id]['fg']).grid(row=row_index, column=3)
            else:
                tkinter.Label(frame, text='--', bg=ui.Color.white).grid(row=row_index, column=3)
        else:
            tkinter.Label(frame, text='--', bg=ui.Color.white).grid(row=row_index, column=3)
        row_index += 1


##
# @brief        Helper function to configure scrolling test list
def test_list_canvas_scroll_configure(event):
    global test_list_canvas
    test_list_canvas.configure(scrollregion=test_list_canvas.bbox("all"))
