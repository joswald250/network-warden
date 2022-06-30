

import tkinter as tk
import tkinter.ttk as ttk
from matplotlib import pyplot as plt

import gui
import graph_network


class NetworkPage(tk.Toplevel):
    """An object which inherits from tk.Toplevel to create a window providing
    the user with options for which graph(s) they would like to plot.

    :param tk: A tk.Toplevel object
    :type tk: tk.Toplevel
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
    
    def __init__(self, parent):
        """Calls super function and then instantiates several tkinter objects
        to actually create the look/feel of the window.

        :param parent: Should be the root tk.Tk object from MainApp.
        :type parent: tk.Tk
        """
        super().__init__(parent)
        self.parent = parent
        
        self.title("Network Warden")
        self.rowconfigure(0, weight=1, minsize=75)
        self.rowconfigure(1, weight=1, minsize=75)
        self.rowconfigure(2, weight=1, minsize=75)
        self.columnconfigure(0, weight=1, minsize=100)

        # Three frames stacked on top of each other
        frm_greeting = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_greeting.grid(row=0, column=0, pady=10, padx=5)

        frm_opt_menu = ttk.Frame(
            master=self,
            relief=tk.FLAT,
            borderwidth=5
        )
        frm_opt_menu.grid(row=1, column=0, pady=10, padx=5)

        frm_buttons = ttk.Frame(
            master=self,
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
        lbl_greeting.grid(row=0, column=0, sticky="ew", padx=25)

        # Switching to opt_menu frame
        lbl_graph_type = ttk.Label(
            master=frm_opt_menu,
            text="Graph Type(s): "
        )
        lbl_graph_type.grid(row=0, column=0, sticky="w", padx=5)
        
        # initialize string variable for option menu
        self.string_var = tk.StringVar()
        self.string_var.set(self.graph_types[0])
        self.opt_graph_type = tk.OptionMenu(
            frm_opt_menu,
            self.string_var,
            # command=self.update_opt_graph_type,
            *self.graph_types
        )
        self.opt_graph_type.grid(row=0, column=1, padx=5, sticky="ew")

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
    
    # def update_opt_graph_type(self, event):
    #     graph_type = self.string_var.get()
    #     self.string_var.set(graph_type)
    
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
    
    def cancel_to_welcome(self):
        self.destroy()
        gui.MainApp()