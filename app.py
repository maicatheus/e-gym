import cv2
import mediapipe as mp
import math
import time

def exercicioFlexao(body):
    global baixoCount, flexCount, cimaFlag
    nariz = body[0][1]

    if(nariz < linhaHorizonte and not cimaFlag):
        cimaFlag = True
        flexCount += 1

    elif(nariz > linhaHorizonte and cimaFlag):
        cimaFlag = False

def exercicioAbdominal(body):
    try:
        cintura = body[24]
        theta = 30
        y2 = 0
        x1,y1 = cintura[0], cintura[1]
        x2 = ((y1 - y2)* math.cos(theta) + x1 * math.sin(theta))/math.sin(theta)
        nariz = body[0]
        a = (y1 - y2)
        b = (x2 - x1)
        c = (x1*y2 - y1*x2)
        
        d = (abs(a*nariz[0] + b*nariz[1] + c))/math.sqrt(a**2 + b**2)
        print(f"distancia nariz reta: {d}")
        if(d <=0 and abdmFlag):
            abdmFlag = False
            abdmCount += 1
        
        if(d > 50 and not abdmFlag):
            abdmFlag = True
            
        return(int(x2),y2)
    except:
        return (0,0)

def tipoExercicio(body):
    mao = body[16][1]
    cintura = body[24][1]
    if(mao > cintura):
        return "flexao"
    if(mao < cintura):
        return "Abdominal"
    
    return "desconhecido"

camera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
scale = 3
pTime = 0
color = (255,0,0)
thickness = 3

linhaHorizonte = 235

cimaFlag = True
abdmFlag = True
flexCount = 0
abdmCount = 0

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

        tipo = tipoExercicio(body)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        if(tipo == "flexao"):
            exercicioFlexao(body)
            cv2.line(frame, (0,linhaHorizonte), (700,linhaHorizonte), color, 1)
            cv2.putText(frame,str(f"Flex count: {int(flexCount)}"),(0,140),font,scale,color,thickness)

        if(tipo == "Abdominal"):
            retaAbdominal = exercicioAbdominal(body)
            cv2.line(frame, body[24],retaAbdominal , color, 3)
            cv2.putText(frame,str(f"abdom. count: {int(abdmCount)}"),(0,140),font,scale,color,thickness)


        cv2.putText(frame,str(f"FPS: {int(fps)}"),(0,40),font,scale,color,thickness)
        cv2.putText(frame,str(f"exercicio: {tipo}"),(0,100),font,scale,color,thickness)



        cv2.imshow("e-gym", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        print("Algum problema!")

camera.release()
cv2.destroyAllWindows()