###################################################################################################################
# @file         main.py
# @addtogroup   NorthGate
# @brief        Entry point for NorthGate tool.
# @description  This file contains the implementation of master frame for NorthGate tool. Master frame contains a
#               header, a view list and view area.
#
#               Header -> Header is placed at top. It contains Logo, grid name, execution progress details and reset
#               button. Grid name is selected based on selected platform, os and grid in gta_view. Execution progress
#               details contains total number of test cases in the selected grid, with passed and failed count. Reset
#               button is used to clear the current context and restart the tool with default settings.
#
#               View List -> View list is placed in left corner of the frame. It contains a list of available views.
#               For more details on views see @ref gta_grids.py
#
#               View Area -> This is a child frame of master frame, which will change based on selected view from view
#               list.
#
# @author       Rohit Kumar
###################################################################################################################

import sys
import time
import tkinter
from functools import partial

from Libs.manual.modules import alert
from Libs.manual.modules import context
from Libs.manual.modules import ui
from Libs.manual.views import gta_grids

APPLICATION_NAME = "North Gate"
ID = "#MAIN#"  # ID is used to identify all the controls present in main frame
FRAME_WIDTH = 1024  # Default width of master frame
FRAME_HEIGHT = 768  # Default height of master frame
HEADER_HEIGHT = 50  # Default height of top header in master frame
VIEW_LIST_WIDTH = 102  # Default width of left panel containing a list of available views
VIEW_START_X = VIEW_LIST_WIDTH  # View area starting X position
VIEW_START_Y = 50  # View area starting Y position

controls = {}  # Contains all the controls present in the frame
tool_context = {}  # Stores current context of the tool [Selected Platform, selected OS etc..]
active_view = None  # Stores currently active module object

PROCESS_PER_MONITOR_DPI_AWARE = 2


##
# Per monitor DPI aware. The app will check for the DPI when it will be created and adjusts the scale factor whenever
# the DPI changes. The application will not be automatically scaled by the system.
# windll.user32.SetProcessDPIAware(PROCESS_PER_MONITOR_DPI_AWARE)


##
# @brief        Initializes master frame and its components
def init_frame():
    global tool_context

    master_frame = tkinter.Tk()
    master_frame.geometry("{0}x{1}".format(FRAME_WIDTH, FRAME_HEIGHT))
    master_frame.title(APPLICATION_NAME)
    master_frame.resizable(0, 0)
    master_frame.config(bd=0)

    ##
    # Header
    init_frame_header(master_frame)

    ##
    # View List
    # @todo add feature view in the view list
    # init_view_list(master_frame, [gta_grids, m.views.features])
    init_view_list(master_frame, [gta_grids])

    ##
    # View area will be initialized in view

    return master_frame


##
# @brief        Initializes Header in master frame with its components
# @param[in]    frame
def init_frame_header(frame):
    global tool_context
    global controls

    ##
    # Create a Canvas to add any shape in header
    canvas_header = tkinter.Canvas(frame, bg=ui.Color.info, height=HEADER_HEIGHT, width=FRAME_WIDTH,
                                   highlightthickness=0)
    canvas_header.place(x=0, y=0)

    ##
    # Logo
    ui.draw_label(frame, "intel", 20, 10, bg=ui.Color.info, fg=ui.Color.white, font="Sans 18 bold")

    ##
    # Grid name
    if 'title' not in tool_context.keys():
        tool_context['title'] = ""
    controls[ID + 'session_title_label'] = ui.draw_label(
        frame, tool_context['title'], VIEW_LIST_WIDTH, 15, bg=ui.Color.info,
        fg=ui.Color.white, font="Sans 12 bold")

    ##
    # Current execution details
    if 'total' not in tool_context.keys():
        tool_context['total'] = ""
    controls[ID + 'session_total_label'] = ui.draw_label(
        frame, tool_context['total'], FRAME_WIDTH - 420, 15, bg=ui.Color.info, fg=ui.Color.warning,
        font="Sans 12 bold")

    if 'passed' not in tool_context.keys():
        tool_context['passed'] = ""
    controls[ID + 'session_passed_label'] = ui.draw_label(
        frame, tool_context['passed'], FRAME_WIDTH - 320, 15, bg=ui.Color.info, fg=ui.Color.success,
        font="Sans 12 bold")

    if 'failed' not in tool_context.keys():
        tool_context['failed'] = ""
    controls[ID + 'session_failed_label'] = ui.draw_label(
        frame, tool_context['failed'], FRAME_WIDTH - 200, 15, bg=ui.Color.info, fg=ui.Color.danger,
        font="Sans 12 bold")

    ##
    # Reset Button
    ui.draw_button(
        frame, "Reset", 10, FRAME_WIDTH - 100, 13, action_reset_session, bg=ui.Color.danger, fg=ui.Color.white,
        relief=tkinter.FLAT)

    # IDSID
    # @todo Add IDSID in the header for reference
    # ui.draw_label(frame, "rohitku1", FRAME_WIDTH-150, 10, bg=ui.Color.info, fg=ui.Color.white, font="Sans 16")


