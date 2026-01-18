# Chord Visualizer v1

A real-time hand gesture-controlled musical instrument that uses computer vision to detect finger positions and synthesizes corresponding musical chords.

## Features

- **Real-time hand tracking**: Uses MediaPipe for accurate hand landmark detection
- **Gesture-to-chord mapping**: Maps finger bend angles to musical notes
- **Audio synthesis**: Chord sounds created using pyo
- **Visual feedback**: Displays hand landmarks and skeleton in real-time
- **Multi-hand support**: supports chords played with both hands

## How It Works

The system tracks hand landmarks and calculates the bend angles of fingers (index and middle on both hands). These angles are mapped to musical notes using a chromatic scale, creating 4-note chords that are synthesized in real-time.

### Gesture Mapping
- **Left Hand Index Finger**: Maps to first chord note
- **Left Hand Middle Finger**: Maps to second chord note based on upward pitch difference from first chord note
- **Right Hand Index Finger**: Maps to third chord note based on upward
pitch difference from second chord note
- **Right Hand Middle Finger**: Maps to fourth chord note based on upward pitch difference from third chord note

Finger bend angles (45°-150°) are divided into 8 note bins spanning a musical scale.

## Requirements

- Python 3.10
- Webcam
- macOS (currently optimized for macOS with CoreAudio)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd chord-visualizer-v1
```

### 2. Create conda environment
```bash
conda env create -f environment.yml
conda activate chord-visualizer-py310
```

### 3. macOS Setup
pyo requires libFLAC. If you see an ImportError about libFLAC.12.dylib:
1. Make sure Homebrew is installed.
2. Install FLAC: `brew install flac`
3. Create symlink so pyo can find it:
   `ln -s /opt/homebrew/opt/flac/lib/libFLAC.14.dylib /opt/homebrew/opt/flac/lib/libFLAC.12.dylib`

## Usage

1. Ensure your webcam is connected and accessible
2. Activate the conda environment:
   ```bash
   conda activate chord-visualizer-py310
   ```
3. Run the main application:
   ```bash
   python src/main.py
   ```
4. Position your hands in front of the camera
5. Bend your fingers to different angles to create different chords
6. Press 'q' to quit

## Project Structure

```
chord-visualizer-v1/
├── environment.yml          # Conda environment specification
├── models/
│   └── hand_landmarker.task # MediaPipe hand tracking model
├── src/
│   ├── audio_engine.py      # Audio synthesis engine using pyo
│   ├── config.py           # Configuration constants
│   ├── cv_utils.py         # Computer vision utilities for hand tracking
│   ├── hand_info.py        # Hand landmark definitions and connections
│   ├── main.py             # Main application entry point
│   └── notes.py            # Note mapping and frequency calculations
└── README.md
```

## Key Components

### Hand Tracking (`cv_utils.py`)
- `draw_landmarks()`: Visualizes detected hand landmarks
- `draw_hand_skeleton()`: Draws connections between hand joints
- `get_angle()`: Calculates 3D angles between hand landmarks

### Audio Engine (`audio_engine.py`)
- Synthesizes chords using triangle wave oscillators
- Applies effects: low-pass filtering, distortion, chorus, reverb

### Note Mapping (`notes.py`)
- Maps finger angles to musical notes
- Calculates frequencies using 12-tone equal temperament
- Generates chord frequencies from note indices

## Dependencies

- **mediapipe**: Hand tracking and landmark detection
- **opencv-python**: Computer vision and image processing
- **pyo**: Real-time audio synthesis
- **numpy**: Numerical computations
- **sounddevice**: Audio output (used by pyo)

## Timeline
- 1/16/2026: Started project, implemented basic hand detection functionality (hand detection, displaying hand landmarks)
- 1/17/2026: Implemented audio synthesis engine with pyo, note mapping system, and gesture recognition. Added real-time chord synthesis and multi-hand support

## Future improvements

- More precise gesture recognition (finger extension detection vs. angle measurement vs. relative position)
- Chord shape recognition for common musical chords
- Support for additional effects and parameters
- Chord visualization perhaps using Lissajous curves
