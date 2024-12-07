import datetime
from tkinter import ttk
import tkinter as tk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from typing import Optional

BUTTON_FONT: tuple = ("Helvetica", 12, "bold")
BUTTON_PADDING: int = 10
BACKGROUND_COLOR: str = "#ffedc0"
FOREGROUND_COLOR: str = "#454545"
BACKGROUND_COLOR_MAIN: str = "yellow"


class ITC:
    """To compute the ITC."""

    def __init__(self, df, window):
        """To make the main settings."""
        self.df = df
        self.df['time'] = self.df.iloc[:, 0].apply(
            lambda x: datetime.datetime(1899, 12, 30) +
            datetime.timedelta(days=x))
        self.window = window

        frame = ttk.Frame(self.window)
        frame.grid(column=0, row=0)
        # frame.pack(fill='both', expand=True)

        columns = tuple(self.df.columns)
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.grid(column=0, row=0, rowspan=8)
        # self.tree.pack(side='left', fill='both')

        self.beta: Optional[float] = None
        self.DTC: Optional[float] = None
        # self.itc_1 = None
        # self.itc_2 = None
        # self.itc_3 = None
        # self.mtc_1 = None
        # self.mtc_2 = None
        # self.mtc_3 = None

        for col in columns:
            self.tree.heading(col, text=col)

        for row in self.df.itertuples(index=False):
            self.tree.insert("", "end", values=row)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, rowspan=8, sticky='ns')
        # vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        # hsb = ttk.Scrollbar(frame, orient="horizontal",
        # command=self.tree.xview)
        # hsb.pack(side='bottom', fill='x')
        # self.tree.configure(xscrollcommand=hsb.set)

        entry_for_beta = ttk.Entry(frame)
        text_for_beta = tk.Label(frame, text='beta')
        button_for_beta = tk.Button(frame, text='Obtain beta',
                                    command=lambda: self.get_entry(
                                        entry_for_beta,
                                        'self.beta'
                                        ))
        text_for_beta.grid(row=0, column=3)
        entry_for_beta.grid(row=0, column=4)
        button_for_beta.grid(row=0, column=5)
        entry_for_dtc = tk.Entry(frame)
        text_for_dtc = tk.Label(frame, text='DTC')
        button_for_dtc = tk.Button(frame, text='Obtain DTC',
                                   command=lambda: self.get_entry(
                                       entry_for_dtc,
                                       'self.DTC'
                                       ))
        text_for_dtc.grid(row=1, column=3)
        entry_for_dtc.grid(row=1, column=4)
        button_for_dtc.grid(row=1, column=5)

        self.Label_1 = tk.Label(frame, text='   T1 = ')
        self.Label_2 = tk.Label(frame, text='   T2 = ')
        self.Label_3 = tk.Label(frame, text='R1 =     ')
        self.Label_4 = tk.Label(frame, text='R2 =     ')
        self.Label_5 = tk.Label(frame, text='     ')
        self.Label_6 = tk.Label(frame, text='     ')
        self.Label_7 = tk.Label(frame, text='          Technique 1')
        self.Label_8 = tk.Label(frame, text='')
        self.Label_9 = tk.Label(frame, text='          Technique 2')
        self.Label_10 = tk.Label(frame, text='')
        self.Label_11 = tk.Label(frame, text='         Technique 3')
        self.Label_12 = tk.Label(frame, text='')
        self.Label_13 = tk.Label(frame, text='         Mean values')
        self.Label_14 = tk.Label(frame, text='')
        self.Label_1.grid(row=0, column=6)
        self.Label_2.grid(row=1, column=6)
        self.Label_3.grid(row=0, column=8)
        self.Label_4.grid(row=1, column=8)
        self.Label_5.grid(row=1, column=7)
        self.Label_6.grid(row=0, column=7)
        self.Label_7.grid(row=0, column=9)
        self.Label_8.grid(row=1, column=9)
        self.Label_9.grid(row=2, column=9)
        self.Label_10.grid(row=3, column=9)
        self.Label_11.grid(row=4, column=9)
        self.Label_12.grid(row=5, column=9)
        self.Label_13.grid(row=6, column=9)
        self.Label_14.grid(row=7, column=9)

        main_button = tk.Button(
            frame,
            text='Compute ITC',
            command=self.compute
            )
        main_button.grid(row=2, column=2, columnspan=3)

        self.window.update()
        self.setup_ui()

    def setup_ui(self):
        """To set the initial view."""
        self.canvas_frame = ttk.Frame(self.window)
        # self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas_frame.grid(row=1, column=0)
        self.fig = self.create_plot(
            self.df['time'],
            self.df['temperature'],
            'orange',
            self.df['time'],
            self.df['reactivity'], 'blue'
            )
        self.canvas = self._create_canvas()
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self._create_controls()

    def _create_canvas(self):
        canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.toolbar = NavigationToolbar2Tk(canvas, self.canvas_frame)
        self.toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return canvas

    def _create_controls(self):
        style = ttk.Style()
        style.configure(
            'TButton',
            font=BUTTON_FONT,
            padding=(BUTTON_PADDING, BUTTON_PADDING),
            )
        style.configure('TCheckbutton', font=BUTTON_FONT)
        style.configure('TMenubutton', font=BUTTON_FONT)
        self._setup_top_controls()

    def _setup_top_controls(self):
        top_frame = ttk.Frame(self.window)
        # top_frame.pack(pady=10)
        top_frame.grid(row=3, column=0)
        self.Button1 = ttk.Button(
            top_frame,
            text="Button1",
            command=self.сommand1
            )
        self.Button2 = ttk.Button(
            top_frame,
            text="Button2",
            command=self.сommand2
            )
        self.Button3 = ttk.Button(
            top_frame,
            text="Button3",
            command=self.сommand3
            )
        self.Button4 = ttk.Button(
            top_frame,
            text="Button4",
            command=self.сommand4
            )
        self.Button1.pack(side=tk.LEFT, padx=10)
        self.Button2.pack(side=tk.LEFT, padx=10)
        self.Button3.pack(side=tk.LEFT, padx=10)
        self.Button4.pack(side=tk.LEFT, padx=10)

    def determine_parametrs_via_click(self, event) -> tuple[datetime.date, float, float]:
        """
        To work witk dataset and to add a lines.

        To obtain the interval via getting the click coordinates,
        To choose the data interval from the dataset.
        """
        # To get the click coordinates
        x_pix, y_pix = event.x, event.y

        # To transfer the pixel coordinates to the data coordinates
        x_data = self.ax.transData.inverted().transform((x_pix, y_pix))[0]
        y_data_left = self.ax.transData.inverted().transform((x_pix, y_pix))[1]
        y_data_right = self.ax2.transData.inverted().transform((x_pix, y_pix))[1]

        # Transfer the time coordinates from numbers format to the time format
        time_data = mdates.num2date(x_data)
        # To remove nanoseconds
        # time_data = time_data.replace(microsecond=0)
        # print(f'initial time_data = {time_data}')
        # To remove +00:00 in the end
        time_data = datetime.datetime.strptime(
            str(time_data)[:-6],
            '%Y-%m-%d %H:%M:%S.%f'
            )
        # print(f'after strtime and [-6] time_data = {time_data}')
        self.time_data = self.df[self.df['time'] <= time_data]['time'].iat[-1]
        y_data_left = self.df[self.df['time'] <= time_data]['temperature'].iat[-1]
        y_data_right = self.df[self.df['time'] <= time_data]['reactivity'].iat[-1]

        # print(f"Time: {time_data}, Temperature: {round(y_data_left, 2)},
        # Reactivity: {round(y_data_right, 4)}")

        # Для отладки можно также нарисовать линии на графике
        self.ax.plot(
            [x_data, x_data],
            [self.df['temperature'].min(),
             self.df['temperature'].max()], color='red', linestyle='--')
        # self.ax2.plot([x_data, x_data], [self.df['reactivity'].min(),
        # self.df['reactivity'].max()], color='blue', linestyle='--')

        self.canvas.draw_idle()
        return (self.time_data,
                "{:.2f}".format(y_data_left),
                "{:.4f}".format(y_data_right))

    def helper(self, event, label_1_number, label_2_number, title_r: str) -> tuple[datetime.date, float, float]:
        """To the on_click function."""
        time_data_number = self.determine_parametrs_via_click(event)[0]
        temperature_data_number = self.determine_parametrs_via_click(event)[1]
        time_reactivity_number = self.determine_parametrs_via_click(event)[2]
        label_1_number.config(text=f'{temperature_data_number} \N{DEGREE SIGN}C')
        label_2_number.config(text=title_r + str(time_reactivity_number) + ' beta')
        return (time_data_number,
                temperature_data_number,
                time_reactivity_number)

    def on_click(self, event):
        """To obtain the parameters.

        To obtain the time, temperature and reactivity in the correct format.
        """
        if event.button == 1:
            self.time_data_1, self.temperature_data_1, self.time_reactivity_1 = self.helper(event, self.Label_6, self.Label_3, 'R1= ')

        if event.button == 3:
            self.time_data_2, self.temperature_data_2, self.time_reactivity_2 = self.helper(event, self.Label_5, self.Label_4, 'R2= ')

    def create_plot(self, time,
                    temperature,
                    temp_color,
                    time2,
                    reactivity,
                    react_color,
                    y_label_left='Temperature, \N{DEGREE SIGN}C',
                    y_label_right='Reactivity, beta',
                    x_label='Time (minutes)',
                    title=None):
        """To create plots via paremeters gotten."""
        fig = Figure(figsize=(12, 4.5), dpi=100)
        self.ax = fig.add_subplot(111)

        self.ax.grid(True, linestyle=':')
        self.ax.set_ylabel(y_label_left, family='Times New Roman', fontsize=14)
        self.ax.set_xlabel(x_label, family='Times New Roman', fontsize=14)
        self.ax.set_title(title, family='Times New Roman', fontsize=20)

        self.ax.plot(time, temperature, color=temp_color)
        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel(
            y_label_right,
            family='Times New Roman',
            fontsize=14
            )
        self.ax2.scatter(time2, reactivity, color=react_color)
        # Format the x-axis to display time in minutes
        # self.ax.xaxis.set_major_formatter(DateFormatter('%M:%S'))
        fig.tight_layout()
        return fig

    def get_entry(self, entry, value):
        """To get the beta and the DTC values."""
        if value == 'self.beta':
            self.beta = entry.get()
            return float(self.beta)
        if value == 'self.DTC':
            self.DTC = entry.get()
            return float(self.DTC)

    def technique_1(self):
        """To compute the ITC via technique 1.

        The ITC is computed by dR/dT. The sets of measurements were taken from
        the beginning and from the end of this test from reactivity data and
        from temperature data. The mean values were computed respectively, and
        dR/dT is the result.
        """
        reactivity_no = self.df.columns.get_loc('reactivity')
        temperature_no = self.df.columns.get_loc('temperature')
        first_index = self.df[self.df['time'] == self.time_data_1].index[0]
        first_reactivity = self.df.iloc[first_index:first_index+100, reactivity_no].mean()
        first_temperature = self.df.iloc[first_index:first_index+100, temperature_no].mean()
        last_index = self.df[self.df['time'] == self.time_data_2].index[0]
        last_reactivity = self.df.iloc[last_index:last_index+5, reactivity_no].mean()
        last_temperature = self.df.iloc[last_index-5:last_index, temperature_no].mean()
        d_temperature = last_temperature - first_temperature
        d_reactivity = last_reactivity - first_reactivity
        self.itc_1 = (d_reactivity / d_temperature) * float(self.beta) * 1000
        self.mtc_1 = self.itc_1 - float(self.DTC)
        self.Label_8.config(text=f'ITC = {"{:.2f}".format(self.itc_1)}, MTC = {"{:.2f}".format(self.mtc_1)}')
        return self.itc_1, self.mtc_1

    def technique_2(self):
        """To compute the ITC via technique 2.

        The ITC is computed as a slope coeffisient of the function R(T).
        """
        reactivity_no = self.df.columns.get_loc('reactivity')
        temperature_no = self.df.columns.get_loc('temperature')
        first_index = self.df[self.df['time'] == self.time_data_1].index[0]
        last_index = self.df[self.df['time'] == self.time_data_2].index[0]

        reactivity = self.df.iloc[first_index:last_index,  reactivity_no]
        temperature = self.df.iloc[first_index:last_index, temperature_no]

        f1 = np.polyfit(temperature, reactivity, 1)

        self.itc_2 = float(f1[0]) * float(self.beta) * 1000
        self.mtc_2 = self.itc_2 - float(self.DTC)

        self.Label_10.config(text=f'ITC = {"{:.2f}".format(self.itc_2)}, MTC = {"{:.2f}".format(self.mtc_2)}')
        return self.itc_2, self.mtc_2

    def technique_3(self):
        """To compute the ITC via technique 3.

        The ITC is computed as the average value among the set of ITC,
        each of them computed via 100 measurements, that is shifts for one
        point to compute the next ITC.
        """
        time_no = self.df.columns.get_loc('time')
        reactivity_no = self.df.columns.get_loc('reactivity')
        temperature_no = self.df.columns.get_loc('temperature')
        first_index = self.df[self.df['time'] == self.time_data_1].index[0]
        last_index = self.df[self.df['time'] == self.time_data_2].index[0]
        itc = []
        for i in range(last_index - first_index - 100):
            time = self.df.iloc[first_index:first_index+100, time_no].apply(mdates.date2num)
            time_indexes = [i for i in range(first_index, first_index+101)]
            reactivity = self.df.iloc[first_index:first_index+100, reactivity_no]
            temperature = self.df.iloc[first_index:first_index+100, temperature_no]

            f1 = np.polyfit(time, reactivity, 1)
            reactivity_fitted = np.poly1d(f1)
            f2 = np.polyfit(time, temperature, 1)
            temperature_fitted = np.poly1d(f2)

            d_reactivity = reactivity_fitted(time_indexes[-1]) - reactivity_fitted(time_indexes[0])
            d_temperature = temperature_fitted(time_indexes[-1]) - temperature_fitted(time_indexes[0])
            itc_i = float(d_reactivity / d_temperature) * float(self.beta) * 1000
            itc.append(itc_i)
            first_index += 1

        self.itc_3 = float(np.mean(itc))
        self.mtc_3 = float(self.itc_3 - float(self.DTC))
        self.Label_12.config(text=f'ITC = {"{:.2f}".format(self.itc_3)}, MTC = {"{:.2f}".format(self.mtc_3)}')
        return self.itc_3, self.mtc_3

    def average_itc(self):
        """To get the final ITC.

        Final ITC is the average value from the values
        from techniques 1 - 3.
        """
        self.itc = round((self.itc_1+self.itc_2+self.itc_3)/3, 2)
        self.mtc = round((self.mtc_1+self.mtc_2+self.mtc_3)/3, 2)
        self.Label_14.config(text=f'ITC = {"{:.2f}".format(self.itc)}, MTC = {"{:.2f}".format(self.mtc)}')

    def compute(self):
        """To launch the functions."""
        self.technique_1()
        self.technique_2()
        self.technique_3()
        self.average_itc()

    def сommand1(self):
        """Reserved to the Button 1."""
        pass

    def сommand2(self):
        """Reserved to the Button 2."""
        pass

    def сommand3(self):
        """Reserved to the Button 3."""
        pass

    def сommand4(self):
        """Reserved to the Button 4."""
        pass
