import cv2
import mediapipe as mp
from playsound import playsound

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

# State machine: was the hand up?
hand_was_up = False

# Create window and set fullscreen
cv2.namedWindow("Stick Figure Pose + Hit Detection", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Stick Figure Pose + Hit Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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

        # Convert normalized y positions to pixel space
        h, w, _ = frame.shape
        wrist_y = wrist.y * h
        shoulder_y = shoulder.y * h
        hip_y = hip.y * h
        threshold_y = (shoulder_y + hip_y) / 2  # Midpoint between shoulder and hip, used

        # Check if hand is above threshold level
        if wrist_y < threshold_y:
            hand_was_up = True

        # If hand was up and now goes below threshold level
        if hand_was_up and wrist_y > threshold_y:
            cv2.putText(frame, "Hit detected!", (100, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
            # playsound("sound\\hit_shuttle.mp3")  # Play sound on hit
            hand_was_up = False  # reset state

    # Show the frame with stick figure overlay
    cv2.imshow("Stick Figure Pose + Hit Detection", frame)

    # Press 'q' to exit fullscreen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
