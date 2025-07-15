import tkinter as tk

def play_clip_placeholder():
    """A placeholder function for our button."""
    print("Play button clicked! (No audio yet)")

# Create the main application window
root = tk.Tk()

# Set the title of the window
root.title("Guess The Song")

# Set the size of the window (width x height)
root.geometry("500x300")

# Create a button widget
play_button = tk.Button(root, text="Play Clip", command=play_clip_placeholder)

# Add the button to the window
play_button.pack()

# Start the application's main loop
root.mainloop()
