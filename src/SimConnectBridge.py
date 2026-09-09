#!/usr/bin/env python3
"""
SimConnect Bridge for MSFS 2020
Handles communication between SimConnect variables and Audio Controller
"""

import logging
from typing import Callable, Dict
from AudioController import AudioController


class SimConnectBridge:
    """Bridge between SimConnect and Audio Controller"""
    
    # SimConnect Variable Definitions
    SIMCONNECT_VARIABLES = {
        'AUDIO_VOLUME': {'type': 'FLOAT32', 'range': (0.0, 1.0)},
        'AUDIO_PLAY': {'type': 'BOOL', 'range': (0, 1)},
        'AUDIO_STOP': {'type': 'BOOL', 'range': (0, 1)},
        'AUDIO_NEXT': {'type': 'BOOL', 'range': (0, 1)},
        'AUDIO_PREVIOUS': {'type': 'BOOL', 'range': (0, 1)},
        'AUDIO_CURRENT_TRACK': {'type': 'STRING32', 'range': None},
        'AUDIO_TRACK_COUNT': {'type': 'INT32', 'range': None},
    }
    
    def __init__(self, audio_controller: AudioController):
        """
        Initialize SimConnect bridge
        
        Args:
            audio_controller: Instance of AudioController
        """
        self.logger = logging.getLogger(__name__)
        self.audio_controller = audio_controller
        
        # Variable state tracking
        self.variable_state: Dict = {
            'AUDIO_VOLUME': 1.0,
            'AUDIO_PLAY': False,
            'AUDIO_STOP': False,
            'AUDIO_NEXT': False,
            'AUDIO_PREVIOUS': False,
            'AUDIO_CURRENT_TRACK': '',
            'AUDIO_TRACK_COUNT': 0,
        }
        
        # Callbacks for variable changes
        self.callbacks: Dict[str, Callable] = {}
        self._register_callbacks()
        
        self.logger.info("SimConnectBridge initialized")
    
    def _register_callbacks(self):
        """Register callbacks for SimConnect variable changes"""
        self.callbacks = {
            'AUDIO_VOLUME': self._handle_volume_change,
            'AUDIO_PLAY': self._handle_play,
            'AUDIO_STOP': self._handle_stop,
            'AUDIO_NEXT': self._handle_next,
            'AUDIO_PREVIOUS': self._handle_previous,
        }
    
    def _handle_volume_change(self, value: float):
        """Handle volume change from SimConnect"""
        self.audio_controller.set_volume(value)
        self.variable_state['AUDIO_VOLUME'] = value
    
    def _handle_play(self, value: bool):
        """Handle play command from SimConnect"""
        if value:
            self.audio_controller.play()
            self.variable_state['AUDIO_PLAY'] = True
    
    def _handle_stop(self, value: bool):
        """Handle stop command from SimConnect"""
        if value:
            self.audio_controller.stop()
            self.variable_state['AUDIO_STOP'] = True
    
    def _handle_next(self, value: bool):
        """Handle next track command from SimConnect"""
        if value:
            self.audio_controller.next_track()
            self.variable_state['AUDIO_NEXT'] = True
    
    def _handle_previous(self, value: bool):
        """Handle previous track command from SimConnect"""
        if value:
            self.audio_controller.previous_track()
            self.variable_state['AUDIO_PREVIOUS'] = True
    
    def update_variables(self):
        """Update SimConnect variables with current audio state"""
        status = self.audio_controller.get_status()
        
        self.variable_state['AUDIO_VOLUME'] = status['volume']
        self.variable_state['AUDIO_CURRENT_TRACK'] = status['current_track'] or ''
        self.variable_state['AUDIO_TRACK_COUNT'] = status['total_tracks']
    
    def process_variable_change(self, var_name: str, value):
        """Process incoming variable change from SimConnect"""
        if var_name not in self.SIMCONNECT_VARIABLES:
            self.logger.warning(f"Unknown variable: {var_name}")
            return
        
        if var_name in self.callbacks:
            try:
                self.callbacks[var_name](value)
                self.logger.debug(f"Processed {var_name} = {value}")
            except Exception as e:
                self.logger.error(f"Error processing {var_name}: {e}")
    
    def get_variable_state(self, var_name: str):
        """Get current state of a SimConnect variable"""
        return self.variable_state.get(var_name)
    
    def get_all_variables(self) -> Dict:
        """Get all SimConnect variables and their current values"""
        self.update_variables()
        return self.variable_state.copy()
