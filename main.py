import tkinter as tk
import pygame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os # To read environment variables
from dotenv import load_dotenv

load_dotenv()

def fetch_playlist_tracks(playlist_url):
    """Fetches track names and artists from a Spotify playlist."""
    try:
        # Authenticate with Spotify using your credentials
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)

        results = sp.playlist_tracks(playlist_url)
        tracks = results['items']
        
        print("--- Found Tracks ---")
        for item in tracks:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            print(f"- {track_name} by {artist_name}")
        print("--------------------")

    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        print("Are your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables set correctly?")


def play_clip():
    """Loads and plays the sample audio file."""
    try:
        pygame.mixer.music.load("sample.mp3")
        pygame.mixer.music.play()
        print("Playing sample.mp3")
    except pygame.error as e:
        print(f"Error playing sound: {e}")

# --- Setup ---
pygame.mixer.init()

# <<<<<<< NEW CODE HERE <<<<<<<
# Find any public Spotify playlist and paste its URL here
# For example: "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
TARGET_PLAYLIST = "https://open.spotify.com/playlist/4bFczrl6d5rwABtAsqhfwB" 
fetch_playlist_tracks(TARGET_PLAYLIST)
# >>>>>>>>>>>> END NEW CODE >>>>>>>>>>>>

# --- GUI ---
root = tk.Tk()
root.title("Guess The Song")
root.geometry("500x300")

play_button = tk.Button(root, text="Play Clip", command=play_clip)
play_button.pack(pady=10)

root.mainloop()
