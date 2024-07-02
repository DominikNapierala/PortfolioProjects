import pandas as pd
import tkinter as tk
import seaborn as sns
import matplotlib.pyplot as plt
import customtkinter as ctk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
from tkinter import messagebox
from typing import Union
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    sns.set_theme(font = "Bahnschrift", font_scale = 2)
    app_window()

def app_window():
    app = ctk.CTk() # This line creates the instance of the app.
    app.geometry("1000x610")
    app.wm_minsize(1000, 610)
    app.title("CSV file modifier and data visualizer")
    global button_font
    button_font = ctk.CTkFont(family="Bahnschrift Condensed", size = 20)
    global label_font
    label_font = ctk.CTkFont(family="Bahnschrift Condensed", size = 18)

    treeview_item_font = ("Bahnschrift Condensed", 20)
    style = ttk.Style()
    style.configure('Treeview', font = treeview_item_font, rowheight = 30)
    style.configure('Treeview.Heading', font = (treeview_item_font[0], treeview_item_font[1] + 2))

    border_color = "#84A98C" 

# Frames
###########################
    # Notebooks
    notebook_controls = ctk.CTkTabview(
        app,
        width = 250,
        fg_color = "#84A98C",
        segmented_button_fg_color = "#52796F",
        segmented_button_selected_color = "#ccff33",
        segmented_button_selected_hover_color = "#52796F",
        text_color = "#2F3E46"
    )
    data_options_tab = notebook_controls.add("Data")
    viz_options_tab = notebook_controls.add("Graphs")

    notebook_table_viz = ctk.CTkTabview(
        app,
        fg_color = "#84A98C",
        segmented_button_fg_color = "#52796F",
        segmented_button_selected_color = "#ccff33",
        segmented_button_selected_hover_color = "#52796F",
        text_color = "#2F3E46"
    )
    table_tab = notebook_table_viz.add("Table")
    viz_tab = notebook_table_viz.add("Visualization")
    ###########################

    # Controls notebook frames
    controls_frame = ctk.CTkFrame(
        master = data_options_tab,
        border_width = 1,
        border_color = border_color
    )

    visualize_data_frame = ctk.CTkFrame(
        master = viz_options_tab,
        border_width = 1,
        border_color = border_color
    )
    ###########################

    # Table & viz notebook frames
    table_frame = ctk.CTkFrame(
        master = table_tab,
        border_width = 0,
        border_color = border_color
    )

    viz_frame = ctk.CTkFrame(
        master = viz_tab,
        border_width = 1,
        border_color = border_color
    )
    ###########################

    buttons_frame = ctk.CTkFrame(
        master = controls_frame,
        border_width = 1,
        border_color = border_color,
        fg_color = "#e9ecef"
    )

    replace_frame = ctk.CTkFrame(
        master = controls_frame,
        border_width = 1,
        border_color = border_color,
        fg_color = "#e9ecef"
    )

    delete_selected_rows_frame = ctk.CTkFrame(
        master = controls_frame,
        border_width = 1,
        border_color = border_color,
        fg_color = "#e9ecef"
    )

    delete_selected_column_frame = ctk.CTkFrame(
        master = controls_frame,
        border_width = 1,
        border_color = border_color,
        fg_color = "#e9ecef"
    )

    ###########################
    # notebook_controls.add(controls_frame, text = "data")
    # notebook_controls.add(visualize_data_frame, text = "viz")

    # notebook_table_viz.add(table_frame, text = "table")
    # notebook_table_viz.add(viz_frame, text = "viz")

###########################

