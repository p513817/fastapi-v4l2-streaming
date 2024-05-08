from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import cv2
import base64
import asyncio
from utils.camera import CameraStream

app = FastAPI()
cam = CameraStream()
cam.start()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    return HTMLResponse(content=open("./static/index.html", 'r').read())

@app.websocket("/base64")
async def video_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            frame = cam.read()
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(jpg_as_text)
            await asyncio.sleep(0)
    finally:
        cam.release()
        await websocket.close()

@app.websocket("/bytes")
async def video_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            frame = cam.read()
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0)
    finally:
        cam.release()
        await websocket.close()
