from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import cv2, os,json
import time
from ultralytics import YOLOWorld

# Iniciar la aplicación FastAPI
app = FastAPI()

# Cargar modelo YOLO
model = YOLOWorld("yolov8l-worldv2.pt")
#Cargar Clases del modelo que se quieren detectar
model.set_classes(["Hard Hat", "Face masks", "person"])

rtsp_path = 0#"rtsp://admin:admin@192.168.137.45:1935"  
#En caso de ser una camara RTSP, se debe colocar la dirección de la camara y debe estar en la misma red

def guardar_resultados(results):
    # Verificar si el archivo ya existe y si no existe se crea junto con el encabezado
    if not os.path.exists("results.csv"):
        with open("results.csv", "w") as f:
            f.write("id,name,class,confidence,x1,y1,x2,y2,fecha,hora\n") # Encabezado

    for idx, result in enumerate(results):
        datos_lista = json.loads(result.to_json())  # lista de resultados en formato JSON   
        
        for datos in datos_lista:  # Iterar sobre cada detección en la lista
            #Extraer la información necesaria de las detecciones
            name = datos.get("name", "Unknown")
            class_id = datos.get("class", -1)
            confidence = datos.get("confidence", 0.0)
            box = datos.get("box", {})
            fecha = time.strftime("%Y-%m-%d", time.localtime())
            hora = time.strftime("%H:%M:%S", time.localtime())
            #Coordenadas de la caja delimitadora 
            x1 = box.get("x1", 0)
            y1 = box.get("y1", 0)
            x2 = box.get("x2", 0)
            y2 = box.get("y2", 0)

            # Guardar los datos extraidos en el archivo CSV
            with open("results.csv", "a") as f:
                f.write(f"{idx},{name},{class_id},{confidence},{x1},{y1},{x2},{y2},{fecha},{hora}\n")  


async def capturar_stream(request: Request, path):
    # Iniciar captura de video/ imagen/ camara (dependiendo del path)
    cap = cv2.VideoCapture(path)
    
    while cap.isOpened():
        success, frame = cap.read()
        
        if not success:
            break  # Si no se pudo leer el frame, terminar el streaming
        
        # Si el cliente cierra la conexión, detener el streaming
        if await request.is_disconnected():
            print("Cliente desconectado, deteniendo stream.")
            break  

        # Procesar frame con YOLO
        results = model.predict(frame)
        frame = results[0].plot()  # Dibujar detecciones en el frame
        guardar_resultados(results)  # Guardar resultados en un archivo CSV
        # Convertir frame a formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        # Enviar frame como stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        #time.sleep(1)  # Ajusta el tiempo para mejorar la fluidez
   
    # Liberar recursos
    cap.release()

#Endoints de la API

@app.get("/stream") #captura de video en tiempo real
async def stream_video(request: Request):
    return StreamingResponse(capturar_stream(request,rtsp_path), 
                             media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/video") #captura de video almacenado
async def stream_video(request: Request):
    path_video = "videoEPPS.mp4"
    return StreamingResponse(capturar_stream(request,path_video), 
                             media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/imagen") #captura de imagen almacenada
async def stream_video(request: Request):
    path_imagen = "imagen.jpg"
    return StreamingResponse(capturar_stream(request,path_imagen), 
                             media_type="multipart/x-mixed-replace; boundary=frame")