import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, Scrollbar, Frame
from attribute_class import *
from class_predefine import theme_folder_structure

def find_longest_common_prefix(paths):
    """
    Find the longest common prefix among a list of paths.

    Parameters:
        paths (list): List of theme paths as strings.

    Returns:
        list: Longest common prefix as a list of levels.
    """
    if not paths:
        return []

    # Split each path into a list of levels
    split_paths = [path.split("/") for path in paths]

    # Find the shortest path for boundary comparison
    min_length = min(len(path) for path in split_paths)

    common_prefix = []
    for i in range(min_length):
        # Check if all paths share the same level at index i
        level_set = {path[i] for path in split_paths}
        if len(level_set) == 1:
            common_prefix.append(level_set.pop())
        else:
            break

    return common_prefix


def validate_common_prefix(theme_structure, common_prefix):
    """
    Validate the common prefix against the theme folder structure.

    Parameters:
        theme_structure (dict): Nested dictionary representing the theme hierarchy.
        common_prefix (list): List of levels representing the common prefix.

    Returns:
        bool: True if the prefix is valid within the theme structure, False otherwise.
    """
    current_structure = theme_structure
    for level in common_prefix:
        if level in current_structure:
            current_structure = current_structure[level]
        else:
            return False  # The prefix doesn't exist in the theme structure
    return True


def find_min_common_theme(eis, theme_folder_structure):
    """
    Find the minimum common theme for the indicators (EIs).

    Parameters:
        eis (list): List of Existing Indicator objects.
        theme_folder_structure (dict): Nested dictionary representing the theme hierarchy.

    Returns:
        str: Minimum common theme path or None if no themes found.
    """
    # Extract themes from indicators
    themes = [ei.indicatorTheme for ei in eis if ei.indicatorTheme]  # Ensure indicatorTheme is not None

    if not themes:  # If themes list is empty
        print("No themes found for the provided indicators.")
        return None

    # Normalize theme paths
    themes = [theme.replace("\\", "/") for theme in themes]

    # Find the longest common prefix
    common_prefix = find_longest_common_prefix(themes)

    # Validate the common prefix against the theme folder structure
    if validate_common_prefix(theme_folder_structure, common_prefix):
        # Join the prefix back into a path
        return "/".join(common_prefix)
    else:
        print("Common prefix does not exist in the theme folder structure.")
        return None

def flatten_structure(d, parent_key='', sep=' > ', depth=0):
    items = []
    for k, v in d.items():
        # Create indentation, each level increases space or special characters
        indent = ' ' * (depth * 4)  # Use four spaces as indentation for each level
        new_key = parent_key + sep + k if parent_key else k
        display_key = indent + k  # Key for display, including indentation
        items.append((new_key, display_key))  # Store path and display key as a tuple
        if v:  # If there are child nodes under the current node, recursively add them
            items.extend(flatten_structure(v, new_key, sep=sep, depth=depth + 1))
    return items


def get_theme():
    # Create the main window
    root = tk.Tk()
    root.title("Select an Analysis Theme")
    root.geometry("600x400")

    # Use scrollbar
    frame = Frame(root, padx=20, pady=20)  # Add padding
    frame.pack(fill="both", expand=True)

    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, padx=10, pady=10)  # Container for radio buttons also adds padding

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Variable to save user's choice
    user_choice = tk.StringVar()

    # Generate radio buttons
    flattened_themes = flatten_structure(theme_folder_structure)
    for actual_key, display_key in flattened_themes:
        radio_button = ttk.Radiobutton(scrollable_frame, text=display_key, variable=user_choice, value=actual_key)
        radio_button.pack(anchor='w', pady=2)  # Add vertical spacing between each radio button

    # Add a confirmation button and set action
    def confirm_selection():
        print(f"The analysis theme you selected is: {user_choice.get()}")  # Print the selected theme
        root.quit()

    confirm_button = ttk.Button(root, text="Confirm", command=confirm_selection)
    confirm_button.pack(pady=20)

    # Run the main loop
    root.mainloop()
    # Continue execution after the window is closed
    root.destroy()
    return user_choice.get()  # Return user's choice

