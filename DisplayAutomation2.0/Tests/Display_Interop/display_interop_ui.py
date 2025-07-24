###############################################################################################
# @file         display_interop_ui.py
# @brief        Display Interop APP Usage (To RUN Interop suite for more commandlines / custom usage of Interop test )
# @details
#   1. Open command prompt in Admin mode from "Output" root folder and run command "python display_interop_ui.py".
#	2. Display Interop UI / Application will open.
#	3. Select required physically connected displays, Display1, Display2, Display3, if no display is selected it takes default as "DP_A" - which is eDP.
#	4. Select Display Topology like SINGLE or EXTENDED or CLONE, if nothing selected - APP applies all combinations of Topology.
#	5. Select any events like Test Video Clip, Trigger CS/S3/S4, Apply ModeSet, HPD, Test Audio Endpoints, Verify HDCP,
#      Very Cursor, Enable/Disable Gfx Driver, Rotation for each display topology.
#	6. Select "Auto Randomization" based on test needs, which generates all permutation and combinations of Events in each cmd line.
#	7. Click "Repetition" which enables user to enter "No. of Times" to stress the cmd line.
#   8. Select Verifiers, Auto Verify - To Enable DE Verification
#                      Manual Verify - To interact with user at every step.
#                     Minimal Verify - To Verify only UnderRun [Runs bare test without any verifications like DE and Plane]
#   9. Click "Save", will generate required command line and auto append to "run_interop.bat" batch file.
#       [ Note : Generated command line will be shown in log window UI]
#	10. Click "Run" Button to start / Execute all selected test command line one by one.
#		Note : To Review or Edit test command lines present in run_interop.bat batch file from root.
#	11. To reset all fields, click on "Reset" button.
#   12. Logs of each test case generated in "Output" root is renamed and stored as INTEROP_Test_log_1, INTEROP_Test_log_2,.........and so on.
#	13. Click "Clear Log" to clean log window UI.
# CommandLine : python display_interop_ui.py
# An occurrence of underrun leads to failure of test otherwise, test is considered to be passed.
# @authors      Raghupathy, Dushyanth Kumar, Balaji Gurusamy,Sanehadeep Kaur
########################################################################################################################

import copy
import datetime
import os
import sys
import tkinter as ttk
from random import shuffle

from Libs.Core.display_config.display_config import DisplayConfiguration
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.hw_emu.she_utility import SHE_UTILITY, SheDisplayType
from Libs.Core.machine_info.machine_info import SystemInfo

##
# Clearing existed BAT Batch file
batch_file_name = "run_interop.bat"
if os.path.isfile(batch_file_name):
    os.remove(batch_file_name)

with open("run_interop.bat", 'a+') as f:
    f.write("REM ======== TEST SUIT FOR DISPLAY INTEROP ========\n")

display_config = DisplayConfiguration()
machine_info = SystemInfo()
she_utility = SHE_UTILITY()
platform = None
gfx_display_hwinfo = machine_info.get_gfx_display_hardwareinfo()
# WA : currently test are execute on single platform. so loop break after 1 st iteration.
# once Enable MultiAdapter remove the break statement.
for i in range(len(gfx_display_hwinfo)):
    platform = str(gfx_display_hwinfo[i].DisplayAdapterName).lower()
    break

##
# Creating object for TKinter
master = ttk.Tk()
master.cmds_count = 0
master.geometry("380x730")
vbt_title = "Display Interop on {0} Platform".format(platform.upper())
master.title(vbt_title)
master.resizable(0, 0)
master.configure(background="gray97")

##
# Reference X and Y positions
global grefxpos
global grefypos
global random_list
global events

events = 11
random_list = []
grefxpos = 30
grefypos = 15
text_log = ['Log : \n']
var = ttk.IntVar()
Selection = var.get()
var.set(1)

##
# Creating frames for APP
linxpos_s = grefxpos - 20
linypos_s = grefypos + 45
linxpos_e = linxpos_s + 360
linypos_e = linypos_s + 120
canvas = ttk.Canvas(master, bg="white", height=560, width=380)

canvas.create_line(linxpos_s, linypos_s, linxpos_e, linypos_s)
canvas.create_line(linxpos_e, linypos_s, linxpos_e, linypos_e)
canvas.create_line(linxpos_e, linypos_e, linxpos_s, linypos_e)
canvas.create_line(linxpos_s, linypos_e, linxpos_s, linypos_s)
canvas.pack(fill=ttk.BOTH)

linxpos_s = linypos_s = linxpos_e = linypos_e = 0
linxpos_s = grefxpos - 20
linypos_s = grefypos - 30 + 405
linxpos_e = linxpos_s + 360
linypos_e = linypos_s + 30 + 30
canvas.create_line(linxpos_s, linypos_s, linxpos_e, linypos_s)
canvas.create_line(linxpos_e, linypos_s, linxpos_e, linypos_e)
canvas.create_line(linxpos_e, linypos_e, linxpos_s, linypos_e)
canvas.create_line(linxpos_s, linypos_e, linxpos_s, linypos_s)
canvas.pack(fill=ttk.BOTH)

