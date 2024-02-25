# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 22:07:35 2024

@author: Administrator
"""

import tkinter as tk
import os
import subprocess
from CreateGuiPlot import create_gui

def on_ok_button():
    # Callback function for the OK button
    if check_var1.get() and check_var2.get() == False and check_var3.get() == False and check_var4.get() == False:
        #for deepslice
        print(1)
        # Add your logic for when Option 1 is checked and OK button is clicked
    elif check_var3.get() and check_var1.get() == False and check_var2.get() == False and check_var4.get() == False:
        print(3) #for counting
        #os.system('conda run -p C:/Users/Administrator/anaconda3/envs/StardistForImagej  python X:/Users/LabSoftware/ImageJSoftware/AutomaticCountingWithRoiatlas/AutomaticCounting/Initial_File.py')
    elif check_var4.get() and check_var1.get() == False and check_var2.get() == False and check_var3.get() == False:
        create_gui()
    elif check_var2.get() and check_var1.get() == False and check_var3.get() == False and check_var4.get() == False:
         print(2) #arrange names
    else:
        print("OK button clicked, but Option  is not checked")
        # Add your logic for when Option 1 is not checked and OK button is clicked
    #root.destroy()  # Close the window when Cancel button is clicked

def on_cancel_button():
    # Callback function for the Cancel button
    #print("Cancel button clicked")
    root.destroy()  # Close the window when Cancel button is clicked

def main():
    # Create the main window
   global root
    # Create variables to hold the state of the checkbuttons
   global check_var1, check_var2, check_var3, check_var4

   # Create the main window
   root = tk.Tk()
   root.title("Menu")

   # Set the size of the root window
   root.geometry("500x500")  # Width x Height


   # Create a label
   label = tk.Label(root, text="Counting labels in brain slides:", font=('Helvetica', 14))
   label.grid(row=0, column=0, sticky='e',pady =20)

   # Create variables to hold the state of the checkbuttons
   check_var1 = tk.BooleanVar()
   check_var2 = tk.BooleanVar()
   check_var3 = tk.BooleanVar()
   check_var4 = tk.BooleanVar()

   # Create three checkbuttons with a custom font size
   checkbutton1 = tk.Checkbutton(root, text="DeepSlice Automatic Registration with the atlas", variable=check_var1, font=('Helvetica', 12,'bold'), bg='lightblue', fg='black')
   checkbutton2 = tk.Checkbutton(root, text="Rename Roi Atlas files", variable=check_var2, font=('Helvetica', 12,'bold'), bg='lightgreen', fg='black')
   checkbutton3 = tk.Checkbutton(root, text="Counting labels in each atlas Roi", variable=check_var3, font=('Helvetica', 12,'bold'),bg='lightcoral', fg='black')
   checkbutton4 = tk.Checkbutton(root, text="Post plotting of Roi regions", variable=check_var4, font=('Helvetica', 12,'bold'),bg='yellow', fg='black')
   
   # Pack the checkbuttons
   checkbutton1.grid(row=1, column=0, sticky='w',pady =20)
   checkbutton2.grid(row=2, column=0, sticky='w',pady =20)
   checkbutton3.grid(row=3, column=0, sticky='w',pady =20)
   checkbutton4.grid(row=4, column=0, sticky='w',pady =20)

   # Create OK and Cancel buttons
   ok_button = tk.Button(root, text="OK", command=on_ok_button, font=('Helvetica', 12))
   cancel_button = tk.Button(root, text="Continue", command=on_cancel_button, font=('Helvetica', 12))
   
   # Pack the buttons
   ok_button.grid(row=5, column=0, sticky='w',padx = 10,pady = 50)
   cancel_button.grid(row=5, column=1, sticky='w', pady = 50)
   
  
   

   # Start the Tkinter event loop
   root.mainloop()

if __name__ == "__main__":
    main()