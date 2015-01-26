#!/usr/bin/python

#-------------------------------------------------------------------------------
__author__     = "Daniel Gregory"
__email__      = "gigs94@gmail.com"
__version__    = "0.0.0"
__status__     = "Experimental"
#-------------------------------------------------------------------------------


import Tkinter
import argparse
import logging
import json
import os
import pika
from ConfigParser import RawConfigParser

#-------------------------------------------------------------------------------
class pychat_client(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)


def get_users():
    pass

def create_account():
    pass

def send_msg():
    pass

def encrypt_msg():
    pass

def decrypt_msg():
    pass

def read_config_file():
    pass

def write_config_file():
    pass



#-------------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pyChat Client')
    subparsers = parser.add_subparsers()

    debug_parser = subparsers.add_parser('debug', help='debug help')
    debug_parser.add_argument('directory')
    debug_parser.set_defaults(func=debug)

    args = parser.parse_args()
    args.func(args)

    app = pychat_client(None)
    app.title('pyChat')
    app.mainloop()

    sys.exit()
