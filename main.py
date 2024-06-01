import subprocess
import time
import os

class Sqlmap:
    def __init__(self, target):
        self.target = target

    def scan(self, options, output_file):
        try:
            command = ["sqlmap"] + options.split() + ["-u", self.target]
            with open(output_file, "w") as f:
                result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                with open(output_file, "r") as f:
                    output = f.read()
                return output, result.returncode
            else:
                return f"Error: {result.stderr}\n", result.returncode
        except FileNotFoundError:
            return "Error: sqlmap not found. Please install sqlmap and try again.\n", 1

def clear_console():
    print("\033c", end="")

def get_input(prompt, exit_option="0"):
    while True:
        user_input = input(prompt).strip()
        clear_console()
        if user_input == exit_option:
            return None
        if user_input:
            return user_input
        print(f"Invalid input. Please enter a value or press {exit_option} to return.")

def start_scan(helper, options):
    output_file = f"sqlmap_scan_{int(time.time())}.log"
    print("*" * 60)
    print("Scan starting... please wait.\n")
    time.sleep(1)
    try:
        result, exit_code = helper.scan(options, output_file)
        print(result)
        print("*" * 60)
        print(f"Scan completed with exit code: {exit_code}\n")

        save_log = get_input("Would you like to save the log output? (yes/no): ").lower()
        if save_log == "yes":
            new_filename = get_input("Would you like to give a custom name to the log file? (leave empty for default): ", exit_option="")
            if new_filename:
                new_filename = new_filename if new_filename.endswith(".log") else new_filename + ".log"
                output_file = os.path.join(os.getcwd(), new_filename)
            with open(output_file, "w") as f:
                f.write(result)
            print(f"Output saved to {output_file}\n")
        else:
            print("Log output not saved.\n")

    except KeyboardInterrupt:
        print("\nScan interrupted. Returning to the main menu...\n")

def display_operations(operations):
    print("Operations:\n")
    keys = list(operations.keys())
    half = (len(keys) + 1) // 2
    for i in range(half):
        key1 = keys[i]
        key2 = keys[i + half] if i + half < len(keys) else ""
        desc1 = operations[key1]["description"]
        desc2 = operations[key2]["description"] if key2 else ""
        print(f"  {key1:2}) -> {desc1:35}  {key2:2}) -> {desc2}")
    print("\n  0) -> QUIT")

def main():
    ascii_art = """                                                          
 _____ _____ __    _____ _____ _____ __    _____ _____ _____ 
|   __|     |  |  |     |  _  |  _  |  |  |     |_   _|   __|
|__   |  |  |  |__| | | |     |   __|  |__|-   -| | | |   __|
|_____|__  _|_____|_|_|_|__|__|__|  |_____|_____| |_| |_____|
         |__|                                                
                                                                                 
by @mikropsoft
"""
    print(ascii_art)
    time.sleep(1)

    operations = {
        1:  {"description": "Test for SQL Injection", "command": "--batch"},
        2:  {"description": "Fingerprint the DBMS", "command": "--fingerprint"},
        3:  {"description": "List DBMS databases", "command": "--dbs"},
        4:  {"description": "List DBMS tables", "command": "--tables"},
        5:  {"description": "List DBMS columns", "command": "--columns"},
        6:  {"description": "Dump DBMS database table entries", "command": "--dump"},
        7:  {"description": "Dump DBMS database table entries by condition", "command": "--dump -C column_name -T table_name -D database_name --where"},
        8:  {"description": "Search for DBMS database names", "command": "--search -D"},
        9:  {"description": "Search for DBMS table names", "command": "--search -T"},
        10: {"description": "Search for DBMS column names", "command": "--search -C"},
        11: {"description": "Check for DBMS privilege", "command": "--privileges"},
        12: {"description": "Check for DBMS roles", "command": "--roles"},
        13: {"description": "Check for DBMS user password hashes", "command": "--passwords"},
        14: {"description": "Test for common issues (WAF/IPS)", "command": "--tamper"},
        15: {"description": "Enumerate DBMS users", "command": "--users"},
        16: {"description": "Enumerate DBMS user privileges", "command": "--privileges --users"},
        17: {"description": "Enumerate DBMS user roles", "command": "--roles --users"},
        18: {"description": "Enumerate DBMS schema", "command": "--schema"},
        19: {"description": "Enumerate DBMS system databases", "command": "--system-dbs"},
        20: {"description": "Enumerate DBMS data", "command": "--data"},
    }

    while True:
        try:
            display_operations(operations)
            operation_input = get_input("\n> Choose operation: ")
            if operation_input is None:
                print("\nExiting the tool. Goodbye!")
                break

            try:
                operation = int(operation_input)
                if operation == 0:
                    print("\nExiting the tool. Goodbye!")
                    break
                if operation not in operations:
                    print("Invalid operation\n")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            print("\n" + "*" * 60)
            print(ascii_art)
            print("Press ctrl + c to close the tool.")
            target = get_input("\n> Enter the URL to test for SQL injection (Example: http://example.com/index.php?id=1), or enter 0 to return: ")
            if target is None:
                continue

            additional_options = get_input("\n> Enter additional options for the scan (leave empty for default): ", exit_option="")
            if additional_options is None:
                additional_options = ""

            helper = Sqlmap(target)
            options = f"{operations[operation]['command']} {additional_options}".strip()
            start_scan(helper, options)

        except KeyboardInterrupt:
            print("\nCtrl+C detected. Exiting the tool. Goodbye!\n")
            break

if __name__ == "__main__":
    main()
