import socket
import os
import requests
import shutil
import json
import tkinter as tk
from tkinter import messagebox
import random
import math
import time
import pygame  


CREDENTIALS_FILE = "users.json"
PROFILE_FILE = "profile.json"  


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=4)
        return True
    except OSError:
        return False

def download_file(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, url.split("/")[-1])
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    print(f"Downloaded: {filename}")

def update_resources():
    if check_internet():
        print("Internet found 🌐 — downloading online resources...")
        online_folder = "online_resources"
        if not os.path.exists(online_folder):
            os.makedirs(online_folder)
        urls = [
            "https://cdn.pixabay.com/download/audio/2024/03/15/audio_0d2a689d30.mp3",
            "https://cdn.pixabay.com/download/audio/2025/06/21/audio_fba2cc81f7.mp3",
            "https://videos.pexels.com/video-files/3571264/3571264-uhd_3840_2160_30fps.mp4"
        ]
        for url in urls:
            download_file(url, online_folder)
        if not os.path.exists("local_resources"):
            os.makedirs("local_resources")
        for filename in os.listdir(online_folder):
            shutil.copy(os.path.join(online_folder, filename),
                        os.path.join("local_resources", filename))
        print("----Local storage updated----")
    else:
        print("----No internet — using local resources----")
        if os.path.exists("local_resources"):
            print(f"Found {len(os.listdir('local_resources'))} local files.")
        else:
            print("----No local resources found----")

def cm_to_pixels(cm, root):
    inches = cm / 2.54
    return int(inches * root.winfo_fpixels('1i'))


def profile_setup():
    a = input("Enter filename in the correct manner that already has to be exist:")
    if os.path.exists(a):
        print("File found")
        with open(a, "r") as file:
            data = json.load(file)
            print("----This is your data present in your file----")
            print(data)
        return data
    else:
        print("File is not found ")
        print("----👋 Welcome! Let's set up your child's sensory preferences.----\n")
        likes_sounds = input("Step 1/6: Does your child enjoy calming sounds (like rain, ocean waves)? (Y/N): ").strip().upper() == "Y"
        likes_visuals = input("Step 2/6: Does your child enjoy visual animations (like soft patterns or colors)? (Y/N): ").strip().upper() == "Y"
        likes_breathing = input("Step 3/6: Does your child find breathing guides helpful? (Y/N): ").strip().upper() == "Y"
        likes_games = input("Step 4/6: Does your child enjoy soothing games (like popping bubbles)? (Y/N): ").strip().upper() == "Y"
        sensitive_to_sound = input("Step 5/6: Is your child sensitive to sound? (Y/N): ").strip().upper() == "Y"
        enable_logging = input("Step 6/6: Would you like to enable session logging to track calming tool usage? (Y/N): ").strip().upper() == "Y"
        print("\n✅ Now choose your child’s favorite calming tool for the “Calm Now” button:")
        print("  1. Calming Sounds")
        print("  2. Visual Animations")
        print("  3. Breathing Guide")
        print("  4. Soothing Games")
        calm_now_choice = input("\nEnter your choice:").strip()
        filename = input("Enter the json file that you want to store all data in (format: filename.json): ")
        child_profile = {
            "likes_sounds": likes_sounds,
            "likes_visuals": likes_visuals,
            "likes_breathing": likes_breathing,
            "likes_games": likes_games,
            "sensitive_to_sound": sensitive_to_sound,
            "enable_logging": enable_logging,
            "calm_now_choice": calm_now_choice
        }
        with open(filename, "w") as file:
            json.dump(child_profile, file)
        return child_profile

def load_profile_toolkit():
    return profile_setup()


def play_calming_sounds():
    try:
        local_folder = "local_resources"
        sound_file = None
        if os.path.exists(local_folder):
            for file in os.listdir(local_folder):
                if file.lower().endswith(".mp3"):
                    sound_file = os.path.join(local_folder, file)
                    break
        if sound_file:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            messagebox.showinfo("Calming Sounds", f"Playing: {os.path.basename(sound_file)}")
        else:
            messagebox.showwarning("No Sound Found", "No MP3 file found in local_resources folder.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not play sound: {e}")

def show_visual_animations():
    try:
        local_folder = "local_resources"
        video_file = None
        if os.path.exists(local_folder):
            for file in os.listdir(local_folder):
                if file.lower().endswith(".mp4"):
                    video_file = os.path.join(local_folder, file)
                    break
        if video_file:
            messagebox.showinfo("Visual Animations", f"Playing Video: {os.path.basename(video_file)}")
            os.startfile(video_file)
        else:
            messagebox.showwarning("No Video Found", "No MP4 file found in local_resources folder.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not play video: {e}")

