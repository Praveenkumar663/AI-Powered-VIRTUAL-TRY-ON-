'''import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Webcam setup
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame
    results = hands.process(rgb_frame)

    # Detect faces in the frame
    results_face = face_detection.process(rgb_frame)

    # Check if hands and faces are detected
    if results.multi_hand_landmarks and results_face.detections:
        for landmarks in results.multi_hand_landmarks:
            # Get the landmarks for the fingers
            thumb_tip = landmarks.landmark[4]
            index_tip = landmarks.landmark[8]
            middle_tip = landmarks.landmark[12]
            ring_tip = landmarks.landmark[16]
            pinky_tip = landmarks.landmark[20]

            # Get the position of the face
            face_location = results_face.detections[0].location_data.relative_bounding_box

            # Check if any finger is near the mouth region
            if (
                thumb_tip.y > face_location.ymin and
                index_tip.y > face_location.ymin and
                middle_tip.y > face_location.ymin and
                ring_tip.y > face_location.ymin and
                pinky_tip.y > face_location.ymin
            ):
                cv2.putText(
                    frame,
                    "Nail Biting Detected",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

    cv2.imshow("Nail Biting Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
'''



import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands in the frame
    results_hands = hands.process(rgb_frame)

    # Detect faces in the frame
    results_face_detection = face_detection.process(rgb_frame)

    # Detect face mesh landmarks
    results_face_mesh = face_mesh.process(rgb_frame)

    # Render face mesh landmarks
    if results_face_mesh.multi_face_landmarks:
        for face_landmarks in results_face_mesh.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1),
            )

    # Check if hands and faces are detected
    if results_hands.multi_hand_landmarks and results_face_detection.detections:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # Get the landmarks for the fingers
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            ring_tip = hand_landmarks.landmark[16]
            pinky_tip = hand_landmarks.landmark[20]

            # Get the position of the face
            face_location = results_face_detection.detections[0].location_data.relative_bounding_box

            # Check if any finger is near the mouth region
            if (
                thumb_tip.y * frame.shape[0] > face_location.ymin * frame.shape[0]
                #and index_tip.y * frame.shape[0] > face_location.ymin * frame.shape[0]
            ):
                cv2.putText(
                    frame,
                    "Nail Biting Detected",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

    cv2.imshow("Nail Biting Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
