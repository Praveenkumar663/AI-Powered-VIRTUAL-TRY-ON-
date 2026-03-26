import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open webcam feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get pose landmarks
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get left & right shoulder landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Get left & right hip landmarks
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        if left_shoulder and right_shoulder and left_hip and right_hip:
            # Convert normalized coordinates to image coordinates
            left_shoulder_x, left_shoulder_y = int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])
            right_shoulder_x, right_shoulder_y = int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])

            left_hip_x, left_hip_y = int(left_hip.x * frame.shape[1]), int(left_hip.y * frame.shape[0])
            right_hip_x, right_hip_y = int(right_hip.x * frame.shape[1]), int(right_hip.y * frame.shape[0])

            # Draw circles at shoulder points (Green)
            cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 10, (0, 255, 0), -1)
            cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 10, (0, 255, 0), -1)

            # Draw circles at hip points (Blue)
            cv2.circle(frame, (left_hip_x, left_hip_y), 10, (255, 0, 0), -1)
            cv2.circle(frame, (right_hip_x, right_hip_y), 10, (255, 0, 0), -1)

            # Display coordinates
            cv2.putText(frame, f"LS ({left_shoulder_x}, {left_shoulder_y})", (left_shoulder_x + 10, left_shoulder_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"RS ({right_shoulder_x}, {right_shoulder_y})", (right_shoulder_x + 10, right_shoulder_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.putText(frame, f"LH ({left_hip_x}, {left_hip_y})", (left_hip_x + 10, left_hip_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(frame, f"RH ({right_hip_x}, {right_hip_y})", (right_hip_x + 10, right_hip_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display the frame with detected points
    cv2.imshow('Shoulder and Hip Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
