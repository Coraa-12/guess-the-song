import tkinter as tk
import pygame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_playlist_tracks(playlist_url):
    """
    Fetches track names from a Spotify playlist and filters for English titles.
    Returns a list of dictionaries, where each dictionary represents a track.
    """
    english_tracks = []
    try:
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        results = sp.playlist_tracks(playlist_url)
        
        for item in results['items']:
            track = item['track']
            # Check if the track name contains only ASCII characters
            if track['name'].isascii():
                track_info = {
                    'name': track['name'],
                    'artist': track['artists'][0]['name']
                }
                english_tracks.append(track_info)
        return english_tracks

    except Exception as e:
        print(f"Error fetching from Spotify: {e}")
        return []


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

TARGET_PLAYLIST = "https://open.spotify.com/playlist/4bFczrl6d5rwABtAsqhfwB" 
# Fetch the filtered list of tracks
game_tracks = fetch_playlist_tracks(TARGET_PLAYLIST)

# Print the filtered results to confirm it worked
print("--- Filtered English Tracks ---")
for track in game_tracks:
    print(f"- {track['name']} by {track['artist']}")
print("-----------------------------")


# --- GUI ---
root = tk.Tk()
root.title("Guess The Song")
root.geometry("500x300")

play_button = tk.Button(root, text="Play Clip", command=play_clip)
play_button.pack(pady=10)

root.mainloop()