##
# Variable Initialisation
OPTIONS_displays_re = []
OPTIONS_displays_re_SHE = []
OPTIONS_displays = ["NONE"]
OPTIONS_displays_SHE = ["NONE"]
she_utility.intialize()
enumerated_displays = display_config.get_enumerated_display_info()
for i in range(enumerated_displays.Count):
    display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
    OPTIONS_displays.append(display_port)
SHE_port_connected = she_utility.port
SHE_enumerated_displays = she_utility.emu_port_id(SHE_port_connected)
for i in range(len(SHE_enumerated_displays)):
    enum_port = SheDisplayType(SHE_enumerated_displays[i])
    OPTIONS_displays_SHE.append(enum_port)


##
# @brief        To display live logs in APP
# @return       None
def update_log_list():
    xcurrpos = 5
    ycurrpos = 490
    txtboxwidth = 348
    txtboxheight = 200
    scrbarheight = 20

    scrollbar1 = ttk.Scrollbar(master, orient=ttk.HORIZONTAL)
    scrollbar2 = ttk.Scrollbar(master, orient=ttk.VERTICAL)
    mylist = ttk.Listbox(master, xscrollcommand=scrollbar1.set, yscrollcommand=scrollbar2.set)
    # now = datetime.datetime.now()
    # temp = now.strftime("%H:%M:%S")
    # test_count = 1
    for i in range(0, len(text_log)):
        line = text_log[i]
        if 'Log' in line:
            mylist.insert(ttk.END, "{}".format(line))
        elif 'Info' in line:
            mylist.insert(ttk.END, "{0}".format(line))
        else:
            mylist.insert(ttk.END, "{0}".format(line))
            # test_count += 1

    mylist.place(x=xcurrpos, y=ycurrpos, width=txtboxwidth, height=txtboxheight)

    xcurrpos = xcurrpos + 0
    ycurrpos = ycurrpos + txtboxheight + 1

    scrollbar1.place(x=xcurrpos, y=ycurrpos, width=txtboxwidth, height=scrbarheight)

    xcurrpos = xcurrpos + txtboxwidth + 1
    ycurrpos = ycurrpos - (txtboxheight + 1)

    scrollbar2.place(x=xcurrpos, y=ycurrpos, width=scrbarheight, height=txtboxheight)

    scrollbar1.config(command=mylist.xview)
    scrollbar2.config(command=mylist.yview)


update_log_list()
text_log.append(
    "{} : Info  : Make Sure GfxValSim is Uninstalled\Removed".format(datetime.datetime.now().strftime("%H:%M:%S")))
update_log_list()


##
# @brief        To refresh the selection
# @return       None
def refresh():
    Selection = var.get()
    if Selection == 2:
        variable_2_1_ctrl.configure(state="disabled")
        variable_2_2_ctrl.configure(state="disabled")
        variable_2_3_ctrl.configure(state="disabled")
        c6.configure(state="disabled")
    else:
        variable_2_1_ctrl.configure(state="normal")
        variable_2_2_ctrl.configure(state="normal")
        variable_2_3_ctrl.configure(state="normal")
        c6.configure(state="normal")


##
# @brief        To check whether SHE2.0 tool is connected or not
# @param[in]    *args - Argument List
# @return       None
def is_SHE_tool_Connected(*args):
    appStartPos_x = grefxpos
    appStartPos_y = grefypos - 30
    label = ttk.Label(master, text="Is SHE tool Connected", fg='black', bg='white')
    label.place(x=appStartPos_x - 15, y=appStartPos_y + 20)
    ttk.Radiobutton(master, text="YES", fg='black', bg='white', variable=var, value=1, command=refresh).place(
        x=appStartPos_x - 15, y=appStartPos_y + 40)
    ttk.Radiobutton(master, text="No", fg='black', bg='white', variable=var, value=2, command=refresh).place(
        x=appStartPos_x + 55, y=appStartPos_y + 40)
    Selection = var.get()


is_SHE_tool_Connected()


##
# @brief        To update Display Port 1 in Config frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_d1(*args):
    available_choices = []
    d1_selection = variable_1_1.get()
    d2_selection = variable_1_2.get()
    d3_selection = variable_1_3.get()

    available_choices = copy.copy(OPTIONS_displays)

    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if d1_selection != 'NONE':
        available_choices.remove(d1_selection)
    if d2_selection != 'NONE':
        available_choices.remove(d2_selection)
    if d3_selection != 'NONE':
        available_choices.remove(d3_selection)

    variable_1_2_ctrl['menu'].delete(0, 'end')
    variable_1_3_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_1_2_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_2, choice))
        variable_1_3_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_3, choice))


