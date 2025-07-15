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

def prepare_song_clip(track_info):
    """Downloads a song, cuts a 5-second clip, and stores its info."""
    global current_song_info
    current_song_info = track_info
    
    search_query = f"{track_info['name']} by {track_info['artist']}"
    # print(f"Preparing song: {current_song_info['name']}") # <--- COMMENT THIS OUT

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
        # print("Download complete.") # <--- COMMENT THIS OUT

        song = AudioSegment.from_mp3("full_song.mp3")
        clip = song[30000:35000] 
        clip.export("game_clip.mp3", format="mp3")
        # print("Clip created successfully.") # <--- COMMENT THIS OUT
    except Exception as e:
        print(f"An error occurred during song preparation: {e}")

def fetch_playlist_tracks(playlist_url):
    # ... (this function remains the same)
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

def play_clip():
    """Loads and plays the sample audio file."""
    try:
        pygame.mixer.music.load("game_clip.mp3")
        pygame.mixer.music.play()
        print("Playing game_clip.mp3")
    except pygame.error as e:
        print(f"Error playing sound: {e}")
        print("Has the game clip been created yet?")

# --- Setup ---
pygame.mixer.init()

TARGET_PLAYLIST = "https://open.spotify.com/playlist/4bFczrl6d5rwABtAsqhfwB?si=5wY9ch0DS3KFpqpUK0mc1Q"
game_tracks = fetch_playlist_tracks(TARGET_PLAYLIST)

if game_tracks:
    # Pick a random song from our list and prepare it
    random_song = random.choice(game_tracks)
    prepare_song_clip(random_song)
else:
    print("No tracks found to prepare. Check your playlist URL.")

# --- GUI ---
root = tk.Tk()
root.title("Guess The Song")
root.geometry("500x300")

play_button = tk.Button(root, text="Play Clip", command=play_clip)
play_button.pack(pady=10)

root.mainloop()
