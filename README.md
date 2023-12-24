# foscam-FI8918W
Foscam FI8918W interface in python
Control your Foscam camera using CGI commands through this Python script.

## Prerequisites

- Python 3.x
- Required Python packages: `argparse`, `requests`

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/bitstrike/foscam-controller.git
    cd foscam-controller
    ```

2. Run the script:

    ```bash
    python foscam.py -a <monitor_address> -u <username> -p <password> -c <command>
    ```

    Example:

    ```bash
    python foscam.py -a 192.168.1.1 -u admin -p admin -c move_up
    ```

3. Available Commands:

    - `reset` - Reset Camera
    - `move_up` - Move Up
    - `move_down` - Move Down
    - `move_left` - Move Left
    - `move_right` - Move Right
    - ... (list other available commands)

4. Optional Arguments:

    - `-s, --preset` - Preset value for set_preset command
    - `-n, --iterations` - Number of times to execute the command (default: 1)

## Additional Notes

- Make sure to replace `<monitor_address>`, `<username>`, and `<password>` with your Foscam details.

- For more information on available commands and usage, run:

    ```bash
    python foscam.py --help
    ```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
