import logging
import struct

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class Client(object):
    def __init__(self, modbus_host, modbus_port):
        self.modbus_host = modbus_host
        self.modbus_port = modbus_port
        self.modbus_client = ModbusTcpClient(self.modbus_host, self.modbus_port)

    def connect(self):
        return self.modbus_client.connect()

    def disconnect(self):
        return self.modbus_client.close()

    def check_if_socket_open(self):
        return self.modbus_client.is_socket_open()

    def get_all_data(self):
        try:
            out = {}
            out["internal_temp"] = self.get_internal_temp()
            out["external_temp"] = self.get_external_temp()
            out["cp_state"] = self.get_cp_state()
            out["pp_state"] = self.get_pp_state()
            out["hcc3_error_code"] = self.get_hcc3_error_code()
            out["state"] = self.get_amtron_state()
            out["operation_mode"] = self.get_amtron_operation_mode()
            out["connector_type"] = self.get_connector_type()
            out["no_of_phases"] = self.get_amtron_no_of_phases()
            out["rated_current"] = self.get_amtron_rated_current()
            out["installation_current"] = self.get_amtron_installation_current()
            out["serial_number"] = self.get_serial_number()
            out["charging_session_meter_count"] = self.get_charging_session_meter_count()
            out["actual_power_consumption"] = self.get_actual_power_consumption()
            out["wallbox_name"] = self.get_amtron_wallbox_name()
            out["max_current_t1"] = self.get_max_current_t1()
            out["start_hour_t1"] = self.get_start_hour_t1()
            out["start_minute_t1"] = self.get_start_minute_t1()

            return out
        except Exception as e:
            logging.error(f"An error occurred while polling all data: {e}")

    # Input Registers
    def get_internal_temp(self):
        return self.get_16bit_uint(0x0300, "internal temperature")

    def get_external_temp(self):
        return self.get_16bit_uint(0x0301, "external temperature")

    def get_cp_state(self):
        return self.get_16bit_uint(0x0302, "CP state")

    def get_pp_state(self):
        return self.get_16bit_uint(0x0303, "PP state")

    def get_hcc3_error_code(self):
        return self.get_16bit_uint(0x0304, "HCC3 Error Code")

    def get_amtron_state(self):
        return self.get_16bit_uint(0x0305, "AMTRON State")

    def get_amtron_operation_mode(self):
        return self.get_16bit_uint(0x0306, "AMTRON Operation Mode")

    def get_connector_type(self):
        return self.get_16bit_uint(0x0307, "Connector Type")

    def get_amtron_no_of_phases(self):
        return self.get_16bit_uint(0x0308, "AMTRON No. of Phases")

    def get_amtron_rated_current(self):
        return self.get_16bit_uint(0x0309, "AMTRON Rated Current")

    def get_amtron_installation_current(self):
        return self.get_16bit_uint(0x030A, "AMTRON Installation Current")

    def get_serial_number(self):
        return self.get_32bit_uint(0x030B, "Serial number")

    def get_charging_session_meter_count(self):
        return self.get_32bit_uint(0x030D, "Charging session meter count")

    def get_actual_power_consumption(self):
        return self.get_32bit_uint(0x030F, "Actual power consumption")

    def get_amtron_wallbox_name(self):
        return self.get_string(0x0311, 11, 22, "Wallbox Name")

    def get_max_current_t1(self):
        return self.get_16bit_uint(0x031D, "Max Current T1")

    def get_start_hour_t1(self):
        return self.get_16bit_uint(0x031E, "Start hour T1")

    def get_start_minute_t1(self):
        return self.get_16bit_uint(0x031F, "Start minute T1")

    def get_16bit_uint(self, register, name):
        try:
            self.connect()
            rr = self.modbus_client.read_input_registers(register, 1, unit=255)

            if not rr.isError():
                res = BinaryPayloadDecoder.fromRegisters(
                    rr.registers, Endian.Big, Endian.Little
                ).decode_16bit_uint()

                self.modbus_client.close()
                return res

        except Exception as e:
            logging.warning(f"An error occurred while polling {name}: {e}")

    def get_32bit_uint(self, register, name):
        try:
            self.connect()
            rr = self.modbus_client.read_input_registers(register, 2, unit=255)

            if not rr.isError():
                res = BinaryPayloadDecoder.fromRegisters(
                    rr.registers, Endian.Big, Endian.Little
                ).decode_32bit_uint()

                self.modbus_client.close()
                return res

        except Exception as e:
            logging.warning(f"An error occurred while polling {name}: {e}")

    def get_string(self, register, length, chars, name):
        try:
            self.connect()
            rr = self.modbus_client.read_input_registers(register, length, unit=255)

            # This solves the string swap bytes issue
            # https://stackoverflow.com/questions/62411062/python-modbus-string-decoding-issue
            for i in range(len(rr.registers)):
                rr.registers[i] = struct.unpack("<H", struct.pack(">H", rr.registers[i]))[0]

            if not rr.isError():
                res = BinaryPayloadDecoder.fromRegisters(rr.registers) \
                    .decode_string(chars) \
                    .decode('UTF-8') \
                    .replace('\x00', '')  # Remove null chars 0x00 at the end of the name

                self.modbus_client.close()
                return res

        except Exception as e:
            logging.warning(f"An error occurred while polling {name}: {e}")
