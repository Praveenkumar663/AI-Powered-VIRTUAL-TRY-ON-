from flask import Flask, render_template, flash, request, session, redirect
import mysql.connector

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def DoctorLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/NewProduct")
def NewProduct():
    return render_template('NewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    userdata = cur.fetchall()
    cur.execute("select * from protb")
    productdata = cur.fetchall()
    cur.execute("select * from booktb")
    bookingdata = cur.fetchall()
    data = {"userdata": userdata, "productdata": productdata, "bookingdata": bookingdata}
    return render_template('AdminHome.html', data=data)


@app.route("/AProductInfo")
def AProductInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb   ")
    data = cur.fetchall()
    return render_template('AProductInfo.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            return redirect("/AdminHome")

            # conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            # cur = conn.cursor()
            # cur.execute("SELECT * FROM regtb ")
            # userdata = cur.fetchall()
            # cur.execute("select * from protb")
            # productdata = cur.fetchall()
            # cur.execute("select * from booktb")
            # bookingdata = cur.fetchall()
            # data = {"userdata": userdata, "productdata": productdata, "bookingdata": bookingdata}
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from protb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('AProductInfo.html', data=data)


@app.route("/newproduct", methods=['GET', 'POST'])
def newproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']
        size = request.form['size']

        print("quantity: ", qty)

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  protb VALUES ('','" + pname + "','" + ptype + "','" + size + "','" + price + "','" + qty + "','" + info + "','" + savename + "')")
        conn.commit()
        conn.close()

    flash('Product Register successfully')
    return render_template('NewProduct.html')


@app.route("/EProductInfo")
def EProductInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('EProductInfo.html', data=data)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from protb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('EProductInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return redirect("/UserHome")


@app.route("/Search")
def Search():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb")
    data = cur.fetchall()

    return render_template('Search.html', data=data)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('Search.html', data=data)


@app.route("/search1", methods=['GET', 'POST'])
def search1():
    if request.method == 'POST':
        ptype = request.form['ptype']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('index.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)


@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  where id='" + id + "' ")
    data = cur.fetchall()
    print(data)
    return render_template('AddCart.html', data=data)


@app.route("/TryOn")
def TryOn():
    import shutil
    id = request.args.get('id')
    tt = request.args.get('tt')
    session['pid'] = id
    print(tt)

    if tt == "Tshirt":

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + session['pid'] + "'")
        data = cursor.fetchone()

        if data:

            savename = data[7]
            # copy file
            shutil.copyfile("static/upload/" + savename, "Resources/Shirts/Test.png")

        else:
            return 'No Record Found!'

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
                # print(left_shoulder)
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

                # imgShirt = cv2.resize(imgShirt, (0, 0), None, 0.7, 0.7)

                if left_shoulder and right_shoulder:

                    left_shoulder_x, left_shoulder_y = int(left_shoulder.x * frame.shape[1]), int(
                        left_shoulder.y * frame.shape[0])
                    right_shoulder_x, right_shoulder_y = int(right_shoulder.x * frame.shape[1]), int(
                        right_shoulder.y * frame.shape[0])

                    # Draw circles at the shoulder points
                    cv2.circle(frame, (left_shoulder_x, left_shoulder_y), 5, (0, 255, 0), -1)
                    cv2.circle(frame, (right_shoulder_x, right_shoulder_y), 5, (0, 255, 0), -1)

                    widthOfShirt = int((left_shoulder_x - right_shoulder_x) * 1.3)
                    # widthOfShirt = int((lm11[0] - lm12[0]))
                    print(widthOfShirt)

                    currentScale = (left_shoulder_x - right_shoulder_x) / 190
                    offset = int(44 * currentScale), int(48 * currentScale)
                    try:
                        imgShirt = cv2.resize(imgShirt, (widthOfShirt + 1, int(widthOfShirt * 1.3)))

                        # frame = cvzone.overlayPNG(frame, imgShirt, (right_shoulder_x-30, right_shoulder_y-20))

                        frame = cvzone.overlayPNG(frame, imgShirt,
                                                  (right_shoulder_x - offset[0], right_shoulder_y - offset[1]))
                    except:
                        pass

            # Display the frame with pose landmarks
            cv2.imshow('Pose Estimation', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
    elif tt=="Sunglasses":


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + session['pid'] + "'")
        data = cursor.fetchone()

        if data:

            savename = data[7]
            # copy file
            # shutil.copyfile("static/upload/" + savename, "Resources/Shirts/Test.png")

        else:
            return 'No Record Found!'

        import cv2
        import mediapipe as mp
        import numpy as np
        # Initialize Mediapipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.8)

        # Load sunglass image
        sunglass = cv2.imread('static/upload/' + savename, cv2.IMREAD_UNCHANGED)

        def overlay_sunglass(frame, landmarks, scale_factor=1.5):
            # Extract relevant landmarks for sunglass placement
            left_eye = landmarks[0]
            right_eye = landmarks[1]

            # Calculate sunglasses position and size
            glasses_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * scale_factor)
            glasses_height = int(glasses_width * (sunglass.shape[0] / sunglass.shape[1]))

            # Resize sunglasses image
            glasses_resized = cv2.resize(sunglass, (glasses_width + 50, glasses_height + 25))

            # Calculate position for overlay
            # x_offset = left_eye[0] - int(glasses_width / 6)
            # y_offset = left_eye[1] - int(glasses_height / 2)

            x_offset = left_eye[0] - 40
            y_offset = left_eye[1] - int(glasses_height / 2)

            print(x_offset)
            print(y_offset)

            # Overlay sunglasses on the frame
            for c in range(0, 3):
                frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] = (
                        frame[y_offset:y_offset + glasses_resized.shape[0],
                        x_offset:x_offset + glasses_resized.shape[1], c] *
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
                    # mp_drawing.draw_detection(frame, detection)

                    # Extract face landmarks

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

    elif tt=="Hat":
        import cv2
        import mediapipe as mp
        import numpy as np

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + session['pid'] + "'")
        data = cursor.fetchone()

        if data:

            savename = data[7]
            # copy file
            # shutil.copyfile("static/upload/" + savename, "Resources/Shirts/Test.png")

        else:
            return 'No Record Found!'

        # Initialize Mediapipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

        # Load hat image
        hat = cv2.imread("static/upload/" + savename, cv2.IMREAD_UNCHANGED)

        def overlay_hat(frame, landmarks, scale_factor=2.5):
            # Extract relevant landmarks for hat placement
            top_of_head = landmarks[0]  # Adjust the landmark index based on your preference

            # Calculate hat position and size
            hat_width = int(np.linalg.norm(np.array(landmarks[0]) - np.array(landmarks[1])) * scale_factor)
            hat_height = int(hat_width * (hat.shape[0] / hat.shape[1]))

            # Resize hat image
            hat_resized = cv2.resize(hat, (hat_width, hat_height))

            # Calculate position for overlay
            # x_offset = top_of_head[0] - int(hat_width / 2)
            # y_offset = top_of_head[1] - hat_height
            print(hat_height)

            x_offset = top_of_head[0] - int(hat_width / 3)
            y_offset = top_of_head[1] - hat_height

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
                    # mp_drawing.draw_detection(frame, detection)

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

    else:

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + session['pid'] + "'")
        data = cursor.fetchone()

        if data:
            savename = data[7]

        else:
            return 'No Record Found!'

        import cv2
        import mediapipe as mp
        import numpy as np

        # Initialize Mediapipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

        # Load sunglass image
        sunglass = cv2.imread("static/upload/" + savename,
                              cv2.IMREAD_UNCHANGED)

        def overlay_sunglass(frame, landmarks, scale_factor=1.5):
            # Extract relevant landmarks for sunglass placement
            left_eye = landmarks[0]
            right_eye = landmarks[1]
            print(left_eye)

            # Calculate sunglasses position and size
            glasses_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)) * scale_factor)
            glasses_height = int(glasses_width * (sunglass.shape[0] / sunglass.shape[1]))

            # Resize sunglasses image
            glasses_resized = cv2.resize(sunglass, (glasses_width + 50, glasses_height + 25))

            # Calculate position for overlay
            # x_offset = left_eye[0] - int(glasses_width / 6)
            # y_offset = left_eye[1] - int(glasses_height / 2)

            x_offset = left_eye[0] - 40
            y_offset = left_eye[1] + 130

            print(x_offset)
            print(y_offset)

            # Overlay sunglasses on the frame
            for c in range(0, 3):
                frame[y_offset:y_offset + glasses_resized.shape[0], x_offset:x_offset + glasses_resized.shape[1], c] = (
                        frame[y_offset:y_offset + glasses_resized.shape[0],
                        x_offset:x_offset + glasses_resized.shape[1], c] *
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
                    # mp_drawing.draw_detection(frame, detection)

                    # Extract face landmarks
                    # landmarks = [(int(l.x * iw), int(l.y * ih)) for l in mp_face_detection.get_key_points_for_visualization(detection).landmark]
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

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb")
    data = cur.fetchall()

    return render_template('Search.html', data=data)


@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['uname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[4]
            cQty = data[5]

            Image = data[7]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)

        clqty = int(cQty) - int(qty)

        if clqty == 0:

            flash('Currently Not available ')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        elif clqty < 0:
            flash(f"Only {cQty} is available right now!")

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','0','')")
            conn.commit()
            conn.close()

            flash('Add To Cart  Successfully')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cursor = conn.cursor()
            cursor.execute(
                "update   protb set Qty='" + str(clqty) + "'  where id ='" + pid + "'  ")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)


