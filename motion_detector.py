def draw_pose(frame, results, mp_pose, mp_drawing):
    """Draw stick figure landmarks on the frame."""
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=3),
        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2)
    )

def get_landmarks(results, handedness, mp_pose):
    """Return key landmarks depending on handedness."""
    landmarks = results.pose_landmarks.landmark
    wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP] if handedness == 'R' else landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
    right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
    return wrist, shoulder, hip, left_foot, right_foot

def is_body_visible(wrist, shoulder, hip, left_foot, right_foot, threshold=0.5):
    """Check if all key landmarks are sufficiently visible."""
    return all(l.visibility > threshold for l in [wrist, shoulder, hip, left_foot, right_foot])