##
# @brief        Initializes View List in master frame
# @param[in]    frame
# @param[in]    view_list, list of view modules from views package
def init_view_list(frame, view_list):
    global tool_context
    global active_view
    global controls

    ##
    # If active_view is present in tool_context, make that view as active at the time of tool initialization
    if 'active_view' in tool_context.keys():
        for view in view_list:
            if view.__name__ == tool_context['active_view']:
                active_view = view

    ##
    # Create a Canvas to add any shape in view list
    canvas_view_list = tkinter.Canvas(
        frame, bg=ui.Color.dark, height=FRAME_HEIGHT, width=VIEW_LIST_WIDTH, highlightthickness=0)
    canvas_view_list.place(x=0, y=50)

    ##
    # Add views based on view_list
    next_y = HEADER_HEIGHT
    for view in view_list:
        f = partial(action_change_view, frame, view)
        f.__name__ = "action_change_view"
        if active_view is None:
            tool_context[view.ID] = {}
            active_view = view
            tool_context['active_view'] = active_view.__name__
            context.store(tool_context)

            ##
            # Initialize the active view
            init_view(frame, view)

            controls[ID + 'button_view_' + view.NAME] = ui.draw_button(
                frame, view.NAME, 13, 0, next_y, f, bg=ui.Color.black,
                fg=ui.Color.white, overrelief=tkinter.RAISED, relief=tkinter.FLAT)
        else:
            if view.__name__ == active_view.__name__:
                init_view(frame, view)
                controls[ID + 'button_view_' + view.NAME] = ui.draw_button(
                    frame, view.NAME, 13, 0, next_y, f, bg=ui.Color.black,
                    fg=ui.Color.white, overrelief=tkinter.RAISED, relief=tkinter.FLAT)
            else:
                controls[ID + 'button_view_' + view.NAME] = ui.draw_button(
                    frame, view.NAME, 13, 0, next_y, f, bg=ui.Color.dark,
                    fg=ui.Color.white, overrelief=tkinter.RAISED, relief=tkinter.FLAT)
        next_y += 30


##
# @brief        Initializes the given view in view area
# @param[in]    frame
# @param[in]    view
def init_view(frame, view):
    global tool_context
    global controls

    ##
    # Call the init method from view module
    # @note Every view module has init() and destroy() methods
    view.init(frame, controls, VIEW_START_X, VIEW_START_Y, FRAME_WIDTH, FRAME_HEIGHT)


##
# @brief        Attached action method with view list buttons
# @description  action_change_view() changes the active_view by destroying the previous one and initializing the new
#               view
# @param[in]    frame
# @param[in]    view, new view
def action_change_view(frame, view):
    global tool_context
    global active_view
    global controls

    ##
    # To handle the click on active view button
    if active_view.ID == view.ID:
        return

    ##
    # Call the destroy() method from view module
    # @note Every view module has init() and destroy() methods
    active_view.destroy(frame, controls)

    ##
    # Change the button color based on the selection
    controls[ID + 'button_view_' + active_view.NAME][0].config(bg=ui.Color.dark)

    ##
    # Initialize new view
    init_view(frame, view)

    ##
    # Change the active_view value in tool_context and save it
    active_view = view
    tool_context['active_view'] = active_view.__name__
    context.store(tool_context)

    controls[ID + 'button_view_' + active_view.NAME][0].config(bg=ui.Color.black)


##
# @brief        Attached action method with reset button
# @description  action_reset_session() destroys all the active view, deletes the tool context, resets grid name and
#               execution data and start the tool with default values.
def action_reset_session():
    global main_frame
    global tool_context
    global controls
    global active_view

    ##
    # @todo add confirm alert before resetting all the data

    ##
    # Destroy active view
    active_view.destroy(main_frame, controls)
    active_view = None

    ##
    # Delete tool context
    tool_context = {}
    context.store(tool_context)
    context.delete()

    ##
    # Clear control dictionary
    controls = {}

    ##
    # Destroy master frame
    main_frame.destroy()

    ##
    # Wait for 1 second for everything to settle
    time.sleep(1)

    ##
    # Initialize the master frame
    main_frame = init_frame()
    main_frame.mainloop()


if __name__ == '__main__':
    ##
    # Get previously stored tool context
    tool_context = context.get()

    ##
    # @todo: Continue the last test in case of reboot scenario

    ##
    # Otherwise, follow normal initialization sequence
    #
    # Ask user for IDSID before starting the tool
    alert_output = None
    while alert_output is None:
        ##
        # If any IDSID is present in tool_context, confirm. Otherwise ask for new.
        if bool(tool_context) is False or 'IDSID' not in tool_context.keys():
            tool_context = {}
            alert_output = alert.prompt(
                'Please enter your IDSID. Developers may contact you using this ID.', [{'name': 'IDSID'}])
        else:
            alert_output = alert.prompt(
                'Please enter your IDSID. Developers may contact you using this ID.',
                [{'name': 'IDSID', 'value': tool_context['IDSID']}])

        ##
        # Make sure entered IDSID is not None or ''. If it is, exit.
        if alert_output is not None:
            if alert_output['IDSID'] == '':
                alert_output = None
        else:
            sys.exit(0)

    ##
    # Store IDSID for future reference
    tool_context['IDSID'] = alert_output['IDSID']
    context.store(tool_context)

    ##
    # Initialize the master frame
    main_frame = init_frame()
    main_frame.mainloop()
