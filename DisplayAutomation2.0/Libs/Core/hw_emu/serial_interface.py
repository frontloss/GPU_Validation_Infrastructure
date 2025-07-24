###############################################################################################
# @file     serial_interface.py
# @brief    Code to read and Write Data to Serial Interfaces
# @author   Sharath M, Sri Sumanth Geesala
################################################################################################

import time
import logging
import serial
import serial.tools.list_ports


##
# @brief        Get the list of connected com ports Details and connection details on them
# @return       (status, com_ports, hw_ids) - (Connection status: True if any comport is connected False otherwise ,
#               connected comport details , connection details (HW ID) on the comports)
def get_connected_com_ports_and_hw_ids():
    com_ports = []
    hw_ids = []
    status = False
    ports = serial.tools.list_ports.comports()
    for port in sorted(ports):
        ser = None
        try_count = 3
        try:
            com_port_name = port.device
            ser = serial.Serial(port=com_port_name, baudrate=9600, bytesize=8, stopbits=1, parity='N')
            ser.timeout = 2
            if ser.isOpen():
                while try_count > 0:
                    ser.write("0".encode())
                    time.sleep(1)
                    read_data = ser.readall()
                    data_read = read_data.decode()
                    logging.debug(f'{com_port_name}: data_read= {data_read}')
                    if data_read and not data_read.isspace():
                        com_ports.append(com_port_name)
                        hw_ids.append(data_read)
                        status = True
                        break
                    try_count = try_count - 1
                ser.close()
            else:
                logging.error(f'Not able to open Serial port {com_port_name}')
        except Exception as e:
            logging.error(e)
            if ser is not None and ser.isOpen():
                ser.close()
    return status, com_ports, hw_ids


##
# @brief        Write Data to serial port
# @param[in]    comport - Com Port Details
# @param[in]    write_data - byte data to be written to serial port
# @return       status - Connection status: returns True if write is successful, False otherwise.
def serial_port_write(comport, write_data):
    status = False
    ser = None
    try:
        ser = serial.Serial(port=comport, baudrate=9600, bytesize=8, stopbits=1, parity='N')
        ser.timeout = 2
        if ser.isOpen():
            logging.debug(f'Writing data to {comport} data = {write_data.encode()}')
            num_bytes_written = ser.write(write_data.encode())
            logging.debug(f'Num bytes written to {comport}= {num_bytes_written}')
            time.sleep(0.1)
            if num_bytes_written == len(write_data.encode()):
                status = True
            ser.close()
        else:
            logging.error(f'Not able to open Serial port {comport}')
    except Exception as e:
        logging.error(e)
        if ser is not None and ser.isOpen():
            ser.close()
        status = False
    return status


##
# @brief        Read Data from serial port
# @param[in]    comport - Com Port details
# @param[in]    write_data - byte data to be written to serial port, i.e the opcode and firmware memory address to read
# @return       (status,data_read) - (Connection status True if write is successful False otherwise, byte data read)
def serial_port_read(comport, write_data):
    status = False
    data_read = None
    ser = None
    try:
        ser = serial.Serial(port=comport, baudrate=9600, bytesize=8, stopbits=1, parity='N')
        ser.timeout = 2
        if ser.isOpen():
            logging.debug(f'Writing data to {comport} data = {write_data.encode()}')
            num_bytes_written = ser.write(write_data.encode())
            if num_bytes_written == len(write_data.encode()):
                time.sleep(0.1)
                data_read = ser.readall().decode()
                if data_read is None or data_read.isspace():
                    logging.error(f'Data is not received from {comport}')
                    status = False
                else:
                    logging.debug(f'Num bytes read from {comport}= {len(data_read)}')
                    status = True
            ser.close()
        else:
            logging.error(f'Not able to open Serial port {comport}')
    except Exception as e:
        logging.error(e)
        if ser is not None and ser.isOpen():
            ser.close()
        status = False
    return status, data_read
