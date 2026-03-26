import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Load sunglass image
sunglass = cv2.imread('../Resources/1png/1GLASS/2-2-sunglasses-picture.png', cv2.IMREAD_UNCHANGED)

'''def overlay_sunglass(frame, landmarks):
    # Extract relevant landmarks for sunglass placement
    left_eye = landmarks[0]
    right_eye = landmarks[1]

    # Calculate sunglasses position and size
    glasses_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * 1.5)
    glasses_height = int(glasses_width * (sunglass.shape[0] / sunglass.shape[1]))

    # Resize sunglasses image
    glasses_resized = cv2.resize(sunglass, (glasses_width, glasses_height))

    # Calculate position for overlay
    x_offset = left_eye[0] - int(glasses_width / 4)
    y_offset = left_eye[1] - int(glasses_height / 4)

    # Overlay sunglasses on the frame
    for c in range(0, 3):
        frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] = (
            frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] *
            (1 - glasses_resized[:, :, 3] / 255.0) +
            glasses_resized[:, :, c] * (glasses_resized[:, :, 3] / 255.0)
        )

    return frame'''
def overlay_sunglass(frame, landmarks, scale_factor=1.5):
    # Extract relevant landmarks for sunglass placement
    left_eye = landmarks[0]
    right_eye = landmarks[1]

    # Calculate sunglasses position and size
    glasses_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * scale_factor)
    glasses_height = int(glasses_width * (sunglass.shape[0] / sunglass.shape[1]))



    # Resize sunglasses image
    glasses_resized = cv2.resize(sunglass, (glasses_width+50, glasses_height+25))

    # Calculate position for overlay
    #x_offset = left_eye[0] - int(glasses_width / 6)
    #y_offset = left_eye[1] - int(glasses_height / 2)

    x_offset = left_eye[0]-40
    y_offset = left_eye[1] - int(glasses_height / 2)

    print(x_offset)
    print(y_offset)

    # Overlay sunglasses on the frame
    for c in range(0, 3):
        frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] = (
            frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] *
            (1 - glasses_resized[:, :, 3] / 255.0) +
            glasses_resized[:, :, c] * (glasses_resized[:, :, 3] / 255.0)
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
            #landmarks = [(int(l.x * iw), int(l.y * ih)) for l in mp_face_detection.get_key_points_for_visualization(detection).landmark]
            landmarks = [(int(l.x * iw), int(l.y * ih)) for l in detection.location_data.relative_keypoints]

            # Overlay sunglasses on the face
            try:
                frame = overlay_sunglass(frame, landmarks)
            except:
                pass


    cv2.imshow('Virtual Sunglass', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
