import tkinter as tk
import math
import re


result_displayed = False
scientific_mode = False

def click_simulate(text):
    class DummyEvent:
        def __init__(self, t):
            self.widget = type("W", (), {"cget": lambda self, x: t})()
    click(DummyEvent(text))


def click(event):
    global result_displayed, scientific_mode
    
    
    
    text = event.widget.cget("text")
    
    new_input_keys = set("0123456789.()+_/×÷")
    func_keys = {"sin", "cos", "tan", "log", "sqrt", "pi"}
    
    if result_displayed and (text in func_keys or text in new_input_keys):
        entry.delete(0, tk.END)
        result_displayed = False
    
    if text == "=":
        try:
            expression = entry.get()
            expression = expression.replace("÷", "/").replace("×", "*")

            expression = re.sub(r'(\d+(\.\d+)?)%',r'(\1/100)', expression)
            
            
            result = eval(expression, {"__builtins__":None}, vars(math))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
        
        result_displayed = True
        
    
    elif text == "C":
        entry.delete(0, tk.END)
        result_displayed = False
    
    elif text == "Mode":
        toggle_mode()
        result_displayed = False

    elif text == "Basic":
        scientific_mode = False
        rebuild_buttons()
        result_displayed = False

    elif text == "Scientific":
        scientific_mode = True
        rebuild_buttons()
        result_displayed = False        

    elif text == "+/-":
        expr = entry.get()
        if not expr:
            return
            
        i = len(expr) - 1
        while i >= 0 and (expr[i].isdigit() or expr[i] == '.'):
            i -= 1

        if i >=0 and expr[i] in "+-*/":
            if expr[i] == '+':
                expr = expr[:i] + '-' + expr[i+1:]
            
            elif expr[i] == '-':
                expr = expr[:i] + '+' + expr[i+1:]
            else:
                expr = expr[:i+1] + '(-' | expr[i+1:] + ')'
        

        else:
            if expr.startswith('-'):
                expr = expr[1:]
            else:
                expr = '-' +expr

        entry.delete(0, tk.END)
        entry.insert(tk.END, expr)
    
    elif text == "%":
        expr = entry.get().strip()
        if not expr:
            return
        
        if expr[-1] in "+-*/(":
            return

        if expr[-1].isdigit() or expr[-1] == '.':
            entry.insert(tk.END, "%")
    
    else:
        if text in ("sin", "cos", "tan", "log", "sqrt"):
            entry.insert(tk.END, f"{text}(")
        elif text == "pi":
            entry.insert(tk.END, "pi")
        else:
            entry.insert(tk.END, text)
            
        result_displayed = False
        
        
def toggle_mode():
    for widget in button_frame.winfo_children():
        widget.destroy()
        
    Mode_text = [
        ["Basic"], 
        ["Scientific"], 
        ["graphing"]
    ]
    
    for row in Mode_text:
        frame = tk.Frame(button_frame)
        frame.pack()
        for btn_text in row:
            button = tk.Button(frame, text = btn_text, font = "Arial 18", padx= 20, pady= 10)
            button.pack(side = tk.LEFT, padx= 3, pady=3)
            button.bind("<Button-1>", click)
    
def rebuild_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()
        
    button_texts= [
        ["C", "+/-" , "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["Mode", "0", ".", "="]
    ]
    
    "÷" == "/"
    
    if scientific_mode:
        button_texts.insert(0, ["sin", "cos", "tan"])
        button_texts.insert(1, ["sqrt", "pi", "(", ")"])

    for row in button_texts:
        frame = tk.Frame(button_frame)
        frame.pack()
        for btn_text in row:
            button = tk.Button(frame, text = btn_text, font = "Arial 18", padx= 20, pady= 10)
            button.pack(side = tk.LEFT, padx= 5, pady=5)
            button.bind("<Button-1>", click)

def key_press(event):
    key = event.char
    
    if event.keysym == "Return":
        click_simulate("=")
    elif event.keysym == "BackSpace":
        entry.delete(len(entry.get()) - 1, tk.END)
    elif event.keysym == "Escape":
        click_simulate("C")
    elif key in "0123456789.+-*/()":
        click_simulate(key)
    elif key == "%":
        click_simulate("%")
            
    elif event.keysym in ["Return", "KP_Enter"]:
        click_simulate("=")


root = tk.Tk()
root.title("Calculator")

entry = tk.Entry(root, font="Arial 20", borderwidth = 5, relief= "sunken")
entry.pack(fill=tk.X, padx=10, pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

root.bind("<Key>", key_press)


scientific_mode = False
rebuild_buttons()
        
root.mainloop()