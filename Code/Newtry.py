import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Load T-shirt image
tshirt_image = cv2.imread("path/to/tshirt/image.png", cv2.IMREAD_UNCHANGED)

# Function to overlay T-shirt on the detected body
def overlay_tshirt(frame, landmarks, tshirt_image):
    # Extract relevant landmarks for the upper body
    upper_body_landmarks = np.array([landmarks[i] for i in range(11, 32)])

    # Convert landmarks to integer coordinates
    upper_body_landmarks_int = np.round(upper_body_landmarks * np.array(frame.shape[1::-1])).astype(int)
    upper_body_landmarks_int = upper_body_landmarks_int.reshape((-1, 2))

    # Find the bounding box around the upper body
    x, y, w, h = cv2.boundingRect(upper_body_landmarks_int)
    h += 50  # Adjust height for better appearance

    # Resize T-shirt image to match the bounding box dimensions
    tshirt_resized = cv2.resize(tshirt_image, (w, h))

    # Overlay T-shirt on the frame
    frame[y:y+h, x:x+w, :] = (
        tshirt_resized[:, :, 3:] * (tshirt_resized[:, :, :3] / 255.0)
        + frame[y:y+h, x:x+w, :] * (1.0 - tshirt_resized[:, :, 3:] / 255.0)
    )


# Start capturing video from the camera
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Pose model
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Overlay T-shirt on the detected body
            overlay_tshirt(frame, results.pose_landmarks.landmark, tshirt_image)

        # Display the resulting frame
        cv2.imshow('Virtual Try-On', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
