import subprocess
import time
import os
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox


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


class SqlmapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sqlmap GUI")

        self.target_label = tk.Label(root, text="Target:")
        self.target_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.target_entry = tk.Entry(root, width=50)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.options_label = tk.Label(root, text="Options:")
        self.options_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.options_entry = tk.Entry(root, width=50)
        self.options_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.scan_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.save_button = tk.Button(root, text="Save Output", command=self.save_output)
        self.save_button.grid(row=4, column=1, padx=5, pady=5, sticky="e")

        self.operations = {
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

        self.operation_label = tk.Label(root, text="Operation:")
        self.operation_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")

        self.operation_var = tk.StringVar(root)
        self.operation_var.set(list(self.operations.values())[0]["description"])

        self.operation_menu = tk.OptionMenu(root, self.operation_var, *[op["description"] for op in self.operations.values()])
        self.operation_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    def start_scan(self):
        target = self.target_entry.get()
        additional_options = self.options_entry.get()
        selected_operation = self.operation_var.get()

        operation_command = ""
        for op in self.operations.values():
            if op["description"] == selected_operation:
                operation_command = op["command"]
                break

        options = f"{operation_command} {additional_options}".strip()
        output_file = f"sqlmap_scan_{int(time.time())}.log"

        self.output_text.insert(tk.END, "Scan starting... please wait.\n")

        try:
            helper = Sqlmap(target)
            result, exit_code = helper.scan(options, output_file)
            self.output_text.insert(tk.END, result + "\n")
            self.output_text.insert(tk.END, f"Scan completed with exit code: {exit_code}\n")
            self.output_file = output_file
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def save_output(self):
        if hasattr(self, "output_file") and os.path.exists(self.output_file):
            save_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log files", "*.log"), ("All files", "*.*")])
            if save_path:
                os.rename(self.output_file, save_path)
                messagebox.showinfo("Save Output", f"Output saved to {save_path}")
        else:
            messagebox.showwarning("Save Output", "No scan output available to save.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SqlmapGUI(root)
    root.mainloop()
