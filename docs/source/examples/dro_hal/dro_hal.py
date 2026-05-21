"""
DRO Hardware Abstraction Layer (HAL)
====================================

The ``dro_hal`` module serves as the primary communication bridge between 
Python and the AKKON Digital Read Out (DRO) controller. It encapsulates 
the serial communication protocol and provides a high-level API to access 
real-time encoder data and device information.

:Version: 1.0.0
:Author: Gerhard Burger
:Copyright: 2026, Gerhard Burger
:License: MIT
"""

import serial
import struct
import time

__version__ = "1.0.0"
__author__ = "Gerhard Burger"

class DROController:
    """
    Main controller class for managing communication with the BlackPill I/O Carrier.
    
    This class handles the serial connection, packet framing, and the conversion 
    of raw binary data into structured Python types.
    """

    # Constants from the Delphi unit
    MAX_AXES = 3
    DRO_SUCCESS = 0
    DRO_DTMOK = 0
    DRO_ERR_CRC = -6
    DRO_ERR_SEND_FAIL = -1
    DRO_ERR_NOT_ACCEPTED = -2
    DRO_ERR_INVALID_AXIS = -5

    # Command Codes
    DRO_GET_CONTROLLER_INFO = 1
    DRO_SET_ZERO = 2
    DRO_SET_TRANSMISSION = 3
    DRO_GET_DEVICE_INFO = 5
    DRO_SET_NEXT_DIVIDER = 6
    DRO_SET_PREV_DIVIDER = 7
    DRO_SET_DIVIDER_INDEX = 8
    DRO_SET_CUSTOM_DIVIDER = 9
    DRO_SET_BUZZER_STATE = 10
    DRO_GET_PARAMS = 11
    DRO_SET_PARAMS = 12
    DRO_SET_ENCODER_RESOLUTION = 13
    DRO_SET_POSITION_MONITOR_PARAMS = 14
    DRO_SET_AXIS_FLAG = 16
    DRO_SET_R0X_VALUE = 17
    DRO_SET_R0X = 20
    DRO_SET_W0X_VALUE = 21
    DRO_GET_R0X_VALUE = 22
    DRO_GET_W0X_VALUE = 23
    DRO_SET_HC05_CONFIG = 24
    DRO_JUMP_BOOTLOADER = 99

    # Struct formats (packed records)
    # < = Little Endian, q = int64, H = uint16, B = byte, I = uint32, h = int16
    FMT_DEVICE_CONTEXT_INFO = "<BBBBB B 22s 11s"
    FMT_DRO_INFO_REC = "<q H B B h"
    FMT_CONTROLLER_INFO_REC = f"<{MAX_AXES * struct.calcsize(FMT_DRO_INFO_REC)}s B"
    FMT_TRANSMISSION_PARAMS = "<I I I"
    FMT_POSITION_MONITOR = "<I I"

    def __init__(self, port, baudrate=115200, timeout=1):
        """
        Initializes the DROController and opens the serial port.

        :param port: The serial port name (e.g., 'COM5' or '/dev/ttyUSB0').
        :type port: str
        :param baudrate: Connection speed, defaults to 115200.
        :type baudrate: int
        :param timeout: Serial read timeout in seconds, defaults to 1.
        :type timeout: int
        """
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.bt_device_name = "AKKON_DRO"

    def calc_crc8(self, data: bytes) -> int:
        """
        Calculates the CRC-8-ATM checksum for a byte sequence.

        Uses the polynomial 0x07. This is required for both outgoing 
        and incoming packets to ensure data integrity.

        :param data: The data to be hashed.
        :type data: bytes
        :return: The 8-bit checksum.
        :rtype: int
        """
        polynomial = 0x07
        crc = 0x00
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ polynomial) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    def send_receive(self, cmd: int, payload: bytes = b"", expected_len: int = 0):
        """
        Low-level method to handle the binary protocol exchange.

        Constructs a packet with start byte $24, command, length, and CRC.
        Then waits for the controller's response and validates its checksum.

        :param cmd: The command identifier.
        :type cmd: int
        :param payload: Optional binary data to send, defaults to b"".
        :type payload: bytes
        :param expected_len: Expected size of the returned data payload, defaults to 0.
        :type expected_len: int
        :return: A tuple of (status, data). Status 0 indicates success.
        :rtype: tuple(int, bytes or None)
        """
        header = struct.pack("<BBB", 0x24, cmd, len(payload))
        full_packet = header + payload
        crc = self.calc_crc8(full_packet)
        full_packet += struct.pack("B", crc)

        try:
            self.ser.write(full_packet)
            response = self.ser.read(expected_len + 5)
            
            if len(response) >= 5 and response[0] == 0x24:
                status = response[2]
                data_len = response[3]
                actual_data = response[4:4+data_len]
                check_data = response[1:4+data_len]
                calc_crc = self.calc_crc8(check_data)
                
                if calc_crc == response[4+data_len]:
                    return status, actual_data
                else:
                    return self.DRO_ERR_CRC, None
                    
            return self.DRO_ERR_SEND_FAIL, None
        except Exception as e:
            print(f"Communication Error: {e}")
            return self.DRO_ERR_SEND_FAIL, None

    def set_zero(self, axis: int) -> bool:
        """
        Resets the position of a specific axis to zero.

        :param axis: Index of the axis (0, 1, or 2).
        :type axis: int
        :return: True if the command was acknowledged successfully.
        :rtype: bool
        """
        status, _ = self.send_receive(self.DRO_SET_ZERO, struct.pack("<B", axis))
        return status == 0

    def set_divider_index(self, axis: int, index: int) -> bool:
        """
        Sets the divider index for an axis to scale the encoder input.

        :param axis: Index of the axis.
        :type axis: int
        :param index: The divider index value.
        :type index: int
        :return: True on success.
        :rtype: bool
        """
        status, _ = self.send_receive(self.DRO_SET_DIVIDER_INDEX, struct.pack("<BB", axis, index))
        return status == 0

    def set_custom_divider(self, axis: int, value: int) -> bool:
        """
        Sets a specific custom divider value for an axis.

        :param axis: Index of the axis.
        :type axis: int
        :param value: The custom 16-bit divider value.
        :type value: int
        :return: True on success.
        :rtype: bool
        """
        status, _ = self.send_receive(self.DRO_SET_CUSTOM_DIVIDER, struct.pack("<BH", axis, value))
        return status == 0

    def set_w0x_value(self, axis: int, value: int) -> bool:
        """
        Sets the workpiece zero point (W0x) for the given axis.

        :param axis: Index of the axis.
        :type axis: int
        :param value: The 64-bit integer position value.
        :type value: int
        :return: True on success.
        :rtype: bool
        """
        status, _ = self.send_receive(self.DRO_SET_W0X_VALUE, struct.pack("<Bq", axis, value))
        return status == 0

    def get_w0x_value(self, axis: int):
        """
        Retrieves the current workpiece zero point (W0x) from the controller.

        :param axis: Index of the axis.
        :type axis: int
        :return: The 64-bit position value, or None if the request failed.
        :rtype: int or None
        """
        status, data = self.send_receive(self.DRO_GET_W0X_VALUE, struct.pack("<B", axis), expected_len=9)
        if status == 0 and data:
            return struct.unpack("<Bq", data)[1]
        return None

    def set_transmission(self, axis: int, num: int, den: int, res: int) -> bool:
        """
        Configures the mechanical gear ratio and encoder resolution.

        :param axis: Index of the axis.
        :type axis: int
        :param num: Gear ratio numerator.
        :type num: int
        :param den: Gear ratio denominator.
        :type den: int
        :param res: Encoder resolution (pulses per unit).
        :type res: int
        :return: True on success.
        :rtype: bool
        """
        payload = struct.pack("<BIII", axis, num, den, res)
        status, _ = self.send_receive(self.DRO_SET_TRANSMISSION, payload)
        return status == 0

    def get_device_info(self) -> dict or None:
        """
        Fetches hardware and firmware metadata from the controller.

        :return: Dictionary containing 'HW_Ver', 'FW_Ver', 'AxisCount', 'Date', and 'Name'.
        :rtype: dict or None
        """
        expected_size = struct.calcsize(self.FMT_DEVICE_CONTEXT_INFO)
        status, data = self.send_receive(self.DRO_GET_DEVICE_INFO, expected_len=expected_size)
        
        if status == 0 and data and len(data) >= expected_size:
            unpacked = struct.unpack(self.FMT_DEVICE_CONTEXT_INFO, data)
            
            return {
                "HW_Ver": f"{unpacked[0]}.{unpacked[1]}",
                "FW_Ver": f"{unpacked[2]}.{unpacked[3]}.{unpacked[4]}",
                "AxisCount": unpacked[5],
                "Date": unpacked[6].split(b'\x00')[0].decode('ascii', errors='ignore').strip(),
                "Name": unpacked[7].split(b'\x00')[0].decode('ascii', errors='ignore').strip()
            }
        return None
    
    def read_controller_info(self) -> list or None:
        """
        Reads real-time data for all axes simultaneously.

        Returns a list of dictionaries, one for each axis, containing position, 
        velocity, and status flags.

        :return: List of axis data dictionaries, or None on failure.
        :rtype: list or None
        """
        status, data = self.send_receive(self.DRO_GET_CONTROLLER_INFO, expected_len=struct.calcsize(self.FMT_CONTROLLER_INFO_REC))
        if status == 0 and data:
            axes = []
            info_size = struct.calcsize(self.FMT_DRO_INFO_REC)
            for i in range(self.MAX_AXES):
                chunk = data[i*info_size : (i+1)*info_size]
                pos, div, flags, div_idx, vel = struct.unpack(self.FMT_DRO_INFO_REC, chunk)
                axes.append({
                    "Pos": pos, 
                    "Div": div, 
                    "Vel": vel, 
                    "Flags": flags,
                    "DivIdx": div_idx
                })
            return axes
        return None

    def close(self):
        """
        Safely closes the serial connection to the hardware.
        """
        self.ser.close()
