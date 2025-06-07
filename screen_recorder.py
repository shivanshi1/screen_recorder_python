"""
Python Screen Recorder with Screenshot Capability

This script records the screen and saves it as a video file.
It also listens for keyboard events to take screenshots or stop recording:
  - Press 's' to take a screenshot.
  - Press 'q' to stop recording and exit.

Requirements:
- Python 3.7+
- Packages: mss, opencv-python, numpy, keyboard

Usage:
- Run this script in your terminal or VSCode.
- The recorded video is saved in the 'output_video' directory.
- Screenshots are saved in the 'screenshots' directory.
"""

import cv2
import numpy as np
import mss
import os
import time
import keyboard

def main():
    # Create output directories for video and screenshots
    output_video_dir = 'output_video'
    screenshot_dir = 'screenshots'
    os.makedirs(output_video_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Create a unique output video filename
    output_video = os.path.join(output_video_dir, f'output_{int(time.time())}.mp4')

    # Screen capture region (full screen)
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 1 is the primary monitor

        # Get monitor dimensions
        width = monitor['width']
        height = monitor['height']

        # Define video codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MPEG-4
        fps = 20.0
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        print("Screen recording started...")
        print("Press 's' to take a screenshot.")
        print("Press 'q' to stop recording and exit.")

        frame_count = 0

        try:
            while True:
                # Capture screen
                img = sct.grab(monitor)

                # Convert to numpy array
                frame = np.array(img)

                # Convert BGRA to BGR (OpenCV format)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Write frame to video
                out.write(frame)
                frame_count += 1

                # Check for screenshot key press 's'
                if keyboard.is_pressed('s'):
                    screenshot_path = os.path.join(screenshot_dir, f'screenshot_{int(time.time())}.png')
                    cv2.imwrite(screenshot_path, frame)
                    print(f"Screenshot saved: {screenshot_path}")
                    # Wait a bit to avoid multiple screenshots for one press
                    time.sleep(0.5)
                
                # Check for quit key press 'q'
                if keyboard.is_pressed('q'):
                    print("Stopping recording...")
                    break

                # To reduce CPU usage and maintain fps
                time.sleep(1/fps)
        except KeyboardInterrupt:
            print("Recording interrupted by user.")

        # Release resources
        out.release()
        print(f"Recording saved to {output_video}")
        print("Exiting...")

if __name__ == "__main__":
    main()