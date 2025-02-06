from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import cv2, os,json
import time
from ultralytics import YOLOWorld

app = FastAPI()

# Cargar modelo YOLO
model = YOLOWorld("yolov8l-worldv2.pt")
model.set_classes(["Hard Hat", "Face masks", "person"])

rtsp_path = 0#"rtsp://admin:admin@192.168.137.45:1935"  

def guardar_resultados(results):
    # Verificar si el archivo ya existe y escribir el encabezado si es necesario
    if not os.path.exists("results.csv"):
        with open("results.csv", "w") as f:
            f.write("id,name,class,confidence,x1,y1,x2,y2,fecha,hora\n")  # Encabezado corregido

    for idx, result in enumerate(results):
        datos_lista = json.loads(result.to_json())  # Ahora es una lista de detecciones
        
        for datos in datos_lista:  # Iterar sobre cada detección en la lista
            name = datos.get("name", "Unknown")
            class_id = datos.get("class", -1)
            confidence = datos.get("confidence", 0.0)
            box = datos.get("box", {})
            fecha = time.strftime("%Y-%m-%d", time.localtime())
            hora = time.strftime("%H:%M:%S", time.localtime())

            x1 = box.get("x1", 0)
            y1 = box.get("y1", 0)
            x2 = box.get("x2", 0)
            y2 = box.get("y2", 0)

            with open("results.csv", "a") as f:
                f.write(f"{idx},{name},{class_id},{confidence},{x1},{y1},{x2},{y2},{fecha},{hora}\n")  # Guardar cada detección


async def capturar_stream(request: Request,path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break  # Si la cámara se desconecta, detener el bucle
        
        # Si el cliente cierra la conexión, detener el streaming
        if await request.is_disconnected():
            print("Cliente desconectado, deteniendo stream.")
            break  

        # Procesar frame con YOLO
        results = model.predict(frame)
        frame = results[0].plot()  # Dibujar detecciones en el frame
        guardar_resultados(results)  # Guardar resultados en un archivo CSV
        # Convertir a JPEG
        _, buffer = cv2.imencode('.jpg', frame)

        # Enviar frame como stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        #time.sleep(1)  # Ajusta el tiempo para mejorar la fluidez
    cap.release()

@app.get("/stream")
async def stream_video(request: Request):
    return StreamingResponse(capturar_stream(request,rtsp_path), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/video")
async def stream_video(request: Request):
    path_video = "videoEPPS.mp4"
    return StreamingResponse(capturar_stream(request,path_video), media_type="multipart/x-mixed-replace; boundary=frame")
