import tkinter as tk
import pygame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import random
import yt_dlp
from pydub import AudioSegment

load_dotenv()

# --- Global Game State ---
current_song_info = {}

# --- Core Functions ---
def start_new_round():
    """Selects a new random song, prepares it, and resets the UI."""
    if game_tracks:
        # Clear the previous guess and feedback
        guess_entry.delete(0, tk.END)
        feedback_label.config(text="")

        # Prepare a new song
        random_song = random.choice(game_tracks)
        prepare_song_clip(random_song)
    else:
        feedback_label.config(text="Playlist is empty or failed to load.", fg="red")

def prepare_song_clip(track_info):
    """Downloads a song, cuts a 5-second clip, and stores its info."""
    global current_song_info
    current_song_info = track_info

    search_query = f"{track_info['name']} by {track_info['artist']}"
    # print(f"Preparing song: {current_song_info['name']}") # Keep this commented

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'outtmpl': 'full_song',
        'default_search': 'ytsearch1:',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        song = AudioSegment.from_mp3("full_song.mp3")
        clip = song[30000:35000]
        clip.export("game_clip.mp3", format="mp3")
        # print("Clip created successfully.") # Keep this commented
    except Exception as e:
        print(f"An error occurred during song preparation: {e}")

def fetch_playlist_tracks(playlist_url):
    # This function remains the same
    english_tracks = []
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        results = sp.playlist_tracks(playlist_url)

        for item in results['items']:
            track = item['track']
            if track['name'].isascii():
                track_info = { 'name': track['name'], 'artist': track['artists'][0]['name'] }
                english_tracks.append(track_info)
        return english_tracks
    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        return []

def play_audio(filename):
    """Loads and plays the specified audio file."""
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def stop_audio():
    """Stops the currently playing music."""
    pygame.mixer.music.stop()

def check_guess():
    """Checks the user's guess and plays the full song on failure."""
    user_guess = guess_entry.get()
    correct_answer = current_song_info.get('name', '')

    if user_guess.lower() == correct_answer.lower():
        feedback_label.config(text="Correct! 🎉", fg="green")
    else:
        feedback_label.config(text=f"Nope! It was: {correct_answer}", fg="red")
        # Play the full song to reveal the answer
        play_audio("full_song.mp3")

# --- Setup ---
pygame.mixer.init()
TARGET_PLAYLIST = "https://open.spotify.com/playlist/4bFczrl6d5rwABtAsqhfwB?si=oW7VyhBXSxqXDOfvovOrlg"
game_tracks = fetch_playlist_tracks(TARGET_PLAYLIST)

# --- GUI ---
root = tk.Tk()
root.title("Guess The Song")
root.geometry("500x300")

# --- Widgets ---
# Create a frame to hold the audio control buttons
audio_frame = tk.Frame(root)
audio_frame.pack(pady=5)

# Add the Play and Stop buttons to the frame
play_button = tk.Button(audio_frame, text="▶️ Play Clip", command=lambda: play_audio("game_clip.mp3"))
play_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(audio_frame, text="⏹️ Stop", command=stop_audio)
stop_button.pack(side=tk.LEFT, padx=5)

# Add the rest of the widgets
guess_entry = tk.Entry(root, width=50)
guess_entry.pack(pady=5)

guess_button = tk.Button(root, text="Guess", command=check_guess)
guess_button.pack(pady=5)

next_song_button = tk.Button(root, text="Next Song", command=start_new_round)
next_song_button.pack(pady=10)

feedback_label = tk.Label(root, text="", font=("Helvetica", 12))
feedback_label.pack(pady=10)

# --- Start First Round ---
start_new_round()

# --- Main Loop ---
root.mainloop()
