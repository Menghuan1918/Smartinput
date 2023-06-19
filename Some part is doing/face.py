import cv2
import face_recognition

video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 指定每隔多少帧进行一次人脸检测
frame_skip = 5
frame_count = 0

while True:
    ret, frame = video_capture.read()
    frame_count += 1
    if frame_count % frame_skip == 0:
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
    # 假设只有一个人脸
        if len(face_locations) == 1:
            (top, right, bottom, left) = face_locations[0]

        # 计算人脸中心点
            face_center = ((right + left) // 2, (bottom + top) // 2)

        # 计算图像中心点
            img_center = (frame.shape[1] // 2, frame.shape[0] // 2)

        # 计算人脸中心点与图像中心点的偏差
            offset_x = face_center[0] - img_center[0]
            offset_y = face_center[1] - img_center[1]

        # 你可以设定一个阈值来决定何时认为人脸在中央
            if abs(offset_x) < 100 and abs(offset_y) < 100:
                print("Face is in the center")
            else:
                print("Face is not in the center")

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
