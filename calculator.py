import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Python Calculator")
root.geometry("350x500")
root.resizable(False, False)

# Entry field for displaying the equation
equation = ""

def press(num):
    global equation
    equation += str(num)
    equation_field.delete(0, tk.END)
    equation_field.insert(tk.END, equation)

def equalpress():
    global equation
    try:
        total = str(eval(equation))  # Evaluate the math expression
        equation_field.delete(0, tk.END)
        equation_field.insert(tk.END, total)
        equation = total
    except:
        equation_field.delete(0, tk.END)
        equation_field.insert(tk.END, "Error")
        equation = ""

def clear():
    global equation
    equation = ""
    equation_field.delete(0, tk.END)

# Entry widget
equation_field = tk.Entry(root, font=('Arial', 20), bd=8, insertwidth=2, width=14, borderwidth=4, justify='right')
equation_field.grid(row=0, column=0, columnspan=4, pady=20)

# Button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
]

# Add buttons
for (text, row, col) in buttons:
    if text == '=':
        tk.Button(root, text=text, padx=20, pady=20, font=('Arial', 18), bg='lightgreen',
                  command=equalpress).grid(row=row, column=col, padx=5, pady=5)
    else:
        tk.Button(root, text=text, padx=20, pady=20, font=('Arial', 18),
                  command=lambda t=text: press(t)).grid(row=row, column=col, padx=5, pady=5)

# Clear button
tk.Button(root, text='C', padx=20, pady=20, font=('Arial', 18), bg='lightcoral',
          command=clear).grid(row=5, column=0, columnspan=4, sticky='we', padx=5, pady=5)

root.mainloop()
