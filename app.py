import cv2
import mediapipe as mp
import threading
import time

camera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
scale = 3
pTime = 0
color = (255,0,0)
thickness = 3

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
while True:
    try:
        ret, frame = camera.read()
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frameRgb)
        body = []
        if results.pose_landmarks:
            for index, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = frame.shape
                cx , cy = int(lm.x*w), int(lm.y*h)
                body.append((cx,cy))
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)
        cv2.line(frame, (0,235), (700,235), color, 1)

        cv2.imshow("e-gym", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("Algum problema!")

camera.release()
cv2.destroyAllWindows()