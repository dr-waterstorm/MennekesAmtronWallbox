from amtronwallbox.client import Client


class MennekesAmtronWallbox(object):
    def __init__(self, modbus_host, modbus_port):
        # connect to modbus server
        self.client = Client(modbus_host, modbus_port)

    def get_all_data(self):
        # get all known registers
        data = self.client.get_all_data()

    def print_all_data(self):
        print(self.client.get_all_data())
