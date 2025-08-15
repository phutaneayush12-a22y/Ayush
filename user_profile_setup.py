import json
import os

def profile_setup():
    a=input("Enter filename in the correct manner that already has to be exist:")
    if os.path.exists(a):
        print("File found")
        with open(a,"r") as file:
            data=json.load(file)
            print("----This is your data present in your file----")
            print(data)
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
         calm_now_choice = input("\nEnter the your choice:").strip()

         filename=input("Enter the json file that you want store all data in like in this format(filename.json):")

         child_profile = {
               "likes_sounds": likes_sounds,
               "likes_visuals": likes_visuals,
               "likes_breathing": likes_breathing,
               "likes_games": likes_games,
               "sensitive_to_sound": sensitive_to_sound,
               "enable_logging": enable_logging,
               "calm_now_choice": calm_now_choice
            }
         


         with open(filename,"w") as file:
             
             data1=json.dump(child_profile,file)
             


profile_setup()



             