# Widgets
###########################

    # Buttons
    ###########################
    choose_file_button = ctk.CTkButton(
        master = buttons_frame,
        text = "Select CSV file",
        command = lambda: create_table(table_layout, delete_selected_column_dropdown),
        font = button_font
    )

    export_table_button = ctk.CTkButton(
        master = buttons_frame,
        text = "Export table",
        command = lambda: export_table(table_layout),
        font = button_font
    )

    # dummy_button = ctk.CTkButton(
    #     master = buttons_frame,
    #     text = "table content",
    #     command = lambda: get_table_content(table_layout)
    # )

    # Table
    ###########################
    table_layout = ttk.Treeview(
        master = table_frame,
        columns = (),
        show = "headings"
    )

    ys = ctk.CTkScrollbar(
        master = table_frame,
        orientation = 'vertical',
        command = table_layout.yview
    )

    xs = ctk.CTkScrollbar(
        master = table_frame,
        orientation = 'horizontal',
        command = table_layout.xview
    )

    table_layout['yscrollcommand'] = ys.set
    table_layout['xscrollcommand'] = xs.set

    # Find & Replace
    ###########################

        # Variables
    find_what_var = ctk.StringVar()
    replace_with_var = ctk.StringVar()

        # Widgets
    find_what_label = ctk.CTkLabel(
        master = replace_frame,
        text = "Find:",
        font = label_font
    )

    find_what = ctk.CTkEntry(
        master = replace_frame,
        textvariable = find_what_var
    )

    replace_with_label = ctk.CTkLabel(
        master = replace_frame,
        text = "Replace with:",
        font = label_font
    )

    replace_with = ctk.CTkEntry(
        master = replace_frame,
        textvariable = replace_with_var
    )

    replace_button = ctk.CTkButton(
        master = replace_frame,
        text = "Replace",
        command = lambda: replace_values(table_layout, tuple([find_what_var.get(), replace_with_var.get()])),
        font = button_font
    )

    # Remove selected rows
    ###########################

        # Widgets
    delete_selected_rows_label = ctk.CTkLabel(
        master = delete_selected_rows_frame,
        text = "Select rows you want to delete.",
        font = label_font
    )

    delete_selected_rows_button = ctk.CTkButton(
        master = delete_selected_rows_frame,
        text = "Delete rows",
        command = lambda: delete_selected_rows(table_layout),
        font = button_font
    )

    # Remove selected column
    ###########################
        # Variables
    dropdown_menu_value = ctk.StringVar(value = "...")

        # Widgets
    delete_selected_column_label = ctk.CTkLabel(
        master = delete_selected_column_frame,
        text = "Select a column to delete.",
        font = label_font
    )
    delete_selected_column_dropdown = ctk.CTkComboBox(
        master = delete_selected_column_frame,
        state = "readonly",
        variable = dropdown_menu_value,
        font = label_font,
        dropdown_font = label_font
    )
    delete_selected_column_button = ctk.CTkButton(
        master = delete_selected_column_frame,
        text = "Delete",
        command = lambda: delete_selected_column(dropdown_menu_value, table_layout, delete_selected_column_dropdown),
        font = button_font
    )

    # Viz types
    ###########################
        # Barplot
    # barplot_label = ctk.CTkLabel(
    #     master = barplot_frame,
    #     text = "Barplot"
    # )

    barplot_button = ctk.CTkButton(
        master = visualize_data_frame,
        text = "Barplot",
        command = lambda: barplot_options(table_layout, viz_canvas),
        font = button_font
    )

        # Lineplot
    # lineplot_label = ctk.CTkLabel(
    #     master = lineplot_frame,
    #     text = "Lineplot"
    # )

    lineplot_button = ctk.CTkButton(
        master = visualize_data_frame,
        text = "Lineplot",
        command = lambda: lineplot_options(table_layout, viz_canvas),
        font = button_font
    )

        # Scatterplot
    # scatterplot_label = ctk.CTkLabel(
    #     master = scatterplot_frame,
    #     text = "Scatterplot"
    # )

    scatterplot_button = ctk.CTkButton(
        master = visualize_data_frame,
        text = "Scatterplot",
        command = lambda: scatterplot_options(table_layout, viz_canvas),
        font = button_font
    )

        # Boxplot
    # boxplot_label = ctk.CTkLabel(
    #     master = boxplot_frame,
    #     text = "Boxplot"
    # )

    boxplot_button = ctk.CTkButton(
        master = visualize_data_frame,
        text = "Boxplot",
        command = lambda: boxplot_options(table_layout, viz_canvas),
        font = button_font
    )

    # Viz canvas
    ###########################
    fig = plt.Figure()
    fig.patch.set_facecolor((200/255, 210/255, 195/255))
    viz_canvas = FigureCanvasTkAgg(
        fig,
        master = viz_frame
    )

# When you use the bind method on a Tkinter widget, the callback function you bind to the event always receives an event object as its first parameter.
# table_layout.bind("<<TreeviewSelect>>", lambda event: row_selection(table_layout))

    # table_layout.bind("<Button-1>", lambda event: selected_column(table_layout, event))

###########################

