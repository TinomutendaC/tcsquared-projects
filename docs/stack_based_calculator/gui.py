"""
gui.py
------
Group 6 - Expression Evaluator (Stack-Based Calculator)
CUITM205 Mini Project

Tkinter front-end for the calculator. This module only handles the
graphical interface (display, buttons, history panel) and delegates
all calculation logic to evaluator.py, keeping the project modular:

    data_structures.py  -> Stack, Queue
    evaluator.py         -> Shunting-Yard + Postfix Evaluation algorithms
    gui.py (this file)   -> Tkinter GUI
    main.py               -> entry point
"""

import tkinter as tk
from tkinter import font as tkfont

from evaluator import evaluate_expression, ExpressionError


BG_COLOR = "#1e1e2f"
DISPLAY_BG = "#282a3a"
BTN_NUM_BG = "#3a3d5c"
BTN_OP_BG = "#5b5f97"
BTN_EQUAL_BG = "#4caf50"
BTN_CLEAR_BG = "#e05263"
TEXT_COLOR = "#f5f5f5"
HISTORY_BG = "#24263a"


class CalculatorApp:
    """Main GUI application class."""

    def __init__(self, root):
        self.root = root
        self.root.title("Group 6 - Stack-Based Expression Evaluator")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.expression = tk.StringVar(value="")
        self.history = []  # simple in-memory calculation history

        self._build_ui()
        self._bind_keys()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        display_font = tkfont.Font(family="Consolas", size=22)
        postfix_font = tkfont.Font(family="Consolas", size=11)
        btn_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")

        container = tk.Frame(self.root, bg=BG_COLOR, padx=12, pady=12)
        container.grid(row=0, column=0)

        # --- Display -----------------------------------------------------
        display_frame = tk.Frame(container, bg=DISPLAY_BG, bd=0)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10))

        self.display_entry = tk.Entry(
            display_frame,
            textvariable=self.expression,
            font=display_font,
            bg=DISPLAY_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat",
            justify="right",
            bd=10,
        )
        self.display_entry.pack(fill="x", ipady=10)

        self.postfix_label = tk.Label(
            display_frame,
            text="postfix: ",
            font=postfix_font,
            bg=DISPLAY_BG,
            fg="#9a9ec9",
            anchor="e",
        )
        self.postfix_label.pack(fill="x", padx=8, pady=(0, 6))

        # --- Buttons -------------------------------------------------------
        buttons = [
            ("C", 1, 0, BTN_CLEAR_BG), ("(", 1, 1, BTN_OP_BG), (")", 1, 2, BTN_OP_BG), ("%", 1, 3, BTN_OP_BG),
            ("7", 2, 0, BTN_NUM_BG), ("8", 2, 1, BTN_NUM_BG), ("9", 2, 2, BTN_NUM_BG), ("/", 2, 3, BTN_OP_BG),
            ("4", 3, 0, BTN_NUM_BG), ("5", 3, 1, BTN_NUM_BG), ("6", 3, 2, BTN_NUM_BG), ("*", 3, 3, BTN_OP_BG),
            ("1", 4, 0, BTN_NUM_BG), ("2", 4, 1, BTN_NUM_BG), ("3", 4, 2, BTN_NUM_BG), ("-", 4, 3, BTN_OP_BG),
            ("0", 5, 0, BTN_NUM_BG), (".", 5, 1, BTN_NUM_BG), ("^", 5, 2, BTN_OP_BG), ("+", 5, 3, BTN_OP_BG),
            ("\u2190", 6, 0, BTN_CLEAR_BG), ("History", 6, 1, BTN_OP_BG), ("=", 6, 2, BTN_EQUAL_BG, 2),
        ]

        for spec in buttons:
            if len(spec) == 4:
                label, row, col, color = spec
                colspan = 1
            else:
                label, row, col, color, colspan = spec

            command = self._make_command(label)
            btn = tk.Button(
                container,
                text=label,
                font=btn_font,
                bg=color,
                fg=TEXT_COLOR,
                activebackground=color,
                activeforeground=TEXT_COLOR,
                relief="flat",
                bd=0,
                width=5,
                height=2,
                command=command,
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

        # --- History panel (hidden until toggled) --------------------------
        self.history_visible = False
        self.history_frame = tk.Frame(container, bg=HISTORY_BG)
        self.history_listbox = tk.Listbox(
            self.history_frame,
            bg=HISTORY_BG,
            fg=TEXT_COLOR,
            font=("Consolas", 11),
            height=8,
            width=32,
            relief="flat",
            highlightthickness=0,
        )
        self.history_listbox.pack(fill="both", expand=True, padx=4, pady=4)
        self.history_listbox.bind("<<ListboxSelect>>", self._reuse_history_item)

    def _bind_keys(self):
        self.root.bind("<Return>", lambda event: self._evaluate())
        self.root.bind("<KP_Enter>", lambda event: self._evaluate())
        self.root.bind("<BackSpace>", lambda event: self._backspace())
        self.root.bind("<Escape>", lambda event: self._clear())

    # ------------------------------------------------------------------
    # Button command dispatch
    # ------------------------------------------------------------------
    def _make_command(self, label):
        if label == "C":
            return self._clear
        if label == "\u2190":
            return self._backspace
        if label == "=":
            return self._evaluate
        if label == "History":
            return self._toggle_history
        return lambda: self._append(label)

    def _append(self, char):
        self.expression.set(self.expression.get() + char)
        self.display_entry.icursor(tk.END)

    def _clear(self):
        self.expression.set("")
        self.postfix_label.config(text="postfix: ")

    def _backspace(self):
        current = self.expression.get()
        self.expression.set(current[:-1])

    def _toggle_history(self):
        self.history_visible = not self.history_visible
        if self.history_visible:
            self.history_frame.grid(row=0, column=4, rowspan=7, padx=(10, 0), sticky="nsew")
        else:
            self.history_frame.grid_forget()

    def _reuse_history_item(self, _event):
        selection = self.history_listbox.curselection()
        if not selection:
            return
        entry = self.history_listbox.get(selection[0])
        expr_part = entry.split(" = ")[0]
        self.expression.set(expr_part)

    # ------------------------------------------------------------------
    # Core action: evaluate the current expression
    # ------------------------------------------------------------------
    def _evaluate(self):
        raw_expression = self.expression.get()
        try:
            result, postfix = evaluate_expression(raw_expression)
        except ExpressionError as error:
            self.postfix_label.config(text=f"Error: {error}", fg="#ff6b6b")
            return
        except Exception as error:  # safety net for any unexpected failure
            self.postfix_label.config(text=f"Error: {error}", fg="#ff6b6b")
            return

        if result == int(result):
            display_result = str(int(result))
        else:
            display_result = f"{result:g}"

        self.postfix_label.config(text=f"postfix: {postfix}", fg="#9a9ec9")
        self.expression.set(display_result)

        history_entry = f"{raw_expression} = {display_result}"
        self.history.append(history_entry)
        self.history_listbox.insert(tk.END, history_entry)


def run():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
