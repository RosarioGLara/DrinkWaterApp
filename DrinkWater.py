import tkinter as tk
import json
from datetime import datetime
import os
from tkinter import *


def getDay():
    return datetime.now().strftime("%Y-%m-%d")

def send_notification():
    date = datetime.now()
    hour = date.hour
    day = getDay()

    try:
        with open('save_goals.json', 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 
    
    glasses_remaining = int(data.get(day, {}).get('glasses drunk', 0))
    total_glasses = int(data.get(day, {}).get('hydration goal',0))

    if glasses_remaining == total_glasses  or hour >= 23:
        data[day]['missed glasses'] -= 1
        print('goal completed')
        root.destroy()
        return 

    popup = tk.Toplevel(root)
    popup.title('Hydration Remainder')
    popup.geometry('250x150')
    tk.Label(popup, text= 'Time for another glass!').pack(pady=5)
    def ready():
        data[day]['missed glasses'] = total_glasses - 1
        data[day]['glasses drunk'] = glasses_remaining + 1

        with open('save_goals.json', 'w') as file:
            json.dump(data,file, indent=2)
        popup.destroy()
        root.after(60000, send_notification)
    def later():
        popup.destroy()
        root.after(60000, send_notification)

    tk.Button(popup, text='Ready', command=ready).pack(pady=5)
    tk.Button(popup, text='Later', command=later).pack(pady=5)

def submit_goal():
    day = getDay()
    goal = int(entry.get())
    filename = 'save_goals.json'
    data = {}
    #check if the file exists 
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            data = {day: { 'hydration goal' : goal, 
                          'glases drunk' : 0, 
                          'missed glasses' : goal-1} }
            json.dump(data, file, indent = 2)
            return
    #if it exists then you continue to keep track of your data. 
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = {}
    #check if the user wants to update the number of glasses drunk
    if day not in data: 
        data = {day: { 'hydration goal' : goal,  'glasses drunk' : 0 , 'missed glasses': goal-1}}
    else:
        data[day]['hydration goal'] = int(goal)
    
    with open(filename, 'w') as file:
        json.dump(data,file, indent=2)
    entry.config(state='disabled')

def show_message():
    confirmation_label.config(text='Goal Saved!')

def do_both():
    submit_goal()
    show_message()

root = tk.Tk()
root.title('Water Drinking Tracker')
root.geometry("300x300")

text = tk.Label(root, text='Welcome to your hydration tracker')
goal = tk.Label(root, text='Set your drinking goal (glasses):')
entry = tk.Entry(root, width=10, bg='gray')
submit_button = tk.Button(root, text='Submit', command=do_both,
                          state=tk.ACTIVE, width=5, justify=CENTER)
start_button = tk.Button(root, text='Start', command= send_notification)
confirmation_label = tk.Label(root, text='', fg='green')  # Add this label to show feedback

text.pack(pady=10)
goal.pack()
entry.pack(pady=5)
submit_button.pack(pady=10)
confirmation_label.pack(pady=5)
start_button.pack(pady=20)
root.mainloop()