# Packing
###########################
    # Frames
    notebook_controls.grid(
        row = 0,
        column = 0,
        sticky = "nsew",
        padx = (10, 5),
        pady = 10
    )

    notebook_table_viz.grid(
        row = 0,
        column = 1,
        sticky = "nsew",
        padx = (5, 10),
        pady = 10
    )

    # Widgets
    app.rowconfigure(0, weight = 1)
    app.columnconfigure(1, weight = 1)
    controls_frame.pack(fill = "both", expand = True)
    controls_frame.rowconfigure((0, 1, 2, 3), weight = 1)
    controls_frame.columnconfigure(0, weight = 1)
    visualize_data_frame.pack(fill = "both", expand = True)
    visualize_data_frame.rowconfigure((0, 1, 2, 3), weight = 1)
    visualize_data_frame.columnconfigure(0, weight = 1)

        # Controls frame
            # Buttons
    choose_file_button.pack(padx = 5, pady = 5, fill = "both", expand = True)
    export_table_button.pack(padx = 5, pady = 5, fill = "both", expand = True)
    buttons_frame.grid(row = 0, column = 0, pady = (5, 0))
    # dummy_button.pack()

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
    delete_selected_column_frame.grid(row = 3, column = 0, padx = 10, pady = (0, 5))

        # Table frame
    table_layout.grid(row = 0, column = 0, sticky = "nsew", padx = 10, pady = 10)
    xs.grid(row = 1, column = 0, sticky = "ew", padx = 5, pady = (0, 5))
    ys.grid(row = 0, column = 1, sticky = "ns", padx = (0, 5), pady = 5)
    table_frame.pack(fill = "both", expand = True)
    table_frame.rowconfigure(0, weight = 1)
    table_frame.columnconfigure(0, weight = 1)

        # Viz frame
    viz_frame.pack(fill = "both", expand = True)
    viz_canvas.get_tk_widget().pack(
        fill = "both",
        expand = True
    )

        # Viz types frame
            # Barplot
    # barplot_label.pack(padx = 5, pady = (5, 0), anchor = "center")
    # barplot_button.pack(padx = 5, pady = (0, 5))
    barplot_button.grid(row = 0, column = 0, padx = 5, pady = 5)

            # Lineplot
    # lineplot_label.pack(padx = 5, pady = (5, 0), anchor = "center")
    # lineplot_button.pack(padx = 5, pady = (0, 5))
    lineplot_button.grid(row = 1, column = 0,
                        #sticky = "nsew",
                        padx = 5, pady = 5)

            # Scatterplot
    # scatterplot_label.pack(padx = 5, pady = (5, 0), anchor = "center")
    # scatterplot_button.pack(padx = 5, pady = (0, 5))
    scatterplot_button.grid(row = 2, column = 0, padx = 5, pady = 5)

            # Boxplot
    # boxplot_label.pack(padx = 5, pady = (5, 0), anchor = "center")
    # boxplot_button.pack(padx = 5, pady = (0, 5))
    boxplot_button.grid(row = 3, column = 0, padx = 5, pady = 5)

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
            combobox["values"] = combobox.configure(values = column_names) # This line appends column names to the dropdown menu for column deletion.
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

def get_table_content(widget):
    current_column_headers = list(widget["column"])
    current_table_content = []
    for item in widget.get_children():
        # current_table_content.append([x for x in widget.item(item)["values"]]) # This solution doesnt work for some reason.
        current_table_content.append(widget.item(item)["values"])

    data_frame = pd.DataFrame(
        data = current_table_content,
        columns = current_column_headers
        )

    return current_column_headers, current_table_content, data_frame



def delete_selected_column(combobox_variable, widget, combobox):
    selected_column = combobox_variable.get()
    columns = list(widget["columns"])
    
    if selected_column in columns:
        selected_column_id = columns.index(selected_column)
    else:
        return

    new_table_content = []
    for item in widget.get_children():
        values = list(widget.item(item)["values"])
        del values[selected_column_id]
        new_table_content.append(values)

    new_column_headers = [col for i, col in enumerate(columns) if i != selected_column_id]
    
    for item in widget.get_children():  # Clear the table.
        widget.delete(item)

    combobox["values"] = combobox.configure(values = new_column_headers)  # Update the dropdown menu.

    if new_column_headers:
        combobox.set(new_column_headers[0])
    else:
        combobox.set("")

    widget["columns"] = new_column_headers
    for column in widget["columns"]:
        widget.heading(column, text=column)

    for row in new_table_content:
        widget.insert(
            parent = "",
            index = "end",
            values = tuple(row)
        )

def barplot_show(data, **kwargs):
    plot_parameters = {
        "data": data
    }

    try:
        if kwargs["hue_column"] != "...":
            if kwargs["hue_dtype"] != "...":
                data[kwargs["hue_column"]] = data[kwargs["hue_column"]].astype(kwargs["hue_dtype"])
                plot_parameters["hue"] = kwargs["hue_column"]

        if kwargs["colorpalette"] != "...":
                plot_parameters["palette"] = kwargs["colorpalette"]

