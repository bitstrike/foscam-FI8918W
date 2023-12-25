#!/usr/bin/env python3

import argparse
import requests
import base64
import sys

class Foscam:
    def __init__(self, monitor_address, username, password):
        self.monitor_address = monitor_address
        self.username = username
        self.password = password
        self.session = requests.Session()

    def help(self):
        help_text = """
        Foscam Controller Help:
        --------------------------------------
        Command line arguments:
          -a, --monitor-address   IP address or hostname of the Foscam camera.
          -u, --username          Foscam camera username.
          -p, --password          Foscam camera password.
          -c, --command           Command to send to the camera.
          -s, --preset            Preset value for set_preset command
          -n, --iterations        Number of times to execute the command (default: 1)

        Available Commands:
          reset                  - Reset Camera
          move_up                - Move Up
          move_down              - Move Down
          move_left              - Move Left
          move_right             - Move Right
          move_up_right          - Diagonally Up Right
          move_down_right        - Diagonally Down Right
          move_up_left           - Diagonally Up Left
          move_down_left         - Diagonally Down Left
          stop                   - Stop Movement
          set_preset <num>       - Set Preset (e.g., set_preset 1)
          goto_preset <num>      - Go to Preset (e.g., goto_preset 1)
          iron                   - Turn IR On (Wake)
          iroff                  - Turn IR Off (Sleep)
          reboot                 - Reboot Camera
        """
        return help_text

    def db(self, line):
        print(f"DEBUG: {line}")

    def send_cmd(self, cmd):
        url = f"http://{self.username}:{self.password}@{self.monitor_address}/{cmd}"
        response = requests.get(url, verify=False)

        if response.ok:
            print(f"Command '{cmd}' sent successfully")
        else:
            print(f"Error sending command '{cmd}': {response.status_code} - {response.text}")

    def move_up(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=0&onestep=1")

    def move_up_right(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=90&onestep=1")

    def move_up_left(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=91")

    def move_down(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=2&onestep=3")

    def move_right(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=4&onestep=5")

    def move_left(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=6&onestep=7")

    def move_down_right(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=92&onestep=1")

    def move_down_left(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=93")

    def move_stop(self, preset_value=1, iterations=1):
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command=1")

    def set_preset (self, preset_value=1, iterations=1):
        preset_cmd = 30 + (preset_value * 2)
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command={preset_cmd}&preset={preset_value}")

    def goto_preset (self, preset_value=1, iterations=1):
        preset_cmd = 31 + (preset_value * 2)
        for _ in range(iterations):
            self.send_cmd(f"decoder_control.cgi?command={preset_cmd}&preset={preset_value}")

    def iron (self, preset_value=1, iterations=1):
        self.send_cmd("decoder_control.cgi?command=95&")

    def iroff (self, preset_value=1, iterations=1):
        self.send_cmd("decoder_control.cgi?command=94&")

    def camera_reset(self):
        self.send_cmd("reboot.cgi?")

def parse_args():
    parser = argparse.ArgumentParser(description="Control Foscam camera via CGI commands.")
    parser.add_argument("monitor_address", help="Foscam monitor address")
    parser.add_argument("username", help="Foscam login username")
    parser.add_argument("password", help="Foscam login password")
    parser.add_argument("command", help="Command to execute (e.g., move_up, camera_reset)")

    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description="Foscam Controller")
    parser.add_argument("-a", "--monitor-address", required=True, help="IP address or hostname of the Foscam camera.")
    parser.add_argument("-u", "--username", required=True, help="Foscam camera username.")
    parser.add_argument("-p", "--password", required=True, help="Foscam camera password.")
    parser.add_argument("-c", "--command", required=True, help="Command to send to the camera.")
    parser.add_argument("-s", "--preset", type=int, help="Preset value for set_preset command")
    parser.add_argument("-n", "--iterations", type=int, default=1, help="Number of times to execute the command (default: 1)")

    args = parser.parse_args()

    foscam = Foscam(
        monitor_address=args.monitor_address,
        username=args.username,
        password=args.password
    )

    if args.command.lower() == "help":
        print(foscam.help())
        sys.exit()

    command_functions = {
        'reset': foscam.camera_reset,
        'move_up': foscam.move_up,
        'move_down': foscam.move_down,
        'move_left': foscam.move_left,
        'move_right': foscam.move_right,
        'move_up_right': foscam.move_up_right,
        'move_down_right': foscam.move_down_right,
        'move_up_left': foscam.move_up_left,
        'move_down_left': foscam.move_down_left,
        'stop': foscam.move_stop,
        'set_preset': foscam.set_preset,
        'goto_preset': foscam.goto_preset,
        'iron': foscam.iron,
        'iroff': foscam.iroff,
        'reboot': foscam.camera_reset,
    }

    if args.command.lower() == "help":
        foscam.help()
        sys.exit()

    # Check if preset argument is provided, otherwise default to 1
    preset_value_from_command_line = args.preset if args.preset is not None else 1

    command_to_execute = args.command

    if command_to_execute not in command_functions:
        valid_commands = ', '.join(command_functions.keys())
        print(f"Error: Invalid command '{command_to_execute}'. Valid commands are: {valid_commands}")
        sys.exit(1)

    foscam.db("send command")
    command_functions[command_to_execute](preset_value_from_command_line, iterations=args.iterations)

if __name__ == "__main__":
    main()

