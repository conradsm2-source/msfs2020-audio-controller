# Installation Guide - MSFS 2020 Audio Controller

## Prerequisites

- Microsoft Flight Simulator 2020
- Python 3.8 or higher
- SimConnect SDK
- Windows OS (C: drive access required)

## Step 1: Install Python Dependencies

```bash
pip install pygame
```

## Step 2: Configure External MP3 Folder

1. Create a folder on your C: drive (e.g., `C:\Music\MSFS_Audio`)
2. Add your MP3 files to this folder
3. Edit `config/config.json`:

```json
{
  "mp3_folder_path": "C:\\Your\\Path\\To\\Music",
  "supported_formats": ["mp3", "wav", "flac"]
}
```

## Step 3: Install SimConnect SDK

1. Download SimConnect SDK from [Microsoft Flight Simulator SDK](https://www.flightsimulator.com/)
2. Install to your MSFS 2020 directory
3. Note the installation path for later use

## Step 4: Add to Aircraft Model

1. Locate your aircraft's `model.xml` file
2. Add the following include:

```xml
<Include Path="path/to/model_integration.xml"/>
```

3. Or manually copy the SimVars section from `xml/model_integration.xml`

## Step 5: Test the System

### Run Audio Controller

```bash
python src/AudioController.py
```

### Run MP3 Manager Test

```bash
python src/MP3Manager.py
```

### Start SimConnect Bridge

Create a test script:

```python
from src.AudioController import AudioController
from src.SimConnectBridge import SimConnectBridge

controller = AudioController()
bridge = SimConnectBridge(controller)

# Test playback
controller.play()
controller.set_volume(0.7)
print(controller.get_status())
```

## Troubleshooting

### MP3 Folder Not Found
- Verify the path in `config.json` uses proper escaping: `C:\\\\Music\\\\MSFS_Audio`
- Ensure the folder exists before running

### SimConnect Connection Failed
- Install SimConnect SDK properly
- Check that MSFS 2020 is running when connecting
- Verify SimConnect.cfg exists in the config directory

### No Audio Playing
- Check that pygame mixer initialized successfully
- Verify MP3 files are valid and not corrupted
- Check Windows volume settings
- Review logs in `logs/audio_controller.log`

### Variable Updates Not Working
- Ensure aircraft model includes the audio_device.xml
- Verify SimConnect variables are properly defined
- Check aircraft.cfg for any conflicts

## Advanced Configuration

### Custom Volume Step

Edit `config/config.json`:

```json
"volume_step": 0.10
```

### Enable Debug Mode

```json
"debug_mode": true,
"log_file": "logs/audio_controller.log"
```

### Add More Audio Formats

```json
"supported_formats": ["mp3", "wav", "flac", "ogg", "m4a"]
```

## Integration with Existing Panels

If you have an existing glass cockpit panel:

1. Add new controls to your panel XML using the AUDIO_* SimVars
2. Create event handlers for button clicks
3. Link to the audio system using the provided events

Example:

```xml
<Control Type="Button" Name="PLAY_BUTTON">
    <OnClick Action="AUDIO_PLAY_PRESSED"/>
</Control>
```

## Next Steps

- See [XML Configuration Guide](XML_CONFIGURATION.md)
- Review [SimConnect Reference](SIMCONNECT_REFERENCE.md)
- Check example files in `examples/`