# These two blocks must be true for the program to show the graph.
#########################################################################################################
        if kwargs["x_column"] != "...":
            if kwargs["x_dtype"] != "...":
                data[kwargs["x_column"]] = data[kwargs["x_column"]].astype(kwargs["x_dtype"])
                plot_parameters["x"] = kwargs["x_column"]

                if kwargs["y_column"] != "...":
                    if kwargs["y_dtype"] != "...":
                        data[kwargs["y_column"]] = data[kwargs["y_column"]].astype(kwargs["y_dtype"])
                        plot_parameters["y"] = kwargs["y_column"]

                        fig = kwargs["canvas"].figure
                        fig.clear()
                        ax = fig.add_subplot(111)
                        ax.set_facecolor((235/255, 235/255, 235/255))
                        # ax.tick_params(axis='x', fontname='Arial')
                        # ax.tick_params(axis='y', fontname='Arial')
                        sns.barplot(**plot_parameters, ax = ax, errorbar = None, estimator = kwargs["y_aggregation"])
                        # for p in ax.patches: # This loop iterates through each bar (patch) in the plot.
                        #     ax.annotate(
                        #         f'{p.get_height():.2f}', # 'f'{p.get_height():.2f}'' Formats the height (p.get_height()) of the bar to two decimal places (:.2f).
                        #         (p.get_x() + p.get_width() / 2., p.get_height()), # Specifies the position where the annotation text will be placed. 'p.get_x() + p.get_width() / 2.' calculates the x-coordinate at the center of the bar. 'p.get_height()' uses the bar's height as the y-coordinate for the annotation.
                        #         ha = 'center',
                        #         va = 'center',
                        #         fontsize = 10,
                        #         color = 'black',
                        #         xytext = (0, 5),
                        #         textcoords = 'offset points'
                        #     )
                        for container in ax.containers:  # This handles grouped bars with hue
                            ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=15, color='black')
                        kwargs["canvas"].draw()
#########################################################################################################

    except ValueError:
        messagebox.showinfo(title = "Incorrect dtype", message = "You selected an incorrect data type for one or more of your columns.")


def boxplot_show(data, **kwargs):
    plot_parameters = {
        "data": data
    }

    try:
        if kwargs["hue_column"] != "...":
            if kwargs["hue_dtype"] != "...":
                data[kwargs["hue_column"]] = data[kwargs["hue_column"]].astype(kwargs["hue_dtype"])
                plot_parameters["hue"] = kwargs["hue_column"]

        if kwargs["colorpalette"] != "...":
                plot_parameters["palette"] = kwargs["colorpalette"]

# These two blocks must be true for the program to show the graph.
#########################################################################################################
        if kwargs["x_column"] != "...":
            if kwargs["x_dtype"] != "...":
                data[kwargs["x_column"]] = data[kwargs["x_column"]].astype(kwargs["x_dtype"])
                plot_parameters["x"] = kwargs["x_column"]

                if kwargs["y_column"] != "...":
                    if kwargs["y_dtype"] != "...":
                        data[kwargs["y_column"]] = data[kwargs["y_column"]].astype(kwargs["y_dtype"])
                        plot_parameters["y"] = kwargs["y_column"]

                        fig = kwargs["canvas"].figure
                        fig.clear()
                        ax = fig.add_subplot(111)
                        ax.set_facecolor((235/255, 235/255, 235/255))
                        sns.boxplot(**plot_parameters, ax = ax)

                        kwargs["canvas"].draw()
#########################################################################################################

    except ValueError:
        messagebox.showinfo(title = "Incorrect dtype", message = "You selected an incorrect data type for one or more of your columns.")


def lineplot_show(data, **kwargs):
    plot_parameters = {
        "data": data
    }

    try:
        if kwargs["hue_column"] != "...":
            if kwargs["hue_dtype"] != "...":
                data[kwargs["hue_column"]] = data[kwargs["hue_column"]].astype(kwargs["hue_dtype"])
                plot_parameters["hue"] = kwargs["hue_column"]

        if kwargs["colorpalette"] != "...":
                plot_parameters["palette"] = kwargs["colorpalette"]

# These two blocks must be true for the program to show the graph.
#########################################################################################################
        if kwargs["x_column"] != "...":
            if kwargs["x_dtype"] != "...":
                data[kwargs["x_column"]] = data[kwargs["x_column"]].astype(kwargs["x_dtype"])
                plot_parameters["x"] = kwargs["x_column"]

                if kwargs["y_column"] != "...":
                    if kwargs["y_dtype"] != "...":
                        data[kwargs["y_column"]] = data[kwargs["y_column"]].astype(kwargs["y_dtype"])
                        plot_parameters["y"] = kwargs["y_column"]

                        fig = kwargs["canvas"].figure
                        fig.clear()
                        ax = fig.add_subplot(111)
                        ax.set_facecolor((235/255, 235/255, 235/255))
                        sns.lineplot(**plot_parameters, ax = ax, errorbar = None)

                        # for line in ax.lines: # This part generates a label for each data point but it looks bad. Too crowded.
                        #     x_data = line.get_xdata()
                        #     y_data = line.get_ydata()
                        #     for i, (x, y) in enumerate(zip(x_data, y_data)):
                        #         ax.text(x, y, f'{y:.2f}', color='black', fontsize=10, ha='center', va='bottom')

                        kwargs["canvas"].draw()
#########################################################################################################

    except ValueError:
        messagebox.showinfo(title = "Incorrect dtype", message = "You selected an incorrect data type for one or more of your columns.")


def scatterplot_show(data, **kwargs):
    plot_parameters = {
        "data": data
    }

