#####################################################################################################################
# @file     bat_ui.py
# @brief    Python wrapper helper module providing psr verification
# @details  Display BAT APP Usage (To RUN BAT suite for more commandlines / custom usage of BAT test )
# 1. Open command prompt in Admin mode from "Output" root folder and run command "python bat_ui.py".
# 2. Display BAT v1.0 UI / Application will open.
# 3. Select "Display Environmnet" as Simulated or Physical - based on your requirement
#   ( "Simulated" for simulating display panel of tester choice , "Physical" to run test on actual panel connected to Target)
#   Note: Refer "Steps to Install\Uninstall - GfxValSim Driver" for Simualtion of Displays on Yangra.
# 4. Select required displays, Display1, Display2, Display3, if no display is selected it takes default as "DP_A" - which is eDP.
# 5. Select EDID/DPCDs for Display1, Display2, Display3 respectively. ( applicable only when Environment == "Simulated" )
# 6. Select "User Events" based on test needs, from drop down choice.
# #       [ example : 2KClip or 4KClip or BOTH, which will play 2k(MPO1) or 4k(MPO2) or BOTH the video clips].
# 7. Select "Power Events" based on test needs, from drop down choice. [ example : CS S3 S4 etc ]
# 8. Select "Mode Level" based on test needs, from drop down choice.
# #       [ example : MMM (Minimum,Middle,Maximum) for applying Limited modes (L0) and ALL (L1) for applying ALL modes].
# 9. Click "ADD Config Test" which will generate required command line and auto append to "run_bat.bat" batch file.
# #       [ Note : Generated command line will be shown in log window UI]
# 10. Select "Other Tests" for testing additional set of test case [ example : PSR1 and PSR2 tests to run].
# 11. Click "ADD Other Test" which will generate required command line and auto append to "run_bat.bat" batch file.
# 12. Click "Run" Button to start / Execute all selected test command line one by one.
#   Note : To Review or Edit test command lines present in run_bat.bat batch file, Click "Open BAT" button.
# 13. To reset all fields, click on "Reset" button.
# #   14. Logs of each test case generated in "Output" root is renamed and stored as BAT_Test_Logs_1, BAT_Test_Logs_2,.........and so on.
# 15. Click "Clear Log" to clean log window UI.
#   Note : Log window UI will display selected command line along with test count.
# # CommandLine : python bat_ui.py
# # An occurrence of underrun leads to failure of test otherwise, test is considered to be passed.
# @author   Raghupathy, Dushyanth Kumar, Balaji Gurusamy
#####################################################################################################################
import datetime
import os
import sys
import tkinter as ttk
from xml.etree import ElementTree as ET

from Libs.Core.display_config import display_config
from Libs.Core.display_config.display_config_enums import CONNECTOR_PORT_TYPE
from Libs.Core.machine_info.machine_info import SystemInfo
from Libs.Core.test_env import test_environment
from Libs.Core.test_env.test_context import TestContext

is_sim_enabled = False
display_check = False

##
# Clearing existed BAT Batch file
batch_file_name = "run_bat.bat"
if os.path.isfile(batch_file_name):
    os.remove(batch_file_name)
with open("run_bat.bat", 'a+') as f:
    f.write("REM ======== TEST SUIT FOR DISPLAY DEV BAT VERSION 1 ========\n")

##
# Creating object for TKinter
master = ttk.Tk()
master.cmds_count = 0
master.geometry("400x730")
master.title("Display BAT v1.0")
master.resizable(0, 0)
master.configure(background="gray97")

##
# Reference X and Y positions
global grefxpos
global grefypos

grefxpos = 30
grefypos = 15

##
# Creating frames for APP
canvas = ttk.Canvas(master, bg="gray97", height=390 + 80, width=400)
canvas.create_line(10, 5, 390, 5)
canvas.create_line(10, 5, 10, 40)
canvas.create_line(10, 40, 390, 40)
canvas.create_line(390, 5, 390, 40)
canvas.pack(fill=ttk.BOTH)

canvas.create_line(10, 40, 390, 40)
canvas.create_line(10, 40, 10, 190)
canvas.create_line(10, 160, 390, 160)
canvas.create_line(390, 40, 390, 190)
canvas.pack(fill=ttk.BOTH)

canvas.create_line(10, 285, 390, 285)
canvas.create_line(10, 160, 10, 405)
canvas.create_line(10, 407, 390, 407)
canvas.create_line(390, 160, 390, 405)
canvas.pack(fill=ttk.BOTH)

canvas.create_line(10, 407, 390, 407)
canvas.create_line(10, 405, 10, 450)
canvas.create_line(10, 450, 390, 450)
canvas.create_line(390, 405, 390, 450)
canvas.pack(fill=ttk.BOTH)

##
# Creating Objects and Variable Initialisation
test_environment.TestEnvironment.load_dll_module()
enumerated_displays = display_config.DisplayConfiguration().get_enumerated_display_info()
OPTIONS_displays = ["NONE"]
OPTIONS_supported_displays = ["NONE"]

OPTIONS_edid_dpcd_index = ["NONE"]
OPTIONS_edid_dpcd_edp = ["NONE"]
OPTIONS_edid_dpcd_dp = ["NONE"]
OPTIONS_edid_dpcd_hdmi = ["NONE"]
OPTIONS_edid_dpcd_index_dict = {}
text_log = ['Log : \n']

