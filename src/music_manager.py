import pygame
import os

class MusicManager:
    def __init__(self):
        """Initialize the music manager"""
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.current_song = None
        self.song_position = 0
        self.song_start_time = 0
        self.is_music_playing = False
        self.music_volume = 0.5
        self.songs = {}  # Dictionary to store multiple songs

    def load_song(self, song_name, file_path):
        """
        Load a song into the manager
        
        Args:
            song_name (str): Name/identifier for the song
            file_path (str): Path to the music file
        """
        try:
            if os.path.exists(file_path):
                self.songs[song_name] = file_path
                return True
            else:
                print(f"File not found: {file_path}")
                return False
        except Exception as e:
            print(f"Error loading song: {e}")
            return False

    def play(self, song_name=None):
        """
        Play a song. If no song_name is provided, play current song
        """
        try:
            if song_name and song_name in self.songs:
                pygame.mixer.music.load(self.songs[song_name])
                self.current_song = song_name
            
            if self.current_song:
                pygame.mixer.music.play()
                self.is_music_playing = True
                self.song_start_time = pygame.time.get_ticks()
                pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            print(f"Error playing song: {e}")

    def pause(self):
        """Pause the currently playing song"""
        if self.is_music_playing:
            pygame.mixer.music.pause()
            self.song_position = pygame.time.get_ticks() - self.song_start_time
            self.is_music_playing = False

    def resume(self):
        """Resume the paused song"""
        if not self.is_music_playing and self.current_song:
            pygame.mixer.music.unpause()
            self.song_start_time = pygame.time.get_ticks() - self.song_position
            self.is_music_playing = True

    def stop(self):
        """Stop the current song"""
        pygame.mixer.music.stop()
        self.is_music_playing = False
        self.song_position = 0

    def set_volume(self, volume):
        """
        Set the music volume
        
        Args:
            volume (float): Volume level between 0.0 and 1.0
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def get_current_time(self):
        """Get the current playback position in milliseconds"""
        if self.is_music_playing:
            return pygame.time.get_ticks() - self.song_start_time
        return self.song_position

    def is_playing(self):
        """Check if music is currently playing"""
        return self.is_music_playing