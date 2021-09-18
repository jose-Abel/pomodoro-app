#!/usr/bin/env python3

from tkinter import *
import math
import requests
from datetime import datetime
import os

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 60
SHORT_BREAK_MIN = 10
LONG_BREAK_MIN = 60
reps = 0
timer = None
paused = False
graph = ""
TOKEN = ""
studied_hours = 0
studied_min = 0
today = datetime.now()
duration = 0.5  # seconds
freq = 300  # Hz

# ---------------------------- SAVE PIXEL ------------------------------- #

def save_pixel():
    global graph, TOKEN

    date_update = date_entry.get()
    worked_hours = hours_entry.get()

    if len(worked_hours) == 0:
        worked_hours = f"{studied_hours}"

    headers = {
        "X-USER-TOKEN": TOKEN
    }

    pixel_data = {
        "date": date_update,
        "quantity": worked_hours,
    }
    #
    response = requests.post(url=graph, json=pixel_data, headers=headers)
    success_message.config(text="Success", fg=GREEN)

# ---------------------------- PAUSE TIMER ------------------------------- #

def pause_timer():
    global paused
    paused = not paused


# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        reps = 0
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
        
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer, paused
        if not paused:
            timer = window.after(1000, count_down, count - 1)
        else:
            timer = window.after(1000, count_down, count)
    else:
        global studied_hours, studied_min

        if title_label.cget("text") == "Work":
            studied_hours += math.floor(WORK_MIN / 60)
            studied_min += math.floor(WORK_MIN % 60)
            if WORK_MIN < 60:
            	if studied_min == 60:
            		studied_hours += 1
            		studied_min = 0

        start_timer()

        if studied_min < 10:
            studied_time_label.config(text=f"{studied_hours}:0{studied_min}")
        else:
            studied_time_label.config(text=f"{studied_hours}:{studied_min}")

        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

website_entry = Entry(width=50)
website_entry.grid(column=0, row=0, columnspan=3)
website_entry.insert(0, f"{graph}.html")

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

tomato_img = PhotoImage(file="~/Documents/pomodoro-app/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=2)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)

pause_button = Button(text="Pause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=2, row=3)

save_button = Button(text="Save", highlightthickness=0, command=save_pixel)
save_button.grid(column=0, row=6)

hours_entry = Entry(width=5)
hours_entry.grid(column=1, row=5)

date_entry = Entry(width=10)
date_entry.grid(column=1, row=6)
date_entry.insert(0, f"{today.strftime('%Y%m%d')}")

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=7)

studied_time_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35))
studied_time_label.grid(column=1, row=8)

success_message = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30))
success_message.grid(column=1, row=9)


window.mainloop()











