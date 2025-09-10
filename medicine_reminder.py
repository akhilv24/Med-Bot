import json
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st
import os

# File path to store reminders
REMINDER_FILE = Path("reminders.json")

# Load existing reminders
def load_reminders():
    if REMINDER_FILE.exists():
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return []

##
def play_reminder_audio():
    audio_path = "reminder.ogg"  # Your uploaded audio file
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/ogg", start_time=0)
    else:
        st.warning("Reminder audio file not found.")

# Save reminders
def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)
        
def clear_all_reminders():
    save_reminders([])

# Add a new reminder
def add_reminder(medicine_name, time_str, dosage):
    reminders = load_reminders()
    reminder = {
        "medicine": medicine_name,
        "time": time_str,
        "dosage": dosage,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    reminders.append(reminder)
    save_reminders(reminders)

# Get reminders for current time range
def get_due_reminders():
    now = datetime.now()
    reminders = load_reminders()
    due = []
    for rem in reminders:
        reminder_time = datetime.strptime(rem["time"], "%H:%M")
        # match hour and minute only
        if now.hour == reminder_time.hour and abs(now.minute - reminder_time.minute) <= 5:
            due.append(rem)
    return due
