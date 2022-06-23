import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt

import graph_network
import helpers


class GUI():
    """Wraps gui functionality into one object

    Returns:
        <class '__main__.GUI'>: essentially None
    """
    
    graph_types = [
        "jitter, download, and upload",
        "upload and download",
        "jitter and download",
        "jitter and upload",
        "jitter",
        "upload",
        "download",
    ]

    def __init__(self):
        """
        Reads settings from config.toml and launches the 
        create_welcome_window function.
        """

        self.config_info = helpers.read_from_config()
        self.username = self.config_info['user']['username']
        self.create_welcome_window()

    def create_welcome_window(self):
        """
        Uses Tkinter to create a basic window that first pops up when 
        network_warden is launched.
        """
        
        self.window = tk.Tk()
        self.window.title("Network Warden")
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.columnconfigure(0, weight=1, minsize=100)

        # Two frames below separate the window into greeting and buttons
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
        lbl_greeting.pack(fill=tk.BOTH) # Note the different geometry manager

        # Buttons are placed in a grid and bound using the command parameter
        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.quit,
            text="Cancel"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15)

        btn_show_network = ttk.Button(
            master=frm_buttons,
            command=self.create_network_window,
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
    
    def create_network_window(self):
        """
        Uses Tkinter to create a basic window to allow user to choose which
        graphs they want displayed. 
        
        Will submit the call to graph_network.py as necessary.
        """
        
        self.quit()
        self.window = tk.Tk()
        self.window.title("Network Warden")
        self.window.rowconfigure(0, weight=1, minsize=75)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.rowconfigure(2, weight=1, minsize=75)
        self.window.columnconfigure(0, weight=1, minsize=100)

        # Three frames stacked on top of each other
        frm_greeting = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_greeting.grid(row=0, column=0, pady=10, padx=5)

        frm_opt_menu = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_opt_menu.grid(row=1, column=0, pady=10, padx=5)

        frm_buttons = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=2, column=0, pady=10, padx=5)

        lbl_greeting = ttk.Label(
            master=frm_greeting,
            text="Please select which graphs you would like to display.",
            width=50,
            wraplength=450
        )
        lbl_greeting.grid(row=0, column=0, sticky="nsew", padx=5)

        # Switching to opt_menu frame
        lbl_graph_type = ttk.Label(
            master=frm_opt_menu,
            text="Graph Type(s): "
        )
        lbl_graph_type.grid(row=0, column=0, sticky="w", padx=5)
        
        # initialize string variable for option menu
        self.string_var = tk.StringVar() 
        self.opt_graph_type = tk.OptionMenu(
            frm_opt_menu,
            self.string_var,
            *self.graph_types
        )
        self.opt_graph_type.grid(row=0, column=1, padx=5, sticky="e")

        # Buttons are placed in a grid and bound using the command parameter
        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.cancel_to_welcome,
            text="Cancel"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15)

        btn_show_network = ttk.Button(
            master=frm_buttons,
            command=self.show_network,
            text="Show Network Statistics"
        )
        btn_show_network.grid(row=0, column=1, pady=3, padx=15)

        self.window.mainloop()

    def create_settings_window(self):
        """Creates settings window to allow user to edit config.toml
        """
        
        # Note the destruction of the welcome window first
        self.quit()
        self.window = tk.Tk()
        self.window.title("Settings")
        self.window.rowconfigure(0, weight=1, minsize=100)
        self.window.rowconfigure(1, weight=1, minsize=75)
        self.window.columnconfigure(0, weight=1, minsize=100)

        # Window is separated into four frames, in a one-two-one shape
        frm_directions = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5,
        )
        frm_directions.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        
        frm_labels = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_labels.grid(row=2, column=0, pady=0, padx=5)

        frm_inputs = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_inputs.grid(row=2, column=1, pady=0, padx=5)

        frm_buttons = ttk.Frame(
            master=self.window,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=3, column=0, pady=10, padx=5, columnspan=2)

        # Labels are grouped together
        lbl_directions = ttk.Label(
            master=frm_directions,
            text="Leave blank any settings you want unchanged. \n\nClick \
                Submit to change settings, click Cancel to leave all \
                    settings unchanged.",
            wraplength=450,
            justify=tk.LEFT
        )
        lbl_directions.grid(row=0, column=0, padx=15, pady=5, sticky="ew")

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

        lbl_remote_server_ip = ttk.Label(
            master=frm_labels,
            text="Remote Server IP: "
        )
        lbl_remote_server_ip.grid(
            row=2,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        lbl_remote_server_key = ttk.Label(
            master=frm_labels,
            text="Remote Server Security Key: "
        )
        lbl_remote_server_key.grid(
            row=3,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        # Note the use of the self keyword
        self.ent_username = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_username.grid(row=0, column=1, padx=15, pady=20, sticky="w")
        self.ent_username.focus_set()   # Set the focus automatically here

        self.ent_ip_address = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_ip_address.grid(row=1, column=1, padx=15, pady=20, sticky="w")

        self.ent_remote_ip_address = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_remote_ip_address.grid(row=2, column=1, padx=15, pady=20, 
                                        sticky="w")

        self.ent_remote_server_key = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_remote_server_key.grid(row=3, column=1, padx=15, pady=20, 
                                        sticky="w")

        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.cancel_to_welcome,
            text="Cancel (NO changes)"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15, sticky="we")

        btn_submit = ttk.Button(
            master=frm_buttons,
            command=self.edit_settings_file,
            text="Submit Changes"
        )
        btn_submit.grid(row=0, column=1, pady=3, padx=15, sticky="ew")

        self.window.mainloop()

    def collect_user_entries(self):
        """Gets entry data from settings window and returns them as a dict
        """
        
        user_settings = {}
        remote_server_settings = {}
        
        user_settings["username"] = self.ent_username.get()
        user_settings["ip_address"] = self.ent_ip_address.get()

        remote_server_settings["ip_address"] = self.ent_remote_ip_address.get()
        remote_server_settings["security_key"] = self.ent_remote_server_key.get()
        
        return user_settings, remote_server_settings
    
    def edit_settings_file(self):
        """Calls collect_user_entries and submits them before opening
        welcom screen again.
        """

        user_settings, remote_server_settings = self.collect_user_entries()
        
        for key in user_settings:
            if user_settings[key]:
                helpers.edit_config('user', key, user_settings[key])
        
        for key in remote_server_settings:
            if remote_server_settings[key]:
                helpers.edit_config('remote_servers', key, remote_server_settings[key])

        self.quit()
        self.create_welcome_window()

    def cancel_to_welcome(self):
        self.window.destroy()
        self.create_welcome_window()

    def quit(self):
        self.window.destroy()
    
    def show_network(self):
        """Gets graph_type string from network window and loads a 
        parameter dictionary that will be passed to the 
        graph_network.py module.
        """
        
        graph_type = self.string_var.get()
        parameters = {}
        if "jitter" in graph_type:
            parameters["jitter"] = True
        if "download" in graph_type:
            parameters["download"] = True
        if "upload" in graph_type:
            parameters["upload"] = True
        
        graph_network.main(**parameters)
        plt.show()

def main():
    app = GUI()

if __name__ == '__main__':
    main()