def start_breathing_guide():
    guide_win = tk.Toplevel()
    guide_win.title("Breathing Guide")
    guide_win.configure(bg="lightgreen")
    canvas = tk.Canvas(guide_win, width=400, height=400, bg="lightgreen", highlightthickness=0)
    canvas.pack()
    bubble = canvas.create_oval(150, 150, 250, 250, fill="lightblue", outline="")
    phase_text = canvas.create_text(200, 50, text="Get Ready...", font=("Arial", 18), fill="black")
    phases = [("Inhale", 4), ("Hold", 4), ("Exhale", 4)]
    total_cycles = 3
    current_cycle = [0]
    current_phase = [0]
    start_time = [time.time()]
    def animate():
        elapsed = time.time() - start_time[0]
        phase_name, duration = phases[current_phase[0]]
        progress = elapsed / duration
        if phase_name == "Inhale":
            radius = 50 + (progress * 50)
            canvas.itemconfig(phase_text, text="Inhale deeply...")
        elif phase_name == "Hold":
            radius = 100
            canvas.itemconfig(phase_text, text="Hold...")
        elif phase_name == "Exhale":
            radius = 100 - (progress * 50)
            canvas.itemconfig(phase_text, text="Exhale slowly...")
        canvas.coords(bubble, 200 - radius, 200 - radius, 200 + radius, 200 + radius)
        if elapsed >= duration:
            current_phase[0] += 1
            if current_phase[0] >= len(phases):
                current_phase[0] = 0
                current_cycle[0] += 1
                if current_cycle[0] >= total_cycles:
                    canvas.itemconfig(phase_text, text="Session Complete!")
                    return
            start_time[0] = time.time()
        guide_win.after(20, animate)
    animate()

def start_soothing_game():
    game_win = tk.Toplevel()
    game_win.title("Bubble Popping Game")
    game_win.geometry("600x400")
    canvas = tk.Canvas(game_win, width=600, height=400, bg="lightblue")
    canvas.pack()
    bubbles = []
    def create_bubble():
        x = random.randint(20, 550)
        y = random.randint(20, 350)
        bubble = canvas.create_oval(x, y, x+30, y+30, fill="pink", outline="")
        bubbles.append(bubble)
        game_win.after(1000, create_bubble)
    def pop_bubble(event):
        clicked = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for bubble in clicked:
            if bubble in bubbles:
                canvas.delete(bubble)
                bubbles.remove(bubble)
    canvas.bind("<Button-1>", pop_bubble)
    create_bubble()

def parent_settings(root, profile):
    settings_window = tk.Toplevel(root)
    settings_window.title("Parent Settings")
    settings_window.geometry("400x300")
    tk.Label(settings_window, text="Select Tools for Child", font=("Arial", 14)).pack(pady=10)
    var_sounds = tk.BooleanVar(value=profile["likes_sounds"])
    var_visuals = tk.BooleanVar(value=profile["likes_visuals"])
    var_breathing = tk.BooleanVar(value=profile["likes_breathing"])
    var_games = tk.BooleanVar(value=profile["likes_games"])
    tk.Checkbutton(settings_window, text="Calming Sounds", variable=var_sounds).pack(anchor="w", padx=20)
    tk.Checkbutton(settings_window, text="Visual Animations", variable=var_visuals).pack(anchor="w", padx=20)
    tk.Checkbutton(settings_window, text="Breathing Guide", variable=var_breathing).pack(anchor="w", padx=20)
    tk.Checkbutton(settings_window, text="Soothing Games", variable=var_games).pack(anchor="w", padx=20)
    tk.Label(settings_window, text="Favorite Tool (1=Sounds, 2=Visuals, 3=Breathing, 4=Games)").pack(pady=5)
    fav_var = tk.StringVar(value=profile.get("calm_now_choice", "1"))
    tk.Entry(settings_window, textvariable=fav_var).pack()
    def save_preferences():
        profile["likes_sounds"] = var_sounds.get()
        profile["likes_visuals"] = var_visuals.get()
        profile["likes_breathing"] = var_breathing.get()
        profile["likes_games"] = var_games.get()
        profile["calm_now_choice"] = fav_var.get()
        filename = input("Enter the json file name to save updated preferences: ")
        with open(filename, "w") as file:
            json.dump(profile, file)
        messagebox.showinfo("Saved", "Preferences updated successfully!")
        settings_window.destroy()
    tk.Button(settings_window, text="Save", command=save_preferences).pack(pady=20)