##
# @brief        To update Display Port 2 in Config frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_d2(*args):
    available_choices = []
    d1_selection = variable_1_1.get()
    d2_selection = variable_1_2.get()
    d3_selection = variable_1_3.get()

    # available_choices = ["NONE", "DP_A", "DP_B", "DP_C", "HDMI_B", "HDMI_C"]
    available_choices = copy.copy(OPTIONS_displays)

    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if d1_selection != 'NONE':
        available_choices.remove(d1_selection)
    if d2_selection != 'NONE':
        available_choices.remove(d2_selection)
    if d3_selection != 'NONE':
        available_choices.remove(d3_selection)

    variable_1_1_ctrl['menu'].delete(0, 'end')
    variable_1_3_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_1_1_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_1, choice))
        variable_1_3_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_3, choice))


##
# @brief        To update Display Port 3 in Config frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_d3(*args):
    available_choices = []
    d1_selection = variable_1_1.get()
    d2_selection = variable_1_2.get()
    d3_selection = variable_1_3.get()

    available_choices = copy.copy(OPTIONS_displays)
    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if d1_selection != 'NONE':
        available_choices.remove(d1_selection)
    if d2_selection != 'NONE':
        available_choices.remove(d2_selection)
    if d3_selection != 'NONE':
        available_choices.remove(d3_selection)

    variable_1_1_ctrl['menu'].delete(0, 'end')
    variable_1_2_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_1_1_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_1, choice))
        variable_1_2_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_1_2, choice))


##
# @brief        To update Emulator Port 1 in Config frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_e1(*args):
    available_choices = []
    e1_selection = variable_2_1.get()
    e2_selection = variable_2_2.get()
    e3_selection = variable_2_3.get()

    available_choices = copy.copy(OPTIONS_displays_SHE)

    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if e1_selection != 'NONE':
        available_choices.remove(e1_selection)
    if e2_selection != 'NONE':
        available_choices.remove(e2_selection)
    if e3_selection != 'NONE':
        available_choices.remove(e3_selection)

    variable_2_2_ctrl['menu'].delete(0, 'end')
    variable_2_3_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_2_2_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_2, choice))
        variable_2_3_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_3, choice))


##
# @brief        To update Emulator Port 2 in Config Frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_e2(*args):
    available_choices = []
    e1_selection = variable_2_1.get()
    e2_selection = variable_2_2.get()
    e3_selection = variable_2_3.get()

    available_choices = copy.copy(OPTIONS_displays_SHE)

    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if e1_selection != 'NONE':
        available_choices.remove(e1_selection)
    if e2_selection != 'NONE':
        available_choices.remove(e2_selection)
    if e3_selection != 'NONE':
        available_choices.remove(e3_selection)

    variable_2_1_ctrl['menu'].delete(0, 'end')
    variable_2_3_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_2_1_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_1, choice))
        variable_2_3_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_3, choice))


##
# @brief        To update Emulator Port 3 in Config Frame
# @param[in]    *args - Argument List
# @return       None
def update_ports_e3(*args):
    available_choices = []
    e1_selection = variable_2_1.get()
    e2_selection = variable_2_2.get()
    e3_selection = variable_2_3.get()

    available_choices = copy.copy(OPTIONS_displays_SHE)

    if "NONE" not in available_choices:
        available_choices.append("NONE")

    if e1_selection != 'NONE':
        available_choices.remove(e1_selection)
    if e2_selection != 'NONE':
        available_choices.remove(e2_selection)
    if e3_selection != 'NONE':
        available_choices.remove(e3_selection)

    variable_2_1_ctrl['menu'].delete(0, 'end')
    variable_2_2_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        variable_2_1_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_1, choice))
        variable_2_2_ctrl['menu'].add_command(label=choice, command=ttk._setit(variable_2_2, choice))


##
# @brief        APP Initialisation
# @param[in]    *args - Argument List
# @return       None
def display_port_field_init(*args):
    OPTIONS_displays_re = []

    OPTIONS_displays_re = copy.copy(OPTIONS_displays)

    if "NONE" not in OPTIONS_displays_re:
        OPTIONS_displays_re.append("NONE")

    variable_1_1.set("NONE")
    variable_1_2.set("NONE")
    variable_1_3.set("NONE")

    variable_1_1_ctrl['menu'].delete(0, 'end')
    variable_1_2_ctrl['menu'].delete(0, 'end')
    variable_1_3_ctrl['menu'].delete(0, 'end')

    for port in OPTIONS_displays_re:
        variable_1_1_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_1_1, port))
        variable_1_2_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_1_2, port))
        variable_1_3_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_1_3, port))

    variable_1_1.trace('w', update_ports_d1)
    variable_1_2.trace('w', update_ports_d2)
    variable_1_3.trace('w', update_ports_d3)


