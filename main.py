import cv2
import mediapipe as mp
import time
from move import Move
from helper_func import simplify_instruction
from sound import init_tts, say
from motion_detector import draw_pose, get_landmarks, is_body_visible

# ====== INITIALIZATION ======
sound_engine = init_tts()
sound_engine.startLoop(False)
# TODO: add sounds
# TODO: cancel the compensation of sound engine delay
COMPENSATION_TIME = 1.2
# minimum time between hits to avoid multiple detections
MIN_HIT_INTERVAL = 1

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

handedness = input("Enter 'R' for right-handed or 'L' for left-handed: ").strip().upper()
if handedness not in ['R', 'L']:
    print("Invalid input. Please enter 'R' or 'L'.")
    exit()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cv2.namedWindow("Stick Figure Pose + Hit Detection", cv2.WINDOW_NORMAL)

# ====== STATE VARIABLES ======
hand_was_up = False
waiting_for_next = False
current_move = None
wait_start_time = None
instruction_given = False

# ====== MAIN LOOP ======
while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        draw_pose(frame, results, mp_pose, mp_drawing)
        wrist, shoulder, hip, left_foot, right_foot = get_landmarks(results, handedness, mp_pose)

        h, w, _ = frame.shape
        wrist_y = wrist.y * h
        shoulder_y = shoulder.y * h
        hip_y = hip.y * h
        threshold_y = (shoulder_y + hip_y) / 2
        my_bool = is_body_visible(wrist, shoulder, hip, left_foot, right_foot)
        if my_bool:
            now = time.time()

            # Generate new move if needed
            if current_move is None and not waiting_for_next:
                current_move = Move.random_move()
                hand_was_up = False
                waiting_for_next = False
                instruction_given = False

            if current_move is not None:
                instruction = simplify_instruction(f"{current_move.side} {current_move.zone} {current_move.direction} {current_move.move_type}", handedness)
                # Display current move
                cv2.putText(frame, str(instruction), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if not instruction_given:
                    # Play instruction sound
                    say(sound_engine, instruction)
                    instruction_given = True

                # Hit detection
                # ensure only one detection per move and add a small delay to avoid immediate re-detection
                if not waiting_for_next and (wait_start_time is None or now - wait_start_time > MIN_HIT_INTERVAL):
                    if wrist_y < threshold_y:
                        hand_was_up = True

                    if hand_was_up and wrist_y > threshold_y:
                        cv2.putText(frame, "Hit detected!", (100, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
                        hand_was_up = False
                        waiting_for_next = True
                        wait_start_time = now

                # Wait before next move
                if waiting_for_next and (now - wait_start_time >= current_move.wait_time - COMPENSATION_TIME):
                    current_move = None
                    waiting_for_next = False
                    wait_start_time = None
                    instruction_given = False

        # Body not fully visible
        else:
            cv2.putText(frame, "Ensure full body is visible", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    cv2.imshow("Stick Figure Pose + Hit Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ====== CLEANUP ======
cap.release()
cv2.destroyAllWindows()
sound_engine.endLoop()