def start_favorite(profile):
    fav = profile.get("calm_now_choice", "1")
    if fav == "1":
        play_calming_sounds()
    elif fav == "2":
        show_visual_animations()
    elif fav == "3":
        start_breathing_guide()
    elif fav == "4":
        start_soothing_game()

def welcome_screen(profile):
    win = tk.Toplevel()
    win.title("Welcome - Choose Activity")
    tk.Label(win, text="Choose a calming activity:", font=("Arial", 16)).pack(pady=15)
    if profile.get("likes_sounds", False):
        tk.Button(win, text="Calming Sounds", width=20, height=2, command=play_calming_sounds).pack(pady=5)
    if profile.get("likes_visuals", False):
        tk.Button(win, text="Visual Animations", width=20, height=2, command=show_visual_animations).pack(pady=5)
    if profile.get("likes_breathing", False):
        tk.Button(win, text="Breathing Guide", width=20, height=2, command=start_breathing_guide).pack(pady=5)
    if profile.get("likes_games", False):
        tk.Button(win, text="Soothing Games", width=20, height=2, command=start_soothing_game).pack(pady=5)
    tk.Button(win, text="Modify Settings", width=20, height=2, command=lambda: parent_settings(win, profile)).pack(pady=10)


def save_credentials(username, password):
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}
    users[username] = password
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(users, f)

def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

def signup_screen():
    signup_win = tk.Tk()
    signup_win.title("Sign Up")
    signup_win.geometry("300x250")
    tk.Label(signup_win, text="Create User ID:").pack(pady=5)
    user_entry = tk.Entry(signup_win)
    user_entry.pack()
    tk.Label(signup_win, text="Create Password:").pack(pady=5)
    pass_entry = tk.Entry(signup_win, show="*")
    pass_entry.pack()
    def register_user():
        user_id = user_entry.get().strip()
        password = pass_entry.get().strip()
        if "@" not in user_id or not user_id.endswith(".com"):
            messagebox.showerror("Error", "Invalid User ID. Must contain '@' and end with '.com'.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return
        users = load_credentials()
        if user_id in users:
            messagebox.showerror("Error", "User already exists! Please login.")
            signup_win.destroy()
            login_screen()
            return
        save_credentials(user_id, password)
        messagebox.showinfo("Success", "Sign Up Successful! Please login.")
        signup_win.destroy()
        login_screen()
    tk.Button(signup_win, text="Sign Up", command=register_user).pack(pady=20)
    signup_win.mainloop()

def login_screen():
    login_win = tk.Tk()
    login_win.title("Login")
    login_win.geometry("300x250")
    tk.Label(login_win, text="User ID:").pack(pady=5)
    user_entry = tk.Entry(login_win)
    user_entry.pack()
    tk.Label(login_win, text="Password:").pack(pady=5)
    pass_entry = tk.Entry(login_win, show="*")
    pass_entry.pack()
    def validate_login():
        user_id = user_entry.get().strip()
        password = pass_entry.get().strip()
        users = load_credentials()
        if user_id not in users:
            messagebox.showerror("Error", "User not found! Please sign up.")
            return
        if users[user_id] != password:
            messagebox.showerror("Error", "Incorrect password.")
            return
        messagebox.showinfo("Success", "Login Successful!")
        login_win.destroy()
        update_resources()
        profile = load_profile_toolkit()
        main_ui(profile)
    tk.Button(login_win, text="Login", command=validate_login).pack(pady=10)
    tk.Button(login_win, text="Sign Up", command=lambda: [login_win.destroy(), signup_screen()]).pack(pady=10)
    login_win.mainloop()


def main_ui(profile):
    root = tk.Tk()
    root.title("Sensory Comfort Toolkit")
    width_px = cm_to_pixels(20, root)
    height_px = cm_to_pixels(10, root)
    root.geometry(f"{width_px}x{height_px}")
    tk.Label(root, text="Sensory Comfort Toolkit", font=("Arial", 16)).pack(pady=15)
    tk.Button(root, text="Calm Now", width=20, height=2, command=lambda: start_favorite(profile)).pack(pady=10)
    tk.Button(root, text="Welcome", width=20, height=2, command=lambda: welcome_screen(profile)).pack(pady=10)
    root.mainloop()


if __name__ == "__main__":
    login_screen()
