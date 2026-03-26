import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

# Load sunglass image
sunglass = cv2.imread('../Resources/1png/1jewel/Jewellery Design 2022 PNG Image Free Download (41).png', cv2.IMREAD_UNCHANGED)

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
    print(left_eye)

    # Calculate sunglasses position and size
    glasses_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * scale_factor)
    glasses_height = int(glasses_width * (sunglass.shape[0] / sunglass.shape[1]))



    # Resize sunglasses image
    glasses_resized = cv2.resize(sunglass, (glasses_width+50, glasses_height+25))

    # Calculate position for overlay
    #x_offset = left_eye[0] - int(glasses_width / 6)
    #y_offset = left_eye[1] - int(glasses_height / 2)

    x_offset = left_eye[0]-40
    y_offset = left_eye[1]+130

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


'''import cv2
import mediapipe as mp
import os
import cvzone
# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

shirtFolderPath = "Resources/1png/1jewel"
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

            widthOfShirt = int((left_shoulder_x - right_shoulder_x))
            #widthOfShirt = int((lm11[0] - lm12[0]))
            print(widthOfShirt)

            currentScale = (left_shoulder_x -right_shoulder_x) / 190
            offset = int(44 * currentScale), int(48 * currentScale)
            try:
                imgShirt = cv2.resize(imgShirt, (widthOfShirt+1, int(widthOfShirt)))

                #frame = cvzone.overlayPNG(frame, imgShirt, (right_shoulder_x-30, right_shoulder_y-20))

                frame = cvzone.overlayPNG(frame, imgShirt, (right_shoulder_x ,  right_shoulder_y))
            except:
                pass


    # Display the frame with pose landmarks
    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()'''

'''import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
# print(listShirts)
fixedRatio = 262 / 190  # widthOfShirt/widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        # center = bboxInfo["center"]
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        print(widthOfShirt)

        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)

        try:
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        elif lmList[15][1] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)'''