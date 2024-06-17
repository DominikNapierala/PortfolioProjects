import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
from tkinter import messagebox
from typing import Union
import csv

def main():
    app_window()

def app_window():
    button_font = ("Arial", 10, "normal")
    app = tk.Tk() # This line creates the instance of the app.
    app.geometry("800x450")
    app.wm_minsize(800, 450)
    app.title("CSV file modifier and data visualizer")

# Frames
###########################
    controls_frame = ttk.Frame(
        master = app,
        borderwidth = 1,
        relief = "solid"
    )

    buttons_frame = ttk.Frame(
        master = controls_frame,
        borderwidth = 1,
        relief = "solid"
    )

    table_frame= ttk.Frame(
        master = app,
        borderwidth = 1,
        relief = "solid"
    )

    replace_frame = ttk.Frame(
        master = controls_frame,
        borderwidth = 1,
        relief = "solid"
    )

    delete_selected_rows_frame = ttk.Frame(
        master = controls_frame,
        borderwidth = 1,
        relief = "solid"
    )

    delete_selected_column_frame = ttk.Frame(
        master = controls_frame,
        borderwidth = 1,
        relief = "solid"
    )

###########################

# Widgets
###########################

    # Buttons
    ###########################
    choose_file_button = ttk.Button(
        master = buttons_frame,
        text = "Select CSV file",
        command = lambda: create_table(table_layout, delete_selected_column_dropdown)
    )

    export_table_button = ttk.Button(
        master = buttons_frame,
        text = "Export table",
        command = lambda: export_table(table_layout)
    )

    # Table
    ###########################
    table_layout = ttk.Treeview(
        master = table_frame,
        columns = (),
        show = "headings"
    )

    ys = ttk.Scrollbar(
        master = table_frame,
        orient = 'vertical',
        command = table_layout.yview
    )

    xs = ttk.Scrollbar(
        master = table_frame,
        orient = 'horizontal',
        command = table_layout.xview
    )

    table_layout['yscrollcommand'] = ys.set
    table_layout['xscrollcommand'] = xs.set

    # Find & Replace
    ###########################

        # Variables
    find_what_var = tk.StringVar()
    replace_with_var = tk.StringVar()

        # Widgets
    find_what_label = ttk.Label(
        master = replace_frame,
        text = "Find:"
    )

    find_what = ttk.Entry(
        master = replace_frame,
        state = "enabled",
        textvariable = find_what_var
    )

    replace_with_label = ttk.Label(
        master = replace_frame,
        text = "Replace with:"
    )

    replace_with = ttk.Entry(
        master = replace_frame,
        state = "enabled",
        textvariable = replace_with_var
    )

    replace_button = ttk.Button(
        master = replace_frame,
        text = "Replace",
        command = lambda: replace_values(table_layout, tuple([find_what_var.get(), replace_with_var.get()]))
    )

    # Remove selected rows
    ###########################

        # Widgets
    delete_selected_rows_label = ttk.Label(
        master = delete_selected_rows_frame,
        text = "Select rows you want to delete."
    )

    delete_selected_rows_button = ttk.Button(
        master = delete_selected_rows_frame,
        text = "Delete rows",
        command = lambda: delete_selected_rows(table_layout)
    )

    # Remove selected column
    ###########################
        # Variables
    dropdown_menu_value = tk.StringVar(value = "...")

        # Widgets
    delete_selected_column_label = ttk.Label(
        master = delete_selected_column_frame,
        text = "Select a column to delete."
    )
    delete_selected_column_dropdown = ttk.Combobox(
        master = delete_selected_column_frame,
        state = "readonly",
        textvariable = dropdown_menu_value
    )
    delete_selected_column_button = ttk.Button(
        master = delete_selected_column_frame,
        text = "Delete",
        command = lambda: delete_selected_column(dropdown_menu_value, table_layout, delete_selected_column_dropdown)
    )

# When you use the bind method on a Tkinter widget, the callback function you bind to the event always receives an event object as its first parameter.
# table_layout.bind("<<TreeviewSelect>>", lambda event: row_selection(table_layout))

    # table_layout.bind("<Button-1>", lambda event: selected_column(table_layout, event))

###########################

# Packing
###########################
    # Frames

    controls_frame.grid(
        row = 0,
        column = 0,
        sticky = "nsew",
        padx = (10, 5),
        pady = 10
    )

    table_frame.grid(
        row = 0,
        column = 1,
        sticky = "nsew",
        padx = (5, 10),
        pady = 10
    )

    # Widgets
    app.rowconfigure(0, weight = 1)
    app.columnconfigure(1, weight = 1)
    controls_frame.rowconfigure((0, 1, 2, 3), weight = 1)

        # Controls frame
            # Buttons
    choose_file_button.pack(padx = 5, pady = 5, fill = "both", expand = True)
    export_table_button.pack(padx = 5, pady = 5, fill = "both", expand = True)
    buttons_frame.grid(row = 0, column = 0, pady = (5, 0))

            # Find & Replace
    find_what_label.pack(pady = (5, 0))
    find_what.pack(padx = 10)
    replace_with_label.pack(pady = (5,0))
    replace_with.pack(padx = 10)
    replace_button.pack(pady = 10)
    replace_frame.grid(row = 1, column = 0)

            # Delete selected rows
    delete_selected_rows_label.pack(padx = 5, pady = (5, 0))
    delete_selected_rows_button.pack(pady = 10)
    delete_selected_rows_frame.grid(row = 2, column = 0, padx = 10)

            # Delete selected column
    delete_selected_column_label.pack(padx = 5, pady = 5)
    delete_selected_column_dropdown.pack(padx = 5, pady = 5)
    delete_selected_column_button.pack(padx = 5, pady = 5)
    delete_selected_column_frame.grid(row = 3, column = 0, padx = 10)


        # Table frame
    table_layout.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)
    xs.grid(row = 1, column = 0, sticky = "ew")
    ys.grid(row = 0, column = 1, sticky = "ns")
    table_frame.rowconfigure(0, weight = 1)
    table_frame.columnconfigure(0, weight = 1)

