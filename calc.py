import tkinter as tk
import math
from fractions import Fraction

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - Office Theme")
        self.root.geometry("350x390")
        self.root.configure(bg="#3E2C23")

        self.input_var = tk.StringVar()
        self.is_fraction = False
        self.is_degree = True

        self.frac_btn = None
        self.mode_btn = None

        self.display = tk.Entry(
            root, textvariable=self.input_var, font=("Helvetica", 20),
            bg="#5A3E36", fg="white", bd=0, insertbackground="white", relief=tk.FLAT
        )
        self.display.grid(row=0, column=0, columnspan=5, pady=5, sticky="nsew")

        self.build_interface()

    def build_interface(self):
        keys = [
            ['sin', 'cos', 'tan', '^2', 'Del'],
            ['7', '8', '9', '/', 'log(x)'],
            ['4', '5', '6', '*', '1/x'],
            ['1', '2', '3', '-', 'x!'],
            ['0', '.', 'C', '+', 'sqrt'],
            ['Frac', 'Deg/Rad','=']
        ]
        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                bg = "#8C5C44" if key in {'Del', 'C', '='} else "#D2A679"
                fg = "white" if key in {'Del', 'C', '='} else "black"
                active = "#A97142" if key not in {'Frac', 'Deg/Rad'} else "#3B2F2F"

                btn = tk.Button(
                    self.root, text=key, width=5, height=2,
                    font=("Helvetica", 14, "bold"),
                    bg=bg, fg=fg,
                    activebackground=active, activeforeground="white",
                    command=lambda k=key: self.on_click(k)
                )
                btn.grid(row=i + 1, column=j, sticky="nsew", padx=1, pady=1)
                if key == 'Frac':
                    self.frac_btn = btn
                elif key == 'Deg/Rad':
                    self.mode_btn = btn
            self.root.rowconfigure(i + 1, weight=1)
        for j in range(5):
            self.root.columnconfigure(j, weight=1)

        self.update_toggle_colors()
    def on_click(self, key):
        try:
            text = self.display.get()
            if key == '=':
                result = eval(text)
                if self.is_fraction:
                    result = Fraction(result).limit_denominator()
                self.input_var.set(result)
            elif key == 'C':
                self.input_var.set("")
            elif key == 'Del':
                self.input_var.set(text[:-1])
            elif key == 'Frac':
                self.is_fraction = not self.is_fraction
                self.update_toggle_colors()
            elif key == 'Deg/Rad':
                self.is_degree = not self.is_degree
                self.update_toggle_colors()
            elif key in ('sin', 'cos', 'tan'):
                angle = float(text)
                radians = math.radians(angle) if self.is_degree else angle
                if key == 'sin':
                    result = math.sin(radians)
                elif key == 'cos':
                    result = math.cos(radians)
                else:  
                    if self.is_degree and angle % 180 == 90:
                        self.input_var.set("Undefined")
                        return
                    result = math.tan(radians)
                self.input_var.set(self.format_output(result))
            elif key == '^2':
                result = float(text) ** 2
                self.input_var.set(self.format_output(result))
            elif key == 'log(x)':
                result = math.log10(float(text))
                self.input_var.set(self.format_output(result))
            elif key == '1/x':
                result = 1 / float(text)
                self.input_var.set(self.format_output(result))
            elif key == 'x!':
                result = math.factorial(int(text))
                self.input_var.set(result)
            elif key == '10^x':
                result = 10 ** float(text)
                self.input_var.set(self.format_output(result))
            elif key == 'sqrt':
                result = math.sqrt(float(text))
                self.input_var.set(self.format_output(result))
            else:
                self.input_var.set(text + key)
        except Exception:
            self.input_var.set("Error")
    def update_toggle_colors(self):
        if self.frac_btn:
            self.frac_btn.config(
                bg="#8B4513" if self.is_fraction else "#D2A679",
                fg="black"
            )
        if self.mode_btn:
            self.mode_btn.config(
                bg="#8B4513" if self.is_degree else "#D2A679",
                fg="black"
            )
    def format_output(self, val):
        if self.is_fraction:
            return str(Fraction(val).limit_denominator())
        return str(val)
if __name__ == '__main__':
    app_root = tk.Tk()
    calc = ScientificCalculator(app_root)
    app_root.mainloop()
