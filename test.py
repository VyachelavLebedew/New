import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import pandas as pd
from typing import Optional
from ITC_module import ITC
pd.options.mode.chained_assignment = None


BUTTON_FONT: tuple = ("Helvetica", 12, "bold")
BUTTON_PADDING: Optional[int] = 10
BACKGROUND_COLOR: str = "#ffedc0"
FOREGROUND_COLOR: str = "#454545"
BACKGROUND_COLOR_MAIN: str = "yellow"
BUTTONS: list[str] = ['Fuel loading',
                      'Crytical state',
                      'CR coupling',
                      'Imax',
                      'ITC',
                      'Symmetry',
                      'DRDH',
                      'DRWM',
                      'VOR',
                      'APP',
                      'PRC',
                      'EP']


class Main:
    """This is the main class aimed to lounch other modules."""

    def __init__(self, root):
        """To set the title and to launch other main functions."""
        self.root = root
        self.root.title('Vis')
        self.initialize_attributes()
        self.setup_ui()

    def initialize_attributes(self):
        """To set the main commands list."""
        self.buttons_tk = []
        self.COMMANDS = [self.fuel_loading,
                         self.crytical_state,
                         self.cr_coupling,
                         self.imax,
                         self.itc,
                         self.symmetry,
                         self.drdh,
                         self.drwm,
                         self.vor,
                         self.app,
                         self.pcr,
                         self.ep,
                         ]

    def setup_ui(self):
        """To create the style of base controls."""
        self._create_controls()

    def _create_controls(self):
        """To set the style of base controls."""
        style = ttk.Style()
        style.configure('TButton', font=BUTTON_FONT,
                        padding=(BUTTON_PADDING, BUTTON_PADDING),
                        relief="raised",
                        background=BACKGROUND_COLOR, foreground="#FFFFFF")
        style.configure('TCheckbutton', font=BUTTON_FONT)
        style.configure('TMenubutton', font=BUTTON_FONT)
        self._setup_top_controls()

    def display_dataframe_on_canvas(self, df, root):
        """To fill the display with the values of file obtained."""
        lst = [tuple(df.values[i]) for i in range(10)]
        columns = tuple(df.columns)
        tree = ttk.Treeview(columns=columns, show="headings")
        tree.pack(fill='both', expand=1)
        for i in columns:
            tree.heading(i, text=i)
        for i in lst:
            tree.insert("", 'end', values=i)
        scrollbar = ttk.Scrollbar(orient="horizontal", command=tree.xview)
        scrollbar.pack(side='top', fill='x')
        tree["xscrollcommand"] = scrollbar.set

    def _setup_top_controls(self):
        """To set up the top controls."""
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0")
        # self.top_frame.grid(row = 3, column = 0)
        self.top_frame.pack(pady=10)
        self.table = tk.Frame(self.top_frame)
        self.open_button = tk.Button(self.top_frame,
                                     text="Open file",
                                     width=15,
                                     command=self.open_file,
                                     bg=BACKGROUND_COLOR,
                                     fg=FOREGROUND_COLOR,
                                     font=BUTTON_FONT)
        self.start_button = tk.Button(self.top_frame,
                                      text="START",
                                      width=15,
                                      command=self.start,
                                      bg=BACKGROUND_COLOR,
                                      fg=FOREGROUND_COLOR,
                                      font=BUTTON_FONT,
                                      state='disabled')
        for i in range(len(BUTTONS)):
            button = tk.Button(self.top_frame,
                               text=BUTTONS[i],
                               width=15,
                               command=self.COMMANDS[i],
                               bg=BACKGROUND_COLOR,
                               fg=FOREGROUND_COLOR,
                               font=BUTTON_FONT,
                               state='disabled')
            button.grid(row=1, column=i, padx=10)
            self.buttons_tk += [button]
        self.open_button.grid(row=0, column=0, columnspan=6, padx=10)
        self.start_button.grid(row=0, column=3, columnspan=6, padx=10)

    def open_file(self):
        """To open and to read an initial file."""
        global df
        file_name = fd.askopenfile(filetypes=(("TXT files", "*.txt"),
                                              ("s17 files", "*.s17*"),
                                              ("All files", "*.*")))
        if file_name:
            try:
                file = pd.read_csv(file_name, sep='\t', encoding='ANSI')
                self.df = pd.DataFrame(file)
                self.display_dataframe_on_canvas(self.df, root)
                for button in self.buttons_tk:
                    button['state'] = 'normal'

                # self.auto_process()
                # Автоматически выполним действия построения графика
            except Exception as e:
                tk.messagebox.showerror("File Error",
                                        f"Failed to open file:\n{str(e)}")
        else:
            tk.messagebox.showwarning("File Selection", "No file selected.")

    def auto_process(self):
        """
        To test the mudule.

        Let us to avoid the choosing data manually - to safe
        some time.
        """
        self.lst_ITC = [1]
        self.create_sth("time", self.lst_ITC)

        self.lst_ITC = [250, 251]
        self.create_sth("reactivity", self.lst_ITC)

        self.lst_ITC = [63, 64, 65, 66]
        self.create_sth("temperature", self.lst_ITC)

        self.start()

    def fuel_loading(self):
        """To make a computings related to the fuel loading process."""
        pass

    def crytical_state(self):
        """To make a computings related to the reaching the crytical state."""
        pass

    def cr_coupling(self):
        """To make a computings related to the CR coupling checking."""
        pass

    def imax(self):
        """To make a computings to determine Imax."""
        pass

    def on_mouse_wheel(self, event):
        """Mouse control function."""
        self.window.yview("scroll", event.delta, "units")
        return "break"

    def itc(self):
        """To make a computings to determine ITC."""
        self.lst_ITC = []
        self.time_ITC = []
        self.reactivity_ITC = []
        self.temperature_ITC = []
        self.df_new = pd.DataFrame()
        self.window = tk.Toplevel(self.root)
        self.window.geometry("1000x800")  # Increase the ITC window size
        # Restrict to change the window size
        self.window.wm_resizable(False, False)
        self.canvas = tk.Canvas(self.window, borderwidth=0, bg='#ffffff')
        self.vsb = tk.Scrollbar(self.window,
                                orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.master_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.canvas.create_window((0, 0),
                                  window=self.master_frame,
                                  anchor='nw')
        self.window.bind("<MouseWheel>", self.on_mouse_wheel)
        for i in range(len(self.df.columns)):
            checkbutton = tk.Button(self.master_frame,
                                    text=self.df.columns[i],
                                    width=70,
                                    command=lambda i=i: self.one(i),
                                    bg="#f0f0f0",
                                    font=BUTTON_FONT)
            checkbutton.grid(row=i, column=0, pady=2)

        self.time_button = tk.Button(
            self.master_frame,
            text="Obtain time",
            width=20,
            command=lambda: self.create_sth(
                                        self.time_button['text'][7:],
                                        self.lst_ITC),
            bg=BACKGROUND_COLOR,
            fg=FOREGROUND_COLOR,
            font=BUTTON_FONT)
        self.reactivity_button = tk.Button(
            self.master_frame,
            text="Obtain reactivity",
            width=20,
            command=lambda: self.create_sth(
                                        self.reactivity_button['text'][7:],
                                        self.lst_ITC),
            bg=BACKGROUND_COLOR,
            fg=FOREGROUND_COLOR,
            font=BUTTON_FONT,
            state='disabled')
        self.temperature_button = tk.Button(
            self.master_frame,
            text="Obtain temperature",
            width=20,
            command=lambda: self.create_sth(
                                        self.temperature_button['text'][7:],
                                        self.lst_ITC),
            bg=BACKGROUND_COLOR,
            fg=FOREGROUND_COLOR,
            font=BUTTON_FONT,
            state='disabled',
            )
        self.time_button.grid(row=0, column=1, padx=15)
        self.reactivity_button.grid(row=1, column=1, padx=15)
        self.temperature_button.grid(row=2, column=1, padx=15)
        self.master_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def symmetry(self):
        """To make a computings related to symmetry astimating."""
        pass

    def drdh(self):
        """To make a computings to determine drdh."""
        pass

    def drwm(self):
        """To make a computings to determine."""
        pass

    def vor(self):
        """To make a computings related to VOR test."""
        pass

    def app(self):
        """To make a computings to determine APP efficiency."""
        pass

    def pcr(self):
        """To make a computings to determine PCR."""
        pass

    def ep(self):
        """To make a computings to determine APP efficiency."""
        pass

    def start(self):
        """To launch the module choosen."""
        window = tk.Tk()
        window.geometry("1000x1000")
        ITC(self.df_new, window)

    def one(self, i):
        """To fill the ITС list."""
        self.lst_ITC += [i]

    def create_sth(self, text, lst):
        """To avoid misunderstandings during choosing the parameters."""
        self.df_test = self.df.iloc[:, lst]
        self.df_test['result'] = self.df_test.mean(axis=1)
        self.df_new[text] = self.df_test['result']
        self.lst_ITC = []
        if text == 'time':
            self.time_button['state'] = 'disabled'
            self.reactivity_button['state'] = 'normal'
        if text == 'reactivity':
            self.reactivity_button['state'] = 'disabled'
            self.temperature_button['state'] = 'normal'
        if text == 'temperature':
            self.temperature_button['state'] = 'disabled'
            self.start_button['state'] = 'normal'

    def on_click(self, event):
        """To set the ranges."""
        if event.button == 1:
            pass
        elif event.button == 3:
            pass


root = tk.Tk()
app = Main(root)
root.geometry("700x500")
root.config(bg=BACKGROUND_COLOR_MAIN)
root.mainloop()