# Optional arguments
#########################################################################################################
    try:
        if kwargs["hue_column"] != "...":
            if kwargs["hue_dtype"] != "...":
                data[kwargs["hue_column"]] = data[kwargs["hue_column"]].astype(kwargs["hue_dtype"])
                plot_parameters["hue"] = kwargs["hue_column"]

        if kwargs["size_column"] != "...":
            if kwargs["size_dtype"] != "...":
                data[kwargs["size_column"]] = data[kwargs["size_column"]].astype(kwargs["size_dtype"])
                plot_parameters["size"] = kwargs["size_column"]

        if kwargs["colorpalette"] != "...":
                plot_parameters["palette"] = kwargs["colorpalette"]

# These two blocks must be true for the program to show the graph.
#########################################################################################################
        if kwargs["x_column"] != "...":
            if kwargs["x_dtype"] != "...":
                data[kwargs["x_column"]] = data[kwargs["x_column"]].astype(kwargs["x_dtype"])
                plot_parameters["x"] = kwargs["x_column"]

                if kwargs["y_column"] != "...":
                    if kwargs["y_dtype"] != "...":
                        data[kwargs["y_column"]] = data[kwargs["y_column"]].astype(kwargs["y_dtype"])
                        plot_parameters["y"] = kwargs["y_column"]

                        fig = kwargs["canvas"].figure
                        fig.clear()
                        ax = fig.add_subplot(111)
                        ax.set_facecolor((235/255, 235/255, 235/255))
                        # ax.tick_params(axis='x', fontname='Arial')
                        # ax.tick_params(axis='y', fontname='Arial')
                        sns.scatterplot(**plot_parameters, ax = ax)

                        # for line in ax.lines: # This part generates a label for each data point but it looks bad. Too crowded.
                        #     x_data = line.get_xdata()
                        #     y_data = line.get_ydata()
                        #     for i, (x, y) in enumerate(zip(x_data, y_data)):
                        #         ax.text(x, y, f'{y:.2f}', color='black', fontsize=10, ha='center', va='bottom')

                        kwargs["canvas"].draw()
#########################################################################################################

    except ValueError:
        messagebox.showinfo(title = "Incorrect dtype", message = "You selected an incorrect data type for one or more of your columns.")

    # Visualization functions
###########################
def barplot_options(widget, canvas):
    column_headers, table_content, data_frame = get_table_content(widget)

    options = ctk.CTkToplevel()
    options.title("Specify barplot options")
    options.resizable(False, False)

    dummy_button = ctk.CTkButton(
        master = options,
        text = "Viz!",
        command = lambda: barplot_show(
            data = data_frame,
            x_column = x_dropdown_value.get(),
            y_column = y_dropdown_value.get(),
            x_dtype = x_dtype_value.get(),
            y_dtype = y_dtype_value.get(),
            y_aggregation = y_aggregation_value.get(),
            hue_column = hue_dropdown_value.get(),
            hue_dtype = hue_dtype_value.get(),
            colorpalette = colorpalette_dropdown_value.get(),
            canvas = canvas
        ),
        font = button_font
    )

    dummy_label = ctk.CTkLabel(
        master = options,
        text = "Data type",
        font = label_font
    )

    dummy_label_2 = ctk.CTkLabel(
        master = options,
        text = "Aggregation",
        font = label_font
    )

    x_dtype_value = ctk.StringVar(value = "...")
    x_dropdown_value = ctk.StringVar(value = "...")
    x_label = ctk.CTkLabel(
        master = options,
        text = "X: ",
        font = label_font
    )
    x = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    x_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    y_dtype_value = ctk.StringVar(value = "...")
    y_dropdown_value = ctk.StringVar(value = "...")
    y_aggregation_value = ctk.StringVar(value = "sum")
    y_label = ctk.CTkLabel(
        master = options,
        text = "Y: ",
        font = label_font
    )
    y = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    y_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )
    y_aggregation = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_aggregation_value,
        font = label_font,
        dropdown_font = label_font
    )

    hue_dtype_value = ctk.StringVar(value = "...")
    hue_dropdown_value = ctk.StringVar(value = "...")
    hue_label = ctk.CTkLabel(
        master = options,
        text = "Hue: ",
        font = label_font
    )
    hue = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    hue_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    colorpalette_dropdown_value = ctk.StringVar(value = "...")
    colorpalette_label = ctk.CTkLabel(
        master = options,
        text = "Color palette: ",
        font = label_font
    )
    colorpalette = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = colorpalette_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )

    dummy_label.grid(row = 0, column = 2)
    dummy_label_2.grid(row = 0, column = 3)
    x_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    x.grid(row = 1, column = 1, padx = 5, pady = 5)
    x_dtype.grid(row = 1, column = 2, padx = 5, pady = 5)

    y_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    y.grid(row = 2, column = 1, padx = 5, pady = 5)
    y_dtype.grid(row = 2, column = 2, padx = 5, pady = 5)
    y_aggregation.grid(row = 2, column = 3, padx = 5, pady = 5)

    hue_label.grid(row = 3, column = 0, padx = 5, pady = 5)
    hue.grid(row = 3, column = 1, padx = 5, pady = 5)
    hue_dtype.grid(row = 3, column = 2, padx = 5, pady = 5)

    colorpalette_label.grid(row = 4, column = 0, padx = 5, pady = 5)
    colorpalette.grid(row = 4, column = 1, padx = 5, pady = 5)

    dummy_button.grid(row = 5, column = 1, padx = 5, pady = 5)

    x["values"] = x.configure(values = column_headers)
    x_dtype["value"] = x_dtype.configure(values = ["string", "int", "float"])

    y["values"] = y.configure(values = column_headers)
    y_dtype["value"] = y_dtype.configure(values = ["string", "int", "float"])
    y_aggregation["value"] = y_aggregation.configure(values = ["sum", "mean", "max", "min"])

    hue["values"] = hue.configure(values = column_headers)
    hue_dtype["value"] = hue_dtype.configure(values = ["string", "int", "float"])

    colorpalette["values"] = colorpalette.configure(values = [
        "Greens",
        "Blues",
        "Oranges",
        "Purples",
        "YlOrBr",
        "YlOrRd",
        "OrRd",
        "BuGn",
        "BuPu",
        "GnBu",
        "PuBu",
        "PuBuGn",
        "YlGn",
        "YlGnBu",
        "viridis",
        "plasma",
        "magma",
        "inferno",
        "RdYlBu",
        "RdYlGn",
        "BrBG",
        "PiYG",
        "PRGn",
        "PuOr",
        "RdBu",
        "Spectral",
        "coolwarm",
        "bwr",
        "seismic"
    ])


