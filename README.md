# EchoTranscribe

## Introduction

**EchoTranscribe** is a powerful cross-platform tool designed to extract audio and transcribe text from any video file. Leveraging the capabilities of PyQt for a seamless graphical interface and Whisper for state-of-the-art speech recognition, this software makes it easy to convert video content into text on multiple platforms.

## Features

- **Multi-Platform Support**: Run EchoTranscribe on Windows, macOS, and Linux with ease.
- **Audio Extraction**: Extract high-quality audio from any video file using FFmpeg.
- **Advanced Speech Recognition**: Convert extracted audio to text with Whisper's cutting-edge model.
- **User-Friendly Interface**: Built with PyQt, providing an intuitive and smooth user experience.
- **Real-time Progress**: Monitor the extraction and transcription process in real-time.
- **Text Export**: Easily save transcribed text to a file for further use.

## Installation

### Prerequisites

- **Python 3.8+**
- **FFmpeg** (Ensure FFmpeg is installed and added to your system PATH)
- **PyQt5**
- **Whisper**
- **Other dependencies**: See `requirements.txt`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EchoTranscribe.git
   cd EchoTranscribe
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Open the application.
2. Select a video file from your local storage.
3. Click "Start" to extract the audio and transcribe the text.
4. View the progress and final output directly within the application.
5. Export the transcribed text if needed.

## Contributing

We welcome contributions! If you have ideas or improvements, feel free to fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Whisper** for providing a robust speech recognition model.
- **PyQt** for the flexible and powerful GUI framework.
- **FFmpeg** for the indispensable tool in multimedia processing.

