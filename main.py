import cv2
import mediapipe as mp
import pygame
import time
from move import Move

# Initialize the mixer
pygame.mixer.init()
# TODO: load sounds

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# let user define right or left handed
handedness = input("Enter 'R' for right-handed or 'L' for left-handed: ").strip().upper()
if handedness not in ['R', 'L']:
    print("Invalid input. Please enter 'R' or 'L'.")
    exit()

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Create window (not fullscreen)
cv2.namedWindow("Stick Figure Pose + Hit Detection", cv2.WINDOW_NORMAL)

# Current move to perform
current_move = None
# State machine: was the hand up?
hand_was_up = False
# State machine: waiting for next move after hit
waiting_for_next = False

while True:
    # Capture frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Draw stick figure
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=3),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2)
        )

        # Get landmark coordinates (normalized 0-1)
        landmarks = results.pose_landmarks.landmark
        wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]

        # Convert normalized y positions to pixel space
        h, w, _ = frame.shape
        wrist_y = wrist.y * h
        shoulder_y = shoulder.y * h
        hip_y = hip.y * h
        threshold_y = (shoulder_y + hip_y) / 2  # Midpoint between shoulder and hip, used

        # Start the process when the whole body is visible (wrist, shoulder, hip, and feet)
        if wrist.visibility > 0.5 and shoulder.visibility > 0.5 and hip.visibility > 0.5 \
        and left_foot.visibility > 0.5 and right_foot.visibility > 0.5:

            now = time.time()

            # 1️⃣ Generate a move if none exists AND not in waiting state
            if current_move is None and not waiting_for_next:
                current_move = Move.random_move()
                hand_was_up = False  # reset hit flag
                waiting_for_next = False

            # Always display current move (if any)
            if current_move is not None:
                cv2.putText(frame, str(current_move), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Hit detection
            if current_move is not None:
                if wrist_y < threshold_y:
                    hand_was_up = True

                if hand_was_up and wrist_y > threshold_y:
                    cv2.putText(frame, "Hit detected!", (100, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
                    hand_was_up = False
                    waiting_for_next = True
                    wait_start_time = now  # start the post-hit wait timer

            # 2️⃣ After hit, wait for the move's wait_time before generating the next move
            if waiting_for_next and (now - wait_start_time >= current_move.wait_time):
                current_move = None
                waiting_for_next = False

    # Show the frame with stick figure overlay
    cv2.imshow("Stick Figure Pose + Hit Detection", frame)

    # Press 'q' to exit fullscreen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
