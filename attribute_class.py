import pandas as pd
import tkinter as tk
from tkinter import ttk
from class_predefine import *
from uml_class import Complementary_Information, Spatial_Parameter, Temporal_Parameter, Existing_Indicator


# Define classes for data storage

class ColumnClassification:
    def __init__(self, column_name, data_type, additional_info=None):
        self.column_name = column_name
        self.data_type = data_type
        self.additional_info = additional_info

    def to_dict(self):
        return {
            "column_name": self.column_name,
            "data_type": self.data_type,
            "additional_info": self.additional_info.to_dict() if self.additional_info else None,
        }

def infer_data_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "int"
    elif pd.api.types.is_float_dtype(series):
        return "float"
    elif pd.api.types.is_string_dtype(series):
        return "text"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    else:
        return "unknown"

class Spatial_Parameter:
    def __init__(self, dataName, dataDescription, dataType, parameterCode, spatialLevel):
        self.dataName = dataName
        self.dataDescription = dataDescription
        self.dataType = dataType
        self.parameterCode = parameterCode
        self.spatialLevel = spatialLevel

    def to_dict(self):
        return {
            "dataName": self.dataName,
            "dataDescription": self.dataDescription,
            "dataType": self.dataType,
            "parameterCode": self.parameterCode,
            "spatialLevel": self.spatialLevel
        }

class Temporal_Parameter:
    def __init__(self, dataName, dataDescription, dataType, parameterCode, temporalLevel):
        self.dataName = dataName
        self.dataDescription = dataDescription
        self.dataType = dataType
        self.parameterCode = parameterCode
        self.temporalLevel = temporalLevel

    def to_dict(self):
        return {
            "dataName": self.dataName,
            "dataDescription": self.dataDescription,
            "dataType": self.dataType,
            "parameterCode": self.parameterCode,
            "temporalLevel": self.temporalLevel
        }