##
# @brief        Emulator Port Field Initialisation
# @param[in]    *args - Argument List
# @return       None
def emulator_port_field_init(*args):
    OPTIONS_displays_re_SHE = []

    OPTIONS_displays_re_SHE = copy.copy(OPTIONS_displays_SHE)

    if "NONE" not in OPTIONS_displays_re_SHE:
        OPTIONS_displays_re_SHE.append("NONE")

    variable_2_1.set("NONE")
    variable_2_2.set("NONE")
    variable_2_3.set("NONE")

    variable_2_1_ctrl['menu'].delete(0, 'end')
    variable_2_2_ctrl['menu'].delete(0, 'end')
    variable_2_3_ctrl['menu'].delete(0, 'end')

    for port in OPTIONS_displays_re_SHE:
        variable_2_1_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_2_1, port))
        variable_2_2_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_2_2, port))
        variable_2_3_ctrl['menu'].add_command(label=port, command=ttk._setit(variable_2_3, port))

    variable_2_1.trace('w', update_ports_e1)
    variable_2_2.trace('w', update_ports_e2)
    variable_2_3.trace('w', update_ports_e3)


##
# Creating Labels and Buttons for required fields in APP
appStartPos_x = grefxpos
appStartPos_y = grefypos - 30

# Display 1 Port Selection
lable1_1 = ttk.Label(master, text="Device 1", fg='black', bg='white')
lable1_1.place(x=appStartPos_x + 12, y=appStartPos_y + 65)
variable_1_1 = ttk.StringVar(master)
variable_1_1.set(OPTIONS_displays[0])  # default value
variable_1_1_ctrl = ttk.OptionMenu(master, variable_1_1, *OPTIONS_displays)
variable_1_1_ctrl.place(x=appStartPos_x, y=appStartPos_y + 95)

# Display 2 Port Selection
lable1_2 = ttk.Label(master, text="Device 2", fg='black', bg='white')
lable1_2.place(x=appStartPos_x + 132, y=appStartPos_y + 65)
variable_1_2 = ttk.StringVar(master)
variable_1_2.set(OPTIONS_displays[0])  # default value
variable_1_2_ctrl = ttk.OptionMenu(master, variable_1_2, *OPTIONS_displays)
variable_1_2_ctrl.place(x=appStartPos_x + 120, y=appStartPos_y + 95)

# Display 3 Port Selection
lable1_3 = ttk.Label(master, text="Device 3", fg='black', bg='white')
lable1_3.place(x=appStartPos_x + 252, y=appStartPos_y + 65)
variable_1_3 = ttk.StringVar(master)
variable_1_3.set(OPTIONS_displays[0])  # default value
variable_1_3_ctrl = ttk.OptionMenu(master, variable_1_3, *OPTIONS_displays)
variable_1_3_ctrl.place(x=appStartPos_x + 240, y=appStartPos_y + 95)

# Emulator 1 Port Selection
variable_2_1 = ttk.StringVar(master)
variable_2_1.set(OPTIONS_displays_SHE[0])  # default value
variable_2_1_ctrl = ttk.OptionMenu(master, variable_2_1, *OPTIONS_displays_SHE)
variable_2_1_ctrl.place(x=appStartPos_x, y=appStartPos_y + 135)

# Emulator 2 Port Selection
variable_2_2 = ttk.StringVar(master)
variable_2_2.set(OPTIONS_displays_SHE[0])  # default value
variable_2_2_ctrl = ttk.OptionMenu(master, variable_2_2, *OPTIONS_displays_SHE)
variable_2_2_ctrl.place(x=appStartPos_x + 120, y=appStartPos_y + 135)

# Emulator 3 port Selection
variable_2_3 = ttk.StringVar(master)
variable_2_3.set(OPTIONS_displays_SHE[0])  # default value
variable_2_3_ctrl = ttk.OptionMenu(master, variable_2_3, *OPTIONS_displays_SHE)
variable_2_3_ctrl.place(x=appStartPos_x + 240, y=appStartPos_y + 135)


