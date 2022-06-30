

import tkinter as tk
import tkinter.ttk as ttk

import gui
import helpers


class SettingsPage(tk.Toplevel):
    """The settings page of the GUI

    :param tk: Toplevel object from tkinter
    :type tk: tk.Toplevel
    :return: Toplevel object from tkinter
    :rtype: tk.Toplevel
    """
    
    def __init__(self, parent):
        """Calls super function and then instantiates several tkinter objects
        to actually create the look/feel of the window.

        :param parent: Should be the root tk.Tk object from MainApp.
        :type parent: tk.Tk
        """
        super().__init__(parent)
        self.parent = parent
        
        self.title("Settings")
        self.rowconfigure(0, weight=1, minsize=100)
        self.columnconfigure(0, weight=1, minsize=100)
    
    # Window is separated into two tabs, with four frames each,
    # in a one-two-one shape
        ntb_tabs = ttk.Notebook(
            master=self,
            padding=(5, 5),
        )
        
        frm_user = SettingsUserTab(ntb_tabs)
        frm_remote = SettingsRemoteTab(ntb_tabs)
        # Instead of gridding the above frames, you must add them to the
        # Notebook object you created earlier.
        ntb_tabs.add(frm_user, text="User Settings")
        ntb_tabs.add(frm_remote, text="Remote Settings")
        ntb_tabs.grid(row=0, column=0)


