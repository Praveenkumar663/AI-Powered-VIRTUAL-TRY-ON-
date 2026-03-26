import mediapipe as mp
import cv2
import numpy as np

# Create a MediaPipe Hands object
hands = mp.solutions.hands.Hands()

# Read the input video
cap = cv2.VideoCapture(0)

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()

    # Convert the frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run MediaPipe Hands on the image
    results = hands.process(image)

    # Get the finger landmarks if hands are detected
    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmarks of the hand
            finger_landmarks = hand_landmarks.landmark
            print(len(finger_landmarks))
            # Check if there are enough landmarks detected
            if len(finger_landmarks) >= 20:
                mouth_center = ((finger_landmarks[19].x + finger_landmarks[20].x) / 2,
                                (finger_landmarks[19].y + finger_landmarks[20].y) / 2)
                for finger in finger_landmarks:
                    finger_point = (finger.x, finger.y)
                    #print(cv2.norm(np.array(finger_point) - np.array(mouth_center)))
                    if cv2.norm(np.array(finger_point) - np.array(mouth_center)) < 0.02:
                        #print("Finger is near the mouth region!")
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

    # Display the frame
    cv2.imshow("Frame", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()

# Close all windows
cv2.destroyAllWindows()