def lineplot_options(widget, canvas):
    column_headers, table_content, data_frame = get_table_content(widget)

    options = tk.Toplevel()
    options.title("Specify lineplot options")
    options.resizable(False, False)

    dummy_button = ctk.CTkButton(
        master = options,
        text = "Viz!",
        command = lambda: lineplot_show(
            data = data_frame,
            x_column = x_dropdown_value.get(),
            y_column = y_dropdown_value.get(),
            x_dtype = x_dtype_value.get(),
            y_dtype = y_dtype_value.get(),
            hue_column = hue_dropdown_value.get(),
            hue_dtype = hue_dtype_value.get(),
            colorpalette = colorpalette_dropdown_value.get(),
            canvas = canvas
        ),
        font = button_font
    )

    dummy_label = ctk.CTkLabel(
        master = options,
        text = "dtype",
        font = label_font
    )

    x_dtype_value = ctk.StringVar(value = "...")
    x_dropdown_value = ctk.StringVar(value = "...")
    x_label = ctk.CTkLabel(
        master = options,
        text = "X: ",
        font = label_font
    )
    x = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    x_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    y_dtype_value = ctk.StringVar(value = "...")
    y_dropdown_value = ctk.StringVar(value = "...")
    y_label = ctk.CTkLabel(
        master = options,
        text = "Y: ",
        font = label_font
    )
    y = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    y_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    hue_dtype_value = ctk.StringVar(value = "...")
    hue_dropdown_value = ctk.StringVar(value = "...")
    hue_label = ctk.CTkLabel(
        master = options,
        text = "Hue: ",
        font = label_font
    )
    hue = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    hue_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    colorpalette_dropdown_value = ctk.StringVar(value = "...")
    colorpalette_label = ctk.CTkLabel(
        master = options,
        text = "Color palette: ",
        font = label_font
    )
    colorpalette = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = colorpalette_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )

    dummy_label.grid(row = 0, column = 2)
    x_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    x.grid(row = 1, column = 1, padx = 5, pady = 5)
    x_dtype.grid(row = 1, column = 2, padx = 5, pady = 5)

    y_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    y.grid(row = 2, column = 1, padx = 5, pady = 5)
    y_dtype.grid(row = 2, column = 2, padx = 5, pady = 5)

    hue_label.grid(row = 3, column = 0, padx = 5, pady = 5)
    hue.grid(row = 3, column = 1, padx = 5, pady = 5)
    hue_dtype.grid(row = 3, column = 2, padx = 5, pady = 5)

    colorpalette_label.grid(row = 4, column = 0, padx = 5, pady = 5)
    colorpalette.grid(row = 4, column = 1, padx = 5, pady = 5)

    dummy_button.grid(row = 5, column = 1, padx = 5, pady = 5)

    x["values"] = x.configure(values = column_headers)
    x_dtype["value"] = x_dtype.configure(values = ["string", "int", "float", "datetime64[ns]"])

    y["values"] = y.configure(values = column_headers)
    y_dtype["value"] = y_dtype.configure(values = ["string", "int", "float"])

    hue["values"] = hue.configure(values = column_headers)
    hue_dtype["value"] = hue_dtype.configure(values = ["string", "int", "float"])

    colorpalette["values"] = colorpalette.configure(values = [
        "Greens",
        "Blues",
        "Oranges",
        "Purples",
        "YlOrBr",
        "YlOrRd",
        "OrRd",
        "BuGn",
        "BuPu",
        "GnBu",
        "PuBu",
        "PuBuGn",
        "YlGn",
        "YlGnBu",
        "viridis",
        "plasma",
        "magma",
        "inferno",
        "RdYlBu",
        "RdYlGn",
        "BrBG",
        "PiYG",
        "PRGn",
        "PuOr",
        "RdBu",
        "Spectral",
        "coolwarm",
        "bwr",
        "seismic"
    ])

