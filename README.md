# chord-visualizer-v1

## Timeline
- 1/16/2026: Started project, implemented basic hand detection functionality (hand detection, displaying hand landmarks)

## Setup info
macOS users:
pyo requires libFLAC. If you see an ImportError about libFLAC.12.dylib:
1. Make sure Homebrew is installed.
2. Install FLAC: `brew install flac`
3. Create symlink so pyo can find it:
   `ln -s /opt/homebrew/opt/flac/lib/libFLAC.14.dylib /opt/homebrew/opt/flac/lib/libFLAC.12.dylib`
