# XML Configuration Guide

## Overview

The MSFS 2020 Audio Controller uses XML files to define:
- Audio device parameters
- SimConnect variables
- Cockpit controls and events
- Display elements

## Audio Device Definition

### File: `audio_device.xml`

Defines the audio device component and its SimConnect variables.

```xml
<Component ID="AUDIO_DEVICE" Enabled="True">
    <Parameter Name="FolderPath" Value="C:\Music\MSFS_Audio"/>
    <Parameter Name="MaxVolume" Value="1.0"/>
    <Parameter Name="VolumeStep" Value="0.05"/>
</Component>
```

## SimConnect Variables

### Variable: AUDIO_VOLUME
- **Type**: FLOAT32
- **Range**: 0.0 - 1.0
- **Unit**: percentage
- **Purpose**: Master volume control
- **Example**: 0.5 = 50% volume

### Variable: AUDIO_PLAY
- **Type**: BOOL
- **Range**: 0 or 1
- **Purpose**: Trigger playback
- **Usage**: Set to 1 to start playing

### Variable: AUDIO_STOP
- **Type**: BOOL
- **Range**: 0 or 1
- **Purpose**: Stop playback
- **Usage**: Set to 1 to stop playing

### Variable: AUDIO_NEXT
- **Type**: BOOL
- **Range**: 0 or 1
- **Purpose**: Play next track
- **Usage**: Set to 1 to advance to next track

### Variable: AUDIO_PREVIOUS
- **Type**: BOOL
- **Range**: 0 or 1
- **Purpose**: Play previous track
- **Usage**: Set to 1 to go to previous track

### Variable: AUDIO_CURRENT_TRACK
- **Type**: STRING32
- **Purpose**: Display currently playing track filename
- **Read-Only**: Yes

### Variable: AUDIO_TRACK_COUNT
- **Type**: INT32
- **Purpose**: Total number of tracks in folder
- **Read-Only**: Yes

### Variable: AUDIO_IS_PLAYING
- **Type**: BOOL
- **Purpose**: Indicates playback status
- **Read-Only**: Yes

### Variable: AUDIO_TRACK_INDEX
- **Type**: INT32
- **Purpose**: Current track index (0-based)
- **Read-Only**: Yes

## Model Integration

### File: `model_integration.xml`

Integrates audio system into aircraft model.

#### Including in model.xml

```xml
<Include Path="audio_device.xml"/>
```

#### Cockpit Events

Define button click events:

```xml
<Event Name="AUDIO_PLAY_PRESSED">
    <Action Type="SimVar">
        <Var Name="AUDIO_PLAY" Value="1"/>
    </Action>
    <ResetVar Name="AUDIO_PLAY" Delay="500ms"/>
</Event>
```

#### Displays

Create text and gauge displays:

```xml
<Display Name="AUDIO_STATUS" Type="Text">
    <Content>
        <Line 1>Track: $(AUDIO_CURRENT_TRACK)</Line>
        <Line 2>Volume: $(AUDIO_VOLUME*100)%</Line>
    </Content>
</Display>
```

## Control Types

### Button
```xml
<Control Type="Button" Name="PLAY_BTN">
    <Param Name="Label" Value="▶ PLAY"/>
    <Param Name="OnClick" Value="AUDIO_PLAY_PRESSED"/>
</Control>
```

### Knob
```xml
<Control Type="Knob" Name="VOLUME_KNOB">
    <Param Name="Variable" Value="AUDIO_VOLUME"/>
    <Param Name="MinValue" Value="0.0"/>
    <Param Name="MaxValue" Value="1.0"/>
    <Param Name="Step" Value="0.05"/>
</Control>
```

### LED Indicator
```xml
<Display Type="LED" Name="PLAYING_INDICATOR">
    <Param Name="Variable" Value="AUDIO_IS_PLAYING"/>
    <Param Name="OnColor" Value="0x00FF00"/>
    <Param Name="OffColor" Value="0x333333"/>
</Display>
```

### Text Display
```xml
<Display Type="TextBox" Name="TRACK_DISPLAY">
    <Param Name="Content" Value="$(AUDIO_CURRENT_TRACK)"/>
    <Param Name="ReadOnly" Value="True"/>
</Display>
```

## Variable String Formatting

### Display Track Information
```xml
<Content>$(AUDIO_TRACK_INDEX+1) / $(AUDIO_TRACK_COUNT)</Content>
```
Output: "3 / 10"

### Display Volume as Percentage
```xml
<Content>$(AUDIO_VOLUME*100)%</Content>
```
Output: "75%"

### Conditional Display
```xml
<Content>$(AUDIO_IS_PLAYING ? 'Playing' : 'Stopped')</Content>
```

## Animation Example

Create volume knob rotation based on volume level:

```xml
<Animation Name="VOLUME_KNOB_ANIMATION">
    <Params ID="0">
        <Param Name="Volume" Value="AUDIO_VOLUME" Min="0" Max="1" Type="Rotation"/>
    </Params>
    <Keyframe Time="0" Value="0"/>
    <Keyframe Time="1" Value="270"/>
</Animation>
```

## Tips and Best Practices

1. **Always reset toggle variables** after use:
   ```xml
   <ResetVar Name="AUDIO_PLAY" Delay="500ms"/>
   ```

2. **Use proper string escaping** in paths:
   ```xml
   <Parameter Name="FolderPath" Value="C:\\Music\\MSFS_Audio"/>
   ```

3. **Group related variables** in displays:
   ```xml
   <Display Name="AUDIO_INFO">
       <Line 1>$(AUDIO_CURRENT_TRACK)</Line>
       <Line 2>$(AUDIO_TRACK_INDEX+1)/$(AUDIO_TRACK_COUNT)</Line>
       <Line 3>Vol: $(AUDIO_VOLUME*100)%</Line>
   </Display>
   ```

4. **Use meaningful control names** for debugging

5. **Test incrementally** - add one section at a time

## Common Mistakes

- ❌ Forgetting to reset toggle variables
- ❌ Using wrong variable types (INT32 vs FLOAT32)
- ❌ Path escaping errors
- ❌ Circular includes
- ❌ Missing parameter values

## Validation

Test your XML:
1. Validate XML syntax in an XML editor
2. Check that all referenced variables exist
3. Ensure folder paths are correct
4. Test each control individually in MSFS