##
# @brief        Checkbox Update
# @return       None
def update_checkbox1():
    if check_box_var1.get():
        random_list.append('1')
        text_log.append("{} : Info  : Selected Test Video\Audio".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append(
            "{} : Info  : De-Selected Test Video\Audio".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Checkbox Update
# @return       None
def update_checkbox2():
    check_box_var3.set(0)
    if check_box_var2.get():
        random_list.append('5')
        text_log.append("{} : Info  : CS Selected, Disabled S3".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : CS De-Selected".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Checkbox Update
# @return       None
def update_checkbox3():
    check_box_var2.set(0)
    if check_box_var3.get():
        random_list.append('6')
        text_log.append("{} : Info  : S3  Selected, Disabled CS".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : S3 De-Selected".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Checkbox Update
# @return       None
def update_checkbox4():
    if check_box_var4.get():
        random_list.append('7')
        text_log.append("{} : Info  : S4 Selected".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : S4 De-Selected".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Checkbox Update
# @return       None
def update_checkbox5():
    if check_box_var5.get():
        random_list.append('3')
        text_log.append("{} : Info  : Selected Test ModeSet".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test ModeSet".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Checkbox Update
# @return       None
def update_checkbox6():
    if check_box_var6.get():
        random_list.append('10')
        text_log.append("{} : Info  : Selected Test HPD (Unplug and Plug Display,if SHE tool Connected)".format(
            datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test HPD".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Check Audio Update
# @return       None
def update_check_audio():
    if check_box_var7.get():
        random_list.append('2')
        text_log.append(
            "{} : Info  : Selected Test Audio Endpoints".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append(
            "{} : Info  : De-Selected Test Audio Endpoints".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Update Check HDCP
# @return       None
def update_check_hdcp():
    if check_box_var8.get():
        random_list.append('9')
        text_log.append("{} : Info  : Selected Test HDCP".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test HDCP".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Verify Cursor Update
# @return       None
def update_verify_cursor():
    if check_box_var10.get():
        random_list.append('4')
        text_log.append("{} : Info  : Selected Test Cursor".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test Cursor".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Update Enable Disable
# @return       None
def update_enable_disable():
    if check_box_var12.get():
        random_list.append('11')
        text_log.append("{} : Info  : Selected Test GFX Driver (Disable and Enable)".format(
            datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test GFX Driver (Disable and Enable)".format(
            datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Rotation Update
# @return       None
def update_rotation():
    if check_box_var13.get():
        random_list.append('8')
        text_log.append("{} : Info  : Selected Test Rotation".format(datetime.datetime.now().strftime("%H:%M:%S")))
    else:
        text_log.append("{} : Info  : De-Selected Test Rotation".format(datetime.datetime.now().strftime("%H:%M:%S")))
    update_log_list()


##
# @brief        Single Checkbox Update
# @return       None
def update_check_box_single():
    if check_box_single.get():
        text_log.append(
            "{} : Info  : Selected Set Config SINGLE Display".format(datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Checkbox Update Extend
# @return       None
def update_check_box_extend():
    if check_box_extend.get():
        text_log.append(
            "{} : Info  : Selected Set Config EXTENDED Display".format(datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Checkbox Update Clone
# @return       None
def update_check_box_clone():
    if check_box_clone.get():
        text_log.append(
            "{} : Info  : Selected Set Config CLONE Display".format(datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Auto Verify Update
# @return       None
def update_auto_verify():
    if check_box_auto_verify.get():
        check_box_minimal_verify.set(0)
        text_log.append("{} : Info  : Enabled DE Verification".format(datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Update Manual Verify
# @return       None
def update_manual_verify():
    if check_box_manual_verify.get():
        check_box_minimal_verify.set(0)
        text_log.append("{} : Info  : Enabled Manual Verification which needs User Input".format(
            datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Minimal Update verify
# @return       None
def update_minimal_verify():
    if check_box_minimal_verify.get():
        check_box_auto_verify.set(0)
        check_box_manual_verify.set(0)
        text_log.append(
            "{} : Info  : Enabled only UnderRun Verification".format(datetime.datetime.now().strftime("%H:%M:%S")))
        update_log_list()


##
# @brief        Auto Random Update
# @return       None
def update_auto_random():
    if check_box_var9.get():
        check_box_var1.set(0)
        check_box_var2.set(0)
        check_box_var3.set(0)
        check_box_var4.set(0)
        check_box_var5.set(0)
        check_box_var6.set(0)
        check_box_var7.set(0)
        check_box_var8.set(0)
        check_box_var10.set(0)
        check_box_var11.set(0)
        check_box_var12.set(0)
        check_box_var13.set(0)

        x = [i for i in range(1, int(events) + 1)]
        for i in range(1, int(events) + 1):
            del random_list[:]
            shuffle(x)
            for item in x:
                random_list.append(item)
            save_fields()


##
# @brief        Repetition Update
# @return       None
def update_repetition():
    if check_box_var11.get():
        check_box_var9.set(0)
        enter_data = ttk.Entry(master, width=5, background="khaki", bg="white", textvariable=val)
        enter_data.place(x=appStartPos_x + 300, y=appStartPos_y + 372)


check_box_single = ttk.IntVar()
check_box_extend = ttk.IntVar()
check_box_clone = ttk.IntVar()

check_box_var1 = ttk.IntVar()
check_box_var2 = ttk.IntVar()
check_box_var3 = ttk.IntVar()
check_box_var4 = ttk.IntVar()
check_box_var5 = ttk.IntVar()
check_box_var6 = ttk.IntVar()
check_box_var7 = ttk.IntVar()

check_box_var8 = ttk.IntVar()
check_box_var9 = ttk.IntVar()
check_box_var10 = ttk.IntVar()
check_box_var11 = ttk.IntVar()
check_box_var12 = ttk.IntVar()
check_box_var13 = ttk.IntVar()

check_box_var14 = ttk.IntVar()
check_box_var15 = ttk.IntVar()
check_box_var16 = ttk.IntVar()

check_box_auto_verify = ttk.IntVar()
check_box_manual_verify = ttk.IntVar()
check_box_minimal_verify = ttk.IntVar()

c_single = ttk.Checkbutton(master, text="SINGLE", variable=check_box_single, bg="white",
                           command=update_check_box_single)
c_single.place(x=appStartPos_x, y=appStartPos_y + 165)

c_extend = ttk.Checkbutton(master, text="EXTENDED", variable=check_box_extend, bg="white",
                           command=update_check_box_extend)
c_extend.place(x=appStartPos_x + 120, y=appStartPos_y + 165)

c_clone = ttk.Checkbutton(master, text="CLONE", variable=check_box_clone, bg="white", command=update_check_box_clone)
c_clone.place(x=appStartPos_x + 240, y=appStartPos_y + 165)

c1 = ttk.Checkbutton(master, text="1. Test VIDEO\AUDIO", variable=check_box_var1, bg="white", command=update_checkbox1)
c1.place(x=appStartPos_x - 20, y=appStartPos_y + 200)

c7 = ttk.Checkbutton(master, text="2. Test AUDIO (ENDPOINT)", variable=check_box_var7, bg="white",
                     command=update_check_audio)
c7.place(x=appStartPos_x - 20, y=appStartPos_y + 220)

c5 = ttk.Checkbutton(master, text="3. Test MODESET (MMM)", variable=check_box_var5, bg="white",
                     command=update_checkbox5)
c5.place(x=appStartPos_x - 20, y=appStartPos_y + 240)

c10 = ttk.Checkbutton(master, text="4. Test CURSOR", variable=check_box_var10, bg="white", command=update_verify_cursor)
c10.place(x=appStartPos_x - 20, y=appStartPos_y + 260)

c2 = ttk.Checkbutton(master, text="5. Test PM CS", variable=check_box_var2, bg="white", command=update_checkbox2)
c2.place(x=appStartPos_x - 20, y=appStartPos_y + 280)

c3 = ttk.Checkbutton(master, text="6. Test PM S3", variable=check_box_var3, bg="white", command=update_checkbox3)
c3.place(x=appStartPos_x - 20, y=appStartPos_y + 300)

c4 = ttk.Checkbutton(master, text="7. Test PM S4", variable=check_box_var4, bg="white", command=update_checkbox4)
c4.place(x=appStartPos_x + 160, y=appStartPos_y + 200)

c13 = ttk.Checkbutton(master, text="8. Test ROTATION (90 Degree)", variable=check_box_var13, bg="white",
                      command=update_rotation)
c13.place(x=appStartPos_x + 160, y=appStartPos_y + 220)

c8 = ttk.Checkbutton(master, text="9. Test HDCP(Type-0\1)", variable=check_box_var8, bg="white",
                     command=update_check_hdcp)
c8.place(x=appStartPos_x + 160, y=appStartPos_y + 240)

c6 = ttk.Checkbutton(master, text="10. Test HPD (Unplug\Plug)", variable=check_box_var6, bg="white",
                     command=update_checkbox6)
c6.place(x=appStartPos_x + 160, y=appStartPos_y + 260)

c12 = ttk.Checkbutton(master, text="11. Test DRIVER (Dis\Enable)", variable=check_box_var12, bg="white",
                      command=update_enable_disable)
c12.place(x=appStartPos_x + 160, y=appStartPos_y + 280)

# c14 = ttk.Checkbutton(master, text="12.", variable = check_box_var14, bg = "white")
# c14.place(x=appStartPos_x+160, y= appStartPos_y + 200)
#
# c15 = ttk.Checkbutton(master, text="13.", variable = check_box_var15, bg = "white")
# c15.place(x=appStartPos_x+160, y= appStartPos_y + 220)
#
# c16 = ttk.Checkbutton(master, text="14.", variable = check_box_var16, bg = "white")
# c16.place(x=appStartPos_x+160, y= appStartPos_y + 240)

# ========
c9 = ttk.Checkbutton(master, text="Auto Randomization", variable=check_box_var9, foreground='blue2', bg="white",
                     command=update_auto_random)
c9.place(x=appStartPos_x - 15, y=appStartPos_y + 407)

val = ttk.IntVar()
ttk.Label(master, text="No. of Times : ", background='white').place(x=appStartPos_x + 210, y=appStartPos_y + 407)

c11 = ttk.Checkbutton(master, text="Repetition", variable=check_box_var11, foreground='red4', bg="white",
                      command=update_repetition)
c11.place(x=appStartPos_x + 120, y=appStartPos_y + 407)

c_auto_verify = ttk.Checkbutton(master, text="DE Verify", variable=check_box_auto_verify, bg="white",
                                command=update_auto_verify)
c_auto_verify.place(x=appStartPos_x - 15, y=appStartPos_y + 437)

c_manual_verify = ttk.Checkbutton(master, text="Manually Verify", variable=check_box_manual_verify, bg='white',
                                  command=update_manual_verify)
c_manual_verify.place(x=appStartPos_x + 95, y=appStartPos_y + 437)

c_minimal_verify = ttk.Checkbutton(master, text="UnderRun Verify", variable=check_box_minimal_verify, bg="white",
                                   command=update_minimal_verify)
c_minimal_verify.place(x=appStartPos_x + 225, y=appStartPos_y + 437)

display_port_field_init()
emulator_port_field_init()


##
# @brief        To clear logs in APP
# @return       None
def clear_log():
    del text_log[:]
    text_log.append('Log : \n')
    update_log_list()


##
# @brief        To Reset fields existed in APP
# @return       None
def reset_options():
    variable_1_1.set(OPTIONS_displays[0])  # default value
    variable_1_2.set(OPTIONS_displays[0])  # default value
    variable_1_3.set(OPTIONS_displays[0])  # default value

    variable_2_1.set(OPTIONS_displays_SHE[0])  # default value
    variable_2_2.set(OPTIONS_displays_SHE[0])  # default value
    variable_2_3.set(OPTIONS_displays_SHE[0])  # default value

    check_box_single.set(0)
    check_box_extend.set(0)
    check_box_clone.set(0)

    check_box_var1.set(0)
    check_box_var2.set(0)
    check_box_var3.set(0)
    check_box_var4.set(0)
    check_box_var5.set(0)
    check_box_var6.set(0)
    check_box_var7.set(0)
    check_box_var8.set(0)
    check_box_var9.set(0)
    check_box_var10.set(0)
    check_box_var11.set(0)
    check_box_var12.set(0)
    check_box_var13.set(0)

    check_box_auto_verify.set(0)
    check_box_manual_verify.set(0)
    check_box_minimal_verify.set(0)

    del random_list[:]
    val.set(0)


##
# @brief        Create command lines for selected displays and events from APP
# @details      Generates batch file with all saved command lines
#               Explore logs in root folder with Test number
# @return       None
def save_fields():
    test_completion_time = 0
    total_time = 0
    displays = []

    variable_topo = "NONE"
    temp_topo_single = "NONE"
    temp_topo_extend = "NONE"
    temp_topo_clone = "NONE"
    variable_7_verfiy = "NONE"
    random_list_type = "NONE"
    temp_auto_verify = "NONE"
    temp_manual_verify = "NONE"
    temp_minimal_verfiy = "NONE"
    she_enum_port = "NONE"

    if variable_2_1.get() != "NONE" or variable_2_2.get() != "NONE" or variable_2_3.get() != "NONE":
        she_enum_port = "-ENMPRT " + variable_2_1.get() + " " + variable_2_2.get() + " " + variable_2_3.get()

    if check_box_auto_verify.get():
        temp_auto_verify = "AUTO"
    if check_box_manual_verify.get():
        temp_manual_verify = "MANL"
    if check_box_minimal_verify.get():
        temp_minimal_verfiy = "MNML"
    if temp_auto_verify != "NONE" or temp_manual_verify != "NONE" or temp_minimal_verfiy != "NONE":
        variable_7_verfiy = "-VRFR " + temp_auto_verify + " " + temp_manual_verify + " " + temp_minimal_verfiy

    if check_box_single.get():
        temp_topo_single = "SD"
    if check_box_extend.get():
        temp_topo_extend = "ED"
    if check_box_clone.get():
        temp_topo_clone = "CD"
    if temp_topo_single != "NONE" or temp_topo_extend != "NONE" or temp_topo_clone != "NONE":
        variable_topo = "-TOPO " + temp_topo_single + " " + temp_topo_extend + " " + temp_topo_clone

    if len(random_list) != 0:
        for item in random_list:
            if str(item) == '1':
                test_completion_time = test_completion_time + 150
            if str(item) == '2' or str(item) == '3' or str(item) == '4':
                test_completion_time = test_completion_time + 60
            if str(item) == '5':
                test_completion_time = test_completion_time + 60
            if str(item) == '6':
                test_completion_time = test_completion_time + 60
            if str(item) == '7':
                test_completion_time = test_completion_time + 60
            if str(item) == '8':
                test_completion_time = test_completion_time + 60
            if str(item) == '9':
                test_completion_time = test_completion_time + 60
            if str(item) == '10':
                test_completion_time = test_completion_time + 60
            if str(item) == '11':
                test_completion_time = test_completion_time + 60

    if variable_1_1.get() == "NONE" and variable_1_2.get() == "NONE" and variable_1_3.get() == "NONE":
        variable_1_1_port = "DP_A"
        total_time = int(60 + test_completion_time)
    else:
        variable_1_1_port = variable_1_1.get()

    if len(random_list) != 0:
        for item in random_list:
            random_list_type = random_list_type + ' ' + str(item)
        random_list_type = "-RNDM " + random_list_type

    if variable_1_1.get() != "NONE":
        displays.append(variable_1_1.get())
    if variable_1_2.get() != "NONE":
        displays.append(variable_1_2.get())
    if variable_1_3.get() != "NONE":
        displays.append(variable_1_3.get())

    if variable_2_1.get() != "NONE":
        displays.append(variable_2_1.get())
    if variable_2_2.get() != "NONE":
        displays.append(variable_2_2.get())
    if variable_2_3.get() != "NONE":
        displays.append(variable_2_3.get())

    ##
    # To display approximate time taken for test
    if len(displays) == 1:
        total_time = int(61 + test_completion_time)
    if len(displays) == 2:
        total_time = int(121 + (3 * test_completion_time))
    if len(displays) == 3:
        total_time = int(121 + (6 * test_completion_time))

    line = "python Tests\Display_Interop\display_interop.py -{0} -{1} -{2} {3} {4} {5} {6} \n".format(variable_1_1_port,
                                                                                                      variable_1_2.get(),
                                                                                                      variable_1_3.get(),
                                                                                                      she_enum_port,
                                                                                                      variable_topo,
                                                                                                      variable_7_verfiy,
                                                                                                      random_list_type)

    temp = line.replace("-NONE", "")
    cmd_line = temp.replace("NONE", "")

    master.cmds_count = master.cmds_count + 1
    log_name = 'rename Logs INTEROP_Test_log_{}\n'.format(master.cmds_count)
    ##
    # Batch file creation with saved command lines
    with open("run_interop.bat", 'a+') as f:
        temp = str(type(val.get()))
        nooftimes = val.get()
        if check_box_var11.get() == 1 and 'int' in temp:
            print(nooftimes)
            for each_time in range(1, nooftimes + 1):
                log_name_rep = 'rename Logs INTEROP_Test_log_{}_{}\n'.format(master.cmds_count, each_time)
                print(cmd_line)
                text_log.append(
                    "{} : Test : {}_{} {}".format(datetime.datetime.now().strftime("%H:%M:%S"), master.cmds_count,
                                                  each_time, cmd_line))
                update_log_list()

                f.write(cmd_line)
                f.write('timeout /t 5\n')
                f.write(log_name_rep)

            total_time_ex = nooftimes * int(total_time / 60)
            time_log = "{} : Info  : Above Test Suit takes approximately {} mins to Complete".format(
                datetime.datetime.now().strftime("%H:%M:%S"), total_time_ex)
            text_log.append(time_log)
            update_log_list()

        else:
            print(cmd_line)
            text_log.append(
                "{} : Test : {} {}".format(datetime.datetime.now().strftime("%H:%M:%S"), master.cmds_count, cmd_line))
            total_time_ex = int(total_time / 60)
            time_log = "{} : Info  : Above Test takes approximately {} mins to Complete".format(
                datetime.datetime.now().strftime("%H:%M:%S"), total_time_ex)
            text_log.append(time_log)
            update_log_list()

            f.write(cmd_line)
            f.write('timeout /t 5\n')
            f.write(log_name)


##
# @brief        Minimizes APP nad starts executing batch file
# @return       None
def run_fields():
    master.wm_state('iconic')
    os.system("run_interop.bat")
    sys.exit()


##
# Buttons to add tests, open bat, reset fields, run batch file
button = ttk.Button(master, text="Clear Log", width=9, command=clear_log)
button.place(x=appStartPos_x - 15, y=appStartPos_y + 470)

button = ttk.Button(master, text="Reset", width=8, command=reset_options)
button.place(x=appStartPos_x + 80, y=appStartPos_y + 470)

button = ttk.Button(master, text="Save", width=8, command=save_fields)
button.place(x=appStartPos_x + 170, y=appStartPos_y + 470)

button = ttk.Button(master, text="Run", width=8, command=run_fields)
button.place(x=appStartPos_x + 260, y=appStartPos_y + 470)

ttk.mainloop()
