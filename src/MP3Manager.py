#!/usr/bin/env python3
"""
MP3 Manager
Handles MP3 file discovery, validation, and metadata retrieval
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional


class MP3Manager:
    """Manages MP3 files in external folder"""
    
    SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'ogg']
    
    def __init__(self, folder_path: str):
        """
        Initialize MP3 Manager
        
        Args:
            folder_path: Path to folder containing audio files
        """
        self.logger = logging.getLogger(__name__)
        self.folder_path = folder_path
        self.playlist: List[Dict] = []
        self._scan_folder()
    
    def _scan_folder(self):
        """Scan folder and build playlist"""
        if not os.path.exists(self.folder_path):
            self.logger.error(f"Folder not found: {self.folder_path}")
            return
        
        try:
            for filename in sorted(os.listdir(self.folder_path)):
                file_path = os.path.join(self.folder_path, filename)
                
                if os.path.isfile(file_path):
                    ext = filename.split('.')[-1].lower()
                    if ext in self.SUPPORTED_FORMATS:
                        track_info = self._get_file_info(file_path, filename)
                        self.playlist.append(track_info)
            
            self.logger.info(f"Scanned folder. Found {len(self.playlist)} audio files")
        except Exception as e:
            self.logger.error(f"Error scanning folder: {e}")
    
    def _get_file_info(self, file_path: str, filename: str) -> Dict:
        """Extract file information"""
        try:
            stat = os.stat(file_path)
            return {
                'filename': filename,
                'full_path': file_path,
                'size_bytes': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'extension': filename.split('.')[-1].lower(),
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
            }
        except Exception as e:
            self.logger.error(f"Error getting file info for {filename}: {e}")
            return {}
    
    def get_playlist(self) -> List[Dict]:
        """Get current playlist"""
        return self.playlist
    
    def get_track_by_index(self, index: int) -> Optional[Dict]:
        """Get track by index"""
        if 0 <= index < len(self.playlist):
            return self.playlist[index]
        return None
    
    def get_track_count(self) -> int:
        """Get total number of tracks"""
        return len(self.playlist)
    
    def filter_by_extension(self, extension: str) -> List[Dict]:
        """Filter playlist by file extension"""
        return [track for track in self.playlist if track['extension'] == extension.lower()]
    
    def search_by_filename(self, search_term: str) -> List[Dict]:
        """Search playlist by filename"""
        search_term = search_term.lower()
        return [track for track in self.playlist if search_term in track['filename'].lower()]
    
    def get_total_size(self) -> Dict:
        """Get total size of all files"""
        total_bytes = sum(track.get('size_bytes', 0) for track in self.playlist)
        return {
            'bytes': total_bytes,
            'mb': total_bytes / (1024 * 1024),
            'gb': total_bytes / (1024 * 1024 * 1024),
        }
    
    def refresh_playlist(self):
        """Refresh playlist from folder"""
        self.playlist.clear()
        self._scan_folder()
        self.logger.info("Playlist refreshed")
    
    def print_playlist(self):
        """Print formatted playlist"""
        print("\n" + "="*60)
        print(f"Playlist: {self.folder_path}")
        print(f"Total Tracks: {len(self.playlist)}")
        print("="*60)
        
        for idx, track in enumerate(self.playlist, 1):
            print(f"{idx:3d}. {track['filename']} ({track['size_mb']:.2f} MB)")
        
        total_size = self.get_total_size()
        print("="*60)
        print(f"Total Size: {total_size['mb']:.2f} MB ({total_size['gb']:.2f} GB)")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Example usage
    manager = MP3Manager(r"C:\Music\MSFS_Audio")
    manager.print_playlist()