class SettingsUserTab(ttk.Frame):
    """One tab of the Notebook object in the SettingsPage window.

    :param ttk: Inherits from a ttk.Frame object
    :type ttk: ttk.Frame
    """
    
    def __init__(self, parent):
        """Calls super function and then instantiates several tkinter objects
        to actually create the look/feel of the window.

        :param parent: Should be the SettingsPage ttk.Notebook object.
        :type parent: ttk.Notebook
        """
        super().__init__(parent)
        self.parent = parent
        
        self.relief=tk.FLAT
        self.borderwidth=5
        
        frm_directions = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5,
        )
        frm_directions.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        
        frm_labels = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_labels.grid(row=2, column=0, pady=0, padx=5)

        frm_inputs = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_inputs.grid(row=2, column=1, pady=0, padx=5)

        frm_buttons = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=3, column=0, pady=10, padx=5, columnspan=2)

        # Labels are grouped together
        lbl_directions = ttk.Label(
            master=frm_directions,
            text=("Leave blank any settings you want unchanged. \n\nClick Submit to change settings, click Cancel to leave all settings unchanged."),
            wraplength=500,
            justify=tk.CENTER
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

        lbl_remote_server_capability = ttk.Label(
            master=frm_labels,
            text="Do you have a remote server you want to set up?"
        )
        lbl_remote_server_capability.grid(
            row=2,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

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

        # Create a variable for the radiobuttons and a variable to hold 
        # whether any radiobutton has been clicked. This will allow for
        # input validation.
        self.remote_server_var = tk.StringVar(frm_inputs, value="False")
        self.radio_clicked_bool = False
        self.rb_remote_server_off = tk.Radiobutton(
            master=frm_inputs,
            text="No",
            variable=self.remote_server_var,
            value="False",
            command=self.radio_clicked
        )
        self.rb_remote_server_on = tk.Radiobutton(
            master=frm_inputs,
            text="Yes",
            variable=self.remote_server_var,
            value="True",
            command=self.radio_clicked         
        )
        self.rb_remote_server_off.grid(row=2, column=1, padx=1, pady=0, 
                                        sticky="w")
        self.rb_remote_server_on.grid(row=3, column=1, padx=1, pady=0,
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
        
    def collect_user_entries(self):
        """Gets entry data from settings window and returns them as a dict
        """
        
        user_settings = {}
        
        if self.ent_username.get() != "":
            user_settings["username"] = self.ent_username.get()
        if self.ent_ip_address.get() != "":
            user_settings["ip_address"] = self.ent_ip_address.get()
        rsc = self.remote_server_var.get()
        
        if self.radio_clicked_bool:
            if rsc == "True":
                user_settings["remote_server_capability"] = True
            else:
                user_settings["remote_server_capability"] = False
            return user_settings
    
    def edit_settings_file(self):
        """Calls collect_user_entries and submits them before opening
        welcom screen again.
        """

        user_settings = self.collect_user_entries()
        if user_settings is not None:
            for key in user_settings:
                    helpers.edit_config('user', key, user_settings[key])

        self.cancel_to_welcome()
    
    def radio_clicked(self):
        self.radio_clicked_bool = True
    
    def cancel_to_welcome(self):
        self.parent.master.destroy()
        gui.MainApp()


class SettingsRemoteTab(ttk.Frame):
    """One tab of the Notebook object in the SettingsPage window.

    :param ttk: Inherits from a ttk.Frame object
    :type ttk: ttk.Frame
    """
    
    def __init__(self, parent):
        """Calls super function and then instantiates several tkinter objects
        to actually create the look/feel of the window.

        :param parent: Should be the SettingsPage ttk.Notebook object.
        :type parent: ttk.Notebook
        """
        super().__init__(parent)
        self.parent = parent
        
        self.relief=tk.FLAT
        self.borderwidth=5
        
        frm_directions = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5,
        )
        frm_directions.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        
        frm_labels = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_labels.grid(row=2, column=0, pady=0, padx=5)

        frm_inputs = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_inputs.grid(row=2, column=1, pady=0, padx=100)

        frm_buttons = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=3, column=0, pady=10, padx=5, columnspan=2)

        # Labels are grouped together
        caption = "Leave blank any settings you want unchanged. \n\nClick Submit to change settings, click Cancel to leave all settings unchanged."
        lbl_directions = ttk.Label(
            master=frm_directions,
            text=caption,
            wraplength=500,
            justify=tk.CENTER
        )
        lbl_directions.grid(row=0, column=0, padx=15, pady=5, sticky="ew")

        lbl_username = ttk.Label(
            master=frm_labels,
            text="Remote Host Username: "
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
            text="Remote Host IP Address: "
        )
        lbl_ip_address.grid(
            row=1,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        lbl_remote_server_sk = ttk.Label(
            master=frm_labels,
            text="Remote Host Security Key: "
        )
        lbl_remote_server_sk.grid(
            row=2,
            column=0,
            padx=15,
            pady=20,
            sticky="w"
        )

        self.ent_username = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_username.grid(row=0, column=1, padx=15, pady=20, sticky="e")
        self.ent_username.focus_set()   # Set the focus automatically here

        self.ent_ip_address = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_ip_address.grid(row=1, column=1, padx=15, pady=20, sticky="e")

        self.ent_remote_server_key = ttk.Entry(
            master=frm_inputs,
            width=20
        )
        self.ent_remote_server_key.grid(row=3, column=1, padx=15, pady=20, 
                                        sticky="e")

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
        
    def collect_user_entries(self):
        """Gets entry data from settings window and returns them as a dict
        """
        
        remote_server_settings = {}
        if self.ent_username.get() != "":
            remote_server_settings["username"] = self.ent_username.get()
        if self.ent_ip_address.get() != "":
            remote_server_settings["ip_address"] = self.ent_ip_address.get()
        if self.ent_remote_server_key.get() != "":
            remote_server_settings["security_key"] = self.ent_remote_server_key.get()
        
        return remote_server_settings
    
    def edit_settings_file(self):
        """Calls collect_user_entries and submits them before opening
        welcom screen again.
        """

        remote_server_settings = self.collect_user_entries()
        if len(remote_server_settings) != 0:
            for key in remote_server_settings:
                helpers.edit_config('remote_servers', key,
                                    remote_server_settings[key])

        self.cancel_to_welcome()
    
    def cancel_to_welcome(self):
        self.parent.master.destroy()
        gui.MainApp()