def scatterplot_options(widget, canvas):
    column_headers, table_content, data_frame = get_table_content(widget)

    options = tk.Toplevel()
    options.title("Specify scatterplot options")
    options.resizable(False, False)

    dummy_button = ctk.CTkButton(
        master = options,
        text = "Viz!",
        command = lambda: scatterplot_show(
            data = data_frame,
            x_column = x_dropdown_value.get(),
            y_column = y_dropdown_value.get(),
            x_dtype = x_dtype_value.get(),
            y_dtype = y_dtype_value.get(),
            hue_column = hue_dropdown_value.get(),
            hue_dtype = hue_dtype_value.get(),
            size_column = size_dropdown_value.get(),
            size_dtype = size_dtype_value.get(),
            colorpalette = colorpalette_dropdown_value.get(),
            canvas = canvas
        ),
        font = button_font
    )

    dummy_label = ctk.CTkLabel(
        master = options,
        text = "dtype",
        font = label_font
    )

    x_dtype_value = ctk.StringVar(value = "...")
    x_dropdown_value = ctk.StringVar(value = "...")
    x_label = ctk.CTkLabel(
        master = options,
        text = "X: ",
        font = label_font
    )
    x = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    x_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    y_dtype_value = ctk.StringVar(value = "...")
    y_dropdown_value = ctk.StringVar(value = "...")
    y_label = ctk.CTkLabel(
        master = options,
        text = "Y: ",
        font = label_font
    )
    y = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    y_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    hue_dtype_value = ctk.StringVar(value = "...")
    hue_dropdown_value = ctk.StringVar(value = "...")
    hue_label = ctk.CTkLabel(
        master = options,
        text = "Hue: ",
        font = label_font
    )
    hue = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    hue_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    size_dtype_value = ctk.StringVar(value = "...")
    size_dropdown_value = ctk.StringVar(value = "...")
    size_label = ctk.CTkLabel(
        master = options,
        text = "Size: ",
        font = label_font
    )
    size = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = size_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    size_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = size_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    colorpalette_dropdown_value = ctk.StringVar(value = "...")
    colorpalette_label = ctk.CTkLabel(
        master = options,
        text = "Color palette: ",
        font = label_font
    )
    colorpalette = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = colorpalette_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )

    dummy_label.grid(row = 0, column = 2)
    x_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    x.grid(row = 1, column = 1, padx = 5, pady = 5)
    x_dtype.grid(row = 1, column = 2, padx = 5, pady = 5)

    y_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    y.grid(row = 2, column = 1, padx = 5, pady = 5)
    y_dtype.grid(row = 2, column = 2, padx = 5, pady = 5)

    hue_label.grid(row = 3, column = 0, padx = 5, pady = 5)
    hue.grid(row = 3, column = 1, padx = 5, pady = 5)
    hue_dtype.grid(row = 3, column = 2, padx = 5, pady = 5)

    size_label.grid(row = 4, column = 0, padx = 5, pady = 5)
    size.grid(row = 4, column = 1, padx = 5, pady = 5)
    size_dtype.grid(row = 4, column = 2, padx = 5, pady = 5)

    colorpalette_label.grid(row = 5, column = 0, padx = 5, pady = 5)
    colorpalette.grid(row = 5, column = 1, padx = 5, pady = 5)

    dummy_button.grid(row = 6, column = 1, padx = 5, pady = 5)

    x["values"] = x.configure(values = column_headers)
    x_dtype["value"] = x_dtype.configure(values = ["int", "float", "datetime64[ns]"])

    y["values"] = y.configure(values = column_headers)
    y_dtype["value"] = y_dtype.configure(values = ["int", "float"])

    hue["values"] = hue.configure(values = column_headers)
    hue_dtype["value"] = hue_dtype.configure(values = ["string", "int", "float"])

    size["values"] = size.configure(values = column_headers)
    size_dtype["value"] = size_dtype.configure(values = ["int", "float"])

    colorpalette["values"] = colorpalette.configure(values = [
        "Greens",
        "Blues",
        "Oranges",
        "Purples",
        "YlOrBr",
        "YlOrRd",
        "OrRd",
        "BuGn",
        "BuPu",
        "GnBu",
        "PuBu",
        "PuBuGn",
        "YlGn",
        "YlGnBu",
        "viridis",
        "plasma",
        "magma",
        "inferno",
        "RdYlBu",
        "RdYlGn",
        "BrBG",
        "PiYG",
        "PRGn",
        "PuOr",
        "RdBu",
        "Spectral",
        "coolwarm",
        "bwr",
        "seismic"
    ])