@app.route("/Cart")
def Cart():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['uname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "update   carttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

    return render_template('UserBook.html', data1=data1, data2=data2)


@app.route("/BookInfo")
def BookInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('UserBook.html', data1=data1, data2=data2)


@app.route("/ABookInfo")
def ABookInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('ABookInfo.html', data1=data1, data2=data2)

@app.route("/ASalesInfo")
def ASalesInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb ")
    data2 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
    cur = conn.cursor()
    cur.execute("SELECT distinct username FROM  booktb ")
    data = cur.fetchall()

    return render_template('ASalesInfo.html', data1=data1, data2=data2, data=data)


@app.route("/asale", methods=['GET', 'POST'])
def asale():
    if request.method == 'POST':
        uname = request.form['username']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cur = conn.cursor()
        cur.execute("SELECT distinct username FROM  booktb ")
        data = cur.fetchall()

        return render_template('ASalesInfo.html', data1=data1, data2=data2, data=data)


@app.route("/Update")
def Update():
    uid = request.args.get('uid')
    session["uid"] = uid

    return render_template('Update.html')


@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        price = request.form['price']
        Qty = request.form['qty']
        date = request.form['date']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1virtualtryondb')
        cursor = conn.cursor()
        cursor.execute(
            "update protb set price='" + price + "',Qty='" + Qty + "',exdate='" + date + "' where id='" + session[
                'uid'] + "' ")
        conn.commit()
        conn.close()

        flash('Product Info Update')

        return render_template('AProductInfo.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