class ColumnClassifierApp:
    def __init__(self, root, df):
        self.root = root
        self.df = df

        self.spatial_parameters_list = []
        self.temporal_parameters_list = []
        self.indicators_list = []
        self.complementary_info_list = []

        self.spatial_vars = {}
        self.temporal_vars = {}
        self.indicator_vars = {}
        self.ci_vars = {}


        self.result = None

        self.spatial_counter = 1
        self.temporal_counter = 1
        self.indicator_counter = 1
        self.ci_counter = 1

        self.hS_F = [('COUNTRY',), ('REGION',), ('DEPARTEMENT',), ('ARRONDISSEMENT',), ('CANTON',), ('COMMUNE',), ('IRIS',), ('GEOPOINT',)]
        self.hT_F = [('YEAR',), ('QUARTER',), ('MONTH',), ('DATE',), ('WEEK',)]

        self.root.title("Column Classifier")
        self.root.geometry("800x600")

        self.setup_initial_interface()

    def setup_initial_interface(self):
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both", padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.container, orient="vertical")
        self.canvas = tk.Canvas(self.container, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        tk.Label(self.scrollable_frame, text="Get Spatial Parameters", font=("Helvetica", 16)).pack(pady=10)
        self.spatial_vars = {}

        for i, col in enumerate(self.df.columns):
            var = tk.BooleanVar()
            check = tk.Checkbutton(self.scrollable_frame, text=f"{col} (Type: {infer_data_type(self.df[col])})", variable=var)
            check.pack(anchor='w')
            self.spatial_vars[col] = var

        self.next_button = tk.Button(self.root, text="Next Step", command=self.setup_spatial_parameter_classification)
        self.next_button.pack(pady=10)

    def setup_spatial_parameter_classification(self):
        # if not any(self.spatial_vars.values()):
        #     self.ask_for_manual_input("Spatial")
        #     return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Select Spatial Level", font=("Helvetica", 16)).pack(pady=10)
        for col, var in self.spatial_vars.items():
            if var.get():
                frame = tk.Frame(self.scrollable_frame)
                frame.pack(fill='x', padx=10, pady=5)
                label = tk.Label(frame, text=f"Classify {col}:")
                label.pack(side='left')
                combo = ttk.Combobox(frame, values=[level for tuple in self.hS_F for level in tuple], state="readonly")
                combo.pack(side='left', padx=5)
                combo.set("Select Level")
                combo.bind("<<ComboboxSelected>>", lambda e, col=col, combo=combo: self.add_spatial_parameter(col, combo.get()))

        # self.spatial_vars = {col: var for col, var in self.spatial_vars.items() if var.get()}

        self.next_button.config(text="Next Step", command=self.setup_temporal_parameter_selection)

    def setup_temporal_parameter_selection(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Get Temporal Parameters", font=("Helvetica", 16)).pack(pady=10)
        self.temporal_vars = {}

        for i, col in enumerate(self.df.columns):
            if col not in self.spatial_vars or not self.spatial_vars[col].get():
                var = tk.BooleanVar()
                check = tk.Checkbutton(self.scrollable_frame, text=f"{col} (Type: {infer_data_type(self.df[col])})", variable=var)
                check.pack(anchor='w')
                self.temporal_vars[col] = var

        # self.temporal_vars = {col: var for col, var in self.temporal_vars.items() if var.get()}

        self.next_button.config(text="Next Step", command=self.setup_temporal_parameter_classification)

    def setup_temporal_parameter_classification(self):
        # if not any(self.temporal_vars.values()):
        #     print('none')
        # else :
        #     print('yes')
        # if not any(self.temporal_vars.values()):
        #     self.ask_for_manual_input("Temporal")
        #     return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Select Temporal Level", font=("Helvetica", 16)).pack(pady=10)
        for col, var in self.temporal_vars.items():
            if var.get():
                frame = tk.Frame(self.scrollable_frame)
                frame.pack(fill='x', padx=10, pady=5)
                label = tk.Label(frame, text=f"Classify {col}:")
                label.pack(side='left')
                combo = ttk.Combobox(frame, values=[level for tuple in self.hT_F for level in tuple], state="readonly")
                combo.pack(side='left', padx=5)
                combo.set("Select Level")
                combo.bind("<<ComboboxSelected>>", lambda e, col=col, combo=combo: self.add_temporal_parameter(col, combo.get()))

        self.next_button.config(text="Next Step", command=self.setup_indicator_selection)

    def ask_for_manual_input(self, param_type):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text=f"Enter {param_type} Parameter Information", font=("Helvetica", 16)).pack(pady=10)

        # Example of manual input for a parameter
        self.name_entry = tk.Entry(self.scrollable_frame)
        self.name_entry.pack()

        self.level_entry = tk.Entry(self.scrollable_frame)
        self.level_entry.pack()

        self.next_button.config(text="Next Step", command=lambda: self.create_manual_parameter(param_type))

    def create_manual_parameter(self, param_type):
        def create_manual_parameter(self, param_type):
            # 获取用户输入的参数名称和层级
            name = self.name_entry.get()
            level = self.level_entry.get()

            # 根据参数类型创建相应的参数对象
            if param_type == "Spatial":
                # 创建Spatial_Parameter对象
                new_param = Spatial_Parameter(
                    dataName=name,
                    dataDescription="Manual Description",  # 可以添加额外的输入字段让用户定义描述
                    dataType="Manual Type",  # 可以添加额外的输入字段让用户定义数据类型
                    parameterCode=f"sp{self.spatial_counter}",
                    spatialLevel=level
                )
                self.spatial_parameters_list.append(new_param)
                self.spatial_counter += 1  # 更新计数器
            elif param_type == "Temporal":
                # 创建Temporal_Parameter对象
                new_param = Temporal_Parameter(
                    dataName=name,
                    dataDescription="Manual Description",
                    dataType="Manual Type",
                    parameterCode=f"tp{self.temporal_counter}",
                    temporalLevel=level
                )
                self.temporal_parameters_list.append(new_param)
                self.temporal_counter += 1  # 更新计数器

    def add_spatial_parameter(self, col, level):
        param = Spatial_Parameter(col, "Description", "Data type", f"sp{self.spatial_counter}", level)
        self.spatial_parameters_list.append(param)
        self.spatial_counter += 1

    def add_temporal_parameter(self, col, level):
        param = Temporal_Parameter(col, "Description", "Data type", f"tp{self.temporal_counter}", level)
        self.temporal_parameters_list.append(param)
        self.temporal_counter += 1

    def add_indicator(self, col):
        param = Existing_Indicator(col, "Description", "Data type", f"ei{self.indicator_counter}")
        self.indicators_list.append(param)
        self.indicator_counter += 1

    def add_ci(self, col, related_para):
        param = Complementary_Information(col, "Description", "Data type", f"ci{self.ci_counter}", related_para)
        self.complementary_info_list.append(param)
        self.ci_counter += 1

    def setup_indicator_selection(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Get Indicator", font=("Helvetica", 16)).pack(pady=10)
        self.indicator_vars = {}

        for i, col in enumerate(self.df.columns):
            if (col not in self.spatial_vars or not self.spatial_vars[col].get()) and (col not in self.temporal_vars or not self.temporal_vars[col].get()):
                # Initialize BooleanVar
                is_numeric = pd.api.types.is_numeric_dtype(self.df[col])
                var = tk.BooleanVar(value=is_numeric)  # Set True if numeric, otherwise False
                # Create a Checkbutton for the column
                check = tk.Checkbutton(self.scrollable_frame, text=f"{col} (Type: {infer_data_type(self.df[col])})", variable=var)
                check.pack(anchor='w')
                self.indicator_vars[col] = var
                data_type = self.df[col].dtype

        self.next_button.config(text="Next Step", command=self.setup_complementary_information)

    def setup_complementary_information(self):

        for col, var in self.indicator_vars.items():
            if var.get():
                self.add_indicator(col)

        print("Columns for complementary info:", [col for col in self.df.columns if
                                                  col not in self.spatial_vars and col not in self.temporal_vars and col not in self.indicator_vars])

        spatial_values = [col for col in self.spatial_vars if self.spatial_vars[col].get()]
        temporal_values = [col for col in self.temporal_vars if self.temporal_vars[col].get()]

        combo_values = spatial_values + temporal_values  # Assuming these are direct column names

        # Clearing previous widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Set Complementary Information", font=("Helvetica", 16)).pack(pady=10)

        self.ci_vars = {}
        for i, col in enumerate(self.df.columns):
            if ((col not in self.spatial_vars or not self.spatial_vars[col].get())
                    and (col not in self.temporal_vars or not self.temporal_vars[col].get())
                    and (col not in self.indicator_vars or not self.indicator_vars[col].get())):
                label_text = f"{col} (Type: {self.df[col].dtype}):"
                frame = tk.Frame(self.scrollable_frame)
                frame.pack(fill='x', padx=5, pady=5)
                tk.Label(frame, text=label_text, font=("Helvetica", 12)).pack(side="left")

                combo = ttk.Combobox(frame, values=combo_values, state="readonly")
                combo.pack(side="left", padx=10)
                combo.set("Select")
                combo.bind("<<ComboboxSelected>>",
                           lambda e, col=col, combo=combo: self.add_ci(col,
                                                                       None if combo.get() == "Select" else combo.get()))


        # # Display options for selecting related parameter
        # related_options = [param.dataName for param in self.spatial_parameters_list + self.temporal_parameters_list]
        # self.related_parameter_var = tk.StringVar(value="Select")
        # related_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.related_parameter_var,
        #                                 values=combo_values, state="readonly")
        # related_dropdown.pack()

        self.next_button.config(text="Submit", command=self.submit)

    def submit(self):
        # Collecting complementary information
        for col, var in self.ci_vars.items():
            if var.get():
                related_param_name = self.related_parameter_var.get()
                related_param = next((param for param in self.spatial_parameters_list + self.temporal_parameters_list if param.dataName == related_param_name), None)
                ci = Complementary_Information(col, "Description", "Data Type", f"ci{self.ci_counter}", related_param)
                self.complementary_info_list.append(ci)
                self.ci_counter += 1

        self.result = {
            "Spatial Parameters": self.spatial_parameters_list,
            "Temporal Parameters": self.temporal_parameters_list,
            "Complementary Information": self.complementary_info_list,
            "Indicators": self.indicators_list
        }

        # Print all classified information
        print("Spatial Parameters:", [param.to_dict() for param in self.spatial_parameters_list])
        print("Temporal Parameters:", [param.to_dict() for param in self.temporal_parameters_list])
        print("Complementary Information:", [ci.to_dict() for ci in self.complementary_info_list])
        print("Indicators:", [param.to_dict() for param in self.indicators_list])
        self.root.destroy()

    def get_result(self):
        return self.result

# class ColumnClassifierApp:
#     def __init__(self, root, df):
#         self.root = root
#         self.df = df
#
#         # Lists to store classified column objects by type
#         self.complementary_info_list = []
#         self.spatial_parameters_list = []
#         self.temporal_parameters_list = []
#         self.indicators_list = []
#
#         self.column_objects = []  # General list for all classified columns
#
#         self.result = None
#
#         # Counters for auto-generating codes
#         self.spatial_counter = 1
#         self.temporal_counter = 1
#         self.ci_counter = 1
#         self.indicator_counter = 1
#
#         self.used_levels = set()  # To track used levels across all hierarchies
#
#         self.root.title("Column Classifier")
#         self.root.geometry("800x600")  # Set window size
#
#         tk.Label(root, text="Classify Columns", font=("Helvetica", 16)).pack(pady=10)
#
#         # Scrollable frame setup
#         container = tk.Frame(root)
#         container.pack(expand=True, fill="both", padx=10, pady=10)
#
#         canvas = tk.Canvas(container)
#         scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
#         scrollable_frame = tk.Frame(canvas)
#
#         scrollable_frame.bind(
#             "<Configure>",
#             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#         )
#
#         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)
#
#         canvas.pack(side="left", fill="both", expand=True)
#         scrollbar.pack(side="right", fill="y")
#
#         # Populate scrollable frame with column classifiers
#         for i, col in enumerate(self.df.columns):
#             tk.Label(scrollable_frame, text=f"{col} (Type: {infer_data_type(self.df[col])}):", font=("Helvetica", 12)).grid(row=i, column=0, sticky="w", padx=5, pady=5)
#
#             combo = ttk.Combobox(
#                 scrollable_frame,
#                 values=["Spatial Parameter", "Temporal Parameter", "Complementary Information", "Indicator"],
#                 state="readonly"
#             )
#             combo.grid(row=i, column=1, padx=5, pady=5)
#             combo.set("Select")
#             combo.bind("<<ComboboxSelected>>", lambda e, col=col, combo=combo: self.handle_selection(combo, col))
#
#         # Add submit button
#         submit_button = tk.Button(root, text="Submit", command=self.submit)
#         submit_button.pack(pady=10)
#
#     def handle_selection(self, combo, col):
#         selected_value = combo.get()
#         col_type = infer_data_type(self.df[col])
#         if selected_value == "Spatial Parameter":
#             self.create_spatial_parameter(col, col_type)
#         elif selected_value == "Temporal Parameter":
#             self.create_temporal_parameter(col, col_type)
#         elif selected_value == "Complementary Information":
#             self.create_complementary_info(col, col_type)
#         elif selected_value == "Indicator":
#             self.create_indicator(col, col_type)
#
#     def create_complementary_info(self, col, col_type):
#         ci_code = f"comp{self.ci_counter}"
#         self.ci_counter += 1
#
#         obj = Complementary_Information(
#             dataName=col,
#             dataDescription=f"Description for {col}",
#             dataType=col_type,
#             ciCode=ci_code
#         )
#         self.complementary_info_list.append(obj)
#         self.column_objects.append(obj)
#
#     def create_spatial_parameter(self, col, col_type):
#         param_code = f"sp{self.spatial_counter}"
#         self.spatial_counter += 1
#
#         # Combine and deduplicate spatial levels
#         available_levels = {level for group in hS_F for _, level in group}
#         spatial_level = self.select_level("Select Spatial Level", sorted(available_levels))
#         self.used_levels.add(spatial_level)
#
#         obj = Spatial_Parameter(
#             dataName=col,
#             dataDescription=f"Description for {col}",
#             dataType=col_type,
#             parameterCode=param_code,
#             spatialLevel=spatial_level
#         )
#         self.spatial_parameters_list.append(obj)
#         self.column_objects.append(obj)
#
#     def create_temporal_parameter(self, col, col_type):
#         param_code = f"tp{self.temporal_counter}"
#         self.temporal_counter += 1
#
#         # Combine and deduplicate temporal levels
#         available_levels = {level for group in hT_F for _, level in group}
#         temporal_level = self.select_level("Select Temporal Level", sorted(available_levels))
#         self.used_levels.add(temporal_level)
#
#         obj = Temporal_Parameter(
#             dataName=col,
#             dataDescription=f"Description for {col}",
#             dataType=col_type,
#             parameterCode=param_code,
#             temporalLevel=temporal_level
#         )
#         self.temporal_parameters_list.append(obj)
#         self.column_objects.append(obj)
#
#     def create_indicator(self, col, col_type):
#         indicator_code = f"ind{self.indicator_counter}"
#         self.indicator_counter += 1
#
#         obj = Existing_Indicator(
#             dataName=col,
#             dataDescription=f"Description for {col}",
#             dataType=col_type,
#             indicatorCode=indicator_code
#         )
#         self.indicators_list.append(obj)
#         self.column_objects.append(obj)
#
#     def select_level(self, title, available_levels):
#         """
#         Display a selection window with a fixed list of levels.
#
#         Parameters:
#             title (str): Title of the selection window.
#             available_levels (list): List of levels to display in the window.
#
#         Returns:
#             str: The selected level.
#         """
#         # Create a new window for level selection
#         level_window = tk.Toplevel(self.root)
#         level_window.title(title)
#
#         # Create a Listbox and populate it with all available levels
#         level_listbox = tk.Listbox(level_window, height=10, width=50)
#         for level in available_levels:
#             level_listbox.insert(tk.END, level)
#         level_listbox.pack(pady=10)
#
#         # Variable to store the selected level
#         selected_level = tk.StringVar()
#
#         # Function to confirm the selection
#         def confirm_selection():
#             selected = level_listbox.curselection()  # Get selected index
#             if selected:  # If a selection is made
#                 selected_level.set(level_listbox.get(selected))  # Get the value
#             else:
#                 selected_level.set("")  # Set to empty string if nothing is selected
#             level_window.destroy()  # Close the window
#
#         # Add Confirm button
#         confirm_btn = tk.Button(level_window, text="Confirm", command=confirm_selection)
#         confirm_btn.pack(pady=10)
#
#         # Wait for the user to make a selection
#         level_window.wait_window()
#
#         # Return the selected level
#         return selected_level.get()
#
#     def submit(self):
#         # Prepare the result dictionary
#         self.result = {
#             "Spatial Parameters": self.spatial_parameters_list,
#             "Temporal Parameters": self.temporal_parameters_list,
#             "Complementary Information": self.complementary_info_list,
#             "Indicators": self.indicators_list
#         }
#
#         # Print the classified data (optional)
#         print("Classified Columns:")
#
#         print("\nSpatial Parameters:")
#         for obj in self.spatial_parameters_list:
#             print(obj.to_dict())
#
#         print("\nTemporal Parameters:")
#         for obj in self.temporal_parameters_list:
#             print(obj.to_dict())
#
#         print("\nComplementary Information:")
#         for obj in self.complementary_info_list:
#             print(obj.to_dict())
#
#         print("\nIndicators:")
#         for obj in self.indicators_list:
#             print(obj.to_dict())
#
#         self.root.destroy()  # Close the Tkinter window
#
#     def get_result(self):
#         return self.result
