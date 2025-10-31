import cv2
import os
import time
from datetime import datetime
import numpy as np

class VideoRecorder:
    """Grabador de video REAL usando OpenCV"""
    
    def __init__(self, test_name, browser_name, output_dir="videos"):
        self.test_name = test_name
        self.browser_name = browser_name
        self.output_dir = output_dir
        self.video_writer = None
        self.recording = False
        self.frame_size = None
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
    
    def start_recording(self):
        """Iniciar grabación de video REAL"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.filename = f"{self.output_dir}/{self.test_name}_{self.browser_name}_{timestamp}.mp4"
            
            # Inicializar variables
            self.recording = True
            self.frames = []
            
            print(f"🎥 Iniciando grabación de video REAL: {self.filename}")
            
        except Exception as e:
            print(f"❌ Error iniciando grabación: {e}")
    
    def capture_frame(self, driver):
        """Capturar un frame REAL del navegador"""
        if not self.recording:
            return
            
        try:
            # Tomar screenshot y guardar temporalmente
            temp_filename = f"temp_frame_{int(time.time()*1000)}.png"
            driver.save_screenshot(temp_filename)
            
            # Leer la imagen con OpenCV
            frame = cv2.imread(temp_filename)
            
            if frame is not None:
                # Si es el primer frame, configurar el tamaño del video
                if self.frame_size is None:
                    height, width = frame.shape[:2]
                    self.frame_size = (width, height)
                    
                    # Configurar el video writer
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    self.video_writer = cv2.VideoWriter(
                        self.filename, 
                        fourcc, 
                        1.0,  # 1 frame por segundo
                        self.frame_size
                    )
                    print(f"📏 Tamaño de video configurado: {self.frame_size}")
                
                # Escribir frame al video
                self.video_writer.write(frame)
                print(f"📹 Frame escrito al video")
            
            # Eliminar archivo temporal
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        except Exception as e:
            print(f"❌ Error capturando frame: {e}")
    
    def stop_recording(self):
        """Detener grabación y guardar video REAL"""
        if not self.recording or self.video_writer is None:
            print("⚠️  No hay grabación activa para detener")
            return None
            
        try:
            self.recording = False
            
            # Liberar el video writer
            self.video_writer.release()
            
            # Verificar que el archivo se creó
            if os.path.exists(self.filename):
                file_size = os.path.getsize(self.filename)
                print(f"🎥 Video REAL guardado: {self.filename} ({file_size} bytes)")
                return self.filename
            else:
                print("❌ El archivo de video no se creó")
                return None
            
        except Exception as e:
            print(f"❌ Error guardando video: {e}")
            return None