###########################
    app.mainloop()



# Functions
###########################
def open_file() -> str: # Returns file path.
    file_path = askopenfilename(
        title = "Select your CSV file",
        defaultextension = ".csv",
        filetypes = [("CSV files", "*.csv")]
    )
    return file_path

def return_data_frame(file_path: str, names: Union[tuple, list]): # Asks for a file path and column names and returns a data frame.
    return(pd.read_csv(
        file_path,
        skiprows = 1,
        names = names
        )
    )

def create_table_headings(file_path: str) -> tuple:
    number_of_columns_in_a_header_row = 0
    max_number_of_columns_in_a_file = 0
    with open(file_path, "r", newline = "", encoding = 'utf-8-sig') as file:
        header_row = next(csv.reader(file)) # Using csv.reader() here fixes the issue with quoted fields in the header row like "Yields of Corporate Bonds : O.T.C (3-year, AA-)".
        number_of_columns_in_a_header_row = len(header_row)
        column_names = tuple(header_row)
        reader = csv.reader(file)
        for row in reader:
            max_number_of_columns_in_a_file = max(max_number_of_columns_in_a_file, len(row))
    if max_number_of_columns_in_a_file > number_of_columns_in_a_header_row:
        result = messagebox.askquestion(
            "Null column headers found",
            f"Your file contains data in {max_number_of_columns_in_a_file} columns but only {number_of_columns_in_a_header_row} headers were found. Do you want to add {max_number_of_columns_in_a_file - number_of_columns_in_a_header_row} dummy column headers in order to proceed?"
        )
        if result == "yes":
            return tuple([f"column{i}" if i > len(column_names) else column_names[i-1].strip().replace("\"", "").title() for i in range(1, max_number_of_columns_in_a_file + 1)])
    elif max_number_of_columns_in_a_file == number_of_columns_in_a_header_row:
        return tuple([f"column{i}" if i > len(column_names) else column_names[i-1].strip().replace("\"", "").title() for i in range(1, max_number_of_columns_in_a_file + 1)])


def create_table(widget, combobox):
    for item in widget.get_children(): # This part clears the table.
        widget.delete(item)

    try:
        file_path = open_file()
        column_names = create_table_headings(file_path)
        if column_names:
            #print(column_names)
            widget["columns"] = column_names
            combobox["values"] = column_names # This line appends column names to the dropdown menu for column deletion.
            for column in widget["columns"]:
                widget.heading(column, text = column)
            data_frame = return_data_frame(file_path, column_names)
            for column, row in data_frame.iterrows():
                widget.insert(
                    parent = "",
                    index = "end",
                    values = tuple(row)
                )
        else:
            None
    except FileNotFoundError:
        None

# def row_selection(widget):
#     for row in widget.selection():
#         print(widget.item(row)["values"])
#         print(widget.item(row))

def delete_selected_rows(widget):
    for row in widget.selection():
        widget.delete(row)

def replace_values(widget, values_to_replace: tuple):
    old_values = []
    new_values = []
    for i in widget.get_children():
        old_values.append(str(widget.item(i)["values"]))
        new_values.append([str(values_to_replace[1]) if str(x) == str(values_to_replace[0]) else str(x) for x in widget.item(i)["values"]])
    for item in widget.get_children(): # This part clears the table.
        widget.delete(item)
    for row in new_values:
        widget.insert(
            parent = "",
            index = "end",
            values = tuple(row)
        )

def export_table(widget):
    headers = [widget.heading(col)["text"] for col in widget["columns"]]
    items = [widget.item(item)["values"] for item in widget.get_children()]
    file_path = asksaveasfilename(
            title = "Save your CSV file",
            defaultextension = ".csv",
            filetypes = [("CSV files", "*.csv")]
        )
    if file_path:
        with open(
            file_path,
            "w",
            newline = ""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in items:
                writer.writerow(row)


def delete_selected_column(combobox_variable, widget, combobox):
    selected_column = combobox_variable.get()
    selected_column_id = None
    columns = widget["column"]
    column_info = []
    for i in columns:
        column_info.append({i: columns.index(i)})
    for dict in column_info:
        for key in dict:
            if key == selected_column:
                selected_column_id = dict[key]

    new_table_content = []
    for item in widget.get_children():
        new_table_content.append([x for x in widget.item(item)["values"] if widget.item(item)["values"].index(x) != selected_column_id])

    new_column_headers = []
    new_column_headers = [x for x in columns if columns.index(x) != selected_column_id]

    for item in widget.get_children(): # This part clears the table.
        widget.delete(item)

    combobox["values"] = new_column_headers # This part updates the dropdown menu.

    try: # This part sets the current dropdown item to the new available item and deletes the widget if user deletes all columns.
        if selected_column_id != None:
            combobox.set(new_column_headers[0])
    except IndexError:
        widget.delete()
    widget["columns"] = tuple(new_column_headers)
    for column in widget["columns"]:
        widget.heading(column, text = column)

    for row in new_table_content:
        widget.insert(
            parent = "",
            index = "end",
            values = tuple(row)
        )

###########################

if __name__ == "__main__":
    main()
