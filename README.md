# Hand Gesture Volume Control with OpenCV and MediaPipe

This project demonstrates how to control the volume of your system using hand gestures captured by a webcam. The system uses OpenCV for image processing and MediaPipe for hand tracking. The volume is adjusted by detecting the distance between the thumb and index finger.

## Features

- **Real-time hand tracking** using MediaPipe.
- **Volume control** based on the distance between the thumb and index finger.
- **Display** the volume percentage on the screen.
- **Works with any webcam** to detect hand gestures.
- Uses the `pycaw` library to interact with system volume.

## Requirements

To run this project, you need to install the following libraries:

- `opencv-python`
- `mediapipe`
- `pycaw`
- `math`
- `comtypes`

You can install the required libraries using pip:

```bash
pip install opencv-python mediapipe pycaw comtypes
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/hand-gesture-volume-control.git
```

2. Navigate to the project folder:

```bash
cd hand-gesture-volume-control
```

3. Run the main Python script:

```bash
python main.py
```

4. Point your hand towards the webcam. The system will detect your hand and adjust the volume based on the distance between your thumb and index finger.

   - **Close distance (thumb and index finger together)**: Low volume.
   - **Wide distance (thumb and index finger apart)**: High volume.

5. Press **'q'** to exit the program.

## Code Explanation

### 1. HandTracker Class
- Initializes MediaPipe's hand tracking with customizable detection and tracking confidence.
- `detect_hands`: Detects hands and draws landmarks.
- `get_landmark_positions`: Returns the positions of key landmarks on the hand.

### 2. Main Function
- Captures video frames using OpenCV.
- Processes frames to detect hand landmarks.
- Calculates the distance between the thumb and index finger.
- Adjusts system volume using `pycaw` based on the distance.

### 3. Hand Gesture Volume Control
- The thumb and index finger tips' distance controls the volume.
- The volume range is mapped between the system's minimum and maximum volume.

### 4. FPS Display
- The frames per second (FPS) is displayed on the screen for performance tracking.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
