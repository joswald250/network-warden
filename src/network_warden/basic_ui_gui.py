import tkinter as tk
import tkinter.ttk as ttk

import graph_network
import tomli_helpers


class UI():
    def __init__(self):
        self.config_info = tomli_helpers.read_from_config()
        self.username = self.config_info['user']['username']
        self.create_welcome_window()

    def create_welcome_window(self):
        self.window = tk.Tk()
        self.window.title("Network Warden")
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.columnconfigure(0, weight=1, minsize=100)

        frm_greeting = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_greeting.grid(row=0, column=0, pady=10, padx=5)

        frm_buttons = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=1, column=0, pady=10, padx=5)

        lbl_greeting = ttk.Label(
            master=frm_greeting,
            text="Welome to Network Warden " + self.username + "!",
            width=30)
        lbl_greeting.pack(fill=tk.BOTH)

        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.quit,
            text="Cancel"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15)

        btn_show_network = ttk.Button(
            master=frm_buttons,
            command=self.show_network,
            text="Show Network Statistics"
        )
        btn_show_network.grid(row=0, column=1, pady=3, padx=15)

        btn_settings = ttk.Button(
            master=frm_buttons,
            command=self.create_settings_window,
            text="Settings"
        )
        btn_settings.grid(row=0, column=2, pady=3, padx=15)

        self.window.mainloop()

    def create_settings_window(self):
        self.window.destroy()
        self.window = tk.Tk()
        self.window.title("Settings")
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.columnconfigure(0, weight=1, minsize=100)

        frm_labels = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_labels.grid(row=0, column=0, pady=10, padx=5)

        frm_inputs = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_inputs.grid(row=0, column=1, pady=10, padx=5)

        frm_buttons = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=1, column=0, pady=10, padx=5, columnspan=2)

        lbl_username = ttk.Label(
            master=frm_labels,
            text="Username: "
        )
        lbl_username.grid(
            row=0,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        lbl_ip_address = ttk.Label(
            master=frm_labels,
            text="IP Address: "
        )
        lbl_ip_address.grid(
            row=1,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        ent_username = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        ent_username.grid(row=0, column=1, padx=15, pady=20, sticky="w")

        ent_ip_address = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        ent_ip_address.grid(row=1, column=1, padx=15, pady=20, sticky="w")

        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.cancel_to_welcome,
            text="Cancel (NO changes)"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15, sticky="we")

        btn_submit = ttk.Button(
            master=frm_buttons,
            command=self.quit,
            text="Submit Changes"
        )
        btn_submit.grid(row=0, column=1, pady=3, padx=15, sticky="ew")


        self.window.mainloop()

    def cancel_to_welcome(self):
        self.window.destroy()
        self.create_welcome_window()

    def quit(self):
        self.window.destroy()
    
    def show_network(self):
        graph_network.main()

app = UI()
