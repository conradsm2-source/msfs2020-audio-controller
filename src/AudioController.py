#!/usr/bin/env python3
"""
MSFS 2020 Aircraft Audio Controller
Manages MP3 playback and integration with SimConnect variables
"""

import os
import json
import logging
import pygame
from pathlib import Path
from typing import List, Optional

class AudioController:
    """Main audio controller for MSFS aircraft"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """
        Initialize the audio controller
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()
        
        # Audio state variables
        self.current_track_index = 0
        self.is_playing = False
        self.volume = 1.0
        self.playlist: List[str] = []
        self.current_track: Optional[str] = None
        
        # Load MP3 files from external folder
        self._load_playlist()
        
        self.logger.info(f"AudioController initialized. Found {len(self.playlist)} tracks")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {config_path}")
            return {}
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, "audio_controller.log")),
                logging.StreamHandler()
            ]
        )
    
    def _load_playlist(self):
        """Load all MP3 files from configured folder"""
        mp3_folder = self.config.get('mp3_folder_path', 'C:\\Music\\MSFS_Audio')
        
        if not os.path.exists(mp3_folder):
            self.logger.warning(f"MP3 folder not found: {mp3_folder}")
            return
        
        supported_formats = tuple(self.config.get('supported_formats', ['mp3']))
        
        try:
            for file in sorted(os.listdir(mp3_folder)):
                if file.lower().endswith(supported_formats):
                    full_path = os.path.join(mp3_folder, file)
                    self.playlist.append(full_path)
            
            self.logger.info(f"Loaded {len(self.playlist)} audio files")
        except Exception as e:
            self.logger.error(f"Error loading playlist: {e}")
    
    def play(self) -> bool:
        """Play current track"""
        if not self.playlist or self.current_track_index >= len(self.playlist):
            self.logger.warning("No tracks available to play")
            return False
        
        try:
            track_path = self.playlist[self.current_track_index]
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            self.is_playing = True
            self.current_track = os.path.basename(track_path)
            self.logger.info(f"Playing: {self.current_track}")
            return True
        except Exception as e:
            self.logger.error(f"Error playing track: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop playback"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.logger.info("Playback stopped")
            return True
        except Exception as e:
            self.logger.error(f"Error stopping playback: {e}")
            return False
    
    def next_track(self) -> bool:
        """Play next track"""
        if not self.playlist:
            return False
        
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.logger.info(f"Next track: index {self.current_track_index}")
        return self.play()
    
    def previous_track(self) -> bool:
        """Play previous track"""
        if not self.playlist:
            return False
        
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.logger.info(f"Previous track: index {self.current_track_index}")
        return self.play()
    
    def set_volume(self, volume: float) -> bool:
        """Set volume level (0.0 - 1.0)"""
        try:
            volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(volume)
            self.volume = volume
            self.logger.info(f"Volume set to: {volume:.2f}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting volume: {e}")
            return False
    
    def increase_volume(self) -> float:
        """Increase volume by step"""
        step = self.config.get('volume_step', 0.05)
        new_volume = self.volume + step
        self.set_volume(new_volume)
        return self.volume
    
    def decrease_volume(self) -> float:
        """Decrease volume by step"""
        step = self.config.get('volume_step', 0.05)
        new_volume = self.volume - step
        self.set_volume(new_volume)
        return self.volume
    
    def get_status(self) -> dict:
        """Get current playback status"""
        return {
            'is_playing': self.is_playing,
            'current_track': self.current_track,
            'track_index': self.current_track_index,
            'total_tracks': len(self.playlist),
            'volume': self.volume,
            'playlist': self.playlist
        }


if __name__ == "__main__":
    controller = AudioController()
    print(f"Loaded {len(controller.playlist)} tracks")
