import tkinter as tk
from tkinter import filedialog
import csv
import io

def select_file():
    """
    Opens a file dialog to select a .xls file (which is actually a .txt file).
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("XLS Files", "*.xls")])
    if not file_path:
        raise Exception("No .xls file selected.")
    return file_path

def process_file(file_path):
    """
    Reads the content of the file and converts it to a CSV format.
    """
    with open(file_path, "r") as txt_file:
        txt_data = txt_file.read()

    lines = txt_data.split('\n')
    csv_data = [line.split('\t') for line in lines]

    csv_output = io.StringIO()
    csv_writer = csv.writer(csv_output)
    csv_writer.writerows(csv_data)

    return csv_output.getvalue()
