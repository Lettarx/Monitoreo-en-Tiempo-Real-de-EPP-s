import cv2

cap = cv2.VideoCapture(0) # indice de la camara, en este caso la camara principal(0)

while True:
    ret, frame = cap.read() #leer el frame, ret es un booleano que indica si se pudo leer el frame
    cv2.imshow("frame", frame) #mostrar el frame en una ventana llamada "frame"
    if cv2.waitKey(1) & 0xFF == ord('q'): #esperar a que se presione la tecla 'q' para salir del bucle
        break