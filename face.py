import cv2
import face_recognition

# 启用GPU加速
#cv2.cuda.setDevice(0)
#face_recognition.api.cuda_enabled = True

# 初始化摄像头
video_capture = cv2.VideoCapture(0)
#video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)q
#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 循环获取摄像头图像
while True:
    # 读取摄像头图像
    ret, frame = video_capture.read()
    # 将图像转换为RGB格式
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.imshow('Video', frame)
    # 按下Q键退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放摄像头资源
video_capture.release()
cv2.destroyAllWindows()
