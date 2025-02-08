import cv2
import mediapipe as mp

# ser = serial.Serial('/dev/cu.usbmodem11201', 9600)  # Replace 'COM3' with your Arduino's serial port


# Initialize Mediapipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize two video captures: 0 for default (FaceTime), 1 for USB webcam
cap1 = cv2.VideoCapture(0)  # First camera (FaceTime or built-in)
cap2 = cv2.VideoCapture(1)  # Second camera (USB webcam)

# Check if both cameras opened successfully
if not cap1.isOpened() or not cap2.isOpened():
    print("Error: Could not open both cameras.")
    cap1.release()
    cap2.release()
    exit()

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("Error: Failed to capture frame from one of the cameras.")
        break

    # Process both frames for pose detection
    rgb_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    rgb_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    results1 = pose.process(rgb_frame1)
    results2 = pose.process(rgb_frame2)

    # Draw landmarks on both frames
    if results1.pose_landmarks:
        mp_drawing.draw_landmarks(frame1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if results2.pose_landmarks:
        mp_drawing.draw_landmarks(frame2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display both frames in separate windows
    cv2.imshow('Camera 1 - Player 1', frame1)
    cv2.imshow('Camera 2 - Player 2', frame2)

    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release both cameras
cap1.release()
cap2.release()
cv2.destroyAllWindows()
