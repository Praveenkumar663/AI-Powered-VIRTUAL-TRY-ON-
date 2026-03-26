import cv2
import mediapipe as mp
import os
import cvzone
# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
imageNumber = 0

shirtRatioHeightWidth = 1.5
# Open a webcam feed
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

        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        # Get the left and right shoulder landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        #print(left_shoulder)
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        #imgShirt = cv2.resize(imgShirt, (0, 0), None, 0.7, 0.7)

        if left_shoulder and right_shoulder:

            left_shoulder_x, left_shoulder_y = int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])
            right_shoulder_x, right_shoulder_y = int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])

            # Draw circles at the shoulder points
            cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 5, (0, 255, 0), -1)

            widthOfShirt = int((left_shoulder_x - right_shoulder_x)*1.3)
            #widthOfShirt = int((lm11[0] - lm12[0]))
            print(widthOfShirt)

            currentScale = (left_shoulder_x -right_shoulder_x) / 190
            offset = int(44 * currentScale), int(48 * currentScale)
            try:
                imgShirt = cv2.resize(imgShirt, (widthOfShirt+1, int(widthOfShirt * 1.3)))

                #frame = cvzone.overlayPNG(frame, imgShirt, (right_shoulder_x-30, right_shoulder_y-20))

                frame = cvzone.overlayPNG(frame, imgShirt, (right_shoulder_x - offset[0],  right_shoulder_y - offset[1]))
            except:
                pass


    # Display the frame with pose landmarks
    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()