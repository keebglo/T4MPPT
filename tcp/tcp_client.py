import socket

from proto_msg_factory import (
    EmergencyMsg, EMSUpdate, PowerOff, UpdateRequest, UpdateMsg, ProtoMsg)


class TCPClient:
    def __init__(self, address):
        self.ip_address = address
        self._print_msg("client created with")
        self._make_socket()
        self._connect()

    def _make_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.sock is None:
                print("client socket not created")
            else:
                print("client socket created")
        except socket.error as e:
            print(e)

    def _connect(self):
        self._print_msg("attempting to connect to")
        try:
            self.sock.connect(self.ip_address)
            print("connection successful")
        except Exception as e:
            print("Connection failed with: ")
            print(e)

    def _print_msg(self, message):
        print(
            message + " {} on port {}".format(
                self.ip_address[0], self.ip_address[1]))

    def post(self, msg):
        try:
            self.sock.send(msg[0] + msg[1])
        except Exception as e:
            print(e)

    def end_connection(self):
        self.sock.send(ProtoMsg.hang_up())
        self.sock.close()


class Gui:

    def go(self):
        self.display_main_menu()
        self.get_user_msg_selection()

    def display_main_menu(self):
        print("-------------------------------")
        print("Client Commands:")
        print("-------------------------------")
        print("1 : Send Emergency Message")
        print("2 : Send EMS Update Message")
        print("3 : Send Update Message")
        print("4 : Power Off")
        print("X : Close connection")
        print("-------------------------------")

    def get_user_msg_selection(self):
        # message_selected = input(">: ")
        run_program = True

        client = TCPClient(("localhost", 10000))

        while run_program:
            message_selected = input(">: ")
            if message_selected == "1":
                emergency_msg = EmergencyMsg().get_packed_msg()
                client.post(emergency_msg)
            elif message_selected == "2":
                ems_update_msg = EMSUpdate().get_packed_msg()
                client.post(ems_update_msg)
            elif message_selected == "3":
                update_msg = UpdateMsg().get_packed_msg()
                client.post(update_msg)
            elif message_selected == "4":
                power_off_msg = PowerOff().get_packed_msg()
                client.post(power_off_msg)
            elif message_selected == "5":
                update_req_msg = UpdateRequest().get_packed_msg()
                client.post(update_req_msg)
            elif message_selected == "X":
                client.end_connection()
                run_program = False
                print("connection ended")


if __name__ == "__main__":
    gui = Gui()
    gui.go()
