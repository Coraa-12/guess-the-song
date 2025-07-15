import tkinter as tk
import pygame

def play_clip():
    """Loads and plays the sample audio file."""
    try:
        pygame.mixer.music.load("MGS_Alert.mp3")
        pygame.mixer.music.play()
        print("Playing sample.mp3")
    except pygame.error as e:
        print(f"Error playing sound: {e}")
        print("Did you place sample.mp3 in the project folder?")

# --- Setup ---
# Initialize the pygame mixer
pygame.mixer.init()

# Create the main application window
root = tk.Tk()
root.title("Guess The Song")
root.geometry("500x300")

# --- Widgets ---
# Create a button widget
play_button = tk.Button(root, text="Play Clip", command=play_clip)
play_button.pack(pady=10) # pady adds some vertical padding

# --- Main Loop ---
root.mainloop()