# Getting Panel Index for displays from PanelIndex XML to plug particular EDID/DPCDs
xml_file = os.path.join(TestContext.panel_input_data(), "PanelInputData.xml")
xml_root = ET.parse(xml_file).getroot()
for instance in list(xml_root):
    test = instance.findall('PanelInstance')
    for test_item in test:
        OPTIONS_edid_dpcd_index_dict[test_item.attrib['PanelIndex']] = test_item.attrib['EDID']

for key, value in OPTIONS_edid_dpcd_index_dict.items():
    if key.startswith("EDP"):
        OPTIONS_edid_dpcd_edp.append(value)
    elif key.startswith("DP"):
        OPTIONS_edid_dpcd_dp.append(value)
    elif key.startswith("HDM"):
        OPTIONS_edid_dpcd_hdmi.append(value)

OPTIONS_user_events = ["NONE", "2KClip", "4KClip", "2KClip 4KClip"]
OPTIONS_power_events = ["NONE", "CS", "S3", "S4", "CS S4", "S3 S4"]
OPTIONS_mode_levels = ["NONE", "ALL", "MMM"]
OPTIONS_diplay_connection = ["PHYSICAL", "SIMULATED"]
OTHER_tests = ["Others Tests", "Audio Basic Test", "PSR1 Basic Test", "PSR2 Basic Test", "Virtual Basic Test"]
# For getting GFX Index list and Platform Name
tri_display_platforms = ['SKL', 'KBL', 'GLK', 'CFL', 'ICL', 'LKF', 'ICLLP', 'ICLHP', 'LKF1', 'LKFR']
adapter_dict = TestContext().get_gfx_adapter_details()
platform_name = SystemInfo().get_platform_details(adapter_dict['gfx_0'].deviceID).PlatformName
# For checking four display capability and for setting flag for enabling and disabling fourth display
# according to platform.
if platform_name not in tri_display_platforms:
    quad_display_support = True
else:
    quad_display_support = False
gfx_index_list = adapter_dict.keys()
OPTIONS_displays_re = []


##
# To display live logs in APP
# @return NA
def update_log_list():
    xcurrpos = 5
    ycurrpos = 485
    txtboxwidth = 375
    txtboxheight = 200
    scrbarheight = 20

    scrollbar1 = ttk.Scrollbar(master, orient=ttk.HORIZONTAL)
    scrollbar2 = ttk.Scrollbar(master, orient=ttk.VERTICAL)
    mylist = ttk.Listbox(master, xscrollcommand=scrollbar1.set, yscrollcommand=scrollbar2.set)

    for i in range(0, len(text_log)):
        line = text_log[i]
        if 'Log' in line:
            mylist.insert(ttk.END, "{0}".format(line))
        elif 'Info' in line:
            mylist.insert(ttk.END, "{0}".format(line))
        else:
            mylist.insert(ttk.END, "{0}".format(line))

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


##
# @brief To map EDID orDPCDs to ports for Simulated Displays
# @param[in] ctrl_name
# @param[in] port
# @return NA
def fill_edid_dpcd_data(ctrl_name, port):
    if display_type.get() == "PHYSICAL":
        return
    # To split port name from GFX value
    port = port[7:]

    if ctrl_name == "D1":
        edid1.set(OPTIONS_edid_dpcd_hdmi[0])
        edid1_ctrl['menu'].delete(0, 'end')
        if 'HDMI' in port:
            for panel_index in OPTIONS_edid_dpcd_hdmi:
                edid1_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid1, panel_index))
        elif port == 'DP_A':
            for panel_index in OPTIONS_edid_dpcd_edp:
                edid1_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid1, panel_index))
        elif 'DP' in port:
            for panel_index in OPTIONS_edid_dpcd_dp:
                edid1_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid1, panel_index))

    elif ctrl_name == "D2":
        edid2.set(OPTIONS_edid_dpcd_hdmi[0])
        edid2_ctrl['menu'].delete(0, 'end')
        if 'HDMI' in port:
            for panel_index in OPTIONS_edid_dpcd_hdmi:
                edid2_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid2, panel_index))
        elif port == 'DP_A':
            for panel_index in OPTIONS_edid_dpcd_edp:
                edid2_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid2, panel_index))
        elif 'DP' in port:
            for panel_index in OPTIONS_edid_dpcd_dp:
                edid2_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid2, panel_index))

    elif ctrl_name == "D3":
        edid3.set(OPTIONS_edid_dpcd_hdmi[0])
        edid3_ctrl['menu'].delete(0, 'end')
        if 'HDMI' in port:
            for panel_index in OPTIONS_edid_dpcd_hdmi:
                edid3_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid3, panel_index))
        elif port == 'DP_A':
            for panel_index in OPTIONS_edid_dpcd_edp:
                edid3_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid3, panel_index))
        elif 'DP' in port:
            for panel_index in OPTIONS_edid_dpcd_dp:
                edid3_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid3, panel_index))

    elif ctrl_name == "D4":
        edid4.set(OPTIONS_edid_dpcd_hdmi[0])
        edid4_ctrl['menu'].delete(0, 'end')
        if 'HDMI' in port:
            for panel_index in OPTIONS_edid_dpcd_hdmi:
                edid4_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid4, panel_index))
        elif port == 'DP_A':
            for panel_index in OPTIONS_edid_dpcd_edp:
                edid4_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid4, panel_index))
        elif 'DP' in port:
            for panel_index in OPTIONS_edid_dpcd_dp:
                edid4_ctrl['menu'].add_command(label=panel_index, command=ttk._setit(edid4, panel_index))


