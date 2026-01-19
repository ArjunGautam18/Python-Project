import tkinter as tk
from tkinter import ttk

def length_converter(value, from_unit, to_unit):
    conversion_factor = {
        "meters": 1,
        "kilometers": 1000,
        "inches": 0.0254,
        "feet": 0.3048
    }
    return value * conversion_factor[from_unit] / conversion_factor[to_unit]

def convert_units():
    try:
        value = float(entry_value.get())
        category = combo_category.get()
        from_unit = combo_from.get()
        to_unit = combo_to.get()

        if category == "Length":
            result = length_converter(value, from_unit, to_unit)
        else:
            result = 0

        label_result.config(text=f"Result: {result:.2f} {to_unit}")

    except ValueError:
        label_result.config(text="Please put a valid number.")

# Main application window
root = tk.Tk()
root.title("Unit Converter")
root.geometry("400x300")

# Dropdown category
label_category = tk.Label(root, text="Select Category:")
label_category.pack(pady=5)
combo_category = ttk.Combobox(root, values=["Length"], state="readonly")
combo_category.current(0)
combo_category.pack(pady=5)

# Dropdown for "from" unit
label_from = tk.Label(root, text="Convert:")
label_from.pack(pady=5)
combo_from = ttk.Combobox(
    root,
    values=["meters", "kilometers", "inches", "feet"],
    state="readonly"
)
combo_from.current(0)
combo_from.pack(pady=5)

# Dropdown for "to" unit
label_to = tk.Label(root, text="Convert to:")
label_to.pack(pady=5)
combo_to = ttk.Combobox(
    root,
    values=["meters", "kilometers", "inches", "feet"],
    state="readonly"
)
combo_to.current(1)
combo_to.pack(pady=5)

# Entry for value input
label_value = tk.Label(root, text="Enter Value:")
label_value.pack(pady=5)
entry_value = tk.Entry(root)
entry_value.pack(pady=5)

# Button to perform conversion
button_convert = tk.Button(root, text="Convert", command=convert_units)
button_convert.pack(pady=11)

# Label to display result
label_result = tk.Label(root, text="Result:", font=("Arial", 14))
label_result.pack(pady=22)

# Run the application
root.mainloop()
