"""This module intends to create a GUI for users that is clean and functional.

This module calls classes from other modules for each toplevel window (and a 
couple of sub-classes for these toplevel windows), that are all called by 
the '__init__' method of the MainApp class. 

    :return: Simply runs a tkinter mainloop until the user exits.
    :rtype: None
"""

import tkinter as tk
import tkinter.ttk as ttk

import helpers
import gui_network
import gui_settings

class WelcomePage(tk.Toplevel):
    """An object which inherits from tk.Toplevel to create a simple welcome
    window with options for the user.

    :param tk: A tk.Toplevel object
    :type tk: tk.Toplevel
    """
    
    def __init__(self, parent):
        """Calls super function and then instantiates several tkinter objects
        to actually create the look/feel of the window.

        :param parent: Should be the root tk.Tk object from MainApp.
        :type parent: tk.Tk
        """
        super().__init__(parent)
        self.parent = parent
        
        self.config_info = helpers.read_from_config()
        self.username = self.config_info['user']['username']
        
        self.title("Network Warden")
        self.rowconfigure(0, weight=1, minsize=100)
        self.rowconfigure(1, weight=1, minsize=75)
        self.columnconfigure(0, weight=1, minsize=100)

        # Two frames below separate the window into greeting and buttons
        frm_greeting = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_greeting.grid(row=0, column=0, pady=10, padx=5)

        frm_buttons = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_buttons.grid(row=1, column=0, pady=10, padx=5)

        lbl_greeting = ttk.Label(
            master=frm_greeting,
            text="Welome to Network Warden " + self.username + "!",
            width=30)
        lbl_greeting.pack(fill=tk.BOTH) # Note the different geometry manager
        
        if self.username == "":
            lbl_setup = ttk.Label(
                master=frm_greeting,
                text="Please first set up this software by clicking on Settings.",
                width=30,
                wraplength=500
            )
            lbl_setup.pack(fill=tk.BOTH)
        # Buttons are placed in a grid and bound using the command parameter
        btn_cancel = ttk.Button(
            master=frm_buttons,
            command=self.quit,
            text="Exit"
        )
        btn_cancel.grid(row=0, column=0, pady=3, padx=15)

        btn_show_network = ttk.Button(
            master=frm_buttons,
            command=self.create_network_page,
            text="Show Network Statistics"
        )
        btn_show_network.grid(row=0, column=1, pady=3, padx=15)

        btn_settings = ttk.Button(
            master=frm_buttons,
            command=self.create_settings_page,
            text="Settings"
        )
        btn_settings.grid(row=0, column=2, pady=3, padx=15)
        
    def create_network_page(self):
        self.destroy()
        gui_network.NetworkPage(self.parent)
        
    def create_settings_page(self):
        self.destroy()
        gui_settings.SettingsPage(self.parent)
        
    # def quit(self):
    #     self.destroy()



class MainApp(tk.Tk):
    """Calls super method for tk.Tk, makes the window resizable, and then 
    launches the WelcomePage class with itself (MainApp) as the parent.

    :return: essentially None
    :rtype: <class '__main__.GUI'>
    """

    def __init__(self):
        """
        Reads settings from config.toml and launches the 
        create_welcome_window function.
        """

        super().__init__()
        
        
        self.resizable(True, True)
        self.withdraw()
        
        self.welcomepage = WelcomePage(self)
        
    def quit(self):
        self.destroy()
        

def main():
    """Launches the GUI by creating a MainApp object and beginning the tkinter
    mainloop.
    """
    
    app = MainApp()
    app.mainloop()

if __name__ == '__main__':
    main()