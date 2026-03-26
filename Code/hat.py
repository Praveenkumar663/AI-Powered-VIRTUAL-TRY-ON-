import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Load hat image
hat = cv2.imread('../Resources/1png/1hat/pngfind.com-dad-hat-png-1429641.png', cv2.IMREAD_UNCHANGED)

def overlay_hat(frame, landmarks, scale_factor=2.5):
    # Extract relevant landmarks for hat placement
    top_of_head = landmarks[0]  # Adjust the landmark index based on your preference

    # Calculate hat position and size
    hat_width = int(np.linalg.norm(np.array(landmarks[0]) - np.array(landmarks[1])) * scale_factor)
    hat_height = int(hat_width * (hat.shape[0] / hat.shape[1]))

    # Resize hat image
    hat_resized = cv2.resize(hat, (hat_width, hat_height))

    # Calculate position for overlay
    #x_offset = top_of_head[0] - int(hat_width / 2)
    #y_offset = top_of_head[1] - hat_height
    print(hat_height)

    x_offset = top_of_head[0] - int(hat_width/3)
    y_offset = top_of_head[1]- hat_height

    # Overlay hat on the frame
    for c in range(0, 3):
        frame[y_offset:y_offset + hat_resized.shape[0], x_offset:x_offset + hat_resized.shape[1], c] = (
            frame[y_offset:y_offset + hat_resized.shape[0], x_offset:x_offset + hat_resized.shape[1], c] *
            (1 - hat_resized[:, :, 3] / 255.0) +
            hat_resized[:, :, c] * (hat_resized[:, :, 3] / 255.0)
        )

    return frame

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform face detection
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

            # Draw bounding box around face
            #mp_drawing.draw_detection(frame, detection)

            # Extract face landmarks
            landmarks = [(int(l.x * iw), int(l.y * ih)) for l in detection.location_data.relative_keypoints]

            # Overlay hat on the face
            try:
                frame = overlay_hat(frame, landmarks)
            except:
                pass


    cv2.imshow('Virtual Hat', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
