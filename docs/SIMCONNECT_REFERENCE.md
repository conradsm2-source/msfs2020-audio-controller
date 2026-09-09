# SimConnect Reference Guide

## Overview

SimConnect is the SDK that allows aircraft add-ons to communicate with MSFS 2020. The Audio Controller uses SimConnect to:
- Read and write simulation variables
- Receive and send events
- Synchronize with the simulation

## SimConnect Variable Types

### FLOAT32
- 32-bit floating point number
- Range: -3.4E+38 to +3.4E+38
- Precision: ~7 decimal digits
- **Used for**: AUDIO_VOLUME

### BOOL
- Boolean value (0 or 1)
- Used for: Event triggers
- **Used for**: AUDIO_PLAY, AUDIO_STOP, AUDIO_NEXT, AUDIO_PREVIOUS

### INT32
- 32-bit signed integer
- Range: -2,147,483,648 to 2,147,483,647
- **Used for**: AUDIO_TRACK_COUNT, AUDIO_TRACK_INDEX

### STRING32
- 32-character string
- **Used for**: AUDIO_CURRENT_TRACK

## Audio Controller Variables

### Master Control Variables

#### AUDIO_VOLUME
```python
# Python example
bridge.process_variable_change('AUDIO_VOLUME', 0.75)  # Set volume to 75%
volume = bridge.get_variable_state('AUDIO_VOLUME')    # Get current volume
```

#### AUDIO_PLAY
```python
# Trigger play
bridge.process_variable_change('AUDIO_PLAY', 1)
```

#### AUDIO_STOP
```python
# Trigger stop
bridge.process_variable_change('AUDIO_STOP', 1)
```

#### AUDIO_NEXT
```python
# Play next track
bridge.process_variable_change('AUDIO_NEXT', 1)
```

#### AUDIO_PREVIOUS
```python
# Play previous track
bridge.process_variable_change('AUDIO_PREVIOUS', 1)
```

### Status Variables (Read-Only)

#### AUDIO_CURRENT_TRACK
```python
# Get current track filename
current = bridge.get_variable_state('AUDIO_CURRENT_TRACK')
print(f"Now playing: {current}")
```

#### AUDIO_TRACK_COUNT
```python
# Get total number of tracks
total = bridge.get_variable_state('AUDIO_TRACK_COUNT')
print(f"Total tracks: {total}")
```

#### AUDIO_IS_PLAYING
```python
# Check if audio is playing
is_playing = bridge.get_variable_state('AUDIO_IS_PLAYING')
if is_playing:
    print("Audio is playing")
else:
    print("Audio is stopped")
```

#### AUDIO_TRACK_INDEX
```python
# Get current track index (0-based)
index = bridge.get_variable_state('AUDIO_TRACK_INDEX')
print(f"Playing track {index + 1}")
```

## SimConnect Connection

### Polling Method

Poll for variable updates at regular intervals:

```python
import time
from src.AudioController import AudioController
from src.SimConnectBridge import SimConnectBridge

controller = AudioController()
bridge = SimConnectBridge(controller)

while True:
    # Update variables from SimConnect
    bridge.update_variables()
    
    # Get all current states
    states = bridge.get_all_variables()
    print(f"Volume: {states['AUDIO_VOLUME']}")
    print(f"Playing: {states['AUDIO_CURRENT_TRACK']}")
    
    time.sleep(0.1)  # 100ms polling interval
```

### Event-Driven Method

Handle specific variable changes:

```python
# When AUDIO_PLAY changes to 1
bridge.process_variable_change('AUDIO_PLAY', 1)

# When AUDIO_VOLUME changes
bridge.process_variable_change('AUDIO_VOLUME', 0.8)

# When AUDIO_NEXT is triggered
bridge.process_variable_change('AUDIO_NEXT', 1)
```

## Common Workflows

### Play Audio
```python
# Set volume first
bridge.process_variable_change('AUDIO_VOLUME', 0.5)

# Then play
bridge.process_variable_change('AUDIO_PLAY', 1)
```

### Volume Control
```python
# Increase volume
current_vol = bridge.get_variable_state('AUDIO_VOLUME')
bridge.process_variable_change('AUDIO_VOLUME', min(current_vol + 0.1, 1.0))

# Decrease volume
bridge.process_variable_change('AUDIO_VOLUME', max(current_vol - 0.1, 0.0))
```

### Track Navigation
```python
# Next track
bridge.process_variable_change('AUDIO_NEXT', 1)

# Previous track
bridge.process_variable_change('AUDIO_PREVIOUS', 1)
```

### Get Playback Status
```python
status = {
    'track': bridge.get_variable_state('AUDIO_CURRENT_TRACK'),
    'index': bridge.get_variable_state('AUDIO_TRACK_INDEX'),
    'total': bridge.get_variable_state('AUDIO_TRACK_COUNT'),
    'volume': bridge.get_variable_state('AUDIO_VOLUME'),
    'playing': bridge.get_variable_state('AUDIO_IS_PLAYING')
}

print(f"Now playing: {status['track']}")
print(f"Track: {status['index']+1}/{status['total']}")
print(f"Volume: {status['volume']*100:.0f}%")
```

## Error Handling

### Variable Out of Range
```python
try:
    # Volume must be 0.0 - 1.0
    bridge.process_variable_change('AUDIO_VOLUME', 1.5)  # Will be clamped
except ValueError as e:
    print(f"Error: {e}")
```

### Unknown Variable
```python
try:
    bridge.process_variable_change('AUDIO_INVALID', 1)
except KeyError:
    print("Variable not recognized")
```

### No Audio Files
```python
if bridge.get_variable_state('AUDIO_TRACK_COUNT') == 0:
    print("No audio files found in folder")
```

## Performance Considerations

1. **Polling Interval**: Use 100-200ms for responsive controls
2. **Variable Updates**: Only update variables that changed
3. **String Variables**: Minimize updates to STRING32 variables
4. **Logging**: Disable debug logging in production

## Debugging

### Check Variable States
```python
all_vars = bridge.get_all_variables()
for var_name, value in all_vars.items():
    print(f"{var_name}: {value}")
```

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```python
from src.MP3Manager import MP3Manager

mp3_manager = MP3Manager(r"C:\Music\MSFS_Audio")
print(f"Found {mp3_manager.get_track_count()} tracks")
mp3_manager.print_playlist()
```

## XML Integration

SimConnect variables defined in XML are automatically available:

```xml
<Variable Name="AUDIO_VOLUME" Type="FLOAT32" Min="0.0" Max="1.0"/>
```

Access in Python:
```python
bridge.process_variable_change('AUDIO_VOLUME', 0.7)
```

## Best Practices

1. **Always clamp numeric values**
   ```python
   volume = max(0.0, min(1.0, volume))  # Ensure 0.0-1.0 range
   ```

2. **Reset toggle variables after use**
   ```python
   bridge.process_variable_change('AUDIO_PLAY', 1)
   # After 500ms, reset:
   bridge.process_variable_change('AUDIO_PLAY', 0)
   ```

3. **Check for errors gracefully**
   ```python
   if bridge.get_variable_state('AUDIO_TRACK_COUNT') > 0:
       bridge.process_variable_change('AUDIO_PLAY', 1)
   ```

4. **Log important events**
   ```python
   logging.info(f"Playing: {current_track}")
   ```

5. **Synchronize with simulation time**
   ```python
   # Only process variable changes when MSFS is running
   ```