def boxplot_options(widget, canvas):
    column_headers, table_content, data_frame = get_table_content(widget)

    options = tk.Toplevel()
    options.title("Specify boxplot options")
    options.resizable(False, False)

    dummy_button = ctk.CTkButton(
        master = options,
        text = "Viz!",
        command = lambda: boxplot_show(
            data = data_frame,
            x_column = x_dropdown_value.get(),
            y_column = y_dropdown_value.get(),
            x_dtype = x_dtype_value.get(),
            y_dtype = y_dtype_value.get(),
            hue_column = hue_dropdown_value.get(),
            hue_dtype = hue_dtype_value.get(),
            colorpalette = colorpalette_dropdown_value.get(),
            canvas = canvas
        ),
        font = button_font
    )

    dummy_label = ctk.CTkLabel(
        master = options,
        text = "dtype",
        font = label_font
    )

    x_dtype_value = ctk.StringVar(value = "...")
    x_dropdown_value = ctk.StringVar(value = "...")
    x_label = ctk.CTkLabel(
        master = options,
        text = "X: ",
        font = label_font
    )
    x = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    x_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = x_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    y_dtype_value = ctk.StringVar(value = "...")
    y_dropdown_value = ctk.StringVar(value = "...")
    y_label = ctk.CTkLabel(
        master = options,
        text = "Y: ",
        font = label_font
    )
    y = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    y_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = y_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    hue_dtype_value = ctk.StringVar(value = "...")
    hue_dropdown_value = ctk.StringVar(value = "...")
    hue_label = ctk.CTkLabel(
        master = options,
        text = "Hue: ",
        font = label_font
    )
    hue = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )
    hue_dtype = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = hue_dtype_value,
        font = label_font,
        dropdown_font = label_font
    )

    colorpalette_dropdown_value = ctk.StringVar(value = "...")
    colorpalette_label = ctk.CTkLabel(
        master = options,
        text = "Color palette: ",
        font = label_font
    )
    colorpalette = ctk.CTkComboBox(
        master = options,
        state = "readonly",
        variable = colorpalette_dropdown_value,
        font = label_font,
        dropdown_font = label_font
    )

    dummy_label.grid(row = 0, column = 2)
    x_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    x.grid(row = 1, column = 1, padx = 5, pady = 5)
    x_dtype.grid(row = 1, column = 2, padx = 5, pady = 5)

    y_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    y.grid(row = 2, column = 1, padx = 5, pady = 5)
    y_dtype.grid(row = 2, column = 2, padx = 5, pady = 5)

    hue_label.grid(row = 3, column = 0, padx = 5, pady = 5)
    hue.grid(row = 3, column = 1, padx = 5, pady = 5)
    hue_dtype.grid(row = 3, column = 2, padx = 5, pady = 5)

    colorpalette_label.grid(row = 5, column = 0, padx = 5, pady = 5)
    colorpalette.grid(row = 5, column = 1, padx = 5, pady = 5)

    dummy_button.grid(row = 6, column = 1, padx = 5, pady = 5)

    x["values"] = x.configure(values = column_headers)
    x_dtype["value"] = x_dtype.configure(values = ["string", "int", "float"])

    y["values"] = y.configure(values = column_headers)
    y_dtype["value"] = y_dtype.configure(values = ["int", "float"])

    hue["values"] = hue.configure(values = column_headers)
    hue_dtype["value"] = hue_dtype.configure(values = ["string", "int", "float"])

    colorpalette["values"] = colorpalette.configure(values = [
        "Greens",
        "Blues",
        "Oranges",
        "Purples",
        "YlOrBr",
        "YlOrRd",
        "OrRd",
        "BuGn",
        "BuPu",
        "GnBu",
        "PuBu",
        "PuBuGn",
        "YlGn",
        "YlGnBu",
        "viridis",
        "plasma",
        "magma",
        "inferno",
        "RdYlBu",
        "RdYlGn",
        "BrBG",
        "PiYG",
        "PRGn",
        "PuOr",
        "RdBu",
        "Spectral",
        "coolwarm",
        "bwr",
        "seismic"
    ])


###########################

if __name__ == "__main__":
    main()