##
# @brief To update Display Port 1 in Config frame
# @param[in] args
# @return NA
def update_ports_d1(*args):
    available_choices = []
    d1_selection = display1.get()
    d2_selection = display2.get()
    d3_selection = display3.get()
    d4_selection = display4.get()

    if is_sim_enabled is False:
        for i in range(enumerated_displays.Count):
            display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            gfx_index = str(enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
            port_type = str(enumerated_displays.ConnectedDisplays[i].PortType).upper()
            if 'DP' in str(display_port).upper() and port_type == 'EMBEDDED':
                display_port = 'E' + display_port  # Change display type to EDP
            display_ports = gfx_index.upper() + ' -' + display_port
            available_choices.append(display_ports)
    else:
        for index in gfx_index_list:
            index = index.lower()
            port_dict = display_config.get_supported_ports(index)
            for port in port_dict.keys():
                if 'DP' in port and port_dict[port] == 'EMBEDDED':
                    ports = index.upper() + " -" + 'E' + str(port).upper()  # Change display type to EDP
                else:
                    ports = index.upper() + " -" + port
                OPTIONS_displays_re.append(ports)
    if "NONE" not in available_choices:
        available_choices.append("NONE")
    try:
        if d1_selection != 'NONE':
            available_choices.remove(d1_selection)
        if d2_selection != 'NONE':
            available_choices.remove(d2_selection)
        if d3_selection != 'NONE':
            available_choices.remove(d3_selection)
        if d4_selection != 'NONE':
            available_choices.remove(d4_selection)
    except ValueError:
        pass

    display2_ctrl['menu'].delete(0, 'end')
    display3_ctrl['menu'].delete(0, 'end')
    display4_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        display2_ctrl['menu'].add_command(label=choice, command=ttk._setit(display2, choice))
        display3_ctrl['menu'].add_command(label=choice, command=ttk._setit(display3, choice))
        if quad_display_support:
            display4_ctrl['menu'].add_command(label=choice, command=ttk._setit(display4, choice))

    if d1_selection != 'NONE':
        fill_edid_dpcd_data('D1', d1_selection)
    else:
        edid1.set("NONE")  # default value
        edid1_ctrl['menu'].delete(0, 'end')


##
# @brief To update Display Port 2 in Config frame
# @param[in] args
# @return NA
def update_ports_d2(*args):
    available_choices = []
    d1_selection = display1.get()
    d2_selection = display2.get()
    d3_selection = display3.get()
    d4_selection = display4.get()
    if is_sim_enabled is False:
        for i in range(enumerated_displays.Count):
            display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            gfx_index = str(enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
            port_type = str(enumerated_displays.ConnectedDisplays[i].PortType).upper()
            if 'DP' in str(display_port).upper() and port_type == 'EMBEDDED':
                display_port = 'E' + display_port  # Change display type to EDP
            display_ports = gfx_index.upper() + ' -' + display_port
            available_choices.append(display_ports)
    else:
        for index in gfx_index_list:
            index = index.lower()
            port_dict = display_config.get_supported_ports(index)
            for port in port_dict.keys():
                if 'DP' in port and port_dict[port] == 'EMBEDDED':
                    ports = index.upper() + " -" + 'E' + str(port).upper()  # Change display type to EDP
                else:
                    ports = index.upper() + " -" + port
                OPTIONS_displays_re.append(ports)
    if "NONE" not in available_choices:
        available_choices.append("NONE")
    try:
        if d1_selection != 'NONE':
            available_choices.remove(d1_selection)
        if d2_selection != 'NONE':
            available_choices.remove(d2_selection)
        if d3_selection != 'NONE':
            available_choices.remove(d3_selection)
        if d4_selection != 'NONE':
            available_choices.remove(d4_selection)
    except ValueError:
        pass

    display1_ctrl['menu'].delete(0, 'end')
    display3_ctrl['menu'].delete(0, 'end')
    display4_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        display1_ctrl['menu'].add_command(label=choice, command=ttk._setit(display1, choice))
        display3_ctrl['menu'].add_command(label=choice, command=ttk._setit(display3, choice))
        if quad_display_support:
            display4_ctrl['menu'].add_command(label=choice, command=ttk._setit(display4, choice))

    if d2_selection != 'NONE':
        fill_edid_dpcd_data('D2', d2_selection)
    else:
        edid2.set("NONE")  # default value
        edid2_ctrl['menu'].delete(0, 'end')


##
# @brief To update Display Port 3 in Config frame
# @param[in] args
# @return NA
def update_ports_d3(*args):
    available_choices = []
    d1_selection = display1.get()
    d2_selection = display2.get()
    d3_selection = display3.get()
    d4_selection = display4.get()
    if is_sim_enabled is False:
        for i in range(enumerated_displays.Count):
            display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            gfx_index = str(enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
            port_type = str(enumerated_displays.ConnectedDisplays[i].PortType).upper()
            if 'DP' in str(display_port).upper() and port_type == 'EMBEDDED':
                display_port = 'E' + display_port  # Change display type to EDP
            display_ports = gfx_index.upper() + ' -' + display_port
            available_choices.append(display_ports)
    else:
        for index in gfx_index_list:
            index = index.lower()
            port_dict = display_config.get_supported_ports(index)
            for port in port_dict.keys():
                if 'DP' in port and port_dict[port] == 'EMBEDDED':
                    ports = index.upper() + " -" + 'E' + str(port).upper()  # Change display type to EDP
                else:
                    ports = index.upper() + " -" + port
                OPTIONS_displays_re.append(ports)
    if "NONE" not in available_choices:
        available_choices.append("NONE")
    try:
        if d1_selection != 'NONE':
            available_choices.remove(d1_selection)
        if d2_selection != 'NONE':
            available_choices.remove(d2_selection)
        if d3_selection != 'NONE':
            available_choices.remove(d3_selection)
        if d4_selection != 'NONE':
            available_choices.remove(d4_selection)
    except ValueError:
        pass

    display1_ctrl['menu'].delete(0, 'end')
    display2_ctrl['menu'].delete(0, 'end')
    display4_ctrl['menu'].delete(0, 'end')

    for choice in available_choices:
        display1_ctrl['menu'].add_command(label=choice, command=ttk._setit(display1, choice))
        display2_ctrl['menu'].add_command(label=choice, command=ttk._setit(display2, choice))
        if quad_display_support:
            display4_ctrl['menu'].add_command(label=choice, command=ttk._setit(display4, choice))

    if d3_selection != 'NONE':
        fill_edid_dpcd_data('D3', d3_selection)
    else:
        edid3.set("NONE")  # default value
        edid3_ctrl['menu'].delete(0, 'end')


##
# @brief To update Display Port 4 in Config frame
# @param[in] args
# @return NA
def update_ports_d4(*args):
    available_choices = []
    d1_selection = display1.get()
    d2_selection = display2.get()
    d3_selection = display3.get()
    d4_selection = display4.get()
    if is_sim_enabled is False:
        for i in range(enumerated_displays.Count):
            display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            gfx_index = str(enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
            port_type = str(enumerated_displays.ConnectedDisplays[i].PortType).upper()
            if 'DP' in str(display_port).upper() and port_type == 'EMBEDDED':
                display_port = 'E' + display_port  # Change display type to EDP
            display_ports = gfx_index.upper() + ' -' + display_port
            available_choices.append(display_ports)
    else:
        for index in gfx_index_list:
            index = index.lower()
            port_dict = display_config.get_supported_ports(index)
            for port in port_dict.keys():
                if 'DP' in port and port_dict[port] == 'EMBEDDED':
                    ports = index.upper() + " -" + 'E' + str(port).upper()  # Change display type to EDP
                else:
                    ports = index.upper() + " -" + port
                OPTIONS_displays_re.append(ports)

    if "NONE" not in available_choices:
        available_choices.append("NONE")
    try:
        if d1_selection != 'NONE':
            available_choices.remove(d1_selection)
        if d2_selection != 'NONE':
            available_choices.remove(d2_selection)
        if d3_selection != 'NONE':
            available_choices.remove(d3_selection)
        if d4_selection != 'NONE':
            available_choices.remove(d4_selection)
    except ValueError:
        pass

    display1_ctrl['menu'].delete(0, 'end')
    display2_ctrl['menu'].delete(0, 'end')
    display3_ctrl['menu'].delete(0, 'end')
    for choice in available_choices:
        display1_ctrl['menu'].add_command(label=choice, command=ttk._setit(display1, choice))
        display2_ctrl['menu'].add_command(label=choice, command=ttk._setit(display2, choice))
        display3_ctrl['menu'].add_command(label=choice, command=ttk._setit(display3, choice))

    if d4_selection != 'NONE':
        fill_edid_dpcd_data('D4', d4_selection)
    else:
        edid4.set("NONE")  # default value
        edid4_ctrl['menu'].delete(0, 'end')


##
# @brief APP Initialisation
# @param[in] args
# @return NA
def display_port_field_init(*args):
    OPTIONS_displays_re = []
    global is_sim_enabled
    if not quad_display_support:
        text_log.append("{0} : Info  : {1} Does Not Supports Four Displays".format(datetime.datetime.now().
                                                                                   strftime("%H:%M:%S"), platform_name))

    if display_type.get() == "PHYSICAL":
        is_sim_enabled = False
        text_log.append("{} : Info  : Make Sure GfxValSim Driver UnInstalled/Removed".format(datetime.datetime.now().
                                                                                             strftime("%H:%M:%S")))
        update_log_list()
    else:
        is_sim_enabled = True
        text_log.append("{} : Info  : Make Sure GfxValSim Driver Installed".format(datetime.datetime.now().
                                                                                   strftime("%H:%M:%S")))
        update_log_list()

    if is_sim_enabled is False:
        for i in range(enumerated_displays.Count):
            display_port = CONNECTOR_PORT_TYPE(enumerated_displays.ConnectedDisplays[i].ConnectorNPortType).name
            gfx_index = str(enumerated_displays.ConnectedDisplays[i].DisplayAndAdapterInfo.adapterInfo.gfxIndex)
            port_type = str(enumerated_displays.ConnectedDisplays[i].PortType).upper()
            if 'DP' in str(display_port).upper() and port_type == 'EMBEDDED':
                display_port = 'E' + display_port  # Change display type to EDP
            display_ports = gfx_index.upper() + ' -' + display_port
            OPTIONS_displays_re.append(display_ports)
    else:
        for index in gfx_index_list:
            index = index.lower()
            port_dict = display_config.get_supported_ports(index)
            for port in port_dict.keys():
                if 'DP' in port and port_dict[port] == 'EMBEDDED':
                    ports = index.upper() + " -" + 'EDP_A'
                else:
                    ports = index.upper() + " -" + port
                OPTIONS_displays_re.append(ports)

    if "NONE" not in OPTIONS_displays_re:
        OPTIONS_displays_re.append("NONE")

    display1.set("NONE")
    display2.set("NONE")
    display3.set("NONE")
    display4.set("NONE")

    display1_ctrl['menu'].delete(0, 'end')
    display2_ctrl['menu'].delete(0, 'end')
    display3_ctrl['menu'].delete(0, 'end')
    display4_ctrl['menu'].delete(0, 'end')

    for port in OPTIONS_displays_re:
        display1_ctrl['menu'].add_command(label=port, command=ttk._setit(display1, port))
        display2_ctrl['menu'].add_command(label=port, command=ttk._setit(display2, port))
        display3_ctrl['menu'].add_command(label=port, command=ttk._setit(display3, port))
        if quad_display_support:
            display4_ctrl['menu'].add_command(label=port, command=ttk._setit(display4, port))
    try:
        display1.trace('w', update_ports_d1)
        display2.trace('w', update_ports_d2)
        display3.trace('w', update_ports_d3)
        display4.trace('w', update_ports_d4)
    except ValueError:
        pass


# Creating Labels and Buttons for required fields in APP
display_type = ttk.StringVar(master)
display_type.set(OPTIONS_diplay_connection[0])  # default value

appStartPos_x = grefxpos
appStartPos_y = grefypos

edidRefPos_x = grefxpos + 5
edidRefPos_y = grefypos + 85

lable_env = ttk.Label(master, text="Select Display Environment", fg='black', bg='gray97')
lable_env.place(x=appStartPos_x, y=appStartPos_y)
display_env_ctrl = ttk.OptionMenu(master, display_type, *OPTIONS_diplay_connection)
display_env_ctrl.place(x=(appStartPos_x + 170), y=(appStartPos_y - 8))
display_type.trace('w', display_port_field_init)

# Display 1 Port Selection
lable_display1 = ttk.Label(master, text="Display 1", fg='black', bg='gray97')
lable_display1.place(x=appStartPos_x + 12, y=appStartPos_y + 30)
display1 = ttk.StringVar(master)
display1.set(OPTIONS_displays[0])  # default value
display1_ctrl = ttk.OptionMenu(master, display1, *OPTIONS_displays)
display1_ctrl.place(x=appStartPos_x, y=appStartPos_y + 50, width=150, height=30)

# Display 1 EDID Selection
lable_edid1 = ttk.Label(master, text="Display1 EDID", fg='black', bg='gray97')
lable_edid1.place(x=edidRefPos_x, y=edidRefPos_y + 70)
edid1 = ttk.StringVar(master)
edid1.set(OPTIONS_edid_dpcd_index[0])  # default value
edid1_ctrl = ttk.OptionMenu(master, edid1, *OPTIONS_edid_dpcd_index)
edid1_ctrl.place(x=(edidRefPos_x + 100), y=(edidRefPos_y + 65), width=225, height=30)

# Display 2 Port Selection
lable_display2 = ttk.Label(master, text="Display 2", fg='black', bg='gray97')
lable_display2.place(x=appStartPos_x + 132 + 70, y=appStartPos_y + 30)
display2 = ttk.StringVar(master)
display2.set(OPTIONS_displays[0])  # default value
display2_ctrl = ttk.OptionMenu(master, display2, *OPTIONS_displays)
display2_ctrl.place(x=appStartPos_x + 120 + 70, y=appStartPos_y + 50, width=150, height=30)

# Display 2 EDID Selection
lable_edid2 = ttk.Label(master, text="Display2 EDID", fg='black', bg='gray97')
lable_edid2.place(x=edidRefPos_x, y=edidRefPos_y + 30 + 70)
edid2 = ttk.StringVar(master)
edid2.set(OPTIONS_edid_dpcd_index[0])  # default value
edid2_ctrl = ttk.OptionMenu(master, edid2, *OPTIONS_edid_dpcd_index)
edidRefPos_y = edidRefPos_y + 30
edid2_ctrl.place(x=edidRefPos_x + 100, y=(edidRefPos_y + 65), width=225, height=30)

# Display 3 Port Selection
lable_display3 = ttk.Label(master, text="Display 3", fg='black', bg='gray97')
lable_display3.place(x=appStartPos_x + 12, y=appStartPos_y + 30 + 60)
display3 = ttk.StringVar(master)
display3.set(OPTIONS_displays[0])  # default value
display3_ctrl = ttk.OptionMenu(master, display3, *OPTIONS_displays)
display3_ctrl.place(x=appStartPos_x, y=appStartPos_y + 50 + 60, width=150, height=30)

# Display 3 EDID Selection
lable1_3_3 = ttk.Label(master, text="Display3 EDID", fg='black', bg='gray97')
lable1_3_3.place(x=edidRefPos_x, y=edidRefPos_y + 30 + 70)
edid3 = ttk.StringVar(master)
edid3.set(OPTIONS_edid_dpcd_index[0])  # default value
edid3_ctrl = ttk.OptionMenu(master, edid3, *OPTIONS_edid_dpcd_index)
edidRefPos_y = edidRefPos_y + 30
edid3_ctrl.place(x=edidRefPos_x + 100, y=(edidRefPos_y + 65), width=225, height=30)
# Display 4 Port Selection
lable1_4 = ttk.Label(master, text="Display 4", fg='black', bg='gray97')
lable1_4.place(x=appStartPos_x + 132 + 70, y=appStartPos_y + 30 + 60)
display4 = ttk.StringVar(master)
display4.set(OPTIONS_displays[0])  # default value
display4_ctrl = ttk.OptionMenu(master, display4, *OPTIONS_displays)
display4_ctrl.place(x=appStartPos_x + 120 + 70, y=appStartPos_y + 50 + 60, width=150, height=30)

# Display 4 EDID Selection
lable1_4_4 = ttk.Label(master, text="Display4 EDID", fg='black', bg='gray97')
lable1_4_4.place(x=edidRefPos_x, y=edidRefPos_y + 30 + 70)
edid4 = ttk.StringVar(master)
edid4.set(OPTIONS_edid_dpcd_index[0])  # default value
edid4_ctrl = ttk.OptionMenu(master, edid4, *OPTIONS_edid_dpcd_index)
edidRefPos_y = edidRefPos_y + 30
edid4_ctrl.place(x=edidRefPos_x + 100, y=(edidRefPos_y + 65), width=225, height=30)

display_port_field_init()

userEvPos_x = grefxpos + 70
userEvPos_y = grefypos + 277

lable2 = ttk.Label(master, text="        Select User Event MPO", fg='black', bg='gray97')
lable2.place(x=userEvPos_x, y=userEvPos_y)
mpo = ttk.StringVar(master)
mpo.set(OPTIONS_user_events[0])  # default value
w = ttk.OptionMenu(master, mpo, *OPTIONS_user_events)
w.place(x=userEvPos_x + 170, y=userEvPos_y - 5)

lable3 = ttk.Label(master, text="              Select Power Event", fg='black', bg='gray97')
lable3.place(x=userEvPos_x, y=userEvPos_y + 30)

pwr = ttk.StringVar(master)
pwr.set(OPTIONS_power_events[0])  # default value
w = ttk.OptionMenu(master, pwr, *OPTIONS_power_events)
w.place(x=userEvPos_x + 170, y=userEvPos_y + 25)

lable4 = ttk.Label(master, text="         Select Mode Set Event", fg='black', bg='gray97')
lable4.place(x=userEvPos_x, y=userEvPos_y + 60)
mode_lvl = ttk.StringVar(master)
mode_lvl.set(OPTIONS_mode_levels[0])  # default value
w = ttk.OptionMenu(master, mode_lvl, *OPTIONS_mode_levels)
w.place(x=userEvPos_x + 170, y=userEvPos_y + 55)

other_tests = ttk.StringVar(master)
other_tests.set(OTHER_tests[0])  # default value
w = ttk.OptionMenu(master, other_tests, *OTHER_tests)
w.place(x=userEvPos_x - 65, y=userEvPos_y + 125)

lable6 = ttk.Label(master, text="MPO1 : 2K Clip MPO2 : 4K Clip | ModeSet L0 : MMM L1 : All Modes", fg='black',
                   bg='gray67')
lable6.place(x=20, y=465)
lable6.pack(side=ttk.BOTTOM, fill=ttk.X)


##
# @brief To Reset fields existed in APP
# @return NA
def reset_fields():
    display1.set(OPTIONS_displays[0])  # default value
    display2.set(OPTIONS_displays[0])  # default value
    display3.set(OPTIONS_displays[0])  # default value
    display4.set(OPTIONS_displays[0])  # default value
    display_type.set(OPTIONS_diplay_connection[0])  # default value

    # EDID DPCD Reset
    edid1.set("NONE")  # default value
    edid2.set("NONE")  # default value
    edid3.set("NONE")  # default value
    edid4.set("NONE")  # default value

    mpo.set(OPTIONS_user_events[0])  # default value

    pwr.set(OPTIONS_power_events[0])  # default value

    mode_lvl.set(OPTIONS_mode_levels[0])  # default value

    other_tests.set(OTHER_tests[0])  # default value


# Create command lines for selected displays and events from APP
# Generates batch file with all saved command lines
# Explore logs in root folder with Test number


cmd_lines = []


##
# @brief ABC
# @return NA
def save_config_entry_fields():
    global display_check
    test_completion_time = 0
    total_time = 0
    displays = []
    if display1.get() != "NONE" or display2.get() != "NONE" or display3.get() != "NONE" or display4.get() != "NONE":
        display_check = True

        if mpo.get() != "NONE":
            if mpo.get() == "2KClip":
                usr_eve_type = "MPO1"
                test_completion_time = test_completion_time + 120
            elif mpo.get() == "4KClip":
                usr_eve_type = "MPO2"
                test_completion_time = test_completion_time + 120
            else:
                usr_eve_type = "MPO1 MPO2"
                test_completion_time = test_completion_time + 240
            selected_mpo_event = "-USR_EVE " + usr_eve_type
        else:
            selected_mpo_event = mpo.get()

        if pwr.get() != "NONE" or mode_lvl.get() != "NONE":
            if mpo.get() == "2KClip":
                test_completion_time = test_completion_time + 120
            elif mpo.get() == "4KClip":
                test_completion_time = test_completion_time + 120

        if pwr.get() != "NONE":
            selected_pwr_event = "-PWR_EVE " + pwr.get()
            test_completion_time = test_completion_time + 120
        else:
            selected_pwr_event = pwr.get()

        if mode_lvl.get() != "NONE":
            if mode_lvl.get() == "MMM":
                mode_level = "L0"
                test_completion_time = test_completion_time + 59
            else:
                mode_level = "L1"
                test_completion_time = test_completion_time + 330
            selected_mode_level = "-MODE_LVL " + mode_level
        else:
            selected_mode_level = mode_lvl.get()

        display1_port = display1.get()

        if display1.get() != "NONE":
            displays.append(display1.get())
        if display2.get() != "NONE":
            displays.append(display2.get())
        if display3.get() != "NONE":
            displays.append(display3.get())
        if display4.get() != "NONE":
            displays.append(display4.get())
        # To display approximate time taken for test
        if len(displays) == 1:
            total_time = int(37 + test_completion_time)
        if len(displays) == 2:
            total_time = int(74 + (2 * test_completion_time))
        if len(displays) == 3:
            total_time = int(111 + (5 * test_completion_time))
        if len(displays) == 4:
            total_time = int(148 + (6 * test_completion_time))

        if display_type.get() == "PHYSICAL":
            simulation_type = "-EMU"
            display2_port = display2.get()
            display3_port = display3.get()
            display4_port = display4.get()
        else:
            simulation_type = "-SIM"
            display2_port = display2.get()
            display3_port = display3.get()
            display4_port = display4.get()

            display1_edid_found = False
            display2_edid_found = False
            display3_edid_found = False
            display4_edid_found = False

            for key in OPTIONS_edid_dpcd_index_dict.keys():
                if display1_edid_found is not True:
                    if edid1.get() != "NONE" and display1.get() != "NONE":
                        if OPTIONS_edid_dpcd_index_dict[key] == edid1.get():
                            display1_port = display1_port + " SINK_" + key
                            display1_edid_found = True
                            continue
                    else:
                        display1_edid_found = True
                        continue
                if display2_edid_found is not True:
                    if edid2.get() != "NONE" and display2.get() != "NONE":
                        if OPTIONS_edid_dpcd_index_dict[key] == edid2.get():
                            display2_port = display2.get() + " SINK_" + key
                            display2_edid_found = True
                            continue
                    else:
                        display2_edid_found = True
                        continue
                if display3_edid_found is not True:
                    if edid3.get() != "NONE" and display3.get() != "NONE":
                        if OPTIONS_edid_dpcd_index_dict[key] == edid3.get():
                            display3_port = display3.get() + " SINK_" + key
                            display3_edid_found = True
                            continue
                    else:
                        display3_edid_found = True
                        continue
                if display4_edid_found is not True:
                    if edid4.get() != "NONE" and display4.get() != "NONE":
                        if OPTIONS_edid_dpcd_index_dict[key] == edid4.get():
                            display4_port = display4_port + " SINK_" + key
                            display4_edid_found = True
                            continue
                    else:
                        display4_edid_found = True
                        continue
                if display1_edid_found and display2_edid_found and display3_edid_found and display4_edid_found:
                    break
        line = "python Tests\\Display_Dev_BAT\\display_dev_bat_v1.py -{0} -{1} -{2} -{3} {4} {5} {6} {7}\n". \
            format(display1_port, display2_port, display3_port, display4_port, selected_mpo_event, selected_pwr_event,
                   selected_mode_level,
                   simulation_type)

        temp = line.replace("-NONE", "")
        cmd_line = temp.replace("NONE", "")

        master.cmds_count = master.cmds_count + 1
        log_name = 'rename Logs BAT_Test_log_{}\n'.format(master.cmds_count)

        # Batch file creation with saved command lines
        with open("run_bat.bat", 'a+') as f:
            print(cmd_line)
            text_log.append(
                "{} : Test : {} {}".format(datetime.datetime.now().strftime("%H:%M:%S"), master.cmds_count, cmd_line))
            total_time_ex = int(total_time / 60)
            time_log = "{} : Info  : Above Test takes approximately {} min(s) to Complete". \
                format(datetime.datetime.now().strftime("%H:%M:%S"), total_time_ex)
            text_log.append(time_log)
            update_log_list()

            f.write(cmd_line)
            f.write('timeout /t 5\n')
            f.write(log_name)
    else:
        text_log.append("{} : Info  : Make Sure to Select minimum One Display".format(datetime.datetime.now().
                                                                                      strftime("%H:%M:%S")))
        update_log_list()


##
# @brief To add PSR tests in batch file
# @return NA
def save_other_tests_entry_fields():
    global display_check
    test_completion_time = 0
    cmd_line = ""
    if other_tests.get() != "Others Tests":
        display_check = True
        if other_tests.get() == "Audio Basic Test":
            port_run = ""
            if display1.get() == "NONE" and display2.get() == "NONE" and display3.get() == "NONE" and \
                    display4.get() == "NONE":
                port_run = "-DP_A"
                test_completion_time = test_completion_time + 2
            else:
                if display1.get() != "NONE":
                    display1_port = display1.get()
                    port_run = "-" + display1_port[7:] + " "
                    test_completion_time = test_completion_time + 2
                if display2.get() != "NONE":
                    display2_port = display2.get()
                    port_run += "-" + display2_port[7:] + " "
                    test_completion_time = test_completion_time + 2
                if display3.get() != "NONE":
                    display3_port = display3.get()
                    port_run += "-" + display3_port[7:] + " "
                    test_completion_time = test_completion_time + 2
                if display4.get() != "NONE":
                    display4_port = display4.get()
                    port_run += "-" + display4_port[7:]
                    test_completion_time = test_completion_time + 2
            text_log.append("{} : Info  : Make Sure Intel Audio Driver Installed".
                            format(datetime.datetime.now().strftime("%H:%M:%S")))
            cmd_line = "python Tests\\Audio\\EndpointVerification\\audio_endpoint_basic.py " + port_run + "\n"
        elif other_tests.get() == "PSR1 Basic Test":
            test_completion_time = test_completion_time + 11
            cmd_line = "python Tests\\Power\\PSR\\psr_feature_basic.py -edp_a -config single -psr_version psr1 \n"
        elif other_tests.get() == "PSR2 Basic Test":
            test_completion_time = test_completion_time + 11
            cmd_line = "python Tests\\Power\\PSR\\psr_feature_basic.py -edp_a -config single -psr_version psr2 \n"
        elif other_tests.get() == "Virtual Basic Test":
            test_completion_time = test_completion_time + 4
            cmd_line = "python Tests\\VirtualDisplay\\virtual_display_basic.py -edp_a -config single \n"
        master.cmds_count = master.cmds_count + 1

        log_name = 'rename Logs \"{0}_{1}\"\n'.format(cmd_line.split("\\")[-1].strip('\n').replace('.py', '').strip(),
                                                      master.cmds_count)

        with open("run_bat.bat", 'a+') as f:
            print(cmd_line)
            text_log.append("{} : Test : {} {}".format(datetime.datetime.now().strftime("%H:%M:%S"), master.cmds_count,
                                                       cmd_line))
            text_log.append("{} : Info  : Above Test takes approximately {} min(s) to Complete".
                            format(datetime.datetime.now().strftime("%H:%M:%S"), test_completion_time))
            update_log_list()
            f.write(cmd_line)
            f.write('timeout /t 5\n')
            f.write(log_name)
    else:
        text_log.append("{} : Info  : Make Sure to Select Valid Other Test Case".format(datetime.datetime.now().
                                                                                        strftime("%H:%M:%S")))
        update_log_list()


##
# @brief Minimizes APP and starts executing batch file
# @return NA
def save_run_batfile():
    if display_check:
        master.wm_state('iconic')
        os.system("run_bat.bat")
        sys.exit()
    else:
        text_log.append("{} : Info  : Make Sure to Add Test Case".format(datetime.datetime.now().
                                                                         strftime("%H:%M:%S")))
        update_log_list()


##
# @brief To clear logs in APP
# @return NA
def clear_log():
    del text_log[:]
    text_log.append('Log : \n')
    update_log_list()


button = ttk.Button(master, text="Clear Log", width=10, command=clear_log)
button.place(x=110, y=365 + 90)


##
# @brief To modify created batch file, if required
# @return NA
def open_bat():
    batch_file_name = "run_bat.bat"
    if os.path.isfile(batch_file_name):
        temp_str = "notepad.exe run_bat.bat"
        os.system(temp_str)


# Buttons to add tests, open bat, reset fields, run batch file
button = ttk.Button(master, text="ADD Config Test", width=20, command=save_config_entry_fields)
button.place(x=userEvPos_x + 82, y=userEvPos_y + 85)

button = ttk.Button(master, text="ADD Other Test", width=20, command=save_other_tests_entry_fields)
button.place(x=userEvPos_x + 82, y=userEvPos_y + 125)

button = ttk.Button(master, text="Open BAT", width=10, command=open_bat)
button.place(x=userEvPos_x - 85, y=userEvPos_y + 165)

button = ttk.Button(master, text="Reset", width=8, command=reset_fields)
button.place(x=userEvPos_x + 115, y=userEvPos_y + 165)

button = ttk.Button(master, text="Run", width=10, command=save_run_batfile)
button.place(x=userEvPos_x + 205, y=userEvPos_y + 165)

ttk.mainloop()
