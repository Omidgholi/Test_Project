import pandas as pd
from tkcalendar import DateEntry
from datetime import date
import tkinter as tk
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
import os
import main



def serve_end_cal():
    global end_cal
    global end_button
    start_button.config(state="disabled")
    end_cal = DateEntry(root, mindate=start_cal.get_date(), maxdate=date.today())
    end_cal.grid(row=0, column=1)
    end_button = tk.Button(root, text="Submit End Range", command=get_date)
    end_button.grid(row=1, column=1)


def get_date():
    select_venue()
    end_button.config(state="disabled")


def range_data():
    start_cal.grid(row=0, column=0)
    start_button.grid(row=1, column=0)


def all_data():
    all_button.destroy()
    range_button.destroy()
    select_venue()


def analysis():
    try:
        start_date = pd.to_datetime(start_cal.get_date(), infer_datetime_format=True, cache=True)
        end_date = pd.to_datetime(end_cal.get_date(), infer_datetime_format=True, cache=True)
    except:
        #start_date = pd.to_datetime("1/1/2000", infer_datetime_format=True)
        #end_date = pd.to_datetime("1/1/2070", infer_datetime_format=True)
        start_date = None
        end_date = None


    print(start_date, end_date)
    venue = clicked.get()
    print(venue)
    root.destroy()
    main.gym_analysis(venue, start_date, end_date)
    tk.messagebox.showinfo(message="Report Successfully Saved to Data.csv")


def select_venue():
    venue_label = tk.Label(text="Please select a venue you would like to analyse from the options below")
    venue_label.grid()
    global clicked
    clicked = StringVar(root)
    clicked.set("ALL")
    venue_options = ["ALL","ARC Floor 1", "Climbing", "ARC Olympic Lifting Zones", "ARC Floor 2",
                                     "South Court", "4 Court Gym", "North Court", "Recreation Pool", "Competition Pool",
                                     "ARC Express", "Spa", "Aquaplex Pool Deck", "Tennis Courts"]
    venue_select = OptionMenu(root, clicked, *venue_options)
    venue_select.grid()

    analysis_button = tk.Button(root, text="Submit", command=analysis)
    analysis_button.grid()
    analysis_label= tk.Label(root,text="*Clicking submit will run the analysis*")
    analysis_label.grid()



root = tk.Tk()
root.title("ARC Gym Analysis")
#image = ImageTk.PhotoImage(Image.open("ARC_Image.png"))
#serve_image = Label(root, image=image)
#serve_image.grid()
date_label = tk.Label(text="How would you like to sort through the data?")
all_button = tk.Button(text="All Dates", command=all_data)
range_button = tk.Button(text="Date Range", command=range_data)
all_button.grid()
range_button.grid()

start_cal = DateEntry(root, maxdate=date.today())

start_button = tk.Button(text="Submit Start Range", command=serve_end_cal)

root.mainloop()